#!/usr/bin/env python3
"""
INVARIANT_06 — Gold Star audit trail: verification/SANDBOX_LOG.md
"""

from __future__ import annotations

import hashlib
from datetime import datetime, timezone
from pathlib import Path
from typing import Literal

_ACTOR = "project_id: sandbox-runtime-001"
_CONSTITUTION_NAME = "THE_LIVING_CONSTITUTION.md"


def sha256_file(path: Path) -> str:
    if not path.is_file():
        return "MISSING"
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def constitutional_hash(tlc_root: Path) -> str:
    return sha256_file(tlc_root / _CONSTITUTION_NAME)


def sandbox_log_path(tlc_root: Path) -> Path:
    return tlc_root / "verification" / "SANDBOX_LOG.md"


def ensure_initialized(tlc_root: Path) -> None:
    """Write header and first Initialized row if the ledger does not exist."""
    path = sandbox_log_path(tlc_root)
    if path.is_file():
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    ch = constitutional_hash(tlc_root)
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    body = f"""# Sandbox Evidence Ledger (Gold Star)

Structured audit trail for Lower Sandbox actions. One row per execution event.

| Timestamp (ISO 8601) | Actor | Action | Result | Constitutional Hash (SHA-256) |
|----------------------|-------|--------|--------|--------------------------------|
| {ts} | {_ACTOR} | Initialized ledger | Success | `{ch}` |
"""
    path.write_text(body, encoding="utf-8")


def append_entry(
    tlc_root: Path,
    action: str,
    result: Literal["Success", "Fail"],
    *,
    constitutional_hash_value: str | None = None,
    related_invariant: str | None = None,
) -> None:
    ensure_initialized(tlc_root)
    path = sandbox_log_path(tlc_root)
    ch = constitutional_hash_value if constitutional_hash_value is not None else constitutional_hash(tlc_root)
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    if related_invariant:
        action = f"{action} ({related_invariant})"
    line = f"| {ts} | {_ACTOR} | {action} | {result} | `{ch}` |\n"
    with path.open("a", encoding="utf-8") as f:
        f.write(line)
