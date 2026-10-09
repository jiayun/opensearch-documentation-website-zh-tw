#!/usr/bin/env python3
"""Keep up to four pages in flight, waiting for subscription quota resets.

No partial publishing. Runtime progress/logs live in .translation-cache.
A finished page frees its slot immediately; there is no batch barrier.
Ctrl-C/SIGTERM stops dispatch; in-flight pages finish with atomic checkpoints.
"""
from __future__ import annotations

from collections import Counter
import argparse
import fcntl
import json
import os
from pathlib import Path
import signal
import threading
import time

from translation_pipeline import config
from translation_pipeline.pipeline import Runner, RunOptions
from translation_pipeline.prompts import PromptContext
from translation_pipeline.providers import ProviderPool, ProviderError, QUOTA, build_providers
from translation_pipeline.store import Manifest, RunLog, atomic_write_json, now
from translation_pipeline.terms import TermRules
from translation_pipeline.scheduling import RollingScheduler, is_review, mixed_batch, review_turn, review_can_run

MAX_ACTIVE = min(4, config.MAX_WORKERS)
CHECKPOINT_SECONDS = 30
RESCAN_SECONDS = 300
CONTEXT_REFRESH_SECONDS = 60
PAGE_COOLDOWN_SECONDS = 3600
QUALITY_RETRY_SECONDS = 5 * 3600


