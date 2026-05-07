"""
PROACTIVE Severity Scorer — Violation-to-Label Mapping

Scores MR analysis results by severity and maps them to GitLab labels.
Used by the triage flow to automatically classify merge requests.

Scoring Rules:
  I6 violations (Fail Closed)       → safety-critical  (score 10)
  I2 violations (Phantom Work)      → phantom-work     (score 7)
  I1/I3/I4/I5 violations            → epistemic-risk   (score 5-8)
  No violations                     → (none)           (score 0)
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from typing import List, Optional

from proactive.validator import Violation

logger = logging.getLogger(__name__)

__all__ = [
    "SeverityResult",
    "LABEL_SAFETY_CRITICAL",
    "LABEL_EPISTEMIC_RISK",
    "LABEL_PHANTOM_WORK",
    "LABEL_PROACTIVE_PASS",
    "score_severity",
]

# ---------------------------------------------------------------------------
# Label constants
# ---------------------------------------------------------------------------

LABEL_SAFETY_CRITICAL = "safety-critical"
LABEL_EPISTEMIC_RISK = "epistemic-risk"
LABEL_PHANTOM_WORK = "phantom-work"
LABEL_PROACTIVE_PASS = "proactive-pass"

# ---------------------------------------------------------------------------
# Invariant weights
# ---------------------------------------------------------------------------

_INVARIANT_WEIGHTS = {
    "I1": 5,   # Evidence-First
    "I2": 7,   # No Phantom Work
    "I3": 6,   # Confidence-Verification
    "I4": 5,   # Traceability
    "I5": 5,   # Safety Over Fluency
    "I6": 10,  # Fail Closed
}

_SEVERITY_MULTIPLIER = {
    "ERROR": 1.0,
    "WARNING": 0.5,
}


# ---------------------------------------------------------------------------
# Dataclass
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class SeverityResult:
    """Result of severity scoring for an MR."""

    score: float
    labels: List[str]
    action: str           # "BLOCK", "WARN", "ALLOW"
    summary: str
    violation_counts: dict = field(default_factory=dict)


# ---------------------------------------------------------------------------
# Scoring logic
# ---------------------------------------------------------------------------

def _compute_score(violations: List[Violation]) -> float:
    """Compute a weighted severity score from violations."""
    total = 0.0
    for v in violations:
        base = _INVARIANT_WEIGHTS.get(v.invariant, 5)
        multiplier = _SEVERITY_MULTIPLIER.get(v.severity, 0.5)
        total += base * multiplier
    return round(total, 2)


def _determine_labels(violations: List[Violation]) -> List[str]:
    """Determine which labels to assign based on violations."""
    if not violations:
        return [LABEL_PROACTIVE_PASS]

    labels = []
    invariants_hit = {v.invariant for v in violations}
    severities_hit = {v.severity for v in violations}

    # I6 violations are always safety-critical
    if "I6" in invariants_hit:
        labels.append(LABEL_SAFETY_CRITICAL)

    # I2 violations with ERROR severity indicate phantom work
    i2_errors = [v for v in violations if v.invariant == "I2" and v.severity == "ERROR"]
    if i2_errors:
        labels.append(LABEL_PHANTOM_WORK)

    # Any other violations indicate epistemic risk
    other_invariants = invariants_hit - {"I6", "I2"}
    if other_invariants or ("I2" in invariants_hit and not i2_errors):
        labels.append(LABEL_EPISTEMIC_RISK)

    # If we only have warnings and no specific labels yet, add epistemic-risk
    if not labels and "WARNING" in severities_hit:
        labels.append(LABEL_EPISTEMIC_RISK)

    return labels if labels else [LABEL_PROACTIVE_PASS]


def _determine_action(violations: List[Violation]) -> str:
    """Determine merge action based on violations."""
    if not violations:
        return "ALLOW"

    has_errors = any(v.severity == "ERROR" for v in violations)
    has_i6 = any(v.invariant == "I6" for v in violations)

    if has_i6 or has_errors:
        return "BLOCK"
    return "WARN"


def _count_violations(violations: List[Violation]) -> dict:
    """Count violations by invariant."""
    counts: dict = {}
    for v in violations:
        key = f"{v.invariant}_{v.severity}"
        counts[key] = counts.get(key, 0) + 1
    return counts


def _build_summary(violations: List[Violation], labels: List[str], action: str) -> str:
    """Build a human-readable summary of the severity assessment."""
    if not violations:
        return "No violations detected. MR is safe to merge."

    error_count = sum(1 for v in violations if v.severity == "ERROR")
    warning_count = sum(1 for v in violations if v.severity == "WARNING")
    invariants = sorted({v.invariant for v in violations})

    parts = []
    if error_count:
        parts.append(f"{error_count} error(s)")
    if warning_count:
        parts.append(f"{warning_count} warning(s)")

    label_str = ", ".join(labels)
    inv_str = ", ".join(invariants)

    return (
        f"Found {' and '.join(parts)} across invariants [{inv_str}]. "
        f"Labels: [{label_str}]. Action: {action}."
    )


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def score_severity(violations: List[Violation]) -> SeverityResult:
    """Score the severity of violations and determine labels and action.

    Args:
        violations: List of Violation objects from the validator.

    Returns:
        SeverityResult with score, labels, action, and summary.
    """
    score = _compute_score(violations)
    labels = _determine_labels(violations)
    action = _determine_action(violations)
    counts = _count_violations(violations)
    summary = _build_summary(violations, labels, action)

    logger.info(
        "Severity scored: %.2f, labels=%s, action=%s",
        score, labels, action,
    )

    return SeverityResult(
        score=score,
        labels=labels,
        action=action,
        summary=summary,
        violation_counts=counts,
    )
