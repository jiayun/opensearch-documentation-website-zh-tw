import unittest
from test_translation_helpers import REPO
from translation_pipeline.pipeline import protected_draft, PageProblems
from translation_pipeline.protect import Protector, tokens_in


class RepairTokensTests(unittest.TestCase):
    def test_repeated_and_nested_tokens_use_original_source_ids(self):
        source = 'Text `x` and `x`.\n\n{% capture example %}\n```json\n{"x": 1}\n```\n{% endcapture %}\n'
        draft = source.replace('Text', '中文').replace(' and ', ' 與 ')
        protector = Protector()
        original = protector.protect_body(source)
        repaired = protected_draft(protector, original, draft)
        self.assertEqual(sorted(tokens_in(original)), sorted(tokens_in(repaired)))
        self.assertEqual(protector.restore(repaired), draft)

    def test_changed_code_is_rejected_instead_of_silently_overwritten(self):
        source = 'Example\n\n```json\n{"x": 1}\n```\n'
        protector = Protector()
        protected = protector.protect_body(source)
        with self.assertRaises(PageProblems):
            protected_draft(protector, protected, source.replace('"x": 1', '"x": 2'))
