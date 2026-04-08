#!/usr/bin/env python3
"""
scripts/test_guardian_readonly.py

AC-005: Constitution Files Read-Only — CRSP-001 acceptance criterion test harness.

Verifies that the Guardian Kernel blocks 100% of write attempts to
THE_LIVING_CONSTITUTION.md, CLAUDE.md, and MASTER_PROJECT_INVENTORY.md
without a human cryptographic signature, emits STOP signals with HALT-002
(FAIL_HALT), and logs every decision as a structured record.

Invariants under test:
  INVARIANT_READ_ONLY_01  — Constitution Files Read-Only Without Cryptographic Signature
                            (severity: CRITICAL)

Halt condition exercised:
  HALT-002 — Unauthorized write to constitution file detected (no cryptographic signature)
              halt_state: FAIL_HALT

Scenario A: write_file targeting THE_LIVING_CONSTITUTION.md (no human_crypto_signature)
            Expected: decision=FAIL, INVARIANT_READ_ONLY_01 in violated_invariants,
                      CRITICAL severity confirmed, HALT-002 FAIL_HALT emitted.

Scenario B: write_file targeting CLAUDE.md (no human_crypto_signature)
            Expected: decision=FAIL, INVARIANT_READ_ONLY_01 in violated_invariants,
                      CRITICAL severity confirmed, HALT-002 FAIL_HALT emitted.

Scenario C: write_file targeting MASTER_PROJECT_INVENTORY.md (no human_crypto_signature)
            Expected: decision=FAIL, INVARIANT_READ_ONLY_01 in violated_invariants.

Scenario D (negative control): write_file to non-protected path with toca_anchor
            Expected: decision=PASS — confirms no false-positive on clean calls.

Constraint: Direct import of guardian module (Blind Man's harness — no MCP server).
            Same harness approach as scripts/test_guardian_invariants.py (AC-004).

Usage:
  python3 scripts/test_guardian_readonly.py

Exit codes:
  0 — all assertions passed
  1 — one or more assertions failed

Output:
  verification/test_guardian_readonly_<ISO-timestamp>.json
"""

from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

# ---------------------------------------------------------------------------
# Path bootstrap — add TLC root and src/ to sys.path so guardian imports cleanly
# regardless of working directory. Mirrors AC-004 harness exactly.
# ---------------------------------------------------------------------------

_SCRIPTS_DIR = Path(__file__).parent.resolve()
TLC_ROOT = _SCRIPTS_DIR.parent
SRC_DIR = TLC_ROOT / "src"

for _p in (str(TLC_ROOT), str(SRC_DIR)):
    if _p not in sys.path:
        sys.path.insert(0, _p)

import guardian  # noqa: E402  (guardian is in src/; sys.path patched above)


