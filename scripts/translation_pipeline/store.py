"""Atomic file writes, the baseline source store, the manifest and the cache."""

from __future__ import annotations

import copy
import hashlib
import json
import os
import tempfile
import threading
from datetime import datetime, timezone
from pathlib import Path

from . import config


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_text(text: str) -> str:
    return sha256_bytes(text.encode("utf-8"))


def now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def atomic_write(path: Path, data: bytes) -> None:
    """Write via a temp file in the same directory, fsync, then rename."""
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(prefix=f".{path.name}.", suffix=".tmp", dir=path.parent)
    try:
        with os.fdopen(fd, "wb") as handle:
            handle.write(data)
            handle.flush()
            os.fsync(handle.fileno())
        if path.exists():
            os.chmod(tmp, path.stat().st_mode & 0o777)
        else:
            os.chmod(tmp, 0o644)
        os.replace(tmp, path)
    except BaseException:
        if os.path.exists(tmp):
            os.unlink(tmp)
        raise


def atomic_write_json(path: Path, data) -> None:
    atomic_write(path, (json.dumps(data, ensure_ascii=False, indent=1, sort_keys=True) + "\n").encode("utf-8"))


class SourceStore:
    """Immutable baseline content stored as plain files at translation/source/<page>.

    The site's heading-ID plugin reads these files directly, so they must stay
    byte-identical to the baseline commit.
    """

    def __init__(self, root: Path) -> None:
        self.dir = root / config.SOURCE_STORE_DIR

    def blob_path(self, page: str) -> Path:
        return self.dir / page

    def write(self, page: str, data: bytes) -> None:
        path = self.blob_path(page)
        if path.exists() and path.read_bytes() == data:
            return
        atomic_write(path, data)

    def read(self, page: str) -> bytes:
        return self.blob_path(page).read_bytes()

    def exists(self, page: str) -> bool:
        return self.blob_path(page).is_file()

    def pages(self) -> list[str]:
        if not self.dir.exists():
            return []
        return sorted(p.relative_to(self.dir).as_posix() for p in self.dir.rglob("*") if p.is_file())


class SourceInventory:
    """translation/source-inventory.json: the page set and source hashes pinned
    at ``init``. ``run`` never writes it, so an incomplete manifest or source
    store (page and entry both removed) cannot pass the publish check, and the
    check needs no git history."""

    def __init__(self, path: Path, data: dict) -> None:
        self.path = path
        self.data = data

    @classmethod
    def build(cls, root: Path, baseline_commit: str, hashes: dict[str, str]) -> "SourceInventory":
        return cls(root / config.SOURCE_INVENTORY_PATH, {
            "schema_version": config.SCHEMA_VERSION,
            "baseline_commit": baseline_commit,
            "page_count": len(hashes),
            "pages": dict(sorted(hashes.items())),
        })

    @classmethod
    def load(cls, root: Path) -> "SourceInventory":
        path = root / config.SOURCE_INVENTORY_PATH
        with open(path, encoding="utf-8") as handle:
            data = json.load(handle)
        if data.get("schema_version") != config.SCHEMA_VERSION:
            raise ValueError(f"unsupported source inventory schema_version {data.get('schema_version')}")
        if not isinstance(data.get("pages"), dict) or data.get("page_count") != len(data["pages"]):
            raise ValueError("source inventory page_count does not match its page list")
        return cls(path, data)

    @property
    def pages(self) -> dict[str, str]:
        return self.data["pages"]

    def save(self) -> None:
        atomic_write_json(self.path, self.data)


class Manifest:
    """translation/manifest.json; every mutation is saved atomically under a lock."""

    def __init__(self, path: Path, data: dict) -> None:
        self.path = path
        self.data = data
        self.lock = threading.RLock()

    @classmethod
    def load(cls, root: Path) -> "Manifest":
        path = root / config.MANIFEST_PATH
        with open(path, encoding="utf-8") as handle:
            data = json.load(handle)
        if data.get("schema_version") != config.SCHEMA_VERSION:
            raise ValueError(f"unsupported manifest schema_version {data.get('schema_version')}")
        return cls(path, data)

    @classmethod
    def new(cls, root: Path, baseline_commit: str) -> "Manifest":
        return cls(root / config.MANIFEST_PATH, {
            "schema_version": config.SCHEMA_VERSION,
            "baseline_commit": baseline_commit,
            "target_language": config.TARGET_LANGUAGE,
            "source_store": config.SOURCE_STORE_DIR,
            "pages": {},
        })

    @property
    def pages(self) -> dict:
        return self.data["pages"]

    def entry(self, page: str) -> dict:
        with self.lock:
            return copy.deepcopy(self.pages[page])

    def update(self, page: str, **fields) -> dict:
        with self.lock:
            self.pages[page].update(fields)
            self.save()
            return copy.deepcopy(self.pages[page])

    def save(self) -> None:
        with self.lock:
            atomic_write_json(self.path, self.data)


def new_entry(source_sha256: str, original_fm: dict) -> dict:
    return {
        "source_sha256": source_sha256,
        "original_front_matter": original_fm,
        "status": "pending",
        "attempts": 0,
        "target_sha256": None,
        "translated_source_sha256": None,
        "translator": None,
        "reviewer": None,
        "last_error": None,
        "updated_at": None,
    }


class Cache:
    """Ignored working cache: validated chunk results, journal and logs."""

    def __init__(self, root: Path) -> None:
        self.dir = root / config.CACHE_DIR

    def _key_path(self, kind: str, key: str) -> Path:
        return self.dir / kind / key[:2] / f"{key}.json"

    @staticmethod
    def key(*parts: str) -> str:
        return sha256_text("\0".join(parts))

    def get(self, kind: str, key: str) -> dict | None:
        path = self._key_path(kind, key)
        try:
            with open(path, encoding="utf-8") as handle:
                return json.load(handle)
        except (OSError, json.JSONDecodeError):
            return None

    def put(self, kind: str, key: str, value: dict) -> None:
        atomic_write_json(self._key_path(kind, key), value)

    # The journal records an intended page commit before the target file is
    # written, so that a crash between the file write and the manifest save
    # can be recovered on the next run.
    def journal_path(self, page: str) -> Path:
        return self.dir / "journal" / (sha256_text(page)[:24] + ".json")

    def write_journal(self, page: str, record: dict) -> None:
        atomic_write_json(self.journal_path(page), record)

    def read_journal(self, page: str) -> dict | None:
        path = self.journal_path(page)
        try:
            with open(path, encoding="utf-8") as handle:
                return json.load(handle)
        except (OSError, json.JSONDecodeError):
            return None

    def clear_journal(self, page: str) -> None:
        try:
            self.journal_path(page).unlink()
        except FileNotFoundError:
            pass

    def log_path(self, run_id: str) -> Path:
        return self.dir / "logs" / f"run-{run_id}.jsonl"


class RunLog:
    """Thread-safe JSONL event log. Callers pass already-redacted details."""

    def __init__(self, path: Path | None) -> None:
        self.path = path
        self._lock = threading.Lock()
        if path:
            path.parent.mkdir(parents=True, exist_ok=True)

    def __call__(self, event: str, **fields) -> None:
        if not self.path:
            return
        record = {"at": now(), "event": event, **fields}
        line = json.dumps(record, ensure_ascii=False, default=str)
        with self._lock, open(self.path, "a", encoding="utf-8") as handle:
            handle.write(line + "\n")
