"""Keep review backlog moving while giving cloud translation regular work."""
from __future__ import annotations

import threading


def is_review(entry) -> bool:
    return entry.get('status') == 'translated'


def review_can_run(entry, providers, reviewers) -> bool:
    families = {p.get('family') for p in (entry.get('translator') or {}).get('providers', [])}
    return any(providers[name].family not in families for name in reviewers)


def mixed_batch(candidates, entries, limit=25, review_first=True):
    reviews = [page for page in candidates if is_review(entries[page])]
    translations = [page for page in candidates if not is_review(entries[page])]
    queues = [reviews, translations] if review_first else [translations, reviews]
    selected = []
    indexes = [0, 0]
    while len(selected) < limit and any(indexes[i] < len(queues[i]) for i in (0, 1)):
        for i in (0, 1):
            if indexes[i] < len(queues[i]) and len(selected) < limit:
                selected.append(queues[i][indexes[i]])
                indexes[i] += 1
    return selected


def review_turn(active_kinds, last_was_review) -> bool:
    """Whether the next refill should start with a review.

    Balances the in-flight mix; on a tie, alternates with the last dispatch so
    single-slot refills keep interleaving reviews and new translations.
    """
    reviews = sum(1 for kind in active_kinds if kind)
    translations = len(active_kinds) - reviews
    if reviews != translations:
        return reviews < translations
    return not last_was_review


class RollingScheduler:
    """Run at most max_active tasks, refilling a slot as soon as any task ends.

    There is no batch barrier: one slow task never holds the other slots idle.
    A key never runs twice at once; callers decide what to retry and when.
    Completions are collected with wait(); close() stops further dispatch while
    running tasks finish on their own (non-daemon) threads.
    """

    def __init__(self, task, max_active=4):
        if max_active < 1:
            raise ValueError("max_active must be at least 1")
        self._task = task
        self.max_active = max_active
        # Reentrant so wake()/close() are safe from a signal handler that
        # interrupts the owning thread while it holds the lock.
        self._cond = threading.Condition(threading.RLock())
        self._active: dict = {}
        self._done: list = []
        self._woken = False
        self._closed = False

    @property
    def active(self) -> list:
        with self._cond:
            return list(self._active)

    @property
    def closed(self) -> bool:
        return self._closed

    def free_slots(self) -> int:
        with self._cond:
            return 0 if self._closed else self.max_active - len(self._active)

    def submit(self, keys, *args) -> list:
        """Start keys in order until slots run out.

        Skips keys still running or whose result wait() has not returned yet,
        so a caller always sees an outcome before it can retry that key.
        Extra args are passed to the task so each dispatch keeps the context
        it was started with.
        """
        started = []
        with self._cond:
            uncollected = {done[0] for done in self._done}
            for key in keys:
                if self._closed or len(self._active) >= self.max_active:
                    break
                if key in self._active or key in uncollected:
                    continue
                thread = threading.Thread(target=self._run, args=(key, args), name=f"task:{key}")
                self._active[key] = thread
                started.append((key, thread))
        for _, thread in started:
            thread.start()
        return [key for key, _ in started]

    def _run(self, key, args) -> None:
        outcome, error = None, None
        try:
            outcome = self._task(key, *args)
        except BaseException as exc:  # a crashed task must still free its slot
            outcome, error = "error", exc
        finally:
            with self._cond:
                self._active.pop(key, None)
                self._done.append((key, outcome, error))
                self._cond.notify_all()

    def wait(self, timeout=None) -> list:
        """Return finished (key, outcome, error) tuples.

        Blocks up to timeout only when nothing has finished yet; wake() or
        close() end the wait early.
        """
        with self._cond:
            if not self._done and not self._woken:
                self._cond.wait(timeout)
            done, self._done = self._done, []
            self._woken = False
            return done

    def wake(self) -> None:
        with self._cond:
            self._woken = True
            self._cond.notify_all()

    def close(self) -> None:
        """Stop dispatching; tasks already running are left to finish."""
        with self._cond:
            self._closed = True
            self._woken = True
            self._cond.notify_all()

    def drain(self, timeout=None) -> list:
        """Wait for running tasks to finish and return all uncollected results."""
        with self._cond:
            self._cond.wait_for(lambda: not self._active, timeout)
            done, self._done = self._done, []
            return done
