import copy
import json
import unittest

from test_translation_helpers import REPO  # adds scripts to sys.path
from translation_pipeline.frontmatter import add_modification_notice, split_document, translatable_fields
from translation_pipeline.metadata import (METADATA_REVIEW_SCOPE, MetadataOnlyError,
                                            metadata_continuation_problems, migrate_url_metadata)
from translation_pipeline.store import sha256_bytes


class MetadataMigrationTests(unittest.TestCase):
    def source(self, fields='title: Test\nnav_order: 1', body='Text.\n'):
        return f'---\n{fields}\n---\n\n{body}'

    def target(self, source):
        return add_modification_notice(source.replace('title: Test', 'title: "測試"')
                                       .replace('Text.', '既有中文內容。'))

    def test_add_canonical_preserves_reviewed_body_and_visible_fields(self):
        old = self.source()
        new = old.replace('nav_order: 1', 'nav_order: 1\ncanonical_url: https://docs.opensearch.org/latest/test/')
        target = self.target(old)
        result = split_document(migrate_url_metadata(old, new, target))
        self.assertEqual(result.body, split_document(target).body)
        self.assertEqual(result.data['title'], '測試')
        self.assertEqual(result.data['canonical_url'], 'https://docs.opensearch.org/latest/test/')

    def test_redirect_alias_changes_and_additional_redirect_are_copied(self):
        old = self.source('title: Test\nredirect_from:\n  - /old/\n  - /obsolete/')
        new = old.replace('  - /obsolete/', 'redirect_to: https://docs.opensearch.org/latest/test/')
        result = split_document(migrate_url_metadata(old, new, self.target(old)))
        self.assertEqual(result.data['redirect_from'], ['/old/'])
        self.assertEqual(result.data['redirect_to'], 'https://docs.opensearch.org/latest/test/')

    def test_removed_metadata_is_removed_without_changing_prose(self):
        old = self.source('title: Test\nredirect_to: /old/')
        new = self.source('title: Test')
        self.assertNotIn('redirect_to', split_document(migrate_url_metadata(old, new, self.target(old))).data)

    def test_trailing_blank_lines_and_unrelated_comments_are_preserved(self):
        old = self.source('title: Test\n# Copyright Example\nnav_order: 1\n')
        new = old.replace('\n---\n', '\ncanonical_url: https://docs.opensearch.org/latest/test/\n---\n')
        result = migrate_url_metadata(old, new, self.target(old))
        self.assertIn('# Copyright Example', result)
        self.assertEqual(split_document(result).body, split_document(self.target(old)).body)

    def test_prose_title_other_metadata_and_comment_changes_require_full_review(self):
        old = self.source('title: Test\n# Copyright Example\nnav_order: 1')
        changes = [('Text.', 'Different text.'), ('title: Test', 'title: Changed'),
                   ('nav_order: 1', 'nav_order: 2'), ('Copyright Example', 'Copyright Other')]
        for before, after in changes:
            with self.subTest(after=after), self.assertRaises(MetadataOnlyError):
                migrate_url_metadata(old, old.replace(before, after), self.target(old))

    def test_unrecorded_translation_metadata_and_missing_notice_are_rejected(self):
        old = self.source()
        with self.assertRaises(MetadataOnlyError):
            migrate_url_metadata(old, old, self.target(old).replace('nav_order: 1', 'nav_order: 2'))
        with self.assertRaises(MetadataOnlyError):
            migrate_url_metadata(old, old, old)

    def test_legal_notice_inside_a_metadata_span_cannot_be_removed(self):
        old = self.source('title: Test\ncanonical_url: /old/ # Copyright Example')
        new = self.source('title: Test\ncanonical_url: /new/')
        with self.assertRaises(MetadataOnlyError):
            migrate_url_metadata(old, new, self.target(old))


