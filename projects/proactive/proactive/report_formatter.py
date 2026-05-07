"""
PROACTIVE Report Formatter — V&T Statement Generation

Fifth layer of the PROACTIVE pipeline. Takes the full MRAnalysisResult
and formats it as a structured MR comment with a mandatory V&T
(Verification & Truth) statement.

The V&T statement is the enforcement mechanism for:
- I1 (Evidence-First): every claim is tagged
- I2 (No Phantom Work): no phantom completions
- I5 (Safety Over Fluency): uncertainty is explicit

Output: Formatted markdown string ready to post as an MR comment.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from proactive.mr_analyzer import MRAnalysisResult, Claim

__all__ = [
    "format_review_comment",
]

_VERDICT_ICONS = {
    "APPROVED": "✅",
    "FLAGGED": "⚠️",
    "BLOCKED": "🚫",
    "DRIFT_DETECTED": "🔀",
    "PENDING_CLARIFICATION": "❓",
}

_SEVERITY_ICONS = {
    "ERROR": "❌",
    "WARNING": "⚠️",
}


# ---------------------------------------------------------------------------
# Section formatters
# ---------------------------------------------------------------------------

def _format_header(result: "MRAnalysisResult") -> str:
    icon = _VERDICT_ICONS.get(result.verdict, "ℹ️")
    trust_pct = int(result.trust_score * 100)
    return (
        f"## PROACTIVE Constitutional Review\n\n"
        f"{icon} **Verdict:** {result.verdict}\n"
        f"**Trust Score:** {trust_pct}%\n"
    )


def _format_intent(result: "MRAnalysisResult") -> str:
    if not result.receipt:
        return ""

    p = result.receipt.parsed_intent
    lines = [
        "### Intent\n",
        f"- **Action:** {p.action}",
        f"- **Target:** {p.target}",
        f"- **Scope:** {p.scope}",
        f"- **Goal:** {p.goal}",
    ]
    if p.constraints:
        lines.append(f"- **Constraints:** {', '.join(p.constraints)}")
    if p.ambiguities:
        lines.append(f"- **Ambiguities:** {', '.join(p.ambiguities)}")
    lines.append(f"- **Confidence:** {int(result.receipt.confidence * 100)}%")

    if result.receipt.clarification_questions:
        lines.append("\n**Clarification needed:**")
        for q in result.receipt.clarification_questions:
            lines.append(f"- {q}")

    return "\n".join(lines) + "\n"


def _format_contract(result: "MRAnalysisResult") -> str:
    if not result.contract:
        return ""

    c = result.contract
    needs = "\n".join(f"  - {n}" for n in c.agent_needs)
    status_label = (
        "CONFIRMED — Ready to proceed"
        if c.status == "CONFIRMED"
        else f"PENDING — {c.status}"
    )

    return (
        "### Contract Window\n\n"
        f"- **Status:** {status_label}\n"
        f"- **Risk Level:** {c.risk_assessment}\n"
        f"- **Risk Factors:**\n"
        + "\n".join(f"  - {f}" for f in c.risk_factors) + "\n"
        f"- **Constraints:** {', '.join(c.constraints) if c.constraints else 'none'}\n"
        f"- **Agent Needs:**\n{needs}\n"
    )


def _format_claims(claims: list["Claim"]) -> str:
    """Format detected claims by type."""
    if not claims:
        return "### Claims Detected\n\nNo verifiable claims found.\n"

    by_type = {}
    for c in claims:
        by_type.setdefault(c.claim_type, []).append(c)

    lines = ["### Claims Detected\n"]
    for ctype, clist in by_type.items():
        lines.append(f"**{ctype.capitalize()}** ({len(clist)}):")
        for c in clist:
            src = f" [{c.source}]" if c.source else ""
            line_info = f" (line {c.line_number})" if c.line_number else ""
            lines.append(f"- {c.text}{src}{line_info}")
    return "\n".join(lines) + "\n"


def _format_violations(result: "MRAnalysisResult") -> str:
    if not result.violations:
        return "### Invariant Checks\n\n✅ No violations detected.\n"

    errors = [v for v in result.violations if v.severity == "ERROR"]
    warnings = [v for v in result.violations if v.severity == "WARNING"]

    lines = ["### Invariant Violations\n"]

    if errors:
        lines.append("**ERRORS** (merge blocked):\n")
        for v in errors:
            loc = f" {v.location.get('file')}:{v.location.get('line')}" if v.location else ""
            lines.append(f"- {_SEVERITY_ICONS['ERROR']} `[{v.invariant}]`{loc} {v.message}")
            if v.suggested_fix:
                lines.append(f"  - 💡 *Fix:* {v.suggested_fix}")

    if warnings:
        lines.append("\n**WARNINGS**:\n")
        for v in warnings:
            loc = f" {v.location.get('file')}:{v.location.get('line')}" if v.location else ""
            lines.append(f"- {_SEVERITY_ICONS['WARNING']} `[{v.invariant}]`{loc} {v.message}")
            if v.suggested_fix:
                lines.append(f"  - 💡 *Fix:* {v.suggested_fix}")

    return "\n".join(lines) + "\n"


def _format_drift(result: "MRAnalysisResult") -> str:
    if not result.drift:
        return ""

    if not result.drift.has_drift:
        return "### Drift Detection\n\n✅ No drift detected. Diff aligns with stated intent.\n"

    lines = [
        "### Drift Detection\n",
        f"⚠️ **Drift Detected** (severity: {result.drift.drift_severity})\n",
    ]
    if result.drift.unrelated_additions:
        lines.append("**Unrelated additions:**")
        for item in result.drift.unrelated_additions:
            lines.append(f"- {item}")
    if result.drift.suggestion:
        lines.append(f"\n*{result.drift.suggestion}*")

    return "\n".join(lines) + "\n"


def _format_evidence_summary(result: "MRAnalysisResult") -> str:
    """Summarize the evidence used for verification."""
    lines = ["### Evidence Summary\n"]

    # Pipeline / test artifact info
    if result.pipeline_url:
        lines.append(f"- **CI Pipeline:** [{result.pipeline_url}]({result.pipeline_url})")
    if result.pipeline_status:
        lines.append(f"- **Pipeline Status:** {result.pipeline_status}")
    lines.append(f"- **Test Artifacts:** {'✅ Present' if result.test_artifacts_exist else '❌ Not found'}")

    # Number of claims and violations
    lines.append(f"- **Claims Analyzed:** {len(result.claims_found)}")
    lines.append(f"- **Violations Detected:** {len(result.violations)}")
    if result.receipt:
        lines.append(f"- **Intent Confidence:** {int(result.receipt.confidence * 100)}%")

    # Invariant failure counts
    inv_counts = {}
    for v in result.violations:
        inv_counts[v.invariant] = inv_counts.get(v.invariant, 0) + 1
    if inv_counts:
        lines.append("- **Invariant Failures:**")
        for inv, count in inv_counts.items():
            lines.append(f"  - {inv}: {count} violations")

    return "\n".join(lines) + "\n"


def _format_vt_statement(result: "MRAnalysisResult") -> str:
    """Generate the mandatory V&T statement with concrete evidence references."""
    claims_count = len(result.claims_found)
    violations_count = len(result.violations)

    # Build EXISTS list with specific evidence items
    exists_items = [
        f"Analyzed {claims_count} claim(s) from description/comments",
        f"Checked {violations_count} invariant(s)",
    ]
    if result.contract:
        exists_items.append(f"Contract window rendered (status: {result.contract.status})")
    if result.drift:
        exists_items.append("Diff compared to intent for drift")
    if result.pipeline_url:
        exists_items.append(f"CI pipeline inspected: {result.pipeline_url}")

    # VERIFIED AGAINST list
    verified_items = ["MR description and title", "Code diff"]
    if result.receipt:
        verified_items.append(
            f"Intent receipt (action={result.receipt.parsed_intent.action}, "
            f"target={result.receipt.parsed_intent.target})"
        )
    if result.test_artifacts_exist:
        verified_items.append("Test artifacts (assumed present)")

    # NOT CLAIMED (limitations)
    not_claimed_items = [
        "No code execution or runtime testing performed",
        "No access to actual test run artifacts (only existence)",
        "No security audit or penetration testing",
        "No verification of external dependencies",
    ]

    # Status line
    status = result.verdict
    if status == "APPROVED":
        status_line = f"PASS — All invariants satisfied, evidence checked"
    elif status == "BLOCKED":
        status_line = f"BLOCK — {violations_count} ERROR violation(s) detected"
    elif status == "FLAGGED":
        status_line = f"WARN — {violations_count} WARNING violation(s) detected"
    elif status == "DRIFT_DETECTED":
        drift_count = len(result.drift.unrelated_additions) if result.drift else 0
        status_line = f"WARN — Scope drift detected ({drift_count} unrelated change(s))"
    else:
        status_line = f"PENDING — {status}"

    exists_block = "\n".join(f"  - {i}" for i in exists_items)
    verified_block = "\n".join(f"  - {i}" for i in verified_items)
    not_claimed_block = "\n".join(f"  - {i}" for i in not_claimed_items)

    return (
        "---\n\n"
        "**V&T Statement (Verification & Truth):**\n"
        f"- **EXISTS:**\n{exists_block}\n"
        f"- **VERIFIED AGAINST:**\n{verified_block}\n"
        f"- **NOT CLAIMED:**\n{not_claimed_block}\n"
        f"- **STATUS:** {status_line}\n"
    )


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def format_review_comment(result: "MRAnalysisResult") -> str:
    """Format a full PROACTIVE review as a markdown MR comment.

    Includes intent, contract window, claims, violations, drift detection,
    evidence summary, and the mandatory V&T statement.

    Args:
        result: MRAnalysisResult from analyze_mr().

    Returns:
        Markdown string ready to post as an MR comment.
    """
    sections = [
        _format_header(result),
        _format_intent(result),
        _format_contract(result),
        _format_claims(result.claims_found),
        _format_violations(result),
        _format_drift(result),
        _format_evidence_summary(result),
        _format_vt_statement(result),
    ]

    return "\n".join(s for s in sections if s)