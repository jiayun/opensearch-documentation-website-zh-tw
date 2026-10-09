"""init and run: baseline enumeration, per-page translation, review and commit."""

from __future__ import annotations

import json
import re
import subprocess
import threading
import copy
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable

import yaml

from . import config
from .checks import compare_translation
from .frontmatter import (Document, FrontMatterError, add_modification_notice, original_front_matter, rewrite,
                          split_document, translatable_fields)
from .prompts import (REVIEWER_SYSTEM, TRANSLATOR_SYSTEM, PromptContext, ReviewResult,
                      parse_review, validate_translation)
from .protect import TOKEN_RE, PlaceholderError, Protector
from .protect import legal_notice_lines
from .providers import (INVALID, TRUNCATED, NoProviderAvailable, ProviderError, ProviderPool,
                        extract_json_object)
from .segment import Chunk, split_body
from .source_errata import apply_source_errata
from .store import (Cache, Manifest, RunLog, SourceInventory, SourceStore, atomic_write, new_entry, now,
                    sha256_bytes, sha256_text)
from .terms import TermRules


# -- init -----------------------------------------------------------------------

class InitError(RuntimeError):
    pass


def _git(root: Path, args: list[str], stdin: bytes | None = None) -> bytes:
    proc = subprocess.run(["git", *args], cwd=root, input=stdin, capture_output=True, check=False)
    if proc.returncode != 0:
        raise InitError(f"git {' '.join(args[:2])} failed: {proc.stderr.decode(errors='replace').strip()}")
    return proc.stdout


def baseline_pages(root: Path, commit: str) -> dict[str, bytes]:
    """All rendered documentation pages at the baseline commit."""
    cfg = yaml.safe_load(_git(root, ["show", f"{commit}:_config.yml"])) or {}
    collections = cfg.get("collections") or {}
    if not isinstance(collections, dict):
        raise InitError("_config.yml collections must be a mapping")
    prefixes = tuple(f"_{name}/" for name, c in collections.items() if isinstance(c, dict) and c.get("output"))
    names = [n.decode("utf-8") for n in _git(root, ["ls-tree", "-r", "-z", "--name-only", commit]).split(b"\0") if n]
    wanted = [n for n in names if (n.startswith(prefixes) and n.endswith(config.DOC_EXTENSIONS))
              or n in config.ROOT_PAGES]
    request = "".join(f"{commit}:{n}\n" for n in wanted).encode("utf-8")
    out = _git(root, ["cat-file", "--batch"], stdin=request)
    pages: dict[str, bytes] = {}
    pos = 0
    for name in wanted:
        nl = out.index(b"\n", pos)
        header = out[pos:nl].split()
        if len(header) != 3 or header[1] != b"blob":
            raise InitError(f"cannot read {name} at {commit}")
        size = int(header[2])
        data = out[nl + 1:nl + 1 + size]
        pos = nl + 1 + size + 1
        if data.startswith(b"---"):   # Jekyll renders only files with front matter
            pages[name] = data
    return pages


def init(root: Path, commit: str = config.BASELINE_COMMIT) -> dict:
    manifest_path = root / config.MANIFEST_PATH
    manifest = Manifest.load(root) if manifest_path.exists() else Manifest.new(root, commit)
    if manifest.data["baseline_commit"] != commit:
        raise InitError(f"manifest baseline {manifest.data['baseline_commit']} != {commit}")
    store = SourceStore(root)
    pages = baseline_pages(root, commit)
    added = 0
    for page, data in sorted(pages.items()):
        digest = sha256_bytes(data)
        entry = manifest.pages.get(page)
        if entry and entry["source_sha256"] != digest:
            raise InitError(f"{page}: baseline content differs from manifest source_sha256")
        if store.exists(page) and sha256_bytes(store.read(page)) != digest:
            raise InitError(f"{page}: stored baseline blob differs from the baseline commit")
        store.write(page, data)
        if not entry:
            doc = split_document(data.decode("utf-8"))
            manifest.pages[page] = new_entry(digest, original_front_matter(doc.data))
            added += 1
    unknown = sorted(set(manifest.pages) - set(pages))
    if unknown:
        raise InitError(f"manifest lists pages missing from the baseline: {unknown[:5]}")
    inventory = SourceInventory.build(root, commit, {p: sha256_bytes(d) for p, d in pages.items()})
    if inventory.path.exists():
        try:
            existing = SourceInventory.load(root)
        except (OSError, ValueError) as exc:
            raise InitError(f"source inventory: {exc}")
        if existing.data != inventory.data:
            raise InitError("source inventory differs from the baseline commit; "
                            "re-baselining requires removing it deliberately")
    else:
        inventory.save()
    manifest.save()
    return {"pages": len(pages), "added": added}


