#!/usr/bin/env python3
"""zh-TW translation pipeline for the OpenSearch documentation.

Commands:
  init     Enumerate baseline pages, store immutable sources, create/extend the manifest.
  status   Print aggregate progress (no model calls).
  run      Translate and review pages with the configured model CLIs.
  check    Fail-closed publish check (no model calls).

See translation/README.md for details.
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from translation_pipeline import config  # noqa: E402
from translation_pipeline.checks import run_check  # noqa: E402
from translation_pipeline.pipeline import (InitError, Runner, RunOptions, init,  # noqa: E402
                                           resolve_page)
from translation_pipeline.prompts import PromptContext  # noqa: E402
from translation_pipeline.providers import ProviderPool, build_providers  # noqa: E402
from translation_pipeline.store import Cache, Manifest, RunLog, sha256_bytes  # noqa: E402
from translation_pipeline.terms import TermRules  # noqa: E402

KNOWN_PROVIDERS = ("claude", "agy", "ollama-cloud", "ollama-local", "codex", "codex-review")


def _provider_list(value: str) -> list[str]:
    names = [v.strip() for v in value.split(",") if v.strip()]
    unknown = [n for n in names if n not in KNOWN_PROVIDERS and n != "none"]
    if unknown:
        raise argparse.ArgumentTypeError(f"unknown provider(s): {', '.join(unknown)}")
    return [] if names == ["none"] else names


def _paths_arg(values: list[str] | None) -> list[str]:
    out: list[str] = []
    for value in values or []:
        out += [v for v in value.split(",") if v.strip()]
    return out


def _requested(args) -> list[str] | None:
    """Pages named by --pilot or --paths (mutually exclusive), or None for all."""
    if args.pilot:
        return list(config.PILOT_PATHS)
    return _paths_arg(args.paths) or None


def cmd_init(args, root: Path) -> int:
    try:
        result = init(root, args.baseline)
    except InitError as exc:
        print(f"init failed: {exc}", file=sys.stderr)
        return 1
    print(f"init: {result['pages']} pages at baseline {args.baseline[:12]} ({result['added']} added to manifest; "
          f"source inventory {config.SOURCE_INVENTORY_PATH})")
    return 0


def _page_state(root: Path, page: str, entry: dict) -> str:
    status = entry.get("status")
    if status in ("translated", "reviewed"):
        path = root / page
        if not path.is_file() or sha256_bytes(path.read_bytes()) != entry.get("target_sha256"):
            return "stale"
        if entry.get("translated_source_sha256") != entry.get("source_sha256"):
            return "stale"
    return status


def cmd_status(args, root: Path) -> int:
    try:
        manifest = Manifest.load(root)
    except (OSError, ValueError) as exc:
        print(f"status: cannot load manifest ({exc}); run `init` first", file=sys.stderr)
        return 1
    pages = manifest.pages
    selected = sorted(pages)
    requested = _requested(args)
    if requested is not None:
        selected = list(dict.fromkeys(p for p in (resolve_page(manifest, r)[0] for r in requested) if p))
    counts: dict[str, int] = {}
    errors = exhausted = 0
    for page in selected:
        entry = pages[page]
        state = _page_state(root, page, entry)
        counts[state] = counts.get(state, 0) + 1
        errors += bool(entry.get("last_error"))
        exhausted += entry.get("attempts", 0) >= config.MAX_PAGE_ATTEMPTS and state != "reviewed"
    if args.json:
        print(json.dumps({"total": len(selected), "counts": counts, "with_errors": errors,
                          "attempts_exhausted": exhausted,
                          "baseline_commit": manifest.data.get("baseline_commit")}, indent=1))
    else:
        order = ("reviewed", "translated", "pending", "stale")
        parts = [f"{k}={counts.get(k, 0)}" for k in order] + \
                [f"{k}={v}" for k, v in sorted(counts.items()) if k not in order]
        print(f"pages={len(selected)} " + " ".join(parts) + f" with_errors={errors} attempts_exhausted={exhausted}")
        if args.verbose:
            for page in selected:
                entry = pages[page]
                line = f"{_page_state(root, page, entry):10} attempts={entry.get('attempts', 0)} {page}"
                if entry.get("last_error"):
                    line += f"  [{entry['last_error'][:120]}]"
                print(line)
    return 0


def cmd_run(args, root: Path) -> int:
    import fcntl
    directory = root / config.CACHE_DIR
    directory.mkdir(exist_ok=True)
    with (directory / 'translation-run.lock').open('a') as lock:
        try:
            fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError:
            print('run: another translation runner owns the manifest', file=sys.stderr)
            return 2
        return _cmd_run(args, root)


def _cmd_run(args, root: Path) -> int:
    try:
        manifest = Manifest.load(root)
    except (OSError, ValueError) as exc:
        print(f"run: cannot load manifest ({exc}); run `init` first", file=sys.stderr)
        return 1
    translators = args.translator or list(config.DEFAULT_TRANSLATORS)
    reviewers = args.reviewer if args.reviewer is not None else list(config.DEFAULT_REVIEWERS)
    bad = [r for r in reviewers if r not in config.REVIEW_APPROVED_PROVIDERS]
    if bad:
        print(f"run: {', '.join(bad)} is not a quality-approved review backend "
              f"(allowed: {', '.join(sorted(config.REVIEW_APPROVED_PROVIDERS))}, or none)", file=sys.stderr)
        return 2
    if args.workers < 1 or args.workers > config.MAX_WORKERS:
        print(f"run: --workers must be between 1 and {config.MAX_WORKERS}", file=sys.stderr)
        return 2
    requested = _requested(args)
    if requested is not None:
        pages = []
        for item in requested:
            page, note = resolve_page(manifest, item)
            if note:
                print(f"note: {note}")
            if page is None:
                return 2
            if page not in pages:
                pages.append(page)
    else:
        priority = {name: index for index, name in enumerate([
            "index.md", "search.md", "404.md", "_getting-started", "_install-and-configure",
            "_dashboards", "_security", "_mappings", "_query-dsl", "_api-reference"
        ])}
        pages = sorted(manifest.pages, key=lambda page: (priority.get(page.split("/", 1)[0], len(priority)), page))
    run_id = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    cache = Cache(root)
    log = RunLog(None if args.dry_run else cache.log_path(run_id))
    pool = ProviderPool(build_providers(claude_model=args.claude_model),
                        stop_on_quota=args.stop_on_quota, log=log)
    runner = Runner(root, manifest, pool, PromptContext.load(root), TermRules.load(root / config.BANNED_TERMS_PATH),
                    RunOptions(translators, reviewers, args.workers, args.dry_run, args.reset_attempts), log)
    selected = runner.select(pages, args.limit)
    if not selected:
        print("run: nothing to do (selected pages are reviewed and current, or out of attempts)")
        return 0
    print(f"run: {len(selected)} page(s); translators={','.join(translators)} "
          f"reviewers={','.join(reviewers) or 'none'} workers={args.workers}")
    counts = runner.run(selected)
    if pool.disabled:
        print("providers disabled: " + ", ".join(f"{k} ({v})" for k, v in sorted(pool.disabled.items())))
    for name, agg in sorted(pool.usage.items()):
        reported = " ".join(f"{k}={v}" for k, v in sorted(agg["reported"].items())) or "none"
        line = f"usage {name}: calls={agg['calls']} reported({agg['calls_with_usage']} calls): {reported}"
        if agg["estimated"]:
            line += " | CLI estimate (not billed usage): " + \
                " ".join(f"{k}={round(v, 4)}" for k, v in sorted(agg["estimated"].items()))
        print(line)
    if log.path:
        print(f"log: {log.path.relative_to(root)}")
    if counts.get("stopped"):
        return 3
    return 1 if counts.get("failed") else 0


def cmd_check(args, root: Path) -> int:
    paths = _requested(args)
    if args.complete and (args.allow_incomplete or paths):
        print("check: --complete covers every page; it cannot be combined with --allow-incomplete, "
              "--pilot or --paths", file=sys.stderr)
        return 2
    publish = not args.allow_incomplete
    report = run_check(root, TermRules.load(root / config.BANNED_TERMS_PATH), publish=publish, paths=paths)
    counts = " ".join(f"{k}={v}" for k, v in sorted(report.counts.items()))
    # A subset that passes with reviews required is not the site publish gate.
    mode = ("publish" if not paths else "selected pages, review required") if publish else "integrity"
    if report.ok:
        print(f"check ({mode}): OK pages={report.total} {counts}")
        return 0
    print(f"check ({mode}): FAILED pages={report.total} {counts} problems={len(report.problems)}")
    limit = None if args.verbose else 20
    for problem in report.problems[:limit]:
        print(f"  - {problem}")
    if limit and len(report.problems) > limit:
        print(f"  ... {len(report.problems) - limit} more (use --verbose)")
    return 1


def _selection_args(parser: argparse.ArgumentParser, note: str = "") -> None:
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--pilot", action="store_true", help="only the pilot pages" + note)
    group.add_argument("--paths", action="append", help="comma-separated page paths (repeatable)" + note)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--root", type=Path, default=config.repo_root(), help=argparse.SUPPRESS)
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("init", help="store baseline sources and create/extend the manifest")
    p.add_argument("--baseline", default=config.BASELINE_COMMIT, help="baseline commit (default: %(default)s)")
    p.set_defaults(func=cmd_init)

    p = sub.add_parser("status", help="aggregate progress")
    _selection_args(p)
    p.add_argument("--json", action="store_true")
    p.add_argument("--verbose", "-v", action="store_true", help="one line per page")
    p.set_defaults(func=cmd_status)

    p = sub.add_parser("run", help="translate and review pages")
    _selection_args(p)
    p.add_argument("--limit", type=int, help="process at most N pages that need work")
    p.add_argument("--workers", type=int, default=1, help=f"parallel pages, 1-{config.MAX_WORKERS}")
    p.add_argument("--translator", type=_provider_list,
                   help=f"comma-separated translator chain (default: {','.join(config.DEFAULT_TRANSLATORS)})")
    p.add_argument("--reviewer", type=_provider_list,
                   help=f"comma-separated reviewer chain or 'none' (default: {','.join(config.DEFAULT_REVIEWERS)})")
    p.add_argument("--stop-on-quota", "--run-stop-on-quota", dest="stop_on_quota", action="store_true",
                   help="stop scheduling new work as soon as any provider reports a quota limit")
    p.add_argument("--reset-attempts", action="store_true", help="reset the attempt counter of selected pages")
    p.add_argument("--dry-run", action="store_true", help="show the work plan without model calls or writes")
    p.add_argument("--claude-model", help="model passed to `claude --model` (default: account default)")
    p.set_defaults(func=cmd_run)

    p = sub.add_parser("check", help="fail-closed publish check")
    p.add_argument("--complete", action="store_true",
                   help="require every page to be reviewed (the default; kept for CI callers)")
    p.add_argument("--allow-incomplete", action="store_true",
                   help="integrity check only: pending/translated pages are allowed")
    _selection_args(p, " (checked with review required unless --allow-incomplete; the page set "
                       "is always checked in full)")
    p.add_argument("--verbose", "-v", action="store_true", help="list every problem")
    p.set_defaults(func=cmd_check)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    return args.func(args, args.root.resolve())


if __name__ == "__main__":
    sys.exit(main())
