import json
from pathlib import Path
import unittest
from unittest import mock

from test_translation_helpers import REPO
import translation as cli
from translation_pipeline import providers as P


class GrokTests(unittest.TestCase):
    def test_cli_accepts_grok_alongside_configured_model_providers(self):
        args = cli.build_parser().parse_args([
            'run', '--translator', 'ollama-cloud-glm,agy-flash,grok',
            '--reviewer', 'agy-sonnet,grok', '--dry-run',
        ])
        self.assertEqual(args.translator, ['ollama-cloud-glm', 'agy-flash', 'grok'])
        self.assertEqual(args.reviewer, ['agy-sonnet', 'grok'])

    def test_prompt_file_is_removed_and_tools_are_disabled(self):
        seen = {}
        prompt = '原文; $(do-not-run)\n' * 10000

        def runner(argv, stdin, timeout, name):
            path = Path(argv[argv.index('--prompt-file') + 1])
            seen.update(argv=argv, path=path)
            self.assertNotIn(REPO, path.resolve().parents)
            self.assertEqual(path.read_text(), prompt)
            self.assertEqual(stdin, '')
            self.assertEqual(name, 'grok')
            return 0, json.dumps({'text': '{"approved":true}', 'stopReason': 'end_turn',
                                  'modelUsage': {'grok-4.7-build': {'inputTokens': 3}}}), ''

        reply = P.GrokProvider(runner=runner).complete('SYS', prompt)
        self.assertFalse(seen['path'].exists())
        argv = seen['argv']
        self.assertNotIn(prompt, argv)
        self.assertEqual(argv[argv.index('--tools') + 1], '')
        self.assertEqual(argv[argv.index('--reasoning-effort') + 1], 'low')
        self.assertEqual(argv[argv.index('--deny') + 1], '*')
        self.assertEqual(argv[argv.index('--permission-mode') + 1], 'plan')
        self.assertEqual(argv[argv.index('--system-prompt-override') + 1], 'SYS')
        self.assertIn('--no-subagents', argv)
        self.assertIn('--disable-web-search', argv)
        self.assertNotIn('--always-approve', argv)
        self.assertEqual(reply.model, 'grok-4.7-build')
        self.assertEqual(reply.text, '{"approved":true}')
        self.assertNotEqual(P.GrokProvider().family, P.AgyProvider().family)
        self.assertNotEqual(P.GrokProvider().family, P.ClaudeProvider().family)

    def test_reported_usage_and_estimated_cost_are_separate(self):
        answer, meta = P.parse_grok_envelope(json.dumps({
            'text': '{"segments":[]}', 'stopReason': 'end_turn',
            'usage': {'input_tokens': 12, 'output_tokens': 4}, 'total_cost_usd': 0.03,
        }))
        self.assertEqual(answer, '{"segments":[]}')
        self.assertEqual(meta['usage'], {'input_tokens': 12, 'output_tokens': 4})
        self.assertEqual(meta['estimated'], {'cost_usd': 0.03})
        self.assertNotIn('usage', P.parse_grok_envelope('{"text":"{}"}')[1])

    def test_failures_never_become_successful_reviews(self):
        cases = [
            ('', 'You are not authenticated.', 1, P.AUTH),
            ('{"text":"{}"}', 'quota exceeded; resets in 2h', 1, P.QUOTA),
            ('{"error":"model grok-x is not available"}', '', 0, P.UNAVAILABLE),
            ('{"text":"{}","stopReason":"max_tokens"}', '', 0, P.TRUNCATED),
            ('{"text":"{}","stopReason":"max_turns"}', '', 0, P.TRUNCATED),
            ('{"text":"{}","stopReason":"error"}', '', 0, P.TRANSPORT),
            ('{"text":"{}","stopReason":"tool_use"}', '', 0, P.TRANSPORT),
            ('{"text":"Individual quota reached"}', '', 0, P.QUOTA),
            ('{"text":""}', '', 0, P.TRANSPORT),
            ('[]', '', 0, P.TRANSPORT),
            ('not JSON', '', 0, P.TRANSPORT),
        ]
        for stdout, stderr, code, kind in cases:
            with self.subTest(stdout=stdout, code=code), self.assertRaises(P.ProviderError) as result:
                P.parse_grok_envelope(stdout, stderr, code)
            self.assertEqual(result.exception.kind, kind)

    def test_subscription_workers_remove_xai_api_keys(self):
        with mock.patch.dict('os.environ', {'XAI_API_KEY': 'secret', 'GROK_API_KEY': 'secret'}):
            env = P.scrubbed_env()
        self.assertNotIn('XAI_API_KEY', env)
        self.assertNotIn('GROK_API_KEY', env)
