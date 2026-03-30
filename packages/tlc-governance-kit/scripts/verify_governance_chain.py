#!/usr/bin/env python3
"""
verify_governance_chain.py

Machine-checkable C-RSP governance chain validation (repo-agnostic layout):
- JSON Schema validation for evidence ledger records (runtime)
- Commit-bound verification artifact under verification/runs/
- Referential closure: doctrine, invariants, enforcement, evidence, inventory
- Inventory manifest vs canonical_paths; MD timestamp sync
- CI parity lines are taken from MASTER_PROJECT_INVENTORY.json
  governance_artifacts.ci_verification_commands (not hardcoded)

Exit codes: 0 OK, 1 validation failure, 2 usage/read/dependency error
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import platform
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Set, Tuple

_SCRIPT_DIR = Path(__file__).resolve().parent
if str(_SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(_SCRIPT_DIR))

from tip_state_helpers import (  # noqa: E402
    is_frozen_verification_context,
    load_pass7_policy,
    load_tip_policy,
    protected_surfaces_changed,
    tip_truth_aligned_with_status,
)

try:
    from jsonschema import Draft202012Validator
    from jsonschema.exceptions import ValidationError
except ImportError:
    print(
        "ERROR: jsonschema is required. Install: pip install -r requirements-verify.txt",
        file=sys.stderr,
    )
    sys.exit(2)

# Fallback when inventory is unreadable (should not happen after required-path checks)
DEFAULT_CI_COMMAND_LINES = (
    "python3 scripts/verify_governance_chain.py --root .",
    "python3 scripts/verify_institutionalization.py --root .",
)


def _parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument(
        "--root",
        type=Path,
        default=None,
        help="Repository root (default: parent of scripts/)",
    )
    return p.parse_args()


def _load_json(path: Path) -> Dict[str, Any]:
    try:
        with path.open("r", encoding="utf-8") as f:
            data = json.load(f)
    except (OSError, json.JSONDecodeError) as e:
        print(f"ERROR: cannot read JSON: {path}: {e}", file=sys.stderr)
        sys.exit(2)
    if not isinstance(data, dict):
        print(f"ERROR: expected object at root: {path}", file=sys.stderr)
        sys.exit(2)
    return data


def _github_actions_provenance() -> Dict[str, Any]:
    """When running in GitHub Actions, embed runner and workflow identity in the run artifact."""
    if os.environ.get("GITHUB_ACTIONS", "").lower() != "true":
        return {}
    return {
        "github_actions": True,
        "workflow": os.environ.get("GITHUB_WORKFLOW", ""),
        "workflow_run_id": os.environ.get("GITHUB_RUN_ID", ""),
        "workflow_run_attempt": os.environ.get("GITHUB_RUN_ATTEMPT", ""),
        "workflow_run_number": os.environ.get("GITHUB_RUN_NUMBER", ""),
        "job": os.environ.get("GITHUB_JOB", ""),
        "repository": os.environ.get("GITHUB_REPOSITORY", ""),
        "ref": os.environ.get("GITHUB_REF", ""),
        "sha": os.environ.get("GITHUB_SHA", ""),
        "github_event_name": os.environ.get("GITHUB_EVENT_NAME", ""),
        "runner_os": os.environ.get("RUNNER_OS", ""),
        "runner_arch": os.environ.get("RUNNER_ARCH", ""),
        "actor": os.environ.get("GITHUB_ACTOR", ""),
    }


def _workflow_sha256(root: Path) -> str:
    p = root / ".github" / "workflows" / "verify.yml"
    if not p.is_file():
        return ""
    return hashlib.sha256(p.read_bytes()).hexdigest()


def _git_head(root: Path) -> str:
    git = shutil.which("git")
    if not git:
        print("ERROR: git executable not found (required for commit-bound artifact).", file=sys.stderr)
        sys.exit(2)
    r = subprocess.run(
        [git, "-C", str(root), "rev-parse", "HEAD"],
        capture_output=True,
        text=True,
        check=False,
    )
    h = (r.stdout or "").strip()
    if r.returncode != 0 or len(h) < 7:
        err = (r.stderr or "").strip()
        print(f"ERROR: git rev-parse HEAD failed: {err}", file=sys.stderr)
        sys.exit(2)
    return h


def _validator_for(schema_path: Path) -> Draft202012Validator:
    schema = _load_json(schema_path)
    Draft202012Validator.check_schema(schema)
    return Draft202012Validator(schema)


def _validate_record(
    validator: Draft202012Validator,
    record: Dict[str, Any],
    ctx: str,
    schema_errors: List[str],
) -> None:
    try:
        validator.validate(record)
    except ValidationError as e:
        schema_errors.append(f"{ctx}: {e.message}")


def _evidence_hook_is_checkable(path_str: str) -> bool:
    s = path_str.strip()
    if not s:
        return False
    low = s.lower()
    if "github actions" in low or "external to repo" in low or s.strip().upper().startswith("N/A"):
        return False
    if s.startswith("http://") or s.startswith("https://"):
        return False
    if "/" not in s:
        return False
    return True


def _check_ci_provenance_inventory(root: Path, data: Dict[str, Any], errors: List[str]) -> None:
    """INVARIANT_21: inventory ci_provenance vs verify.yml hash; verified vs remote record."""
    cp = data.get("ci_provenance")
    if not isinstance(cp, dict):
        errors.append("INVARIANT_21: MASTER_PROJECT_INVENTORY.json must include ci_provenance object")
        return
    wh = _workflow_sha256(root)
    if not wh:
        errors.append("INVARIANT_21: cannot compute .github/workflows/verify.yml sha256")
        return
    inv_h = str(cp.get("verify_workflow_sha256") or "").strip()
    if inv_h != wh:
        errors.append(
            "INVARIANT_21: ci_provenance.verify_workflow_sha256 must equal sha256(.github/workflows/verify.yml) "
            f"(inventory {inv_h!r} vs current {wh!r})"
        )
    st = str(cp.get("status") or "").strip()
    if st not in ("verified", "pending", "blocked", "critical"):
        errors.append(
            f"INVARIANT_21: ci_provenance.status must be verified|pending|blocked|critical (got {st!r})"
        )
        return
    for k in (
        "last_verified_run_id",
        "last_verified_commit",
        "last_remote_qualifying_commit",
        "artifact_name",
        "verify_workflow_sha256",
        "status",
        "tip_state_truth",
    ):
        v = cp.get(k)
        if v is None or (isinstance(v, str) and not str(v).strip()):
            errors.append(f"INVARIANT_21: ci_provenance missing or empty {k!r}")
    if st != "verified":
        return
    rec_path = root / "verification" / "ci-remote-evidence" / "record.json"
    if not rec_path.is_file():
        errors.append("INVARIANT_21: status=verified requires verification/ci-remote-evidence/record.json")
        return
    rec = _load_json(rec_path)
    if str(cp.get("last_verified_run_id")) != str(rec.get("workflow_run_id")):
        errors.append(
            "INVARIANT_21: ci_provenance.last_verified_run_id must match record.json workflow_run_id when status=verified"
        )
    if str(cp.get("last_verified_commit")) != str(rec.get("artifact_commit_hash")):
        errors.append(
            "INVARIANT_21: ci_provenance.last_verified_commit must match record.json artifact_commit_hash when status=verified"
        )
    if str(cp.get("artifact_name")) != str(rec.get("artifact_name")):
        errors.append(
            "INVARIANT_21: ci_provenance.artifact_name must match record.json artifact_name when status=verified"
        )


def _check_tip_state_exactness(root: Path, cp: Dict[str, Any], errors: List[str]) -> None:
    """INVARIANT_30–INVARIANT_36: tip-state truth, HEAD alignment, protected-surface drift."""
    tst = str(cp.get("tip_state_truth") or "").strip()
    if not tst:
        errors.append(
            "INVARIANT_32: ci_provenance.tip_state_truth is required "
            "(tip_verified|tip_pending|tip_blocked|tip_critical)"
        )
        return
    if tst not in ("tip_verified", "tip_pending", "tip_blocked", "tip_critical"):
        errors.append(f"INVARIANT_32: invalid ci_provenance.tip_state_truth {tst!r}")
    st = str(cp.get("status") or "").strip()
    if st and not tip_truth_aligned_with_status(st, tst):
        errors.append(
            f"INVARIANT_32: ci_provenance.status {st!r} must map to tip_state_truth "
            f"(verified→tip_verified, pending→tip_pending, blocked→tip_blocked, critical→tip_critical)"
        )
    lrq = str(cp.get("last_remote_qualifying_commit") or "").strip()
    lvc = str(cp.get("last_verified_commit") or "").strip()
    if not lrq:
        errors.append("INVARIANT_32: ci_provenance.last_remote_qualifying_commit is required")
    elif lvc and lrq != lvc:
        errors.append(
            "INVARIANT_32: last_verified_commit must equal last_remote_qualifying_commit "
            f"({lvc!r} vs {lrq!r})"
        )
    rec_path = root / "verification" / "ci-remote-evidence" / "record.json"
    if rec_path.is_file():
        rec = _load_json(rec_path)
        ach = str(rec.get("artifact_commit_hash") or "").strip()
        if ach and lrq and lrq != ach:
            errors.append(
                "INVARIANT_21: ci_provenance.last_remote_qualifying_commit must match "
                f"record.json artifact_commit_hash ({lrq!r} vs {ach!r})"
            )
    head = _git_head(root)
    p7 = load_pass7_policy(root)
    if st == "verified":
        if tst != "tip_verified":
            errors.append("INVARIANT_30: status=verified requires tip_state_truth=tip_verified")
        if not is_frozen_verification_context(root, lvc, p7):
            errors.append(
                "INVARIANT_37: inventory must not claim verified tip-state on a mutable branch tip; "
                "use pending+tip_pending at development tips. tip_verified is only valid on a frozen "
                "verification target (detached HEAD, provenance/verified-* branch, or tlc-gov-verified-* tag) "
                "with HEAD == last_verified_commit == record artifact_commit_hash "
                "(verification/pass7-branch-verification-policy.json)"
            )
        elif lvc and lvc != head:
            errors.append(
                "INVARIANT_30: status=verified requires git HEAD == ci_provenance.last_verified_commit "
                f"(HEAD={head!r} last_verified_commit={lvc!r})"
            )
        elif lrq and lrq != head:
            errors.append(
                "INVARIANT_30: status=verified requires HEAD == last_remote_qualifying_commit "
                f"(HEAD={head!r} last_remote_qualifying_commit={lrq!r})"
            )
    elif st == "pending":
        if head != lrq and lrq:
            pol = load_tip_policy(root)
            changed, paths = protected_surfaces_changed(root, lrq, "HEAD", pol)
            esc = str(cp.get("escalation_state") or "none").strip()
            if changed and esc == "none":
                errors.append(
                    "INVARIANT_30: protected surfaces changed since last_remote_qualifying_commit "
                    f"({paths[:5]}{'...' if len(paths) > 5 else ''}) but escalation_state is none; "
                    "use review_required or stronger per verification/review-escalation-policy.json"
                )


def _check_ci_remote_record(root: Path, errors: List[str]) -> None:
    """INVARIANT_15–20: optional committed record of remote CI provenance; strict when claimed_remote."""
    p = root / "verification" / "ci-remote-evidence" / "record.json"
    if not p.is_file():
        errors.append("verification/ci-remote-evidence/record.json missing")
        return
    try:
        with p.open("r", encoding="utf-8") as f:
            rec = json.load(f)
    except (OSError, json.JSONDecodeError) as e:
        errors.append(f"ci-remote-evidence/record.json: invalid JSON: {e}")
        return
    if not isinstance(rec, dict):
        errors.append("ci-remote-evidence/record.json: root must be an object")
        return
    if rec.get("claimed_remote") is True:
        if rec.get("workflow_conclusion") != "success":
            errors.append(
                "INVARIANT_16: claimed_remote record requires workflow_conclusion=success "
                f"(got {rec.get('workflow_conclusion')!r})"
            )
        if rec.get("artifact_upload_succeeded") is not True:
            errors.append(
                "INVARIANT_17: claimed_remote record requires artifact_upload_succeeded=true "
                f"(got {rec.get('artifact_upload_succeeded')!r})"
            )
        ach = str(rec.get("artifact_commit_hash") or "").strip()
        if len(ach) < 7:
            errors.append(f"INVARIANT_18: claimed_remote record requires non-empty artifact_commit_hash (got {ach!r})")


def _check_ci_parity(root: Path, errors: List[str], ci_command_lines: Tuple[str, ...]) -> None:
    wf = root / ".github" / "workflows" / "verify.yml"
    if not wf.is_file():
        errors.append("INVARIANT_13: missing .github/workflows/verify.yml")
        return
    text = wf.read_text(encoding="utf-8")
    for line in ci_command_lines:
        if line not in text:
            errors.append(
                f"INVARIANT_13: verify.yml must contain exact command line: {line!r}"
            )


def _check_inventory_manifest(
    root: Path,
    data: Dict[str, Any],
    errors: List[str],
    broken: List[str],
) -> Tuple[str, ...]:
    gov = data.get("governance_artifacts") or {}
    canonical = gov.get("canonical_paths") or {}
    manifest = gov.get("artifact_manifest")
    if not isinstance(manifest, list) or not manifest:
        errors.append(
            "governance_artifacts.artifact_manifest must be a non-empty array (inventory integrity)"
        )
        return DEFAULT_CI_COMMAND_LINES
    ci_cmds = gov.get("ci_verification_commands")
    if not isinstance(ci_cmds, list) or len(ci_cmds) < 1:
        errors.append(
            "governance_artifacts.ci_verification_commands must be a non-empty array "
            "listing exact python command lines required in .github/workflows/verify.yml"
        )
        return DEFAULT_CI_COMMAND_LINES
    if not all(isinstance(x, str) and x.strip() for x in ci_cmds):
        errors.append("governance_artifacts.ci_verification_commands entries must be non-empty strings")
        return DEFAULT_CI_COMMAND_LINES

    for i, row in enumerate(manifest):
        if not isinstance(row, dict):
            errors.append(f"artifact_manifest[{i}]: expected object")
            continue
        ck = row.get("canonical_key")
        rel = row.get("relative_path")
        st = row.get("verification_status")
        eid = row.get("evidence_ledger_record_id")
        if not ck or not rel:
            errors.append(f"artifact_manifest[{i}]: missing canonical_key or relative_path")
            continue
        if ck not in canonical:
            broken.append(f"artifact_manifest key {ck!r} not in canonical_paths")
            continue
        if canonical[ck] != rel:
            broken.append(
                f"artifact_manifest path for {ck!r} ({rel!r}) != canonical_paths ({canonical[ck]!r})"
            )
        p = root / rel
        if not p.is_file():
            errors.append(f"governance artifact manifest path missing on disk: {rel}")
        if st not in ("verified", "unverified", "pending"):
            errors.append(
                f"artifact_manifest[{ck}]: verification_status must be verified|unverified|pending (got {st!r})"
            )
        if eid is not None and not isinstance(eid, str):
            errors.append(f"artifact_manifest[{ck}]: evidence_ledger_record_id must be string or null")

    return tuple(str(x).strip() for x in ci_cmds)


def _collect_errors(root: Path) -> Tuple[
    List[str],
    List[str],
    List[str],
    List[str],
    List[str],
    Set[str],
]:
    """Returns failures, broken_chain, invariant_failures, missing_evidence, schema_err, inv_ok."""
    errors: List[str] = []
    broken: List[str] = []
    inv_fail: List[str] = []
    missing_ev: List[str] = []
    schema_err: List[str] = []
    inv_ok: Set[str] = set()

    required_paths = [
        root / "00-constitution" / "invariant-registry.json",
        root / "00-constitution" / "doctrine-to-invariant.map.json",
        root / "03-enforcement" / "enforcement-map.json",
        root / "02-agents" / "agent-capabilities.json",
        root / "verification" / "evidence-ledger.schema.json",
        root / "verification" / "evidence-ledger" / "seed.json",
        root / "verification" / "governance-verification.template.json",
        root / "verification" / "governance-verification-run.schema.json",
        root / "verification" / "ci-remote-evidence" / "record.json",
        root / "verification" / "regression-ledger.schema.json",
        root / "verification" / "regression-ledger" / "ledger.json",
        root / "verification" / "review-escalation-policy.json",
        root / "verification" / "GOVERNANCE_SYSTEM_CARD.md",
        root / "verification" / "independent-review" / "last-review.json",
        root / "verification" / "pass7-branch-verification-policy.json",
    ]
    for p in required_paths:
        if not p.is_file():
            errors.append(f"missing required file: {p.relative_to(root)}")

    if errors:
        return errors, broken, inv_fail, missing_ev, schema_err, inv_ok

    ev_schema_path = root / "verification" / "evidence-ledger.schema.json"
    run_schema_path = root / "verification" / "governance-verification-run.schema.json"
    try:
        ev_validator = _validator_for(ev_schema_path)
        _validator_for(run_schema_path)
    except Exception as e:
        schema_err.append(f"schema meta-validation failed: {e}")
        return errors, broken, inv_fail, missing_ev, schema_err, inv_ok

    ledger_dir = root / "verification" / "evidence-ledger"
    for jp in sorted(ledger_dir.glob("*.json")):
        data = _load_json(jp)
        records = data.get("records")
        if not isinstance(records, list):
            schema_err.append(f"{jp.relative_to(root)}: top-level records[] required")
            continue
        for j, rec in enumerate(records):
            if not isinstance(rec, dict):
                schema_err.append(f"{jp.relative_to(root)} records[{j}]: expected object")
                continue
            rid = rec.get("record_id", f"idx{j}")
            _validate_record(ev_validator, rec, f"{jp.name}#{rid}", schema_err)

    inv_path = root / "00-constitution" / "invariant-registry.json"
    doctrine_path = root / "00-constitution" / "doctrine-to-invariant.map.json"
    enf_path = root / "03-enforcement" / "enforcement-map.json"
    agents_path = root / "02-agents" / "agent-capabilities.json"
    seed_path = root / "verification" / "evidence-ledger" / "seed.json"
    inventory_path = root / "MASTER_PROJECT_INVENTORY.json"
    inventory_md_path = root / "MASTER_PROJECT_INVENTORY.md"

    reg = _load_json(inv_path)
    inv_rows = reg.get("invariants", [])
    inv_ids = {x["id"] for x in inv_rows if isinstance(x, dict) and "id" in x}
    expected = {f"INVARIANT_{i:02d}" for i in range(1, 38)}
    if inv_ids != expected:
        inv_fail.append(
            f"invariant-registry must define exactly INVARIANT_01..INVARIANT_37; got {sorted(inv_ids)}"
        )

    for row in inv_rows:
        if not isinstance(row, dict):
            continue
        iid = row.get("id")
        for key in ("enforcement_mechanism", "evidence_path_or_rule"):
            if not str(row.get(key, "")).strip():
                inv_fail.append(f"invariant {iid}: missing {key}")

    for fc in reg.get("failure_class_artifacts", []) or []:
        if not isinstance(fc, dict):
            continue
        md_rel = fc.get("markdown")
        if md_rel:
            mp = root / md_rel
            if not mp.is_file():
                inv_fail.append(f"failure class {fc.get('id')}: markdown missing at {md_rel}")

    doctrine = _load_json(doctrine_path)
    for key in ("doctrines", "articles"):
        for item in doctrine.get(key, []) or []:
            if not isinstance(item, dict):
                continue
            ids = list(item.get("invariant_ids") or [])
            if not ids:
                broken.append(f"{key} entry {item.get('id')}: invariant_ids empty")
            for i in ids:
                if i not in inv_ids:
                    broken.append(f"{key} {item.get('id')}: unknown invariant {i}")

    enf = _load_json(enf_path)
    covered: Set[str] = set()
    for mod in enf.get("modules", []) or []:
        if not isinstance(mod, dict):
            continue
        mid = mod.get("id")
        hook = mod.get("enforcement_hook")
        if not hook:
            inv_fail.append(f"enforcement module {mid}: missing enforcement_hook")
            continue
        if hook.endswith(".py") or hook.endswith(".yml") or hook.endswith(".yaml"):
            hp = root / hook
            if not hp.is_file():
                inv_fail.append(f"enforcement hook not found: {hook}")
        evh = mod.get("evidence_hook", "")
        if _evidence_hook_is_checkable(str(evh)):
            ep = root / str(evh)
            if evh.endswith("/"):
                if not ep.is_dir():
                    broken.append(f"module {mid}: evidence_hook dir missing: {evh}")
            else:
                if not ep.is_file() and not ep.is_dir():
                    broken.append(f"module {mid}: evidence_hook path missing: {evh}")
        vm = str(mod.get("verification_method") or mod.get("evidence_hook") or "")
        if not vm.strip():
            broken.append(f"module {mid}: must declare evidence_hook (verification path)")
        for i in mod.get("invariant_ids") or []:
            if isinstance(i, str):
                covered.add(i)

    if expected - covered:
        inv_fail.append(
            "INVARIANT_14: invariants not covered by any enforcement module: "
            f"{sorted(expected - covered)}"
        )

    agents = _load_json(agents_path)
    for ag in agents.get("agents", []) or []:
        if not isinstance(ag, dict):
            continue
        aid = ag.get("id")
        for fld in ("allowed_actions", "forbidden_actions", "required_output_constraints"):
            if not isinstance(ag.get(fld), list) or len(ag.get(fld) or []) == 0:
                inv_fail.append(f"agent {aid}: {fld} must be non-empty list")

    seed = _load_json(seed_path)
    valid_states = {"verified", "unverified", "missing"}
    record_ids: Set[str] = set()
    for rec in seed.get("records", []) or []:
        if not isinstance(rec, dict):
            continue
        rid = rec.get("record_id")
        if isinstance(rid, str):
            record_ids.add(rid)
        st = rec.get("evidence_state")
        if st not in valid_states:
            missing_ev.append(
                f"evidence record {rid}: evidence_state must be one of {valid_states} (got {st!r})"
            )
        for inv in rec.get("related_invariant_ids") or []:
            if inv not in inv_ids:
                broken.append(f"record {rid}: unknown related_invariant_ids {inv}")

    data = _load_json(inventory_path)
    ci_lines = _check_inventory_manifest(root, data, errors, broken)
    _check_ci_parity(root, errors, ci_lines)
    _check_ci_remote_record(root, errors)
    _check_ci_provenance_inventory(root, data, errors)
    cp2 = data.get("ci_provenance")
    if isinstance(cp2, dict):
        _check_tip_state_exactness(root, cp2, errors)

    gov = data.get("governance_artifacts") or {}
    canonical = gov.get("canonical_paths") or {}
    if not canonical:
        errors.append("MASTER_PROJECT_INVENTORY.json: governance_artifacts.canonical_paths missing or empty")
    else:
        paths_seen: Set[str] = set()
        for k, rel in canonical.items():
            if rel in paths_seen:
                errors.append(f"duplicate canonical path for keys in governance_artifacts: {rel}")
            paths_seen.add(rel)
            p = root / rel
            if not p.is_file():
                errors.append(f"governance canonical path missing on disk: {rel}")

    manifest = gov.get("artifact_manifest") or []
    for row in manifest:
        if not isinstance(row, dict):
            continue
        eid = row.get("evidence_ledger_record_id")
        if eid and eid not in record_ids:
            broken.append(
                f"artifact_manifest evidence_ledger_record_id {eid!r} not found in evidence ledger records"
            )

    meta = data.get("meta") or {}
    ts = meta.get("generated_at_utc")
    if not ts:
        errors.append("MASTER_PROJECT_INVENTORY.json: meta.generated_at_utc missing")
    else:
        try:
            md_text = inventory_md_path.read_text(encoding="utf-8")
        except OSError as e:
            print(f"ERROR: cannot read {inventory_md_path}: {e}", file=sys.stderr)
            sys.exit(2)
        if ts not in md_text:
            errors.append(
                "INVARIANT_04: MASTER_PROJECT_INVENTORY.md must contain the same "
                f"meta.generated_at_utc token as JSON: {ts!r}"
            )

    # Invariants that passed checks (for artifact); computed before merging all failure lists
    all_hard = errors + inv_fail + broken + missing_ev + schema_err
    if not all_hard:
        inv_ok = set(inv_ids)

    return errors, broken, inv_fail, missing_ev, schema_err, inv_ok


def _github_actions_post_write_checks(
    runs_dir: Path,
    artifact_path: Path,
    errors: List[str],
) -> None:
    """INVARIANT_21: in CI, run artifact must be present, latest, and bound to this workflow run id."""
    if os.environ.get("GITHUB_ACTIONS", "").lower() != "true":
        return
    json_files = sorted(runs_dir.glob("*.json"), key=lambda p: p.stat().st_mtime)
    if not json_files:
        errors.append(
            "INVARIANT_21: GITHUB_ACTIONS requires at least one verification/runs/*.json after governance write"
        )
        return
    latest = json_files[-1]
    if latest.resolve() != artifact_path.resolve():
        errors.append(
            f"INVARIANT_21: newest verification/runs artifact must be this run ({artifact_path.name}); newest is {latest.name}"
        )
    rid = (os.environ.get("GITHUB_RUN_ID") or "").strip()
    if not rid:
        errors.append("INVARIANT_21: GITHUB_RUN_ID must be non-empty in GitHub Actions for provenance binding")
        return
    try:
        data = _load_json(artifact_path)
    except (OSError, json.JSONDecodeError):
        errors.append("INVARIANT_21: cannot re-read run artifact for run-id check")
        return
    gh = data.get("github_actions_provenance") or {}
    if str(gh.get("workflow_run_id") or "") != rid:
        errors.append(
            "INVARIANT_21: artifact github_actions_provenance.workflow_run_id must match GITHUB_RUN_ID"
        )


def _build_acceptance_results(
    has_fail: bool,
) -> List[Dict[str, Any]]:
    return [
        {"id": "AC-1", "passed": not has_fail, "detail": "Evidence ledger JSON Schema validation"},
        {"id": "AC-2", "passed": not has_fail, "detail": "Commit-bound verification artifact generated"},
        {"id": "AC-3", "passed": not has_fail, "detail": "commit_hash non-empty from git"},
        {"id": "AC-4", "passed": not has_fail, "detail": "Referential governance chain complete"},
        {"id": "AC-5", "passed": not has_fail, "detail": "CI commands match inventory ci_verification_commands"},
        {"id": "AC-6", "passed": not has_fail, "detail": "Inventory manifest + MD timestamp sync"},
        {"id": "AC-7", "passed": not has_fail, "detail": "Failures yield non-zero exit"},
    ]


def main() -> None:
    args = _parse_args()
    script_dir = Path(__file__).resolve().parent
    root = (args.root or script_dir.parent).resolve()

    runs_dir = root / "verification" / "runs"
    runs_dir.mkdir(parents=True, exist_ok=True)

    commit_hash = _git_head(root)
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    fname = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ") + "-governance.json"
    artifact_rel = f"verification/runs/{fname}"
    artifact_path = root / artifact_rel

    errors, broken, inv_fail, missing_ev, schema_err, inv_ok = _collect_errors(root)
    merged = errors + inv_fail + broken + missing_ev + schema_err

    gh_prov = _github_actions_provenance()
    gsha = (gh_prov.get("sha") or "").strip()
    if os.environ.get("GITHUB_ACTIONS", "").lower() == "true":
        if not gsha:
            merged.append("INVARIANT_21: GITHUB_SHA must be non-empty in GitHub Actions")
        elif gsha != commit_hash:
            merged.append(
                f"INVARIANT_21: governance artifact commit_hash must match GITHUB_SHA "
                f"(GITHUB_SHA={gsha!r} git_HEAD={commit_hash!r})"
            )
    elif gsha and gsha != commit_hash:
        merged.append(
            f"github_actions provenance GITHUB_SHA ({gsha}) != git rev-parse HEAD ({commit_hash})"
        )

    has_fail = len(merged) > 0
    wf_sha = _workflow_sha256(root)

    run_payload: Dict[str, Any] = {
        "commit_hash": commit_hash,
        "timestamp": ts,
        "invariants_verified": sorted(inv_ok),
        "acceptance_results": _build_acceptance_results(has_fail),
        "failures": merged,
        "environment": {
            "python": sys.version.split()[0],
            "platform": platform.platform(),
            "cwd": str(root),
        },
        "run_status": "failed" if has_fail else "passed",
        "broken_chain_links": broken,
        "invariant_failures": inv_fail,
        "missing_evidence_explicit": missing_ev,
        "schema_validation_errors": schema_err,
        "artifact_path": artifact_rel,
        "github_actions_provenance": gh_prov,
        "commit_matches_github_sha": (not gsha) or (gsha == commit_hash),
        "verify_workflow_sha256": wf_sha,
    }

    run_schema_path = root / "verification" / "governance-verification-run.schema.json"
    try:
        run_validator = _validator_for(run_schema_path)
        run_validator.validate(run_payload)
    except Exception as e:
        print(f"ERROR: run artifact failed schema validation: {e}", file=sys.stderr)
        run_payload["failures"].append(f"internal: run artifact schema validation: {e}")
        run_payload["run_status"] = "failed"
        has_fail = True

    try:
        with artifact_path.open("w", encoding="utf-8") as f:
            json.dump(run_payload, f, indent=2, sort_keys=False)
            f.write("\n")
    except OSError as e:
        print(f"ERROR: cannot write {artifact_path}: {e}", file=sys.stderr)
        sys.exit(2)

    post: List[str] = []
    _github_actions_post_write_checks(runs_dir, artifact_path, post)
    if post:
        merged.extend(post)
        has_fail = True
        run_payload["failures"] = merged
        run_payload["run_status"] = "failed"
        run_payload["acceptance_results"] = _build_acceptance_results(True)
        try:
            run_validator = _validator_for(run_schema_path)
            run_validator.validate(run_payload)
        except Exception as e:
            print(f"ERROR: run artifact failed schema validation after post-checks: {e}", file=sys.stderr)
            sys.exit(2)
        try:
            with artifact_path.open("w", encoding="utf-8") as f:
                json.dump(run_payload, f, indent=2, sort_keys=False)
                f.write("\n")
        except OSError as e:
            print(f"ERROR: cannot rewrite {artifact_path}: {e}", file=sys.stderr)
            sys.exit(2)

    if has_fail:
        print("ERROR: governance chain validation failed:", file=sys.stderr)
        for cat, label in (
            (errors, "errors"),
            (inv_fail, "invariant_failures"),
            (broken, "broken_chain_links"),
            (missing_ev, "missing_evidence"),
            (schema_err, "schema_validation_errors"),
        ):
            for e in cat:
                print(f"  [{label}] {e}", file=sys.stderr)
        sys.exit(1)

    print("OK: governance chain validation passed")
    print(f"ARTIFACT: {artifact_rel}")
    sys.exit(0)


if __name__ == "__main__":
    main()
