#!/usr/bin/env python3
"""Deduplicate navigation markup, preserving every existing link and tree node."""
import argparse
import hashlib
from pathlib import Path
import re

BASE = '/opensearch-documentation-website-zh-tw/3.9'
NAV = re.compile(r'(<nav\b[^>]*id="site-nav"[^>]*>)(.*?)(</nav>)', re.S)


def canonical_navigation(markup):
    markup = re.sub(r'class="([^"]*)"', lambda m: 'class="' + ' '.join(c for c in m[1].split() if c not in {'active', 'in-category'}) + '"', markup)
    markup = re.sub(r'\s*aria-current="[^"]*"', '', markup)
    markup = re.sub(r'aria-expanded="true"', 'aria-expanded="false"', markup)
    return markup.strip()


def share(site):
    asset_dir = site / 'assets/navigation'
    asset_dir.mkdir(parents=True, exist_ok=True)
    trees = {}
    saved = pages = 0
    for path in site.rglob('*.html'):
        if path.is_relative_to(asset_dir) or 'pagefind' in path.parts: continue
        source = path.read_text()
        match = NAV.search(source)
        if not match or 'data-navigation-src=' in match[1]: continue
        tree = canonical_navigation(match[2])
        key = hashlib.sha256(tree.encode()).hexdigest()[:24]
        if key not in trees:
            (asset_dir / (key + '.html')).write_text(tree)
            trees[key] = tree
        href = BASE + '/assets/navigation/' + key + '.html'
        # Keep the category/version panel in the initial HTML as an immediate fallback.
        panel = tree.split('</div>', 1)[0] + '</div>' if tree.lstrip().startswith('<div') else ''
        fallback = panel + '<p class="text-small" data-nav-loading>文件導覽載入中…</p><noscript><p><a href="' + href + '">開啟完整文件導覽</a></p></noscript>'
        opening = match[1][:-1] + ' data-navigation-src="' + href + '">'
        replacement = opening + fallback + match[3]
        target = source[:match.start()] + replacement + source[match.end():]
        saved += len(source.encode()) - len(target.encode())
        pages += 1
        path.write_text(target)
    print(f'Shared navigation: {pages} pages, {len(trees)} trees, saved {saved / 1_000_000:.1f} MB.')
    if pages and len(trees) > 40:
        raise RuntimeError('navigation trees did not deduplicate sufficiently; inspect page-specific state')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--site', type=Path, default=Path('_site/3.9'))
    share(parser.parse_args().site)
