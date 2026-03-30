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
            ".next",
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
        return 0 if _run_py(["scripts/verify_governance_chain.py", "--root", "."], tmp) != 0 else 1

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
        return 0 if _run_py(["scripts/verify_governance_chain.py", "--root", "."], tmp) != 0 else 1

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
        return 0 if _run_py(["scripts/verify_governance_chain.py", "--root", "."], tmp) != 0 else 1

    return ("tip verified without HEAD == last_verified_commit fails verify_governance_chain", _fn)


def case_verified_on_mutable_branch_at_anchor_fails_pass7() -> Tuple[str, Callable[[Path], int]]:
    """INVARIANT_37: status=verified on a symbolic branch is invalid even when HEAD == anchor."""

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
        return 0 if _run_py(["scripts/verify_governance_chain.py", "--root", "."], tmp) != 0 else 1

    return ("PASS7 verified on mutable branch at anchor fails verify_governance_chain", _fn)


def main() -> None:
    cases: List[Tuple[str, Callable[[Path], int]]] = [
        case_invalid_artifact_schema(),
        case_commit_mismatch_ci_self_verify(),
        case_missing_artifact_dir(),
        case_broken_doctrine_invariant_link(),
        case_broken_invariant_enforcement_link(),
        case_stale_inventory_provenance_pointer(),
        case_tip_verified_without_matching_head(),
        case_verified_on_mutable_branch_at_anchor_fails_pass7(),
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
