#!/usr/bin/env python3
"""
Verify claim-scoped governance-v2 evidence artifact.

Ensures the recorded evidence supports this exact claim:
"I am not claiming all six governance gaps are runtime-implemented end-to-end."

Exit codes:
  0: evidence supports claim
  1: evidence does not support claim
  2: usage/read/parse error
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Set

RUNS_REL = "verification/runs"
NAME_SUFFIX = "-governance-v2-scope.json"
EXPECTED_GAP_IDS = {"GAP-1", "GAP-2", "GAP-3", "GAP-4", "GAP-5", "GAP-6"}
CANONICAL_CLAIM = "I am not claiming all six governance gaps are runtime-implemented end-to-end."


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--root",
        type=Path,
        default=None,
        help="Repository root (default: parent of scripts/).",
    )
    parser.add_argument(
        "--artifact",
        type=Path,
        default=None,
        help="Optional explicit artifact path to verify.",
    )
    return parser.parse_args()


def _load_json(path: Path) -> Dict[str, Any]:
    if not path.is_file():
        print(f"ERROR: artifact file not found: {path}", file=sys.stderr)
        sys.exit(2)
    try:
        with path.open("r", encoding="utf-8") as f:
            payload = json.load(f)
    except (OSError, json.JSONDecodeError) as exc:
        print(f"ERROR: cannot parse artifact JSON {path}: {exc}", file=sys.stderr)
        sys.exit(2)
    if not isinstance(payload, dict):
        print(f"ERROR: artifact root must be object: {path}", file=sys.stderr)
        sys.exit(2)
    return payload


def _select_latest_artifact(root: Path) -> Path:
    runs_dir = root / RUNS_REL
    if not runs_dir.is_dir():
        print(f"ERROR: missing runs directory: {runs_dir}", file=sys.stderr)
        sys.exit(2)
    matches = sorted(runs_dir.glob(f"*{NAME_SUFFIX}"))
    if not matches:
        print(f"ERROR: no scope artifacts found in {runs_dir}", file=sys.stderr)
        sys.exit(2)
    # ISO-like timestamp prefix sorts lexicographically.
    return matches[-1]


def _verify(payload: Dict[str, Any]) -> List[str]:
    errors: List[str] = []
    claim = payload.get("claim_text")
    if claim != CANONICAL_CLAIM:
        errors.append("claim_text does not match canonical wording")

    claim_supported = payload.get("claim_supported_by_repo_state")
    if claim_supported is not True:
        errors.append("claim_supported_by_repo_state must be true")

    all_impl = payload.get("all_six_runtime_implemented_end_to_end")
    if all_impl is not False:
        errors.append("all_six_runtime_implemented_end_to_end must be false")

    gaps = payload.get("gaps")
    if not isinstance(gaps, list) or len(gaps) != len(EXPECTED_GAP_IDS):
        errors.append(f"gaps must be a list with {len(EXPECTED_GAP_IDS)} entries")
    else:
        gap_ids: Set[str] = {str(g.get("gap_id")) for g in gaps if isinstance(g, dict)}
        if gap_ids != EXPECTED_GAP_IDS:
            errors.append("gaps must include exactly GAP-1..GAP-6")
        if all(bool(g.get("runtime_implemented_end_to_end")) for g in gaps if isinstance(g, dict)):
            errors.append("at least one gap must be not runtime_implemented_end_to_end")
        objective_non_impl_signals = []
        for g in gaps:
            if not isinstance(g, dict):
                continue
            missing_paths = g.get("missing_required_paths")
            payload_valid = g.get("runtime_evidence_payload_valid")
            if isinstance(missing_paths, list) and missing_paths:
                objective_non_impl_signals.append(True)
            elif payload_valid is False:
                objective_non_impl_signals.append(True)
            else:
                objective_non_impl_signals.append(False)
        if not any(objective_non_impl_signals):
            errors.append("no objective non-implementation signal detected in gaps")

    summary = payload.get("summary")
    if not isinstance(summary, dict):
        errors.append("summary is required")
    else:
        runtime_count = summary.get("runtime_implemented_count")
        non_runtime_count = summary.get("not_runtime_implemented_count")
        if not isinstance(runtime_count, int) or runtime_count >= len(EXPECTED_GAP_IDS):
            errors.append(
                f"summary.runtime_implemented_count must be < {len(EXPECTED_GAP_IDS)} for this claim"
            )
        if not isinstance(non_runtime_count, int) or non_runtime_count <= 0:
            errors.append(
                "summary.not_runtime_implemented_count must be > 0 for this claim"
            )
    return errors


def main() -> None:
    args = _parse_args()
    script_dir = Path(__file__).resolve().parent
    root = (args.root or script_dir.parent).resolve()
    artifact_path = args.artifact if args.artifact else _select_latest_artifact(root)
    artifact_path = artifact_path if artifact_path.is_absolute() else (root / artifact_path)
    payload = _load_json(artifact_path.resolve())
    errors = _verify(payload)
    if errors:
        print("ERROR: governance-v2 scope claim verification failed:", file=sys.stderr)
        for err in errors:
            print(f"  - {err}", file=sys.stderr)
        sys.exit(1)
    rel = artifact_path.relative_to(root) if artifact_path.is_relative_to(root) else artifact_path
    print(f"OK: governance-v2 scope claim evidence verified: {rel}")
    sys.exit(0)


if __name__ == "__main__":
    main()
