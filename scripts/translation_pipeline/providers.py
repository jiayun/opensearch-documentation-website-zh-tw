"""Model providers, response-envelope parsing and failure classification.

Every provider only returns text. CLIs run with ``shell=False`` in a fresh
temporary working directory outside the repository, with the prompt passed
on stdin (claude) or as the single ``--print=<prompt>`` argv element (agy),
and with API-key environment variables removed so the CLIs use the signed-in
account rather than paid API keys.

Usage: ``ModelReply.meta["usage"]`` holds only token counters the provider
reported itself; CLI-side estimates (such as Claude's ``total_cost_usd``) go
to ``meta["estimated"]`` and are never mixed with reported counts.
"""

from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
import tempfile
import threading
import time
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError
import urllib.error
import urllib.request
from dataclasses import dataclass, field
from typing import Any, Callable

from . import config

# Failure kinds. Only SWITCH_KINDS disable a provider and move to the next
# one; transport failures are retried; invalid/truncated replies are handed
# back to the caller for a validation retry.
QUOTA, AUTH, UNAVAILABLE, TRANSPORT, INVALID, TRUNCATED = (
    "quota", "auth", "unavailable", "transport", "invalid", "truncated")
SWITCH_KINDS = frozenset({QUOTA, AUTH, UNAVAILABLE})

_QUOTA_RE = re.compile(
    r"usage limit|limit reached|hit your (?:session |usage |weekly |daily |monthly |message |token )?limit|reached your .*limit|quota|resource[_ ]exhausted|"
    r"rate[_ ]?limit|too many requests|\b429\b|\b402\b|insufficient (credit|balance|funds)|"
    r"credit balance|out of credits|exceeded your|weekly limit|daily limit", re.I)
_AUTH_RE = re.compile(
    r"not logged in|please (run )?/?log ?in|log ?in again|invalid api key|invalid x-api-key|"
    r"authenticat|unauthori[sz]ed|\b401\b|\b403\b|forbidden|oauth|token (has )?expired|"
    r"invalid credentials|missing credentials|no credentials|permission denied", re.I)
_UNAVAILABLE_RE = re.compile(
    r"command not found|no such file or directory|model .{0,80}not found|not found.{0,40}model|"
    r"unknown model|invalid model|model .{0,80}(unavailable|not available|does not exist|not supported)|"
    r"connection refused|\b404\b|\b410\b|was retired|model.{0,80}retired|is not enabled|not available in your (region|country)", re.I)

_SECRET_RES = (
    re.compile(r"sk-ant-[A-Za-z0-9_\-]+"),
    re.compile(r"sk-[A-Za-z0-9]{20,}"),
    re.compile(r"AIza[0-9A-Za-z_\-]{20,}"),
    re.compile(r"ya29\.[0-9A-Za-z_.\-]+"),
    re.compile(r"(?i)bearer\s+[A-Za-z0-9_.\-=]+"),
    re.compile(r"(?i)((?:api[_-]?key|access[_-]?token|refresh[_-]?token|secret|password)\"?\s*[:=]\s*\"?)[^\s\"',}]+"),
)


def redact(text: str, limit: int = 2000) -> str:
    text = text or ""
    for regex in _SECRET_RES:
        text = regex.sub(lambda m: (m.group(1) if m.re.groups else "") + "[REDACTED]", text)
    return text if len(text) <= limit else text[:limit] + f"…[+{len(text) - limit} chars]"


def classify_failure(message: str) -> str:
    """Classify an error message; anything unclear is a transport failure."""
    if re.search(r"too many concurrent|concurrent request.{0,30}(limit|exceed)|concurrency limit", message or "", re.I):
        return TRANSPORT  # temporary capacity, not exhausted account quota
    if _QUOTA_RE.search(message or ""):
        return QUOTA
    if _AUTH_RE.search(message or ""):
        return AUTH
    if _UNAVAILABLE_RE.search(message or ""):
        return UNAVAILABLE
    return TRANSPORT


