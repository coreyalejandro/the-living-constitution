#!/usr/bin/env python3
"""
EXPECTED-FAILURE harness for governance verification (adversarial cases).

Each case copies the repo workspace to a temp directory, mutates one condition,
and asserts the relevant verifier exits non-zero.

Run: python3 scripts/governance_failure_injection_tests.py

Exit: 0 all cases behaved as expected, 1 otherwise
"""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Callable, List, Tuple

ROOT = Path(__file__).resolve().parent.parent


def _run_py(args: List[str], cwd: Path, extra_env: dict | None = None) -> int:
    env = os.environ.copy()
    if extra_env:
        env.update(extra_env)
    r = subprocess.run(
        [sys.executable] + args,
        cwd=str(cwd),
        capture_output=True,
        text=True,
        env=env,
    )
    return r.returncode


def _clone_workspace(dst: Path) -> None:
    if dst.exists():
        shutil.rmtree(dst)
    shutil.copytree(
        ROOT,
        dst,
        ignore=shutil.ignore_patterns(
            ".git",
            "__pycache__",
            ".venv",
            "node_modules",
            ".claude",
            ".claud *",
        ),
    )


def case_invalid_artifact_schema() -> Tuple[str, Callable[[Path], int]]:
    def _fn(tmp: Path) -> int:
        try:
            from jsonschema import Draft202012Validator
        except ImportError:
            return 1
        bad = {"commit_hash": "short"}
        p = tmp / "verification" / "runs" / "bad-governance.json"
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(json.dumps(bad), encoding="utf-8")
        schema = json.loads((ROOT / "verification" / "governance-verification-run.schema.json").read_text())
        v = Draft202012Validator(schema)
        try:
            v.validate(json.loads(p.read_text()))
            return 1
        except Exception:
            return 0

    return ("invalid governance artifact fails schema validation", _fn)


def case_commit_mismatch_ci_self_verify() -> Tuple[str, Callable[[Path], int]]:
    def _fn(tmp: Path) -> int:
        _clone_workspace(tmp)
        runs = sorted((tmp / "verification" / "runs").glob("*-governance.json"))
        if not runs:
            return 0
        good = json.loads(runs[-1].read_text(encoding="utf-8"))
        good["commit_hash"] = "0" * 40
        art_dir = tmp / "verification" / "_bad"
        art_dir.mkdir(parents=True, exist_ok=True)
        (art_dir / "x-governance.json").write_text(json.dumps(good), encoding="utf-8")
        return 0 if _run_py(
            ["scripts/ci_self_verify_governance_artifact.py"],
            tmp,
            {"GITHUB_ARTIFACT_DIR": "verification/_bad", "GITHUB_SHA": "a" * 40},
        ) != 0 else 1

    return ("ci_self_verify detects commit_hash != GITHUB_SHA", _fn)


def case_missing_artifact_dir() -> Tuple[str, Callable[[Path], int]]:
    def _fn(tmp: Path) -> int:
        _clone_workspace(tmp)
        code = _run_py(
            ["scripts/ci_self_verify_governance_artifact.py"],
            tmp,
            {"GITHUB_ARTIFACT_DIR": "verification/_missing", "GITHUB_SHA": "a" * 40},
        )
        return 0 if code != 0 else 1

    return ("ci_self_verify fails on missing artifact dir", _fn)


def case_broken_doctrine_invariant_link() -> Tuple[str, Callable[[Path], int]]:
    def _fn(tmp: Path) -> int:
        _clone_workspace(tmp)
        doc_path = tmp / "00-constitution" / "doctrine-to-invariant.map.json"
        doc = json.loads(doc_path.read_text(encoding="utf-8"))
        doc["doctrines"][0]["invariant_ids"] = ["INVARIANT_NONEXISTENT"]
        doc_path.write_text(json.dumps(doc, indent=2), encoding="utf-8")
        return 0 if _run_py(["scripts/verify_project_topology.py", "--root", ".", "--with-governance"], tmp) != 0 else 1

    return ("broken doctrine to invariant link fails verify_governance_chain", _fn)


def case_broken_invariant_enforcement_link() -> Tuple[str, Callable[[Path], int]]:
    def _fn(tmp: Path) -> int:
        _clone_workspace(tmp)
        enf_path = tmp / "03-enforcement" / "enforcement-map.json"
        enf = json.loads(enf_path.read_text(encoding="utf-8"))
        for m in enf.get("modules", []):
            if m.get("id") == "tlc_governance_chain":
                m["enforcement_hook"] = "scripts/does_not_exist_ever.py"
        enf_path.write_text(json.dumps(enf, indent=2), encoding="utf-8")
        return 0 if _run_py(["scripts/verify_project_topology.py", "--root", ".", "--with-governance"], tmp) != 0 else 1

    return ("broken enforcement hook path fails verify_governance_chain", _fn)


