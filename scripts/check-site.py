#!/usr/bin/env python3
"""Check every rendered internal link, resource and fragment using only stdlib."""
from __future__ import annotations
import argparse
from dataclasses import dataclass, field
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import sys
from urllib.parse import unquote, urljoin, urlsplit

BASE = '/opensearch-documentation-website-zh-tw/3.9'
ORIGIN = 'https://jiayun.github.io'


@dataclass
class Page:
    path: Path
    url: str
    ids: set = field(default_factory=set)
    links: list = field(default_factory=list)
    lang: str | None = None
    canonical: str | None = None
    robots: str = ''
    redirect: bool = False
    indexed: bool = False
    fragment: bool = False


class Parser(HTMLParser):
    def __init__(self, page):
        super().__init__(convert_charrefs=True)
        self.page = page

    def handle_starttag(self, tag, attrs):
        data = dict(attrs)
        if data.get('id'): self.page.ids.add(data['id'])
        if tag == 'a' and data.get('name'): self.page.ids.add(data['name'])
        if tag == 'html': self.page.lang = data.get('lang')
        if 'data-pagefind-body' in data: self.page.indexed = True
        if tag == 'meta':
            if data.get('name', '').lower() == 'robots': self.page.robots = data.get('content', '')
            if data.get('http-equiv', '').lower() == 'refresh': self.page.redirect = True
        if tag == 'link' and 'canonical' in data.get('rel', '').split():
            self.page.canonical = data.get('href')
        if tag in {'a', 'link', 'script', 'img', 'iframe', 'source', 'video', 'audio', 'use'}:
            for attr in ('href', 'src', 'poster', 'xlink:href'):
                value = data.get(attr)
                if value: self.page.links.append(value)
            # Data URI srcsets include commas internally; the other common srcsets are URL+descriptor lists.
            value = data.get('srcset', '')
            if value and not value.startswith('data:'):
                self.page.links.extend(item.strip().split()[0] for item in value.split(',') if item.strip())


def page_url(relative: str, base=BASE) -> str:
    if relative == 'index.html': return base + '/'
    if relative.endswith('/index.html'): relative = relative[:-len('index.html')]
    return base + '/' + relative


def resolve_link(site: Path, source_url: str, href: str, base=BASE):
    """Return local file+decoded fragment; legitimate ../ links resolve normally."""
    parsed = urlsplit(urljoin(ORIGIN + source_url, href))
    if parsed.scheme in {'mailto', 'tel', 'data', 'blob'}: return None
    if parsed.scheme not in {'http', 'https'}: raise ValueError('unsupported link scheme')
    if parsed.netloc != urlsplit(ORIGIN).netloc: return None
    path = unquote(parsed.path)
    if path == base: path += '/'
    if not path.startswith(base + '/'): raise ValueError('same-origin link is outside the repository/version prefix')
    target = (site / path[len(base) + 1:]).resolve()
    if not target.is_relative_to(site.resolve()): raise ValueError('link escapes the site output')
    if target.is_dir(): target /= 'index.html'
    if not target.is_file(): raise ValueError('target file does not exist')
    return target, unquote(parsed.fragment)


def collect(site: Path, base=BASE):
    pages = {}
    for path in site.rglob('*.html'):
        if 'pagefind' in path.relative_to(site).parts: continue
        page = Page(path.resolve(), page_url(path.relative_to(site).as_posix(), base))
        page.fragment = path.relative_to(site).parts[:2] == ('assets', 'navigation')
        Parser(page).feed(path.read_text(encoding='utf-8'))
        pages[page.path] = page
    return pages


def check(site: Path, base=BASE, require_search=True, enforce_metadata=True):
    site = site.resolve()
    failures = []
    if not site.is_dir(): return [('/', 'output', 'site directory missing')]
    pages = collect(site, base)
    def fail(page, href, reason): failures.append((page.url, href, reason))
    for page in pages.values():
        if not page.fragment and page.lang != 'zh-TW': fail(page, 'lang', 'missing or incorrect HTML language')
        if enforce_metadata and not page.redirect and not page.fragment:
            expected = ORIGIN + page.url
            if page.canonical != expected: fail(page, 'canonical', 'canonical URL is not the current page')
            if page.url.endswith(('/search.html', '/404.html')) and 'noindex' not in page.robots:
                fail(page, 'robots', 'search/404 page must be noindex')
        if page.url.endswith(('/search.html', '/404.html')) and page.indexed:
            fail(page, 'search-index', 'search/404 page has a content-index marker')
        for href in page.links:
            if page.fragment and href.startswith('#svg-'): continue
            if 'googletagmanager.com' in href or 'google-analytics.com' in href:
                fail(page, href, 'official analytics dependency')
            try: target = resolve_link(site, page.url, href, base)
            except ValueError as error: fail(page, href, str(error)); continue
            if target is None: continue
            path, fragment = target
            destination = pages.get(path)
            fragment = fragment.split(':~:', 1)[0]
            if fragment and fragment.lower() != 'top' and destination and not destination.redirect and fragment not in destination.ids:
                fail(page, href, 'target fragment does not exist')
    for path in site.rglob('*.js'):
        if 'pagefind' in path.relative_to(site).parts: continue
        if 'search-api.opensearch.org' in path.read_text(encoding='utf-8'):
            failures.append(('/', str(path.relative_to(site)), 'official search API dependency'))
    if require_search and not (site / 'pagefind/pagefind.js').is_file():
        failures.append(('/', 'pagefind', 'static search bundle missing'))
    output_root = site.parent if site.name == '3.9' else site
    total = sum(path.stat().st_size for path in output_root.rglob('*') if path.is_file())
    if total >= 1_000_000_000: failures.append(('/', 'size', 'published website must be smaller than 1 GB'))
    print(f'Checked {len(pages)} HTML pages; artifact {total / 1_000_000:.1f} MB; {len(failures)} findings.')
    return sorted(set(failures))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--site', type=Path, default=Path('_site/3.9'))
    parser.add_argument('--baseline', type=Path)
    parser.add_argument('--record-baseline', type=Path)
    parser.add_argument('--baseline-build', action='store_true', help='collect genuine upstream link failures without localized metadata/search requirements')
    args = parser.parse_args()
    failures = check(args.site, require_search=not args.baseline_build, enforce_metadata=not args.baseline_build)
    if args.baseline_build:
        failures = [f for f in failures if f[1] != 'lang' and f[2] not in {'official search API dependency', 'official analytics dependency'}]
    if args.record_baseline:
        if not args.baseline_build: parser.error('record-baseline requires an unmodified --baseline-build')
        args.record_baseline.parent.mkdir(parents=True, exist_ok=True)
        args.record_baseline.write_text(json.dumps(failures, ensure_ascii=False, indent=2) + '\n')
        print(f'Recorded {len(failures)} upstream link findings in {args.record_baseline}.')
        return 0
    if args.baseline:
        known = set(map(tuple, json.loads(args.baseline.read_text())))
        retained = [finding for finding in failures if finding in known]
        print(f'{len(retained)} exact upstream link findings retained; {len(known - set(failures))} fixed.')
        failures = [finding for finding in failures if finding not in known]
    for finding in failures[:40]: print(f'{finding[0]}: {finding[1]}: {finding[2]}', file=sys.stderr)
    if len(failures) > 40: print(f'... {len(failures) - 40} additional findings.', file=sys.stderr)
    return int(bool(failures))


if __name__ == '__main__': raise SystemExit(main())
