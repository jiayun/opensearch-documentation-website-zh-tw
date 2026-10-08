import json
from pathlib import Path
import tempfile
import unittest
from unittest import mock
from test_translation_helpers import make_repo, MATCH_PAGE, config
from translation_pipeline.pipeline import init
from translation_pipeline.store import Manifest, sha256_bytes
from translation_pipeline.site_source import prepare_source


class SiteSourceTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.commit = make_repo(self.root, {'_docs/a.md': MATCH_PAGE, '_docs/b.md': MATCH_PAGE})
        self.patch = mock.patch.object(config, 'BASELINE_COMMIT', self.commit)
        self.patch.start()
        init(self.root, self.commit)
        self.destination = self.root / '.translation-cache/site-source'

    def tearDown(self):
        self.patch.stop()
        self.tmp.cleanup()

    def reviewed(self, page):
        manifest = Manifest.load(self.root)
        digest = sha256_bytes((self.root / page).read_bytes())
        manifest.update(page, status='reviewed', target_sha256=digest,
                        translated_source_sha256=manifest.pages[page]['source_sha256'],
                        translator={'providers': [{'provider': 'claude', 'model': 'test', 'family': 'claude'}]},
                        reviewer={'provider': 'agy', 'model': 'test', 'family': 'agy', 'approved': True,
                                  'at': 'test', 'target_sha256': digest})

    def test_preview_preserves_reviewed_and_restores_unreviewed_without_mutation(self):
        from translation_pipeline.frontmatter import add_modification_notice
        (self.root / '_docs/a.md').write_text(add_modification_notice(MATCH_PAGE))
        self.reviewed('_docs/a.md')
        (self.root / '_docs/b.md').write_text('unreviewed draft must not reach public site')
        before = (self.root / config.MANIFEST_PATH).read_bytes()
        report = prepare_source(self.root, self.destination)
        self.assertEqual((report['reviewed'], report['english']), (1, 1))
        self.assertEqual((self.destination / '_docs/a.md').read_bytes(), (self.root / '_docs/a.md').read_bytes())
        self.assertEqual((self.destination / '_docs/b.md').read_text(), MATCH_PAGE)
        self.assertEqual((self.root / config.MANIFEST_PATH).read_bytes(), before)
        self.assertIn('unreviewed draft', (self.root / '_docs/b.md').read_text())

    def test_review_hash_mismatch_is_rejected(self):
        self.reviewed('_docs/a.md')
        (self.root / '_docs/a.md').write_text('tampered')
        with self.assertRaisesRegex(ValueError, 'not verified'):
            prepare_source(self.root, self.destination)

    def test_complete_mode_does_not_allow_english_fallback(self):
        with self.assertRaisesRegex(ValueError, 'requires review'):
            prepare_source(self.root, self.destination, 'complete')

    def test_destination_cannot_delete_repository(self):
        with self.assertRaisesRegex(ValueError, 'must not contain'):
            prepare_source(self.root, self.root, 'preview')

    def test_unrelated_destination_files_are_not_deleted(self):
        other = self.root / 'important-files'
        other.mkdir()
        original = other / 'keep.txt'
        original.write_text('keep')
        with self.assertRaisesRegex(ValueError, 'refusing to replace'):
            prepare_source(self.root, other, 'preview')
        self.assertEqual(original.read_text(), 'keep')
