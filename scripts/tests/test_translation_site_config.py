"""Keep translated navigation aligned with upstream collection removals."""
from pathlib import Path
import unittest

import yaml


ROOT = Path(__file__).resolve().parents[2]


class TranslationSiteConfigTests(unittest.TestCase):
    def test_translated_navigation_references_existing_output_collections(self):
        upstream = yaml.safe_load((ROOT / '_config.yml').read_text())
        translated = yaml.safe_load((ROOT / '_config.zh-tw.yml').read_text())
        for group, settings in translated.items():
            if not group.endswith('_collection'):
                continue
            for collection in settings['collections']:
                with self.subTest(group=group, collection=collection):
                    # Jekyll merges nested mappings, so a stale translated entry
                    # would restore a navigation item removed by upstream.
                    self.assertIn(collection, upstream[group]['collections'])
                    self.assertTrue(upstream['collections'][collection]['output'])
                    self.assertTrue(any((ROOT / f'_{collection}').rglob('*.md')))