# ---------------------------------------------------------------------------
# Helpers — mirrors AC-004 harness structure exactly
# ---------------------------------------------------------------------------


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _activate_guardian() -> None:
    """
    Bootstrap the Guardian module into ACTIVE state for direct function-level
    testing (no MCP server required).

    Executes ordered operations from CRSP-001.json:
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
) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    """
    Simulate an agent tool call through the Guardian enforcement engine.

    Mirrors MCP intercept_tool_call handler (AC-004 pattern):
      1. evaluate_invariants → logs decision (INVARIANT_GUARDIAN_LOG_01)
      2. emit_stop for every violated invariant (OP-FAIL-HALT, Step 6 / HALT-002)

    Returns:
      (verdict, stop_signals) — verdict dict + list of STOP signal records emitted
    """
    verdict = guardian.evaluate_invariants(agent_id, tool_name, params)

    stop_signals: list[dict[str, Any]] = []
    for violated_id in verdict.get("violated_invariants", []):
        stop_record = guardian.emit_stop(
            agent_id, violated_id, verdict.get("rationale", "")
        )
        stop_signals.append(stop_record)

    return verdict, stop_signals


# ---------------------------------------------------------------------------
# Test case definitions
#
# Each entry:
#   id                          — unique test identifier
#   name                        — human-readable description
#   agent_id                    — one of the 6 Agent Republic roles
#   tool_name                   — tool the agent attempts to call
#   params                      — tool call parameters (no human_crypto_signature)
#   expected_decision           — "PASS" or "FAIL"
#   expect_invariant_violated   — invariant ID that MUST appear in
#                                  violated_invariants (FAIL cases only)
#   expect_critical_severity    — True if the violated invariant must be CRITICAL
#   expect_halt_state           — expected halt_state in the STOP signal record
#   tags                        — for metadata
# ---------------------------------------------------------------------------

TEST_CASES: list[dict[str, Any]] = [
    # ------------------------------------------------------------------ #
    # SCENARIO A — AC-005 primary                                          #
    # write_file targeting THE_LIVING_CONSTITUTION.md                      #
    # No human_crypto_signature → INVARIANT_READ_ONLY_01 FAIL             #
    # HALT-002 FAIL_HALT must be emitted per CRSP-001.json halt_matrix     #
    # ------------------------------------------------------------------ #
    {
        "id": "TC-A",
        "name": "Scenario A: builder write_file to THE_LIVING_CONSTITUTION.md (no signature)",
        "agent_id": "builder",
        "tool_name": "write_file",
        "params": {
            "path": "THE_LIVING_CONSTITUTION.md",
            "content": "## Unauthorized Amendment\n",
            "toca_anchor": "T1.builder.constitution-write-attempt",
        },
        "expected_decision": "FAIL",
        "expect_invariant_violated": "INVARIANT_READ_ONLY_01",
        "expect_critical_severity": True,
        "expect_halt_state": "FAIL_HALT",
        "expect_stop_signal": True,
        "tags": ["INVARIANT_READ_ONLY_01", "HALT-002", "AC-005", "Scenario-A"],
    },

    # ------------------------------------------------------------------ #
    # SCENARIO B — AC-005 primary                                          #
    # write_file targeting CLAUDE.md                                       #
    # No human_crypto_signature → INVARIANT_READ_ONLY_01 FAIL             #
    # HALT-002 FAIL_HALT must be emitted per CRSP-001.json halt_matrix     #
    # ------------------------------------------------------------------ #
    {
        "id": "TC-B",
        "name": "Scenario B: planner write_file to CLAUDE.md (no signature)",
        "agent_id": "planner",
        "tool_name": "write_file",
        "params": {
            "path": "CLAUDE.md",
            "content": "## Unauthorized Rule Override\n",
            "toca_anchor": "T1.planner.claude-write-attempt",
        },
        "expected_decision": "FAIL",
        "expect_invariant_violated": "INVARIANT_READ_ONLY_01",
        "expect_critical_severity": True,
        "expect_halt_state": "FAIL_HALT",
        "expect_stop_signal": True,
        "tags": ["INVARIANT_READ_ONLY_01", "HALT-002", "AC-005", "Scenario-B"],
    },

    # ------------------------------------------------------------------ #
    # SCENARIO C — third Trinity file (MASTER_PROJECT_INVENTORY.md)        #
    # write_file targeting MASTER_PROJECT_INVENTORY.md                     #
    # No human_crypto_signature → INVARIANT_READ_ONLY_01 FAIL             #
    # ------------------------------------------------------------------ #
    {
        "id": "TC-C",
        "name": "Scenario C: datasci write_file to MASTER_PROJECT_INVENTORY.md (no signature)",
        "agent_id": "datasci",
        "tool_name": "write_file",
        "params": {
            "path": "MASTER_PROJECT_INVENTORY.md",
            "content": "## Unauthorized Project Entry\n",
            "toca_anchor": "T1.datasci.inventory-write-attempt",
        },
        "expected_decision": "FAIL",
        "expect_invariant_violated": "INVARIANT_READ_ONLY_01",
        "expect_critical_severity": True,
        "expect_halt_state": "FAIL_HALT",
        "expect_stop_signal": True,
        "tags": ["INVARIANT_READ_ONLY_01", "HALT-002", "AC-005", "Scenario-C"],
    },

    # ------------------------------------------------------------------ #
    # Variant: edit_file against THE_LIVING_CONSTITUTION.md (no signature) #
    # Verifies all write_tools in the checked set, not just write_file.    #
    # ------------------------------------------------------------------ #
    {
        "id": "TC-A-EDIT",
        "name": "Scenario A variant: sentinel edit_file to THE_LIVING_CONSTITUTION.md (no sig)",
        "agent_id": "sentinel",
        "tool_name": "edit_file",
        "params": {
            "path": "THE_LIVING_CONSTITUTION.md",
            "old_string": "Article I",
            "new_string": "Article I — Modified",
        },
        "expected_decision": "FAIL",
        "expect_invariant_violated": "INVARIANT_READ_ONLY_01",
        "expect_critical_severity": True,
        "expect_halt_state": "FAIL_HALT",
        "expect_stop_signal": True,
        "tags": ["INVARIANT_READ_ONLY_01", "HALT-002", "AC-005", "Scenario-A"],
    },

    # ------------------------------------------------------------------ #
    # Variant: str_replace against CLAUDE.md (no signature)                #
    # ------------------------------------------------------------------ #
    {
        "id": "TC-B-STR",
        "name": "Scenario B variant: reviewer str_replace to CLAUDE.md (no signature)",
        "agent_id": "reviewer",
        "tool_name": "str_replace",
        "params": {
            "path": "CLAUDE.md",
            "old_string": "Rules",
            "new_string": "Overridden Rules",
        },
        "expected_decision": "FAIL",
        "expect_invariant_violated": "INVARIANT_READ_ONLY_01",
        "expect_critical_severity": True,
        "expect_halt_state": "FAIL_HALT",
        "expect_stop_signal": True,
        "tags": ["INVARIANT_READ_ONLY_01", "HALT-002", "AC-005", "Scenario-B"],
    },

    # ------------------------------------------------------------------ #
    # SCENARIO D — negative control (no false positives)                   #
    # write_file to a non-protected path with full valid params            #
    # All invariants must PASS.                                            #
    # ------------------------------------------------------------------ #
    {
        "id": "TC-D",
        "name": "Scenario D: builder valid write_file to non-protected path (PASS control)",
        "agent_id": "builder",
        "tool_name": "write_file",
        "params": {
            "path": "src/new_module.py",
            "content": "# new module\n",
            "toca_anchor": "T1.builder.new-module",
            "test_coverage": 90.0,
        },
        "expected_decision": "PASS",
        "expect_invariant_violated": None,
        "expect_critical_severity": False,
        "expect_halt_state": None,
        "expect_stop_signal": False,
        "tags": ["PASS-control", "AC-005"],
    },
]


# ---------------------------------------------------------------------------
# Assertion logic
# ---------------------------------------------------------------------------


def _assert_test_case(
    tc: dict[str, Any],
    verdict: dict[str, Any],
    stop_signals: list[dict[str, Any]],
) -> tuple[bool, list[str]]:
    """
    Evaluate all assertions for one test case.

    Returns (overall_passed, list_of_failure_messages).
    An empty failure list means all assertions passed.

    Assertions for FAIL cases:
      1. decision == "FAIL"
      2. expect_invariant_violated present in violated_invariants
      3. The failing invariant result has severity == "CRITICAL" (when expected)
      4. At least one STOP signal emitted
      5. STOP signal halt_state == "FAIL_HALT" (HALT-002)

    Assertions for PASS cases:
      1. decision == "PASS"
      2. violated_invariants is empty
      3. No STOP signals emitted
    """
    failures: list[str] = []
    actual_decision = verdict.get("decision", "UNKNOWN")
    violated = verdict.get("violated_invariants", [])
    inv_results: list[dict[str, Any]] = verdict.get("invariant_results", [])

    if tc["expected_decision"] == "FAIL":
        # Assertion 1: decision must be FAIL
        if actual_decision != "FAIL":
            failures.append(
                f"A1 FAIL: Expected decision=FAIL but Guardian returned '{actual_decision}'. "
                f"Agent '{tc['agent_id']}' calling '{tc['tool_name']}' targeting "
                f"'{tc['params'].get('path', '')}' must be blocked."
            )

        # Assertion 2: specific invariant must be violated
        expected_inv = tc.get("expect_invariant_violated")
        if expected_inv and expected_inv not in violated:
            failures.append(
                f"A2 FAIL: Expected {expected_inv} in violated_invariants "
                f"but got: {violated}. Guardian did not enforce the read-only invariant."
            )

        # Assertion 3: violated invariant must carry CRITICAL severity
        if tc.get("expect_critical_severity") and expected_inv:
            inv_entry = next(
                (r for r in inv_results if r.get("invariant_id") == expected_inv),
                None,
            )
            if inv_entry is None:
                failures.append(
                    f"A3 FAIL: No invariant_results entry found for {expected_inv}. "
                    "Cannot confirm CRITICAL severity."
                )
            elif inv_entry.get("result") != "FAIL":
                failures.append(
                    f"A3 FAIL: invariant_results entry for {expected_inv} shows "
                    f"result='{inv_entry.get('result')}' instead of 'FAIL'."
                )
            elif inv_entry.get("severity") != "CRITICAL":
                failures.append(
                    f"A3 FAIL: {expected_inv} severity is '{inv_entry.get('severity')}' "
                    "but must be 'CRITICAL' per CRSP-001.json invariants section."
                )

        # Assertion 4: STOP signal must be emitted
        if tc.get("expect_stop_signal"):
            if not stop_signals:
                failures.append(
                    "A4 FAIL: Expected STOP signal to be emitted (OP-FAIL-HALT / HALT-002) "
                    "but no emit_stop records were returned. Guardian must emit STOP on "
                    "every constitution file write violation."
                )
            else:
                # Assertion 5: STOP signal must specify FAIL_HALT (HALT-002)
                expected_halt = tc.get("expect_halt_state")
                if expected_halt:
                    halt_states = [s.get("halt_state") for s in stop_signals]
                    if expected_halt not in halt_states:
                        failures.append(
                            f"A5 FAIL: Expected halt_state='{expected_halt}' in STOP "
                            f"signal records but got: {halt_states}. "
                            "HALT-002 requires FAIL_HALT per CRSP-001.json halt_matrix."
                        )
                    # Verify the STOP signal has a STOP signal field
                    stop_signal_values = [s.get("signal") for s in stop_signals]
                    if "STOP" not in stop_signal_values:
                        failures.append(
                            f"A5b FAIL: Expected signal='STOP' in emit_stop record "
                            f"but got: {stop_signal_values}."
                        )

    elif tc["expected_decision"] == "PASS":
        # Assertion 1: decision must be PASS
        if actual_decision != "PASS":
            failures.append(
                f"A1 FAIL: Expected decision=PASS but Guardian returned '{actual_decision}'. "
                f"Violated: {violated}. "
                f"Agent '{tc['agent_id']}' calling '{tc['tool_name']}' to "
                f"'{tc['params'].get('path', '')}' should be permitted."
            )

        # Assertion 2: no invariants should be violated
        if violated:
            failures.append(
                f"A2 FAIL: Expected no violated_invariants but got: {violated}. "
                "False positive — Guardian is blocking a legitimate call."
            )

        # Assertion 3: no STOP signals should be emitted
        if stop_signals:
            failures.append(
                f"A3 FAIL: No STOP signals expected but {len(stop_signals)} were emitted. "
                f"STOP signal invariants: {[s.get('invariant_violated') for s in stop_signals]}"
            )

    else:
        failures.append(
            f"Unknown expected_decision value: '{tc['expected_decision']}'."
        )

    return len(failures) == 0, failures


# ---------------------------------------------------------------------------
# Runner
# ---------------------------------------------------------------------------


def run_tests() -> int:
    """
    Execute all AC-005 test cases, collect results, write JSON report.
    Returns exit code: 0 = all passed, 1 = one or more failed.
    """
    run_timestamp = _now_iso()

    # Bootstrap Guardian (Steps 1-2 then ACTIVE) — Blind Man's harness
    print("[test_guardian_readonly] Bootstrapping Guardian Kernel (CRSP-001)...")
    _activate_guardian()
    print(
        f"[test_guardian_readonly] Guardian ACTIVE. "
        f"{len(guardian._invariants)} invariants registered."  # noqa: SLF001
    )

    results: list[dict[str, Any]] = []
    fail_count = 0

    for tc in TEST_CASES:
        agent_id = tc["agent_id"]
        tool_name = tc["tool_name"]
        params = tc["params"]
        target_path = params.get("path", "")

        print(
            f"  [{tc['id']}] {tc['name'][:72]}"
            f"\n          → agent={agent_id}, tool={tool_name}, target={target_path}"
        )

        verdict, stop_signals = _simulate_tool_call(agent_id, tool_name, params)
        assertion_passed, failure_messages = _assert_test_case(tc, verdict, stop_signals)

        if not assertion_passed:
            fail_count += 1
            for msg in failure_messages:
                print(f"    {msg}")
        else:
            status = (
                f"BLOCKED with CRITICAL HALT-002 FAIL_HALT"
                if tc["expected_decision"] == "FAIL"
                else "PERMITTED (no false positive)"
            )
            print(f"    PASS — {status}")

        results.append(
            {
                "id": tc["id"],
                "name": tc["name"],
                "agent_id": agent_id,
                "tool_name": tool_name,
                "target_path": target_path,
                "params": params,
                "tags": tc.get("tags", []),
                "expected_decision": tc["expected_decision"],
                "expect_invariant_violated": tc.get("expect_invariant_violated"),
                "expect_critical_severity": tc.get("expect_critical_severity"),
                "expect_halt_state": tc.get("expect_halt_state"),
                "actual_decision": verdict.get("decision"),
                "actual_violated_invariants": verdict.get("violated_invariants", []),
                "stop_signals_emitted": len(stop_signals),
                "stop_signal_halt_states": [s.get("halt_state") for s in stop_signals],
                "stop_signal_types": [s.get("signal") for s in stop_signals],
                "assertion_passed": assertion_passed,
                "assertion_failures": failure_messages,
                "guardian_verdict": verdict,
            }
        )

    total = len(results)
    passed = total - fail_count
    exit_code = 0 if fail_count == 0 else 1

    # ------------------------------------------------------------------
    # AC-005 primary assertion matrix
    # ------------------------------------------------------------------
    scenario_a_result = next(
        (r["assertion_passed"] for r in results if r["id"] == "TC-A"), None
    )
    scenario_b_result = next(
        (r["assertion_passed"] for r in results if r["id"] == "TC-B"), None
    )
    scenario_c_result = next(
        (r["assertion_passed"] for r in results if r["id"] == "TC-C"), None
    )
    scenario_d_result = next(
        (r["assertion_passed"] for r in results if r["id"] == "TC-D"), None
    )

    # Verify INVARIANT_READ_ONLY_01 blocked 100% of write attempts to all 3 Trinity files
    readonly_fail_cases = [
        r for r in results if "INVARIANT_READ_ONLY_01" in r.get("tags", [])
    ]
    all_readonly_blocked = all(
        r["actual_decision"] == "FAIL"
        and "INVARIANT_READ_ONLY_01" in r["actual_violated_invariants"]
        for r in readonly_fail_cases
    )
    all_readonly_halt_002 = all(
        "FAIL_HALT" in r["stop_signal_halt_states"] for r in readonly_fail_cases
    )

    # ------------------------------------------------------------------
    # Build structured JSON report (written to verification/)
    # ------------------------------------------------------------------
    report: dict[str, Any] = {
        "report_type": "AC-005 Constitution Files Read-Only Test",
        "contract_id": "CRSP-001",
        "acceptance_criterion": "AC-005",
        "ac_005_criterion_text": (
            "Any write attempt to THE_LIVING_CONSTITUTION.md, CLAUDE.md, or "
            "MASTER_PROJECT_INVENTORY.md without cryptographic signature is blocked "
            "with a STOP signal and logged."
        ),
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
        "assertion_matrix": {
            "scenario_a": {
                "description": (
                    "write_file to THE_LIVING_CONSTITUTION.md triggers CRITICAL "
                    "INVARIANT_READ_ONLY_01 FAIL + HALT-002 FAIL_HALT"
                ),
                "result": scenario_a_result,
            },
            "scenario_b": {
                "description": (
                    "write_file to CLAUDE.md triggers CRITICAL "
                    "INVARIANT_READ_ONLY_01 FAIL + HALT-002 FAIL_HALT"
                ),
                "result": scenario_b_result,
            },
            "scenario_c": {
                "description": (
                    "write_file to MASTER_PROJECT_INVENTORY.md triggers CRITICAL "
                    "INVARIANT_READ_ONLY_01 FAIL + HALT-002 FAIL_HALT"
                ),
                "result": scenario_c_result,
            },
            "scenario_d_no_false_positive": {
                "description": (
                    "write_file to non-protected path passes without triggering "
                    "INVARIANT_READ_ONLY_01"
                ),
                "result": scenario_d_result,
            },
            "invariant_read_only_01_blocks_100pct": all_readonly_blocked,
            "halt_002_fail_halt_emitted_100pct": all_readonly_halt_002,
        },
        "test_cases": results,
        "invariant_under_test": {
            "id": "INVARIANT_READ_ONLY_01",
            "name": "Constitution Files Read-Only Without Cryptographic Signature",
            "severity": "CRITICAL",
            "source": "projects/c-rsp/BUILD_CONTRACT.md Directive 3; THE_LIVING_CONSTITUTION.md",
            "halt_matrix_ref": "HALT-002",
            "halt_state": "FAIL_HALT",
        },
        "crsp_001_reference": {
            "section": "acceptance_criteria.domain_acceptance_criteria",
            "criterion_id": "AC-005",
            "criterion_name": "Constitution Files Read-Only",
            "verification_command": "python3 scripts/test_guardian_readonly.py",
        },
    }

    # Write report
    report_ts = run_timestamp.replace(":", "-").replace("+", "Z").rstrip("Z")
    report_filename = f"test_guardian_readonly_{report_ts}.json"
    report_path = TLC_ROOT / "verification" / report_filename
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(json.dumps(report, indent=2), encoding="utf-8")

    # Summary to stdout
    status_label = "ALL TESTS PASSED" if exit_code == 0 else f"{fail_count} TEST(S) FAILED"
    print(f"\n[test_guardian_readonly] {status_label} ({passed}/{total})")
    print(f"[test_guardian_readonly] Report written to: {report_path}")
    print(
        f"[test_guardian_readonly] "
        f"Scenario A (THE_LIVING_CONSTITUTION.md): "
        f"{'PASS' if scenario_a_result else 'FAIL'}"
    )
    print(
        f"[test_guardian_readonly] "
        f"Scenario B (CLAUDE.md): "
        f"{'PASS' if scenario_b_result else 'FAIL'}"
    )
    print(
        f"[test_guardian_readonly] "
        f"INVARIANT_READ_ONLY_01 blocks 100%: "
        f"{'YES' if all_readonly_blocked else 'NO'}"
    )
    print(
        f"[test_guardian_readonly] "
        f"HALT-002 FAIL_HALT emitted 100%: "
        f"{'YES' if all_readonly_halt_002 else 'NO'}"
    )

    return exit_code


# ---------------------------------------------------------------------------
# CLI entrypoint
# ---------------------------------------------------------------------------


def main() -> None:
    exit_code = run_tests()
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
