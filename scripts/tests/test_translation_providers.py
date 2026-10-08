import json
import os
import sys
import unittest
from datetime import datetime
from zoneinfo import ZoneInfo
from unittest import mock

from test_translation_helpers import REPO, FakeProvider

from translation_pipeline import providers as P
from translation_pipeline.providers import (AUTH, INVALID, QUOTA, TRANSPORT, TRUNCATED, UNAVAILABLE,
                                            AgyProvider, ClaudeProvider, NoProviderAvailable,
                                            OllamaProvider, ProviderError, ProviderPool)


class ClassificationTests(unittest.TestCase):
    def test_explicit_taipei_reset_time(self):
        now = datetime(2026, 10, 8, 0, 30, tzinfo=ZoneInfo('Asia/Taipei')).timestamp()
        expected = datetime(2026, 10, 8, 3, 1, tzinfo=ZoneInfo('Asia/Taipei')).timestamp()
        self.assertEqual(P.quota_reset_timestamp("You've hit your session limit · resets 3am (Asia/Taipei)", now), expected)
        self.assertIsNone(P.quota_reset_timestamp('connection reset by peer', now))
        self.assertIsNone(P.quota_reset_timestamp('resets 3am (Unknown/Zone)', now))
    def test_classify_failure(self):
        cases = {
            "Claude AI usage limit reached|1760000000": QUOTA,
            "You've hit your limit · resets 3pm": QUOTA,
            "You've hit your session limit · resets 3am (Asia/Taipei)": QUOTA,
            "You’ve hit your session limit · resets 3am (Asia/Taipei)": QUOTA,
            "You've hit your weekly limit · resets Oct 9": QUOTA,
            "429 RESOURCE_EXHAUSTED: Quota exceeded for model": QUOTA,
            "Invalid API key · Please run /login": AUTH,
            "HTTP 401: unauthorized": AUTH,
            "OAuth token has expired": AUTH,
            "agy: command not found": UNAVAILABLE,
            "model 'gemma4:12b-mlx' not found, try pulling it first": UNAVAILABLE,
            "connection refused": UNAVAILABLE,
            "API Error: 529 overloaded": TRANSPORT,
            "socket hang up": TRANSPORT,
        }
        for message, kind in cases.items():
            self.assertEqual(P.classify_failure(message), kind, message)

    def test_redact_removes_secrets(self):
        text = "key sk-ant-api03-abcdef123 and AIzaSyA1234567890123456789012 Bearer abc.def api_key=hunter2"
        cleaned = P.redact(text)
        for secret in ("sk-ant-api03", "AIzaSy", "abc.def", "hunter2"):
            self.assertNotIn(secret, cleaned)


