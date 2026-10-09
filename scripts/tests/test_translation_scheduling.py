import unittest
from translation_pipeline.scheduling import mixed_batch

class SchedulingTests(unittest.TestCase):
    def test_review_backlog_does_not_starve_new_translation(self):
        reviews = [f'r{i}' for i in range(30)]
        translations = [f't{i}' for i in range(30)]
        entries = {p: {'status': 'translated'} for p in reviews}
        entries.update({p: {'status': 'pending'} for p in translations})
        batch = mixed_batch(reviews + translations, entries)
        self.assertEqual(len(batch), 25)
        self.assertEqual(batch[:4], ['r0', 't0', 'r1', 't1'])
        self.assertEqual(sum(p.startswith('t') for p in batch), 12)
        self.assertEqual(len(set(batch)), 25)

    def test_empty_and_unbalanced_queues_use_available_work(self):
        self.assertEqual(mixed_batch([], {}), [])
        for status in ['pending', 'translated']:
            entries = {str(i): {'status': status} for i in range(8)}
            self.assertEqual(mixed_batch(list(entries), entries), list(entries))

    def test_queues_preserve_priority_when_one_is_short(self):
        entries = {'r': {'status': 'translated'}, **{str(i): {'status': 'pending'} for i in range(6)}}
        self.assertEqual(mixed_batch(list(entries), entries, 4), ['r', '0', '1', '2'])
