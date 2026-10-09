"""Hash-pinned Markdown syntax repairs for malformed upstream baseline sources.

``translation/source-errata.json`` maps the SHA-256 of an entire original
baseline file to exact before/after replacements. A repair applies only when
the whole text hashes to that key, and each ``before`` string must occur
exactly once. The immutable files in ``translation/source/`` are never
changed; ``_plugins/heading_ids.rb`` applies the same file to its baseline.
"""

from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path

from .store import sha256_text

ERRATA_PATH = Path(__file__).resolve().parents[2] / "translation" / "source-errata.json"


@lru_cache(maxsize=None)
def load_errata(path: Path = ERRATA_PATH) -> dict[str, list[tuple[str, str]]]:
    """Errata keyed by source SHA-256; a missing file means no errata."""
    try:
        with open(path, encoding="utf-8") as handle:
            data = json.load(handle)
    except FileNotFoundError:
        return {}
    if data.get("schema_version") != 1 or not isinstance(data.get("errata"), dict):
        raise ValueError(f"{path}: unsupported source errata file")
    errata: dict[str, list[tuple[str, str]]] = {}
    for digest, entry in data["errata"].items():
        replacements = entry.get("replacements") if isinstance(entry, dict) else None
        if (not isinstance(replacements, list) or not replacements or not entry.get("reason")
                or len(digest) != 64 or digest.strip("0123456789abcdef")):
            raise ValueError(f"{path}: malformed erratum {digest!r}")
        pairs = []
        for item in replacements:
            before, after = (item.get("before"), item.get("after")) if isinstance(item, dict) else (None, None)
            if not isinstance(before, str) or not isinstance(after, str) or not before or before == after:
                raise ValueError(f"{path}: malformed replacement in erratum {digest}")
            pairs.append((before, after))
        errata[digest] = pairs
    return errata


def apply_source_errata(text: str, path: Path = ERRATA_PATH) -> str:
    """Return `text` with the errata pinned to its exact hash applied."""
    pairs = load_errata(path).get(sha256_text(text))
    if not pairs:
        return text
    for before, after in pairs:
        count = text.count(before)
        if count != 1:
            raise ValueError(f"source erratum pattern occurs {count} times (expected exactly once): {before!r}")
        text = text.replace(before, after, 1)
    return text