class EnvelopeTests(unittest.TestCase):
    def test_actual_session_quota_message_survives_all_claude_error_shapes(self):
        message = "You've hit your session limit · resets 3am (Asia/Taipei)"
        for envelope in [
            {"subtype": "success", "is_error": True, "result": message},
            {"subtype": "error_during_execution", "is_error": True, "result": message},
            {"subtype": "error_during_execution", "is_error": False, "result": message},
            {"subtype": "success", "is_error": False, "result": message},
        ]:
            with self.subTest(envelope=envelope), self.assertRaises(ProviderError) as result:
                P.parse_claude_envelope(json.dumps(envelope))
            self.assertEqual(result.exception.kind, QUOTA)

    def test_claude_success_and_errors(self):
        ok = json.dumps({"type": "result", "subtype": "success", "is_error": False, "result": "{\"a\": 1}"})
        self.assertEqual(P.parse_claude_envelope(ok)[0], "{\"a\": 1}")
        quota = json.dumps({"type": "result", "subtype": "success", "is_error": True,
                            "result": "Claude AI usage limit reached|1760000000"})
        with self.assertRaises(ProviderError) as ctx:
            P.parse_claude_envelope(quota, "", 1)
        self.assertEqual(ctx.exception.kind, QUOTA)
        with self.assertRaises(ProviderError) as ctx:
            P.parse_claude_envelope(json.dumps({"subtype": "error_max_turns", "is_error": False}))
        self.assertEqual(ctx.exception.kind, TRUNCATED)
        with self.assertRaises(ProviderError) as ctx:
            P.parse_claude_envelope('{"type": "result", "result": "par', "", 0)
        self.assertEqual(ctx.exception.kind, TRANSPORT)
        with self.assertRaises(ProviderError) as ctx:
            P.parse_claude_envelope("", "Not logged in · Please run /login", 1)
        self.assertEqual(ctx.exception.kind, AUTH)

    def test_agy_nested_envelopes(self):
        variants = [
            {"response": {"text": "ANSWER"}},
            {"result": {"response": "ANSWER", "stats": {}}},
            {"candidates": [{"content": {"parts": [{"text": "ANS"}, {"text": "WER"}]}, "finishReason": "STOP"}]},
            {"messages": [{"role": "user", "content": "q"}, {"role": "assistant", "content": "ANSWER"}]},
        ]
        for env in variants:
            self.assertEqual(P.parse_agy_envelope(json.dumps(env))[0], "ANSWER", env)
        ndjson = '{"type": "progress"}\n{"response": {"text": "ANSWER"}}\n'
        self.assertEqual(P.parse_agy_envelope(ndjson)[0], "ANSWER")

    def test_agy_errors_and_truncation(self):
        with self.assertRaises(ProviderError) as ctx:
            P.parse_agy_envelope(json.dumps({"error": {"code": 429, "message": "Quota exceeded"}}))
        self.assertEqual(ctx.exception.kind, QUOTA)
        with self.assertRaises(ProviderError) as ctx:
            P.parse_agy_envelope(json.dumps({"response": {"text": "{\"a\"", "finishReason": "MAX_TOKENS"}}))
        self.assertEqual(ctx.exception.kind, TRUNCATED)
        with self.assertRaises(ProviderError) as ctx:
            P.parse_agy_envelope(json.dumps({"response": {}}), "", 0)
        self.assertEqual(ctx.exception.kind, TRANSPORT)

    def test_ollama_truncation_and_errors(self):
        ok = json.dumps({"message": {"role": "assistant", "content": "{}"}, "done": True, "done_reason": "stop"})
        self.assertEqual(P.parse_ollama_response(ok)[0], "{}")
        for body, kind in ((json.dumps({"message": {"content": "{"}, "done": True, "done_reason": "length"}), TRUNCATED),
                           (json.dumps({"error": "model 'x' not found"}), UNAVAILABLE),
                           (json.dumps({"error": "you have reached your weekly usage limit"}), QUOTA)):
            with self.assertRaises(ProviderError) as ctx:
                P.parse_ollama_response(body)
            self.assertEqual(ctx.exception.kind, kind)

    def test_extract_json_object(self):
        self.assertEqual(P.extract_json_object('```json\n{"a": 1}\n```'), {"a": 1})
        self.assertEqual(P.extract_json_object('Here: {"a": {"b": 2}} done'), {"a": {"b": 2}})
        with self.assertRaises(ProviderError) as ctx:
            P.extract_json_object('{"segments": [{"id": "body.000", "text": "未完')
        self.assertEqual(ctx.exception.kind, TRUNCATED)
        with self.assertRaises(ProviderError) as ctx:
            P.extract_json_object("I cannot do that.")
        self.assertEqual(ctx.exception.kind, INVALID)


