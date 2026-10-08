import unittest
from test_translation_helpers import REPO
from translation_pipeline.checks import compare_translation
from translation_pipeline.frontmatter import add_modification_notice
from translation_pipeline.terms import TermRules


class MarkdownContextTests(unittest.TestCase):
    def test_inline_api_placeholder_cannot_become_raw_html_block(self):
        baseline = '---\ntitle: Test\n---\n\n# Test\n\nThe <HTTP METHOD> <endpoint> request returns fields.\n\n## Permissions\n\nText.\n'
        bad = add_modification_notice(baseline.replace('The <HTTP METHOD>', '<HTTP METHOD>'))
        rules = TermRules.load(REPO / 'translation/banned-terms.yml')
        self.assertTrue(any('HTML block/inline' in p for p in compare_translation(baseline, bad, rules)))
        good = add_modification_notice(baseline.replace('The <HTTP METHOD>', '此 <HTTP METHOD>'))
        self.assertFalse(compare_translation(baseline, good, rules))

    def test_code_fences_and_inline_spans_do_not_trigger_html_block_rule(self):
        baseline = '---\ntitle: Test\n---\n\n# Test\n\nText <span>x</span>.\n\n```html\n<endpoint>\n```\n'
        current = add_modification_notice(baseline.replace('Text <span>', '<span>'))
        self.assertFalse(compare_translation(baseline, current, TermRules.load(REPO / 'translation/banned-terms.yml')))
