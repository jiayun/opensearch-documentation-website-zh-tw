import threading
import unittest
from test_translation_helpers import FakeProvider

from translation_pipeline.scheduling import RollingScheduler, mixed_batch, review_turn, review_can_run

TIMEOUT = 5


class Tasks:
    """Tasks that block until released, recording starts and peak concurrency."""

    def __init__(self):
        self.lock = threading.Lock()
        self.started = {}
        self.release = {}
        self.calls = []
        self.running = 0
        self.peak = 0

    def gate(self, key):
        with self.lock:
            self.started.setdefault(key, threading.Event())
            return self.release.setdefault(key, threading.Event())

    def __call__(self, key, *args):
        release = self.gate(key)
        with self.lock:
            self.calls.append((key, args))
            self.running += 1
            self.peak = max(self.peak, self.running)
            self.started[key].set()
        try:
            if not release.wait(TIMEOUT):
                raise AssertionError(f"{key} was never released")
            return f"done:{key}"
        finally:
            with self.lock:
                self.running -= 1

    def wait_started(self, key):
        self.gate(key)
        return self.started[key].wait(TIMEOUT)

    def finish(self, key):
        self.gate(key).set()


def wait_for(scheduler, key):
    """Collect completions until key has finished."""
    results = []
    for _ in range(100):
        results += scheduler.wait(TIMEOUT)
        if any(done == key for done, _, _ in results):
            return results
    raise AssertionError(f"{key} did not finish")


class RollingSchedulerTests(unittest.TestCase):
    def setUp(self):
        self.tasks = Tasks()

    def tearDown(self):
        for key in list(self.tasks.release):
            self.tasks.finish(key)

    def test_free_slot_refills_while_slow_task_still_runs(self):
        scheduler = RollingScheduler(self.tasks, max_active=2)
        self.assertEqual(scheduler.submit(['slow', 'fast', 'third']), ['slow', 'fast'])
        self.assertTrue(self.tasks.wait_started('fast'))
        self.tasks.finish('fast')
        self.assertEqual(wait_for(scheduler, 'fast'), [('fast', 'done:fast', None)])

        self.assertEqual(scheduler.submit(['slow', 'third']), ['third'])
        self.assertTrue(self.tasks.wait_started('third'))
        self.assertIn('slow', scheduler.active)
        self.assertFalse(self.tasks.release['slow'].is_set())

        self.tasks.finish('slow')
        self.tasks.finish('third')
        self.assertEqual(sorted(k for k, _, _ in scheduler.drain(TIMEOUT)), ['slow', 'third'])
        self.assertEqual(scheduler.active, [])

    def test_running_key_is_never_scheduled_twice(self):
        scheduler = RollingScheduler(self.tasks, max_active=4)
        self.assertEqual(scheduler.submit(['a', 'a', 'b']), ['a', 'b'])
        self.assertTrue(self.tasks.wait_started('a'))
        self.assertEqual(scheduler.submit(['a', 'b']), [])
        self.assertEqual(scheduler.free_slots(), 2)
        self.tasks.finish('a')
        self.tasks.finish('b')
        scheduler.drain(TIMEOUT)
        self.assertEqual(sorted(k for k, _ in self.tasks.calls), ['a', 'b'])

    def test_finished_key_is_not_rescheduled_before_its_outcome_is_collected(self):
        scheduler = RollingScheduler(self.tasks, max_active=2)
        scheduler.submit(['a'])
        self.tasks.finish('a')
        # Wait for the slot to free without collecting the result.
        with scheduler._cond:
            self.assertTrue(scheduler._cond.wait_for(lambda: not scheduler._active, TIMEOUT))
        self.assertEqual(scheduler.submit(['a']), [])
        self.assertEqual(scheduler.wait(TIMEOUT), [('a', 'done:a', None)])
        self.assertEqual(scheduler.submit(['a']), ['a'])
        scheduler.drain(TIMEOUT)
        self.assertEqual([k for k, _ in self.tasks.calls], ['a', 'a'])

    def test_rolling_refill_never_exceeds_max_active(self):
        keys = [f'p{i}' for i in range(10)]
        for key in keys:
            self.tasks.finish(key)  # tasks run freely; only the cap limits them
        scheduler = RollingScheduler(self.tasks, max_active=4)
        finished = []
        while len(finished) < len(keys):
            pending = [k for k in keys if k not in finished]
            self.assertLessEqual(len(scheduler.submit(pending)), 4)
            self.assertLessEqual(len(scheduler.active), 4)
            finished += [k for k, _, _ in scheduler.wait(TIMEOUT)]
        self.assertLessEqual(self.tasks.peak, 4)
        self.assertEqual(sorted(finished), sorted(keys))
        self.assertEqual(len(self.tasks.calls), len(keys))

    def test_close_stops_dispatch_and_lets_running_task_finish(self):
        scheduler = RollingScheduler(self.tasks, max_active=2)
        self.assertEqual(scheduler.submit(['running']), ['running'])
        self.assertTrue(self.tasks.wait_started('running'))
        scheduler.close()
        self.assertEqual(scheduler.wait(TIMEOUT), [])  # close wakes a waiting supervisor
        self.assertEqual(scheduler.free_slots(), 0)
        self.assertEqual(scheduler.submit(['pending1', 'pending2']), [])
        self.tasks.finish('running')
        self.assertEqual(scheduler.drain(TIMEOUT), [('running', 'done:running', None)])
        self.assertEqual([k for k, _ in self.tasks.calls], ['running'])

    def test_crashed_task_frees_its_slot(self):
        error = RuntimeError('boom')

        def task(key):
            raise error

        scheduler = RollingScheduler(task, max_active=1)
        scheduler.submit(['bad'])
        self.assertEqual(scheduler.drain(TIMEOUT), [('bad', 'error', error)])
        self.assertEqual(scheduler.free_slots(), 1)

    def test_each_dispatch_keeps_its_own_context(self):
        scheduler = RollingScheduler(self.tasks, max_active=2)
        first, second = {'prompt': 1}, {'prompt': 2}
        scheduler.submit(['a'], first)
        scheduler.submit(['b'], second)
        self.tasks.finish('a')
        self.tasks.finish('b')
        scheduler.drain(TIMEOUT)
        self.assertEqual(dict(self.tasks.calls), {'a': (first,), 'b': (second,)})

    def test_idle_wait_times_out_and_wake_returns_early(self):
        scheduler = RollingScheduler(self.tasks, max_active=1)
        self.assertEqual(scheduler.wait(0.01), [])
        scheduler.wake()
        self.assertEqual(scheduler.wait(TIMEOUT), [])

    def test_invalid_capacity(self):
        with self.assertRaises(ValueError):
            RollingScheduler(self.tasks, max_active=0)