class ProviderCommandTests(unittest.TestCase):
    def test_claude_argv_and_stdin(self):
        seen = {}

        def runner(argv, stdin, timeout, name):
            seen.update(argv=argv, stdin=stdin)
            return 0, json.dumps({"subtype": "success", "is_error": False, "result": "ok"}), ""
        reply = ClaudeProvider(runner=runner).complete("SYS", "PROMPT")
        self.assertEqual(reply.text, "ok")
        argv = seen["argv"]
        self.assertEqual(argv[:8], ["claude", "-p", "--tools", "", "--output-format", "json",
                                    "--no-session-persistence", "--system-prompt"])
        self.assertEqual(seen["stdin"], "PROMPT")
        self.assertNotIn("PROMPT", argv)

    def test_agy_argv_prompt_is_final_element(self):
        seen = {}

        def runner(argv, stdin, timeout, name):
            seen.update(argv=argv, stdin=stdin)
            return 0, json.dumps({"response": {"text": "ok"}}), ""
        AgyProvider(runner=runner).complete("SYS", "PROMPT; rm -rf /\n--dangerously-skip-permissions")
        argv = seen["argv"]
        self.assertEqual(argv, ["agy", "--model", "gemini-3.1-pro-high", "--mode", "plan",
                                "--output-format", "json", "--disable-slash-commands",
                                "--print=SYS\n\nPROMPT; rm -rf /\n--dangerously-skip-permissions"])
        self.assertEqual(seen["stdin"], "")
        self.assertNotIn("--dangerously-skip-permissions", argv[:-1])
        with self.assertRaises(TypeError):
            AgyProvider(runner=runner, prompt_via="stdin")   # no stdin fallback

    def test_reported_usage_is_separate_from_estimates(self):
        env = {"subtype": "success", "is_error": False, "result": "ok", "total_cost_usd": 0.12,
               "usage": {"input_tokens": 10, "output_tokens": 20, "server_tool_use": {"x": 1}}}
        _, meta = P.parse_claude_envelope(json.dumps(env))
        self.assertEqual(meta["usage"], {"input_tokens": 10, "output_tokens": 20})
        self.assertEqual(meta["estimated"], {"cost_usd": 0.12})
        _, meta = P.parse_claude_envelope(json.dumps({"subtype": "success", "result": "ok"}))
        self.assertNotIn("usage", meta, "no counters are invented")
        _, meta = P.parse_agy_envelope(json.dumps({"response": {"text": "ok"},
                                                   "usageMetadata": {"promptTokenCount": 5}}))
        self.assertEqual(meta["usage"], {"promptTokenCount": 5})
        self.assertNotIn("usage", P.parse_agy_envelope(json.dumps({"response": {"text": "ok"}}))[1])
        _, meta = P.parse_ollama_response(json.dumps({"message": {"content": "{}"}, "done": True,
                                                      "eval_count": 7}))
        self.assertEqual(meta["usage"], {"eval_count": 7})

    def test_pool_aggregates_only_reported_usage(self):
        class Reporting(FakeProvider):
            def complete(self, system, prompt):
                reply = super().complete(system, prompt)
                reply.meta = {"usage": {"output_tokens": 3}, "estimated": {"cost_usd": 0.5}} \
                    if len(self.calls) == 1 else {}
                return reply
        pool = ProviderPool({"claude": Reporting("claude", "claude", lambda p, n: "ok")}, sleep=lambda s: None)
        pool.call(["claude"], "s", "p", "t")
        pool.call(["claude"], "s", "p", "t")
        self.assertEqual(pool.usage["claude"], {"calls": 2, "calls_with_usage": 1,
                                                "reported": {"output_tokens": 3},
                                                "estimated": {"cost_usd": 0.5}})

    def test_ollama_payload(self):
        seen = {}

        def post(url, payload, timeout, name):
            seen.update(url=url, payload=payload)
            return json.dumps({"message": {"content": "{}"}, "done": True, "done_reason": "stop"})
        OllamaProvider("ollama-cloud", "gemma4:cloud", post=post).complete("SYS", "PROMPT")
        self.assertEqual(seen["url"], "http://localhost:11434/api/chat")
        self.assertEqual(seen["payload"]["model"], "gemma4:cloud")
        self.assertFalse(seen["payload"]["stream"])

    def test_run_cli_isolated_cwd_scrubbed_env_no_shell(self):
        script = "import os,sys; print(os.getcwd()); print(os.environ.get('ANTHROPIC_API_KEY', 'none')); print(sys.stdin.read())"
        with mock.patch.dict(os.environ, {"ANTHROPIC_API_KEY": "sk-ant-secret"}), \
                mock.patch("subprocess.run", wraps=P.subprocess.run) as run:
            rc, out, err = P.run_cli([sys.executable, "-c", script], "hello $(whoami)", 30, "test")
        cwd, key, stdin = out.splitlines()[:3]
        self.assertEqual(rc, 0)
        self.assertNotEqual(os.path.realpath(cwd), str(REPO))
        self.assertFalse(os.path.realpath(cwd).startswith(str(REPO)))
        self.assertIn("zhtw-translation-worker-", cwd)
        self.assertEqual(key, "none")
        self.assertEqual(stdin, "hello $(whoami)")
        self.assertIs(run.call_args.kwargs["shell"], False)

    def test_missing_cli_is_unavailable(self):
        with self.assertRaises(ProviderError) as ctx:
            P.run_cli(["definitely-not-a-real-cli-zhtw"], "", 5, "x")
        self.assertEqual(ctx.exception.kind, UNAVAILABLE)

    def test_batch_workers_do_not_inherit_terminal_notification_watchers(self):
        with mock.patch.dict(os.environ, {'SUPERZENT_TERMINAL_ID': 'terminal-test',
                                         'CODEX_TUI_SESSION_LOG_PATH': '/tmp/terminal-test.jsonl',
                                         'OPENAI_API_KEY': 'secret-test'}):
            env = P.scrubbed_env()
        self.assertNotIn('SUPERZENT_TERMINAL_ID', env)
        self.assertNotIn('CODEX_TUI_SESSION_LOG_PATH', env)
        self.assertNotIn('OPENAI_API_KEY', env)