def main(*, retry_now=False):
    root = Path(__file__).resolve().parents[1]
    os.chdir(root)
    cache = root / config.CACHE_DIR
    cache.mkdir(exist_ok=True)
    lock = (cache / "translation-run.lock").open("a")
    try:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except BlockingIOError:
        raise SystemExit("Another translation runner owns the manifest")
    (cache / "overnight.pid").write_text(str(os.getpid()) + "\n")
    log = RunLog(cache / ("overnight-" + time.strftime("%Y%m%dT%H%M%SZ", time.gmtime()) + f"-{os.getpid()}.jsonl"))
    stop = threading.Event()
    pool = ProviderPool(build_providers(), log=log, balance_calls=True)
    manifest = Manifest.load(root)

    def make_runner(prompts, rules):
        # Fresh options per task: concurrent pages never share mutable settings.
        return Runner(root, manifest, pool, prompts, rules,
                      RunOptions(list(config.DEFAULT_TRANSLATORS), list(config.DEFAULT_REVIEWERS), 1), log)

    def run_page(page, prompts, rules):
        return make_runner(prompts, rules)._guarded(page)

    scheduler = RollingScheduler(run_page, MAX_ACTIVE)
    def shutdown(*args):
        stop.set()
        pool.stopped.set()
        scheduler.close()
    signal.signal(signal.SIGTERM, shutdown)
    signal.signal(signal.SIGINT, shutdown)
    # Recover the last known quota states, including overnight restarts.
    previous = cache / "overnight-state.json"
    state = json.loads(previous.read_text()) if previous.exists() else {}
    for name, kind in state.get("disabled", {}).items():
        if name in pool.providers:
            pool.disabled[name] = kind
            pool.disabled_until[name] = state.get("disabled_until", {}).get(name, time.time() + 5 * 3600)
            if name in config.OLLAMA_CLOUD_MODELS and kind == QUOTA:
                for cloud_name in config.OLLAMA_CLOUD_MODELS:
                    pool.disabled[cloud_name] = kind
                    pool.disabled_until[cloud_name] = pool.disabled_until[name]
            elif name in config.AGY_MODELS and kind == QUOTA:
                group = config.AGY_MODELS[name][1]
                for agy_name, (_, bucket) in config.AGY_MODELS.items():
                    if bucket == group:
                        pool.disabled[agy_name] = kind
                        pool.disabled_until[agy_name] = pool.disabled_until[name]
    next_retry = state.get("next_quality_retry", time.time() + QUALITY_RETRY_SECONDS)
    retry_after = state.get("page_retry_after", {})
    if retry_now:
        # Explicitly requested immediate quality repair. This never clears a
        # provider's real quota cooldown, and still limits attempts per page.
        next_retry = time.time()
        retry_after = {}
        log("immediate_quality_retry_requested")
    if state.get("status") == "paused_by_user":
        retry_after = {}  # explicit resume may use newly enabled backends
    # A Claude reset observed at any point triggers one bounded quality retry.
    claude_was_disabled = bool(state.get("disabled", {}).get("claude"))

    prompts = PromptContext.load(root)
    rules = TermRules.load(root / config.BANNED_TERMS_PATH)
    context_loaded_at = time.time()
    retry_version = state.get('prompt_version')
    pages = sorted(manifest.pages, key=lambda p: (manifest.pages[p].get('status') != 'translated', p.split('/')[0] not in {
        'index.md', 'search.md', '404.md', '_getting-started', '_install-and-configure', '_dashboards'}, p))
    kinds = {}  # active page -> dispatched as review-only
    counts = Counter()
    last_completed = []
    last_was_review = False
    remaining = None
    rescan_at = 0.0
    checkpoint_at = 0.0

    def checkpoint(status):
        nonlocal state
        active = scheduler.active
        state = {"pid": os.getpid(), "updated_at": now(), "status": status,
                 "active_pages": active, "active": len(active), "max_active": MAX_ACTIVE,
                 "remaining": remaining, "reviewed": None if remaining is None else len(pages) - remaining,
                 "total": len(pages), "counts": dict(counts), "last_completed": last_completed[-MAX_ACTIVE:],
                 "disabled": dict(pool.disabled), "disabled_until": dict(pool.disabled_until),
                 "next_quality_retry": next_retry, "page_retry_after": dict(retry_after),
                 "codex_worker_cutoff_remaining": 25, "codex_reserved_weekly_percent": 20,
                 "prompt_version": prompts.version,
                 "log": str(log.path.relative_to(root))}
        atomic_write_json(previous, state)

    while True:
        timeout = checkpoint_at - time.time()
        if scheduler.free_slots():
            timeout = min(timeout, rescan_at - time.time())
        done = scheduler.wait(max(0.0, timeout))
        for page, outcome, error in done:
            kinds.pop(page, None)
            counts[outcome] += 1
            last_completed.append({"page": page, "outcome": outcome})
            if error is not None:
                log("page_crashed", page=page, error=f"{type(error).__name__}: {error}"[:500])
            if outcome == "stopped" and stop.is_set():
                continue  # shut down before doing any work; not a failed attempt
            if not make_runner(prompts, rules).is_up_to_date(page):
                retry_after[page] = time.time() + PAGE_COOLDOWN_SECONDS
        if "claude" in pool.disabled:
            claude_was_disabled = True

        if stop.is_set():
            if not scheduler.active:
                break
        elif scheduler.free_slots() and (done or time.time() >= rescan_at):
            if time.time() - context_loaded_at >= CONTEXT_REFRESH_SECONDS:
                # New objects for future tasks only; running pages keep theirs.
                try:
                    prompts, rules = PromptContext.load(root), TermRules.load(root / config.BANNED_TERMS_PATH)
                except Exception as exc:
                    log("context_reload_failed", error=f"{type(exc).__name__}: {exc}"[:500])
                context_loaded_at = time.time()
            runner = make_runner(prompts, rules)
            # Evaluate all providers so elapsed reset times reactivate them.
            translators = pool.available(list(config.DEFAULT_TRANSLATORS))
            reviewers = pool.available(list(config.DEFAULT_REVIEWERS))
            active = set(scheduler.active)
            if retry_version != prompts.version:
                # A changed glossary/repair policy gives exhausted pages one
                # fresh bounded retry. Never reset an in-flight page's counter.
                with manifest.lock:
                    for page in pages:
                        entry = manifest.pages[page]
                        if page not in active and entry.get('status') != 'reviewed' and entry.get('attempts', 0) >= config.MAX_PAGE_ATTEMPTS:
                            entry['attempts'] = 0
                            retry_after.pop(page, None)
                    manifest.save()
                log('quality_policy_changed', previous=retry_version, current=prompts.version)
                retry_version = prompts.version
            if time.time() >= next_retry or (claude_was_disabled and not pool.is_disabled("claude")):
                # Bounded quality retries after a reset; never promote failures.
                with manifest.lock:
                    for page in pages:
                        if page not in active and not runner.is_up_to_date(page):
                            manifest.pages[page]["attempts"] = 0
                    manifest.save()
                next_retry = time.time() + QUALITY_RETRY_SECONDS
                claude_was_disabled = False
            pending = [p for p in pages if not runner.is_up_to_date(p)]
            remaining = len(pending)
            if not remaining and not active:
                # Final publication remains gated on full site/UI/license checks.
                checkpoint("translation_complete_needs_final_validation")
                print(json.dumps(state, ensure_ascii=False), flush=True)
                break
            can_pair = any(pool.providers[t].family != pool.providers[r].family
                           for t in translators for r in reviewers)
            current = time.time()
            retry_after = {p: t for p, t in retry_after.items() if t > current}
            eligible = [p for p in pending if p not in active and p not in retry_after]
            if not translators:
                eligible = [p for p in eligible if is_review(manifest.pages[p])]
            eligible = [page for page in eligible if can_pair or (
                is_review(manifest.pages[page]) and review_can_run(manifest.pages[page], pool.providers, reviewers))]
            candidates = runner.select(eligible, None)
            order = mixed_batch(candidates, manifest.pages, scheduler.free_slots(),
                                review_turn([kinds[p] for p in active if p in kinds], last_was_review))
            dispatch_kinds = {page: is_review(manifest.pages[page]) for page in order}
            for page in scheduler.submit(order, prompts, rules):
                kinds[page] = last_was_review = dispatch_kinds[page]
                log("page_dispatched", page=page, review_only=kinds[page])
            # Sleep until something can change: a cooldown ends, a provider
            # resets, the quality retry is due, or the periodic rescan.
            wakes = [retry_after[p] for p in pending if p in retry_after]
            wakes += [t for t in dict(pool.disabled_until).values() if t > current]
            rescan_at = min([current + RESCAN_SECONDS, next_retry] + wakes)

        if done or time.time() >= checkpoint_at:
            if stop.is_set():
                status = "stopping" if scheduler.active else "stopped"
            else:
                status = "working" if scheduler.active else "waiting_for_quota_or_retry"
            checkpoint(status)
            checkpoint_at = time.time() + CHECKPOINT_SECONDS
            if done:
                print(json.dumps(state, ensure_ascii=False), flush=True)

    for page, outcome, error in scheduler.drain():
        counts[outcome] += 1
        last_completed.append({"page": page, "outcome": outcome})
    remaining = sum(not make_runner(prompts, rules).is_up_to_date(page) for page in pages)
    if stop.is_set():
        checkpoint("stopped")
        print(json.dumps(state, ensure_ascii=False), flush=True)
    lock.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--retry-now", action="store_true",
                        help="immediately retry unfinished pages once with available providers; preserve quota cooldowns")
    main(retry_now=parser.parse_args().retry_now)
