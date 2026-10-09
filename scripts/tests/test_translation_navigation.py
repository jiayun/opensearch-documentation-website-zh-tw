"""Runs the real Jekyll navigation generator through stdlib-only Ruby stand-ins."""
from collections import Counter
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[2]
FIXTURE = Path(__file__).with_name('navigation_fixture.rb')
RUBY = shutil.which('ruby')
BASE = '55880db68ce90d82cf6d83ac9a44bc0fc86a07a2'
FIELDS = ['title', 'parent', 'grand_parent', 'great_grand_parent']


def run_fixture(*args):
    proc = subprocess.run([RUBY, '-EUTF-8:UTF-8', str(FIXTURE), *args], capture_output=True, text=True, encoding='utf-8')
    if proc.returncode:
        raise AssertionError(proc.stderr)
    return json.loads(proc.stdout)


def entry(*ancestry, status='reviewed', sha='0' * 64):
    return {'status': status, 'source_sha256': sha,
            'original_front_matter': {f: v for f, v in zip(FIELDS, ancestry) if v is not None}}


def ancestry_key(fm, start):
    return tuple(fm.get(f) for f in FIELDS[start:]) + (None,) * start


@unittest.skipUnless(RUBY, 'ruby is not installed')
class TranslationNavigationTests(unittest.TestCase):
    def generate(self, pages, titles, aliases=None, sources=None, config=None):
        """pages: path -> manifest entry; titles: path -> (collection, current title)."""
        folder = tempfile.TemporaryDirectory()
        self.addCleanup(folder.cleanup)
        root = Path(folder.name)
        (root / 'translation').mkdir()
        (root / 'translation/manifest.json').write_text(json.dumps({'baseline_commit': BASE, 'pages': pages}))
        if aliases is not None:
            (root / 'translation/navigation-aliases.json').write_text(json.dumps(aliases))
        for path, data in (sources or {}).items():
            target = root / 'translation/source' / path
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(data)
        docs = [{'path': p, 'collection': c, 'data': {'title': t}} for p, (c, t) in titles.items()]
        spec = root / 'spec.json'
        spec.write_text(json.dumps({'source': str(root), 'config': config or {}, 'docs': docs}))
        return run_fixture(str(spec))

    def test_exact_ancestor_beats_duplicate_title_fallback(self):
        pages = {'_c/a.md': entry('A'), '_c/b.md': entry('B'), '_c/a/group.md': entry('Group', 'A'),
                 '_c/b/group.md': entry('Group', 'B'), '_c/a/leaf.md': entry('Leaf', 'Group', 'A')}
        titles = {'_c/a.md': ('c', '甲'), '_c/b.md': ('c', '乙'), '_c/a/group.md': ('c', '甲群組'),
                  '_c/b/group.md': ('c', '乙群組'), '_c/a/leaf.md': ('c', '葉')}
        result = self.generate(pages, titles)
        self.assertTrue(result['ok'], result.get('error'))
        leaf = result['docs']['_c/a/leaf.md']['data']
        self.assertEqual((leaf['parent'], leaf['grand_parent']), ('甲群組', '甲'))

    def test_duplicate_titles_reject_ragged_parent(self):
        pages = {'_c/a.md': entry('A'), '_c/b.md': entry('B'), '_c/a/group.md': entry('Group', 'A'),
                 '_c/b/group.md': entry('Group', 'B'), '_c/leaf.md': entry('Leaf', 'Group')}
        titles = {'_c/a.md': ('c', '甲'), '_c/b.md': ('c', '乙'), '_c/a/group.md': ('c', '甲群組'),
                  '_c/b/group.md': ('c', '乙群組'), '_c/leaf.md': ('c', '葉')}
        result = self.generate(pages, titles)
        self.assertFalse(result['ok'])
        self.assertIn('Missing translated parent for _c/leaf.md', result['error'])
        self.assertIn('ambiguous', result['error'])

    def test_unique_same_collection_title_resolves_ragged_parent(self):
        pages = {'_dashboards/index.md': entry('OpenSearch Dashboards'),
                 '_dashboards/visualize/index.md': entry('Building data visualizations'),
                 '_dashboards/visualize/editor.md': entry('Creating visualizations using queries',
                                                          'Building data visualizations', 'OpenSearch Dashboards')}
        titles = {'_dashboards/index.md': ('dashboards', 'OpenSearch Dashboards 總覽'),
                  '_dashboards/visualize/index.md': ('dashboards', '建立資料視覺化'),
                  '_dashboards/visualize/editor.md': ('dashboards', '使用查詢建立視覺化')}
        result = self.generate(pages, titles)
        self.assertTrue(result['ok'], result.get('error'))
        editor = result['docs']['_dashboards/visualize/editor.md']['data']
        self.assertEqual((editor['parent'], editor['grand_parent']), ('建立資料視覺化', 'OpenSearch Dashboards 總覽'))

    def test_cross_collection_exact_key_must_be_unique(self):
        pages = {'_observing-your-data/index.md': entry('Observability'),
                 '_dashboards/plugins.md': entry('Integrating plugins', 'Observability')}
        titles = {'_observing-your-data/index.md': ('observing-your-data', '可觀測性'),
                  '_dashboards/plugins.md': ('dashboards', '整合外掛程式')}
        result = self.generate(pages, titles)
        self.assertTrue(result['ok'], result.get('error'))
        self.assertEqual(result['docs']['_dashboards/plugins.md']['data']['parent'], '可觀測性')
        pages['_other/index.md'] = entry('Observability')
        titles['_other/index.md'] = ('other', '其他可觀測性')
        result = self.generate(pages, titles)
        self.assertFalse(result['ok'])
        self.assertIn('ambiguous across 2 collections', result['error'])

    def alias_site(self, alias_overrides=(), source=b'---\ntitle: User-defined search processors\n---\n',
                   include_target_doc=True, aliases=True):
        sha = hashlib.sha256(b'---\ntitle: User-defined search processors\n---\n').hexdigest()
        target = '_search-plugins/sp.md'
        pages = {'_search-plugins/index.md': entry('Search pipelines'),
                 target: entry('User-defined search processors', 'Search pipelines', sha=sha),
                 '_search-plugins/agentic.md': entry('Agentic context', 'Search processors', 'Search pipelines')}
        titles = {'_search-plugins/index.md': ('search-plugins', '搜尋管線'),
                  '_search-plugins/agentic.md': ('search-plugins', '代理式內容')}
        if include_target_doc:
            titles[target] = ('search-plugins', '使用者定義的搜尋處理器')
        alias = {'collection': 'search-plugins', 'ancestry': ['Search processors', 'Search pipelines', None, None],
                 'target': target, 'target_original_title': 'User-defined search processors', 'target_source_sha256': sha}
        alias.update(dict(alias_overrides))
        data = {'baseline_commit': BASE, 'aliases': [alias]} if aliases else None
        return self.generate(pages, titles, data, {target: source} if source is not None else {})

    def test_alias_maps_renamed_parent_to_real_target_title(self):
        result = self.alias_site()
        self.assertTrue(result['ok'], result.get('error'))
        agentic = result['docs']['_search-plugins/agentic.md']['data']
        self.assertEqual((agentic['parent'], agentic['grand_parent']), ('使用者定義的搜尋處理器', '搜尋管線'))
        result = self.alias_site(aliases=False)
        self.assertFalse(result['ok'])
        self.assertIn('not found', result['error'])

    def test_alias_rejects_absent_or_changed_target(self):
        cases = {
            'target not in manifest': {'alias_overrides': {'target': '_search-plugins/missing.md'}},
            'target original title changed': {'alias_overrides': {'target_original_title': 'Search processors'}},
            'target manifest source hash changed': {'alias_overrides': {'target_source_sha256': 'f' * 64}},
            'target baseline source missing or changed': {'source': None},
            'target document missing from collection': {'include_target_doc': False},
            'unsafe target path': {'alias_overrides': {'target': '../x.md'}},
        }
        for problem, kwargs in cases.items():
            with self.subTest(problem):
                result = self.alias_site(**kwargs)
                self.assertFalse(result['ok'])
                self.assertIn('Invalid navigation alias', result['error'])
                self.assertIn(problem, result['error'])
        with self.subTest('changed baseline source bytes'):
            result = self.alias_site(source=b'---\ntitle: Changed\n---\n')
            self.assertFalse(result['ok'])
            self.assertIn('target baseline source missing or changed', result['error'])

    def test_renamed_parent_uses_its_current_branch_for_child_navigation(self):
        source = b'---\ntitle: Comparing single queries\n---\n'
        target = '_search-plugins/compare.md'
        pages = {'_search-plugins/index.md': entry('Quality'),
                 '_search-plugins/workbench.md': entry('Workbench', 'Quality'),
                 target: entry('Comparing single queries', 'Workbench', 'Quality',
                               sha=hashlib.sha256(source).hexdigest()),
                 '_search-plugins/stats.md': entry('Stats API', 'Compare Search Results', 'Quality')}
        titles = {'_search-plugins/index.md': ('search-plugins', '品質'),
                  '_search-plugins/workbench.md': ('search-plugins', '工作台'),
                  target: ('search-plugins', '比較單一查詢'),
                  '_search-plugins/stats.md': ('search-plugins', '統計 API')}
        aliases = {'baseline_commit': BASE, 'aliases': [{
            'collection': 'search-plugins', 'ancestry': ['Compare Search Results', 'Quality', None, None],
            'target': target, 'target_original_title': 'Comparing single queries',
            'target_source_sha256': hashlib.sha256(source).hexdigest()}]}
        result = self.generate(pages, titles, aliases, {target: source})
        self.assertTrue(result['ok'], result.get('error'))
        child = result['docs']['_search-plugins/stats.md']['data']
        self.assertEqual((child['parent'], child['grand_parent'], child['great_grand_parent']),
                         ('比較單一查詢', '工作台', '品質'))

    def test_mixed_preview_uses_actual_titles_and_only_warns(self):
        pages = {'_c/index.md': entry('Root'), '_c/english.md': entry('English section', status='pending'),
                 '_c/child.md': entry('Child', 'Root', status='pending'),
                 '_c/reviewed.md': entry('Reviewed', 'English section'),
                 '_c/orphan.md': entry('Orphan', 'Gone', status='pending')}
        titles = {'_c/index.md': ('c', '根'), '_c/english.md': ('c', 'English section'), '_c/child.md': ('c', 'Child'),
                  '_c/reviewed.md': ('c', '已校對'), '_c/orphan.md': ('c', 'Orphan')}
        result = self.generate(pages, titles, config={'translation_preview': True})
        self.assertTrue(result['ok'], result.get('error'))
        docs = {p: d['data'] for p, d in result['docs'].items()}
        self.assertEqual((docs['_c/child.md']['parent'], docs['_c/child.md']['translation_language']), ('根', 'en'))
        self.assertEqual((docs['_c/reviewed.md']['parent'], docs['_c/reviewed.md']['translation_language']),
                         ('English section', 'zh-TW'))
        self.assertNotIn('parent', docs['_c/orphan.md'])
        self.assertTrue(any('Missing translated parent for _c/orphan.md' in w for w in result['warnings']))

    def test_full_corpus_resolves_every_inconsistent_upstream_ancestry(self):
        result = run_fixture('--corpus', str(ROOT))
        self.assertTrue(result['ok'], result.get('error'))
        manifest = json.loads((ROOT / 'translation/manifest.json').read_text(encoding='utf-8'))['pages']
        aliases = json.loads((ROOT / 'translation/navigation-aliases.json').read_text(encoding='utf-8'))['aliases']
        docs = result['docs']
        meta = {p: (d['collection'] or 'none', manifest[p]['original_front_matter']) for p, d in docs.items()}
        exact = {(c, ancestry_key(fm, 0)) for c, fm in meta.values() if fm.get('title') is not None}
        alias_targets = {(a['collection'], tuple(a['ancestry'])): a['target'] for a in aliases}
        kinds = Counter()
        for path, (col, fm) in sorted(meta.items()):
            for i, field in enumerate(FIELDS[1:], 1):
                key = ancestry_key(fm, i)
                if fm.get(field) is None or (col, key) in exact:
                    continue
                if (col, key) in alias_targets:
                    kind, targets = 'alias', [alias_targets[(col, key)]]
                else:
                    targets = [p for p, (c, f) in meta.items() if c == col and f.get('title') == key[0]]
                    kind = 'local'
                    if not targets:
                        kind = 'cross'
                        targets = [p for p, (c, f) in meta.items() if c != col and ancestry_key(f, 0) == key]
                kinds[kind] += 1
                with self.subTest(path=path, field=field, key=key):
                    self.assertEqual(len(targets), 1, targets)
                    self.assertEqual(docs[path]['data'][field], docs[targets[0]]['data']['title'])
        self.assertEqual(dict(kinds), {'local': 68, 'cross': 1, 'alias': 3})
        title = lambda p: docs[p]['data']['title']
        self.assertEqual(docs['_dashboards/dashboard/plugins-dashboards.md']['data']['parent'], title('_observing-your-data/index.md'))
        for page in ['agentic-context-processor.md', 'agentic-query-translator-processor.md']:
            self.assertEqual(docs['_search-plugins/search-pipelines/' + page]['data']['parent'],
                             title('_search-plugins/search-pipelines/search-processors.md'))
        self.assertEqual(docs['_search-plugins/search-relevance/stats-api.md']['data']['parent'],
                         title('_search-plugins/search-relevance/compare-search-results.md'))


if __name__ == '__main__':
    unittest.main()
