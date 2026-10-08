"""Read the signed-in account's usage without starting an inference turn."""
from __future__ import annotations

import json
import os
import queue
import signal
import shutil
import subprocess
import threading
import time


class BudgetUnavailable(RuntimeError):
    pass


def read_rate_limits(timeout=30):
    from .providers import scrubbed_env
    exe = shutil.which("codex")
    if not exe:
        raise BudgetUnavailable("Codex CLI is unavailable")
    messages = queue.Queue()
    with subprocess.Popen([exe, "app-server", "--listen", "stdio://"],
                          stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                          stderr=subprocess.DEVNULL, text=True, env=scrubbed_env(),
                          start_new_session=True) as proc:
        def read():
            for line in proc.stdout:
                messages.put(line)
        threading.Thread(target=read, daemon=True).start()
        deadline = time.monotonic() + timeout
        def send(message):
            proc.stdin.write(json.dumps(message) + "\n")
            proc.stdin.flush()
        def receive(identifier):
            while True:
                remaining = deadline - time.monotonic()
                if remaining <= 0:
                    raise BudgetUnavailable("Codex usage read timed out")
                try:
                    message = json.loads(messages.get(timeout=remaining))
                except queue.Empty:
                    raise BudgetUnavailable("Codex usage read timed out") from None
                except ValueError:
                    continue
                if message.get("id") == identifier:
                    if "error" in message:
                        raise BudgetUnavailable("Codex usage service rejected the read")
                    return message.get("result", {})
        try:
            send({"id": 1, "method": "initialize", "params": {
                "clientInfo": {"name": "zhtw_quota_guard", "version": "1.0"}}})
            receive(1)
            send({"method": "initialized", "params": {}})
            send({"id": 3, "method": "account/read", "params": {"refreshToken": False}})
            account = receive(3).get("account") or {}
            send({"id": 2, "method": "account/rateLimits/read", "params": {
                "excludeResetCreditDetails": True}})
            snapshot = receive(2)
            # Keep only the authentication type, never email/account details.
            snapshot["authType"] = account.get("type")
            return snapshot
        finally:
            # CLI launchers can spawn a child that inherits stdout. Killing
            # only the launcher leaves readline()/pipe cleanup blocked.
            try:
                os.killpg(proc.pid, signal.SIGTERM)
            except ProcessLookupError:
                pass
            try:
                proc.wait(timeout=5)
            except subprocess.TimeoutExpired:
                try:
                    os.killpg(proc.pid, signal.SIGKILL)
                except ProcessLookupError:
                    pass
                proc.wait()


def assess_budget(snapshot, minimum_remaining=25):
    """Conservative cutoff: reserve 20%, with a 5 point dispatch buffer.

    Never infer a weekly meter from a secondary window without its duration.
    All reported weekly buckets must have room; no credit/reset redemption.
    """
    if snapshot.get("ordinaryUsageAllowed") is False:
        return False, "ordinary included usage is unavailable"
    buckets = [snapshot.get("rateLimits") or {}]
    buckets.extend((snapshot.get("rateLimitsByLimitId") or {}).values())
    weekly = []
    for bucket in buckets:
        for key in ("primary", "secondary"):
            window = bucket.get(key) or {}
            used = window.get("usedPercent")
            if isinstance(used, bool) or not isinstance(used, (int, float)) or not 0 <= used <= 100:
                continue
            if window.get("windowDurationMins") == 10080:
                weekly.append(100 - used)
            elif window.get("windowDurationMins") == 300 and used >= 100:
                return False, "five-hour included usage is exhausted"
    if not weekly:
        return False, "authoritative weekly usage is unavailable"
    remaining = min(weekly)
    return remaining > minimum_remaining, f"weekly remaining={remaining:g}%; worker cutoff={minimum_remaining}%"
