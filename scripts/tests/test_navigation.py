import importlib.util
from pathlib import Path
import tempfile
import unittest
from html.parser import HTMLParser

SPEC = importlib.util.spec_from_file_location('shared_navigation', Path(__file__).resolve().parents[1] / 'share-navigation.py')
navigation = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(navigation)


class Links(HTMLParser):
    def __init__(self, text):
        super().__init__(); self.urls = []; self.feed(text)
    def handle_starttag(self, tag, attrs):
        if tag == 'a': self.urls.append(dict(attrs).get('href'))


class NavigationTests(unittest.TestCase):
    def test_active_state_does_not_create_duplicate_assets(self):
        first = '<li class="nav-list-item active"><a role="treeitem"aria-current="page"href="/a/" class="nav-list-link active">A</a></li>'
        second = '<li class="nav-list-item"><a role="treeitem"href="/a/" class="nav-list-link">A</a></li>'
        self.assertEqual(navigation.canonical_navigation(first), navigation.canonical_navigation(second))
        self.assertEqual(Links(first).urls, Links(navigation.canonical_navigation(first)).urls)

    def test_all_links_and_body_survive_and_repeated_build_step_is_safe(self):
        with tempfile.TemporaryDirectory() as folder:
            site = Path(folder)
            inner = '<div id="version-panel">3.9</div><ul><li><a href="/docs/a/">A</a></li><li><a href="/docs/b/">B</a></li></ul>'
            source = '<html><nav id="site-nav">' + inner + '</nav><main><pre>  code\n unchanged </pre></main></html>'
            for name in ['a.html', 'b.html']: (site / name).write_text(source)
            navigation.share(site)
            assets = list((site / 'assets/navigation').glob('*.html'))
            self.assertEqual(len(assets), 1)
            self.assertEqual(Links(inner).urls, Links(assets[0].read_text()).urls)
            result = (site / 'a.html').read_text()
            self.assertIn('<main><pre>  code\n unchanged </pre></main>', result)
            self.assertIn('data-navigation-src=', result)
            self.assertIn('<noscript>', result)
            navigation.share(site)
            self.assertEqual((site / 'a.html').read_text(), result)
            self.assertEqual(len(list((site / 'assets/navigation').glob('*.html'))), 1)


if __name__ == '__main__': unittest.main()
