"""Integrity checks shared by ``run`` (before commit) and ``check`` (publish gate)."""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass, field
from pathlib import Path
import re

from . import config
from .frontmatter import (FrontMatterError, has_modification_notice, split_document, structural_problems,
                          translatable_fields)
from .protect import (STRAY_BRACKET_RE, PlaceholderError, Protector, fenced_blocks,
                      protected_inventory)
from .segment import heading_levels
from .source_errata import apply_source_errata
from .store import Manifest, SourceInventory, SourceStore, sha256_bytes
from .terms import TermRules, check_markdown, check_prose, errors


def _protected_headings(body: str) -> list[int]:
    p = Protector()
    try:
        return heading_levels(p.protect_body(body))
    except PlaceholderError:
        return heading_levels(body)


def _inline_inventory(text: str) -> Counter:
    p = Protector()
    try:
        return p.protected_originals(p.protect_inline(text))
    except PlaceholderError:
        return Counter({text: 1})


def _html_block_openings(body: str) -> Counter:
    # A translated sentence starting with an originally inline unknown HTML
    # tag changes Kramdown's block parsing and can swallow later headings.
    inline_tags = {'a', 'abbr', 'b', 'bdi', 'bdo', 'br', 'button', 'cite', 'code',
                   'data', 'del', 'dfn', 'em', 'i', 'img', 'input', 'ins', 'kbd',
                   'label', 'mark', 'q', 'ruby', 's', 'samp', 'small', 'span',
                   'strong', 'sub', 'sup', 'time', 'u', 'var', 'wbr'}
    protector = Protector()
    protected = protector.protect_body(body)
    result = Counter()
    for token in re.findall(r'(?m)^[ ]{0,3}(⟦P\d+⟧)', protected):
        match = re.match(r'<([A-Za-z][A-Za-z0-9-]*)\b', protector.store[token])
        if match and match[1].lower() not in inline_tags:
            result[match[1].lower()] += 1
    return result


def compare_translation(baseline: str, current: str, rules: TermRules) -> list[str]:
    """Problems that make `current` an unacceptable translation of `baseline`."""
    problems: list[str] = []
    try:
        # Hash-pinned syntax repairs of malformed upstream Markdown; the
        # translation must match the repaired baseline.
        baseline = apply_source_errata(baseline)
    except ValueError as exc:
        return [f"source errata: {exc}"]
    try:
        base_doc = split_document(baseline)
        cur_doc = split_document(current)
    except FrontMatterError as exc:
        return [str(exc)]
    if not base_doc.has_front_matter or not cur_doc.has_front_matter:
        return ["front matter missing (required for the modification notice)"]
    if not has_modification_notice(cur_doc):
        problems.append("modification notice comment missing after the opening ---")
    problems += structural_problems(base_doc.data, cur_doc.data)
    cur_fields = translatable_fields(cur_doc.data)
    for sid, value in translatable_fields(base_doc.data).items():
        if sid in cur_fields and _inline_inventory(value) != _inline_inventory(cur_fields[sid]):
            problems.append(f"front matter {sid[3:]}: protected HTML/Liquid/code/URL regions differ")
    if STRAY_BRACKET_RE.search(current):
        problems.append("leftover placeholder brackets ⟦ ⟧")
        return problems
    if fenced_blocks(base_doc.body) != fenced_blocks(cur_doc.body):
        problems.append("fenced code blocks differ from baseline")
    base_inv, cur_inv = protected_inventory(base_doc.body), protected_inventory(cur_doc.body)
    if base_inv != cur_inv:
        missing = list((base_inv - cur_inv).elements())[:3]
        extra = list((cur_inv - base_inv).elements())[:3]
        problems.append(f"protected code/Liquid/URL regions differ (missing {missing!r}, extra {extra!r})")
    if _protected_headings(base_doc.body) != _protected_headings(cur_doc.body):
        problems.append("heading count or levels differ from baseline")
    if _html_block_openings(base_doc.body) != _html_block_openings(cur_doc.body):
        problems.append('HTML block/inline context changed; retain prose before originally inline HTML tags')
    hits = check_markdown(cur_doc.body, rules)
    for value in translatable_fields(cur_doc.data).values():
        hits += check_prose(value, rules)
    problems += [f"terminology {h.describe()}" for h in errors(hits)]
    return problems


@dataclass
class CheckReport:
    total: int = 0
    counts: dict = field(default_factory=dict)
    problems: list[str] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return not self.problems


