import unittest
from test_translation_helpers import FakeProvider
from translation_pipeline import config
from translation_pipeline.providers import AgyProvider, ProviderPool, ProviderError, QUOTA


class AgyModelsTests(unittest.TestCase):
    def pool(self):
        providers = {name: FakeProvider(name, 'test', lambda p, count: '{}') for name in config.AGY_MODELS}
        providers['claude'] = FakeProvider('claude', 'claude', lambda p, count: '{}')
        return ProviderPool(providers, clock=lambda: 1000, balance_calls=True)

    def test_model_family_does_not_depend_on_cli(self):
        sonnet = AgyProvider('claude-sonnet-5-5-medium', name='agy-sonnet')
        opus = AgyProvider('claude-opus-5-5-medium', name='agy-opus')
        self.assertEqual(sonnet.family, 'claude')
        self.assertEqual(opus.family, 'claude')
        self.assertNotEqual(AgyProvider().family, 'claude')
        self.assertNotEqual(AgyProvider('gpt-oss-120b-medium').family, 'claude')
        self.assertIn('claude-sonnet-5-5-medium', sonnet.argv('prompt'))

    def test_gemini_quota_does_not_disable_claude_gpt_bucket(self):
        pool = self.pool()
        pool.disable('agy', ProviderError(QUOTA, 'Individual quota reached. Resets in 2h.'))
        self.assertEqual(set(pool.disabled), {'agy', 'agy-flash'})
        self.assertIn('agy-sonnet', pool.available(list(config.AGY_MODELS)))
        self.assertEqual(set(pool.disabled_until.values()), {8260})

    def test_claude_gpt_quota_does_not_disable_gemini_or_direct_claude(self):
        pool = self.pool()
        pool.disable('agy-sonnet', ProviderError(QUOTA, 'Individual quota reached.'))
        self.assertEqual(set(pool.disabled), {'agy-sonnet', 'agy-opus', 'agy-gpt'})
        self.assertEqual(pool.available(['agy', 'agy-flash', 'claude']), ['agy', 'agy-flash', 'claude'])

    def test_large_review_prefers_opus_and_pinned_model_stays_pinned(self):
        pool = self.pool()
        chain = ['agy-sonnet', 'agy-opus', 'agy']
        self.assertEqual(pool._order_chain(chain, 'review', 50000)[0], 'agy-opus')
        self.assertEqual(pool._order_chain(chain, 'review', 1000)[0], 'agy')
        self.assertEqual(pool._order_chain(['agy-sonnet'], 'review', 50000), ['agy-sonnet'])

    def test_gemini_receives_work_while_claude_gpt_bucket_is_cooling(self):
        pool = self.pool()
        pool.providers['codex-review'] = FakeProvider('codex-review', 'codex:model', lambda p, n: '{}')
        pool.disable('agy-sonnet', ProviderError(QUOTA, 'Individual quota reached'))
        chain = ['agy-sonnet', 'agy-opus', 'codex-review', 'agy', 'claude']
        self.assertEqual([pool._order_chain(chain, 'review')[0] for _ in range(3)],
                         ['agy', 'agy', 'codex-review'])
