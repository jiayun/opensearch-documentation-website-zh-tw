#!/usr/bin/env python3
"""Serve the built GitHub Pages project at its real repository subpath."""
import argparse
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import unquote, urlsplit

PREFIX = '/opensearch-documentation-website-zh-tw'


class Handler(SimpleHTTPRequestHandler):
    def translate_path(self, path):
        root = Path(self.directory).resolve()
        path = unquote(urlsplit(path).path)
        if path == '/' or path == PREFIX: path = PREFIX + '/'
        if not path.startswith(PREFIX + '/'): return str(root / '__missing__')
        target = (root / path[len(PREFIX) + 1:]).resolve()
        return str(target if target.is_relative_to(root) else root / '__missing__')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--site', type=Path, default=Path('_site'))
    parser.add_argument('--port', type=int, default=4000)
    args = parser.parse_args()
    if not (args.site / '3.9/index.html').is_file(): parser.error('build the website first')
    print(f'Preview: http://127.0.0.1:{args.port}{PREFIX}/3.9/', flush=True)
    ThreadingHTTPServer(('127.0.0.1', args.port), partial(Handler, directory=str(args.site.resolve()))).serve_forever()
