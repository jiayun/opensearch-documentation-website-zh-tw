"""YAML front matter: extract translatable fields and rewrite them surgically.

Visible text is translated: root ``title``, ``description`` and ``summary``,
and, inside nested mappings/lists under any non-structural root (card lists,
``next_steps``, ``flows``...), string values under ``heading``, ``title``,
``description``, ``summary`` or ``text`` plus the string items of ``list``.
Segment IDs are stable paths such as ``fm.more_cards.0.heading`` or
``fm.flows.1.list.2``. Every other value, including ``parent``/``grand_parent``/
``great_grand_parent``, ``permalink``, nav keys, links and images, must parse to
exactly the baseline value afterwards, and list lengths and order stay fixed.
"""

from __future__ import annotations

import copy
import json
import re
from dataclasses import dataclass

import yaml

from .config import (MODIFICATION_NOTICE, ORIGINAL_FM_FIELDS, STRUCTURAL_FM_ROOTS, TRANSLATABLE_FM_FIELDS,
                     TRANSLATABLE_LIST_KEY, TRANSLATABLE_NESTED_KEYS)

_FM_RE = re.compile(r"\A(---[ \t]*\r?\n)(.*?)(\r?\n(?:---|\.\.\.)[ \t]*(?:\r?\n|\Z))", re.S)
# Keys usable in a dotted segment ID; values under other keys are never translated.
_ID_KEY_RE = re.compile(r"^[A-Za-z0-9_-]+$")
_MAX_DEPTH = 8
_MASK = object()


class FrontMatterError(ValueError):
    pass


@dataclass
class Document:
    opening: str      # "---\n"
    raw: str          # YAML text between the delimiters
    closing: str      # "\n---\n"
    body: str
    data: dict

    @property
    def has_front_matter(self) -> bool:
        return bool(self.opening)

    @property
    def newline(self) -> str:
        return "\r\n" if self.opening.endswith("\r\n") else "\n"

    def render(self, raw: str | None = None, body: str | None = None) -> str:
        return self.opening + (self.raw if raw is None else raw) + self.closing + \
            (self.body if body is None else body)


def split_document(text: str) -> Document:
    m = _FM_RE.match(text)
    if not m:
        return Document("", "", "", text, {})
    try:
        data = yaml.safe_load(m.group(2)) or {}
    except yaml.YAMLError as exc:
        raise FrontMatterError(f"invalid YAML front matter: {exc}") from exc
    if not isinstance(data, dict):
        raise FrontMatterError("front matter is not a mapping")
    return Document(m.group(1), m.group(2), m.group(3), text[m.end():], data)


# -- modification notice -------------------------------------------------------------

def has_modification_notice(doc: Document) -> bool:
    return doc.has_front_matter and doc.raw.split("\n", 1)[0].rstrip("\r") == MODIFICATION_NOTICE


def add_modification_notice(text: str) -> str:
    """Insert the modification notice comment after the opening ``---`` (idempotent)."""
    doc = split_document(text)
    if not doc.has_front_matter:
        raise FrontMatterError("page has no front matter for the modification notice")
    if has_modification_notice(doc):
        return text
    return doc.render(raw=MODIFICATION_NOTICE + doc.newline + doc.raw)


# -- translatable fields -----------------------------------------------------------

def original_front_matter(data: dict) -> dict:
    return {k: data[k] for k in ORIGINAL_FM_FIELDS if k in data and data[k] is not None}


def _walk(node, path: tuple, out: dict[str, tuple], depth: int) -> None:
    if depth > _MAX_DEPTH:
        return
    if isinstance(node, list):
        for i, item in enumerate(node):
            if isinstance(item, (dict, list)):
                _walk(item, path + (i,), out, depth + 1)
        return
    if not isinstance(node, dict):
        return
    for key, value in node.items():
        if not isinstance(key, str) or not _ID_KEY_RE.match(key) or key in STRUCTURAL_FM_ROOTS:
            continue
        if isinstance(value, str):
            if key in TRANSLATABLE_NESTED_KEYS and value.strip():
                out[_sid(path + (key,))] = path + (key,)
        elif key == TRANSLATABLE_LIST_KEY and isinstance(value, list):
            for j, item in enumerate(value):
                if isinstance(item, str) and item.strip():
                    out[_sid(path + (key, j))] = path + (key, j)
                elif isinstance(item, (dict, list)):
                    _walk(item, path + (key, j), out, depth + 1)
        elif isinstance(value, (dict, list)):
            _walk(value, path + (key,), out, depth + 1)


def _sid(path: tuple) -> str:
    return "fm." + ".".join(str(p) for p in path)


def field_paths(data: dict) -> dict[str, tuple]:
    """Segment id -> path (keys and list indexes) of every visible string."""
    out: dict[str, tuple] = {}
    for key in TRANSLATABLE_FM_FIELDS:
        value = data.get(key)
        if isinstance(value, str) and value.strip():
            out[f"fm.{key}"] = (key,)
    for key, value in data.items():
        if (isinstance(key, str) and _ID_KEY_RE.match(key) and key not in STRUCTURAL_FM_ROOTS
                and key not in TRANSLATABLE_FM_FIELDS and isinstance(value, (dict, list))):
            _walk(value, (key,), out, 1)
    return out


