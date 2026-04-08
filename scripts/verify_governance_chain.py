#!/usr/bin/env python3
"""
verify_ac006_log.py — AC-006 Evidence Log Auditor (CRSP-001)

Acceptance Criterion: AC-006
  Every intercepted tool-call decision record in verification/crsp_CRSP-001_log.json
  must satisfy:

  Requirement A: timestamp, agent_id, tool_name, decision, rationale are all present.
  Requirement B: Every FAIL decision has at least one associated violated_invariant ID.

Read-only: no files are written.
Exit codes: 0 = chain unbroken, 1 = violation(s) found, 2 = usage/read error.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

LOG_PATH_DEFAULT = "verification/crsp_CRSP-001_log.json"

# Fields AC-006 Requirement A mandates on every decision entry.
_REQUIRED_FIELDS = ("timestamp", "agent_id", "tool_name", "decision", "rationale")


# ---------------------------------------------------------------------------
# Argument parsing
# ---------------------------------------------------------------------------

def _parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument(
        "--root",
        type=Path,
        default=None,
        help="TLC repository root (default: parent of scripts/)",
    )
    p.add_argument(
        "--log",
        type=Path,
        default=None,
        help=f"Explicit log path override (default: <root>/{LOG_PATH_DEFAULT})",
    )
    return p.parse_args()


# ---------------------------------------------------------------------------
# Log loading and entry flattening
# ---------------------------------------------------------------------------

def _load_log(log_path: Path) -> Any:
    if not log_path.is_file():
        print(f"ERROR: log file not found: {log_path}", file=sys.stderr)
        sys.exit(2)
    try:
        with log_path.open("r", encoding="utf-8") as fh:
            return json.load(fh)
    except (OSError, json.JSONDecodeError) as exc:
        print(f"ERROR: cannot parse log JSON at {log_path}: {exc}", file=sys.stderr)
        sys.exit(2)


def _flatten_entries(raw: Any) -> List[Dict[str, Any]]:
    """
    Return a flat list of entry dicts regardless of log shape.

    The log may be:
      - A top-level array of entries (guardian runtime entries)
      - A top-level array where some items are CRSP pipeline objects with a
        nested 'events' list (Stage-2 execution log)
      - A single top-level object
    """
    entries: List[Dict[str, Any]] = []

    def _absorb(obj: Any) -> None:
        if not isinstance(obj, dict):
            return
        nested = obj.get("events")
        if isinstance(nested, list):
            for ev in nested:
                if isinstance(ev, dict):
                    entries.append(ev)
        else:
            entries.append(obj)

    if isinstance(raw, list):
        for item in raw:
            _absorb(item)
    else:
        _absorb(raw)

    return entries


# ---------------------------------------------------------------------------
# Decision entry detection
# ---------------------------------------------------------------------------

def _is_decision_entry(entry: Dict[str, Any]) -> bool:
    """
    True when an entry represents an intercepted tool-call decision.

    Detection heuristics (any is sufficient):
      1. Has both agent_id and tool_name (guardian runtime intercept records).
      2. event/action field contains INTERCEPT, PASS_FORWARD, or FAIL_HALT.
    """
    if entry.get("agent_id") and entry.get("tool_name"):
        return True
    event_label = str(entry.get("event") or entry.get("action") or "").upper()
    return any(
        marker in event_label
        for marker in ("INTERCEPT", "PASS_FORWARD", "FAIL_HALT")
    )


# ---------------------------------------------------------------------------
# Field extractors — tolerant of varying log shapes
# ---------------------------------------------------------------------------

def _get_timestamp(entry: Dict[str, Any]) -> Optional[str]:
    for key in ("timestamp", "timestamp_utc", "created_at_utc"):
        val = entry.get(key)
        if val and str(val).strip():
            return str(val).strip()
    return None


def _get_decision(entry: Dict[str, Any]) -> Optional[str]:
    """
    Resolve overall decision: explicit 'decision' field > 'status' field >
    derived from invariant_results (any FAIL → FAIL, else PASS).
    """
    for key in ("decision", "status"):
        val = str(entry.get(key) or "").strip().upper()
        if val in ("PASS", "FAIL"):
            return val

    results = entry.get("invariant_results") or []
    if not results:
        return None

    for r in results:
        if isinstance(r, dict) and str(r.get("result") or "").upper() == "FAIL":
            return "FAIL"
    return "PASS"


def _get_rationale(entry: Dict[str, Any]) -> Optional[str]:
    """
    Resolve rationale: explicit 'rationale'/'reason'/'summary' field >
    concatenated FAIL reasons from invariant_results.
    """
    for key in ("rationale", "reason", "summary"):
        val = entry.get(key)
        if val and str(val).strip():
            return str(val).strip()

    results = entry.get("invariant_results") or []
    fail_reasons = [
        str(r.get("reason") or r.get("rationale") or "").strip()
        for r in results
        if isinstance(r, dict) and str(r.get("result") or "").upper() == "FAIL"
    ]
    fail_reasons = [r for r in fail_reasons if r]
    if fail_reasons:
        return " | ".join(fail_reasons)

    # Fall back to all reasons if decision is not FAIL but rationale still needed
    all_reasons = [
        str(r.get("reason") or r.get("rationale") or "").strip()
        for r in results
        if isinstance(r, dict)
    ]
    all_reasons = [r for r in all_reasons if r]
    if all_reasons:
        return all_reasons[0]

    return None


def _get_violated_invariants(entry: Dict[str, Any]) -> List[str]:
    """
    Collect violated invariant IDs from a FAIL entry.

    Sources (merged, deduplicated, order-preserved):
      1. 'violated_invariants' list (explicit top-level field)
      2. 'violated_invariant' string (singular top-level field)
      3. invariant_results[*] where result == "FAIL" → invariant_id
    """
    violated: List[str] = []
    seen: set = set()

    def _add(v: str) -> None:
        v = v.strip()
        if v and v not in seen:
            seen.add(v)
            violated.append(v)

    vi_list = entry.get("violated_invariants")
    if isinstance(vi_list, list):
        for x in vi_list:
            if x:
                _add(str(x))

    vi_str = entry.get("violated_invariant")
    if vi_str:
        _add(str(vi_str))

    for r in entry.get("invariant_results") or []:
        if isinstance(r, dict) and str(r.get("result") or "").upper() == "FAIL":
            inv_id = str(r.get("invariant_id") or r.get("id") or "").strip()
            if inv_id:
                _add(inv_id)

    return violated


# ---------------------------------------------------------------------------
# Core audit
# ---------------------------------------------------------------------------

def audit_log(log_path: Path) -> Tuple[List[str], int, int]:
    """
    Audit a CRSP-001 evidence log against AC-006 requirements.

    Returns:
        violations       — list of human-readable violation strings
        total_decisions  — number of decision entries examined
        fail_count       — number of FAIL decisions found
    """
    raw = _load_log(log_path)
    all_entries = _flatten_entries(raw)

    violations: List[str] = []
    total_decisions = 0
    fail_count = 0

    for idx, entry in enumerate(all_entries):
        if not _is_decision_entry(entry):
            continue

        total_decisions += 1

        event_label = entry.get("event") or entry.get("action") or "?"
        agent = entry.get("agent_id") or "?"
        tool = entry.get("tool_name") or "?"
        ctx = f"entry[{idx}] event={event_label!r} agent={agent!r} tool={tool!r}"

        # ---- Requirement A: required fields ----

        ts = _get_timestamp(entry)
        if not ts:
            violations.append(f"[AC-006/A] {ctx}: missing 'timestamp'")

        if not entry.get("agent_id"):
            violations.append(f"[AC-006/A] {ctx}: missing 'agent_id'")

        if not entry.get("tool_name"):
            violations.append(f"[AC-006/A] {ctx}: missing 'tool_name'")

        decision = _get_decision(entry)
        if not decision:
            violations.append(
                f"[AC-006/A] {ctx}: cannot determine 'decision' "
                "(expected PASS or FAIL at top-level or via invariant_results)"
            )

        rationale = _get_rationale(entry)
        if not rationale:
            violations.append(f"[AC-006/A] {ctx}: missing 'rationale'")

        # ---- Requirement B: FAIL must carry violated_invariant IDs ----

        if decision == "FAIL":
            fail_count += 1
            violated = _get_violated_invariants(entry)
            if not violated:
                violations.append(
                    f"[AC-006/B] {ctx}: FAIL decision has no violated_invariant ID(s)"
                )
            else:
                # Informational — confirm which invariants were violated
                print(
                    f"  FAIL  agent={agent!r} tool={tool!r} "
                    f"violated={violated}"
                )

    return violations, total_decisions, fail_count


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main() -> None:
    args = _parse_args()
    script_dir = Path(__file__).resolve().parent
    root = (args.root or script_dir.parent).resolve()

    if args.log:
        log_path = args.log if args.log.is_absolute() else root / args.log
    else:
        log_path = root / LOG_PATH_DEFAULT

    print(f"AC-006 audit — log: {log_path.relative_to(root) if log_path.is_relative_to(root) else log_path}")

    violations, total, fails = audit_log(log_path)

    print(f"Decision entries examined : {total}")
    print(f"FAIL decisions found      : {fails}")
    print(f"Violations                : {len(violations)}")

    if violations:
        print("\nVIOLATIONS DETAIL:", file=sys.stderr)
        for v in violations:
            print(f"  {v}", file=sys.stderr)
        print(
            "\nERROR: AC-006 governance chain BROKEN — "
            f"{len(violations)} violation(s) found. Exit 1.",
            file=sys.stderr,
        )
        sys.exit(1)

    print("OK: AC-006 governance chain is unbroken. Exit 0.")
    sys.exit(0)


if __name__ == "__main__":
    main()
