"""
PROACTIVE V&T Statement Generator — Standalone Verification & Truth Tool

Generates V&T (Verification & Truth) statements from MR descriptions
and diffs without requiring the full pipeline. Provides confidence
breakdowns per claim and exports in multiple formats.

This is Enhancement #5 of the PROACTIVE framework.

Usage:
    from proactive.vt_generator import generate_vt_statement
    result = generate_vt_statement(description, diff)
    print(result.markdown)
"""

from __future__ import annotations

import json
import logging
import re
from dataclasses import dataclass, field
from typing import Dict, List, Optional

from proactive.col import IntentReceipt, compile_intent
from proactive.validator import Violation, check_invariants
from proactive.drift_detector import DriftResult, detect_drift

logger = logging.getLogger(__name__)

__all__ = [
    "ClaimAnalysis",
    "VTStatement",
    "VTGeneratorResult",
    "generate_vt_statement",
]


# ---------------------------------------------------------------------------
# Claim patterns (reused from mr_analyzer but self-contained)
# ---------------------------------------------------------------------------

_CLAIM_PATTERNS = [
    (r"\b(?:all\s+)?tests?\s+pass(?:ing|ed|es)?\b", "completion"),
    (r"\b(?:implementation|feature)\s+(?:is\s+)?completed?\b", "completion"),
    (r"\bfully\s+implemented\b", "completion"),
    (r"\bready\s+(?:for\s+)?(?:review|merge|production)\b", "completion"),
    (r"\bO\([^)]+\)", "performance"),
    (r"\b\d+x\s+(?:faster|slower|improvement)\b", "performance"),
    (r"\breduced\s+(?:latency|time|memory)\b", "performance"),
    (r"\breduces?\s+(?:latency|time|memory)\b", "performance"),
    (r"\bfixes?\s+(?:the\s+)?bug\b", "correctness"),
    (r"\bresolves?\s+(?:the\s+)?issue\b", "correctness"),
    (r"\bno\s+(?:more\s+)?(?:errors?|bugs?|issues?)\b", "correctness"),
    (r"\b(?:prevents?|stops?|blocks?)\s+(?:sql\s+injection|xss|csrf)\b", "security"),
    (r"\b(?:adds?|implements?)\s+(?:authentication|authorization)\b", "security"),
    (r"\b\d+%\s+(?:coverage|test|code)\b", "metric"),
    (r"\bcertainly|definitely|guaranteed|always|never\b", "absolute"),
]


# ---------------------------------------------------------------------------
# Dataclasses
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class ClaimAnalysis:
    """Analysis of a single claim found in MR text."""

    text: str
    claim_type: str
    confidence: float          # 0.0 - 1.0 confidence that claim is verified
    evidence_status: str       # "verified", "inferred", "unverified", "phantom"
    violations: List[str] = field(default_factory=list)
    suggestion: str = ""


@dataclass(frozen=True)
class VTStatement:
    """A structured V&T (Verification & Truth) statement."""

    exists: List[str]
    verified_against: List[str]
    not_claimed: List[str]
    status: str                # "PASS", "WARN", "BLOCK"
    status_detail: str = ""


@dataclass
class VTGeneratorResult:
    """Complete result from the V&T generator."""

    claims: List[ClaimAnalysis] = field(default_factory=list)
    vt_statement: Optional[VTStatement] = None
    intent: Optional[IntentReceipt] = None
    violations: List[Violation] = field(default_factory=list)
    drift: Optional[DriftResult] = None
    overall_confidence: float = 1.0
    total_claims: int = 0
    verified_claims: int = 0
    unverified_claims: int = 0

    @property
    def markdown(self) -> str:
        """Render the V&T statement as markdown."""
        return render_markdown(self)

    @property
    def as_json(self) -> str:
        """Render the result as JSON."""
        return render_json(self)


# ---------------------------------------------------------------------------
# Claim extraction and analysis
# ---------------------------------------------------------------------------

