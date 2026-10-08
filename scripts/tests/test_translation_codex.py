import json
from pathlib import Path
import sys
import tempfile
import time
import unittest
from unittest import mock

from test_translation_helpers import FakeProvider
from translation_pipeline.providers import (AUTH, QUOTA, CodexProvider, ModelReply,
                                            NoProviderAvailable, ProviderError, ProviderPool,
                                            parse_codex_events)


class CodexTests(unittest.TestCase):
    def test_exec_reads_final_message_and_actual_usage_only(self):
        events = [
            {"type": "thread.started", "thread_id": "example"},
            {"type": "item.completed", "item": {"type": "reasoning", "text": "not the answer"}},
            {"type": "item.completed", "item": {"type": "agent_message", "text": '{"approved":true,"issues":[]}'}},
            {"type": "turn.completed", "usage": {"input_tokens": 3, "output_tokens": 9}},
        ]
        text, meta = parse_codex_events('\n'.join(map(json.dumps, events)))
        self.assertTrue(json.loads(text)["approved"])
        self.assertEqual(meta["usage"], {"input_tokens": 3, "output_tokens": 9})

    def test_codex_quota_event_is_classified(self):
        with self.assertRaises(ProviderError) as result:
            parse_codex_events(json.dumps({"type": "turn.failed", "error": {"message": "usage limit reached"}}))
        self.assertEqual(result.exception.kind, QUOTA)

    def test_subscription_required_and_session_is_read_only(self):
        calls = []
        def runner(args, prompt, timeout, provider):
            calls.append((args, prompt))
            return 0, json.dumps({"type": "item.completed", "item": {"type": "agent_message", "text": '{}'}}), ''
        provider = CodexProvider(runner=runner, budget_reader=lambda: {
            'authType': 'chatgpt',
            'rateLimits': {'secondary': {'usedPercent': 10, 'windowDurationMins': 10080}}})
        provider.complete('system', 'content $(whoami)')
        provider.complete('system', 'second')
        self.assertEqual(sum(args[1] == 'login' for args, _ in calls), 0)
        args, prompt = calls[0]
        self.assertIn('--ignore-user-config', args)
        self.assertIn('read-only', args)
        self.assertNotIn('--dangerously-bypass-approvals-and-sandbox', args)
        self.assertIn('content $(whoami)', prompt)
        self.assertNotIn('$(whoami)', ' '.join(args))
        api = CodexProvider(runner=runner, budget_reader=lambda: {'authType': 'apiKey', 'rateLimits': {}})
        with self.assertRaises(ProviderError) as result: api.complete('s', 'p')
        self.assertEqual(result.exception.kind, AUTH)

    def test_codex_can_join_before_other_tools_exhaust_quota(self):
        agy = FakeProvider('agy', 'agy', lambda p, n: 'agy')
        ollama = FakeProvider('ollama-cloud', 'ollama', lambda p, n: 'ollama')
        codex = FakeProvider('codex', 'codex:gpt-6.1-sol', lambda p, n: 'codex')
        pool = ProviderPool({p.name: p for p in [agy, ollama, codex]}, sleep=lambda _: None)
        self.assertIn('codex', pool.available(['codex']))
        pool.disable('agy', ProviderError(QUOTA, 'quota'))
        self.assertIn('codex', pool.available(['codex']))
        pool.disable('ollama-cloud', ProviderError(QUOTA, 'quota'))
        self.assertEqual(pool.call(['codex'], 's', 'p', 'translate').text, 'codex')

    def test_balanced_calls_include_codex_and_keep_pinned_review(self):
        names = ['claude', 'ollama-cloud', 'ollama-cloud-glm',
                 'codex', 'agy', 'agy-sonnet', 'codex-review']
        providers = {n: FakeProvider(n, n, lambda p, count: '{}') for n in names}
        pool = ProviderPool(providers, balance_calls=True)
        chain = ['ollama-cloud-glm', 'ollama-cloud', 'claude', 'codex', 'agy']
        self.assertEqual([pool._order_chain(chain, 'translate')[0] for _ in range(5)],
                         ['ollama-cloud-glm', 'ollama-cloud', 'ollama-cloud-glm', 'claude', 'codex'])
        review = ['agy-sonnet', 'codex-review', 'agy', 'claude']
        self.assertEqual([pool._order_chain(review, 'review')[0] for _ in range(3)],
                         ['agy-sonnet', 'agy-sonnet', 'codex-review'])
        self.assertEqual(pool._order_chain(['claude'], 'review'), ['claude'])

    def test_codex_translation_and_review_use_distinct_models(self):
        translator = CodexProvider()
        reviewer = CodexProvider('codex-review', 'gpt-6-sol', 'medium')
        self.assertNotEqual(translator.model, reviewer.model)
        self.assertNotEqual(translator.family, reviewer.family)

    def test_workers_stop_before_reserved_weekly_usage(self):
        from translation_pipeline.codex_budget import assess_budget
        for used, allowed in [(10, True), (74, True), (75, False), (80, False), (100, False)]:
            snapshot = {'rateLimits': {'secondary': {'usedPercent': used, 'windowDurationMins': 10080}}}
            self.assertEqual(assess_budget(snapshot)[0], allowed)
        self.assertFalse(assess_budget({'rateLimits': {'secondary': {'usedPercent': 0}}})[0])
        self.assertFalse(assess_budget({'ordinaryUsageAllowed': False, 'rateLimits': {
            'secondary': {'usedPercent': 0, 'windowDurationMins': 10080}}})[0])

    def test_multi_bucket_uses_lowest_remaining(self):
        from translation_pipeline.codex_budget import assess_budget
        snapshot = {'rateLimits': {'secondary': {'usedPercent': 0, 'windowDurationMins': 10080}},
                    'rateLimitsByLimitId': {'other': {'secondary': {
                        'usedPercent': 81, 'windowDurationMins': 10080}}}}
        self.assertFalse(assess_budget(snapshot)[0])

    def test_unavailable_meter_never_starts_inference(self):
        calls = []
        def runner(args, *rest):
            calls.append(args)
            return 0, '', 'Logged in using ChatGPT'
        def unavailable():
            raise RuntimeError('offline')
        provider = CodexProvider(runner=runner, budget_reader=unavailable)
        with self.assertRaises(ProviderError) as result:
            provider.complete('s', 'p')
        self.assertEqual(result.exception.kind, QUOTA)
        self.assertEqual(len(calls), 0)

    def test_agy_explicit_relative_reset(self):
        from translation_pipeline.providers import quota_reset_timestamp
        self.assertEqual(quota_reset_timestamp('Resets in 2h3m37s.', 1000), 8477)
        self.assertEqual(quota_reset_timestamp('Resets in 45m.', 1000), 3760)

    def test_budget_timeout_cleans_launcher_child_holding_stdout(self):
        from translation_pipeline.codex_budget import BudgetUnavailable, read_rate_limits
        with tempfile.TemporaryDirectory() as directory:
            fake = Path(directory) / 'codex'
            fake.write_text('#!' + sys.executable + '\n'
                            'import subprocess,sys,time\n'
                            'subprocess.Popen([sys.executable,"-c","import time; time.sleep(60)"])\n'
                            'time.sleep(60)\n')
            fake.chmod(0o755)
            started = time.monotonic()
            with mock.patch('translation_pipeline.codex_budget.shutil.which', return_value=str(fake)):
                with self.assertRaises(BudgetUnavailable):
                    read_rate_limits(timeout=0.2)
            self.assertLess(time.monotonic() - started, 10)


if __name__ == '__main__': unittest.main()