class MixedRefillTests(unittest.TestCase):
    def test_existing_translation_can_be_reviewed_without_new_translator(self):
        providers = {'reviewer': FakeProvider('reviewer', 'gemini', lambda p, n: '{}')}
        entry = {'status': 'translated', 'translator': {'providers': [{'family': 'ollama'}]}}
        self.assertTrue(review_can_run(entry, providers, ['reviewer']))
        entry['translator']['providers'][0]['family'] = 'gemini'
        self.assertFalse(review_can_run(entry, providers, ['reviewer']))
    entries = {'r0': {'status': 'translated'}, 'r1': {'status': 'translated'},
               't0': {'status': 'pending'}, 't1': {'status': 'pending'}}

    def test_refill_can_start_with_new_translation(self):
        pages = list(self.entries)
        self.assertEqual(mixed_batch(pages, self.entries, 3, review_first=False), ['t0', 'r0', 't1'])
        self.assertEqual(mixed_batch(pages, self.entries, 3), ['r0', 't0', 'r1'])

    def test_review_turn_balances_in_flight_then_alternates(self):
        self.assertTrue(review_turn([False, False, True], last_was_review=True))
        self.assertFalse(review_turn([True, True, False], last_was_review=False))
        self.assertFalse(review_turn([True, False], last_was_review=True))
        self.assertTrue(review_turn([], last_was_review=False))

    def test_single_slot_refills_interleave_kinds(self):
        reviews = [f'r{i}' for i in range(3)]
        translations = [f't{i}' for i in range(3)]
        entries = {p: {'status': 'translated'} for p in reviews}
        entries.update({p: {'status': 'pending'} for p in translations})
        queue, dispatched, last = reviews + translations, [], False
        while queue:
            page = mixed_batch(queue, entries, 1, review_turn([], last))[0]
            last = entries[page]['status'] == 'translated'
            dispatched.append(page)
            queue.remove(page)
        self.assertEqual(dispatched, ['r0', 't0', 'r1', 't1', 'r2', 't2'])


if __name__ == '__main__':
    unittest.main()
