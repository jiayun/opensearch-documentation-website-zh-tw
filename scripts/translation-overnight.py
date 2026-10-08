#!/usr/bin/env python3
"""Resume bounded translation batches, waiting for subscription quota resets.

No partial publishing. Runtime progress/logs live in .translation-cache.
Ctrl-C/SIGTERM stops dispatch; in-flight pages finish with atomic checkpoints.
"""
from __future__ import annotations

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
from translation_pipeline.scheduling import mixed_batch


def main():
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
    def shutdown(*args):
        stop.set()
        pool.stopped.set()
    signal.signal(signal.SIGTERM, shutdown)
    signal.signal(signal.SIGINT, shutdown)
    manifest = Manifest.load(root)
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
    if not state:
        pool.disable("claude", ProviderError(QUOTA, "You've hit your session limit · resets 3am (Asia/Taipei)"))
    next_retry = state.get("next_quality_retry", time.time() + 5 * 3600)
    retry_after = state.get("page_retry_after", {})
    if state.get("status") == "paused_by_user":
        retry_after = {}  # explicit resume may use newly enabled backends
    while not stop.is_set():
        runner = Runner(root, manifest, pool, PromptContext.load(root),
                        TermRules.load(root / config.BANNED_TERMS_PATH),
                        RunOptions(list(config.DEFAULT_TRANSLATORS), list(config.DEFAULT_REVIEWERS), 4), log)
        pages = sorted(manifest.pages, key=lambda p: (manifest.pages[p].get('status') != 'translated', p.split('/')[0] not in {
            'index.md', 'search.md', '404.md', '_getting-started', '_install-and-configure', '_dashboards'}, p))
        # Evaluate all providers so elapsed reset times reactivate them.
        translators = pool.available(list(config.DEFAULT_TRANSLATORS))
        reviewers = pool.available(list(config.DEFAULT_REVIEWERS))
        if time.time() >= next_retry or (state.get("disabled", {}).get("claude") and not pool.is_disabled("claude")):
            # Bounded quality retries after a reset; never promote failures.
            for page in pages:
                if not runner.is_up_to_date(page):
                    manifest.pages[page]["attempts"] = 0
            manifest.save()
            next_retry = time.time() + 5 * 3600
        candidates = runner.select([p for p in pages if time.time() >= retry_after.get(p, 0)], None)
        selected = mixed_batch(candidates, manifest.pages)
        can_pair = any(pool.providers[t].family != pool.providers[r].family
                       for t in translators for r in reviewers)
        atomic_write_json(previous, {**state, "pid": os.getpid(), "updated_at": now(),
            "status": "working" if selected and can_pair else "waiting_for_quota_or_retry",
            "active_pages": selected if can_pair else [], "disabled": dict(pool.disabled),
            "log": str(log.path.relative_to(root)),
            "disabled_until": dict(pool.disabled_until), "next_quality_retry": next_retry,
            "codex_worker_cutoff_remaining": 25, "codex_reserved_weekly_percent": 20})
        outcomes = runner.run(selected) if selected and can_pair else {}
        if outcomes:
            for page in selected:
                if not runner.is_up_to_date(page):
                    retry_after[page] = time.time() + 3600
        remaining = sum(not runner.is_up_to_date(p) for p in pages)
        state = {"pid": os.getpid(), "updated_at": now(), "remaining": remaining,
                 "reviewed": len(pages) - remaining, "total": len(pages), "last_batch": outcomes,
                 "disabled": dict(pool.disabled), "disabled_until": dict(pool.disabled_until),
                 "next_quality_retry": next_retry, "codex_worker_cutoff_remaining": 25,
                 "page_retry_after": retry_after,
                 "codex_reserved_weekly_percent": 20,
                 "status": "translation_complete_needs_final_validation" if not remaining else "running",
                 "log": str(log.path.relative_to(root))}
        atomic_write_json(previous, state)
        print(json.dumps(state, ensure_ascii=False), flush=True)
        if not remaining:
            # Final publication remains gated on full site/UI/license checks.
            break
        if not outcomes or not any(outcomes.get(k) for k in ("reviewed", "translated")):
            stop.wait(300)
    lock.close()


if __name__ == "__main__":
    main()