def quota_reset_timestamp(message: str, timestamp: float) -> float | None:
    """Parse only an explicit CLI reset time with a named timezone."""
    relative = re.search(r"resets\s+in\s+((?:\d+\s*[hms]\s*)+)", message, re.I)
    if relative:
        seconds = sum(int(number) * {"h": 3600, "m": 60, "s": 1}[unit.lower()]
                      for number, unit in re.findall(r"(\d+)\s*([hms])", relative[1], re.I))
        if 0 < seconds <= 7 * 24 * 3600:
            return timestamp + seconds + 60
    match = re.search(r"resets\s+(\d{1,2})(?::(\d{2}))?\s*(am|pm)\s*\(([^)]+)\)", message, re.I)
    if not match:
        return None
    hour, minute = int(match[1]), int(match[2] or 0)
    if not 1 <= hour <= 12 or not 0 <= minute <= 59:
        return None
    try:
        zone = ZoneInfo(match[4])
    except ZoneInfoNotFoundError:
        return None
    now = datetime.fromtimestamp(timestamp, zone)
    hour = hour % 12 + (12 if match[3].lower() == "pm" else 0)
    reset = now.replace(hour=hour, minute=minute, second=0, microsecond=0)
    if reset <= now:
        reset += timedelta(days=1)
    return reset.timestamp() + 60  # allow a minute for the service's reset


class ProviderError(Exception):
    def __init__(self, kind: str, message: str, provider: str = "") -> None:
        super().__init__(f"{provider or 'provider'} {kind}: {redact(message, 500)}")
        self.kind = kind
        self.provider = provider
        self.detail = redact(message)


class NoProviderAvailable(Exception):
    pass


@dataclass
class ModelReply:
    text: str
    provider: str
    model: str
    meta: dict = field(default_factory=dict)


# -- JSON helpers --------------------------------------------------------------

def load_json_lenient(text: str) -> Any:
    """Parse a whole JSON document, or the last JSON value of NDJSON output."""
    text = (text or "").strip()
    if not text:
        raise ValueError("empty output")
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass
    for line in reversed(text.splitlines()):
        line = line.strip()
        if line.startswith(("{", "[")):
            try:
                return json.loads(line)
            except json.JSONDecodeError:
                continue
    raise ValueError("output is not JSON")


def extract_json_object(text: str) -> dict:
    """Extract the model's JSON answer from free text.

    Accepts a bare object or one wrapped in a ```json fence. An object that
    starts but never closes is reported as TRUNCATED.
    """
    text = (text or "").strip()
    fence = re.search(r"```(?:json)?\s*\n(.*?)\n```", text, re.S)
    candidates = [fence.group(1)] if fence else []
    candidates.append(text)
    decoder = json.JSONDecoder()
    saw_open = False
    for candidate in candidates:
        start = candidate.find("{")
        while start != -1:
            saw_open = True
            try:
                obj, _ = decoder.raw_decode(candidate, start)
                if isinstance(obj, dict):
                    return obj
            except json.JSONDecodeError as exc:
                if "Unterminated" in exc.msg or exc.pos >= len(candidate) - 1:
                    raise ProviderError(TRUNCATED, f"incomplete JSON answer: {exc.msg}") from exc
            start = candidate.find("{", start + 1)
    if saw_open:
        raise ProviderError(INVALID, "answer contains no valid JSON object")
    raise ProviderError(INVALID, "answer is not JSON")


_TEXT_KEYS = ("result", "response", "text", "content", "output", "answer", "message", "messages",
              "parts", "candidates", "data")
_STOP_KEYS = ("stop_reason", "stopReason", "finish_reason", "finishReason", "done_reason")
_TRUNCATED_STOPS = {"length", "max_tokens", "max_output_tokens", "MAX_TOKENS", "maxTokens", "max_turns"}


def _find_stop_reasons(obj: Any) -> list[str]:
    found = []
    if isinstance(obj, dict):
        for key, value in obj.items():
            if key in _STOP_KEYS and isinstance(value, str):
                found.append(value)
            else:
                found.extend(_find_stop_reasons(value))
    elif isinstance(obj, list):
        for item in obj:
            found.extend(_find_stop_reasons(item))
    return found


def _find_error(obj: Any) -> str | None:
    if isinstance(obj, dict):
        if obj.get("is_error") is True:
            return json.dumps(obj.get("result") or obj.get("error") or obj, ensure_ascii=False)[:4000]
        if str(obj.get("status", "")).lower() in ("error", "failed", "failure"):
            return json.dumps(obj, ensure_ascii=False)[:4000]
        err = obj.get("error")
        if err:
            return err if isinstance(err, str) else json.dumps(err, ensure_ascii=False)[:4000]
        for value in obj.values():
            if isinstance(value, (dict, list)):
                found = _find_error(value)
                if found:
                    return found
    elif isinstance(obj, list):
        for item in obj:
            found = _find_error(item)
            if found:
                return found
    return None


