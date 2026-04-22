#!/usr/bin/env python3
"""
Generate concrete evidence for governance-v2 runtime implementation scope.

This artifact is intentionally claim-scoped:
it records whether all six governance gaps are runtime-implemented end-to-end.

Exit codes:
  0: artifact generated successfully
  1: validation failure while building report
  2: usage/read/write error
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Set

SPEC_REL = "governance/tlc-governance-v2.refactor.json"
RUNTIME_EVIDENCE_DIR_REL = "verification/governance-v2/runtime"
RUNS_REL = "verification/runs"
EXPECTED_GAP_IDS = {"GAP-1", "GAP-2", "GAP-3", "GAP-4", "GAP-5", "GAP-6"}
GAP_RUNTIME_PATH_REQUIREMENTS: Dict[str, List[str]] = {
    "GAP-1": [
        "packages/intent-monitor",
        "ops/calibration",
    ],
    "GAP-2": [
        "governance/voting",
    ],
    "GAP-3": [
        "governance/safety-board",
    ],
    "GAP-4": [
        "governance/appeals",
    ],
    "GAP-5": [
        "governance/proposal-fsm",
    ],
    "GAP-6": [
        "ops/phase-tracker",
    ],
}
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
        "--out",
        type=Path,
        default=None,
        help="Optional output path override for generated JSON artifact.",
    )
    return parser.parse_args()


def _load_json(path: Path) -> Dict[str, Any]:
    if not path.is_file():
        print(f"ERROR: file not found: {path}", file=sys.stderr)
        sys.exit(2)
    try:
        with path.open("r", encoding="utf-8") as f:
            payload = json.load(f)
    except (OSError, json.JSONDecodeError) as exc:
        print(f"ERROR: cannot parse JSON at {path}: {exc}", file=sys.stderr)
        sys.exit(2)
    if not isinstance(payload, dict):
        print(f"ERROR: top-level JSON must be object: {path}", file=sys.stderr)
        sys.exit(2)
    return payload


def _iso_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _normalize_status(value: Any) -> str:
    if not isinstance(value, str):
        return ""
    return value.strip().lower().replace("-", "_")


def _evaluate_required_paths(root: Path, rel_paths: List[str]) -> List[Dict[str, Any]]:
    evaluations: List[Dict[str, Any]] = []
    for rel in rel_paths:
        p = root / rel
        evaluations.append(
            {
                "path": rel,
                "exists": p.exists(),
                "is_dir": p.is_dir(),
                "is_file": p.is_file(),
            }
        )
    return evaluations


def _validate_runtime_evidence_payload(path: Path, gap_id: str) -> bool:
    if not path.is_file():
        return False
    try:
        with path.open("r", encoding="utf-8") as f:
            payload = json.load(f)
    except (OSError, json.JSONDecodeError):
        return False
    if not isinstance(payload, dict):
        return False
    if str(payload.get("gap_id") or "").strip() != gap_id:
        return False
    if payload.get("end_to_end_passed") is not True:
        return False
    entries = payload.get("evidence_entries")
    if not isinstance(entries, list) or not entries:
        return False
    return True


def _build_report(root: Path, spec: Dict[str, Any]) -> Dict[str, Any]:
    meta = spec.get("meta") if isinstance(spec.get("meta"), dict) else {}
    gap_cards = spec.get("gap_cards") if isinstance(spec.get("gap_cards"), list) else []
    runtime_dir = root / RUNTIME_EVIDENCE_DIR_REL

    if not gap_cards:
        print("ERROR: gap_cards missing or empty in governance-v2 refactor spec", file=sys.stderr)
        sys.exit(1)

    report_gaps: List[Dict[str, Any]] = []
    encountered_ids: Set[str] = set()
    for item in gap_cards:
        if not isinstance(item, dict):
            continue
        gap_id = str(item.get("id") or "").strip()
        title = str(item.get("title") or "").strip()
        status = _normalize_status(item.get("status"))
        if not gap_id:
            print("ERROR: encountered gap card with empty id", file=sys.stderr)
            sys.exit(1)
        encountered_ids.add(gap_id)
        required_rel_paths = GAP_RUNTIME_PATH_REQUIREMENTS.get(gap_id, [])
        required_paths = _evaluate_required_paths(root, required_rel_paths)
        required_paths_all_exist = bool(required_paths) and all(p["exists"] for p in required_paths)
        evidence_file = runtime_dir / f"{gap_id}.runtime-evidence.json"
        evidence_exists = evidence_file.is_file()
        evidence_payload_valid = _validate_runtime_evidence_payload(evidence_file, gap_id)
        runtime_implemented = required_paths_all_exist and evidence_payload_valid
        missing_required_paths = [p["path"] for p in required_paths if not p["exists"]]
        report_gaps.append(
            {
                "gap_id": gap_id,
                "title": title,
                "status": status,
                "required_runtime_paths": required_paths,
                "required_paths_all_exist": required_paths_all_exist,
                "missing_required_paths": missing_required_paths,
                "runtime_evidence_file": str(evidence_file.relative_to(root)),
                "runtime_evidence_file_exists": evidence_exists,
                "runtime_evidence_payload_valid": evidence_payload_valid,
                "runtime_implemented_end_to_end": runtime_implemented,
            }
        )

    missing_ids = sorted(EXPECTED_GAP_IDS - encountered_ids)
    if missing_ids:
        print(
            f"ERROR: governance-v2 refactor spec missing expected gap IDs: {missing_ids}",
            file=sys.stderr,
        )
        sys.exit(1)

    all_runtime_implemented = all(g["runtime_implemented_end_to_end"] for g in report_gaps)
    claim_supported = not all_runtime_implemented

    return {
        "artifact_type": "governance_v2_scope_claim_evidence",
        "generated_at_utc": _iso_now(),
        "claim_text": CANONICAL_CLAIM,
        "claim_supported_by_repo_state": claim_supported,
        "all_six_runtime_implemented_end_to_end": all_runtime_implemented,
        "spec_ref": SPEC_REL,
        "spec_meta": {
            "id": meta.get("id"),
            "status": meta.get("status"),
            "updated_utc": meta.get("updated_utc"),
        },
        "runtime_evidence_dir": RUNTIME_EVIDENCE_DIR_REL,
        "gaps": report_gaps,
        "summary": {
            "gap_count": len(report_gaps),
            "runtime_implemented_count": sum(1 for g in report_gaps if g["runtime_implemented_end_to_end"]),
            "not_runtime_implemented_count": sum(1 for g in report_gaps if not g["runtime_implemented_end_to_end"]),
            "missing_required_paths_count": sum(len(g["missing_required_paths"]) for g in report_gaps),
            "invalid_runtime_evidence_payload_count": sum(
                1 for g in report_gaps if not g["runtime_evidence_payload_valid"]
            ),
        },
    }


def main() -> None:
    args = _parse_args()
    script_dir = Path(__file__).resolve().parent
    root = (args.root or script_dir.parent).resolve()
    spec_path = (root / SPEC_REL).resolve()
    spec = _load_json(spec_path)

    report = _build_report(root, spec)

    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    default_out = root / RUNS_REL / f"{timestamp}-governance-v2-scope.json"
    out_path = (args.out if args.out else default_out)
    out_path = out_path if out_path.is_absolute() else (root / out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    try:
        with out_path.open("w", encoding="utf-8") as f:
            json.dump(report, f, indent=2)
            f.write("\n")
    except OSError as exc:
        print(f"ERROR: failed to write report at {out_path}: {exc}", file=sys.stderr)
        sys.exit(2)

    rel_out = out_path.relative_to(root) if out_path.is_relative_to(root) else out_path
    print(f"OK: generated governance-v2 scope evidence artifact: {rel_out}")
    print(
        "OK: claim_supported_by_repo_state="
        f"{report['claim_supported_by_repo_state']} "
        f"(all_six_runtime_implemented_end_to_end={report['all_six_runtime_implemented_end_to_end']})"
    )
    sys.exit(0)


if __name__ == "__main__":
    main()