def provenance_problems(entry: dict, require_review: bool) -> list[str]:
    problems = []
    translator = entry.get("translator") or {}
    providers = translator.get("providers") or []
    if not providers or not all(p.get("provider") and p.get("model") for p in providers):
        problems.append("missing translator provenance")
    if entry.get("translated_source_sha256") != entry.get("source_sha256"):
        problems.append("translation was made from a different source hash")
    if not entry.get("target_sha256"):
        problems.append("missing target_sha256")
    if require_review:
        reviewer = entry.get("reviewer") or {}
        if reviewer.get("approved") is not True:
            problems.append("no approved review")
        if reviewer.get("provider") not in config.REVIEW_APPROVED_PROVIDERS:
            problems.append(f"reviewer {reviewer.get('provider')!r} is not a quality-approved review backend")
        if not reviewer.get("model") or not reviewer.get("at"):
            problems.append("incomplete review provenance")
        if reviewer.get("target_sha256") != entry.get("target_sha256"):
            problems.append("review does not cover the current target hash")
        families = {p.get("family") for p in providers}
        if reviewer.get("family") in families:
            problems.append("reviewer is not distinct from the translator")
    return problems


def run_check(root: Path, rules: TermRules, publish: bool = True,
              paths: list[str] | None = None) -> CheckReport:
    """Fail-closed check. With publish=True every selected page must be reviewed.

    The page set is always checked in full against the source inventory
    pinned at ``init``, the manifest and the source store, even when only some
    pages are selected.
    """
    report = CheckReport()
    try:
        manifest = Manifest.load(root)
    except (OSError, ValueError) as exc:
        report.problems.append(f"manifest: {exc}")
        return report
    if manifest.data.get("baseline_commit") != config.BASELINE_COMMIT:
        report.problems.append(f"manifest baseline_commit {manifest.data.get('baseline_commit')} "
                               f"!= {config.BASELINE_COMMIT}")
    store = SourceStore(root)
    pages = manifest.pages
    if not pages:
        report.problems.append("manifest has no pages")
    stored = set(store.pages())
    if set(pages) != stored:
        report.problems.append(f"source store and manifest disagree "
                               f"({len(set(pages) - stored)} missing blobs, {len(stored - set(pages))} extra)")
    try:
        inventory = SourceInventory.load(root)
    except (OSError, ValueError) as exc:
        report.problems.append(f"source inventory: {exc}")
        inventory = None
    if inventory is not None:
        if inventory.data.get("baseline_commit") != config.BASELINE_COMMIT:
            report.problems.append(f"source inventory baseline_commit {inventory.data.get('baseline_commit')} "
                                   f"!= {config.BASELINE_COMMIT}")
        expected = set(inventory.pages)
        for label, actual in (("manifest", set(pages)), ("source store", stored)):
            if actual != expected:
                missing, extra = sorted(expected - actual), sorted(actual - expected)
                report.problems.append(f"{label} page set differs from the source inventory "
                                       f"(missing {len(missing)} {missing[:3]}, extra {len(extra)} {extra[:3]})")
        drift = sorted(p for p in expected & set(pages) if pages[p].get("source_sha256") != inventory.pages[p])
        if drift:
            report.problems.append(f"{len(drift)} manifest source_sha256 value(s) differ from the source "
                                   f"inventory: {drift[:3]}")
    selected = sorted(pages) if not paths else [p for p in paths]
    report.total = len(selected)
    for page in selected:
        entry = pages.get(page)
        if entry is None:
            report.problems.append(f"{page}: not in manifest")
            continue
        status = entry.get("status")
        report.counts[status] = report.counts.get(status, 0) + 1
        try:
            baseline = store.read(page)
        except OSError as exc:
            report.problems.append(f"{page}: cannot read baseline blob: {exc}")
            continue
        if sha256_bytes(baseline) != entry.get("source_sha256"):
            report.problems.append(f"{page}: baseline blob hash does not match source_sha256")
            continue
        target_path = root / page
        if not target_path.is_file():
            report.problems.append(f"{page}: file missing")
            continue
        current = target_path.read_bytes()
        if status == "pending":
            if publish:
                report.problems.append(f"{page}: pending (not translated)")
            elif current != baseline:
                report.problems.append(f"{page}: pending but file differs from baseline (unrecorded change)")
            continue
        if status not in ("translated", "reviewed"):
            report.problems.append(f"{page}: unknown status {status!r}")
            continue
        if publish and status != "reviewed":
            report.problems.append(f"{page}: translated but not reviewed")
        if sha256_bytes(current) != entry.get("target_sha256"):
            report.problems.append(f"{page}: file hash does not match target_sha256 (changed after review)")
            continue
        for problem in provenance_problems(entry, require_review=(status == "reviewed")):
            report.problems.append(f"{page}: {problem}")
        for problem in compare_translation(baseline.decode("utf-8"), current.decode("utf-8"), rules):
            report.problems.append(f"{page}: {problem}")
    return report