def find_text(obj: Any, depth: int = 0) -> str | None:
    """Locate the model's answer text inside an arbitrarily nested envelope."""
    if depth > 8:
        return None
    if isinstance(obj, str):
        return obj if obj.strip() else None
    if isinstance(obj, list):
        texts = [t for t in (find_text(item, depth + 1) for item in obj) if t]
        roles = [i.get("role") for i in obj if isinstance(i, dict)]
        if roles and any(r in ("assistant", "model") for r in roles):
            for item in reversed(obj):
                if isinstance(item, dict) and item.get("role") in ("assistant", "model"):
                    return find_text(item, depth + 1)
        return "".join(texts) if texts else None
    if isinstance(obj, dict):
        for key in _TEXT_KEYS:
            if key in obj:
                found = find_text(obj[key], depth + 1)
                if found:
                    return found
    return None


_USAGE_KEYS = ("usage", "usageMetadata", "usage_metadata")


def reported_usage(obj: Any, depth: int = 0) -> dict[str, int]:
    """Flat integer counters from the first usage object in an envelope."""
    if depth > 6:
        return {}
    if isinstance(obj, dict):
        for key in _USAGE_KEYS:
            value = obj.get(key)
            if isinstance(value, dict):
                counters = {k: v for k, v in value.items()
                            if isinstance(v, int) and not isinstance(v, bool)}
                if counters:
                    return counters
        children = obj.values()
    elif isinstance(obj, list):
        children = obj
    else:
        return {}
    for child in children:
        found = reported_usage(child, depth + 1)
        if found:
            return found
    return {}


def _meta(usage: dict[str, int], estimated: dict | None = None, **extra) -> dict:
    meta = {k: v for k, v in extra.items() if v is not None}
    if usage:
        meta["usage"] = usage
    if estimated:
        meta["estimated"] = estimated
    return meta


# -- envelope parsers ---------------------------------------------------------

def parse_claude_envelope(stdout: str, stderr: str = "", returncode: int = 0) -> tuple[str, dict]:
    try:
        env = load_json_lenient(stdout)
    except ValueError:
        message = f"exit {returncode}: {stderr or stdout}"
        raise ProviderError(classify_failure(message), message, "claude")
    if not isinstance(env, dict):
        raise ProviderError(TRANSPORT, "unexpected envelope type", "claude")
    if env.get("is_error") or (returncode and env.get("subtype") == "success" and not env.get("result")):
        message = str(env.get("result") or env.get("error") or stderr or "error")
        kind = classify_failure(message + " " + (stderr or ""))
        raise ProviderError(kind, message, "claude")
    subtype = env.get("subtype", "success")
    if subtype != "success":
        message = str(env.get("result") or env.get("error") or stderr or subtype)
        kind = classify_failure(message)
        if kind == TRANSPORT and "max" in subtype:
            kind = TRUNCATED
        raise ProviderError(kind, f"result subtype {subtype}: {message}", "claude")
    if any(s in _TRUNCATED_STOPS for s in _find_stop_reasons(env)):
        raise ProviderError(TRUNCATED, "stopped at output token limit", "claude")
    cost = env.get("total_cost_usd")
    meta = _meta(reported_usage({"usage": env.get("usage")}),
                 {"cost_usd": cost} if isinstance(cost, (int, float)) else None,
                 duration_ms=env.get("duration_ms"), num_turns=env.get("num_turns"),
                 reported_model=env.get("model") or next(iter(env.get("modelUsage") or {}), None))
    if isinstance(env.get("structured_output"), (dict, list)):
        return json.dumps(env["structured_output"], ensure_ascii=False), meta
    text = env.get("result")
    if not isinstance(text, str) or not text.strip():
        raise ProviderError(TRANSPORT, "empty result", "claude")
    if not text.lstrip().startswith(("{", "[", "```")) and _QUOTA_RE.search(text):
        raise ProviderError(QUOTA, text, "claude")
    return text, meta