def _extract_claims(text: str) -> List[dict]:
    """Extract raw claims from text."""
    claims = []
    seen = set()
    for pattern, claim_type in _CLAIM_PATTERNS:
        for match in re.finditer(pattern, text, re.IGNORECASE):
            start = text.rfind(".", 0, match.start())
            end = text.find(".", match.end())
            sentence = text[start + 1: (end + 1 if end != -1 else len(text))].strip()
            if not sentence:
                sentence = match.group()
            key = sentence.lower().strip()
            if key not in seen:
                seen.add(key)
                claims.append({
                    "text": sentence,
                    "claim_type": claim_type,
                    "match": match.group(),
                })
    return claims


def _assess_claim_confidence(
    claim: dict,
    violations: List[Violation],
    has_diff: bool,
) -> ClaimAnalysis:
    """Assess confidence level for a single claim."""
    claim_text = claim["text"].lower()
    claim_type = claim["claim_type"]

    # Check if any violations reference this claim
    related_violations = [
        v.message for v in violations
        if claim["match"].lower() in v.message.lower()
        or claim_type in v.message.lower()
    ]

    # Determine evidence status
    if related_violations:
        if any("phantom" in v.lower() or "I2" in v for v in related_violations):
            evidence_status = "phantom"
            confidence = 0.1
        elif any("untagged" in v.lower() or "I1" in v for v in related_violations):
            evidence_status = "unverified"
            confidence = 0.3
        else:
            evidence_status = "inferred"
            confidence = 0.5
    elif claim_type == "absolute":
        evidence_status = "unverified"
        confidence = 0.2
        related_violations.append("Absolute claim without evidence tag")
    elif claim_type in ("completion", "metric") and not has_diff:
        evidence_status = "unverified"
        confidence = 0.3
    else:
        evidence_status = "inferred"
        confidence = 0.7

    # Build suggestion
    if evidence_status == "phantom":
        suggestion = "Remove completion claim or provide test artifacts."
    elif evidence_status == "unverified":
        suggestion = f"Add evidence tag: '{claim['text'][:50]} [verified]' or hedge with 'likely'."
    elif evidence_status == "inferred":
        suggestion = "Consider adding explicit verification evidence."
    else:
        suggestion = ""

    return ClaimAnalysis(
        text=claim["text"],
        claim_type=claim_type,
        confidence=confidence,
        evidence_status=evidence_status,
        violations=related_violations,
        suggestion=suggestion,
    )


# ---------------------------------------------------------------------------
# V&T statement construction
# ---------------------------------------------------------------------------

def _build_vt_statement(
    claims: List[ClaimAnalysis],
    violations: List[Violation],
    drift: Optional[DriftResult],
    intent: Optional[IntentReceipt],
    has_diff: bool,
) -> VTStatement:
    """Construct a V&T statement from analysis results."""
    # EXISTS
    exists = [f"Analyzed {len(claims)} claim(s) from input text"]
    if intent:
        exists.append(
            f"Intent parsed: action={intent.parsed_intent.action}, "
            f"target={intent.parsed_intent.target}"
        )
    if violations:
        exists.append(f"Checked {len(violations)} invariant violation(s)")
    if drift:
        exists.append("Drift analysis performed against stated intent")
    if has_diff:
        exists.append("Code diff analyzed")

    # VERIFIED AGAINST
    verified_against = ["Input description text"]
    if has_diff:
        verified_against.append("Code diff content")
    if intent:
        verified_against.append(
            f"Intent receipt (confidence: {int(intent.confidence * 100)}%)"
        )

    # NOT CLAIMED
    not_claimed = [
        "No code execution or runtime testing performed",
        "No access to CI/CD pipeline artifacts",
        "No external dependency verification",
        "No security audit performed",
    ]

    # STATUS
    error_count = sum(1 for v in violations if v.severity == "ERROR")
    warning_count = sum(1 for v in violations if v.severity == "WARNING")
    phantom_count = sum(1 for c in claims if c.evidence_status == "phantom")

    if error_count > 0 or phantom_count > 0:
        status = "BLOCK"
        status_detail = f"{error_count} error(s), {phantom_count} phantom claim(s)"
    elif warning_count > 0 or (drift and drift.has_drift):
        status = "WARN"
        parts = []
        if warning_count:
            parts.append(f"{warning_count} warning(s)")
        if drift and drift.has_drift:
            parts.append(f"drift detected ({drift.drift_severity})")
        status_detail = ", ".join(parts)
    else:
        status = "PASS"
        status_detail = "All checks passed"

    return VTStatement(
        exists=exists,
        verified_against=verified_against,
        not_claimed=not_claimed,
        status=status,
        status_detail=status_detail,
    )


