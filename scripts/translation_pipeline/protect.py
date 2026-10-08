"""Replace non-translatable Markdown/Liquid regions with unique placeholders.

Protected regions: fenced code blocks, Liquid raw/comment/capture blocks,
Liquid tags and output, HTML comments, math blocks, inline code, link and
image destinations, reference labels and definitions, autolinks, bare URLs,
kramdown attribute lists, footnote markers, and HTML tags.

A placeholder looks like ``⟦P12⟧``. Placeholders may nest (for example, a
capture block that contains a fenced code block); ``restore`` expands them
until none remain.
"""

from __future__ import annotations

import re
from collections import Counter

TOKEN_RE = re.compile(r"⟦P(\d+)⟧")
STRAY_BRACKET_RE = re.compile(r"[⟦⟧]")

_FENCE_OPEN_RE = re.compile(r"^([ \t]*)(`{3,}|~{3,})(.*)$")
_LIQUID_BLOCK_RE = re.compile(
    r"\{%-?\s*(raw|comment|capture)\b[^%]*?-?%\}.*?\{%-?\s*end\1\s*-?%\}", re.S
)
_HTML_COMMENT_RE = re.compile(r"<!--.*?-->", re.S)
_MATH_BLOCK_RE = re.compile(r"\$\$.+?\$\$", re.S)
_INLINE_CODE_RE = re.compile(r"(?<!`)(`+)(?!`)(.+?)(?<!`)\1(?!`)")
_LINK_DEST_RE = re.compile(
    r"(\]\()((?:<[^>\n]*>|[^\s()]|\([^\s()]*\))+(?:\s+(?:\"[^\"\n]*\"|'[^'\n]*'))?)(\))"
)
_REF_LABEL_RE = re.compile(r"(\]\[)([^\]\n]+)(\])")
_REF_DEF_RE = re.compile(r"^[ ]{0,3}\[[^\]\n]+\]:[ \t]+\S.*$", re.M)
_FOOTNOTE_RE = re.compile(r"\[\^[^\]\n]+\]")
_AUTOLINK_RE = re.compile(r"<(?:https?|mailto|ftp):[^>\s]+>")
_LIQUID_TAG_RE = re.compile(r"\{%.*?%\}", re.S)
_IAL_RE = re.compile(r"\{:[^}\n]*\}|\{#[^}\n]*\}")
_HTML_TAG_RE = re.compile(r"</?[A-Za-z][A-Za-z0-9-]*(?:\s[^<>]*?)?/?>")
# Copyright, SPDX and license/permission notices stay verbatim English, even as
# plain prose. Link text that merely names such a page is still translated.
_LEGAL_LINE_RE = re.compile(
    r"^[^\n]*(?:\bCopyright\s+(?:©|\(c\)|\d{4})|\bTiles are generated per\b|©\s*\d{4}|\bSPDX-License-Identifier:|"
    r"\bAll rights reserved\b|\bLicensed under the\b|\bPermission is hereby granted\b|"
    r"\bLicensed to the Apache Software Foundation\b)[^\n]*$", re.I | re.M)
# CJK text and full-width punctuation end a URL so that boundaries are the same
# before and after translation.
_URL_CHARS = r"[^\s<>()\[\]\"'`⟦⟧　-〿㐀-鿿＀-￯"
_BARE_URL_RE = re.compile(r"(?<![A-Za-z0-9_/])(?:https?|ftp)://" + _URL_CHARS + r"]*" + _URL_CHARS + r".,;:!?]")
# Liquid output plus a URL path written directly after it, such as
# {{site.url}}{{site.baseurl}}/vector-search/ outside a Markdown link.
_LIQUID_OUTPUT_RE = re.compile(r"\{\{.*?\}\}(?:" + _URL_CHARS + r"]*" + _URL_CHARS + r".,;:!?])?", re.S)


class PlaceholderError(ValueError):
    pass


