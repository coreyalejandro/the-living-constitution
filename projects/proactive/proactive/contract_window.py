"""
PROACTIVE Contract Window — Persistent Constraint Rendering

Second layer of the PROACTIVE pipeline. Takes the IntentReceipt from
COL and renders a persistent contract that makes constraints explicit
and auditable at every decision point.

Enforces I4 (traceability) and I1 (evidence-first) by making the
user's intent, the system's understanding, and all active constraints
visible before any action is taken.

Output: ContractWindowState with status CONFIRMED or PENDING.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional

from proactive.col import IntentReceipt


__all__ = [
    "ContractWindowState",
    "create_contract_state",
    "render_contract",
]


# ---------------------------------------------------------------------------
# Risk assessment helpers
# ---------------------------------------------------------------------------

_HIGH_RISK_CONSTRAINTS = {"security", "backward_compat"}
_MEDIUM_RISK_CONSTRAINTS = {"performance", "test_coverage", "type_safety"}

_RISK_BY_ACTION = {
    "remove": "HIGH",
    "fix": "HIGH",
    "refactor": "MEDIUM",
    "update": "MEDIUM",
    "optimize": "MEDIUM",
    "create": "LOW",
    "test": "LOW",
    "document": "LOW",
}

# Keywords in goal that can elevate risk
_GOAL_RISK_KEYWORDS = {
    "security": "HIGH",
    "vulnerability": "HIGH",
    "exploit": "HIGH",
    "performance": "MEDIUM",
    "latency": "MEDIUM",
    "throughput": "MEDIUM",
    "scalability": "MEDIUM",
}

_AGENT_NEEDS_BASE = [
    "Power continuity",
    "Token budget sufficient",
    "Intent translated",
    "Contract visible",
]

_AGENT_NEEDS_BY_CONSTRAINT = {
    "security": "Security review required",
    "performance": "Performance baseline established",
    "backward_compat": "Compatibility matrix verified",
    "test_coverage": "Coverage threshold confirmed",
    "type_safety": "Type checker configured",
    "no_new_deps": "Dependency manifest locked",
}


# ---------------------------------------------------------------------------
# Dataclass
# ---------------------------------------------------------------------------

@dataclass
class ContractWindowState:
    """The rendered persistent contract for a merge request.

    Visible at every decision point in the pipeline. Status is
    CONFIRMED when intent is clear and all needs are met, PENDING
    when clarification is required.
    """

    user_intent_human: str          # Raw text of what the user said
    user_intent_machine: str        # Structured machine interpretation
    working_budget: str             # Token budget display
    agent_needs: List[str]          # What the agent requires to proceed
    risk_assessment: str            # LOW, MEDIUM, or HIGH
    risk_factors: List[str] = field(default_factory=list)  # Why this risk level
    constraints: List[str] = field(default_factory=list)   # Active constraints from intent
    goal: str = ""                   # The inferred goal from COL
    status: str = "PENDING"          # CONFIRMED or PENDING


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

def _assess_risk(
    action: str,
    constraints: List[str],
    goal: str,
    confidence: float,
) -> tuple[str, List[str]]:
    """Determine risk level and contributing factors from intent."""
    factors = []
    base_risk = "LOW"

    # Action-based risk
    action_risk = _RISK_BY_ACTION.get(action, "MEDIUM")
    if action_risk == "HIGH":
        factors.append(f"Action '{action}' is high-risk")
        base_risk = "HIGH"
    elif action_risk == "MEDIUM":
        factors.append(f"Action '{action}' carries moderate risk")
        if base_risk == "LOW":
            base_risk = "MEDIUM"

    # Constraint-based risk
    if any(c in _HIGH_RISK_CONSTRAINTS for c in constraints):
        base_risk = "HIGH"
        high_constraints = [c for c in constraints if c in _HIGH_RISK_CONSTRAINTS]
        factors.append(f"High-risk constraints: {', '.join(high_constraints)}")
    elif any(c in _MEDIUM_RISK_CONSTRAINTS for c in constraints):
        if base_risk != "HIGH":
            base_risk = "MEDIUM"
        medium_constraints = [c for c in constraints if c in _MEDIUM_RISK_CONSTRAINTS]
        factors.append(f"Medium-risk constraints: {', '.join(medium_constraints)}")

    # Goal-based risk
    goal_lower = goal.lower()
    for keyword, risk_level in _GOAL_RISK_KEYWORDS.items():
        if keyword in goal_lower:
            factors.append(f"Goal mentions '{keyword}' ({risk_level} risk)")
            if risk_level == "HIGH":
                base_risk = "HIGH"
            elif risk_level == "MEDIUM" and base_risk != "HIGH":
                base_risk = "MEDIUM"

    # Low confidence can elevate risk
    if confidence < 0.6 and base_risk != "HIGH":
        base_risk = "MEDIUM"
        factors.append(f"Low confidence ({confidence:.2f}) elevates risk")

    # If no factors were added, note that
    if not factors:
        factors.append("No specific risk factors identified")

    return base_risk, factors


def _build_agent_needs(constraints: List[str], risk: str, goal: str) -> List[str]:
    """Build the list of agent needs from base needs + constraint-specific needs."""
    needs = list(_AGENT_NEEDS_BASE)

    # Add needs from constraints
    for constraint in constraints:
        extra = _AGENT_NEEDS_BY_CONSTRAINT.get(constraint)
        if extra and extra not in needs:
            needs.append(extra)

    # Add needs based on goal keywords (optional, but helpful)
    goal_lower = goal.lower()
    if "security" in goal_lower and "Security review required" not in needs:
        needs.append("Security review required")
    if "performance" in goal_lower and "Performance baseline established" not in needs:
        needs.append("Performance baseline established")

    if risk == "HIGH":
        needs.append("No secrets in output")

    return needs


def _machine_intent_summary(intent_receipt: IntentReceipt) -> str:
    """Render the machine's structured understanding as a readable string."""
    p = intent_receipt.parsed_intent
    parts = [
        f"action {p.action}",
        f"target {p.target}",
        f"scope {p.scope}",
        f"goal: {p.goal}",
    ]
    if p.constraints:
        parts.append(f"constraints {', '.join(p.constraints)}")
    if p.ambiguities:
        parts.append(f"ambiguities {', '.join(p.ambiguities)}")
    return ", ".join(parts)


