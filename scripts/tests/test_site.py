import importlib.util
import json
from pathlib import Path
import sys
import tempfile
import unittest

SPEC = importlib.util.spec_from_file_location('site_checker', Path(__file__).resolve().parents[1] / 'check-site.py')
checker = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = checker
SPEC.loader.exec_module(checker)


class TestSite(unittest.TestCase):
    def setUp(self):
        self.folder = tempfile.TemporaryDirectory()
        self.site = Path(self.folder.name)
        for name in ['assets', 'api', 'pagefind']:
            (self.site / name).mkdir()
        (self.site / 'assets/site.css').write_text('body{}')
        (self.site / 'pagefind/pagefind.js').write_text('export const search = () => {};')
        self.write_page('index.html', '<h1 id="intro">首頁</h1>')
        self.write_page('api/index.html', '<h1 id="索引">API</h1>')

    def tearDown(self):
        self.folder.cleanup()

    def write_page(self, name, body, lang='zh-TW', canonical=None, extra=''):
        canonical = canonical or checker.ORIGIN + checker.page_url(name)
        text = f'<html lang="{lang}"><head><link rel="canonical" href="{canonical}">{extra}</head><body>{body}</body></html>'
        (self.site / name).write_text(text)

    def test_relative_parent_assets_are_valid(self):
        self.write_page('api/index.html', '<link rel="stylesheet" href="../assets/site.css"><a href="../#intro">首頁</a>')
        self.assertEqual([], checker.check(self.site))

    def test_encoded_fragment_and_query_are_valid(self):
        self.write_page('index.html', '<a href="api/?q=foo#%E7%B4%A2%E5%BC%95">索引</a>')
        self.assertEqual([], checker.check(self.site))

    def test_missing_target_and_fragment_are_rejected(self):
        self.write_page('index.html', '<a href="missing/">bad</a><a href="api/#missing">bad</a>')
        findings = checker.check(self.site)
        self.assertTrue(any('file does not exist' in f[2] for f in findings))
        self.assertTrue(any('fragment does not exist' in f[2] for f in findings))

    def test_wrong_repository_prefix_is_rejected(self):
        self.write_page('index.html', '<script src="/latest/assets/app.js"></script>')
        self.assertTrue(any('outside' in f[2] for f in checker.check(self.site)))

    def test_external_community_link_is_not_an_internal_failure(self):
        self.write_page('index.html', '<a href="https://forum.opensearch.org/">Forum</a>')
        self.assertEqual([], checker.check(self.site))

    def test_missing_language_and_wrong_canonical_are_rejected(self):
        self.write_page('index.html', '', lang='en', canonical='https://docs.opensearch.org/latest/')
        self.assertEqual(2, len(checker.check(self.site)))

    def test_unsafe_link_scheme_is_rejected(self):
        self.write_page('index.html', '<a href="javascript:alert(1)">bad</a>')
        self.assertTrue(any('scheme' in f[2] for f in checker.check(self.site)))

    def test_search_api_in_script_is_rejected(self):
        (self.site / 'assets/search.js').write_text('fetch("https://search-api.opensearch.org/search")')
        self.assertTrue(any('search API' in f[2] for f in checker.check(self.site)))

    def test_search_and_404_require_noindex_and_are_not_indexed(self):
        self.write_page('search.html', '<div data-pagefind-body>wrong</div>')
        findings = checker.check(self.site)
        self.assertTrue(any('noindex' in f[2] for f in findings))
        self.assertTrue(any('content-index' in f[2] for f in findings))

    def test_alias_redirect_may_have_target_canonical(self):
        self.write_page('alias.html', '', canonical=checker.ORIGIN + checker.BASE + '/api/', extra='<meta http-equiv="refresh" content="0; url=/api/">')
        self.assertEqual([], checker.check(self.site))


if __name__ == '__main__': unittest.main()
