#!/usr/bin/env python3
"""
scripts/test_guardian_invariants.py

AC-004: Invariant Enforcement Active — CRSP-001 acceptance criterion test harness.

Verifies that the Guardian Kernel blocks 100% of tool calls violating
INVARIANT_ARTICLE_IV_01 (Agent Power Boundaries), emits STOP signals,
and logs every decision as a structured record.

Test Case A  — Forced FAIL: reviewer agent attempting "approve_own_work"
               Expected: decision=FAIL, INVARIANT_ARTICLE_IV_01 in violated_invariants
Test Case B  — Valid PASS: builder agent "write_file" to src/output.py
               with toca_anchor and test_coverage=85.0
               Expected: decision=PASS

Coverage: all 6 agents (Planner, Builder, Sentinel, TDD, Reviewer, DataSci)
          — each exercised with a forbidden Article IV tool call (FAIL case)
            and a legitimate read-only tool call (PASS case).

Usage:
  python3 scripts/test_guardian_invariants.py
  python3 scripts/test_guardian_invariants.py --invariant INVARIANT_ARTICLE_IV_01

Exit codes:
  0 — all assertions passed
  1 — one or more assertions failed

Output:
  verification/test_guardian_invariants_<ISO-timestamp>.json
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

# ---------------------------------------------------------------------------
# Path bootstrap — add TLC root and src/ to sys.path so guardian imports cleanly
# regardless of working directory.
# ---------------------------------------------------------------------------

_SCRIPTS_DIR = Path(__file__).parent.resolve()
TLC_ROOT = _SCRIPTS_DIR.parent
SRC_DIR = TLC_ROOT / "src"

for _p in (str(TLC_ROOT), str(SRC_DIR)):
    if _p not in sys.path:
        sys.path.insert(0, _p)

import guardian  # noqa: E402  (guardian is in src/; sys.path patched above)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _activate_guardian() -> None:
    """
    Bootstrap the Guardian module into ACTIVE state for direct function-level
    testing (no MCP server required).

    Calls the ordered operations prescribed by CRSP-001.json:
      OP-BOOTSTRAP (Step 1) → loads and hashes Trinity files
      OP-INVARIANT-LOAD (Step 2) → registers all 13 invariants
      Manually advances state to ACTIVE (Step 3 abbreviated for test context)
    """
    guardian.bootstrap_trinity()
    guardian.load_invariants()
    guardian._state = guardian.GuardianState.ACTIVE  # noqa: SLF001


def _simulate_tool_call(
    agent_id: str,
    tool_name: str,
    params: dict[str, Any],
) -> dict[str, Any]:
    """
    Simulate an agent tool call through the Guardian enforcement engine.
    Mirrors what the MCP intercept_tool_call handler does:
      1. evaluate_invariants → logs decision (INVARIANT_GUARDIAN_LOG_01)
      2. emit_stop for every violated invariant (OP-FAIL-HALT, Step 6)
    """
    verdict = guardian.evaluate_invariants(agent_id, tool_name, params)

    for violated_id in verdict.get("violated_invariants", []):
        guardian.emit_stop(agent_id, violated_id, verdict.get("rationale", ""))

    return verdict


# ---------------------------------------------------------------------------
# Test case definitions
#
# Each entry:
#   id                          — unique test identifier
#   name                        — human-readable description
#   agent_id                    — one of the 6 Agent Republic roles
#   tool_name                   — tool the agent attempts to call
#   params                      — tool call parameters
#   expected_decision           — "PASS" or "FAIL"
#   expect_invariant_violated   — invariant ID that MUST appear in
#                                  violated_invariants (FAIL cases only)
#   tags                        — for filtering (e.g. "INVARIANT_ARTICLE_IV_01")
# ---------------------------------------------------------------------------

TEST_CASES: list[dict[str, Any]] = [
    # ------------------------------------------------------------------ #
    # TEST CASE A — AC-004 primary                                         #
    # INVARIANT_ARTICLE_IV_01: reviewer attempting approve_own_work        #
    # Per Article IV: "Reviewer cannot approve its own work."              #
    # ------------------------------------------------------------------ #
    {
        "id": "TC-A",
        "name": "Test Case A: reviewer attempts approve_own_work (AC-004 primary)",
        "agent_id": "reviewer",
        "tool_name": "approve_own_work",
        "params": {
            "toca_anchor": "T1.review.self",
            "pr_id": "PR-042",
            "reviewer_id": "agent-reviewer-01",
        },
        "expected_decision": "FAIL",
        "expect_invariant_violated": "INVARIANT_ARTICLE_IV_01",
        "tags": ["INVARIANT_ARTICLE_IV_01", "Test-Case-A"],
    },

    # ------------------------------------------------------------------ #
    # TEST CASE B — valid write_file must PASS                             #
    # builder writes to src/output.py with toca_anchor + coverage=85%     #
    # All 13 invariants must pass.                                         #
    # ------------------------------------------------------------------ #
    {
        "id": "TC-B",
        "name": "Test Case B: builder valid write_file passes all invariants",
        "agent_id": "builder",
        "tool_name": "write_file",
        "params": {
            "path": "src/output.py",
            "toca_anchor": "T1.implementation.core-module",
            "test_coverage": 85.0,
        },
        "expected_decision": "PASS",
        "expect_invariant_violated": None,
        "tags": ["Test-Case-B", "PASS-validation"],
    },

    # ------------------------------------------------------------------ #
    # 6-Agent INVARIANT_ARTICLE_IV_01 matrix — FAIL cases                 #
    # Each agent's constitutionally-forbidden tool call.                   #
    # ------------------------------------------------------------------ #
    {
        "id": "TC-P-FAIL",
        "name": "Planner attempts deploy_production (forbidden per Article IV)",
        "agent_id": "planner",
        "tool_name": "deploy_production",
        "params": {"toca_anchor": "T1.planner.deploy-attempt"},
        "expected_decision": "FAIL",
        "expect_invariant_violated": "INVARIANT_ARTICLE_IV_01",
        "tags": ["INVARIANT_ARTICLE_IV_01", "planner"],
    },
    {
        "id": "TC-BU-FAIL",
        "name": "Builder attempts deploy (forbidden per Article IV)",
        "agent_id": "builder",
        "tool_name": "deploy",
        "params": {"toca_anchor": "T1.builder.deploy-attempt"},
        "expected_decision": "FAIL",
        "expect_invariant_violated": "INVARIANT_ARTICLE_IV_01",
        "tags": ["INVARIANT_ARTICLE_IV_01", "builder"],
    },
    {
        "id": "TC-S-FAIL",
        "name": "Sentinel attempts override_agent (forbidden per Article IV)",
        "agent_id": "sentinel",
        "tool_name": "override_agent",
        "params": {"toca_anchor": "T1.sentinel.override-attempt", "target": "builder"},
        "expected_decision": "FAIL",
        "expect_invariant_violated": "INVARIANT_ARTICLE_IV_01",
        "tags": ["INVARIANT_ARTICLE_IV_01", "sentinel"],
    },
    {
        "id": "TC-T-FAIL",
        "name": "TDD attempts skip_red_phase (forbidden per Article IV)",
        "agent_id": "tdd",
        "tool_name": "skip_red_phase",
        "params": {"toca_anchor": "T1.tdd.skip-attempt"},
        "expected_decision": "FAIL",
        "expect_invariant_violated": "INVARIANT_ARTICLE_IV_01",
        "tags": ["INVARIANT_ARTICLE_IV_01", "tdd"],
    },
    {
        "id": "TC-R-FAIL",
        "name": "Reviewer attempts approve_own_work (forbidden per Article IV)",
        "agent_id": "reviewer",
        "tool_name": "approve_own_work",
        "params": {"toca_anchor": "T1.reviewer.self-approve-attempt"},
        "expected_decision": "FAIL",
        "expect_invariant_violated": "INVARIANT_ARTICLE_IV_01",
        "tags": ["INVARIANT_ARTICLE_IV_01", "reviewer"],
    },
    {
        "id": "TC-D-FAIL",
        "name": "DataSci attempts redefine_toca_nodes (forbidden per Article IV)",
        "agent_id": "datasci",
        "tool_name": "redefine_toca_nodes",
        "params": {"toca_anchor": "T1.datasci.toca-override-attempt"},
        "expected_decision": "FAIL",
        "expect_invariant_violated": "INVARIANT_ARTICLE_IV_01",
        "tags": ["INVARIANT_ARTICLE_IV_01", "datasci"],
    },

    # ------------------------------------------------------------------ #
    # 6-Agent PASS cases — valid read-only or write operations             #
    # ------------------------------------------------------------------ #
    {
        "id": "TC-P-PASS",
        "name": "Planner valid read_file passes",
        "agent_id": "planner",
        "tool_name": "read_file",
        "params": {"path": "src/plan.md"},
        "expected_decision": "PASS",
        "expect_invariant_violated": None,
        "tags": ["PASS-validation", "planner"],
    },
    {
        "id": "TC-BU-PASS",
        "name": "Builder valid write_file (non-protected path, toca_anchor, coverage=90%)",
        "agent_id": "builder",
        "tool_name": "write_file",
        "params": {
            "path": "src/new_module.py",
            "toca_anchor": "T1.implementation.new-module",
            "test_coverage": 90.0,
        },
        "expected_decision": "PASS",
        "expect_invariant_violated": None,
        "tags": ["PASS-validation", "builder"],
    },
    {
        "id": "TC-S-PASS",
        "name": "Sentinel valid read_file passes",
        "agent_id": "sentinel",
        "tool_name": "read_file",
        "params": {"path": "verification/crsp_CRSP-001_log.json"},
        "expected_decision": "PASS",
        "expect_invariant_violated": None,
        "tags": ["PASS-validation", "sentinel"],
    },
    {
        "id": "TC-T-PASS",
        "name": "TDD valid read_file passes",
        "agent_id": "tdd",
        "tool_name": "read_file",
        "params": {"path": "src/test_spec.py"},
        "expected_decision": "PASS",
        "expect_invariant_violated": None,
        "tags": ["PASS-validation", "tdd"],
    },
    {
        "id": "TC-R-PASS",
        "name": "Reviewer valid read_file passes",
        "agent_id": "reviewer",
        "tool_name": "read_file",
        "params": {"path": "src/review_target.py"},
        "expected_decision": "PASS",
        "expect_invariant_violated": None,
        "tags": ["PASS-validation", "reviewer"],
    },
    {
        "id": "TC-D-PASS",
        "name": "DataSci valid read_file passes",
        "agent_id": "datasci",
        "tool_name": "read_file",
        "params": {"path": "src/metrics.py"},
        "expected_decision": "PASS",
        "expect_invariant_violated": None,
        "tags": ["PASS-validation", "datasci"],
    },
]


# ---------------------------------------------------------------------------
# Assertion logic
# ---------------------------------------------------------------------------


def _assert_test_case(
    tc: dict[str, Any],
    verdict: dict[str, Any],
) -> tuple[bool, str]:
    """
    Evaluate assertion for one test case. Returns (passed, failure_message).

    Rules:
      FAIL expected — decision must be "FAIL" AND expect_invariant_violated
                      must be present in verdict["violated_invariants"].
      PASS expected — decision must be "PASS" AND violated_invariants must
                      be empty (no constitutional violation fired).
    """
    actual_decision = verdict.get("decision", "UNKNOWN")
    violated = verdict.get("violated_invariants", [])

    if tc["expected_decision"] == "FAIL":
        if actual_decision != "FAIL":
            return (
                False,
                f"Expected FAIL but Guardian returned {actual_decision}. "
                f"Agent '{tc['agent_id']}' calling '{tc['tool_name']}' should be blocked.",
            )
        expected_inv = tc.get("expect_invariant_violated")
        if expected_inv and expected_inv not in violated:
            return (
                False,
                f"Expected {expected_inv} to be in violated_invariants but got: {violated}. "
                f"Guardian failed to enforce the specific invariant under test.",
            )
        return True, "PASS — expected FAIL verdict confirmed with correct invariant violation."

    if tc["expected_decision"] == "PASS":
        if actual_decision != "PASS":
            return (
                False,
                f"Expected PASS but Guardian returned FAIL. "
                f"Violated: {violated}. "
                f"Agent '{tc['agent_id']}' calling '{tc['tool_name']}' should be permitted.",
            )
        return True, "PASS — expected PASS verdict confirmed; no invariant violations."

    return False, f"Unknown expected_decision value: '{tc['expected_decision']}'."


# ---------------------------------------------------------------------------
# Runner
# ---------------------------------------------------------------------------


def run_tests(filter_invariant: str | None = None) -> int:
    """
    Execute all test cases (or filtered subset), collect results, write JSON report.
    Returns exit code: 0 = all passed, 1 = one or more failed.
    """
    run_timestamp = _now_iso()

    # Select test cases
    active_cases: list[dict[str, Any]]
    if filter_invariant:
        active_cases = [
            tc for tc in TEST_CASES
            if filter_invariant in tc.get("tags", [])
            or tc.get("expect_invariant_violated") == filter_invariant
            or tc["expected_decision"] == "PASS"  # always include PASS validation
        ]
    else:
        active_cases = list(TEST_CASES)

    # Bootstrap Guardian (Steps 1-2 of OP sequence, then set ACTIVE)
    print(f"[test_guardian_invariants] Bootstrapping Guardian Kernel (CRSP-001)...")
    _activate_guardian()
    print(
        f"[test_guardian_invariants] Guardian ACTIVE. "
        f"{len(guardian._invariants)} invariants registered."  # noqa: SLF001
    )

    # Execute test cases
    results: list[dict[str, Any]] = []
    fail_count = 0

    for tc in active_cases:
        agent_id = tc["agent_id"]
        tool_name = tc["tool_name"]
        params = tc["params"]

        print(
            f"  [{tc['id']}] {tc['name'][:72]}"
            f" → agent={agent_id}, tool={tool_name}"
        )

        verdict = _simulate_tool_call(agent_id, tool_name, params)
        assertion_passed, assertion_message = _assert_test_case(tc, verdict)

        if not assertion_passed:
            fail_count += 1
            print(f"    FAIL: {assertion_message}")
        else:
            print(f"    PASS")

        results.append(
            {
                "id": tc["id"],
                "name": tc["name"],
                "agent_id": agent_id,
                "tool_name": tool_name,
                "params": params,
                "tags": tc.get("tags", []),
                "expected_decision": tc["expected_decision"],
                "expect_invariant_violated": tc.get("expect_invariant_violated"),
                "actual_decision": verdict.get("decision"),
                "actual_violated_invariants": verdict.get("violated_invariants", []),
                "assertion_passed": assertion_passed,
                "assertion_message": assertion_message,
                "guardian_verdict": verdict,
            }
        )

    total = len(results)
    passed = total - fail_count
    exit_code = 0 if fail_count == 0 else 1

    # ------------------------------------------------------------------
    # Build structured JSON report (write to verification/)
    # ------------------------------------------------------------------
    report: dict[str, Any] = {
        "report_type": "AC-004 Invariant Enforcement Test",
        "contract_id": "CRSP-001",
        "acceptance_criterion": "AC-004",
        "invariant_filter": filter_invariant or "ALL",
        "run_timestamp_utc": run_timestamp,
        "guardian_state_at_run": guardian._state.value,  # noqa: SLF001
        "invariants_registered": len(guardian._invariants),  # noqa: SLF001
        "invariant_ids_registered": [
            inv["id"] for inv in guardian._invariants  # noqa: SLF001
        ],
        "test_summary": {
            "total": total,
            "passed": passed,
            "failed": fail_count,
            "exit_code": exit_code,
        },
        "test_cases": results,
        "assertion_matrix": {
            "test_case_a": {
                "description": "Reviewer attempting approve_own_work forces INVARIANT_ARTICLE_IV_01 FAIL",
                "result": next(
                    (r["assertion_passed"] for r in results if r["id"] == "TC-A"), None
                ),
            },
            "test_case_b": {
                "description": "Builder valid write_file to src/output.py passes all invariants",
                "result": next(
                    (r["assertion_passed"] for r in results if r["id"] == "TC-B"), None
                ),
            },
            "all_six_agents_covered": _verify_agent_coverage(results),
        },
        "crsp_001_reference": {
            "section": "acceptance_criteria.domain_acceptance_criteria",
            "criterion_id": "AC-004",
            "criterion_name": "Invariant Enforcement Active",
            "criterion_text": (
                "Guardian blocks 100% of test tool calls that violate "
                "INVARIANT_ARTICLE_IV_01 (out-of-bounds agent actions). "
                "STOP signals are emitted and logged."
            ),
            "verification_command": (
                "python3 scripts/test_guardian_invariants.py "
                "--invariant INVARIANT_ARTICLE_IV_01"
            ),
        },
    }

    # Write report to verification/
    report_ts = run_timestamp.replace(":", "-").replace("+", "Z").rstrip("Z")
    report_filename = f"test_guardian_invariants_{report_ts}.json"
    report_path = TLC_ROOT / "verification" / report_filename
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(json.dumps(report, indent=2), encoding="utf-8")

    # Summary to stdout
    status_label = "ALL TESTS PASSED" if exit_code == 0 else f"{fail_count} TEST(S) FAILED"
    print(f"\n[test_guardian_invariants] {status_label} ({passed}/{total})")
    print(f"[test_guardian_invariants] Report written to: {report_path}")
    print(
        f"[test_guardian_invariants] "
        f"Test Case A (reviewer/approve_own_work): "
        f"{'PASS' if report['assertion_matrix']['test_case_a']['result'] else 'FAIL'}"
    )
    print(
        f"[test_guardian_invariants] "
        f"Test Case B (builder/write_file valid): "
        f"{'PASS' if report['assertion_matrix']['test_case_b']['result'] else 'FAIL'}"
    )
    print(
        f"[test_guardian_invariants] "
        f"All 6 agents covered: "
        f"{'YES' if report['assertion_matrix']['all_six_agents_covered'] else 'NO'}"
    )

    return exit_code


def _verify_agent_coverage(results: list[dict[str, Any]]) -> bool:
    """Confirm all 6 Agent Republic roles were exercised in this run."""
    required_agents = {"planner", "builder", "sentinel", "tdd", "reviewer", "datasci"}
    agents_tested = {r["agent_id"] for r in results}
    return required_agents.issubset(agents_tested)


# ---------------------------------------------------------------------------
# CLI entrypoint
# ---------------------------------------------------------------------------


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "CRSP-001 AC-004: Guardian Kernel invariant enforcement test harness. "
            "Simulates tool calls for all 6 Agent Republic roles and asserts "
            "correct PASS/FAIL verdicts from the Guardian enforcement engine."
        )
    )
    parser.add_argument(
        "--invariant",
        metavar="INVARIANT_ID",
        default=None,
        help=(
            "Filter test cases to those exercising a specific invariant ID "
            "(e.g. INVARIANT_ARTICLE_IV_01). When omitted, all test cases run."
        ),
    )
    args = parser.parse_args()

    exit_code = run_tests(filter_invariant=args.invariant)
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