class MetadataContinuationTests(unittest.TestCase):
    def fixture(self):
        old = '---\ntitle: Test\n---\n\nText.\n'
        new = old.replace('title: Test', 'title: Test\ncanonical_url: https://docs.opensearch.org/latest/test/')
        before = add_modification_notice(old.replace('title: Test', 'title: 測試').replace('Text.', '既有中文內容。'))
        after = migrate_url_metadata(old, new, before)
        sha = lambda value: sha256_bytes(value.encode())
        fields = lambda text: sha(json.dumps(translatable_fields(split_document(text).data),
                                             ensure_ascii=False, sort_keys=True))
        prior = {'provider': 'agy', 'model': 'gemini-4-argon-high', 'family': 'agy',
                 'at': '2026-11-01T00:00:00Z', 'approved': True, 'issues': [],
                 'target_sha256': sha(before)}
        migration = {'old_source_sha256': sha(old), 'old_target_sha256': sha(before),
                     'source_body_sha256': sha(split_document(old).body),
                     'target_body_sha256': sha(split_document(before).body),
                     'source_visible_fields_sha256': fields(old),
                     'target_visible_fields_sha256': fields(before)}
        review = {'provider': 'grok', 'model': 'grok-4.7-build-fast', 'family': 'xai:grok',
                  'approved': True, 'issues': [], 'at': '2026-11-18T00:00:00Z',
                  'target_sha256': sha(after), 'scope': METADATA_REVIEW_SCOPE,
                  'metadata_request_sha256': 'f' * 64,
                  'retained_content_review': {'source_sha256': sha(old),
                                              'target_sha256': sha(before), 'review': prior}}
        entry = {'source_sha256': sha(new), 'translated_source_sha256': sha(new),
                 'target_sha256': sha(after), 'translator': {
                     'providers': [{'provider': 'claude', 'model': 'claude-opus-5-5', 'family': 'claude'}],
                     'metadata_migration': migration}, 'reviewer': review}
        return entry, new, after

    def test_valid_continuation_has_hash_bound_independent_content_approval(self):
        entry, source, target = self.fixture()
        self.assertEqual(metadata_continuation_problems(entry, source, target), [])

    def test_missing_retained_approval_or_rejected_prior_review_is_not_publishable(self):
        entry, source, target = self.fixture()
        del entry['reviewer']['retained_content_review']
        self.assertTrue(metadata_continuation_problems(entry, source, target))
        entry, source, target = self.fixture()
        entry['reviewer']['retained_content_review']['review']['approved'] = False
        self.assertTrue(metadata_continuation_problems(entry, source, target))

    def test_prior_same_family_or_wrong_hash_is_rejected(self):
        for key, value in [('family', 'claude'), ('target_sha256', '0' * 64), ('provider', 'unknown')]:
            entry, source, target = self.fixture()
            entry['reviewer']['retained_content_review']['review'][key] = value
            with self.subTest(key=key):
                self.assertTrue(metadata_continuation_problems(entry, source, target))

    def test_metadata_review_cannot_cover_new_prose_or_visible_fields(self):
        entry, source, target = self.fixture()
        for original, changed in [(source.replace('Text.', 'New source.'), target),
                                  (source, target.replace('既有中文內容。', '新的內容。')),
                                  (source, target.replace('title: 測試', 'title: 新標題'))]:
            with self.subTest(changed=changed):
                self.assertTrue(metadata_continuation_problems(entry, original, changed))

    def test_missing_fingerprints_and_request_hash_are_rejected(self):
        entry, source, target = self.fixture()
        del entry['translator']['metadata_migration']['target_visible_fields_sha256']
        self.assertTrue(metadata_continuation_problems(entry, source, target))
        entry, source, target = self.fixture()
        entry['reviewer']['metadata_request_sha256'] = 'not-a-hash'
        self.assertTrue(metadata_continuation_problems(entry, source, target))

    def test_multiple_metadata_updates_lead_back_to_a_complete_content_review(self):
        entry, source, target = self.fixture()
        prior = copy.deepcopy(entry['reviewer'])
        migration = copy.deepcopy(entry['translator']['metadata_migration'])
        retained = {'source_sha256': entry['source_sha256'], 'target_sha256': entry['target_sha256'],
                    'review': prior, 'metadata_migration': migration}
        entry['reviewer']['retained_content_review'] = retained
        entry['translator']['metadata_migration']['old_source_sha256'] = entry['source_sha256']
        entry['translator']['metadata_migration']['old_target_sha256'] = entry['target_sha256']
        self.assertEqual(metadata_continuation_problems(entry, source, target), [])

    def test_a_new_complete_review_can_replace_a_metadata_continuation(self):
        entry, source, target = self.fixture()
        del entry['reviewer']['scope']
        del entry['reviewer']['retained_content_review']
        self.assertEqual(metadata_continuation_problems(entry, source, target.replace('內容', '文字')), [])