def parse_agy_envelope(stdout: str, stderr: str = "", returncode: int = 0) -> tuple[str, dict]:
    try:
        env = load_json_lenient(stdout)
    except ValueError:
        message = f"exit {returncode}: {stderr or stdout}"
        raise ProviderError(classify_failure(message), message, "agy")
    error = _find_error(env)
    if error:
        raise ProviderError(classify_failure(error + " " + (stderr or "")), error, "agy")
    if any(s in _TRUNCATED_STOPS for s in _find_stop_reasons(env)):
        raise ProviderError(TRUNCATED, "stopped at output token limit", "agy")
    text = find_text(env)
    if not text:
        message = f"exit {returncode}: no response text; {stderr}"
        raise ProviderError(classify_failure(message) if returncode else TRANSPORT, message, "agy")
    return text, _meta(reported_usage(env))


def parse_ollama_response(body: str, provider: str = "ollama") -> tuple[str, dict]:
    try:
        data = json.loads(body)
    except json.JSONDecodeError:
        raise ProviderError(TRANSPORT, "invalid JSON from Ollama", provider)
    if data.get("error"):
        raise ProviderError(classify_failure(str(data["error"])), str(data["error"]), provider)
    if data.get("done") is False or data.get("done_reason") == "length":
        raise ProviderError(TRUNCATED, f"done={data.get('done')} done_reason={data.get('done_reason')}", provider)
    text = (data.get("message") or {}).get("content")
    if not isinstance(text, str) or not text.strip():
        raise ProviderError(TRANSPORT, "empty message", provider)
    return text, _meta({k: data[k] for k in ("prompt_eval_count", "eval_count")
                        if isinstance(data.get(k), int) and not isinstance(data.get(k), bool)})


# -- process execution ----------------------------------------------------------

def scrubbed_env() -> dict[str, str]:
    env = {k: v for k, v in os.environ.items() if k not in config.SCRUBBED_ENV_VARS}
    # Batch workers have no interactive terminal. Superzent's notification
    # watcher otherwise inherits stdout and prevents EOF after Codex finishes.
    # The signed-in CLI and its account authentication remain unchanged.
    for key in ("SUPERZENT_TERMINAL_ID", "SUPERZENT_HOOK_OWNER_TERMINAL_ID",
                "SUPERZENT_SUPPRESS_AGENT_COMPLETION", "CODEX_TUI_RECORD_SESSION",
                "CODEX_TUI_SESSION_LOG_PATH"):
        env.pop(key, None)
    env["NO_COLOR"] = "1"
    return env


def run_cli(argv: list[str], stdin_text: str, timeout: float, provider: str) -> tuple[int, str, str]:
    exe = shutil.which(argv[0])
    if not exe:
        raise ProviderError(UNAVAILABLE, f"{argv[0]}: command not found", provider)
    with tempfile.TemporaryDirectory(prefix="zhtw-translation-worker-") as cwd:
        try:
            proc = subprocess.run(
                [exe, *argv[1:]], input=stdin_text, capture_output=True, text=True,
                encoding="utf-8", errors="replace", timeout=timeout, cwd=cwd,
                env=scrubbed_env(), shell=False, check=False)
        except subprocess.TimeoutExpired:
            raise ProviderError(TRANSPORT, f"timed out after {timeout}s", provider)
        except OSError as exc:
            raise ProviderError(UNAVAILABLE, str(exc), provider)
    return proc.returncode, proc.stdout, proc.stderr


# -- providers --------------------------------------------------------------------

class Provider:
    name = "provider"
    family = "provider"
    model = ""

    def complete(self, system: str, prompt: str) -> ModelReply:  # pragma: no cover - interface
        raise NotImplementedError


class ClaudeProvider(Provider):
    name = family = "claude"

    def __init__(self, model: str | None = None, timeout: float = 900,
                 runner: Callable = run_cli) -> None:
        self.model = model or "default"
        self._explicit_model = model
        self.timeout = timeout
        self.runner = runner

    def argv(self, system: str) -> list[str]:
        argv = ["claude", "-p", "--tools", "", "--output-format", "json",
                "--no-session-persistence", "--system-prompt", system,
                "--disable-slash-commands", "--strict-mcp-config", "--mcp-config", '{"mcpServers":{}}']
        if self._explicit_model:
            argv += ["--model", self._explicit_model]
        return argv

    def complete(self, system: str, prompt: str) -> ModelReply:
        rc, out, err = self.runner(self.argv(system), prompt, self.timeout, self.name)
        text, meta = parse_claude_envelope(out, err, rc)
        return ModelReply(text, self.name, meta.get("reported_model") or self.model, meta)


