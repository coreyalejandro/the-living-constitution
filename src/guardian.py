"""
src/guardian.py — Guardian Kernel: MCP Safety Enforcement Server

Contract:   CRSP-001 (Series A)
Authority:  CRSP-001.json → sections.execution_model.ordered_operations
Enforces:   11 constitutional invariants + 2 guardian-specific invariants
            as defined in CRSP-001.json → sections.invariants

Ordered Operations implemented (Section 6):
  OP-BOOTSTRAP       (Step 1) — Trinity Bootstrap
  OP-INVARIANT-LOAD  (Step 2) — Invariant Registry Load
  OP-MCP-INIT        (Step 3) — MCP Server Initialization
  OP-INTERCEPT-LOOP  (Step 4) — Tool Call Interception Loop
  OP-PASS-FORWARD    (Step 5) — PASS: Forward Call
  OP-FAIL-HALT       (Step 6) — FAIL: Emit STOP + Structured Log
  OP-EVIDENCE-FLUSH  (Step 7) — Evidence Flush on session end

Key functions (per CRSP-001.json SNIPPET-001):
  bootstrap_trinity()
  load_invariants()
  evaluate_invariants(agent_id, tool_name, params)
  emit_stop(agent_id, invariant_id, reason)
  log_decision(decision_record)

LEGAL NOTE: Any rule present in CRSP-001.md but absent from CRSP-001.json
is legally void and shall not be enforced by this kernel.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import signal
import sys
import traceback
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path
from typing import Any

from mcp.server.fastmcp import FastMCP

# ---------------------------------------------------------------------------
# Constants — fixed paths, never computed at runtime (INVARIANT_GUARDIAN_SELF_01)
# ---------------------------------------------------------------------------

TLC_ROOT: Path = Path(__file__).parent.parent.resolve()
CONTRACT_ID: str = "CRSP-001"
LOG_PATH: Path = TLC_ROOT / "verification" / "crsp_CRSP-001_log.json"
VERIFICATION_DIR: Path = TLC_ROOT / "verification"

# CRSP-001.json → sections.execution_model.ordered_operations step 1
TRINITY_FILES: list[str] = [
    "THE_LIVING_CONSTITUTION.md",
    "CLAUDE.md",
    "MASTER_PROJECT_INVENTORY.md",
]

# CRSP-001.json → sections.invariants.constitutional_invariants INVARIANT_READ_ONLY_01
CONSTITUTION_READ_ONLY_FILES: list[str] = TRINITY_FILES

# CRSP-001.json → sections.execution_model step 3 — Agent Republic (Article IV)
AGENT_IDS: list[str] = ["planner", "builder", "sentinel", "tdd", "reviewer", "datasci"]


# ---------------------------------------------------------------------------
# Guardian State Machine
# CRSP-001.json → sections.lifecycle_state_machine.guardian_state_machine
# ---------------------------------------------------------------------------


class GuardianState(str, Enum):
    INIT = "INIT"
    TRINITY_LOADING = "TRINITY_LOADING"
    INVARIANT_LOADING = "INVARIANT_LOADING"
    MCP_STARTING = "MCP_STARTING"
    ACTIVE = "ACTIVE"
    SAFE_HALT = "SAFE_HALT"
    FAIL_HALT = "FAIL_HALT"


# Module-level state — deliberately not injectable to prevent runtime tampering
# (INVARIANT_GUARDIAN_SELF_01)
_state: GuardianState = GuardianState.INIT
_trinity_hashes: dict[str, str] = {}
_invariants: list[dict[str, Any]] = []


# ---------------------------------------------------------------------------
# CRSP-001.json → sections.invariants.constitutional_invariants (11 entries)
# + sections.invariants.profile_specific_invariants (2 entries)
# Total: 13 invariants. Constitutional count = 11 per contract.
# ---------------------------------------------------------------------------

CONSTITUTIONAL_INVARIANTS: list[dict[str, Any]] = [
    {
        "id": "INVARIANT_TRINITY_01",
        "name": "Trinity Bootstrap Required",
        "severity": "CRITICAL",
        "source": "projects/c-rsp/BUILD_CONTRACT.md Invariant 0",
        "rule": (
            "No code proposal, architecture decision, or executable enforcement mechanism "
            "may be activated until the three Trinity files have been successfully loaded "
            "and verified."
        ),
        "enforcement_action": "Guardian enters SAFE_HALT if Trinity bootstrap fails",
    },
    {
        "id": "INVARIANT_ARTICLE_I_01",
        "name": "ND Access Filter Mandatory",
        "severity": "CRITICAL",
        "source": "THE_LIVING_CONSTITUTION.md Article I — SentinelOS Bill of Rights",
        "rule": (
            "Every agent output must pass through the Neurodivergent Access Layer filter "
            "before reaching the user. Outputs bypassing this filter are unconstitutional."
        ),
        "enforcement_action": "STOP signal emitted; output blocked until ND filter applied",
    },
    {
        "id": "INVARIANT_ARTICLE_I_02",
        "name": "User Rights: Safety, Accessibility, Dignity, Clarity",
        "severity": "HIGH",
        "source": "THE_LIVING_CONSTITUTION.md Article I",
        "rule": (
            "Every user and agent interaction carries rights to safety, accessibility, "
            "dignity, and clarity. Any interaction that violates these rights is blocked."
        ),
        "enforcement_action": "STOP signal emitted; interaction flagged for human review",
    },
    {
        "id": "INVARIANT_ARTICLE_II_01",
        "name": "All Tool Calls Pre-Validated",
        "severity": "CRITICAL",
        "source": "THE_LIVING_CONSTITUTION.md Article II — Claude Code Governance",
        "rule": (
            "All tool calls from any agent must be validated by the Guardian before "
            "execution. No tool call bypasses this gate."
        ),
        "enforcement_action": (
            "Unvalidated calls are blocked; STOP emitted; structured log written"
        ),
    },
    {
        "id": "INVARIANT_ARTICLE_II_02",
        "name": "Code Quality Gates: Immutability, Test Coverage, Security",
        "severity": "HIGH",
        "source": "THE_LIVING_CONSTITUTION.md Article II",
        "rule": (
            "Code-writing tool calls must pass immutability checks (no direct modification "
            "of constitution files), test coverage requirements (Builder cannot ship <80% "
            "coverage), and security checks."
        ),
        "enforcement_action": (
            "Failing calls blocked; Builder receives structured remediation guidance"
        ),
    },
    {
        "id": "INVARIANT_ARTICLE_III_01",
        "name": "ToC&A Anchor Required",
        "severity": "HIGH",
        "source": "THE_LIVING_CONSTITUTION.md Article III — Data Science Theory of Change",
        "rule": (
            "Every agent action must map to at least one Theory of Change node and have a "
            "measurable outcome. Actions with no ToC&A anchor are blocked."
        ),
        "enforcement_action": (
            "STOP emitted; DataSci agent notified to provide ToC&A mapping"
        ),
    },
    {
        "id": "INVARIANT_ARTICLE_IV_01",
        "name": "Agent Power Boundaries Enforced",
        "severity": "CRITICAL",
        "source": "THE_LIVING_CONSTITUTION.md Article IV — Agent Powers and Limitations",
        "rule": (
            "Each agent operates only within its constitutional bounds. Planner cannot "
            "change architectural decisions without human review. Builder cannot deploy to "
            "production. Sentinel cannot override other agents. TDD cannot skip RED phase. "
            "Reviewer cannot approve its own work. DataSci cannot redefine ToC&A nodes "
            "without review."
        ),
        "enforcement_action": (
            "Out-of-bounds actions blocked; STOP emitted; human review required"
        ),
        "agent_forbidden_tools": {
            "planner": {
                "approve_architectural_change_unilaterally",
                "deploy_production",
                "deploy",
                "push_to_production",
            },
            "builder": {
                "deploy_production",
                "deploy",
                "push_to_production",
                "modify_db_schema",
                "modify_auth_system",
            },
            "sentinel": {
                "override_agent",
                "override_planner",
                "override_builder",
                "override_tdd",
                "override_reviewer",
                "override_datasci",
                "modify_own_rules",
                "self_modify",
            },
            "tdd": {
                "skip_red_phase",
                "ship_without_tests",
                "disable_coverage",
            },
            "reviewer": {
                "approve_own_work",
                "self_approve",
            },
            "datasci": {
                "redefine_toca_nodes",
                "change_success_metrics_unilaterally",
                "override_toca_definition",
            },
        },
    },
    {
        "id": "INVARIANT_ARTICLE_V_01",
        "name": "Amendment Requires Eval Harness",
        "severity": "CRITICAL",
        "source": "THE_LIVING_CONSTITUTION.md Article V — Amendment Process",
        "rule": (
            "No agent may propose or execute a modification to the Living Constitution, "
            "CLAUDE.md, or MASTER_PROJECT_INVENTORY.md without passing through the full "
            "amendment process: Observation → Proposal → Eval Harness Review → Ratification."
        ),
        "enforcement_action": (
            "Unauthorized modification attempt blocked; STOP emitted; "
            "Amendment Process SOP-010 invoked"
        ),
    },
    {
        "id": "INVARIANT_READ_ONLY_01",
        "name": "Constitution Files Read-Only Without Cryptographic Signature",
        "severity": "CRITICAL",
        "source": (
            "projects/c-rsp/BUILD_CONTRACT.md Directive 3; THE_LIVING_CONSTITUTION.md"
        ),
        "rule": (
            "THE_LIVING_CONSTITUTION.md, CLAUDE.md, and MASTER_PROJECT_INVENTORY.md are "
            "read-only to all agents. Any write operation requires a human cryptographic "
            "signature in the commit chain."
        ),
        "enforcement_action": (
            "Write attempt blocked; STOP emitted; human signature requested"
        ),
        "protected_files": CONSTITUTION_READ_ONLY_FILES,
    },
    {
        "id": "INVARIANT_EVIDENCE_01",
        "name": "Evidence Generation Mandatory for Every Step",
        "severity": "HIGH",
        "source": "projects/c-rsp/BUILD_CONTRACT.md Directive 4",
        "rule": (
            "Every Guardian decision (PASS or FAIL) must be logged to verification/ as a "
            "structured JSON record. Silent decisions are forbidden."
        ),
        "enforcement_action": (
            "If log write fails: Guardian enters FAIL_HALT; manual recovery required"
        ),
    },
    {
        "id": "INVARIANT_PAIRED_ARTIFACT_01",
        "name": "Paired Artifact Execution",
        "severity": "HIGH",
        "source": (
            "projects/c-rsp/BUILD_CONTRACT.md Directive 5; "
            ".agents/rules/guardian-kernel.md"
        ),
        "rule": (
            "Every C-RSP instance must produce exactly two files sharing an identical "
            "basename: a JSON law file (authoritative, zero Markdown) and a Markdown "
            "commentary file. Any rule in the Markdown absent from the JSON is legally void."
        ),
        "enforcement_action": (
            "C-RSP instance blocked from Active status until both paired artifacts exist "
            "and are syntactically valid"
        ),
    },
]

GUARDIAN_SPECIFIC_INVARIANTS: list[dict[str, Any]] = [
    {
        "id": "INVARIANT_GUARDIAN_SELF_01",
        "name": "Guardian Cannot Self-Modify at Runtime",
        "severity": "CRITICAL",
        "source": "CRSP-001.json profile_specific_invariants",
        "rule": (
            "src/guardian.py enforcement rules cannot be modified at runtime. "
            "All updates require a new C-RSP instance."
        ),
        "enforcement_action": "Runtime self-modification attempt: FAIL_HALT",
    },
    {
        "id": "INVARIANT_GUARDIAN_LOG_01",
        "name": "Log-Before-Act",
        "severity": "HIGH",
        "source": "CRSP-001.json profile_specific_invariants",
        "rule": (
            "Guardian must write the decision record to verification/ before forwarding "
            "or blocking a tool call. No action without prior evidence generation."
        ),
        "enforcement_action": (
            "If log write fails before action: do not proceed; enter FAIL_HALT"
        ),
    },
]

ALL_INVARIANTS: list[dict[str, Any]] = (
    CONSTITUTIONAL_INVARIANTS + GUARDIAN_SPECIFIC_INVARIANTS
)


# ---------------------------------------------------------------------------
# Utility helpers
# ---------------------------------------------------------------------------


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _sha256(content: str) -> str:
    return hashlib.sha256(content.encode("utf-8")).hexdigest()


# ---------------------------------------------------------------------------
# CTRL-004 / INVARIANT_EVIDENCE_01: Evidence write — log before act
# ---------------------------------------------------------------------------


def _write_log(record: dict[str, Any]) -> None:
    """
    Persist one structured record to verification/crsp_CRSP-001_log.json.
    HALT-004: If write fails, emit emergency stderr record and enter FAIL_HALT.
    """
    global _state
    try:
        VERIFICATION_DIR.mkdir(parents=True, exist_ok=True)
        existing: list[dict] = []
        if LOG_PATH.exists():
            try:
                raw = LOG_PATH.read_text(encoding="utf-8")
                parsed = json.loads(raw) if raw.strip() else []
                # Migrate: pre-existing dict logs get wrapped in a list
                if isinstance(parsed, list):
                    existing = parsed
                elif isinstance(parsed, dict):
                    existing = [parsed]
                else:
                    existing = []
            except (json.JSONDecodeError, OSError):
                existing = []
        existing.append(record)
        LOG_PATH.write_text(json.dumps(existing, indent=2), encoding="utf-8")
    except Exception as exc:
        print(
            f"[GUARDIAN FAIL_HALT] HALT-004: Evidence log write failed: {exc}",
            file=sys.stderr,
        )
        _state = GuardianState.FAIL_HALT
        sys.exit(4)


def log_decision(decision_record: dict[str, Any]) -> None:
    """
    INVARIANT_GUARDIAN_LOG_01: Public surface for writing decision records.
    Must be called BEFORE any forward or block action.
    """
    _write_log(decision_record)


# ---------------------------------------------------------------------------
# OP-BOOTSTRAP (Step 1) — Trinity Bootstrap
# CRSP-001.json halt_condition: "Any Trinity file missing or unreadable"
# ---------------------------------------------------------------------------


def bootstrap_trinity() -> None:
    """
    OP-BOOTSTRAP: Load and verify THE_LIVING_CONSTITUTION.md, CLAUDE.md, and
    MASTER_PROJECT_INVENTORY.md. Compute SHA-256 content hashes and log them.
    SAFE_HALT (HALT-001) if any file is missing or unreadable.

    Success condition: All three files loaded; hashes logged to
    verification/crsp_CRSP-001_log.json (per CRSP-001.json).
    """
    global _state, _trinity_hashes
    _state = GuardianState.TRINITY_LOADING

    hashes: dict[str, str] = {}
    missing: list[str] = []

    for fname in TRINITY_FILES:
        fpath = TLC_ROOT / fname
        if not fpath.exists():
            missing.append(fname)
            continue
        try:
            content = fpath.read_text(encoding="utf-8")
            hashes[fname] = _sha256(content)
        except OSError as exc:
            missing.append(f"{fname} (read error: {exc})")

    record: dict[str, Any] = {
        "event": "OP-BOOTSTRAP",
        "timestamp": _now_iso(),
        "contract_id": CONTRACT_ID,
        "trinity_files_loaded": list(hashes.keys()),
        "trinity_files_missing": missing,
        "hashes": hashes,
    }

    if missing:
        record["trinity_bootstrap"] = {"status": "FAIL", "missing": missing}
        record["halt_state"] = GuardianState.SAFE_HALT.value
        record["halt_id"] = "HALT-001"
        _write_log(record)
        _state = GuardianState.SAFE_HALT
        print(
            f"[GUARDIAN SAFE_HALT] HALT-001: Trinity file(s) missing or unreadable: "
            f"{missing}. Restore from git: git checkout HEAD -- <file>",
            file=sys.stderr,
        )
        sys.exit(1)

    record["trinity_bootstrap"] = {"status": "PASS"}
    _write_log(record)
    _trinity_hashes = hashes


# ---------------------------------------------------------------------------
# OP-INVARIANT-LOAD (Step 2) — Invariant Registry Load
# CRSP-001.json success_condition: "Minimum 7 constitutional invariants registered"
# ---------------------------------------------------------------------------


def load_invariants() -> None:
    """
    OP-INVARIANT-LOAD: Register all invariant definitions embedded above
    (sourced from CRSP-001.json sections.invariants). Supplemental load from
    00-constitution/invariant-registry.json if present.

    SAFE_HALT if fewer than 7 constitutional invariants can be registered.
    """
    global _state, _invariants
    _state = GuardianState.INVARIANT_LOADING

    registered: list[dict[str, Any]] = list(ALL_INVARIANTS)

    # Supplemental load from external registry if present (non-blocking)
    supplemental_path = TLC_ROOT / "00-constitution" / "invariant-registry.json"
    supplemental_loaded: list[str] = []
    if supplemental_path.exists():
        try:
            supplemental = json.loads(supplemental_path.read_text(encoding="utf-8"))
            if isinstance(supplemental, list):
                existing_ids = {inv["id"] for inv in registered}
                for entry in supplemental:
                    if isinstance(entry, dict) and entry.get("id") not in existing_ids:
                        registered.append(entry)
                        supplemental_loaded.append(entry.get("id", "unknown"))
        except (json.JSONDecodeError, OSError) as exc:
            print(
                f"[GUARDIAN WARNING] Could not load supplemental invariant registry: {exc}",
                file=sys.stderr,
            )

    constitutional_count = sum(
        1 for inv in registered if inv["id"] in {i["id"] for i in CONSTITUTIONAL_INVARIANTS}
    )

    record: dict[str, Any] = {
        "event": "OP-INVARIANT-LOAD",
        "timestamp": _now_iso(),
        "contract_id": CONTRACT_ID,
        "invariants_loaded": [inv["id"] for inv in registered],
        "constitutional_count": constitutional_count,
        "total_count": len(registered),
        "supplemental_loaded": supplemental_loaded,
    }

    if constitutional_count < 7:
        record["status"] = "FAIL"
        record["halt_state"] = GuardianState.SAFE_HALT.value
        _write_log(record)
        _state = GuardianState.SAFE_HALT
        print(
            f"[GUARDIAN SAFE_HALT] Invariant registry has fewer than 7 constitutional "
            f"invariants ({constitutional_count}). Cannot enforce constitution.",
            file=sys.stderr,
        )
        sys.exit(2)

    record["status"] = "PASS"
    _write_log(record)
    _invariants = registered


# ---------------------------------------------------------------------------
# Individual invariant checker functions
# Each returns (passed: bool, reason: str)
# ---------------------------------------------------------------------------


def _check_invariant_trinity_01(
    agent_id: str, tool_name: str, params: dict[str, Any]
) -> tuple[bool, str]:
    """INVARIANT_TRINITY_01: Trinity must be loaded before any enforcement gate activates."""
    if not _trinity_hashes:
        return (
            False,
            "Trinity files not loaded. Guardian is in pre-bootstrap state. "
            "OP-BOOTSTRAP must complete before any tool calls are intercepted.",
        )
    return True, f"Trinity bootstrap verified. {len(_trinity_hashes)} file(s) hashed."


def _check_invariant_article_i_01(
    agent_id: str, tool_name: str, params: dict[str, Any]
) -> tuple[bool, str]:
    """INVARIANT_ARTICLE_I_01: ND Access Filter Mandatory for user-facing output tools."""
    output_tools = {
        "respond",
        "emit_output",
        "display",
        "stream_response",
        "send_message",
        "write_response",
        "output_to_user",
    }
    if tool_name.lower() in output_tools:
        if not params.get("nd_filter_applied"):
            return (
                False,
                f"Tool '{tool_name}' produces user-facing output but nd_filter_applied "
                "is not set. Output MUST pass through the Neurodivergent Access Layer "
                "before reaching the user (Article I, INVARIANT_ARTICLE_I_01).",
            )
    return True, "ND Access Filter check passed."


def _check_invariant_article_i_02(
    agent_id: str, tool_name: str, params: dict[str, Any]
) -> tuple[bool, str]:
    """INVARIANT_ARTICLE_I_02: User Rights — Safety, Accessibility, Dignity, Clarity."""
    violations: list[str] = []
    if params.get("bypass_safety"):
        violations.append("bypass_safety=true violates User Right: Safety")
    if params.get("skip_accessibility"):
        violations.append("skip_accessibility=true violates User Right: Accessibility")
    if params.get("suppress_content_warnings"):
        violations.append(
            "suppress_content_warnings=true violates User Right: Safety + Dignity"
        )
    if violations:
        return False, "; ".join(violations)
    return True, "User Rights check passed (safety, accessibility, dignity, clarity)."


def _check_invariant_article_ii_01(
    agent_id: str, tool_name: str, params: dict[str, Any]
) -> tuple[bool, str]:
    """INVARIANT_ARTICLE_II_01: All Tool Calls Pre-Validated — no bypass flag permitted."""
    if params.get("bypass_guardian") or params.get("skip_guardian"):
        return (
            False,
            "Tool call carries bypass_guardian/skip_guardian flag. Direct execution "
            "without Guardian validation is unconstitutional per Article II "
            "(INVARIANT_ARTICLE_II_01).",
        )
    return True, "Pre-validation gate satisfied — call is routing through Guardian."


def _check_invariant_article_ii_02(
    agent_id: str, tool_name: str, params: dict[str, Any]
) -> tuple[bool, str]:
    """INVARIANT_ARTICLE_II_02: Code Quality Gates — immutability, coverage, security."""
    code_write_tools = {
        "write_file",
        "create_file",
        "edit_file",
        "patch_file",
        "str_replace",
        "insert",
        "append_to_file",
        "overwrite_file",
    }
    if tool_name.lower() not in code_write_tools:
        return True, "Not a code-write tool; Article II quality gate not applicable."

    violations: list[str] = []

    # Immutability: block writes to constitution files (overlap with READ_ONLY_01)
    target = str(
        params.get("path", "")
        or params.get("file_path", "")
        or params.get("target", "")
    )
    for protected in CONSTITUTION_READ_ONLY_FILES:
        if protected in target:
            violations.append(
                f"Immutability violation: write attempt to protected file '{protected}'. "
                "See also INVARIANT_READ_ONLY_01."
            )

    # Test coverage gate for Builder agent
    if agent_id.lower() == "builder":
        coverage = params.get("test_coverage")
        if coverage is not None:
            try:
                cov_float = float(coverage)
                if cov_float < 80.0:
                    violations.append(
                        f"Builder test coverage {cov_float:.1f}% is below the 80% "
                        "constitutional minimum. Builder cannot ship below 80% coverage."
                    )
            except (TypeError, ValueError):
                pass

    if violations:
        return False, "; ".join(violations)
    return True, "Code quality gates passed (immutability, coverage, security)."


def _check_invariant_article_iii_01(
    agent_id: str, tool_name: str, params: dict[str, Any]
) -> tuple[bool, str]:
    """
    INVARIANT_ARTICLE_III_01: ToC&A Anchor Required.
    Exempt: read-only/query tools (they produce no agent action or outcome).
    """
    _read_only_prefixes = ("get_", "list_", "read_", "check_", "inspect_", "describe_")
    _read_only_tools = {
        "read_file",
        "list_files",
        "search_files",
        "get_status",
        "health_check",
        "query",
        "inspect",
        "view",
        "describe",
        "explain",
        "summarize",
        "guardian_health_check",
    }
    t_lower = tool_name.lower()
    if t_lower in _read_only_tools or any(
        t_lower.startswith(p) for p in _read_only_prefixes
    ):
        return True, "Read-only/query tool; ToC&A anchor not required."

    if not params.get("toca_anchor"):
        return (
            False,
            f"Agent '{agent_id}' action '{tool_name}' has no Theory of Change & Action "
            "(ToC&A) anchor. Every agent action must map to at least one ToC&A node with "
            "a measurable outcome. Provide toca_anchor in params, or route through "
            "DataSci agent for ToC&A mapping (Article III, INVARIANT_ARTICLE_III_01).",
        )
    return True, f"ToC&A anchor present: '{params['toca_anchor']}'."


def _check_invariant_article_iv_01(
    agent_id: str, tool_name: str, params: dict[str, Any]
) -> tuple[bool, str]:
    """INVARIANT_ARTICLE_IV_01: Agent Power Boundaries — each agent within constitutional scope."""
    inv = next(
        (i for i in CONSTITUTIONAL_INVARIANTS if i["id"] == "INVARIANT_ARTICLE_IV_01"),
        None,
    )
    if inv is None:
        return True, "INVARIANT_ARTICLE_IV_01 definition not found; boundary check skipped."

    agent_forbidden: dict[str, set] = inv.get("agent_forbidden_tools", {})
    forbidden = agent_forbidden.get(agent_id.lower(), set())

    if tool_name.lower() in forbidden:
        return (
            False,
            f"Agent '{agent_id}' attempted '{tool_name}' which exceeds its constitutional "
            "power bounds per Article IV (INVARIANT_ARTICLE_IV_01). "
            "Human review is required before this action can proceed.",
        )

    # Planner-specific: architectural decisions require human_review_approved
    if agent_id.lower() == "planner" and "architect" in tool_name.lower():
        if not params.get("human_review_approved"):
            return (
                False,
                "Planner attempting an architectural decision change without "
                "human_review_approved=true. All Planner architectural decisions require "
                "human review (Article IV, INVARIANT_ARTICLE_IV_01).",
            )

    return True, f"Agent '{agent_id}' power boundary check passed for '{tool_name}'."


def _check_invariant_article_v_01(
    agent_id: str, tool_name: str, params: dict[str, Any]
) -> tuple[bool, str]:
    """INVARIANT_ARTICLE_V_01: Amendment Requires Eval Harness (SOP-010)."""
    constitution_write_tools = {
        "write_file",
        "create_file",
        "edit_file",
        "patch_file",
        "str_replace",
        "insert",
        "append_to_file",
        "overwrite_file",
        "modify_constitution",
        "amend_constitution",
        "update_constitution",
    }
    if tool_name.lower() not in constitution_write_tools:
        return True, "Not a constitution-modification tool; amendment check not applicable."

    target = str(
        params.get("path", "")
        or params.get("file_path", "")
        or params.get("target", "")
    )
    amendment_targets = [
        "THE_LIVING_CONSTITUTION.md",
        "CLAUDE.md",
        "MASTER_PROJECT_INVENTORY.md",
    ]
    for at in amendment_targets:
        if at in target:
            ratified = params.get("amendment_ratified")
            signature = params.get("human_crypto_signature")
            if not ratified or not signature:
                return (
                    False,
                    f"Attempt to modify '{at}' without completing the full Amendment "
                    "Process: Observation → Proposal → Eval Harness Review → Ratification "
                    "with human cryptographic signature. SOP-010 invoked. "
                    "INVARIANT_ARTICLE_V_01 violated.",
                )
    return True, "Amendment gate passed."


def _check_invariant_read_only_01(
    agent_id: str, tool_name: str, params: dict[str, Any]
) -> tuple[bool, str]:
    """INVARIANT_READ_ONLY_01: Constitution files read-only without cryptographic signature."""
    write_tools = {
        "write_file",
        "create_file",
        "edit_file",
        "patch_file",
        "str_replace",
        "insert",
        "append_to_file",
        "overwrite_file",
        "delete_file",
        "move_file",
        "rename_file",
    }
    if tool_name.lower() not in write_tools:
        return True, "Not a write operation; read-only check not applicable."

    target = str(
        params.get("path", "")
        or params.get("file_path", "")
        or params.get("target", "")
    )
    for protected in CONSTITUTION_READ_ONLY_FILES:
        if protected in target:
            if not params.get("human_crypto_signature"):
                return (
                    False,
                    f"Write attempt to protected constitution file '{protected}' without "
                    "a human cryptographic signature. INVARIANT_READ_ONLY_01 violated. "
                    "HALT-002 triggered. git revert the offending operation and obtain "
                    "human signature before retrying.",
                )
    return True, "Read-only constitution file check passed."


def _check_invariant_evidence_01(
    agent_id: str, tool_name: str, params: dict[str, Any]
) -> tuple[bool, str]:
    """
    INVARIANT_EVIDENCE_01: Evidence generation mandatory.
    Structurally enforced by log-before-act in evaluate_invariants.
    This checker verifies the verification/ directory is writable.
    """
    try:
        VERIFICATION_DIR.mkdir(parents=True, exist_ok=True)
    except OSError as exc:
        return (
            False,
            f"Cannot create verification/ directory: {exc}. Evidence generation is "
            "mandatory (INVARIANT_EVIDENCE_01). Guardian cannot proceed.",
        )
    test_path = VERIFICATION_DIR / ".guardian_write_probe"
    try:
        test_path.write_text("probe", encoding="utf-8")
        test_path.unlink()
    except OSError as exc:
        return (
            False,
            f"verification/ directory is not writable: {exc}. "
            "INVARIANT_EVIDENCE_01 violated — entering FAIL_HALT.",
        )
    return True, "Evidence directory writable; mandatory structured logging enforced."


def _check_invariant_paired_artifact_01(
    agent_id: str, tool_name: str, params: dict[str, Any]
) -> tuple[bool, str]:
    """INVARIANT_PAIRED_ARTIFACT_01: C-RSP instances require paired .json + .md artifacts."""
    crsp_promotion_tools = {
        "activate_crsp",
        "promote_crsp",
        "finalize_crsp",
        "advance_crsp_to_active",
    }
    if tool_name.lower() not in crsp_promotion_tools:
        return True, "Not a C-RSP promotion action; paired artifact check not applicable."

    basename = str(params.get("basename", "CRSP-001"))
    json_path = TLC_ROOT / f"{basename}.json"
    md_path = TLC_ROOT / f"{basename}.md"

    missing: list[str] = []
    if not json_path.exists():
        missing.append(f"{basename}.json")
    if not md_path.exists():
        missing.append(f"{basename}.md")

    if missing:
        return (
            False,
            f"Paired artifact check failed: {missing} not found at TLC root. "
            f"Both {basename}.json (The Law) and {basename}.md (The Commentary) "
            "must exist before a C-RSP instance can be promoted to Active status.",
        )
    return (
        True,
        f"Paired artifacts {basename}.json and {basename}.md both exist at TLC root.",
    )


def _check_invariant_guardian_self_01(
    agent_id: str, tool_name: str, params: dict[str, Any]
) -> tuple[bool, str]:
    """INVARIANT_GUARDIAN_SELF_01: Guardian cannot self-modify enforcement rules at runtime."""
    self_modify_tools = {
        "modify_guardian",
        "patch_guardian",
        "update_guardian_rules",
        "reload_guardian",
    }
    guardian_source = os.path.join("src", "guardian.py")
    target = str(
        params.get("path", "")
        or params.get("file_path", "")
        or params.get("target", "")
    )

    is_self_modify_tool = tool_name.lower() in self_modify_tools
    is_guardian_file_write = guardian_source in target and tool_name.lower() in {
        "write_file",
        "edit_file",
        "str_replace",
        "patch_file",
        "overwrite_file",
    }

    if is_self_modify_tool or is_guardian_file_write:
        has_crsp = bool(params.get("crsp_instance_id"))
        has_sig = bool(params.get("human_crypto_signature"))
        if not (has_crsp and has_sig):
            return (
                False,
                "Attempt to modify Guardian enforcement rules at runtime without "
                "a new C-RSP instance ID and human cryptographic signature. "
                "INVARIANT_GUARDIAN_SELF_01 violated. FAIL_HALT triggered. "
                "All rule updates require a new C-RSP instance.",
            )
    return True, "Guardian self-modification check passed."


def _check_invariant_guardian_log_01(
    agent_id: str, tool_name: str, params: dict[str, Any]
) -> tuple[bool, str]:
    """
    INVARIANT_GUARDIAN_LOG_01: Log-Before-Act.
    Enforced structurally by evaluate_invariants (calls log_decision before returning).
    This checker verifies the log path is accessible.
    """
    try:
        VERIFICATION_DIR.mkdir(parents=True, exist_ok=True)
        return (
            True,
            "Log-Before-Act is structurally enforced — log_decision() is called "
            "before evaluate_invariants() returns its verdict.",
        )
    except OSError as exc:
        return (
            False,
            f"Cannot ensure verification/ exists: {exc}. "
            "Log-Before-Act invariant cannot be satisfied. FAIL_HALT.",
        )


# ---------------------------------------------------------------------------
# Invariant checker dispatch table — keyed by invariant ID from CRSP-001.json
# ---------------------------------------------------------------------------

_INVARIANT_CHECKERS: dict[
    str, Any  # Callable[[str, str, dict], tuple[bool, str]]
] = {
    "INVARIANT_TRINITY_01": _check_invariant_trinity_01,
    "INVARIANT_ARTICLE_I_01": _check_invariant_article_i_01,
    "INVARIANT_ARTICLE_I_02": _check_invariant_article_i_02,
    "INVARIANT_ARTICLE_II_01": _check_invariant_article_ii_01,
    "INVARIANT_ARTICLE_II_02": _check_invariant_article_ii_02,
    "INVARIANT_ARTICLE_III_01": _check_invariant_article_iii_01,
    "INVARIANT_ARTICLE_IV_01": _check_invariant_article_iv_01,
    "INVARIANT_ARTICLE_V_01": _check_invariant_article_v_01,
    "INVARIANT_READ_ONLY_01": _check_invariant_read_only_01,
    "INVARIANT_EVIDENCE_01": _check_invariant_evidence_01,
    "INVARIANT_PAIRED_ARTIFACT_01": _check_invariant_paired_artifact_01,
    "INVARIANT_GUARDIAN_SELF_01": _check_invariant_guardian_self_01,
    "INVARIANT_GUARDIAN_LOG_01": _check_invariant_guardian_log_01,
}


# ---------------------------------------------------------------------------
# OP-INTERCEPT-LOOP (Step 4) + OP-PASS-FORWARD (Step 5) + OP-FAIL-HALT (Step 6)
# ---------------------------------------------------------------------------


def evaluate_invariants(
    agent_id: str, tool_name: str, params: dict[str, Any]
) -> dict[str, Any]:
    """
    OP-INTERCEPT-LOOP: Evaluate all registered invariants sequentially for a
    given agent tool call.

    CONFLICT-003 resolution: most restrictive invariant wins — a single FAIL
    blocks the call regardless of other PASS results.

    INVARIANT_GUARDIAN_LOG_01: decision record is written to verification/ BEFORE
    this function returns the verdict to the caller.

    Returns a verdict dict containing:
      decision            — "PASS" or "FAIL"
      agent_id            — originating agent
      tool_name           — intercepted tool
      invariants_evaluated — list of invariant IDs checked
      invariant_results   — per-invariant pass/fail with reason
      violated_invariants — IDs of invariants that failed
      rationale           — human-readable summary
      remediation         — guidance for resolving violations (FAIL only)
    """
    global _state

    if _state not in (GuardianState.ACTIVE,):
        blocked_record: dict[str, Any] = {
            "event": "OP-INTERCEPT-LOOP",
            "timestamp": _now_iso(),
            "contract_id": CONTRACT_ID,
            "agent_id": agent_id,
            "tool_name": tool_name,
            "decision": "FAIL",
            "violated_invariants": [],
            "rationale": (
                f"Guardian is not in ACTIVE state (current: {_state.value}). "
                "All tool calls are blocked until Guardian reaches ACTIVE."
            ),
            "halt_id": "HALT-003",
        }
        log_decision(blocked_record)
        return blocked_record

    results: list[dict[str, Any]] = []
    overall_pass = True
    violated_invariants: list[str] = []
    fail_reasons: list[str] = []

    for inv in _invariants:
        inv_id = inv["id"]
        checker = _INVARIANT_CHECKERS.get(inv_id)

        if checker is None:
            results.append(
                {
                    "invariant_id": inv_id,
                    "severity": inv.get("severity"),
                    "result": "SKIP",
                    "reason": "No checker function registered for this invariant ID.",
                }
            )
            continue

        try:
            passed, reason = checker(agent_id, tool_name, params)
        except Exception as exc:
            # HALT-003: unhandled exception in invariant engine
            tb = traceback.format_exc()
            results.append(
                {
                    "invariant_id": inv_id,
                    "severity": inv.get("severity"),
                    "result": "ERROR",
                    "reason": f"Invariant engine exception: {exc}",
                    "traceback": tb,
                }
            )
            overall_pass = False
            violated_invariants.append(inv_id)
            fail_reasons.append(f"{inv_id}: engine exception — {exc}")
            _state = GuardianState.FAIL_HALT
            break

        results.append(
            {
                "invariant_id": inv_id,
                "severity": inv.get("severity"),
                "result": "PASS" if passed else "FAIL",
                "reason": reason,
            }
        )
        if not passed:
            # Most restrictive wins (CONFLICT-003) — continue evaluation to log all failures
            overall_pass = False
            violated_invariants.append(inv_id)
            fail_reasons.append(f"{inv_id}: {reason}")

    decision = "PASS" if overall_pass else "FAIL"

    remediation: str | None = None
    if not overall_pass:
        remediation = (
            "Review violated_invariants in this record. For each: "
            "(1) consult CRSP-001.json sections.invariants for the full rule text; "
            "(2) correct tool call parameters or obtain required human approvals; "
            "(3) for constitution file writes: initiate SOP-010 Amendment Process; "
            "(4) do not retry until all violations are resolved."
        )

    decision_record: dict[str, Any] = {
        "event": "OP-INTERCEPT-LOOP",
        "timestamp": _now_iso(),
        "contract_id": CONTRACT_ID,
        "agent_id": agent_id,
        "tool_name": tool_name,
        "invariants_evaluated": [r["invariant_id"] for r in results],
        "invariant_results": results,
        "decision": decision,
        "violated_invariants": violated_invariants,
        "fail_reasons": fail_reasons,
        "rationale": (
            f"All {len(results)} invariants passed."
            if overall_pass
            else (
                f"{len(violated_invariants)} invariant(s) violated: {violated_invariants}"
            )
        ),
        "remediation": remediation,
    }

    # INVARIANT_GUARDIAN_LOG_01: write BEFORE returning verdict
    log_decision(decision_record)
    return decision_record


def emit_stop(agent_id: str, invariant_id: str, reason: str) -> dict[str, Any]:
    """
    OP-FAIL-HALT: Emit a structured STOP signal to the requesting agent and
    write a structured FAIL record to verification/crsp_CRSP-001_log.json.

    Per CRSP-001.json step 6 success condition:
      STOP signal emitted; structured FAIL record persisted.
    """
    record: dict[str, Any] = {
        "event": "OP-FAIL-HALT",
        "signal": "STOP",
        "timestamp": _now_iso(),
        "contract_id": CONTRACT_ID,
        "agent_id": agent_id,
        "invariant_violated": invariant_id,
        "reason": reason,
        "recommended_remediation": (
            "1. Review CRSP-001.json sections.invariants for the violated invariant rule. "
            "2. Correct the tool call parameters or obtain required approvals. "
            "3. For constitution file writes: initiate SOP-010 Amendment Process. "
            "4. For architectural decisions: obtain human_review_approved=true. "
            "5. Do not retry until the invariant violation is fully resolved."
        ),
        "halt_state": GuardianState.FAIL_HALT.value,
        "recovery_ref": "CRSP-001.json sections.rollback_recovery",
    }
    log_decision(record)
    return record


# ---------------------------------------------------------------------------
# OP-EVIDENCE-FLUSH (Step 7)
# ---------------------------------------------------------------------------


def flush_evidence() -> None:
    """
    OP-EVIDENCE-FLUSH: On session end or SIGTERM, write a session summary record
    to verification/crsp_CRSP-001_log.json.

    CRSP-001.json halt_condition: "Log flush fails after 3 retries"
    """
    summary: dict[str, Any] = {
        "event": "OP-EVIDENCE-FLUSH",
        "signal": "SESSION_END",
        "timestamp": _now_iso(),
        "contract_id": CONTRACT_ID,
        "guardian_state": _state.value,
        "trinity_files_hashed": list(_trinity_hashes.keys()),
        "invariants_registered": len(_invariants),
        "summary": (
            "Guardian Kernel session ended. All buffered log entries flushed. "
            "Authoritative truth surface: verification/crsp_CRSP-001_log.json"
        ),
    }

    for attempt in range(1, 4):
        try:
            _write_log(summary)
            return
        except SystemExit:
            if attempt == 3:
                print(
                    "[GUARDIAN FAIL_HALT] OP-EVIDENCE-FLUSH failed after 3 retries.",
                    file=sys.stderr,
                )


def _handle_sigterm(signum: int, frame: Any) -> None:
    flush_evidence()
    sys.exit(0)


# ---------------------------------------------------------------------------
# OP-MCP-INIT (Step 3): MCP Server — FastMCP pattern (mcp >= 1.0.0)
# Registers tool call interceptors for all 6 Agent Republic roles.
# ---------------------------------------------------------------------------

mcp = FastMCP("guardian-kernel")


@mcp.tool()
def intercept_tool_call(
    agent_id: str,
    tool_name: str,
    params: str,
) -> str:
    """
    Guardian primary interception gate (INVARIANT_ARTICLE_II_01).

    All agent tool calls MUST route through this endpoint before execution.
    Evaluates the call against all 13 registered invariants sequentially.
    Returns a JSON verdict with decision (PASS or FAIL) and full audit trail.

    Args:
        agent_id:  One of: planner, builder, sentinel, tdd, reviewer, datasci
        tool_name: The name of the tool the agent intends to call
        params:    JSON-encoded dict of tool parameters

    Returns:
        JSON string — verdict with decision, invariant_results, rationale, remediation
    """
    try:
        parsed_params: dict[str, Any] = (
            json.loads(params) if isinstance(params, str) else params
        )
    except json.JSONDecodeError as exc:
        err_record = {
            "decision": "FAIL",
            "reason": f"Invalid params JSON: {exc}",
            "agent_id": agent_id,
            "tool_name": tool_name,
            "timestamp": _now_iso(),
            "contract_id": CONTRACT_ID,
        }
        log_decision(err_record)
        return json.dumps(err_record, indent=2)

    verdict = evaluate_invariants(agent_id, tool_name, parsed_params)

    # OP-FAIL-HALT: if any invariant violated, emit structured STOP for each
    for violated_id in verdict.get("violated_invariants", []):
        emit_stop(agent_id, violated_id, verdict.get("rationale", ""))

    return json.dumps(verdict, indent=2)


@mcp.tool()
def guardian_health_check() -> str:
    """
    AC-002: Guardian MCP server health check.
    Returns current runtime state, invariant registry, and trinity status.
    """
    health: dict[str, Any] = {
        "event": "HEALTH_CHECK",
        "guardian_state": _state.value,
        "contract_id": CONTRACT_ID,
        "invariants_registered": len(_invariants),
        "invariant_ids": [inv["id"] for inv in _invariants],
        "constitutional_invariants_count": len(CONSTITUTIONAL_INVARIANTS),
        "guardian_specific_invariants_count": len(GUARDIAN_SPECIFIC_INVARIANTS),
        "trinity_loaded": bool(_trinity_hashes),
        "trinity_files": list(_trinity_hashes.keys()),
        "verification_log": str(LOG_PATH),
        "healthy": _state == GuardianState.ACTIVE,
        "timestamp": _now_iso(),
        "version": "1.0.0",
        "series": "Series-A",
    }
    return json.dumps(health, indent=2)


# Agent-specific interceptors — OP-MCP-INIT registers one per Agent Republic role


@mcp.tool()
def planner_intercept(tool_name: str, params: str) -> str:
    """Constitutional interceptor for Planner agent tool calls."""
    return intercept_tool_call("planner", tool_name, params)


@mcp.tool()
def builder_intercept(tool_name: str, params: str) -> str:
    """Constitutional interceptor for Builder agent tool calls."""
    return intercept_tool_call("builder", tool_name, params)


@mcp.tool()
def sentinel_intercept(tool_name: str, params: str) -> str:
    """Constitutional interceptor for Sentinel agent tool calls."""
    return intercept_tool_call("sentinel", tool_name, params)


@mcp.tool()
def tdd_intercept(tool_name: str, params: str) -> str:
    """Constitutional interceptor for TDD agent tool calls."""
    return intercept_tool_call("tdd", tool_name, params)


@mcp.tool()
def reviewer_intercept(tool_name: str, params: str) -> str:
    """Constitutional interceptor for Reviewer agent tool calls."""
    return intercept_tool_call("reviewer", tool_name, params)


@mcp.tool()
def datasci_intercept(tool_name: str, params: str) -> str:
    """Constitutional interceptor for DataSci agent tool calls."""
    return intercept_tool_call("datasci", tool_name, params)


# ---------------------------------------------------------------------------
# Main entrypoint — executes Ordered Operations 1-3, then enters MCP event loop
# ---------------------------------------------------------------------------


def main() -> None:
    global _state

    parser = argparse.ArgumentParser(
        description="Guardian Kernel — MCP Safety Enforcement Server (CRSP-001 Series A)"
    )
    parser.add_argument(
        "--health-check",
        action="store_true",
        help="Run preflight verification and exit with health report (AC-002).",
    )
    args = parser.parse_args()

    # Register SIGTERM handler so OP-EVIDENCE-FLUSH runs on process termination
    signal.signal(signal.SIGTERM, _handle_sigterm)

    # OP-BOOTSTRAP (Step 1)
    bootstrap_trinity()

    # OP-INVARIANT-LOAD (Step 2)
    load_invariants()

    # AC-002: --health-check mode exits after bootstrap + invariant load
    if args.health_check:
        _state = GuardianState.ACTIVE
        print(guardian_health_check())
        flush_evidence()
        sys.exit(0)

    # OP-MCP-INIT (Step 3)
    _state = GuardianState.MCP_STARTING
    init_record: dict[str, Any] = {
        "event": "OP-MCP-INIT",
        "timestamp": _now_iso(),
        "contract_id": CONTRACT_ID,
        "agent_interceptors_registered": AGENT_IDS,
        "tools_registered": [
            "intercept_tool_call",
            "guardian_health_check",
            "planner_intercept",
            "builder_intercept",
            "sentinel_intercept",
            "tdd_intercept",
            "reviewer_intercept",
            "datasci_intercept",
        ],
        "status": "MCP server starting",
    }
    _write_log(init_record)

    _state = GuardianState.ACTIVE
    active_record: dict[str, Any] = {
        "event": "GUARDIAN_ACTIVE",
        "timestamp": _now_iso(),
        "contract_id": CONTRACT_ID,
        "state": GuardianState.ACTIVE.value,
        "invariants_enforcing": [inv["id"] for inv in _invariants],
        "message": (
            "Guardian Kernel is ACTIVE. All agent tool calls are now subject to "
            "constitutional invariant enforcement. "
            "Authoritative truth surface: verification/crsp_CRSP-001_log.json"
        ),
    }
    _write_log(active_record)

    # OP-INTERCEPT-LOOP (Steps 4-6) is handled by the MCP server event loop.
    # mcp.run() blocks until SIGTERM or process exit.
    mcp.run()


if __name__ == "__main__":
    main()
