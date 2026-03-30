#!/usr/bin/env python3
"""
Append a regression-ledger record after a green governance run (CI).

Reads newest verification/runs/*-governance.json, GitHub env vars, updates
verification/regression-ledger/ledger.json in the workspace.

Exit: 0 OK, 1 error, 2 missing deps
"""

from __future__ import annotations

import hashlib
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List

try:
    from jsonschema import Draft202012Validator
except ImportError:
    print("ERROR: jsonschema required", file=sys.stderr)
    sys.exit(2)


def _load_json(path: Path) -> Dict[str, Any]:
    with path.open("r", encoding="utf-8") as f:
        data = json.load(f)
    if not isinstance(data, dict):
        raise ValueError("expected object")
    return data


def _workflow_sha256(root: Path) -> str:
    p = root / ".github" / "workflows" / "verify.yml"
    if not p.is_file():
        return ""
    return hashlib.sha256(p.read_bytes()).hexdigest()


def _newest_governance_run(root: Path) -> Path:
    runs = sorted(
        (root / "verification" / "runs").glob("*-governance.json"),
        key=lambda p: p.stat().st_mtime,
    )
    if not runs:
        raise FileNotFoundError("no verification/runs/*-governance.json")
    return runs[-1]


def _conclusion_from_run(payload: Dict[str, Any]) -> str:
    st = str(payload.get("run_status") or "")
    if st == "passed":
        return "success"
    if st == "failed":
        return "failure"
    return "failure"


def _escalation_for_inventory(
    conclusion: str,
    event_name: str,
    scheduled_fail_streak: int,
    threshold: int,
) -> str:
    if conclusion != "success":
        if event_name == "schedule" and scheduled_fail_streak + 1 >= threshold:
            return "blocking"
        return "review_required"
    return "none"


def main() -> None:
    root = Path(os.environ.get("GITHUB_WORKSPACE", ".")).resolve()
    if os.environ.get("GITHUB_ACTIONS", "").lower() != "true":
        print("SKIP: append_regression_ledger only runs in GitHub Actions", file=sys.stderr)
        sys.exit(0)

    run_path = _newest_governance_run(root)
    payload = _load_json(run_path)
    commit = str(payload.get("commit_hash") or "").strip()
    wf_sha = str(payload.get("verify_workflow_sha256") or _workflow_sha256(root))

    run_id = (os.environ.get("GITHUB_RUN_ID") or "").strip()
    attempt = (os.environ.get("GITHUB_RUN_ATTEMPT") or "1").strip()
    wf_name = (os.environ.get("GITHUB_WORKFLOW") or "Verify Living Constitution").strip()
    ref = (os.environ.get("GITHUB_REF") or "refs/unknown").strip()
    event_name = (os.environ.get("GITHUB_EVENT_NAME") or "unknown").strip()
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    artifact_name = f"governance-verification-runs-{run_id}-{attempt}"
    artifact_ref = f"actions artifact name={artifact_name}; run_url=https://github.com/{os.environ.get('GITHUB_REPOSITORY','')}/actions/runs/{run_id}"

    pol_path = root / "verification" / "review-escalation-policy.json"
    threshold = 3
    if pol_path.is_file():
        pol = _load_json(pol_path)
        threshold = int(pol.get("scheduled_consecutive_failure_threshold") or 3)

    ledger_path = root / "verification" / "regression-ledger" / "ledger.json"
    ledger = _load_json(ledger_path)
    records: List[Dict[str, Any]] = list(ledger.get("records") or [])

    sched = [r for r in records if isinstance(r, dict) and str(r.get("github_event_name")) == "schedule"]
    fail_streak = 0
    for r in reversed(sched):
        if str(r.get("conclusion")) == "failure":
            fail_streak += 1
        else:
            break

    conclusion = _conclusion_from_run(payload)
    esc = _escalation_for_inventory(conclusion, event_name, fail_streak, threshold)
    reviewer = "not_required" if esc in ("none",) else "pending"

    if esc == "blocking":
        tip_truth = "tip_blocked"
    elif conclusion == "success":
        tip_truth = "tip_verified"
    else:
        tip_truth = "tip_pending"

    record: Dict[str, Any] = {
        "run_id": run_id,
        "run_attempt": attempt,
        "workflow_name": wf_name,
        "workflow_sha256": wf_sha,
        "commit_sha": commit,
        "branch_ref": ref,
        "timestamp_utc": ts,
        "conclusion": "success" if conclusion == "success" else "failure",
        "artifact_name": artifact_name,
        "artifact_path": str(run_path.relative_to(root)),
        "artifact_retrieval_ref": artifact_ref,
        "reviewer_status": reviewer,
        "escalation_state": esc,
        "github_event_name": event_name,
        "tip_state_truth": tip_truth,
        "notes": "appended by scripts/append_regression_ledger.py",
    }
    records.append(record)
    ledger["records"] = records

    schema_path = root / "verification" / "regression-ledger.schema.json"
    schema = _load_json(schema_path)
    Draft202012Validator.check_schema(schema)
    Draft202012Validator(schema).validate(ledger)

    with ledger_path.open("w", encoding="utf-8") as f:
        json.dump(ledger, f, indent=2, sort_keys=False)
        f.write("\n")
    print(f"OK: appended regression ledger record for run {run_id}")
    sys.exit(0)


if __name__ == "__main__":
    main()
