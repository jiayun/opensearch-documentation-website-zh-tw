import contextlib
import io
import json
import tempfile
import unittest
from pathlib import Path
from unittest import mock

import yaml

from test_translation_helpers import (INDEX_PAGE, LANDING_PAGE, MATCH_PAGE, NOTICE, FakeProvider, approve, config,
                                      good_translation, make_repo, request_payload)

import translation as cli
from translation_pipeline.checks import run_check
from translation_pipeline.frontmatter import split_document, translatable_fields
from translation_pipeline.pipeline import InitError, Runner, RunOptions, init, resolve_page
from translation_pipeline.prompts import PromptContext
from translation_pipeline.protect import fenced_blocks
from translation_pipeline.providers import QUOTA, TRANSPORT, ProviderError, ProviderPool
from translation_pipeline.store import Cache, Manifest, RunLog, SourceInventory, SourceStore, sha256_bytes
from translation_pipeline.terms import TermRules

MATCH = "_docs/match.md"
INDEX = "_getting-started/index.md"
BIG = "_docs/big.md"
LANDING = "_docs/landing.md"
ALL = [MATCH, INDEX, BIG, LANDING, "index.md"]


def big_page() -> str:
    sections = []
    for i in range(12):
        sections.append(f"## Section {i}\n\n" + ("This paragraph explains the setting in detail. " * 60) +
                        f"\n\n```json\n{{\"section\": {i}}}\n```\n")
    return "---\ntitle: Big page\nparent: Docs\n---\n\n# Big page\n\n" + "\n".join(sections)


def reject(prompt: str) -> str:
    return json.dumps({"approved": False, "issues": [
        {"id": "section.001", "severity": "major", "problem": "Mistranslated heading",
         "suggestion": "使用「參數」"}]})


class PipelineTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.commit = make_repo(self.root, {
            MATCH: MATCH_PAGE,
            INDEX: INDEX_PAGE,
            BIG: big_page(),
            LANDING: LANDING_PAGE,
            "_docs/static.md": "no front matter, so Jekyll copies it as a static file\n",
            "_hidden/secret.md": "---\ntitle: Hidden\n---\nnot rendered\n",
            "index.md": "---\ntitle: Home\nlayout: home\n---\n\n{% include banner.html %}\n",
            "README.md": "# Repo readme\n",
        })
        patcher = mock.patch.object(config, "BASELINE_COMMIT", self.commit)
        patcher.start()
        self.addCleanup(patcher.stop)
        self.addCleanup(self.tmp.cleanup)
        init(self.root, self.commit)
        self.rules = TermRules.load(self.root / config.BANNED_TERMS_PATH)

    # -- helpers -------------------------------------------------------------------
    def runner(self, translators, reviewers, **options):
        providers = {p.name: p for p in list(translators) + list(reviewers)}
        log = RunLog(self.root / config.CACHE_DIR / "logs" / "test.jsonl")
        pool = ProviderPool(providers, log=log, sleep=lambda s: None,
                            stop_on_quota=options.pop("stop_on_quota", False))
        return Runner(self.root, Manifest.load(self.root), pool, PromptContext.load(self.root), self.rules,
                      RunOptions([p.name for p in translators], [p.name for p in reviewers], **options),
                      log, progress=lambda s: None)

    def claude(self, handler=None):
        return FakeProvider("claude", "claude", handler or (lambda p, n: good_translation(p)))

    def agy(self, handler=None):
        return FakeProvider("agy", "agy", handler or (lambda p, n: approve(p)))

    def entry(self, page):
        return Manifest.load(self.root).pages[page]

    def read(self, page):
        return (self.root / page).read_text(encoding="utf-8")

    # -- init ----------------------------------------------------------------------
    def test_init_enumerates_output_collections_and_root_pages(self):
        manifest = Manifest.load(self.root)
        self.assertEqual(set(manifest.pages), set(ALL))
        inventory = SourceInventory.load(self.root)
        self.assertEqual(inventory.pages, {p: e["source_sha256"] for p, e in manifest.pages.items()})
        self.assertEqual(inventory.data["baseline_commit"], self.commit)
        entry = manifest.pages[MATCH]
        self.assertEqual(entry["status"], "pending")
        self.assertEqual(entry["original_front_matter"],
                         {"title": "Match query", "parent": "Full-text queries", "grand_parent": "Query DSL"})
        self.assertEqual(SourceStore(self.root).read(MATCH), MATCH_PAGE.encode())
        self.assertEqual(entry["source_sha256"], sha256_bytes(MATCH_PAGE.encode()))
        before = (self.root / config.MANIFEST_PATH).read_bytes()
        init(self.root, self.commit)
        self.assertEqual((self.root / config.MANIFEST_PATH).read_bytes(), before, "init is idempotent")

    def test_check_fails_closed_until_everything_is_reviewed(self):
        report = run_check(self.root, self.rules, publish=True)
        self.assertFalse(report.ok)
        self.assertTrue(any("pending" in p for p in report.problems))
        self.assertTrue(run_check(self.root, self.rules, publish=False).ok)

    # -- happy path --------------------------------------------------------------------
    def test_run_translates_reviews_and_passes_publish_check(self):
        claude, agy = self.claude(), self.agy()
        runner = self.runner([claude], [agy], workers=2)
        counts = runner.run(runner.select(sorted(runner.manifest.pages), None))
        self.assertEqual(counts, {"reviewed": 5})
        text = self.read(MATCH)
        self.assertEqual(fenced_blocks(text), fenced_blocks(MATCH_PAGE))
        self.assertIn("parent: Full-text queries\n", text)
        self.assertIn("{{site.url}}{{site.baseurl}}/query-dsl/", text)
        self.assertIn("{% include copy-curl.html %}", text)
        self.assertIn("`match`", text)
        self.assertNotIn("title: Match query", text)
        index = self.read(INDEX)
        self.assertIn('link: /getting-started/intro/', index)
        self.assertIn("permalink: /getting-started/", index)
        entry = self.entry(MATCH)
        self.assertEqual(entry["status"], "reviewed")
        self.assertEqual(entry["target_sha256"], sha256_bytes(text.encode()))
        self.assertEqual(entry["reviewer"]["provider"], "agy")
        self.assertEqual(entry["reviewer"]["target_sha256"], entry["target_sha256"])
        self.assertEqual(entry["translator"]["providers"][0]["provider"], "claude")
        self.assertEqual(entry["original_front_matter"]["title"], "Match query")
        self.assertTrue(text.startswith("---\n" + NOTICE + "\nlayout: default\n"))
        self.assertEqual(text.count(NOTICE), 1)
        self.assertTrue(run_check(self.root, self.rules, publish=True).ok)
        self.assertEqual(runner.select(sorted(runner.manifest.pages), None), [], "reviewed pages are skipped")

    def test_large_page_is_chunked(self):
        claude = self.claude()
        runner = self.runner([claude], [self.agy()])
        self.assertEqual(runner.run([BIG]), {"reviewed": 1})
        self.assertGreater(len(claude.calls), 1)
        for prompt in claude.calls:
            for segment in request_payload(prompt)["segments"]:
                self.assertLessEqual(len(segment["text"]), config.CHUNK_LIMIT)
        self.assertEqual(fenced_blocks(self.read(BIG)), fenced_blocks(big_page()))

    def test_segments_without_prose_skip_the_model(self):
        from translation_pipeline.pipeline import build_work
        text = "---\ntitle: '2.0'\nparent: Docs\n---\n\n```json\n{\"a\": 1}\n```\n"
        work = build_work("_docs/code.md", text.encode(), sha256_bytes(text.encode()))
        claude = self.claude()
        runner = self.runner([claude], [self.agy()])
        self.assertEqual([runner._chunk_request(work, c) for c in work.chunks], [[]])
        self.assertEqual(runner.translate(work, {}).text, text.replace("---\n", "---\n" + NOTICE + "\n", 1))
        self.assertEqual(claude.calls, [])

    # -- malformed model output ------------------------------------------------------------
    def test_truncated_reply_is_retried(self):
        claude = self.claude(lambda p, n: '{"segments": [{"id": "fm.title", "text": "未完' if n == 1
                             else good_translation(p))
        runner = self.runner([claude], [self.agy()])
        self.assertEqual(runner.run([MATCH]), {"reviewed": 1})
        self.assertIn("truncated", json.dumps(request_payload(claude.calls[1])["previous_issues"]))

    def test_incomplete_reply_and_dropped_placeholder_are_retried(self):
        def handler(prompt, n):
            answer = json.loads(good_translation(prompt))
            if n == 1:
                answer["segments"] = answer["segments"][1:]           # drop fm.title
            elif n == 2:
                seg = answer["segments"][-1]
                seg["text"] = seg["text"].replace("⟦P", "⟦X", 1)    # corrupt a placeholder
            return json.dumps(answer, ensure_ascii=False)
        claude = self.claude(handler)
        runner = self.runner([claude], [self.agy()])
        self.assertEqual(runner.run([MATCH]), {"reviewed": 1})
        issues2 = json.dumps(request_payload(claude.calls[1])["previous_issues"], ensure_ascii=False)
        issues3 = json.dumps(request_payload(claude.calls[2])["previous_issues"], ensure_ascii=False)
        self.assertIn("missing segments", issues2)
        self.assertIn("placeholder", issues3)
        self.assertEqual(fenced_blocks(self.read(MATCH)), fenced_blocks(MATCH_PAGE))

    def test_banned_terms_in_reply_are_retried(self):
        claude = self.claude(lambda p, n: good_translation(p).replace("譯", "軟件", 1) if n == 1
                             else good_translation(p))
        runner = self.runner([claude], [self.agy()])
        self.assertEqual(runner.run([MATCH]), {"reviewed": 1})
        self.assertIn("軟件", json.dumps(request_payload(claude.calls[1])["previous_issues"], ensure_ascii=False))
        self.assertNotIn("軟件", self.read(MATCH))

    # -- provider failures -------------------------------------------------------------------
    def test_quota_falls_back_and_reviewer_stays_distinct(self):
        claude = self.claude(lambda p, n: ProviderError(QUOTA, "Claude AI usage limit reached"))
        ollama = FakeProvider("ollama-cloud", "ollama", lambda p, n: good_translation(p))
        agy = self.agy()
        runner = self.runner([claude, ollama], [agy])
        self.assertEqual(runner.run([MATCH, INDEX]), {"reviewed": 2})
        self.assertEqual(len(claude.calls), 1, "quota-limited provider is stopped")
        entry = self.entry(MATCH)
        self.assertEqual(entry["translator"]["providers"][0]["provider"], "ollama-cloud")
        self.assertEqual(entry["reviewer"]["provider"], "agy")

    def test_reviewer_never_reviews_its_own_translation(self):
        runner = self.runner([self.claude()], [self.claude()])
        self.assertEqual(runner.run([MATCH]), {"translated": 1})
        self.assertIsNone(self.entry(MATCH)["reviewer"])

    def test_no_review_backend_marks_translated_then_review_later(self):
        agy = self.agy(lambda p, n: ProviderError(QUOTA, "429 RESOURCE_EXHAUSTED"))
        runner = self.runner([self.claude()], [agy])
        self.assertEqual(runner.run([MATCH]), {"translated": 1})
        self.assertEqual(self.entry(MATCH)["status"], "translated")
        report = run_check(self.root, self.rules, publish=True)
        self.assertTrue(any(MATCH in p and "not reviewed" in p for p in report.problems))
        self.assertTrue(run_check(self.root, self.rules, publish=False).ok)
        claude2, agy2 = self.claude(), self.agy()
        runner = self.runner([claude2], [agy2])
        self.assertEqual(runner.run(runner.select([MATCH], None)), {"reviewed": 1})
        self.assertEqual(claude2.calls, [], "review-only resume does not retranslate")
        self.assertEqual(len(agy2.calls), 1)

    def test_transport_failures_retry_then_fail_without_switching(self):
        claude = self.claude(lambda p, n: ProviderError(TRANSPORT, "socket hang up"))
        ollama = FakeProvider("ollama-cloud", "ollama", lambda p, n: good_translation(p))
        runner = self.runner([claude, ollama], [self.agy()])
        self.assertEqual(runner.run([MATCH]), {"failed": 1})
        self.assertEqual(len(claude.calls), 1 + config.TRANSPORT_RETRIES)
        self.assertEqual(ollama.calls, [])
        entry = self.entry(MATCH)
        self.assertEqual((entry["status"], entry["attempts"]), ("pending", 0))
        self.assertIn("transport", entry["last_error"])
        self.assertEqual(self.read(MATCH), MATCH_PAGE)

    def test_stop_on_quota_stops_new_work(self):
        claude = self.claude(lambda p, n: ProviderError(QUOTA, "usage limit reached"))
        ollama = FakeProvider("ollama-cloud", "ollama", lambda p, n: good_translation(p))
        runner = self.runner([claude, ollama], [self.agy()], stop_on_quota=True)
        self.assertEqual(runner.run([MATCH, INDEX]), {"stopped": 2})
        self.assertEqual(ollama.calls, [])

    # -- review rejection ------------------------------------------------------------------------
    def test_rejection_retranslates_with_findings(self):
        agy = self.agy(lambda p, n: reject(p) if n == 1 else approve(p))
        claude = self.claude()
        runner = self.runner([claude], [agy])
        self.assertEqual(runner.run([MATCH]), {"reviewed": 1})
        self.assertEqual(self.entry(MATCH)["attempts"], 2)
        self.assertIn("Mistranslated heading", json.dumps(request_payload(claude.calls[-1])["previous_issues"]))
        repair = request_payload(claude.calls[-1])
        self.assertEqual(repair['metadata']['task'], 'repair')
        self.assertTrue(all('draft' in segment for segment in repair['segments']))
        self.assertEqual([segment['id'] for segment in repair['segments']], ['body.001'])
        self.assertNotIn('## Parameters', repair['segments'][0]['text'])
        review_items = request_payload(agy.calls[0])["items"]
        self.assertTrue(any("```json" in item["source"] for item in review_items), "reviewer sees full original")
        self.assertTrue(any("```json" in item["translation"] for item in review_items))

    def test_section_repair_keeps_unaffected_draft_bytes_and_full_review(self):
        def reviewer(prompt, number):
            if number == 1:
                return json.dumps({'approved': False, 'issues': [{'id': 'section.002', 'severity': 'major',
                    'problem': 'Correct the parameter heading', 'suggestion': 'Use 參數說明'}]})
            return approve(prompt)
        drafts = []
        def translator(prompt, number):
            payload = request_payload(prompt)
            if payload['metadata'].get('task') == 'repair':
                self.assertEqual([s['id'] for s in payload['segments']], ['body.002'])
                return json.dumps({'segments': [{'id': s['id'], 'text': s['draft'].replace('## 譯', '## 參數說明', 1)}
                                                for s in payload['segments']]}, ensure_ascii=False)
            response = good_translation(prompt)
            drafts.append(response)
            return response
        claude, agy = self.claude(translator), self.agy(reviewer)
        runner = self.runner([claude], [agy])
        self.assertEqual(runner.run([MATCH]), {'reviewed': 1})
        first_items = request_payload(agy.calls[0])['items']
        last_items = request_payload(agy.calls[1])['items']
        for before, after in zip(first_items, last_items):
            if before['id'] != 'section.002':
                self.assertEqual(before['translation'], after['translation'])
        self.assertIn('## 參數說明', self.read(MATCH))
        self.assertEqual(len(claude.calls), 2)

    def test_null_review_location_falls_back_without_unsafe_section_patch(self):
        def reviewer(prompt, number):
            if number == 1:
                return json.dumps({'approved': False, 'issues': [{'id': None, 'severity': 'major',
                                                               'problem': 'Global consistency problem'}]})
            return approve(prompt)
        claude = self.claude()
        self.assertEqual(self.runner([claude], [self.agy(reviewer)]).run([MATCH]), {'reviewed': 1})
        self.assertNotEqual(request_payload(claude.calls[-1])['metadata'].get('task'), 'repair')

    def test_review_payload_explicitly_identifies_protected_legal_attribution(self):
        from translation_pipeline.pipeline import build_work
        notice = 'Tiles are generated per [Copyright and License for OpenStreetMap](https://www.openstreetmap.org/copyright).'
        baseline = '---\ntitle: License\n---\n\n# License\n\n' + notice + '\n'
        work = build_work('license.md', baseline.encode(), sha256_bytes(baseline.encode()))
        items = self.runner([self.claude()], [self.agy()]).review_items(work, baseline)
        self.assertTrue(any(notice in item.get('protected_legal_notices', []) for item in items))

    def test_rejection_is_bounded_and_leaves_file_untouched(self):
        runner = self.runner([self.claude()], [self.agy(lambda p, n: reject(p))])
        self.assertEqual(runner.run([MATCH]), {"failed": 1})
        entry = self.entry(MATCH)
        self.assertEqual((entry["status"], entry["attempts"]), ("pending", config.MAX_PAGE_ATTEMPTS))
        self.assertIn("rejected", entry["last_error"])
        self.assertEqual(self.read(MATCH), MATCH_PAGE)
        runner = self.runner([self.claude()], [self.agy()])
        self.assertEqual(runner.select([MATCH], None), [])
        runner = self.runner([self.claude()], [self.agy()], reset_attempts=True)
        self.assertEqual(runner.select([MATCH], None), [MATCH])

    # -- cache, invalidation, crash safety ------------------------------------------------------------
    def reset_to_pending(self, page, baseline):
        manifest = Manifest.load(self.root)
        manifest.pages[page].update(status="pending", target_sha256=None, reviewer=None, attempts=0)
        manifest.save()
        (self.root / page).write_text(baseline, encoding="utf-8")

    def test_chunk_cache_reuse_and_invalidation(self):
        runner = self.runner([self.claude()], [self.agy()])
        runner.run([MATCH])
        self.reset_to_pending(MATCH, MATCH_PAGE)
        claude, agy = self.claude(), self.agy()
        runner = self.runner([claude], [agy])
        self.assertEqual(runner.run([MATCH]), {"reviewed": 1})
        self.assertEqual((claude.calls, agy.calls), ([], []), "validated chunk and review results are reused")
        # Changing the glossary changes the prompt version and invalidates the cache.
        self.reset_to_pending(MATCH, MATCH_PAGE)
        with open(self.root / config.GLOSSARY_PATH, "a", encoding="utf-8") as handle:
            handle.write("  - {en: wind, zh: 風}\n")
        claude = self.claude()
        runner = self.runner([claude], [self.agy()])
        runner.run([MATCH])
        self.assertEqual(len(claude.calls), 1)

    def test_source_hash_change_invalidates_cache_and_translation(self):
        self.runner([self.claude()], [self.agy()]).run([MATCH])
        new_source = MATCH_PAGE.replace("specific document field", "specific field")
        SourceStore(self.root).write(MATCH, new_source.encode())
        manifest = Manifest.load(self.root)
        manifest.pages[MATCH]["source_sha256"] = sha256_bytes(new_source.encode())
        manifest.save()
        report = run_check(self.root, self.rules, publish=True)
        self.assertTrue(any("different source hash" in p for p in report.problems))
        claude = self.claude()
        runner = self.runner([claude], [self.agy()])
        self.assertEqual(runner.select([MATCH], None), [MATCH], "stale translation is selected again")
        self.assertEqual(runner.run([MATCH]), {"reviewed": 1})
        self.assertEqual(len(claude.calls), 1)
        self.assertEqual(self.entry(MATCH)["translated_source_sha256"], sha256_bytes(new_source.encode()))

    def test_crash_between_file_write_and_manifest_save_is_recovered(self):
        runner = self.runner([self.claude()], [self.agy()])
        original = runner.manifest.update

        def crash_on_commit(page, **fields):
            if "status" in fields:
                raise RuntimeError("simulated crash")
            return original(page, **fields)
        runner.manifest.update = crash_on_commit
        self.assertEqual(runner.run([MATCH]), {"failed": 1})
        self.assertNotEqual(self.read(MATCH), MATCH_PAGE, "file was written before the crash")
        self.assertEqual(self.entry(MATCH)["status"], "pending")
        self.assertIsNotNone(Cache(self.root).read_journal(MATCH))
        claude = self.claude()
        runner = self.runner([claude], [self.agy()])
        self.assertEqual(runner.run([MATCH]), {"skipped": 1})
        self.assertEqual(claude.calls, [])
        self.assertEqual(self.entry(MATCH)["status"], "reviewed")
        self.assertIsNone(Cache(self.root).read_journal(MATCH))
        self.assertTrue(run_check(self.root, self.rules, publish=False, paths=[MATCH]).ok)

    def test_interrupted_large_page_resumes_from_completed_chunks(self):
        def flaky(prompt, n):
            return good_translation(prompt) if n == 1 else ProviderError(TRANSPORT, "connection reset")
        first = self.claude(flaky)
        self.assertEqual(self.runner([first], [self.agy()]).run([BIG]), {"failed": 1})
        second = self.claude()
        self.assertEqual(self.runner([second], [self.agy()]).run([BIG]), {"reviewed": 1})
        total_chunks = len(second.calls) + 1
        self.assertGreater(total_chunks, 2)
        first_ids = {s["id"] for s in request_payload(first.calls[0])["segments"]}
        for prompt in second.calls:
            self.assertFalse(first_ids & {s["id"] for s in request_payload(prompt)["segments"]})

    def test_agy_claude_cannot_review_direct_claude_translation(self):
        sonnet = FakeProvider('agy-sonnet', 'claude', lambda p, n: approve())
        opus = FakeProvider('agy-opus', 'claude', lambda p, n: approve())
        gemini = self.agy()
        self.assertEqual(self.runner([self.claude()], [sonnet, opus, gemini]).run([MATCH]), {'reviewed': 1})
        self.assertEqual(sonnet.calls, [])
        self.assertEqual(opus.calls, [])
        self.assertTrue(gemini.calls)

    def test_drifted_file_is_never_overwritten(self):
        (self.root / MATCH).write_text(MATCH_PAGE + "\nHand edit.\n", encoding="utf-8")
        claude = self.claude()
        self.assertEqual(self.runner([claude], [self.agy()]).run([MATCH]), {"failed": 1})
        self.assertEqual(claude.calls, [])
        self.assertTrue(self.read(MATCH).endswith("Hand edit.\n"))
        self.assertIn("refusing to overwrite", self.entry(MATCH)["last_error"])

    def test_retry_resumes_rejected_draft_and_repairs_before_full_review(self):
        first = self.runner([self.claude()], [self.agy(lambda p, n: reject(p))])
        with mock.patch.object(config, "MAX_PAGE_ATTEMPTS", 1):
            self.assertEqual(first.run([MATCH]), {"failed": 1})
        saved = first.cache.get("pending-repairs", Cache.key(MATCH, self.entry(MATCH)["source_sha256"]))
        self.assertTrue(saved["translator"]["providers"])
        self.assertFalse(saved["review"]["approved"])
        translator, reviewer = self.claude(), self.agy()
        second = self.runner([translator], [reviewer], reset_attempts=True)
        from translation_pipeline.pipeline import Candidate
        with mock.patch.object(second, "repair", return_value=Candidate(saved["text"], saved["translator"])) as repair:
            self.assertEqual(second.run([MATCH]), {"reviewed": 1})
        repair.assert_called_once()
        self.assertEqual(translator.calls, [])
        self.assertEqual(len(reviewer.calls), 1, "resumption still requires independent full review")

    def test_changed_policy_rereviews_saved_draft_without_reusing_issue_ids(self):
        first = self.runner([self.claude()], [self.agy(lambda p, n: reject(p))])
        with mock.patch.object(config, "MAX_PAGE_ATTEMPTS", 1):
            first.run([MATCH])
        translator, reviewer = self.claude(), self.agy()
        second = self.runner([translator], [reviewer], reset_attempts=True)
        second.prompts.version = "changed-policy"
        with mock.patch.object(second, "repair") as repair:
            self.assertEqual(second.run([MATCH]), {"reviewed": 1})
        repair.assert_not_called()
        self.assertEqual(translator.calls, [])
        self.assertEqual(len(reviewer.calls), 1)

    def test_rejected_checkpoint_with_changed_code_is_not_resumed(self):
        first = self.runner([self.claude()], [self.agy(lambda p, n: reject(p))])
        with mock.patch.object(config, "MAX_PAGE_ATTEMPTS", 1):
            first.run([MATCH])
        key = Cache.key(MATCH, self.entry(MATCH)["source_sha256"])
        saved = first.cache.get("pending-repairs", key)
        saved["text"] = saved["text"].replace('"wind"', '"breeze"')
        first.cache.put("pending-repairs", key, saved)
        second = self.runner([self.claude()], [self.agy()], reset_attempts=True)
        with mock.patch.object(second, "repair") as repair, mock.patch.object(second, "translate", wraps=second.translate) as translate:
            self.assertEqual(second.run([MATCH]), {"reviewed": 1})
        repair.assert_not_called()
        translate.assert_called_once()

    # -- publish check tampering ---------------------------------------------------------------------
    def test_check_detects_tampering_and_bad_provenance(self):
        self.runner([self.claude()], [self.agy()]).run(ALL)
        self.assertTrue(run_check(self.root, self.rules).ok)
        path = self.root / MATCH
        good = path.read_text(encoding="utf-8")

        def set_file(text):
            path.write_text(text, encoding="utf-8")
            manifest = Manifest.load(self.root)
            manifest.pages[MATCH]["target_sha256"] = manifest.pages[MATCH]["reviewer"]["target_sha256"] = \
                sha256_bytes(text.encode())
            manifest.save()

        path.write_text(good + "\n", encoding="utf-8")
        self.assertTrue(any("target_sha256" in p for p in run_check(self.root, self.rules).problems))
        cases = {
            "fenced code": good.replace('"wind"', '"breeze"'),
            "terminology": good.replace("譯", "軟件", 1),
            "parent": good.replace("parent: Full-text queries", "parent: 全文查詢"),
            "Liquid": good.replace("{% include copy-curl.html %}", ""),
            "heading": good.replace("## ", "### ", 1),
            "notice": good.replace(NOTICE + "\n", ""),
            "front matter link": good.replace("parent: Full-text queries", "parent: Full-text queries\nlink: /x/"),
        }
        for label, text in cases.items():
            set_file(text)
            problems = " ".join(run_check(self.root, self.rules).problems)
            self.assertTrue(problems, label)
        set_file(good)
        manifest = Manifest.load(self.root)
        manifest.pages[MATCH]["reviewer"]["family"] = "claude"
        manifest.save()
        self.assertTrue(any("not distinct" in p for p in run_check(self.root, self.rules).problems))

    # -- path resolution and CLI ---------------------------------------------------------------------------
    def test_resolve_page(self):
        manifest = Manifest.load(self.root)
        self.assertEqual(resolve_page(manifest, "./_docs/match")[0], MATCH)
        page, note = resolve_page(manifest, "_docs/missing-topic.md")
        self.assertIn(page, manifest.pages)
        self.assertIn("same-topic", note)
        self.assertIsNone(resolve_page(manifest, "_nowhere/x.md")[0])

    def test_cli_status_and_check_exit_codes(self):
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            self.assertEqual(cli.main(["--root", str(self.root), "status"]), 0)
            self.assertEqual(cli.main(["--root", str(self.root), "check", "--complete"]), 1)
            self.assertEqual(cli.main(["--root", str(self.root), "check", "--allow-incomplete"]), 0)
            self.assertEqual(cli.main(["--root", str(self.root), "run", "--paths", MATCH, "--dry-run",
                                       "--reviewer", "agy"]), 0)
        self.assertIn("pages=5 reviewed=0 translated=0 pending=5", out.getvalue())
        with contextlib.redirect_stderr(io.StringIO()), contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(cli.main(["--root", str(self.root), "run", "--pilot"]), 2,
                             "unresolvable pilot paths abort before any model call")
            self.assertEqual(cli.main(["--root", str(self.root), "run", "--reviewer", "ollama-cloud"]), 2)
            self.assertEqual(cli.main(["--root", str(self.root), "run", "--workers", str(config.MAX_WORKERS + 1)]), 2)

    def test_cli_pilot_and_paths_selection(self):
        root = ["--root", str(self.root)]
        out = io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(io.StringIO()):
            self.assertEqual(cli.main(root + ["status", "--pilot"]), 0)
            self.assertEqual(cli.main(root + ["check", "--pilot"]), 1, "pilot pages are not in this repo")
            self.assertEqual(cli.main(root + ["check", "--paths", MATCH]), 1, "pending page, review required")
            self.assertEqual(cli.main(root + ["check", "--paths", MATCH, "--allow-incomplete"]), 0)
            self.assertEqual(cli.main(root + ["check", "--complete", "--pilot"]), 2)
            self.assertEqual(cli.main(root + ["check", "--complete", "--paths", MATCH]), 2)
            for command in ("status", "run", "check"):
                with self.assertRaises(SystemExit) as ctx:
                    cli.main(root + [command, "--pilot", "--paths", MATCH])
                self.assertEqual(ctx.exception.code, 2, command)
            with self.assertRaises(SystemExit):
                cli.main(root + ["run", "--agy-prompt-via", "stdin"])
        self.assertIn("pages=1 ", out.getvalue(), "only _getting-started/index.md of the pilot exists here")
        self.runner([self.claude()], [self.agy()]).run([MATCH])
        with contextlib.redirect_stdout(io.StringIO()) as out:
            self.assertEqual(cli.main(root + ["check", "--paths", MATCH]), 0)
            self.assertEqual(cli.main(root + ["check"]), 1, "the publish gate still needs every page")
        self.assertIn("selected pages, review required", out.getvalue())

    # -- landing pages, notice, inventory ------------------------------------------------------------
    def test_landing_page_cards_are_translated_and_structure_kept(self):
        claude = self.claude()
        self.assertEqual(self.runner([claude], [self.agy()]).run([LANDING]), {"reviewed": 1})
        sent = {s["id"]: s["text"] for s in request_payload(claude.calls[0])["segments"]}
        self.assertIn("fm.flows.0.list.0", sent)
        self.assertNotIn("<b>", sent["fm.flows.0.list.0"], "inline HTML is sent as placeholders")
        text = self.read(LANDING)
        base, data = yaml.safe_load(LANDING_PAGE.split("---\n")[1]), split_document(text).data
        self.assertEqual([c["link"] for c in data["more_cards"]], [c["link"] for c in base["more_cards"]])
        self.assertEqual(data["flows"][0]["list"][0], "<b>譯:</b> 譯")
        self.assertIn("{{site.url}}{{site.baseurl}}/vector-search/", data["more_cards"][0]["description"])
        self.assertEqual(data["features"][0]["image_alt"], "譯 譯")
        self.assertEqual(data["redirect_from"], ["/tutorials/old/"])
        self.assertIn("# Cards rendered by the landing layout.\n", text)
        self.assertTrue(all("譯" in v for v in translatable_fields(data).values()))
        self.assertTrue(run_check(self.root, self.rules, publish=False).ok)

    def test_check_rejects_landing_page_structure_changes(self):
        self.runner([self.claude()], [self.agy()]).run([LANDING])
        path = self.root / LANDING
        good = path.read_text(encoding="utf-8")

        def problems_for(text):
            path.write_text(text, encoding="utf-8")
            manifest = Manifest.load(self.root)
            manifest.pages[LANDING]["target_sha256"] = manifest.pages[LANDING]["reviewer"]["target_sha256"] = \
                sha256_bytes(text.encode())
            manifest.save()
            return " ".join(run_check(self.root, self.rules, publish=False, paths=[LANDING]).problems)
        doc = split_document(good)
        for label, mutate in {
            "nested link": lambda d: d["more_cards"][0].update(link="/zh/"),
            "card order": lambda d: d["more_cards"].reverse(),
            "card count": lambda d: d["features"].pop(),
            "list count": lambda d: d["flows"][0]["list"].pop(),
            "inline HTML": lambda d: d["flows"][0]["list"].__setitem__(0, "平台： 譯"),
            "empty field": lambda d: d["more_cards"][1].update(heading=""),
        }.items():
            data = yaml.safe_load(doc.raw)
            mutate(data)
            raw = NOTICE + "\n" + yaml.safe_dump(data, allow_unicode=True, sort_keys=False)
            self.assertTrue(problems_for("---\n" + raw + "---\n" + doc.body), label)
        self.assertEqual(problems_for(good), "")

    def test_reused_translation_without_notice_is_retranslated(self):
        self.runner([self.claude()], []).run([MATCH])
        path = self.root / MATCH
        stripped = path.read_text(encoding="utf-8").replace(NOTICE + "\n", "")
        path.write_text(stripped, encoding="utf-8")
        manifest = Manifest.load(self.root)
        manifest.pages[MATCH]["target_sha256"] = sha256_bytes(stripped.encode())
        manifest.save()
        claude, agy = self.claude(), self.agy()
        self.assertEqual(self.runner([claude], [agy]).run([MATCH]), {"reviewed": 1})
        self.assertEqual(len(claude.calls), 0, "validated chunks are reused from the cache")
        self.assertIn(NOTICE, self.read(MATCH))

    def test_check_enforces_the_pinned_source_inventory(self):
        self.runner([self.claude()], [self.agy()]).run(ALL)
        self.assertTrue(run_check(self.root, self.rules).ok)
        # Removing a page from both the manifest and the source store.
        manifest = Manifest.load(self.root)
        del manifest.pages[BIG]
        manifest.save()
        (self.root / config.SOURCE_STORE_DIR / BIG).unlink()
        problems = " ".join(run_check(self.root, self.rules).problems)
        self.assertIn("manifest page set differs from the source inventory", problems)
        self.assertIn("source store page set differs", problems)
        self.assertFalse(run_check(self.root, self.rules, publish=False, paths=[MATCH]).ok,
                         "subset checks still check the whole page set")
        inventory_path = self.root / config.SOURCE_INVENTORY_PATH
        inventory_path.unlink()
        self.assertTrue(any("source inventory" in p for p in run_check(self.root, self.rules).problems))

    def test_init_refuses_a_different_inventory_and_check_detects_hash_drift(self):
        inventory = SourceInventory.load(self.root)
        inventory.pages[MATCH] = "0" * 64
        inventory.save()
        with self.assertRaises(InitError):
            init(self.root, self.commit)
        self.assertTrue(any("source_sha256" in p and "inventory" in p
                            for p in run_check(self.root, self.rules, publish=False).problems))
        data = json.loads((self.root / config.SOURCE_INVENTORY_PATH).read_text())
        data["page_count"] = 99
        (self.root / config.SOURCE_INVENTORY_PATH).write_text(json.dumps(data))
        self.assertFalse(run_check(self.root, self.rules, publish=False).ok)

    # -- reply validation ------------------------------------------------------------------------------
    def test_duplicate_segment_ids_are_rejected_and_retried(self):
        def handler(prompt, n):
            answer = json.loads(good_translation(prompt))
            if n == 1:
                answer["segments"].append({"id": answer["segments"][0]["id"], "text": "重複"})
            return json.dumps(answer, ensure_ascii=False)
        claude = self.claude(handler)
        self.assertEqual(self.runner([claude], [self.agy()]).run([MATCH]), {"reviewed": 1})
        self.assertIn("duplicate segment ids", json.dumps(request_payload(claude.calls[1])["previous_issues"]))
        self.assertNotIn("重複", self.read(MATCH))

    def test_empty_glossary_translation_fails_to_load(self):
        with open(self.root / config.GLOSSARY_PATH, "a", encoding="utf-8") as handle:
            handle.write("  - {en: shard, zh: ''}\n")
        with self.assertRaises(ValueError):
            PromptContext.load(self.root)

    def test_usage_is_logged_only_when_reported(self):
        claude = self.claude()
        runner = self.runner([claude], [self.agy()])
        runner.run([MATCH])
        events = [json.loads(line) for line in runner.log.path.read_text().splitlines()]
        calls = [e for e in events if e["event"] == "model_call"]
        self.assertTrue(calls and all("usage" not in e and "estimated" not in e for e in calls))
        run_end = [e for e in events if e["event"] == "run_end"][-1]
        self.assertEqual(run_end["usage"]["claude"]["calls_with_usage"], 0)


if __name__ == "__main__":
    unittest.main()