def _estimate_budget(text_length: int) -> str:
    """Rough token budget estimate based on input length."""
    # ~4 chars per token, pipeline uses ~3 LLM calls
    input_tokens = text_length // 4
    used = input_tokens + 1000  # base overhead
    total = 1_000_000
    return f"{used:,} / {total:,} tokens"


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def create_contract_state(intent_receipt: IntentReceipt) -> ContractWindowState:
    """Create a ContractWindowState from an IntentReceipt.

    Args:
        intent_receipt: Output from COL's compile_intent().

    Returns:
        ContractWindowState with status CONFIRMED or PENDING.
    """
    p = intent_receipt.parsed_intent

    risk_level, risk_factors = _assess_risk(
        p.action,
        p.constraints,
        p.goal,
        intent_receipt.confidence,
    )
    agent_needs = _build_agent_needs(p.constraints, risk_level, p.goal)
    machine_summary = _machine_intent_summary(intent_receipt)
    budget = _estimate_budget(len(intent_receipt.raw_text))

    status = "PENDING" if intent_receipt.needs_clarification else "CONFIRMED"

    return ContractWindowState(
        user_intent_human=intent_receipt.raw_text[:500],
        user_intent_machine=machine_summary,
        working_budget=budget,
        agent_needs=agent_needs,
        risk_assessment=risk_level,
        risk_factors=risk_factors,
        constraints=list(p.constraints),
        goal=p.goal,
        status=status,
    )


def render_contract(state: ContractWindowState, receipt: Optional[IntentReceipt] = None) -> str:
    """Render the contract as a human-readable string for display or logging.

    Args:
        state: A ContractWindowState from create_contract_state().
        receipt: Optional IntentReceipt to show LLM status.

    Returns:
        Formatted contract string.
    """
    needs_block = "\n".join(f"  - {need}" for need in state.agent_needs)
    constraints_block = (
        ", ".join(state.constraints) if state.constraints else "none"
    )
    factors_block = "\n".join(f"  - {factor}" for factor in state.risk_factors)

    # Determine LLM status if receipt provided
    if receipt:
        llm_status = "✅ Active (Claude)" if receipt.llm_used else "⚠️ Fallback (regex)"
    else:
        llm_status = "⚠️ Status unknown (no receipt)"

    status_label = (
        "CONFIRMED — Ready to proceed"
        if state.status == "CONFIRMED"
        else "PENDING — Clarification required before proceeding"
    )

    return (
        f"╔══ PERSISTENT CONTRACT WINDOW ══════════════════════════════╗\n"
        f"  USER INTENT (Human):   {state.user_intent_human[:80]}\n"
        f"  USER INTENT (Machine): {state.user_intent_machine}\n"
        f"  GOAL:                  {state.goal}\n"
        f"  LLM STATUS:            {llm_status}\n"
        f"  WORKING BUDGET:        {state.working_budget}\n"
        f"  RISK LEVEL:            {state.risk_assessment}\n"
        f"  RISK FACTORS:\n{factors_block}\n"
        f"  CONSTRAINTS:           {constraints_block}\n"
        f"  AGENT NEEDS:\n{needs_block}\n"
        f"  STATUS:                {status_label}\n"
        f"╚════════════════════════════════════════════════════════════╝"
    )