"""Split a protected page body into chunks on structural boundaries.

Chunks are contiguous substrings of the protected body, so joining them
reproduces the body exactly. Sizes are measured on the restored (original)
text. Breaks happen at blank lines, preferably before a heading; a single
block larger than the limit falls back to line boundaries. Protected
placeholders are never split because they are single tokens.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Callable

_HEADING_RE = re.compile(r"^#{1,6}[ \t]")


@dataclass
class Chunk:
    index: int
    lead: str      # whitespace before the translatable core
    core: str      # text sent to the model
    trail: str     # whitespace after the core

    @property
    def segment_id(self) -> str:
        return f"body.{self.index:03d}"

    @property
    def text(self) -> str:
        return self.lead + self.core + self.trail


def _units(text: str) -> list[str]:
    """Paragraph units: a block of lines plus its trailing blank lines."""
    units: list[str] = []
    current: list[str] = []
    seen_blank = False
    for line in text.splitlines(keepends=True):
        blank = not line.strip()
        starts_heading = bool(_HEADING_RE.match(line))
        if current and ((seen_blank and not blank) or (starts_heading and not seen_blank)):
            units.append("".join(current))
            current, seen_blank = [], False
        current.append(line)
        if blank:
            seen_blank = True
    if current:
        units.append("".join(current))
    return units


def _split_large(unit: str, limit: int, size: Callable[[str], int]) -> list[str]:
    pieces: list[str] = []
    current = ""
    for line in unit.splitlines(keepends=True):
        if current and size(current + line) > limit:
            pieces.append(current)
            current = ""
        current += line
    if current:
        pieces.append(current)
    return pieces


def split_body(text: str, limit: int, size: Callable[[str], int] = len) -> list[Chunk]:
    if size(text) <= limit:
        pieces = [text]
    else:
        units: list[str] = []
        for unit in _units(text):
            units.extend(_split_large(unit, limit, size) if size(unit) > limit else [unit])
        pieces = []
        current = ""
        current_size = 0
        for unit in units:
            unit_size = size(unit)
            heading_break = _HEADING_RE.match(unit) and current_size >= limit * 0.6
            if current and (current_size + unit_size > limit or heading_break):
                pieces.append(current)
                current, current_size = "", 0
            current += unit
            current_size += unit_size
        if current:
            pieces.append(current)
    chunks = []
    for i, piece in enumerate(pieces):
        core = piece.strip()
        if not core:
            chunks.append(Chunk(i, piece, "", ""))
            continue
        start = piece.index(core)
        chunks.append(Chunk(i, piece[:start], core, piece[start + len(core):]))
    return chunks


def heading_levels(text: str) -> list[int]:
    """ATX heading levels of a protected text (code is already placeholders)."""
    return [len(m.group(1)) for m in re.finditer(r"(?m)^(#{1,6})[ \t]", text)]


def table_rows(text: str) -> int:
    return len(re.findall(r"(?m)^[ \t]*\|", text))
