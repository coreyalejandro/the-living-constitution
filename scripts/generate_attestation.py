#!/usr/bin/env python3
"""
PASS 14: Generate supply-chain attestation binding HEAD commit, verify.yml SHA256,
and a deterministic aggregate hash over verification/runs/*.json.

In GitHub Actions, REQUIRES: GITHUB_RUN_ID, GITHUB_REPOSITORY, GITHUB_SHA.
Optional: GITHUB_RUN_ATTEMPT (default "1").

Local/dev: set ATTESTATION_RUN_ID (and optionally ATTESTATION_REPOSITORY) if not in Actions.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Tuple

_SCRIPT_DIR = Path(__file__).resolve().parent
if str(_SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(_SCRIPT_DIR))

from jsonschema import Draft202012Validator  # noqa: E402
from jsonschema.exceptions import ValidationError  # noqa: E402

from tip_state_helpers import GovernanceError, assert_not_shallow  # noqa: E402


def _parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--root", type=Path, default=None, help="Repository root")
    return p.parse_args()


def _load_json(path: Path) -> Dict[str, Any]:
    with path.open("r", encoding="utf-8") as f:
        data = json.load(f)
    if not isinstance(data, dict):
        raise ValueError(f"expected object in {path}")
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


def _verification_runs_aggregate_sha256(runs_dir: Path) -> Tuple[str, List[str]]:
    if not runs_dir.is_dir():
        print(f"ERROR: missing {runs_dir}", file=sys.stderr)
        sys.exit(2)
    files = sorted(runs_dir.glob("*.json"), key=lambda p: p.name)
    if not files:
        print("ERROR: no verification/runs/*.json to attest", file=sys.stderr)
        sys.exit(2)
    parts: List[str] = []
    for p in files:
        digest = hashlib.sha256(p.read_bytes()).hexdigest()
        parts.append(f"{p.name}\t{digest}")
    canonical = "\n".join(parts).encode("utf-8")
    return hashlib.sha256(canonical).hexdigest(), [p.name for p in files]


def _latest_governance_basename(runs_dir: Path) -> str:
    gov = sorted(runs_dir.glob("*-governance.json"), key=lambda p: p.name)
    if not gov:
        print("ERROR: no *-governance.json under verification/runs/", file=sys.stderr)
        sys.exit(2)
    return gov[-1].name


def _invariants_from_governance_run(runs_dir: Path, basename: str) -> List[str]:
    data = _load_json(runs_dir / basename)
    inv = data.get("invariants_verified")
    if not isinstance(inv, list) or not inv:
        print(f"ERROR: {basename} missing invariants_verified[]", file=sys.stderr)
        sys.exit(2)
    out = [str(x) for x in inv if isinstance(x, str)]
    if not out:
        print(f"ERROR: {basename} has empty invariants_verified", file=sys.stderr)
        sys.exit(2)
    return sorted(out)


def main() -> None:
    args = _parse_args()
    root = (args.root or _SCRIPT_DIR.parent).resolve()
    try:
        assert_not_shallow(root)
    except GovernanceError as e:
        print(f"ERROR: {e.code}: {e}", file=sys.stderr)
        sys.exit(1)

    in_actions = os.environ.get("GITHUB_ACTIONS", "").lower() == "true"
    run_id = (os.environ.get("GITHUB_RUN_ID") or "").strip()
    run_attempt = (os.environ.get("GITHUB_RUN_ATTEMPT") or "1").strip()
    repository = (os.environ.get("GITHUB_REPOSITORY") or "").strip()
    gsha = (os.environ.get("GITHUB_SHA") or "").strip()

    if not run_id:
        run_id = (os.environ.get("ATTESTATION_RUN_ID") or "").strip()
    if not repository:
        repository = (os.environ.get("ATTESTATION_REPOSITORY") or "").strip()

    if not run_id or not repository:
        print(
            "ERROR: set GITHUB_RUN_ID and GITHUB_REPOSITORY (CI) or "
            "ATTESTATION_RUN_ID and ATTESTATION_REPOSITORY (local)",
            file=sys.stderr,
        )
        sys.exit(2)

    commit = _git_head(root)
    if in_actions and gsha and gsha != commit:
        print(
            f"ERROR: GITHUB_SHA {gsha!r} != git HEAD {commit!r}",
            file=sys.stderr,
        )
        sys.exit(2)

    wf_sha = _workflow_sha256(root)
    runs_dir = root / "verification" / "runs"
    agg_sha, _names = _verification_runs_aggregate_sha256(runs_dir)
    gov_base = _latest_governance_basename(runs_dir)
    inv_ok = _invariants_from_governance_run(runs_dir, gov_base)

    ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    payload: Dict[str, Any] = {
        "schema_version": "1.0.0",
        "github_repository": repository,
        "commit": commit,
        "workflow_sha256": wf_sha,
        "github_run_id": run_id,
        "github_run_attempt": run_attempt,
        "artifacts": {
            "verification_runs_aggregate_sha256": agg_sha,
            "governance_run_basename": gov_base,
        },
        "invariants_verified": inv_ok,
        "timestamp": ts,
    }

    schema_path = root / "verification" / "supply-chain-attestation.schema.json"
    try:
        schema = _load_json(schema_path)
        Draft202012Validator.check_schema(schema)
        Draft202012Validator(schema).validate(payload)
    except (OSError, ValueError, ValidationError) as e:
        print(f"ERROR: attestation schema validation failed: {e}", file=sys.stderr)
        sys.exit(2)

    out_dir = root / "verification" / "attestations"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / f"{run_id}-{run_attempt}.json"
    with out_path.open("w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2, sort_keys=True)
        f.write("\n")
    print(f"OK: attestation written {out_path.relative_to(root)}")


if __name__ == "__main__":
    main()