# -- page work ---------------------------------------------------------------------

class PageFailure(Exception):
    """The page cannot proceed in this run (transport, drift, no provider...)."""

    def __init__(self, message: str, stop: bool = False) -> None:
        super().__init__(message)
        self.stop = stop


class PageProblems(Exception):
    """A completed translation pass that failed validation; problems become findings."""

    def __init__(self, problems: list[str], chunk_findings: dict[int, list[str]] | None = None) -> None:
        super().__init__("; ".join(problems[:5]))
        self.problems = problems
        self.chunk_findings = chunk_findings


@dataclass
class PageWork:
    page: str
    source_sha256: str
    baseline: str
    doc: Document
    protector: Protector
    fm_segments: dict[str, str]
    chunks: list[Chunk]
    chunk_spans: list[tuple[int, int]]  # restored offsets in the baseline body


def build_work(page: str, baseline: bytes, source_sha256: str) -> PageWork:
    # Translation and validation use the same explicitly recorded syntax
    # errata; inventory/provenance stay pinned to the immutable raw source.
    text = apply_source_errata(baseline.decode("utf-8"))
    doc = split_document(text)
    if not doc.has_front_matter:
        # The per-file modification notice lives in the front matter.
        raise PageFailure("page has no front matter; cannot add the modification notice")
    protector = Protector()
    fm_segments = {sid: protector.protect_inline(value) for sid, value in translatable_fields(doc.data).items()}
    body = protector.protect_body(doc.body)
    chunks = split_body(body, config.CHUNK_LIMIT, size=lambda s: len(protector.restore(s)))
    spans, offset = [], 0
    for chunk in chunks:
        length = len(protector.restore(chunk.text))
        spans.append((offset, offset + length))
        offset += length
    return PageWork(page, source_sha256, text, doc, protector, fm_segments, chunks, spans)


@dataclass
class Candidate:
    text: str
    translator: dict
    new: bool = True
    segments: dict[str, str] = field(default_factory=dict)

    @property
    def families(self) -> set[str]:
        return {p.get("family") for p in (self.translator or {}).get("providers", [])}


def _has_prose(text: str) -> bool:
    return bool(re.search(r"[A-Za-z]", TOKEN_RE.sub("", text)))


def sections(body: str) -> list[tuple[int, int, str]]:
    """Split a body at ATX headings (ignoring code); returns (start, end, text)."""
    p = Protector()
    try:
        protected = p.protect_body(body)
    except PlaceholderError:
        return [(0, len(body), body)]
    starts = [0] + [m.start() for m in re.finditer(r"(?m)^#{1,6}[ \t]", protected) if m.start() > 0]
    pieces = [protected[a:b] for a, b in zip(starts, starts[1:] + [len(protected)])]
    out, offset = [], 0
    for piece in pieces:
        restored = p.restore(piece)
        out.append((offset, offset + len(restored), restored))
        offset += len(restored)
    return out


def protected_draft(protector: Protector, protected_source: str, draft: str) -> str:
    """Give a draft the source's exact placeholder IDs, including duplicates."""
    from collections import deque
    other = Protector()
    protected = other.protect_body(draft)
    available = defaultdict(deque)
    for match in TOKEN_RE.finditer(protected_source):
        token = match.group(0)
        available[protector.restore(token)].append(token)
    def replace(match):
        original = other.restore(match.group(0))
        if not available[original]:
            raise PageProblems(['repair draft protected regions do not match source'])
        return available[original].popleft()
    result = TOKEN_RE.sub(replace, protected)
    if any(available.values()):
        raise PageProblems(['repair draft is missing protected source regions'])
    return result


# -- runner ------------------------------------------------------------------------

@dataclass
class RunOptions:
    translators: list[str]
    reviewers: list[str]
    workers: int = 1
    dry_run: bool = False
    reset_attempts: bool = False


