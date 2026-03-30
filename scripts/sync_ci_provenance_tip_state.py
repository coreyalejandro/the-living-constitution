#!/usr/bin/env python3
"""
Offline alignment helper: set ci_provenance tip fields from git HEAD, record.json,
and protected-surface diff (PASS 6 / PASS 7).

Does not claim remote success; does not push. Use after local commits until the next
qualifying GitHub Actions run updates verification/ci-remote-evidence/record.json.
PASS 7: inventory stays pending+tip_pending on mutable branch tips; use a tag or
frozen checkout per verification/pass7-branch-verification-policy.json to assert
tip_verified — do not set status=verified on feature/main from this script alone.

Exit: 0 wrote file, 1 error, 2 missing dependency
"""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any, Dict

_SCRIPT_DIR = Path(__file__).resolve().parent
if str(_SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(_SCRIPT_DIR))

from tip_state_helpers import load_tip_policy, protected_surfaces_changed  # noqa: E402


def _load_json(path: Path) -> Dict[str, Any]:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def _wf_sha(root: Path) -> str:
    p = root / ".github" / "workflows" / "verify.yml"
    if not p.is_file():
        return ""
    return hashlib.sha256(p.read_bytes()).hexdigest()


def _git_head(root: Path) -> str:
    git = shutil.which("git")
    if not git:
        raise RuntimeError("git not found")
    r = subprocess.run(
        [git, "-C", str(root), "rev-parse", "HEAD"],
        capture_output=True,
        text=True,
        check=False,
    )
    h = (r.stdout or "").strip()
    if r.returncode != 0 or len(h) < 7:
        raise RuntimeError((r.stderr or "").strip() or "git rev-parse failed")
    return h


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--root", type=Path, default=Path("."), help="Repository root")
    ap.add_argument("--dry-run", action="store_true", help="Print JSON only; do not write")
    args = ap.parse_args()
    root = args.root.resolve()
    inv_path = root / "MASTER_PROJECT_INVENTORY.json"
    rec_path = root / "verification" / "ci-remote-evidence" / "record.json"
    if not inv_path.is_file():
        print("ERROR: MASTER_PROJECT_INVENTORY.json missing", file=sys.stderr)
        sys.exit(2)
    inv = _load_json(inv_path)
    cp = inv.get("ci_provenance")
    if not isinstance(cp, dict):
        print("ERROR: ci_provenance missing", file=sys.stderr)
        sys.exit(1)
    if not rec_path.is_file():
        print("ERROR: verification/ci-remote-evidence/record.json missing", file=sys.stderr)
        sys.exit(2)
    rec = _load_json(rec_path)
    anchor = str(rec.get("artifact_commit_hash") or "").strip()
    if len(anchor) < 7:
        print("ERROR: record.json artifact_commit_hash invalid", file=sys.stderr)
        sys.exit(1)
    head = _git_head(root)
    pol = load_tip_policy(root)
    wf = _wf_sha(root)
    cp["last_remote_qualifying_commit"] = anchor
    cp["last_verified_commit"] = anchor
    cp["verify_workflow_sha256"] = wf
    cp["verify_workflow_sha256_at_last_remote_run"] = str(cp.get("verify_workflow_sha256_at_last_remote_run") or wf)
    if head == anchor:
        cp["status"] = "pending"
        cp["tip_state_truth"] = "tip_pending"
        cp["escalation_state"] = "none"
        cp["reviewer_status"] = cp.get("reviewer_status") or "not_required"
    else:
        changed, paths = protected_surfaces_changed(root, anchor, "HEAD", pol)
        cp["status"] = "pending"
        cp["tip_state_truth"] = "tip_pending"
        cp["escalation_state"] = "review_required" if changed else "none"
        cp["reviewer_status"] = "pending" if changed else (cp.get("reviewer_status") or "not_required")
    cp["last_verified_run_id"] = str(rec.get("workflow_run_id") or cp.get("last_verified_run_id") or "")
    cp["artifact_name"] = str(rec.get("artifact_name") or cp.get("artifact_name") or "")
    if args.dry_run:
        print(json.dumps(cp, indent=2))
        sys.exit(0)
    inv["ci_provenance"] = cp
    with inv_path.open("w", encoding="utf-8") as f:
        json.dump(inv, f, indent=2, sort_keys=False)
        f.write("\n")
    print("OK: updated MASTER_PROJECT_INVENTORY.json ci_provenance (tip-state helper)")
    sys.exit(0)


if __name__ == "__main__":
    try:
        main()
    except RuntimeError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(2)
