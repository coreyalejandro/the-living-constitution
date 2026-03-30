#!/usr/bin/env python3
"""
verify_governance_chain.py

Machine-checkable governance chain validation for TLC:
- JSON Schema validation for evidence ledger records (runtime)
- Commit-bound verification artifact under verification/runs/
- Referential closure: doctrine, invariants, enforcement, evidence, inventory
- Inventory manifest vs canonical_paths; MD timestamp sync

Exit codes: 0 OK, 1 validation failure, 2 usage/read/dependency error
"""

from __future__ import annotations

import argparse
import json
import os
import platform
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Set, Tuple

try:
    from jsonschema import Draft202012Validator
    from jsonschema.exceptions import ValidationError
except ImportError:
    print(
        "ERROR: jsonschema is required. Install: pip install -r requirements-verify.txt",
        file=sys.stderr,
    )
    sys.exit(2)

# Parity: must match .github/workflows/verify.yml and MASTER_PROJECT_INVENTORY ci_verification_commands
EXPECTED_CI_COMMAND_LINES = (
    "python3 scripts/verify_project_topology.py --root . --with-governance",
    "python3 scripts/verify_governance_chain.py --root .",
)


def _parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument(
        "--root",
        type=Path,
        default=None,
        help="TLC repository root (default: parent of scripts/)",
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


def _check_ci_parity(root: Path, errors: List[str]) -> None:
    wf = root / ".github" / "workflows" / "verify.yml"
    if not wf.is_file():
        errors.append("INVARIANT_13: missing .github/workflows/verify.yml")
        return
    text = wf.read_text(encoding="utf-8")
    for line in EXPECTED_CI_COMMAND_LINES:
        if line not in text:
            errors.append(
                f"INVARIANT_13: verify.yml must contain exact command line: {line!r}"
            )


def _check_inventory_manifest(
    root: Path,
    data: Dict[str, Any],
    errors: List[str],
    broken: List[str],
) -> None:
    gov = data.get("governance_artifacts") or {}
    canonical = gov.get("canonical_paths") or {}
    manifest = gov.get("artifact_manifest")
    if not isinstance(manifest, list) or not manifest:
        errors.append(
            "governance_artifacts.artifact_manifest must be a non-empty array (inventory integrity)"
        )
        return
    ci_cmds = gov.get("ci_verification_commands")
    if ci_cmds != list(EXPECTED_CI_COMMAND_LINES):
        errors.append(
            "governance_artifacts.ci_verification_commands must match EXPECTED_CI_COMMAND_LINES "
            f"(got {ci_cmds!r})"
        )

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
    expected = {f"INVARIANT_{i:02d}" for i in range(1, 21)}
    if inv_ids != expected:
        inv_fail.append(
            f"invariant-registry must define exactly INVARIANT_01..INVARIANT_20; got {sorted(inv_ids)}"
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
    _check_inventory_manifest(root, data, errors, broken)
    _check_ci_parity(root, errors)
    _check_ci_remote_record(root, errors)

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


def _build_acceptance_results(
    has_fail: bool,
) -> List[Dict[str, Any]]:
    return [
        {"id": "AC-1", "passed": not has_fail, "detail": "Evidence ledger JSON Schema validation"},
        {"id": "AC-2", "passed": not has_fail, "detail": "Commit-bound verification artifact generated"},
        {"id": "AC-3", "passed": not has_fail, "detail": "commit_hash non-empty from git"},
        {"id": "AC-4", "passed": not has_fail, "detail": "Referential governance chain complete"},
        {"id": "AC-5", "passed": not has_fail, "detail": "CI commands match EXPECTED_CI_COMMAND_LINES"},
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
    if gsha and gsha != commit_hash:
        merged.append(
            f"github_actions provenance GITHUB_SHA ({gsha}) != git rev-parse HEAD ({commit_hash})"
        )

    has_fail = len(merged) > 0

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