class PoolTests(unittest.TestCase):
    def test_unavailable_codex_meter_probes_again_without_spending_quota(self):
        clock = [1000]
        codex = FakeProvider('codex-review', 'codex:test', lambda p, n: 'ok')
        pool = ProviderPool({'codex-review': codex}, clock=lambda: clock[0])
        pool.disable('codex-review', ProviderError(QUOTA, 'Codex weekly reserve: usage read unavailable; workers paused'))
        self.assertEqual(pool.disabled_until['codex-review'], 1300)
        clock[0] = 1299
        self.assertTrue(pool.is_disabled('codex-review'))
        self.assertEqual(codex.calls, [])
        clock[0] = 1300
        self.assertFalse(pool.is_disabled('codex-review'))
        pool.disable('codex-review', ProviderError(QUOTA, 'Codex weekly reserve: weekly remaining=20%; worker cutoff=25%'))
        self.assertEqual(pool.disabled_until['codex-review'], 19300)

    def test_cloud_translation_uses_supported_low_cost_thinking_controls(self):
        for model, expected in [('glm-5.3-flash:cloud', 'low'), ('deepseek-v4.1-flash:cloud', False)]:
            seen = {}
            def post(url, payload, timeout, provider):
                seen.update(payload)
                return json.dumps({'message': {'content': '{}'}, 'done': True})
            OllamaProvider('test', model, post=post).complete('system', 'prompt')
            self.assertEqual(seen['think'], expected)

    def test_kimi_k3_is_not_registered_for_translation_or_backup(self):
        self.assertNotIn('ollama-cloud-kimi', P.config.DEFAULT_TRANSLATORS)
        self.assertNotIn('kimi-k3:cloud', P.config.OLLAMA_CLOUD_MODELS.values())

    def test_cloud_models_share_two_account_request_slots(self):
        from concurrent.futures import ThreadPoolExecutor
        import threading
        import time
        state = {'active': 0, 'peak': 0, 'calls': 0}
        lock = threading.Lock()
        def post(*args):
            with lock:
                state['active'] += 1
                state['peak'] = max(state['peak'], state['active'])
            time.sleep(0.02)
            with lock:
                state['active'] -= 1
                state['calls'] += 1
            return json.dumps({'message': {'content': '{}'}, 'done': True})
        models = ['glm-5.3-flash:cloud', 'deepseek-v4.1-flash:cloud'] * 2
        with ThreadPoolExecutor(max_workers=4) as executor:
            jobs = [executor.submit(OllamaProvider('test', m, post=post).complete, 's', 'p') for m in models]
            for job in jobs:
                job.result()
        self.assertEqual(state['calls'], 4)
        self.assertLessEqual(state['peak'], 2)

    def test_cloud_capacity_error_is_not_five_hour_quota(self):
        self.assertEqual(P.classify_failure('HTTP 429: too many concurrent requests'), TRANSPORT)
        self.assertEqual(P.classify_failure('Cloud usage limit reached'), QUOTA)
        self.assertEqual(P.classify_failure('HTTP 410: model was retired at 2026-09-25'), UNAVAILABLE)

    def test_account_cloud_quota_disables_model_aliases_together(self):
        names = list(P.config.OLLAMA_CLOUD_MODELS)
        providers = {n: FakeProvider(n, 'ollama', lambda p, count: 'ok') for n in names}
        pool = ProviderPool(providers, clock=lambda: 1000)
        pool.disable(names[0], ProviderError(QUOTA, 'Cloud usage limit reached'))
        self.assertEqual(set(pool.disabled), set(names))
        self.assertEqual(set(pool.disabled_until.values()), {19000})

    def test_unavailable_cloud_model_does_not_disable_others(self):
        names = list(P.config.OLLAMA_CLOUD_MODELS)
        providers = {n: FakeProvider(n, 'ollama', lambda p, count: 'ok') for n in names}
        pool = ProviderPool(providers)
        pool.disable(names[0], ProviderError(UNAVAILABLE, 'model unavailable'))
        self.assertEqual(set(pool.disabled), {names[0]})

    def test_quota_backend_is_reenabled_only_after_explicit_reset(self):
        clock = [datetime(2026, 10, 8, 0, 30, tzinfo=ZoneInfo('Asia/Taipei')).timestamp()]
        a = FakeProvider('claude', 'claude', lambda p, n: 'ok')
        pool = ProviderPool({'claude': a}, clock=lambda: clock[0])
        pool.disable('claude', ProviderError(QUOTA, "You've hit your session limit · resets 3am (Asia/Taipei)"))
        self.assertTrue(pool.is_disabled('claude'))
        clock[0] = pool.disabled_until['claude']
        self.assertFalse(pool.is_disabled('claude'))
        self.assertEqual(pool.call(['claude'], 's', 'p', 't').text, 'ok')
    def pool(self, providers, **kw):
        return ProviderPool({p.name: p for p in providers}, sleep=lambda s: None, **kw)

    def test_quota_switches_provider_and_disables_it(self):
        a = FakeProvider("claude", "claude", lambda p, n: ProviderError(QUOTA, "usage limit reached"))
        b = FakeProvider("ollama-cloud", "ollama", lambda p, n: "ok")
        pool = self.pool([a, b])
        self.assertEqual(pool.call(["claude", "ollama-cloud"], "s", "p", "t").provider, "ollama-cloud")
        self.assertEqual(pool.disabled, {"claude": QUOTA})
        pool.call(["claude", "ollama-cloud"], "s", "p", "t")
        self.assertEqual(len(a.calls), 1, "a disabled provider is not called again")

    def test_actual_claude_session_limit_switches_without_any_transport_retry(self):
        message = "You've hit your session limit · resets 3am (Asia/Taipei)"
        def limited(prompt, count):
            P.parse_claude_envelope(json.dumps({"subtype": "success", "is_error": True, "result": message}))
        a = FakeProvider("claude", "claude", limited)
        b = FakeProvider("agy", "agy", lambda p, n: "ok")
        sleep = mock.Mock()
        pool = ProviderPool({p.name: p for p in [a, b]}, sleep=sleep)
        for _ in range(12):
            self.assertEqual(pool.call(["claude", "agy"], "s", "p", "t").provider, "agy")
        self.assertEqual(len(a.calls), 1)
        self.assertEqual(len(b.calls), 12)
        self.assertEqual(pool.disabled, {"claude": QUOTA})
        sleep.assert_not_called()

    def test_concurrent_quota_detection_prevents_sleeping_worker_retry(self):
        a = FakeProvider("claude", "claude", lambda p, n: ProviderError(TRANSPORT, "connection reset"))
        b = FakeProvider("agy", "agy", lambda p, n: "ok")
        pool = self.pool([a, b])
        pool._sleep = lambda seconds: pool.disable("claude", ProviderError(QUOTA, "session limit"))
        self.assertEqual(pool.call(["claude", "agy"], "s", "p", "t").provider, "agy")
        self.assertEqual(len(a.calls), 1)

    def test_auth_and_unavailable_switch(self):
        for kind in (AUTH, UNAVAILABLE):
            a = FakeProvider("claude", "claude", lambda p, n, k=kind: ProviderError(k, "x"))
            b = FakeProvider("agy", "agy", lambda p, n: "ok")
            self.assertEqual(self.pool([a, b]).call(["claude", "agy"], "s", "p", "t").provider, "agy")

    def test_transport_retried_twice_without_switching(self):
        a = FakeProvider("claude", "claude", lambda p, n: ProviderError(TRANSPORT, "socket hang up"))
        b = FakeProvider("agy", "agy", lambda p, n: "ok")
        pool = self.pool([a, b])
        with self.assertRaises(ProviderError) as ctx:
            pool.call(["claude", "agy"], "s", "p", "t")
        self.assertEqual(ctx.exception.kind, TRANSPORT)
        self.assertEqual(len(a.calls), 3)
        self.assertEqual(b.calls, [])
        self.assertEqual(pool.disabled, {})

    def test_transport_recovers_on_retry(self):
        a = FakeProvider("claude", "claude", lambda p, n: ProviderError(TRANSPORT, "reset") if n < 3 else "ok")
        self.assertEqual(self.pool([a]).call(["claude"], "s", "p", "t").text, "ok")

    def test_invalid_reply_is_not_a_provider_switch(self):
        a = FakeProvider("claude", "claude", lambda p, n: ProviderError(TRUNCATED, "cut"))
        b = FakeProvider("agy", "agy", lambda p, n: "ok")
        with self.assertRaises(ProviderError):
            self.pool([a, b]).call(["claude", "agy"], "s", "p", "t")
        self.assertEqual(b.calls, [])

    def test_stop_on_quota(self):
        a = FakeProvider("claude", "claude", lambda p, n: ProviderError(QUOTA, "limit reached"))
        b = FakeProvider("agy", "agy", lambda p, n: "ok")
        pool = self.pool([a, b], stop_on_quota=True)
        with self.assertRaises(NoProviderAvailable):
            pool.call(["claude", "agy"], "s", "p", "t")
        self.assertTrue(pool.stopped.is_set())

    def test_all_unavailable(self):
        a = FakeProvider("claude", "claude", lambda p, n: ProviderError(UNAVAILABLE, "gone"))
        with self.assertRaises(NoProviderAvailable):
            self.pool([a]).call(["claude"], "s", "p", "t")


if __name__ == "__main__":
    unittest.main()