class AgyProvider(Provider):
    """Antigravity CLI. ``--print`` takes its value, so the whole prompt is the
    single final argv element ``--print=<prompt>`` (never split, never a
    shell string); stdin stays empty."""
    name = family = "agy"

    def __init__(self, model: str = config.AGY_MODEL, timeout: float = 900,
                 runner: Callable = run_cli, name: str = "agy") -> None:
        self.name = name
        # Quota buckets are account-specific; review independence is based
        # on the actual model family, not the CLI that happened to run it.
        self.family = "claude" if model.startswith("claude-") else (
            "openai:gpt-oss-120b" if model.startswith("gpt-oss-") else "agy")
        self.model = model
        self.timeout = timeout
        self.runner = runner

    def argv(self, full_prompt: str) -> list[str]:
        return ["agy", "--model", self.model, "--mode", "plan", "--output-format", "json",
                "--disable-slash-commands", "--print=" + full_prompt]

    def complete(self, system: str, prompt: str) -> ModelReply:
        rc, out, err = self.runner(self.argv(f"{system}\n\n{prompt}"), "", self.timeout, self.name)
        text, meta = parse_agy_envelope(out, err, rc)
        return ModelReply(text, self.name, self.model, meta)


def parse_codex_events(stdout: str, stderr: str = "", returncode: int = 0) -> tuple[str, dict]:
    """Read only the final agent message and reported usage from exec JSONL."""
    answer = None
    usage = {}
    for line in stdout.splitlines():
        try:
            event = json.loads(line)
        except json.JSONDecodeError:
            continue
        kind = event.get("type")
        if kind in ("error", "thread.failed", "turn.failed"):
            message = str(event.get("message") or event.get("error") or event)
            raise ProviderError(classify_failure(message), message, "codex")
        if kind == "item.completed" and event.get("item", {}).get("type") == "agent_message":
            answer = event["item"].get("text")
        if kind == "turn.completed":
            usage = reported_usage(event)
    if returncode:
        raise ProviderError(classify_failure(stderr or stdout), stderr or stdout, "codex")
    if not isinstance(answer, str) or not answer.strip():
        raise ProviderError(TRANSPORT, "Codex exec returned no final agent message", "codex")
    if not answer.lstrip().startswith(("{", "[", "```")) and _QUOTA_RE.search(answer):
        raise ProviderError(QUOTA, answer, "codex")
    return answer, _meta(usage)


_CODEX_WORK_LOCK = threading.Lock()


class CodexProvider(Provider):
    """Budget-guarded signed-in ChatGPT account, isolated read-only session."""
    def __init__(self, name="codex", model=config.CODEX_TRANSLATION_MODEL, effort="low",
                 timeout=900, runner=run_cli, budget_reader=None):
        self.name = name
        self.model = model
        self.family = "codex:" + model
        self.effort = effort
        self.timeout = timeout
        self.runner = runner
        from .codex_budget import read_rate_limits
        self.budget_reader = budget_reader or read_rate_limits

    def argv(self):
        return ["codex", "exec", "--ignore-user-config", "--skip-git-repo-check", "--ephemeral",
                "--sandbox", "read-only", "--model", self.model, "--json", "--color", "never",
                "-c", f'model_reasoning_effort="{self.effort}"', "-"]

    def complete(self, system, prompt):
        # Serialize translation and review together so neither can dispatch
        # using a meter read before another Codex task completes.
        with _CODEX_WORK_LOCK:
            return self._complete_with_budget(system, prompt)

    def _complete_with_budget(self, system, prompt):
        from .codex_budget import assess_budget
        try:
            snapshot = self.budget_reader()
            allowed, reason = assess_budget(snapshot)
        except Exception:
            raise ProviderError(QUOTA, "Codex weekly reserve: usage read unavailable; workers paused", self.name) from None
        if snapshot.get("authType") != "chatgpt":
            raise ProviderError(AUTH, "Codex must use the signed-in ChatGPT subscription, not an API key", self.name)
        if not allowed:
            raise ProviderError(QUOTA, "Codex weekly reserve: " + reason, self.name)
        instructions = system + "\n\nReturn only the requested JSON. Do not use tools, execute commands, read files, or access MCP servers.\n\n" + prompt
        code, stdout, stderr = self.runner(self.argv(), instructions, self.timeout, self.name)
        answer, meta = parse_codex_events(stdout, stderr, code)
        return ModelReply(answer, self.name, self.model, meta)