class Protector:
    """Holds the placeholder table for a single page."""

    def __init__(self) -> None:
        self.store: dict[str, str] = {}
        self.block_tokens: set[str] = set()
        self._counter = 0

    # -- token management -------------------------------------------------
    def _token(self, original: str, block: bool = False) -> str:
        token = f"⟦P{self._counter}⟧"
        self._counter += 1
        self.store[token] = original
        if block:
            self.block_tokens.add(token)
        return token

    def _sub(self, regex: re.Pattern, text: str, group: int | None = None,
             mark_blocks: bool = False) -> str:
        def repl(m: re.Match) -> str:
            if group is None:
                original = m.group(0)
                block = mark_blocks and "\n" in original and _owns_lines(text, m.start(), m.end())
                return self._token(original, block=block)
            whole = m.group(0)
            start, end = m.start(group) - m.start(), m.end(group) - m.start()
            return whole[:start] + self._token(m.group(group)) + whole[end:]
        return regex.sub(repl, text)

    # -- public API -------------------------------------------------------
    def protect_body(self, text: str) -> str:
        if STRAY_BRACKET_RE.search(text):
            raise PlaceholderError("source already contains placeholder brackets ⟦ ⟧")
        text = self._protect_fences(text)
        text = self._sub(_LIQUID_BLOCK_RE, text, mark_blocks=True)
        text = self._sub(_HTML_COMMENT_RE, text, mark_blocks=True)
        text = self._sub(_MATH_BLOCK_RE, text, mark_blocks=True)
        text = self._protect_legal(text, mark_blocks=True)
        return self.protect_inline(text)

    def protect_inline(self, text: str) -> str:
        if STRAY_BRACKET_RE.search(TOKEN_RE.sub("", text)):
            raise PlaceholderError("source already contains placeholder brackets ⟦ ⟧")
        text = self._protect_legal(text)
        text = self._sub(_INLINE_CODE_RE, text)
        text = self._sub(_LINK_DEST_RE, text, group=2)
        text = self._sub(_REF_DEF_RE, text)
        text = self._sub(_REF_LABEL_RE, text, group=2)
        text = self._sub(_FOOTNOTE_RE, text)
        text = self._sub(_AUTOLINK_RE, text)
        text = self._sub(_LIQUID_TAG_RE, text)
        text = self._sub(_LIQUID_OUTPUT_RE, text)
        # Destinations that contained spaced Liquid output are caught now.
        text = self._sub(_LINK_DEST_RE, text, group=2)
        text = self._sub(_IAL_RE, text)
        text = self._sub(_HTML_TAG_RE, text)
        text = self._sub(_BARE_URL_RE, text)
        return text

    def restore(self, text: str) -> str:
        for _ in range(64):
            if not TOKEN_RE.search(text):
                break

            def repl(m: re.Match) -> str:
                token = m.group(0)
                if token not in self.store:
                    raise PlaceholderError(f"unknown placeholder {token}")
                return self.store[token]
            text = TOKEN_RE.sub(repl, text)
        if TOKEN_RE.search(text):
            raise PlaceholderError("placeholder nesting too deep")
        return text

    def protected_originals(self, text: str) -> Counter:
        """Multiset of fully restored originals for top-level tokens in text."""
        return Counter(self.restore(m.group(0)) for m in TOKEN_RE.finditer(text))

    def _protect_legal(self, text: str, mark_blocks: bool = False) -> str:
        """Each legal notice line (without its line break) becomes one token."""
        def repl(m: re.Match) -> str:
            line = m.group(0)
            body = line.rstrip("\r")
            if TOKEN_RE.fullmatch(body.strip()):
                return line
            return self._token(body, block=mark_blocks) + line[len(body):]
        return _LEGAL_LINE_RE.sub(repl, text)

    # -- fenced code ------------------------------------------------------
    def _protect_fences(self, text: str) -> str:
        lines = text.splitlines(keepends=True)
        out: list[str] = []
        i = 0
        while i < len(lines):
            line = lines[i]
            m = _FENCE_OPEN_RE.match(line.rstrip("\r\n"))
            if not m or (m.group(2)[0] == "`" and "`" in m.group(3)):
                out.append(line)
                i += 1
                continue
            fence = m.group(2)
            close_re = re.compile(r"^[ \t]*" + re.escape(fence[0]) + "{" + str(len(fence)) + r",}[ \t]*$")
            j = i + 1
            while j < len(lines) and not close_re.match(lines[j].rstrip("\r\n")):
                j += 1
            end = min(j, len(lines) - 1)
            block = "".join(lines[i:end + 1])
            newline = ""
            if block.endswith("\r\n"):
                block, newline = block[:-2], "\r\n"
            elif block.endswith("\n"):
                block, newline = block[:-1], "\n"
            out.append(self._token(block, block=True) + newline)
            i = end + 1
        return "".join(out)


def _owns_lines(text: str, start: int, end: int) -> bool:
    before_ok = start == 0 or text[start - 1] == "\n"
    after_ok = end == len(text) or text[end] in "\r\n"
    return before_ok and after_ok


def tokens_in(text: str) -> Counter:
    return Counter(m.group(0) for m in TOKEN_RE.finditer(text))


def normalize_block_tokens(text: str, block_tokens: set[str]) -> str:
    """Remove indentation a model may add before block placeholders."""
    def repl(m: re.Match) -> str:
        return m.group(2) if m.group(2) in block_tokens else m.group(0)
    return re.sub(r"(?m)^([ \t]+)(⟦P\d+⟧)", repl, text)


def placeholder_problems(source: str, output: str, block_tokens: set[str]) -> list[str]:
    """Return integrity problems between a protected source and model output."""
    problems: list[str] = []
    src, out = tokens_in(source), tokens_in(output)
    if src != out:
        missing = sorted((src - out).elements())
        extra = sorted((out - src).elements())
        if missing:
            problems.append("missing placeholders: " + " ".join(missing[:20]))
        if extra:
            problems.append("unexpected placeholders: " + " ".join(extra[:20]))
    if STRAY_BRACKET_RE.search(TOKEN_RE.sub("", output)):
        problems.append("malformed placeholder brackets in output")
    src_blocks = [m.group(0) for m in TOKEN_RE.finditer(source) if m.group(0) in block_tokens]
    out_blocks = [m.group(0) for m in TOKEN_RE.finditer(output) if m.group(0) in block_tokens]
    if src_blocks != out_blocks and not problems:
        problems.append("block placeholders were reordered")
    for token in set(out_blocks):
        if not re.search(r"(?m)^" + re.escape(token) + r"[ \t]*\r?$", output):
            problems.append(f"block placeholder {token} is not on its own line")
    return problems


def prose_only(text: str) -> str:
    """Text with every protected region removed (used for terminology checks)."""
    p = Protector()
    try:
        protected = p.protect_body(text)
    except PlaceholderError:
        protected = text
    return TOKEN_RE.sub(" ", protected)


def fenced_blocks(text: str) -> list[str]:
    """Fenced code blocks of a document, byte-for-byte, in order."""
    p = Protector()
    protected = p._protect_fences(text)
    return [p.store[m.group(0)] for m in TOKEN_RE.finditer(protected)]


def protected_inventory(text: str) -> Counter:
    """Multiset of restored protected regions (code, Liquid, URLs, ...)."""
    p = Protector()
    protected = p.protect_body(text)
    return Counter(p.restore(m.group(0)) for m in TOKEN_RE.finditer(protected))