def _lookup(data, path: tuple) -> tuple[bool, object]:
    node = data
    for part in path:
        if isinstance(part, int) and isinstance(node, list) and 0 <= part < len(node):
            node = node[part]
        elif isinstance(part, str) and isinstance(node, dict) and part in node:
            node = node[part]
        else:
            return False, None
    return True, node


def _assign(data, path: tuple, value) -> None:
    ok, parent = _lookup(data, path[:-1])
    if not ok:
        raise FrontMatterError(f"cannot locate front matter path {_sid(path)}")
    parent[path[-1]] = value


def translatable_fields(data: dict) -> dict[str, str]:
    """Segment id -> source text for visible front matter strings."""
    return {sid: _lookup(data, path)[1] for sid, path in field_paths(data).items()}


def expected_data(data: dict, translations: dict[str, str]) -> dict:
    paths = field_paths(data)
    result = copy.deepcopy(data)
    for seg_id, text in translations.items():
        if not seg_id.startswith("fm."):
            continue
        if seg_id not in paths:
            raise FrontMatterError(f"segment {seg_id} is not a translatable field")
        _assign(result, paths[seg_id], text)
    return result


# -- rewrite -------------------------------------------------------------------------

def _top_level_span(lines: list[str], key: str) -> tuple[int, int] | None:
    """Line range [start, end) holding a top-level key and its value."""
    start = None
    key_re = re.compile(rf"^(['\"]?){re.escape(key)}\1[ \t]*:")
    for i, line in enumerate(lines):
        if key_re.match(line):
            start = i
            break
    if start is None:
        return None
    end = start + 1
    while end < len(lines):
        line = lines[end]
        # Indented lines and column-0 block sequence items belong to the value.
        if line.strip() and not line[0].isspace() and not line.startswith("-"):
            break
        end += 1
    # Leave trailing blank lines where they were.
    while end > start + 1 and not lines[end - 1].strip():
        end -= 1
    return start, end


def rewrite(doc: Document, translations: dict[str, str]) -> str:
    """Return the front matter block with translated fields.

    Only the top-level spans holding a changed field are replaced (scalars as
    one JSON-quoted line, nested roots re-dumped with ``yaml.safe_dump``);
    every other line, including comments, is kept. Raises FrontMatterError
    unless the result parses to exactly the baseline mapping with only the
    translated fields replaced.
    """
    original = translatable_fields(doc.data)
    translations = {k: v for k, v in translations.items() if k.startswith("fm.") and original.get(k) != v}
    if not translations:
        return doc.opening + doc.raw + doc.closing
    target = expected_data(doc.data, translations)
    paths = field_paths(doc.data)
    order = list(doc.data)
    roots = sorted({paths[sid][0] for sid in translations}, key=order.index)
    newline = "\r\n" if "\r\n" in doc.raw else "\n"
    lines = doc.raw.split(newline)
    replacements: list[tuple[int, int, list[str]]] = []
    for root in roots:
        span = _top_level_span(lines, root)
        if span is None:
            raise FrontMatterError(f"cannot locate front matter key {root}")
        if isinstance(target[root], str):
            new_lines = [f"{root}: " + json.dumps(target[root], ensure_ascii=False)]
        else:
            dumped = yaml.safe_dump({root: target[root]}, allow_unicode=True, sort_keys=False,
                                    default_flow_style=False, width=1_000_000)
            new_lines = dumped.rstrip("\n").split("\n")
        replacements.append((span[0], span[1], new_lines))
    for start, end, new_lines in sorted(replacements, reverse=True):
        lines[start:end] = new_lines
    raw = newline.join(lines)
    try:
        parsed = yaml.safe_load(raw) or {}
    except yaml.YAMLError as exc:
        raise FrontMatterError(f"rewritten front matter is invalid YAML: {exc}") from exc
    if parsed != target:
        raise FrontMatterError("rewritten front matter does not match the expected structure")
    return doc.opening + raw + doc.closing


def structural_problems(baseline: dict, current: dict) -> list[str]:
    """Differences outside the baseline's visible text fields.

    Only paths that hold visible text in the baseline are masked; changed
    links, images, list lengths or card order are reported.
    """
    problems = []
    base = copy.deepcopy(baseline)
    cur = copy.deepcopy(current)
    for sid, path in field_paths(baseline).items():
        ok, value = _lookup(cur, path)
        if not ok or not isinstance(value, str) or not value.strip():
            problems.append(f"front matter {sid[3:]} missing or empty")
            continue
        _assign(base, path, _MASK)
        _assign(cur, path, _MASK)
    for key in sorted(set(base) | set(cur), key=str):
        if base.get(key) != cur.get(key):
            problems.append(f"front matter key {key!r} differs from baseline")
    return problems