def case_stale_inventory_provenance_pointer() -> Tuple[str, Callable[[Path], int]]:
    def _fn(tmp: Path) -> int:
        _clone_workspace(tmp)
        inv_path = tmp / "MASTER_PROJECT_INVENTORY.json"
        inv = json.loads(inv_path.read_text(encoding="utf-8"))
        inv["ci_provenance"]["verify_workflow_sha256"] = "deadbeef" * 8
        inv["ci_provenance"]["status"] = "verified"
        inv["ci_provenance"]["tip_state_truth"] = "tip_verified"
        inv_path.write_text(json.dumps(inv, indent=2), encoding="utf-8")
        return 0 if _run_py(["scripts/verify_institutionalization.py", "--root", "."], tmp) != 0 else 1

    return ("stale inventory workflow hash fails verify_institutionalization", _fn)


def case_tip_verified_without_matching_head() -> Tuple[str, Callable[[Path], int]]:
    """Status surface check fails when ci_provenance is mutated without re-render."""
    def _fn(tmp: Path) -> int:
        _clone_workspace(tmp)
        subprocess.run(["git", "-C", str(tmp), "init"], check=True)
        subprocess.run(
            ["git", "-C", str(tmp), "config", "user.email", "tip-state@example.com"],
            check=True,
        )
        subprocess.run(["git", "-C", str(tmp), "config", "user.name", "tip-state"], check=True)
        subprocess.run(["git", "-C", str(tmp), "add", "-A"], check=True)
        subprocess.run(["git", "-C", str(tmp), "commit", "-m", "init", "--allow-empty"], check=True)
        fake = "0" * 40
        rec_path = tmp / "verification" / "ci-remote-evidence" / "record.json"
        rec = json.loads(rec_path.read_text(encoding="utf-8"))
        rec["artifact_commit_hash"] = fake
        rec_path.write_text(json.dumps(rec, indent=2), encoding="utf-8")
        inv_path = tmp / "MASTER_PROJECT_INVENTORY.json"
        inv = json.loads(inv_path.read_text(encoding="utf-8"))
        inv["ci_provenance"]["status"] = "verified"
        inv["ci_provenance"]["tip_state_truth"] = "tip_verified"
        inv["ci_provenance"]["last_verified_commit"] = fake
        inv["ci_provenance"]["last_remote_qualifying_commit"] = fake
        inv_path.write_text(json.dumps(inv, indent=2), encoding="utf-8")
        return 0 if _run_py(["scripts/render_status_surface.py", "--root", ".", "--check"], tmp) != 0 else 1

    return ("ci_provenance tip-verified mutation without re-render fails status surface check", _fn)


def case_stale_status_md_fails_pass10a() -> Tuple[str, Callable[[Path], int]]:
    """INVARIANT_39: STATUS.md must match render(STATUS.json)."""

    def _fn(tmp: Path) -> int:
        _clone_workspace(tmp)
        p = tmp / "STATUS.md"
        if p.is_file():
            p.write_text(p.read_text(encoding="utf-8") + "\n<!-- stale -->\n", encoding="utf-8")
        return 0 if _run_py(["scripts/render_status_surface.py", "--root", ".", "--check"], tmp) != 0 else 1

    return ("stale STATUS.md fails verify_governance_chain (INVARIANT_39)", _fn)