def http_post_json(url: str, payload: dict, timeout: float, provider: str) -> str:
    data = json.dumps(payload).encode("utf-8")
    request = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(request, timeout=timeout) as resp:
            return resp.read().decode("utf-8", errors="replace")
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        message = f"HTTP {exc.code}: {body}"
        kind = classify_failure(message)
        if kind == TRANSPORT and exc.code in (401, 403):
            kind = AUTH
        raise ProviderError(kind, message, provider)
    except urllib.error.URLError as exc:
        reason = str(exc.reason)
        kind = UNAVAILABLE if "refused" in reason.lower() else TRANSPORT
        raise ProviderError(kind, reason, provider)
    except (TimeoutError, OSError) as exc:
        raise ProviderError(TRANSPORT, str(exc) or "timeout", provider)


_OLLAMA_CLOUD_SLOTS = threading.BoundedSemaphore(2)


class OllamaProvider(Provider):
    family = "ollama"

    def __init__(self, name: str, model: str, url: str = config.OLLAMA_URL, timeout: float = 1200,
                 post: Callable = http_post_json) -> None:
        self.name = name
        self.model = model
        self.url = url
        self.timeout = timeout
        self.post = post

    def complete(self, system: str, prompt: str) -> ModelReply:
        payload = {
            "model": self.model,
            "stream": False,
            "format": "json",
            "messages": [{"role": "system", "content": system}, {"role": "user", "content": prompt}],
            "options": {"temperature": 0.2, "num_ctx": 32768},
        }
        thinking = config.OLLAMA_CLOUD_THINKING.get(self.model)
        if thinking is not None:
            payload["think"] = thinking
        if self.model.endswith((":cloud", "-cloud")):
            with _OLLAMA_CLOUD_SLOTS:
                body = self.post(self.url, payload, self.timeout, self.name)
        else:
            body = self.post(self.url, payload, self.timeout, self.name)
        text, meta = parse_ollama_response(body, self.name)
        return ModelReply(text, self.name, self.model, meta)


def build_providers(claude_model: str | None = None) -> dict[str, Provider]:
    return {
        "claude": ClaudeProvider(model=claude_model),
        **{name: AgyProvider(model=model, name=name) for name, (model, group) in config.AGY_MODELS.items()},
        **{name: OllamaProvider(name, model) for name, model in config.OLLAMA_CLOUD_MODELS.items()},
        "ollama-local": OllamaProvider("ollama-local", config.OLLAMA_LOCAL_MODEL),
        "codex": CodexProvider(),
        "codex-review": CodexProvider("codex-review", config.CODEX_REVIEW_MODEL, "medium"),
    }


# -- pool and call policy -----------------------------------------------------------

