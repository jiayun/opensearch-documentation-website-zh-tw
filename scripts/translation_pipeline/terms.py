"""Terminology check for Mainland China vocabulary and simplified characters.

Only prose is checked: fenced code, inline code, Liquid, URLs, HTML and other
protected regions are removed first. A term occurrence is ignored when it
lies inside one of its listed exception phrases (for example, 支持向量機).
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path

import yaml

from .protect import prose_only


@dataclass
class Term:
    term: str
    preferred: str
    severity: str = "error"
    exceptions: list[str] = field(default_factory=list)


@dataclass
class TermRules:
    terms: list[Term]
    simplified_characters: str = ""
    simplified_exceptions: list[str] = field(default_factory=list)

    @classmethod
    def load(cls, path: Path) -> "TermRules":
        data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
        terms = [Term(t["term"], t.get("preferred", ""), t.get("severity", "error"),
                      list(t.get("exceptions") or [])) for t in data.get("terms") or []]
        return cls(terms, data.get("simplified_characters", ""),
                   list(data.get("simplified_exceptions") or []))


@dataclass
class TermHit:
    term: str
    preferred: str
    severity: str
    context: str

    def describe(self) -> str:
        hint = f" (use {self.preferred})" if self.preferred else ""
        return f"{self.severity}: '{self.term}'{hint} in “{self.context}”"


def _excluded_spans(text: str, phrases: list[str]) -> list[tuple[int, int]]:
    spans = []
    for phrase in phrases:
        for m in re.finditer(re.escape(phrase), text):
            spans.append((m.start(), m.end()))
    return spans


def _inside(start: int, end: int, spans: list[tuple[int, int]]) -> bool:
    return any(s <= start and end <= e for s, e in spans)


def _context(text: str, start: int, end: int) -> str:
    return text[max(0, start - 8):end + 8].replace("\n", " ").strip()


def check_prose(text: str, rules: TermRules) -> list[TermHit]:
    """Check text that is already prose (protected regions removed)."""
    hits: list[TermHit] = []
    for term in rules.terms:
        spans = _excluded_spans(text, term.exceptions)
        for m in re.finditer(re.escape(term.term), text):
            if not _inside(m.start(), m.end(), spans):
                hits.append(TermHit(term.term, term.preferred, term.severity,
                                    _context(text, m.start(), m.end())))
    if rules.simplified_characters:
        spans = _excluded_spans(text, rules.simplified_exceptions)
        pattern = "[" + re.escape(rules.simplified_characters) + "]"
        for m in re.finditer(pattern, text):
            if not _inside(m.start(), m.end(), spans):
                hits.append(TermHit(m.group(0), "", "error",
                                    "simplified character: " + _context(text, m.start(), m.end())))
    return hits


def check_markdown(text: str, rules: TermRules) -> list[TermHit]:
    return check_prose(prose_only(text), rules)


def errors(hits: list[TermHit]) -> list[TermHit]:
    return [h for h in hits if h.severity == "error"]