def case_verified_on_mutable_branch_at_anchor_fails_pass7() -> Tuple[str, Callable[[Path], int]]:
    """Status surface check fails when PASS7-like ci_provenance values are injected without re-render."""

    def _fn(tmp: Path) -> int:
        _clone_workspace(tmp)
        subprocess.run(["git", "-C", str(tmp), "init"], check=True)
        subprocess.run(
            ["git", "-C", str(tmp), "config", "user.email", "pass7@example.com"],
            check=True,
        )
        subprocess.run(["git", "-C", str(tmp), "config", "user.name", "pass7"], check=True)
        subprocess.run(["git", "-C", str(tmp), "add", "-A"], check=True)
        subprocess.run(["git", "-C", str(tmp), "commit", "-m", "init", "--allow-empty"], check=True)
        r = subprocess.run(
            ["git", "-C", str(tmp), "rev-parse", "HEAD"],
            capture_output=True,
            text=True,
            check=True,
        )
        sha = (r.stdout or "").strip()
        rec_path = tmp / "verification" / "ci-remote-evidence" / "record.json"
        rec = json.loads(rec_path.read_text(encoding="utf-8"))
        rec["artifact_commit_hash"] = sha
        rec_path.write_text(json.dumps(rec, indent=2), encoding="utf-8")
        inv_path = tmp / "MASTER_PROJECT_INVENTORY.json"
        inv = json.loads(inv_path.read_text(encoding="utf-8"))
        inv["ci_provenance"]["status"] = "verified"
        inv["ci_provenance"]["tip_state_truth"] = "tip_verified"
        inv["ci_provenance"]["last_verified_commit"] = sha
        inv["ci_provenance"]["last_remote_qualifying_commit"] = sha
        inv_path.write_text(json.dumps(inv, indent=2), encoding="utf-8")
        return 0 if _run_py(["scripts/render_status_surface.py", "--root", ".", "--check"], tmp) != 0 else 1

    return ("PASS7-style verified mutation without re-render fails status surface check", _fn)


def case_tlc_governance_v2_verifier_passes_clean_spec() -> Tuple[str, Callable[[Path], int]]:
    """New governance-v2 verifier should pass against unmodified canonical refactor spec."""

    def _fn(tmp: Path) -> int:
        _clone_workspace(tmp)
        code = _run_py(["scripts/verify_tlc_governance_v2.py", "--root", "."], tmp)
        return 0 if code == 0 else 1

    return ("tlc governance v2 verifier passes on clean spec", _fn)


def case_tlc_governance_v2_weight_corruption_fails() -> Tuple[str, Callable[[Path], int]]:
    """Corrupting dimension weights should fail deterministic governance-v2 verification."""

    def _fn(tmp: Path) -> int:
        _clone_workspace(tmp)
        spec_path = tmp / "governance" / "tlc-governance-v2.refactor.json"
        spec = json.loads(spec_path.read_text(encoding="utf-8"))
        dims = spec["intent_monitor"]["dimensions"]
        # Deliberately break the invariant that weights sum to 1.0.
        dims["safety"]["weight"] = 0.5
        dims["scope"]["weight"] = 0.3
        dims["ethics"]["weight"] = 0.2
        dims["transparency"]["weight"] = 0.2
        spec_path.write_text(json.dumps(spec, indent=2), encoding="utf-8")
        code = _run_py(["scripts/verify_tlc_governance_v2.py", "--root", "."], tmp)
        return 0 if code != 0 else 1

    return ("tlc governance v2 verifier fails on corrupted dimension weights", _fn)


def case_tlc_governance_v2_missing_gap_fails() -> Tuple[str, Callable[[Path], int]]:
    """Removing one required GAP card ID should fail governance-v2 verification."""

    def _fn(tmp: Path) -> int:
        _clone_workspace(tmp)
        spec_path = tmp / "governance" / "tlc-governance-v2.refactor.json"
        spec = json.loads(spec_path.read_text(encoding="utf-8"))
        gaps = [g for g in spec.get("gap_cards", []) if g.get("id") != "GAP-6"]
        spec["gap_cards"] = gaps
        spec_path.write_text(json.dumps(spec, indent=2), encoding="utf-8")
        code = _run_py(["scripts/verify_tlc_governance_v2.py", "--root", "."], tmp)
        return 0 if code != 0 else 1

    return ("tlc governance v2 verifier fails on missing required gap card", _fn)


def case_scope_claim_verifier_passes_generated_artifact() -> Tuple[str, Callable[[Path], int]]:
    """Generated governance-v2 scope artifact should pass claim verifier."""

    def _fn(tmp: Path) -> int:
        _clone_workspace(tmp)
        generate_code = _run_py(["scripts/generate_governance_v2_scope_evidence.py", "--root", "."], tmp)
        if generate_code != 0:
            return 1
        verify_code = _run_py(["scripts/verify_governance_v2_scope_claim.py", "--root", "."], tmp)
        return 0 if verify_code == 0 else 1

    return ("scope claim verifier passes generated artifact", _fn)


