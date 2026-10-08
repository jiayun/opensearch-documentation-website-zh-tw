#!/usr/bin/env python3
"""Preserve upstream notices and verify redistributable website attribution."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
BASELINE = "55880db68ce90d82cf6d83ac9a44bc0fc86a07a2"
MARKER = "Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations."
UPSTREAM_NOTICES = ("LICENSE", "NOTICE", "THIRD-PARTY")
INVENTORY = ROOT / "licenses/inventory.json"


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def original(path: str) -> bytes | None:
    result = subprocess.run(["git", "show", f"{BASELINE}:{path}"], cwd=ROOT,
                            capture_output=True, check=False)
    return result.stdout if result.returncode == 0 else None


def modified_paths() -> list[str]:
    result = subprocess.run(["git", "diff", "--name-only", BASELINE, "--"],
                            cwd=ROOT, capture_output=True, text=True, check=True)
    return result.stdout.splitlines()


def modification_notice(text: str, suffix: str) -> str:
    """Insert a prominent notice without changing YAML data or a shebang."""
    if MARKER in text:
        return text
    if suffix == ".json":
        data = json.loads(text)
        if not isinstance(data, dict):
            raise ValueError("JSON array needs a separate compatible modification-notice strategy")
        data["_translation_notice"] = MARKER
        return json.dumps(data, ensure_ascii=False, indent=2) + "\n"
    if text.startswith("---\n"):
        return "---\n# " + MARKER + "\n" + text[4:]
    if suffix in {".html", ".md", ".markdown", ".svg", ".tpl"}:
        line = "<!-- " + MARKER + " -->\n"
    elif suffix in {".js", ".mjs", ".cjs", ".css", ".scss"}:
        line = "/* " + MARKER + " */\n"
    else:
        line = "# " + MARKER + "\n"
    lines = text.splitlines(keepends=True)
    position = 1 if lines and lines[0].startswith("#!") else 0
    if lines and "frozen_string_literal:" in lines[0]:
        position = 1
    lines.insert(position, line)
    return "".join(lines)


def retained_notices(before: str, after: str) -> list[str]:
    """Keep verbatim copyright/SPDX and embedded complete permission blocks."""
    missing = []
    for line in before.splitlines():
        if re.search(r"Copyright|SPDX-License-Identifier", line) and line.strip() not in after:
            missing.append(line.strip())
    for block in re.findall(r"(?:\{%\s*comment\s*%\}|<!--|/\*)(.*?)(?:\{%\s*endcomment\s*%\}|-->|\*/)", before, re.S):
        if "Permission is hereby granted" in block and block.strip() not in after:
            missing.append("embedded permission and disclaimer text")
    return missing


def check_source(require_modified_notices: bool = False) -> list[str]:
    failures = []
    inventory = json.loads(INVENTORY.read_text())
    for name, expected in inventory["files"].items():
        path = ROOT / "licenses" / name
        if not path.is_file() or digest(path.read_bytes()) != expected:
            failures.append(f"license text missing or changed: licenses/{name}")
    for name in UPSTREAM_NOTICES:
        source = ROOT / name
        copy = ROOT / "licenses" / name
        if not source.is_file() or source.read_bytes() != copy.read_bytes():
            failures.append(f"upstream {name} differs from its retained website copy")
    for name, expected in inventory.get("fonts", {}).items():
        font = ROOT / name
        if not font.is_file() or digest(font.read_bytes()) != expected:
            failures.append(f"original font binary changed or missing: {name}")
    try:
        paths = modified_paths()
    except subprocess.CalledProcessError:
        # CI shallow checkouts still verify all immutable licenses and recorded source docs.
        paths = []
    for name in paths:
        current = ROOT / name
        baseline = original(name)
        if baseline is None:
            continue
        if not current.exists():
            if name in UPSTREAM_NOTICES:
                failures.append(f"upstream notice deleted: {name}")
            continue
        try:
            before = baseline.decode("utf-8")
            after = current.read_text()
        except UnicodeError:
            continue
        if require_modified_notices and MARKER not in after and name not in UPSTREAM_NOTICES:
            failures.append(f"modified upstream file lacks notice: {name}")
        failures.extend(f"{name}: removed notice: {notice}" for notice in retained_notices(before, after))
    return failures


def check_site(destination: Path) -> list[str]:
    failures = []
    inventory = json.loads(INVENTORY.read_text())
    for name, expected in inventory["files"].items():
        path = destination / "licenses" / name
        if not path.is_file() or digest(path.read_bytes()) != expected:
            failures.append(f"built license missing or altered: {path}")
    for name, expected in inventory.get("fonts", {}).items():
        font = destination / name
        if not font.is_file() or digest(font.read_bytes()) != expected:
            failures.append(f"built font binary changed or missing: {name}")
    index = destination / "licenses/index.html"
    if not index.is_file():
        failures.append("built attribution page missing")
    else:
        text = index.read_text()
        for required in ["Copyright OpenSearch contributors.", "社群", "LICENSE", "NOTICE", "THIRD-PARTY"]:
            if required not in text:
                failures.append(f"attribution page missing {required}")
    for page in destination.rglob("*.html"):
        if "pagefind" in page.parts:
            continue
        if page.relative_to(destination).parts[:2] == ("assets", "navigation"):
            continue
        text = page.read_text()
        if '<meta http-equiv="refresh"' in text:
            continue
        if "/licenses/" not in text:
            failures.append(f"page lacks accessible attribution link: {page}")
    return failures


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--site", type=Path)
    parser.add_argument("--require-modified-notices", action="store_true")
    parser.add_argument("--mark", action="store_true", help="add notices to modified existing text files")
    args = parser.parse_args()
    if args.mark:
        for name in modified_paths():
            path = ROOT / name
            if not path.is_file() or name in UPSTREAM_NOTICES or original(name) is None:
                continue
            try:
                before = path.read_text()
            except UnicodeError:
                continue
            path.write_text(modification_notice(before, path.suffix))
    failures = check_source(args.require_modified_notices)
    if args.site:
        failures += check_site(args.site)
    if failures:
        print("\n".join(failures), file=sys.stderr)
        return 1
    print("Upstream and third-party license notices verified.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
