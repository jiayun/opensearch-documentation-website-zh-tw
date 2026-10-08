#!/usr/bin/env python3
"""Repair unambiguous upstream link typos in HTML, preserving Markdown sources."""
import argparse
import html
import importlib.util
from pathlib import Path
import re
import sys
from urllib.parse import urlsplit, urlunsplit

SPEC = importlib.util.spec_from_file_location('built_site_checker', Path(__file__).with_name('check-site.py'))
checker = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = checker
SPEC.loader.exec_module(checker)


def repair_href(site, source_url, href, pages):
    parsed = urlsplit(href)
    if parsed.scheme and (parsed.scheme not in ('http', 'https') or parsed.netloc != 'jiayun.github.io'):
        return href
    raw_path = parsed.path
    candidates = [href]
    if raw_path and not raw_path.startswith(checker.BASE + '/'):
        rooted = checker.BASE + '/' + raw_path.lstrip('/')
        candidates.append(urlunsplit(('', '', rooted, parsed.query, parsed.fragment)))
        if '/security-plugin/' in rooted:
            rooted = rooted.replace('/security-plugin/', '/security/', 1)
            candidates.append(urlunsplit(('', '', rooted, parsed.query, parsed.fragment)))
        if rooted.endswith('/index/'):
            candidates.append(urlunsplit(('', '', rooted[:-len('index/')], parsed.query, parsed.fragment)))
    for candidate in candidates:
        try: target = checker.resolve_link(site, source_url, candidate)
        except ValueError: continue
        if target is None: return href
        path, fragment = target
        page = pages.get(path)
        if fragment and page and not page.redirect:
            possible = fragment.lstrip('#')
            if possible not in page.ids and possible.lower() in page.ids: possible = possible.lower()
            if possible in page.ids and possible != fragment:
                value = urlsplit(candidate)
                candidate = urlunsplit((value.scheme, value.netloc, value.path, value.query, possible))
        return candidate
    return href


class Rewriter(checker.HTMLParser):
    def __init__(self, source, transform):
        super().__init__(convert_charrefs=False)
        self.source = source; self.transform = transform; self.edits = []
        self.lines = [0]
        for match in re.finditer('\n', source): self.lines.append(match.end())

    def handle_starttag(self, tag, attrs):
        if tag not in ('a', 'img', 'script', 'link', 'iframe', 'source'): return
        original = self.get_starttag_text()
        def replace(match):
            value = html.unescape(match[3])
            target = self.transform(value)
            return match[0] if target == value else match[1] + match[2] + html.escape(target, quote=True) + match[2]
        changed = re.sub(r'(\b(?:href|src)\s*=\s*)(["\'])(.*?)\2', replace, original, flags=re.S)
        if changed != original:
            line, column = self.getpos()
            start = self.lines[line - 1] + column
            self.edits.append((start, start + len(original), changed))

    def rewrite(self):
        self.feed(self.source)
        text = self.source
        for start, end, replacement in reversed(self.edits): text = text[:start] + replacement + text[end:]
        return text


def run(site):
    site = site.resolve(); pages = checker.collect(site); changes = 0
    for page in pages.values():
        source = page.path.read_text()
        rewrite = Rewriter(source, lambda href: repair_href(site, page.url, href, pages))
        target = rewrite.rewrite()
        if target != source:
            page.path.write_text(target); changes += len(rewrite.edits)
    print(f'Repaired {changes} unambiguous generated HTML link attributes.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--site', type=Path, default=Path('_site/3.9'))
    run(parser.parse_args().site)