def case_scope_claim_verifier_rejects_all_impl_artifact() -> Tuple[str, Callable[[Path], int]]:
    """Claim verifier must fail if artifact says all six are runtime-implemented."""

    def _fn(tmp: Path) -> int:
        _clone_workspace(tmp)
        art_dir = tmp / "verification" / "runs"
        art_dir.mkdir(parents=True, exist_ok=True)
        artifact_path = art_dir / "99999999T999999Z-governance-v2-scope.json"
        fake_gaps = []
        for gap_id in ("GAP-1", "GAP-2", "GAP-3", "GAP-4", "GAP-5", "GAP-6"):
            fake_gaps.append(
                {
                    "gap_id": gap_id,
                    "runtime_implemented_end_to_end": True,
                    "missing_required_paths": [],
                    "runtime_evidence_payload_valid": True,
                }
            )
        payload = {
            "claim_text": "I am not claiming all six governance gaps are runtime-implemented end-to-end.",
            "claim_supported_by_repo_state": True,
            "all_six_runtime_implemented_end_to_end": True,
            "gaps": fake_gaps,
            "summary": {
                "runtime_implemented_count": 6,
                "not_runtime_implemented_count": 0,
            },
        }
        artifact_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
        verify_code = _run_py(
            ["scripts/verify_governance_v2_scope_claim.py", "--root", ".", "--artifact", str(artifact_path)],
            tmp,
        )
        return 0 if verify_code != 0 else 1

    return ("scope claim verifier rejects all-implemented artifact", _fn)


def case_scope_claim_verifier_rejects_wrong_claim_text() -> Tuple[str, Callable[[Path], int]]:
    """Claim verifier must fail if canonical claim text is altered."""

    def _fn(tmp: Path) -> int:
        _clone_workspace(tmp)
        art_dir = tmp / "verification" / "runs"
        art_dir.mkdir(parents=True, exist_ok=True)
        artifact_path = art_dir / "99999999T999998Z-governance-v2-scope.json"
        fake_gaps = []
        for gap_id in ("GAP-1", "GAP-2", "GAP-3", "GAP-4", "GAP-5", "GAP-6"):
            fake_gaps.append(
                {
                    "gap_id": gap_id,
                    "runtime_implemented_end_to_end": False,
                    "missing_required_paths": ["missing/path"],
                    "runtime_evidence_payload_valid": False,
                }
            )
        payload = {
            "claim_text": "I am not claiming all six governance gaps are complete in production.",
            "claim_supported_by_repo_state": True,
            "all_six_runtime_implemented_end_to_end": False,
            "gaps": fake_gaps,
            "summary": {
                "runtime_implemented_count": 0,
                "not_runtime_implemented_count": 6,
            },
        }
        artifact_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
        verify_code = _run_py(
            ["scripts/verify_governance_v2_scope_claim.py", "--root", ".", "--artifact", str(artifact_path)],
            tmp,
        )
        return 0 if verify_code != 0 else 1

    return ("scope claim verifier rejects non-canonical claim text", _fn)


def main() -> None:
    cases: List[Tuple[str, Callable[[Path], int]]] = [
        case_invalid_artifact_schema(),
        case_commit_mismatch_ci_self_verify(),
        case_missing_artifact_dir(),
        case_broken_doctrine_invariant_link(),
        case_broken_invariant_enforcement_link(),
        case_stale_inventory_provenance_pointer(),
        case_stale_status_md_fails_pass10a(),
        case_tip_verified_without_matching_head(),
        case_verified_on_mutable_branch_at_anchor_fails_pass7(),
        case_tlc_governance_v2_verifier_passes_clean_spec(),
        case_tlc_governance_v2_weight_corruption_fails(),
        case_tlc_governance_v2_missing_gap_fails(),
        case_scope_claim_verifier_passes_generated_artifact(),
        case_scope_claim_verifier_rejects_all_impl_artifact(),
        case_scope_claim_verifier_rejects_wrong_claim_text(),
    ]
    failed = 0
    with tempfile.TemporaryDirectory() as td:
        base = Path(td)
        for label, fn in cases:
            case_root = base / f"case_{abs(hash(label)) % 100000}"
            case_root.mkdir(parents=True, exist_ok=True)
            try:
                code = fn(case_root)
            except Exception as e:
                print(f"FAIL: {label} raised {e}", file=sys.stderr)
                failed += 1
                continue
            if code == 0:
                print(f"OK: {label}")
            else:
                print(f"FAIL: {label} (exit {code})", file=sys.stderr)
                failed += 1
    if failed:
        sys.exit(1)
    print("OK: all failure-injection cases behaved as expected")
    sys.exit(0)


if __name__ == "__main__":
    main()
