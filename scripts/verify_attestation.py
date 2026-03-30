#!/usr/bin/env python3
"""
PASS 14: Verify supply-chain attestation (INVARIANT_57–59).

Recomputes workflow and verification/runs aggregate hashes and compares to attestation.
Fails if commit != git HEAD, workflow_sha256 mismatches, or artifact aggregate mismatches.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from pathlib import Path
from typing import Any, Dict, List

_SCRIPT_DIR = Path(__file__).resolve().parent
if str(_SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(_SCRIPT_DIR))

from jsonschema import Draft202012Validator  # noqa: E402
from jsonschema.exceptions import ValidationError  # noqa: E402

from tip_state_helpers import GovernanceError, assert_not_shallow  # noqa: E402


def _parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--root", type=Path, default=None, help="Repository root")
    p.add_argument(
        "--attestation",
        type=Path,
        required=True,
        help="Path to attestation JSON (e.g. verification/attestations/<run>-<attempt>.json)",
    )
    return p.parse_args()


def _load_json(path: Path) -> Dict[str, Any]:
    with path.open("r", encoding="utf-8") as f:
        data = json.load(f)
    if not isinstance(data, dict):
        raise ValueError("expected object")
    return data


def _git_head(root: Path) -> str:
    r = subprocess.run(
        ["git", "-C", str(root), "rev-parse", "HEAD"],
        capture_output=True,
        text=True,
        check=False,
    )
    h = (r.stdout or "").strip()
    if r.returncode != 0 or len(h) != 40:
        print("ERROR: git rev-parse HEAD failed", file=sys.stderr)
        sys.exit(2)
    return h


def _workflow_sha256(root: Path) -> str:
    p = root / ".github" / "workflows" / "verify.yml"
    if not p.is_file():
        print("ERROR: .github/workflows/verify.yml missing", file=sys.stderr)
        sys.exit(2)
    return hashlib.sha256(p.read_bytes()).hexdigest()


def _verification_runs_aggregate_sha256(runs_dir: Path) -> str:
    if not runs_dir.is_dir():
        print(f"ERROR: missing {runs_dir}", file=sys.stderr)
        sys.exit(2)
    files = sorted(runs_dir.glob("*.json"), key=lambda p: p.name)
    if not files:
        print("ERROR: no verification/runs/*.json", file=sys.stderr)
        sys.exit(2)
    parts: List[str] = []
    for p in files:
        digest = hashlib.sha256(p.read_bytes()).hexdigest()
        parts.append(f"{p.name}\t{digest}")
    canonical = "\n".join(parts).encode("utf-8")
    return hashlib.sha256(canonical).hexdigest()


def main() -> None:
    args = _parse_args()
    root = (args.root or _SCRIPT_DIR.parent).resolve()
    att_path = args.attestation if args.attestation.is_absolute() else root / args.attestation
    att_path = att_path.resolve()

    try:
        assert_not_shallow(root)
    except GovernanceError as e:
        print(f"ERROR: {e.code}: {e}", file=sys.stderr)
        sys.exit(1)

    if not att_path.is_file():
        print(f"ERROR: INVARIANT_57: attestation missing at {att_path}", file=sys.stderr)
        sys.exit(1)

    try:
        att = _load_json(att_path)
    except (OSError, json.JSONDecodeError, ValueError) as e:
        print(f"ERROR: cannot read attestation: {e}", file=sys.stderr)
        sys.exit(2)

    schema_path = root / "verification" / "supply-chain-attestation.schema.json"
    try:
        schema = _load_json(schema_path)
        Draft202012Validator.check_schema(schema)
        Draft202012Validator(schema).validate(att)
    except (OSError, ValueError, ValidationError) as e:
        print(f"ERROR: attestation failed schema validation: {e}", file=sys.stderr)
        sys.exit(1)

    head = _git_head(root)
    ac = str(att.get("commit") or "")
    if ac != head:
        print(
            f"ERROR: INVARIANT_57: attestation commit {ac!r} != git HEAD {head!r}",
            file=sys.stderr,
        )
        sys.exit(1)

    wh = _workflow_sha256(root)
    w_att = str(att.get("workflow_sha256") or "")
    if w_att != wh:
        print(
            f"ERROR: INVARIANT_58: workflow hash mismatch attestation={w_att!r} disk={wh!r}",
            file=sys.stderr,
        )
        sys.exit(1)

    arts = att.get("artifacts")
    if not isinstance(arts, dict):
        print("ERROR: INVARIANT_59: attestation artifacts missing", file=sys.stderr)
        sys.exit(1)
    exp_agg = str(arts.get("verification_runs_aggregate_sha256") or "")
    runs_dir = root / "verification" / "runs"
    got_agg = _verification_runs_aggregate_sha256(runs_dir)
    if exp_agg != got_agg:
        print(
            f"ERROR: INVARIANT_59: verification/runs aggregate mismatch "
            f"attestation={exp_agg!r} recomputed={got_agg!r}",
            file=sys.stderr,
        )
        sys.exit(1)

    gov_base = str(arts.get("governance_run_basename") or "")
    gpath = runs_dir / gov_base
    if not gpath.is_file():
        print(f"ERROR: INVARIANT_59: governance artifact missing {gpath}", file=sys.stderr)
        sys.exit(1)

    needed = {"INVARIANT_57", "INVARIANT_58", "INVARIANT_59"}
    got_inv = set(att.get("invariants_verified") or [])
    if not needed.issubset(got_inv):
        print(
            f"ERROR: INVARIANT_57: attestation invariants_verified must include {sorted(needed)} "
            f"(got subset check)",
            file=sys.stderr,
        )
        sys.exit(1)

    print("OK: supply-chain attestation verified")


if __name__ == "__main__":
    main()
