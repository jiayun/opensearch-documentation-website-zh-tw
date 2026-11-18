"""Keep zh-TW archive routes while upstream single-edition sections redirect."""
import json
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[2]
RUBY = shutil.which('ruby')
PLUGIN = ROOT / '_plugins/translation_archive.rb'
FIXTURE = Path(__file__).with_name('archive_fixture.rb')


@unittest.skipUnless(RUBY, 'ruby is not installed')
class TranslationArchiveTests(unittest.TestCase):
    def apply(self, data, *, config=None, listed=True, manifest=True, absolute=False, passes=1, url='/', link_checks=None):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            if manifest:
                (root / 'translation').mkdir()
                (root / 'translation/manifest.json').write_text(json.dumps({
                    'pages': {'index.md': {}} if listed else {}}))
            settings = {'translation_archive': True, 'lang': 'zh-TW',
                        'url': 'https://example.test', 'baseurl': '/zh/3.9'}
            settings.update(config or {})
            spec = {'source': str(root), 'config': settings, 'passes': passes, 'link_checks': link_checks or [],
                    'docs': [{'path': str(root / 'index.md') if absolute else 'index.md',
                              'url': url, 'data': data, 'content': '原有中文內容'}]}
            result = subprocess.run([RUBY, '-EUTF-8:UTF-8', str(FIXTURE), str(PLUGIN)],
                                    input=json.dumps(spec), capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            return json.loads(result.stdout)[0]

    def test_single_edition_redirect_stays_a_local_document(self):
        data = {'canonical_url': 'https://docs.opensearch.org/latest/clients/',
                'redirect_to': 'https://docs.opensearch.org/latest/clients/',
                'redirect_from': ['/old-clients/'], 'title': '用戶端'}
        result = self.apply(data)
        self.assertEqual(result['data']['canonical_url'], 'https://example.test/zh/3.9/')
        self.assertEqual(result['data']['upstream_canonical_url'], data['canonical_url'])
        self.assertNotIn('redirect_to', result['data'])
        self.assertEqual(result['data']['redirect_from'], ['/old-clients/'])
        self.assertEqual(result['data']['title'], '用戶端')
        self.assertEqual(result['content'], '原有中文內容')

    def test_absolute_document_path_and_missing_upstream_canonical(self):
        result = self.apply({}, absolute=True)
        self.assertEqual(result['data']['upstream_canonical_url'],
                         'https://docs.opensearch.org/latest/')

    def test_404_warning_links_to_the_upstream_about_page(self):
        result = self.apply({}, url='/404.html')['data']
        self.assertEqual(result['upstream_canonical_url'], 'https://docs.opensearch.org/latest/about/')
        self.assertEqual(result['canonical_url'], 'https://example.test/zh/3.9/404.html')

    def test_latest_root_case_and_fragments_are_recognized(self):
        for destination in ['https://docs.opensearch.org/latest',
                            'https://docs.opensearch.org/latest#section',
                            'HTTPS://DOCS.OPENSEARCH.ORG/latest/']:
            with self.subTest(destination=destination):
                result = self.apply({'redirect_to': destination})['data']
                self.assertNotIn('redirect_to', result)
                self.assertEqual(result['upstream_canonical_url'], destination)

    def test_warning_prefers_the_removed_redirect_target(self):
        result = self.apply({'canonical_url': 'https://docs.opensearch.org/latest/old/',
                             'redirect_to': 'https://docs.opensearch.org/latest/new/'})['data']
        self.assertEqual(result['upstream_canonical_url'], 'https://docs.opensearch.org/latest/new/')

    def test_other_redirect_destinations_are_preserved(self):
        for destination in ['/moved/', 'https://other.test/latest/',
                            'https://docs.opensearch.org/3.9/',
                            'https://docs.opensearch.org/latestish/',
                            'https://docs.opensearch.org.evil.test/latest/',
                            'https://user@docs.opensearch.org/latest/',
                            'https://docs.opensearch.org:444/latest/']:
            with self.subTest(destination=destination):
                self.assertEqual(self.apply({'redirect_to': destination})['data']['redirect_to'], destination)

    def test_non_archive_and_english_sites_are_unchanged(self):
        original = {'canonical_url': 'https://docs.opensearch.org/latest/',
                    'redirect_to': 'https://docs.opensearch.org/latest/'}
        for config in [{'translation_archive': False}, {'lang': 'en-US'}]:
            with self.subTest(config=config):
                self.assertEqual(self.apply(original, config=config)['data'], original)

    def test_unlisted_pages_and_missing_manifest_are_unchanged(self):
        original = {'redirect_to': 'https://docs.opensearch.org/latest/'}
        self.assertEqual(self.apply(original, listed=False)['data'], original)
        self.assertEqual(self.apply(original, manifest=False)['data'], original)

    def test_repeated_hook_preserves_the_original_upstream_target(self):
        canonical = 'https://docs.opensearch.org/latest/different-section/'
        result = self.apply({'canonical_url': canonical, 'redirect_to': canonical}, passes=2)
        self.assertEqual(result['data']['upstream_canonical_url'], canonical)
        self.assertEqual(result['data']['canonical_url'], 'https://example.test/zh/3.9/')

    def test_only_the_explicit_upstream_document_link_bypasses_localization(self):
        canonical = 'https://docs.opensearch.org/latest/version-history/'
        checks = [{'element': 'a', 'attribute': 'href', 'value': canonical},
                  {'element': 'a', 'attribute': 'href', 'value': canonical + '#release'},
                  {'element': 'a', 'attribute': 'href', 'value': 'https://docs.opensearch.org/latest/about/'},
                  {'element': 'img', 'attribute': 'src', 'value': canonical}]
        result = self.apply({'canonical_url': canonical}, link_checks=checks)
        self.assertEqual(result['links'], [True, False, False, False])

    def test_english_and_non_archive_links_keep_the_existing_localization_policy(self):
        canonical = 'https://docs.opensearch.org/latest/version-history/'
        check = [{'element': 'a', 'attribute': 'href', 'value': canonical}]
        for config in [{'translation_archive': False}, {'lang': 'en-US'}]:
            result = self.apply({'upstream_canonical_url': canonical}, config=config, link_checks=check)
            self.assertEqual(result['links'], [False])
