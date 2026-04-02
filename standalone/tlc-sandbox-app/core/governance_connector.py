#!/usr/bin/env python3
"""
Poll TLC root STATUS.json for constitutional halt authority (INVARIANT_04 / halt plane).

If ``sandbox_operational_state`` is ``OFF`` or ``QUARANTINE``, the process exits with
code 0 after emitting ``HALT_BY_CONSTITUTIONAL_AUTHORITY``.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, Dict, Optional


HALT_LOG_MESSAGE = "HALT_BY_CONSTITUTIONAL_AUTHORITY"
_HALT_LOG = HALT_LOG_MESSAGE


def read_status(tlc_root: Path) -> Optional[Dict[str, Any]]:
    path = tlc_root / "STATUS.json"
    if not path.is_file():
        return None
    try:
        with path.open("r", encoding="utf-8") as f:
            return json.load(f)
    except (OSError, json.JSONDecodeError):
        return None


def sandbox_operational_state(status: Optional[Dict[str, Any]]) -> str:
    if not status:
        return "ON"
    raw = status.get("sandbox_operational_state")
    if raw is None:
        return "ON"
    if isinstance(raw, str):
        return raw.strip().upper() or "ON"
    return "ON"


def should_halt(status: Optional[Dict[str, Any]]) -> bool:
    s = sandbox_operational_state(status)
    return s in ("OFF", "QUARANTINE")


def poll_halt_authority(tlc_root: Path) -> None:
    """
    If STATUS.json requests sandbox halt, log and exit the process immediately.
    Default when missing key or file: operational (no halt).
    """
    st = read_status(tlc_root)
    if should_halt(st):
        print(_HALT_LOG, file=sys.stderr)
        sys.exit(0)


def poll_halt_authority_non_destructive(tlc_root: Path) -> bool:
    """Return True if halt would trigger (for engine loop without exiting current process)."""
    return should_halt(read_status(tlc_root))