# ---------------------------------------------------------------------------
# Output renderers
# ---------------------------------------------------------------------------

def render_markdown(result: VTGeneratorResult) -> str:
    """Render a VTGeneratorResult as a markdown string."""
    lines = ["## V&T Statement (Verification & Truth)\n"]

    # Summary
    lines.append(f"**Overall Confidence:** {int(result.overall_confidence * 100)}%")
    lines.append(f"**Claims:** {result.total_claims} total, "
                 f"{result.verified_claims} verified, "
                 f"{result.unverified_claims} unverified\n")

    # Intent
    if result.intent:
        p = result.intent.parsed_intent
        lines.append("### Intent")
        lines.append(f"- **Action:** {p.action}")
        lines.append(f"- **Target:** {p.target}")
        lines.append(f"- **Goal:** {p.goal}")
        lines.append(f"- **Confidence:** {int(result.intent.confidence * 100)}%\n")

    # Claims breakdown
    if result.claims:
        lines.append("### Claims Analysis\n")
        lines.append("| Claim | Type | Confidence | Status |")
        lines.append("|-------|------|-----------|--------|")
        for c in result.claims:
            conf_pct = f"{int(c.confidence * 100)}%"
            icon = {
                "verified": "\u2705",
                "inferred": "\U0001f7e1",  # large yellow circle
                "unverified": "\u26a0\ufe0f",
                "phantom": "\u274c",
            }.get(c.evidence_status, "\u2753")
            text_short = c.text[:60] + ("..." if len(c.text) > 60 else "")
            lines.append(f"| {text_short} | {c.claim_type} | {conf_pct} | {icon} {c.evidence_status} |")
        lines.append("")

    # Suggestions
    suggestions = [c for c in result.claims if c.suggestion]
    if suggestions:
        lines.append("### Suggestions\n")
        for c in suggestions:
            lines.append(f"- **{c.claim_type}:** {c.suggestion}")
        lines.append("")

    # Violations
    if result.violations:
        lines.append("### Violations\n")
        for v in result.violations:
            icon = "\u274c" if v.severity == "ERROR" else "\u26a0\ufe0f"
            lines.append(f"- {icon} `[{v.invariant}]` {v.message}")
            if v.suggested_fix:
                lines.append(f"  - \U0001f4a1 {v.suggested_fix}")
        lines.append("")

    # Drift
    if result.drift and result.drift.has_drift:
        lines.append("### Drift Detection\n")
        lines.append(f"\u26a0\ufe0f Drift detected (severity: {result.drift.drift_severity})")
        if result.drift.suggestion:
            lines.append(f"- {result.drift.suggestion}")
        lines.append("")

    # V&T block
    if result.vt_statement:
        vt = result.vt_statement
        lines.append("---\n")
        lines.append("**V&T Statement:**")
        lines.append("- **EXISTS:**")
        for item in vt.exists:
            lines.append(f"  - {item}")
        lines.append("- **VERIFIED AGAINST:**")
        for item in vt.verified_against:
            lines.append(f"  - {item}")
        lines.append("- **NOT CLAIMED:**")
        for item in vt.not_claimed:
            lines.append(f"  - {item}")
        lines.append(f"- **STATUS:** {vt.status} \u2014 {vt.status_detail}")

    return "\n".join(lines)


