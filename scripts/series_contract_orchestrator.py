#!/usr/bin/env python3
"""
Series contract orchestrator.

Enforces sequential execution with hard completion gates:
- only one `active` contract at a time
- next contract cannot activate until current is marked complete
- completion gates must pass before completion is accepted
"""

from __future__ import annotations

import argparse
import json
import shlex
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List


def _utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _load_state(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _save_state(path: Path, data: Dict[str, Any]) -> None:
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def _state_path(root: Path, series: str) -> Path:
    return root / "plans" / series / "CONTRACT_STATE.json"


def _contracts(data: Dict[str, Any]) -> List[Dict[str, Any]]:
    items = data.get("contracts")
    if not isinstance(items, list):
        raise ValueError("contracts must be a list")
    return items


def _validate(data: Dict[str, Any]) -> None:
    ids = []
    active_count = 0
    for c in _contracts(data):
        cid = str(c.get("id") or "").strip()
        if not cid:
            raise ValueError("contract id is required")
        if cid in ids:
            raise ValueError(f"duplicate contract id: {cid}")
        ids.append(cid)
        st = str(c.get("status") or "").strip()
        if st not in {"queued", "active", "complete"}:
            raise ValueError(f"invalid status for {cid}: {st}")
        if st == "active":
            active_count += 1
    if active_count > 1:
        raise ValueError("only one active contract is allowed")
    _validate_sequence(_contracts(data))


def _validate_sequence(items: List[Dict[str, Any]]) -> None:
    """
    Enforce strict progression shape:
    complete* -> active? -> queued*
    """
    seen_active = False
    seen_queued = False
    for c in items:
        cid = str(c.get("id") or "").strip()
        st = str(c.get("status") or "").strip()
        if st == "complete":
            if seen_active or seen_queued:
                raise ValueError(f"invalid state order: complete after non-complete at {cid}")
        elif st == "active":
            if seen_active or seen_queued:
                raise ValueError(f"invalid state order: active out of position at {cid}")
            seen_active = True
        elif st == "queued":
            seen_queued = True


def _active_contract(items: List[Dict[str, Any]]) -> Dict[str, Any] | None:
    for c in items:
        if c.get("status") == "active":
            return c
    return None


def _first_queued(items: List[Dict[str, Any]]) -> Dict[str, Any] | None:
    for c in items:
        if c.get("status") == "queued":
            return c
    return None


def _print_status(data: Dict[str, Any]) -> None:
    for c in _contracts(data):
        cid = c["id"]
        st = c["status"]
        title = c.get("title", "")
        marker = "->" if st == "active" else "  "
        print(f"{marker} {cid:<6} {st:<8} {title}")


def _run_gate(cmd: str, root: Path) -> None:
    _validate_gate_command(cmd)
    args = shlex.split(cmd)
    result = subprocess.run(args, cwd=str(root), capture_output=True, text=True)
    if result.returncode != 0:
        out = (result.stdout or "").strip()
        err = (result.stderr or "").strip()
        raise RuntimeError(
            "gate failed: " + cmd + ("\n" + out if out else "") + ("\n" + err if err else "")
        )


def _validate_gate_command(cmd: str) -> None:
    """
    Keep completion gates deterministic and auditable by restricting command prefixes.
    """
    allowed_prefixes = (
        "python3 scripts/",
        "python3 -c ",
        "./scripts/",
        "git status",
        "git diff",
        "git rev-parse",
    )
    if not cmd.startswith(allowed_prefixes):
        raise RuntimeError(f"disallowed gate command prefix: {cmd}")


def cmd_status(root: Path, series: str) -> int:
    path = _state_path(root, series)
    if not path.is_file():
        print(f"missing state file: {path}", file=sys.stderr)
        return 2
    data = _load_state(path)
    _validate(data)
    _print_status(data)
    return 0


def cmd_start_next(root: Path, series: str) -> int:
    path = _state_path(root, series)
    data = _load_state(path)
    _validate(data)
    items = _contracts(data)

    active = _active_contract(items)
    if active is not None:
        print(f"{active['id']} already active")
        return 0

    nxt = _first_queued(items)
    if nxt is None:
        print("no queued contracts remain")
        return 0

    # Enforce strict ordering: all earlier contracts must be complete.
    idx = items.index(nxt)
    for prev in items[:idx]:
        if prev.get("status") != "complete":
            raise RuntimeError(
                f"cannot activate {nxt['id']}: prior contract {prev['id']} is {prev.get('status')}"
            )

    nxt["status"] = "active"
    nxt["activated_at_utc"] = _utc_now()
    _save_state(path, data)
    print(f"activated {nxt['id']}")
    return 0


def cmd_complete(root: Path, series: str, contract_id: str) -> int:
    path = _state_path(root, series)
    data = _load_state(path)
    _validate(data)
    items = _contracts(data)

    target = None
    for c in items:
        if c.get("id") == contract_id:
            target = c
            break
    if target is None:
        raise RuntimeError(f"unknown contract id: {contract_id}")
    if target.get("status") != "active":
        raise RuntimeError(f"{contract_id} must be active before completion")

    gates = target.get("completion_gates") or []
    if not isinstance(gates, list):
        raise RuntimeError(f"{contract_id} completion_gates must be a list")
    for gate in gates:
        cmd = str(gate or "").strip()
        if not cmd:
            continue
        print(f"running gate: {cmd}")
        _run_gate(cmd, root)

    target["status"] = "complete"
    target["completed_at_utc"] = _utc_now()

    # Auto-activate next queued contract.
    next_one = _first_queued(items)
    if next_one is not None:
        next_one["status"] = "active"
        next_one["activated_at_utc"] = _utc_now()
        print(f"auto-activated next contract: {next_one['id']}")

    _save_state(path, data)
    print(f"completed {contract_id}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)

    p_status = sub.add_parser("status")
    p_status.add_argument("--series", required=True)
    p_status.add_argument("--root", default=".", help="repo root path")

    p_start = sub.add_parser("start-next")
    p_start.add_argument("--series", required=True)
    p_start.add_argument("--root", default=".", help="repo root path")

    p_complete = sub.add_parser("complete")
    p_complete.add_argument("--series", required=True)
    p_complete.add_argument("--id", required=True)
    p_complete.add_argument("--root", default=".", help="repo root path")

    args = parser.parse_args()
    root = Path(args.root).resolve()
    try:
        if args.command == "status":
            return cmd_status(root, args.series)
        if args.command == "start-next":
            return cmd_start_next(root, args.series)
        if args.command == "complete":
            return cmd_complete(root, args.series, args.id)
        return 2
    except Exception as exc:  # pragma: no cover
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
