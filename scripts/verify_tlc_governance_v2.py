#!/usr/bin/env python3
"""
Verify governance/tlc-governance-v2.refactor.json shape and invariants.

Exit codes:
  0: verification passed
  1: verification failed
  2: usage/read error
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, Iterable, List, Set

DEFAULT_REL_PATH = "governance/tlc-governance-v2.refactor.json"
REQUIRED_GAP_IDS = {"GAP-1", "GAP-2", "GAP-3", "GAP-4", "GAP-5", "GAP-6"}
REQUIRED_PHASE_KEYS = {"phase_0", "phase_1", "phase_2", "phase_3"}
REQUIRED_DIMENSIONS = {"safety", "scope", "ethics", "transparency"}


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--root",
        type=Path,
        default=None,
        help="Repository root (default: parent of scripts/)",
    )
    parser.add_argument(
        "--spec",
        type=Path,
        default=None,
        help=f"Explicit path to spec JSON (default: <root>/{DEFAULT_REL_PATH})",
    )
    return parser.parse_args()


def _load_json(path: Path) -> Dict[str, Any]:
    if not path.is_file():
        print(f"ERROR: missing spec file: {path}", file=sys.stderr)
        sys.exit(2)
    try:
        with path.open("r", encoding="utf-8") as f:
            data = json.load(f)
    except (OSError, json.JSONDecodeError) as exc:
        print(f"ERROR: failed to parse JSON at {path}: {exc}", file=sys.stderr)
        sys.exit(2)
    if not isinstance(data, dict):
        print(f"ERROR: top-level JSON must be an object: {path}", file=sys.stderr)
        sys.exit(2)
    return data


def _as_dict(obj: Any) -> Dict[str, Any]:
    return obj if isinstance(obj, dict) else {}


def _as_list(obj: Any) -> List[Any]:
    return obj if isinstance(obj, list) else []


def _has_strings(items: Iterable[Any]) -> bool:
    return all(isinstance(x, str) and x.strip() for x in items)


def _validate_meta(payload: Dict[str, Any], errors: List[str]) -> None:
    meta = _as_dict(payload.get("meta"))
    if not meta.get("id"):
        errors.append("meta.id is required")
    sources = _as_list(meta.get("sources"))
    if len(sources) < 3 or not _has_strings(sources):
        errors.append("meta.sources must contain at least 3 non-empty paths")


def _validate_intent_monitor(payload: Dict[str, Any], errors: List[str]) -> None:
    monitor = _as_dict(payload.get("intent_monitor"))
    dims = _as_dict(monitor.get("dimensions"))
    dim_keys = set(dims.keys())
    missing = REQUIRED_DIMENSIONS - dim_keys
    if missing:
        errors.append(f"intent_monitor.dimensions missing: {sorted(missing)}")
        return

    total_weight = 0.0
    for name in sorted(REQUIRED_DIMENSIONS):
        d = _as_dict(dims.get(name))
        weight = d.get("weight")
        threshold = d.get("threshold")
        if not isinstance(weight, (int, float)) or weight <= 0:
            errors.append(f"intent_monitor.dimensions.{name}.weight must be > 0")
            continue
        total_weight += float(weight)
        if not isinstance(threshold, (int, float)) or not (0 <= float(threshold) <= 1):
            errors.append(f"intent_monitor.dimensions.{name}.threshold must be in [0,1]")
        rules = _as_list(d.get("rules"))
        if not rules:
            errors.append(f"intent_monitor.dimensions.{name}.rules must be non-empty")
            continue
        for idx, rule in enumerate(rules):
            rd = _as_dict(rule)
            if not rd.get("id"):
                errors.append(f"intent_monitor.dimensions.{name}.rules[{idx}] missing id")
            if not rd.get("observable_input"):
                errors.append(
                    f"intent_monitor.dimensions.{name}.rules[{idx}] missing observable_input"
                )
            if not rd.get("evidence_source"):
                errors.append(
                    f"intent_monitor.dimensions.{name}.rules[{idx}] missing evidence_source"
                )
            penalty = rd.get("penalty")
            if not isinstance(penalty, (int, float)) or not (0 < float(penalty) <= 1):
                errors.append(
                    f"intent_monitor.dimensions.{name}.rules[{idx}] penalty must be in (0,1]"
                )

    if abs(total_weight - 1.0) > 1e-9:
        errors.append(f"intent_monitor dimension weights must sum to 1.0, got {total_weight}")

    composite = _as_dict(monitor.get("composite"))
    method = composite.get("method")
    if method != "weighted_sum":
        errors.append("intent_monitor.composite.method must be weighted_sum")
    override = _as_dict(composite.get("override"))
    if override.get("rule") != "any_dimension_below":
        errors.append("intent_monitor.composite.override.rule must be any_dimension_below")
    threshold = override.get("threshold")
    if not isinstance(threshold, (int, float)) or not (0 <= float(threshold) <= 1):
        errors.append("intent_monitor.composite.override.threshold must be in [0,1]")

    calibration = _as_dict(monitor.get("calibration"))
    r_min = calibration.get("min_human_correlation_r")
    if not isinstance(r_min, (int, float)) or float(r_min) < 0.85:
        errors.append("intent_monitor.calibration.min_human_correlation_r must be >= 0.85")


def _validate_fsm(payload: Dict[str, Any], errors: List[str]) -> None:
    fsm = _as_dict(payload.get("governance_fsm"))
    states = _as_list(fsm.get("states"))
    if not states or not _has_strings(states):
        errors.append("governance_fsm.states must be non-empty strings")
        return

    state_set: Set[str] = {str(x) for x in states}
    terminal = _as_list(fsm.get("terminal_states"))
    if not terminal or not _has_strings(terminal):
        errors.append("governance_fsm.terminal_states must be non-empty strings")
        return
    terminal_set = {str(x) for x in terminal}
    if not terminal_set.issubset(state_set):
        errors.append("governance_fsm.terminal_states must be subset of states")

    transitions = _as_list(fsm.get("transitions"))
    if not transitions:
        errors.append("governance_fsm.transitions must be non-empty")
        return
    outgoing: Dict[str, int] = {s: 0 for s in state_set}
    has_vote_to_ratified = False
    for idx, tr in enumerate(transitions):
        td = _as_dict(tr)
        src = td.get("from")
        dst = td.get("to")
        evt = td.get("event")
        if src not in state_set or dst not in state_set:
            errors.append(f"governance_fsm.transitions[{idx}] has unknown state")
            continue
        if not isinstance(evt, str) or not evt.strip():
            errors.append(f"governance_fsm.transitions[{idx}] missing event")
        outgoing[src] = outgoing.get(src, 0) + 1
        if src == "VOTE" and dst == "RATIFIED":
            has_vote_to_ratified = True

    non_terminal = state_set - terminal_set
    for state in sorted(non_terminal):
        if outgoing.get(state, 0) == 0:
            errors.append(f"governance_fsm non-terminal state lacks outgoing transition: {state}")

    if not has_vote_to_ratified:
        errors.append("governance_fsm must include VOTE -> RATIFIED transition")

    timeouts = _as_dict(fsm.get("timeouts_hours"))
    if not timeouts:
        errors.append("governance_fsm.timeouts_hours must be non-empty")


def _validate_phase_criteria(payload: Dict[str, Any], errors: List[str]) -> None:
    phase = _as_dict(payload.get("phase_exit_criteria"))
    missing = REQUIRED_PHASE_KEYS - set(phase.keys())
    if missing:
        errors.append(f"phase_exit_criteria missing keys: {sorted(missing)}")
    for key in sorted(REQUIRED_PHASE_KEYS):
        criteria = _as_list(phase.get(key))
        if len(criteria) < 3 or not _has_strings(criteria):
            errors.append(f"phase_exit_criteria.{key} must contain at least 3 criteria strings")
    if phase.get("graduation_rule") != "all_criteria_required":
        errors.append("phase_exit_criteria.graduation_rule must be all_criteria_required")


def _validate_gaps(payload: Dict[str, Any], errors: List[str]) -> None:
    gaps = _as_list(payload.get("gap_cards"))
    if not gaps:
        errors.append("gap_cards must be non-empty")
        return
    ids = {str(_as_dict(g).get("id")) for g in gaps}
    missing = REQUIRED_GAP_IDS - ids
    if missing:
        errors.append(f"gap_cards missing ids: {sorted(missing)}")
    for idx, g in enumerate(gaps):
        gd = _as_dict(g)
        work_items = _as_list(gd.get("work_items"))
        done = _as_list(gd.get("definition_of_done"))
        if len(work_items) < 2 or not _has_strings(work_items):
            errors.append(f"gap_cards[{idx}] must include at least 2 work_items")
        if len(done) < 2 or not _has_strings(done):
            errors.append(f"gap_cards[{idx}] must include at least 2 definition_of_done items")


def _validate_innovation_gap_closers(payload: Dict[str, Any], errors: List[str]) -> None:
    ideas = _as_list(payload.get("innovation_gap_closers"))
    if len(ideas) < 3:
        errors.append("innovation_gap_closers must include at least 3 items")
    for idx, item in enumerate(ideas):
        entry = _as_dict(item)
        for key in ("id", "idea", "adapted_from", "governance_use"):
            if not isinstance(entry.get(key), str) or not entry.get(key).strip():
                errors.append(f"innovation_gap_closers[{idx}].{key} is required")


def main() -> None:
    args = _parse_args()
    script_dir = Path(__file__).resolve().parent
    root = (args.root or script_dir.parent).resolve()
    spec_path = (args.spec or (root / DEFAULT_REL_PATH)).resolve()

    payload = _load_json(spec_path)
    errors: List[str] = []

    _validate_meta(payload, errors)
    _validate_intent_monitor(payload, errors)
    _validate_fsm(payload, errors)
    _validate_phase_criteria(payload, errors)
    _validate_gaps(payload, errors)
    _validate_innovation_gap_closers(payload, errors)

    if errors:
        print("ERROR: TLC governance v2 verification failed:", file=sys.stderr)
        for err in errors:
            print(f"  - {err}", file=sys.stderr)
        sys.exit(1)

    rel = spec_path.relative_to(root) if spec_path.is_relative_to(root) else spec_path
    print(f"OK: TLC governance v2 refactor verification passed for {rel}")
    sys.exit(0)


if __name__ == "__main__":
    main()