def render_json(result: VTGeneratorResult) -> str:
    """Render a VTGeneratorResult as a JSON string."""
    data = {
        "overall_confidence": result.overall_confidence,
        "total_claims": result.total_claims,
        "verified_claims": result.verified_claims,
        "unverified_claims": result.unverified_claims,
        "claims": [
            {
                "text": c.text,
                "type": c.claim_type,
                "confidence": c.confidence,
                "evidence_status": c.evidence_status,
                "violations": c.violations,
                "suggestion": c.suggestion,
            }
            for c in result.claims
        ],
        "violations": [
            {
                "invariant": v.invariant,
                "severity": v.severity,
                "message": v.message,
                "suggested_fix": v.suggested_fix,
            }
            for v in result.violations
        ],
        "vt_statement": {
            "exists": result.vt_statement.exists,
            "verified_against": result.vt_statement.verified_against,
            "not_claimed": result.vt_statement.not_claimed,
            "status": result.vt_statement.status,
            "status_detail": result.vt_statement.status_detail,
        } if result.vt_statement else None,
    }

    if result.intent:
        data["intent"] = {
            "action": result.intent.parsed_intent.action,
            "target": result.intent.parsed_intent.target,
            "goal": result.intent.parsed_intent.goal,
            "confidence": result.intent.confidence,
        }

    if result.drift:
        data["drift"] = {
            "has_drift": result.drift.has_drift,
            "severity": result.drift.drift_severity,
            "suggestion": result.drift.suggestion,
        }

    return json.dumps(data, indent=2)


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def generate_vt_statement(
    description: str,
    diff: str = "",
    title: str = "",
) -> VTGeneratorResult:
    """Generate a V&T statement from MR description and optional diff.

    Runs a lightweight version of the PROACTIVE pipeline:
    1. Parse intent (COL layer)
    2. Extract and analyze claims
    3. Check invariants (regex-only, no LLM required)
    4. Detect drift (if diff provided)
    5. Build V&T statement with confidence breakdown

    Args:
        description: MR description text.
        diff: Optional unified diff string.
        title: Optional MR title (prepended to description for intent parsing).

    Returns:
        VTGeneratorResult with claims, V&T statement, and confidence scores.
    """
    full_text = f"{title}. {description}".strip() if title else description
    has_diff = bool(diff.strip())

    # Parse intent
    intent = compile_intent(full_text)

    # Build intent dict for validator
    intent_dict = {
        "action": intent.parsed_intent.action,
        "target": intent.parsed_intent.target,
        "scope": intent.parsed_intent.scope,
        "goal": intent.parsed_intent.goal,
        "constraints": intent.parsed_intent.constraints,
        "ambiguities": intent.parsed_intent.ambiguities,
        "confidence": intent.confidence,
    }

    # Check invariants
    violations = check_invariants(
        description, "INPUT_TEXT", intent=intent_dict, skip_i4=True
    )

    # Detect drift
    drift = None
    if has_diff:
        drift = detect_drift(intent, diff)

    # Extract and analyze claims
    raw_claims = _extract_claims(description)
    analyzed_claims = [
        _assess_claim_confidence(c, violations, has_diff)
        for c in raw_claims
    ]

    # Calculate overall confidence
    if analyzed_claims:
        overall_confidence = round(
            sum(c.confidence for c in analyzed_claims) / len(analyzed_claims),
            2,
        )
        verified = sum(1 for c in analyzed_claims if c.evidence_status in ("verified", "inferred"))
        unverified = len(analyzed_claims) - verified
    else:
        # No claims found: confidence 1.0 means "nothing to dispute",
        # not "everything verified". The V&T statement's NOT CLAIMED
        # section makes the actual verification scope explicit.
        overall_confidence = 1.0
        verified = 0
        unverified = 0

    # Build V&T statement
    vt = _build_vt_statement(analyzed_claims, violations, drift, intent, has_diff)

    return VTGeneratorResult(
        claims=analyzed_claims,
        vt_statement=vt,
        intent=intent,
        violations=violations,
        drift=drift,
        overall_confidence=overall_confidence,
        total_claims=len(analyzed_claims),
        verified_claims=verified,
        unverified_claims=unverified,
    )