class ProviderPool:
    """Thread-safe provider registry that remembers disabled providers."""

    def __init__(self, providers: dict[str, Provider], stop_on_quota: bool = False,
                 log: Callable[..., None] | None = None, sleep: Callable[[float], None] = time.sleep,
                 clock: Callable[[], float] = time.time, balance_calls: bool = False) -> None:
        self.providers = providers
        self.stop_on_quota = stop_on_quota
        self.disabled: dict[str, str] = {}
        self.stopped = threading.Event()
        self._lock = threading.Lock()
        self._log = log or (lambda *a, **k: None)
        self._sleep = sleep
        self._clock = clock
        self.disabled_until: dict[str, float] = {}
        self.usage: dict[str, dict] = {}
        self.balance_calls = balance_calls
        self._dispatch_counts: dict[str, int] = {}

    def _record_usage(self, name: str, reply: ModelReply) -> None:
        with self._lock:
            agg = self.usage.setdefault(name, {"calls": 0, "calls_with_usage": 0, "reported": {}, "estimated": {}})
            agg["calls"] += 1
            if reply.meta.get("usage"):
                agg["calls_with_usage"] += 1
            for section in ("usage", "estimated"):
                target = agg["reported" if section == "usage" else "estimated"]
                for key, value in (reply.meta.get(section) or {}).items():
                    target[key] = target.get(key, 0) + value

    def is_disabled(self, name: str) -> bool:
        with self._lock:
            until = self.disabled_until.get(name)
            if until is not None and self._clock() >= until and not self.stopped.is_set():
                self.disabled.pop(name, None)
                self.disabled_until.pop(name, None)
                self._log("provider_reset", provider=name)
            return name in self.disabled

    def disable(self, name: str, error: ProviderError) -> None:
        with self._lock:
            targets = [name]
            if error.kind == QUOTA and name in config.OLLAMA_CLOUD_MODELS:
                targets = [n for n in config.OLLAMA_CLOUD_MODELS if n in self.providers]
            elif error.kind == QUOTA and name in config.AGY_MODELS:
                group = config.AGY_MODELS[name][1]
                targets = [n for n, (_, bucket) in config.AGY_MODELS.items()
                           if bucket == group and n in self.providers]
            for target in targets:
                if target not in self.disabled:
                    self.disabled[target] = error.kind
                    if error.kind == QUOTA:
                        until = quota_reset_timestamp(error.detail, self._clock())
                        # A failed meter read must block inference, but is not
                        # evidence that five-hour account quota was consumed.
                        meter_unavailable = target.startswith('codex') and error.detail.startswith(
                            'Codex weekly reserve: usage read unavailable')
                        delay = 300 if meter_unavailable else 5 * 3600
                        self.disabled_until[target] = until or (self._clock() + delay)
                    self._log("provider_disabled", provider=target, kind=error.kind, detail=error.detail,
                              reset_at=self.disabled_until.get(target))
            if error.kind == QUOTA and self.stop_on_quota:
                self.stopped.set()

    def available(self, chain: list[str]) -> list[str]:
        return [n for n in chain if n in self.providers and not self.is_disabled(n)]

    def _order_chain(self, chain: list[str], purpose: str, prompt_chars: int = 0) -> list[str]:
        if not self.balance_calls or len(chain) < 2:
            return chain
        weights = {"translate": config.TRANSLATION_WEIGHTS,
                   "review": config.REVIEW_WEIGHTS}
        available = self.available(chain)
        if purpose == "review" and prompt_chars > 45000 and "agy-opus" in available:
            return ["agy-opus"] + [n for n in chain if n != "agy-opus"]
        choices = [n for n in weights.get(purpose, []) if n in available]
        if not choices:
            return chain
        with self._lock:
            index = self._dispatch_counts.get(purpose, 0)
            self._dispatch_counts[purpose] = index + 1
        first = choices[index % len(choices)]
        return [first] + [n for n in chain if n != first]

    def call(self, chain: list[str], system: str, prompt: str, purpose: str) -> ModelReply:
        """Call the first usable provider in chain.

        Switches provider only on quota/auth/unavailable. Transport failures
        are retried TRANSPORT_RETRIES times on the same provider and then
        re-raised. INVALID/TRUNCATED replies are re-raised to the caller.
        """
        for name in self._order_chain(chain, purpose, len(prompt)):
            if self.stopped.is_set():
                raise NoProviderAvailable("run stopped after a quota failure")
            if name not in self.providers or self.is_disabled(name):
                continue
            provider = self.providers[name]
            tries = 0
            while True:
                # Another worker can discover the quota while this one sleeps
                # after a transport failure. Do not retry a disabled backend.
                if self.stopped.is_set():
                    raise NoProviderAvailable("run stopped after a quota failure")
                if self.is_disabled(name):
                    break
                started = time.monotonic()
                try:
                    reply = provider.complete(system, prompt)
                    self._record_usage(name, reply)
                    extra = {k: reply.meta[k] for k in ("usage", "estimated") if reply.meta.get(k)}
                    self._log("model_call", provider=name, model=provider.model, purpose=purpose,
                              ok=True, seconds=round(time.monotonic() - started, 1),
                              prompt_chars=len(prompt), reply_chars=len(reply.text), **extra)
                    return reply
                except ProviderError as exc:
                    exc.provider = exc.provider or name
                    self._log("model_call", provider=name, model=provider.model, purpose=purpose,
                              ok=False, kind=exc.kind, detail=exc.detail,
                              seconds=round(time.monotonic() - started, 1))
                    if exc.kind in SWITCH_KINDS:
                        self.disable(name, exc)
                        break
                    if exc.kind == TRANSPORT and tries < config.TRANSPORT_RETRIES:
                        tries += 1
                        self._sleep(5 * tries)
                        continue
                    raise
        raise NoProviderAvailable(f"no available provider among {', '.join(chain)}")