class Runner:
    def __init__(self, root: Path, manifest: Manifest, pool: ProviderPool, prompts: PromptContext,
                 rules: TermRules, options: RunOptions, log: RunLog,
                 progress: Callable[[str], None] = print) -> None:
        self.root = root
        self.manifest = manifest
        self.pool = pool
        self.prompts = prompts
        self.rules = rules
        self.options = options
        self.log = log
        self.progress = progress
        self.store = SourceStore(root)
        self.cache = Cache(root)
        self.counts: dict[str, int] = defaultdict(int)
        self._count_lock = threading.Lock()

    # -- selection ----------------------------------------------------------
    def is_up_to_date(self, page: str) -> bool:
        entry = self.manifest.pages[page]
        path = self.root / page
        return (entry.get("status") == "reviewed" and path.is_file()
                and sha256_bytes(path.read_bytes()) == entry.get("target_sha256")
                and entry.get("translated_source_sha256") == entry.get("source_sha256"))

    def select(self, pages: list[str], limit: int | None) -> list[str]:
        selected = []
        for page in pages:
            if self.is_up_to_date(page):
                continue
            entry = self.manifest.pages[page]
            if entry.get("attempts", 0) >= config.MAX_PAGE_ATTEMPTS and not self.options.reset_attempts:
                reviewer = entry.get("reviewer") or {}
                # A translated page still awaiting its first review is worth a
                # review; one already rejected at this hash is not.
                if entry.get("status") != "translated" or (
                        reviewer.get("approved") is False
                        and reviewer.get("target_sha256") == entry.get("target_sha256")):
                    continue
            selected.append(page)
            if limit and len(selected) >= limit:
                break
        return selected

    # -- orchestration --------------------------------------------------------
    def run(self, pages: list[str]) -> dict:
        total = len(pages)
        self.log("run_start", pages=total, translators=self.options.translators,
                 reviewers=self.options.reviewers, prompt_version=self.prompts.version)
        if self.options.reset_attempts:
            for page in pages:
                self.manifest.pages[page]["attempts"] = 0
            self.manifest.save()
        done = 0
        workers = max(1, min(self.options.workers, config.MAX_WORKERS))
        with ThreadPoolExecutor(max_workers=workers) as executor:
            futures = {executor.submit(self._guarded, page): page for page in pages}
            for future in as_completed(futures):
                outcome = future.result()
                done += 1
                with self._count_lock:
                    self.counts[outcome] += 1
                    summary = " ".join(f"{k}={v}" for k, v in sorted(self.counts.items()))
                self.progress(f"progress {done}/{total}: {summary}")
        self.log("run_end", counts=dict(self.counts), disabled_providers=self.pool.disabled,
                 usage=self.pool.usage)
        return dict(self.counts)

    def _guarded(self, page: str) -> str:
        if self.pool.stopped.is_set() or not self.pool.available(self.options.translators):
            if not self._needs_review_only(page):
                return "stopped"
        try:
            outcome = self.process_page(page)
        except PageFailure as exc:
            self.log("page_failed", page=page, error=str(exc))
            if not self.options.dry_run:
                self.manifest.update(page, last_error=str(exc)[:500], updated_at=now())
            if exc.stop:
                return "stopped"
            return "failed"
        except Exception as exc:  # keep other pages running; record the error
            self.log("page_error", page=page, error=f"{type(exc).__name__}: {exc}")
            if not self.options.dry_run:
                self.manifest.update(page, last_error=f"{type(exc).__name__}: {exc}"[:500], updated_at=now())
            return "failed"
        self.log("page_done", page=page, outcome=outcome)
        return outcome

    def _needs_review_only(self, page: str) -> bool:
        entry = self.manifest.pages[page]
        path = self.root / page
        return (entry.get("status") == "translated" and path.is_file()
                and sha256_bytes(path.read_bytes()) == entry.get("target_sha256"))

    # -- per page ------------------------------------------------------------------
    def recover_journal(self, page: str) -> None:
        record = self.cache.read_journal(page)
        if not record:
            return
        path = self.root / page
        if path.is_file() and sha256_bytes(path.read_bytes()) == record.get("target_sha256"):
            self.manifest.update(page, **record["fields"])
            self.log("journal_recovered", page=page)
        self.cache.clear_journal(page)

    def process_page(self, page: str) -> str:
        if not self.options.dry_run:
            self.recover_journal(page)
        entry = self.manifest.entry(page)
        baseline = self.store.read(page)
        if sha256_bytes(baseline) != entry["source_sha256"]:
            raise PageFailure("stored baseline does not match source_sha256")
        path = self.root / page
        current = path.read_bytes() if path.is_file() else None
        current_sha = sha256_bytes(current) if current is not None else None
        known = entry["status"] in ("translated", "reviewed") and entry.get("target_sha256") == current_sha
        fresh = known and entry.get("translated_source_sha256") == entry["source_sha256"]
        if entry["status"] == "reviewed" and fresh:
            return "skipped"
        if not known and current != baseline:
            raise PageFailure("file differs from both the baseline and the recorded translation; "
                              "refusing to overwrite")
        work = build_work(page, baseline, entry["source_sha256"])
        candidate: Candidate | None = None
        if entry["status"] == "translated" and fresh:
            existing = current.decode("utf-8")
            # A translation recorded before a pipeline rule change (for example
            # the modification notice) is retranslated instead of reviewed.
            if not compare_translation(work.baseline, existing, self.rules):
                candidate = Candidate(existing, entry.get("translator") or {}, new=False)
        if self.options.dry_run:
            self.progress(f"dry-run {page}: chunks={len(work.chunks)} fm_fields={len(work.fm_segments)} "
                          f"status={entry['status']}")
            return "dry-run"
        findings: dict[int, list[str]] = {}
        pending_repair: tuple[Candidate, ReviewResult] | None = None
        if candidate is None:
            # A bounded retry resumes the last rejected draft instead of paying
            # to recreate the whole page. The checkpoint is never an approval.
            saved = self.cache.get("pending-repairs", Cache.key(page, work.source_sha256))
            if saved and saved.get("source_sha256") == work.source_sha256:
                text, provenance = saved.get("text"), saved.get("translator")
                providers = (provenance or {}).get("providers", []) if isinstance(provenance, dict) else []
                if (isinstance(text, str) and providers
                        and all(p.get("provider") and p.get("model") and p.get("family") for p in providers)
                        and not compare_translation(work.baseline, text, self.rules)):
                    previous = Candidate(text, provenance, new=True)
                    record = saved.get("review") or {}
                    if (saved.get("prompt_version") == self.prompts.version
                            and record.get("approved") is False and record.get("issues")
                            and record.get("provider") in self.pool.providers):
                        rejected = ReviewResult(False, record["issues"], record["provider"], record.get("model", ""))
                        pending_repair = (previous, rejected)
                        findings = self.issues_to_findings(work, rejected.issues)
                    else:
                        # Section ids and editorial rules may have changed.
                        # Review the complete saved draft under the current policy.
                        candidate = previous
                    self.log("rejected_draft_resumed", page=page,
                             repair_ready=pending_repair is not None)
        while True:
            if candidate is None:
                attempts = self.manifest.entry(page).get("attempts", 0)
                if attempts >= config.MAX_PAGE_ATTEMPTS:
                    self.manifest.update(page, last_error="attempt limit reached", updated_at=now())
                    return "failed"
                try:
                    if pending_repair:
                        previous, rejected = pending_repair
                        candidate = self.repair(work, previous, rejected)
                        if candidate is None:
                            candidate = self.translate(work, findings, attempts + 1)
                    else:
                        candidate = self.translate(work, findings, attempts + 1)
                except PageProblems as exc:
                    self.manifest.update(page, attempts=attempts + 1, last_error=str(exc)[:500], updated_at=now())
                    self.log("page_invalid", page=page, problems=exc.problems[:20])
                    findings = exc.chunk_findings or {c.index: exc.problems[:20] for c in work.chunks}
                    continue
                self.manifest.update(page, attempts=attempts + 1)
            review = self.review(work, candidate)
            if review is None:
                if candidate.new:
                    self.commit(page, work, candidate, None)
                else:
                    self.manifest.update(page, last_error="no review backend available", updated_at=now())
                return "translated"
            if review.approved:
                self.commit(page, work, candidate, review)
                return "reviewed"
            self.log("review_rejected", page=page, provider=review.provider, issues=review.issues[:20])
            self.cache.put("pending-repairs", Cache.key(page, work.source_sha256), {
                "source_sha256": work.source_sha256, "text": candidate.text,
                "translator": candidate.translator, "prompt_version": self.prompts.version,
                "review": {"approved": False, "issues": review.issues,
                           "provider": review.provider, "model": review.model}, "at": now()})
            if candidate.new:
                self.cache.put("rejected", Cache.key(page, sha256_text(candidate.text)),
                               {"page": page, "text": candidate.text, "issues": review.issues})
            else:
                self.manifest.update(page, reviewer=self._review_record(review, candidate),
                                     last_error="review rejected", updated_at=now())
            findings = self.issues_to_findings(work, review.issues)
            pending_repair = (candidate, review)
            candidate = None
            if self.manifest.entry(page).get("attempts", 0) >= config.MAX_PAGE_ATTEMPTS:
                self.manifest.update(page, last_error=f"review rejected after {config.MAX_PAGE_ATTEMPTS} attempts",
                                     updated_at=now())
                return "failed"

    # -- translation ---------------------------------------------------------------
    def repair(self, work: PageWork, candidate: Candidate, review: ReviewResult) -> Candidate | None:
        """Patch identified sections only; unrelated draft bytes stay unchanged.

        Invalid/global finding IDs conservatively fall back to full translation.
        Any successful patch still receives complete independent review.
        """
        cache_key = Cache.key(work.page, work.source_sha256, self.prompts.version,
                              sha256_text(candidate.text), json.dumps(review.issues, ensure_ascii=False, sort_keys=True))
        cached = self.cache.get('repairs', cache_key)
        if cached and not compare_translation(work.baseline, cached.get('text', ''), self.rules):
            self.log('repair_cache_hit', page=work.page)
            return Candidate(cached['text'], cached['translator'], new=True)
        source_sections = sections(work.doc.body)
        draft_doc = split_document(candidate.text)
        draft_sections = sections(draft_doc.body)
        if len(source_sections) != len(draft_sections):
            return None
        major = [issue for issue in review.issues if issue.get('severity') == 'major']
        if not major:
            return None
        requested = {}
        for issue in major:
            identifier = issue.get('id') or ''
            if identifier == 'front_matter':
                requested[identifier] = None
                continue
            match = re.fullmatch(r'section\.(\d+)', identifier)
            if not match or int(match[1]) >= len(source_sections):
                return None
            requested[identifier] = int(match[1])
        protector = Protector()
        request = []
        locations = {}
        for identifier, index in requested.items():
            if index is None:
                original_fields = translatable_fields(work.doc.data)
                draft_fields = translatable_fields(draft_doc.data)
                for sid, original in original_fields.items():
                    protected = protector.protect_body(original)
                    try:
                        draft = protected_draft(protector, protected, draft_fields[sid])
                    except PageProblems:
                        self.log('repair_fallback', page=work.page, reason='front matter protected context differs')
                        return None
                    request.append({'id': sid, 'kind': 'front_matter', 'text': protected,
                                    'draft': draft})
                    locations[sid] = None
            else:
                sid = f'body.{index:03d}'
                protected = protector.protect_body(source_sections[index][2])
                try:
                    draft = protected_draft(protector, protected, draft_sections[index][2])
                except PageProblems:
                    self.log('repair_fallback', page=work.page, reason='section protected context differs', section=identifier)
                    return None
                request.append({'id': sid, 'kind': 'markdown', 'text': protected,
                                'draft': draft})
                locations[sid] = index
        metadata = {'page': work.page, 'task': 'repair', 'source_sha256': work.source_sha256,
                    'prompt_version': self.prompts.version, 'issue_ids': list(requested)}
        messages = [f"[{i.get('id')}] {i.get('problem')} Suggested correction: {i.get('suggestion', '')}"
                    for i in review.issues if i.get('id') in requested]
        problems = []
        for _ in range(config.MAX_CHUNK_TRIES):
            prompt = self.prompts.translation_prompt(metadata, request, messages + problems)
            try:
                reply = self.pool.call(self.options.translators, TRANSLATOR_SYSTEM, prompt, 'repair')
                answer = extract_json_object(reply.text)
                outputs, problems = validate_translation(request, answer, protector, self.rules)
            except NoProviderAvailable as exc:
                raise PageFailure(f'no repair translator available: {exc}', stop=True)
            except ProviderError as exc:
                if exc.kind in (INVALID, TRUNCATED):
                    problems = [f'previous repair response {exc.kind}; return complete JSON']
                    continue
                raise PageFailure(f'repair translator {exc.kind}: {exc.detail[:300]}')
            if problems:
                self.log('repair_invalid', page=work.page, problems=problems[:20])
                continue
            restored = {sid: protector.restore(text) for sid, text in outputs.items()}
            patches = []
            for sid, index in locations.items():
                if index is None:
                    continue
                start, end, original = draft_sections[index]
                leading = re.match(r'\s*', original).group(0)
                trailing = re.search(r'\s*$', original).group(0)
                # Response validation trims outer whitespace. Keep the old
                # section boundary so adjacent headings never merge.
                replacement = leading + restored[sid].strip() + trailing
                patches.append((start, end, replacement))
            patches.sort(reverse=True)
            body = draft_doc.body
            for start, end, replacement in patches:
                body = body[:start] + replacement + body[end:]
            fields = {sid: text for sid, text in restored.items() if locations[sid] is None}
            text = add_modification_notice(rewrite(draft_doc, fields) + body)
            problems = compare_translation(work.baseline, text, self.rules)
            if problems:
                self.log('repair_invalid', page=work.page, problems=problems[:20])
                continue
            provenance = copy.deepcopy(candidate.translator)
            provenance.update(at=now(), prompt_version=self.prompts.version)
            provenance.setdefault('providers', []).append({
                'provider': reply.provider, 'model': reply.model,
                'family': self.pool.providers[reply.provider].family, 'repairs': list(requested)})
            self.log('page_repaired', page=work.page, sections=list(requested),
                     repaired_chars=sum(len(item['text']) for item in request), draft_chars=len(candidate.text),
                     provider=reply.provider)
            self.cache.put('repairs', cache_key, {'text': text, 'translator': provenance, 'at': now()})
            return Candidate(text, provenance, new=True)
        raise PageProblems(problems)

    def _chunk_request(self, work: PageWork, chunk: Chunk) -> list[dict]:
        """Segments for one model call; text without letters (only code
        placeholders, numbers, punctuation) is passed through unchanged."""
        request = []
        if chunk.index == 0:
            request += [{"id": sid, "kind": "front_matter", "text": text}
                        for sid, text in work.fm_segments.items() if _has_prose(text)]
        if _has_prose(chunk.core):
            request.append({"id": chunk.segment_id, "kind": "markdown", "text": chunk.core})
        return request

    def translate(self, work: PageWork, findings: dict[int, list[str]], attempt: int = 1) -> Candidate:
        outputs: dict[str, str] = {}
        usage: dict[tuple, list[int]] = defaultdict(list)
        for chunk in work.chunks:
            request = self._chunk_request(work, chunk)
            if not request:
                continue
            segs, provider = self.translate_chunk(work, chunk, request, findings.get(chunk.index, []), attempt)
            outputs.update(segs)
            usage[(provider["provider"], provider["model"], provider["family"])].append(chunk.index)
        body = "".join(c.lead + outputs.get(c.segment_id, c.core) + c.trail for c in work.chunks)
        try:
            body = work.protector.restore(body)
            fm = {sid: work.protector.restore(outputs.get(sid, text)) for sid, text in work.fm_segments.items()}
            text = add_modification_notice(rewrite(work.doc, fm) + body)
        except (PlaceholderError, FrontMatterError) as exc:
            raise PageProblems([str(exc)])
        problems = compare_translation(work.baseline, text, self.rules)
        if problems:
            raise PageProblems(problems)
        translator = {
            "providers": [{"provider": p, "model": m, "family": f, "chunks": idx}
                          for (p, m, f), idx in sorted(usage.items())],
            "prompt_version": self.prompts.version,
            "at": now(),
        }
        return Candidate(text, translator, new=True, segments=outputs)

    def translate_chunk(self, work: PageWork, chunk: Chunk, request: list[dict],
                        findings: list[str], attempt: int = 1) -> tuple[dict[str, str], dict]:
        # Chunks without findings reuse earlier validated output; chunks being
        # fixed get a fresh model call per attempt (a crash resumes the same attempt).
        key = Cache.key(work.page, work.source_sha256, self.prompts.version, str(chunk.index),
                        sha256_text(json.dumps(request, ensure_ascii=False, sort_keys=True)),
                        sha256_text(json.dumps(findings, ensure_ascii=False)),
                        str(attempt) if findings else "")
        cached = self.cache.get("chunks", key)
        if cached:
            answer = {"segments": [{"id": k, "text": v} for k, v in cached["segments"].items()]}
            segs, problems = validate_translation(request, answer, work.protector, self.rules)
            if not problems:
                return segs, cached["provider"]
        metadata = {
            "page": work.page, "source_sha256": work.source_sha256,
            "baseline_commit": config.BASELINE_COMMIT, "target_language": config.TARGET_LANGUAGE,
            "chunk": chunk.index, "chunks": len(work.chunks),
            "page_title": work.doc.data.get("title"), "prompt_version": self.prompts.version,
        }
        issues = list(findings)
        problems: list[str] = []
        for _ in range(config.MAX_CHUNK_TRIES):
            prompt = self.prompts.translation_prompt(metadata, request, issues + problems)
            try:
                reply = self.pool.call(self.options.translators, TRANSLATOR_SYSTEM, prompt, "translate")
                answer = extract_json_object(reply.text)
            except NoProviderAvailable as exc:
                raise PageFailure(f"no translator available: {exc}", stop=True)
            except ProviderError as exc:
                if exc.kind in (INVALID, TRUNCATED):
                    problems = [f"previous reply was {exc.kind}: {exc.detail[:200]}; return the complete JSON"]
                    self.log("chunk_invalid", page=work.page, chunk=chunk.index, problems=problems)
                    continue
                raise PageFailure(f"translator {exc.kind} failure: {exc.detail[:300]}")
            segs, problems = validate_translation(request, answer, work.protector, self.rules)
            if not problems:
                provider = {"provider": reply.provider, "model": reply.model,
                            "family": self.pool.providers[reply.provider].family}
                self.cache.put("chunks", key, {"page": work.page, "chunk": chunk.index, "segments": segs,
                                               "provider": provider, "at": now()})
                return segs, provider
            self.log("chunk_invalid", page=work.page, chunk=chunk.index, provider=reply.provider,
                     problems=problems[:20])
        raise PageProblems([f"chunk {chunk.index}: {p}" for p in problems],
                           chunk_findings={chunk.index: problems[:20]})

    # -- review ----------------------------------------------------------------------
    def review_items(self, work: PageWork, text: str) -> list[dict]:
        doc = split_document(text)
        items = []
        if work.fm_segments:
            items.append({"id": "front_matter",
                          "source": json.dumps(translatable_fields(work.doc.data), ensure_ascii=False, indent=1),
                          "translation": json.dumps(translatable_fields(doc.data), ensure_ascii=False, indent=1)})
        src_sections, out_sections = sections(work.doc.body), sections(doc.body)
        if len(src_sections) == len(out_sections):
            for i, (s, o) in enumerate(zip(src_sections, out_sections)):
                if s[2].strip() or o[2].strip():
                    items.append({"id": f"section.{i:03d}", "source": s[2], "translation": o[2],
                                  "protected_legal_notices": legal_notice_lines(s[2])})
        else:
            items.append({"id": "body", "source": work.doc.body, "translation": doc.body,
                          "protected_legal_notices": legal_notice_lines(work.doc.body)})
        return items

    def review(self, work: PageWork, candidate: Candidate) -> ReviewResult | None:
        chain = [n for n in self.options.reviewers
                 if n in self.pool.providers and n in config.REVIEW_APPROVED_PROVIDERS
                 and self.pool.providers[n].family not in candidate.families]
        if not self.pool.available(chain):
            self.log("review_unavailable", page=work.page)
            return None
        key = Cache.key(work.page, sha256_text(candidate.text), self.prompts.version, ",".join(chain))
        cached = self.cache.get("reviews", key)
        if cached:
            return ReviewResult(cached["approved"], cached["issues"], cached["provider"], cached["model"])
        batches, current, size = [], [], 0
        for item in self.review_items(work, candidate.text):
            item_size = len(item["source"]) + len(item["translation"])
            if current and size + item_size > config.REVIEW_LIMIT:
                batches.append(current)
                current, size = [], 0
            current.append(item)
            size += item_size
        if current:
            batches.append(current)
        approved, issues, used = True, [], None
        for n, batch in enumerate(batches, 1):
            metadata = {"page": work.page, "page_title": work.doc.data.get("title"),
                        "part": n, "parts": len(batches), "prompt_version": self.prompts.version}
            prompt = self.prompts.review_prompt(metadata, batch)
            result = None
            for _ in range(config.MAX_CHUNK_TRIES):
                try:
                    reply = self.pool.call([used] if used else chain, REVIEWER_SYSTEM, prompt, "review")
                    result = parse_review(extract_json_object(reply.text), reply.provider, reply.model)
                    break
                except NoProviderAvailable:
                    return None
                except ProviderError as exc:
                    if exc.kind not in (INVALID, TRUNCATED):
                        self.log("review_failed", page=work.page, kind=exc.kind)
                        return None
                except ValueError as exc:
                    self.log("review_invalid", page=work.page, error=str(exc))
            if result is None:
                return None
            used = result.provider
            approved = approved and result.approved
            issues += result.issues
        final = ReviewResult(approved, issues, used, self.pool.providers[used].model)
        if final.approved:   # rejections are not cached, so a retry is reviewed afresh
            self.cache.put("reviews", key, {"approved": final.approved, "issues": final.issues,
                                            "provider": final.provider, "model": final.model})
        return final

    def issues_to_findings(self, work: PageWork, issues: list[dict]) -> dict[int, list[str]]:
        findings: dict[int, list[str]] = defaultdict(list)
        src_sections = sections(work.doc.body)
        all_chunks = [c.index for c in work.chunks]
        for issue in issues:
            message = f"[{issue['severity']}] {issue['problem']}"
            if issue.get("suggestion"):
                message += f" Suggestion: {issue['suggestion']}"
            iid = str(issue.get("id") or "")
            m = re.fullmatch(r"section\.(\d+)", iid)
            if iid == "front_matter":
                targets = [0]
            elif m and int(m.group(1)) < len(src_sections):
                start, end, _ = src_sections[int(m.group(1))]
                targets = [i for i, (a, b) in enumerate(work.chunk_spans) if a < end and start < b] or all_chunks
            else:
                targets = all_chunks
            for index in targets:
                findings[index].append(message)
        return dict(findings)

    # -- commit ------------------------------------------------------------------------
    def _review_record(self, review: ReviewResult, candidate: Candidate) -> dict:
        return {"provider": review.provider, "model": review.model,
                "family": self.pool.providers[review.provider].family,
                "approved": review.approved, "issues": review.issues[:50],
                "target_sha256": sha256_text(candidate.text),
                "prompt_version": self.prompts.version, "at": now()}

    def commit(self, page: str, work: PageWork, candidate: Candidate, review: ReviewResult | None) -> None:
        target_sha = sha256_text(candidate.text)
        fields = {
            "status": "reviewed" if review else "translated",
            "target_sha256": target_sha,
            "translated_source_sha256": work.source_sha256,
            "translator": candidate.translator,
            "reviewer": self._review_record(review, candidate) if review else None,
            "last_error": None,
            "updated_at": now(),
        }
        with self.manifest.lock:
            if candidate.new:
                self.cache.write_journal(page, {"target_sha256": target_sha, "fields": fields})
                atomic_write(self.root / page, candidate.text.encode("utf-8"))
            self.manifest.update(page, **fields)
            self.cache.clear_journal(page)
        self.log("page_committed", page=page, status=fields["status"], target_sha256=target_sha)


def resolve_page(manifest: Manifest, path: str) -> tuple[str | None, str | None]:
    """Resolve a user path to a manifest page; returns (page, note)."""
    pages = manifest.pages
    clean = re.sub(r"^(?:\./|/)+", "", path.strip())
    for candidate in (clean, clean + ".md", clean.rstrip("/") + "/index.md"):
        if candidate in pages:
            return candidate, None if candidate == clean else f"{path} -> {candidate}"
    parent = str(Path(clean).parent)
    stem = Path(clean).stem
    same_dir = sorted(p for p in pages if str(Path(p).parent) == parent)
    for p in same_dir:
        if Path(p).stem in (stem, stem.replace("_", "-")):
            return p, f"{path} -> {p}"
    if same_dir:
        fallback = parent + "/index.md" if parent + "/index.md" in pages else same_dir[0]
        return fallback, f"{path} missing; using same-topic page {fallback}"
    return None, f"{path}: not a documentation page"
