#!/usr/bin/env python3
"""
Institutionalization verification (PASS 5): scheduled path, regression ledger,
review/escalation policy, independent review artifact, escalation vs inventory.

Exit: 0 OK, 1 governance breach, 2 usage/IO/schema dependency error
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
from pathlib import Path
from typing import Any, Dict, List

try:
    from jsonschema import Draft202012Validator
    from jsonschema.exceptions import ValidationError
except ImportError:
    print(
        "ERROR: jsonschema is required. Install: pip install -r requirements-verify.txt",
        file=sys.stderr,
    )
    sys.exit(2)

_SCRIPT_DIR = Path(__file__).resolve().parent
if str(_SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(_SCRIPT_DIR))

from tip_state_helpers import (  # noqa: E402
    GovernanceError,
    assert_not_shallow,
    git_preflight_fetch_tags_or_error,
)


def _load_json(path: Path) -> Dict[str, Any]:
    with path.open("r", encoding="utf-8") as f:
        data = json.load(f)
    if not isinstance(data, dict):
        raise ValueError("root must be object")
    return data


def _workflow_sha256(root: Path, rel: str = ".github/workflows/verify.yml") -> str:
    p = root / rel
    if not p.is_file():
        return ""
    return hashlib.sha256(p.read_bytes()).hexdigest()


def _validate_ledger(root: Path, errors: List[str]) -> None:
    schema_path = root / "verification" / "regression-ledger.schema.json"
    ledger_path = root / "verification" / "regression-ledger" / "ledger.json"
    if not schema_path.is_file():
        errors.append("INVARIANT_22: missing verification/regression-ledger.schema.json")
        return
    if not ledger_path.is_file():
        errors.append("INVARIANT_22: missing verification/regression-ledger/ledger.json")
        return
    schema = _load_json(schema_path)
    Draft202012Validator.check_schema(schema)
    validator = Draft202012Validator(schema)
    ledger = _load_json(ledger_path)
    try:
        validator.validate(ledger)
    except ValidationError as e:
        errors.append(f"INVARIANT_23: regression ledger schema validation failed: {e.message}")
        return
    records = ledger.get("records") or []
    if not isinstance(records, list) or len(records) < 1:
        errors.append("INVARIANT_23: regression ledger must contain at least one record")


def _check_schedule_in_verify_yml(root: Path, errors: List[str]) -> None:
    wf = root / ".github" / "workflows" / "verify.yml"
    if not wf.is_file():
        errors.append("INVARIANT_22: .github/workflows/verify.yml missing")
        return
    text = wf.read_text(encoding="utf-8")
    if "schedule:" not in text and "schedule :" not in text:
        errors.append("INVARIANT_22: verify.yml must declare a schedule: block for remote cadence")
        return
    if "cron:" not in text:
        errors.append("INVARIANT_22: verify.yml schedule must include cron:")


def _check_policy_and_review(root: Path, errors: List[str]) -> None:
    pol = root / "verification" / "review-escalation-policy.json"
    if not pol.is_file():
        errors.append("missing verification/review-escalation-policy.json")
        return
    data = _load_json(pol)
    if not data.get("scheduled_consecutive_failure_threshold"):
        errors.append("review-escalation-policy: scheduled_consecutive_failure_threshold required")
    rev_path = root / "verification" / "independent-review" / "last-review.json"
    if not rev_path.is_file():
        errors.append("INVARIANT_27: verification/independent-review/last-review.json missing")
        return
    rev = _load_json(rev_path)
    for k in ("schema_version", "outcome", "last_review_at_utc"):
        if not str(rev.get(k) or "").strip():
            errors.append(f"INVARIANT_27: independent review missing field {k!r}")


def _check_system_card(root: Path, errors: List[str]) -> None:
    p = root / "verification" / "GOVERNANCE_SYSTEM_CARD.md"
    if not p.is_file():
        errors.append("INVARIANT_28: missing verification/GOVERNANCE_SYSTEM_CARD.md")
        return
    text = p.read_text(encoding="utf-8")
    for needle in (
        "Purpose:",
        "Escalation thresholds",
        "Separation of Powers",
        "Not claimed:",
        "evidence boundary",
    ):
        if needle not in text:
            errors.append(f"INVARIANT_28: GOVERNANCE_SYSTEM_CARD.md must mention {needle!r}")


def _check_ci_provenance_escalation(root: Path, errors: List[str]) -> None:
    inv_path = root / "MASTER_PROJECT_INVENTORY.json"
    data = _load_json(inv_path)
    cp = data.get("ci_provenance")
    if not isinstance(cp, dict):
        errors.append("INVARIANT_24: ci_provenance object required")
        return
    st = str(cp.get("status") or "").strip()
    allowed = ("verified", "pending", "blocked", "critical")
    if st not in allowed:
        errors.append(f"INVARIANT_24: ci_provenance.status must be one of {allowed} (got {st!r})")
    wh = _workflow_sha256(root)
    inv_h = str(cp.get("verify_workflow_sha256") or "").strip()
    if wh and inv_h and inv_h != wh:
        if st == "verified":
            errors.append(
                "INVARIANT_25: workflow hash drift — ci_provenance.verify_workflow_sha256 != "
                f"current verify.yml; status cannot be verified (got {st!r})"
            )
    rec_path = root / "verification" / "ci-remote-evidence" / "record.json"
    if rec_path.is_file():
        rec = _load_json(rec_path)
        if rec.get("claimed_remote") is True:
            if rec.get("workflow_conclusion") != "success" or rec.get("artifact_upload_succeeded") is not True:
                if st == "verified":
                    errors.append(
                        "INVARIANT_24: provenance failure — remote record inconsistent; "
                        "ci_provenance.status cannot remain verified"
                    )
    esc = str(cp.get("escalation_state") or "none").strip()
    tst = str(cp.get("tip_state_truth") or "").strip()
    rev = str(cp.get("reviewer_status") or "pending").strip()
    if esc == "blocking" and tst != "tip_blocked":
        errors.append(
            "INVARIANT_35: escalation_state blocking requires ci_provenance.tip_state_truth tip_blocked"
        )
    if esc == "critical" and tst != "tip_critical":
        errors.append(
            "INVARIANT_35: escalation_state critical requires ci_provenance.tip_state_truth tip_critical"
        )
    if esc in ("blocking", "critical") and rev not in ("acknowledged", "waived"):
        errors.append(
            "INVARIANT_27: escalation_state is blocking or critical but reviewer_status not acknowledged/waived"
        )


def _check_scheduled_failure_threshold(root: Path, errors: List[str]) -> None:
    pol_path = root / "verification" / "review-escalation-policy.json"
    ledger_path = root / "verification" / "regression-ledger" / "ledger.json"
    if not pol_path.is_file() or not ledger_path.is_file():
        return
    pol = _load_json(pol_path)
    n = int(pol.get("scheduled_consecutive_failure_threshold") or 0)
    if n < 1:
        return
    ledger = _load_json(ledger_path)
    records: List[Dict[str, Any]] = [r for r in (ledger.get("records") or []) if isinstance(r, dict)]
    sched = [r for r in records if str(r.get("github_event_name") or "") == "schedule"]
    failures = 0
    for r in reversed(sched):
        if str(r.get("conclusion") or "") == "failure":
            failures += 1
        else:
            break
    if failures >= n:
        inv = _load_json(root / "MASTER_PROJECT_INVENTORY.json")
        cp = inv.get("ci_provenance") or {}
        esc = str(cp.get("escalation_state") or "none")
        if esc != "blocking":
            errors.append(
                f"INVARIANT_24: {failures} consecutive scheduled failures >= threshold {n}; "
                "ci_provenance.escalation_state must be blocking"
            )


def _parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--root", type=Path, default=None, help="Repo root")
    return p.parse_args()


def main() -> None:
    args = _parse_args()
    script_dir = Path(__file__).resolve().parent
    root = (args.root or script_dir.parent).resolve()

    try:
        assert_not_shallow(root)
    except GovernanceError as e:
        print(f"ERROR: {e.code}: {e}", file=sys.stderr)
        sys.exit(1)

    fe = git_preflight_fetch_tags_or_error(root)
    if fe:
        print(f"ERROR: INVARIANT_53: {fe}", file=sys.stderr)
        sys.exit(1)

    errors: List[str] = []
    _check_schedule_in_verify_yml(root, errors)
    _validate_ledger(root, errors)
    _check_policy_and_review(root, errors)
    _check_system_card(root, errors)
    _check_ci_provenance_escalation(root, errors)
    _check_scheduled_failure_threshold(root, errors)
    if errors:
        print("ERROR: institutionalization verification failed:", file=sys.stderr)
        for e in errors:
            print(f"  {e}", file=sys.stderr)
        sys.exit(1)
    print("OK: institutionalization verification passed")
    sys.exit(0)


if __name__ == "__main__":
    main()
