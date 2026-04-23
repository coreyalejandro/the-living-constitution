#!/usr/bin/env python3
"""Regression harness for Guardian strict-semgraph enforcement.

Exercises five scenarios against the three (now four) fixtures under
`verification/semgraph/fixtures/`:

  1. valid                       + strict                    -> PASS, auto_generated=false
  2. invalid-evidence            + strict                    -> FAIL (explicit invalid evidence path)
  3. missing-evidence            + strict + autogen_disabled -> FAIL (hard guard)
  4. missing-evidence            + strict + autogen_enabled  -> PASS, auto_generated=true
  5. autogen-python              + strict + autogen_enabled  -> PASS, auto_generated=true

Exit code 0 iff every scenario matches expectations.
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
GUARDIAN = REPO_ROOT / "src" / "guardian.py"
FIXTURES = REPO_ROOT / "verification" / "semgraph" / "fixtures"


def run_guardian(fixture: str, *, strict: bool, autogen_disabled: bool) -> dict:
    cmd = [sys.executable, str(GUARDIAN), "--evaluate", str(FIXTURES / fixture), "-v"]
    if strict:
        cmd.append("--strict-semgraph")
    env = os.environ.copy()
    env["PYTHONUNBUFFERED"] = "1"
    if autogen_disabled:
        env["TLC_GUARDIAN_AUTOGEN_DISABLED"] = "1"
    else:
        env.pop("TLC_GUARDIAN_AUTOGEN_DISABLED", None)

    proc = subprocess.run(cmd, capture_output=True, text=True, env=env, cwd=str(REPO_ROOT))
    stdout = proc.stdout.strip().splitlines()
    if not stdout:
        return {
            "_return_code": proc.returncode,
            "_stderr": proc.stderr,
            "_error": "no stdout",
        }
    body = "\n".join(stdout[:-1])
    last = stdout[-1]
    try:
        verdict = json.loads(body)
    except json.JSONDecodeError:
        verdict = {}
    verdict["_final_line"] = last
    verdict["_return_code"] = proc.returncode
    verdict["_stderr"] = proc.stderr
    return verdict


def assert_equal(label: str, actual, expected) -> list[str]:
    if actual != expected:
        return [f"{label}: expected {expected!r} got {actual!r}"]
    return []


def scenario(
    name: str,
    fixture: str,
    *,
    strict: bool,
    autogen_disabled: bool,
    expect_decision: str,
    expect_auto_generated: bool,
    expect_semgraph_status: str,
) -> list[str]:
    v = run_guardian(fixture, strict=strict, autogen_disabled=autogen_disabled)
    errs: list[str] = []
    errs += assert_equal(f"{name}.decision", v.get("decision"), expect_decision)
    errs += assert_equal(
        f"{name}.semgraph_auto_generated",
        v.get("semgraph_auto_generated"),
        expect_auto_generated,
    )
    errs += assert_equal(
        f"{name}.semgraph.status",
        (v.get("semgraph") or {}).get("status"),
        expect_semgraph_status,
    )
    return errs


def main() -> int:
    all_errors: list[str] = []
    all_errors += scenario(
        "valid+strict",
        "toolcall-valid.json",
        strict=True,
        autogen_disabled=False,
        expect_decision="PASS",
        expect_auto_generated=False,
        expect_semgraph_status="PASS",
    )
    all_errors += scenario(
        "invalid+strict",
        "toolcall-invalid-evidence.json",
        strict=True,
        autogen_disabled=False,
        expect_decision="FAIL",
        expect_auto_generated=False,
        expect_semgraph_status="FAIL",
    )
    all_errors += scenario(
        "missing+strict+autogen_off",
        "toolcall-missing-evidence.json",
        strict=True,
        autogen_disabled=True,
        expect_decision="FAIL",
        expect_auto_generated=False,
        expect_semgraph_status="MISSING",
    )
    all_errors += scenario(
        "missing+strict+autogen_on",
        "toolcall-missing-evidence.json",
        strict=True,
        autogen_disabled=False,
        expect_decision="PASS",
        expect_auto_generated=True,
        expect_semgraph_status="PASS",
    )
    all_errors += scenario(
        "autogen_python+strict",
        "toolcall-autogen-python.json",
        strict=True,
        autogen_disabled=False,
        expect_decision="PASS",
        expect_auto_generated=True,
        expect_semgraph_status="PASS",
    )

    if all_errors:
        print("GUARDIAN STRICT-SEMGRAPH REGRESSION: FAIL", file=sys.stderr)
        for err in all_errors:
            print(f"  - {err}", file=sys.stderr)
        return 1

    print("GUARDIAN STRICT-SEMGRAPH REGRESSION: PASS (5/5 scenarios)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
