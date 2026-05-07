"""Integration tests for PROACTIVE triage flow.

Tests the end-to-end triage pipeline: fetch context -> validate -> score -> label -> comment.
"""

import pytest
from unittest.mock import Mock, patch

from proactive.severity_scorer import score_severity, LABEL_SAFETY_CRITICAL, LABEL_PHANTOM_WORK, LABEL_PROACTIVE_PASS
from proactive.validator import Violation, check_invariants
from proactive.mr_analyzer import MRContext, MRAnalysisResult, extract_claims
from proactive.report_formatter import format_review_comment


def _make_violation(invariant: str, severity: str = "ERROR") -> Violation:
    return Violation(
        violation_id=f"V-{invariant}-0001",
        invariant=invariant,
        severity=severity,
        location={"file": "test.py", "line": 1},
        message=f"{invariant} violation",
        rule_id=f"{invariant}_test",
    )


class TestTriageFlowCleanCode:
    """Test triage flow with clean code (no violations)."""

    def test_clean_code_gets_pass_label(self):
        result = score_severity([])
        assert LABEL_PROACTIVE_PASS in result.labels

    def test_clean_code_allows_merge(self):
        result = score_severity([])
        assert result.action == "ALLOW"

    def test_clean_code_score_is_zero(self):
        result = score_severity([])
        assert result.score == 0.0


class TestTriageFlowPhantomWork:
    """Test triage flow with phantom completion (F2)."""

    def test_phantom_work_blocks_merge(self):
        violations = [_make_violation("I2", "ERROR")]
        result = score_severity(violations)
        assert result.action == "BLOCK"

    def test_phantom_work_gets_label(self):
        violations = [_make_violation("I2", "ERROR")]
        result = score_severity(violations)
        assert LABEL_PHANTOM_WORK in result.labels

    def test_phantom_work_detected_in_description(self):
        text = "All tests pass. Implementation is complete. Fully implemented."
        violations = check_invariants(text, "MR_DESCRIPTION")
        i2_violations = [v for v in violations if v.invariant == "I2"]
        assert len(i2_violations) > 0


class TestTriageFlowSafetyCritical:
    """Test triage flow with I6 violations."""

    def test_i6_blocks_merge(self):
        violations = [_make_violation("I6", "ERROR")]
        result = score_severity(violations)
        assert result.action == "BLOCK"

    def test_i6_gets_safety_critical_label(self):
        violations = [_make_violation("I6", "ERROR")]
        result = score_severity(violations)
        assert LABEL_SAFETY_CRITICAL in result.labels

    def test_error_suppression_detected(self):
        code = "try:\n    do_something()\nexcept:\n    pass"
        violations = check_invariants(code, "src/main.py")
        i6_violations = [v for v in violations if v.invariant == "I6"]
        assert len(i6_violations) > 0


class TestTriageFlowEpistemicRisk:
    """Test triage flow with I1/I3/I4/I5 violations."""

    def test_untagged_claims_detected(self):
        text = "This function is absolutely guaranteed to work correctly."
        violations = check_invariants(text, "MR_DESCRIPTION")
        i1_violations = [v for v in violations if v.invariant == "I1"]
        assert len(i1_violations) > 0

    def test_missing_traceability_detected(self):
        text = "Fixed the login bug and updated the tests."
        violations = check_invariants(text, "MR_DESCRIPTION")
        i4_violations = [v for v in violations if v.invariant == "I4"]
        assert len(i4_violations) > 0


class TestTriageFlowClaimExtraction:
    """Test claim extraction for triage."""

    def test_extracts_completion_claims(self):
        text = "All tests pass. Implementation is complete."
        claims = extract_claims(text)
        completion_claims = [c for c in claims if c.claim_type == "completion"]
        assert len(completion_claims) > 0

    def test_extracts_security_claims(self):
        text = "This prevents SQL injection attacks."
        claims = extract_claims(text)
        security_claims = [c for c in claims if c.claim_type == "security"]
        assert len(security_claims) > 0

    def test_extracts_performance_claims(self):
        text = "This is 10x faster than the previous implementation."
        claims = extract_claims(text)
        perf_claims = [c for c in claims if c.claim_type == "performance"]
        assert len(perf_claims) > 0


class TestTriageFlowEndToEnd:
    """End-to-end triage flow tests."""

    def test_clean_mr_passes(self):
        text = "Fixes #123. Updated the login function to validate input."
        violations = check_invariants(text, "MR_DESCRIPTION")
        result = score_severity(violations)
        # With issue reference, I4 should pass
        i4_violations = [v for v in violations if v.invariant == "I4"]
        assert len(i4_violations) == 0

    def test_phantom_mr_blocks(self):
        text = "All tests pass. Feature is complete. Fully implemented."
        violations = check_invariants(text, "MR_DESCRIPTION")
        result = score_severity(violations)
        assert result.action == "BLOCK"

    def test_mixed_violations_scored_correctly(self):
        violations = [
            _make_violation("I1", "ERROR"),
            _make_violation("I2", "ERROR"),
            _make_violation("I4", "WARNING"),
            _make_violation("I6", "ERROR"),
        ]
        result = score_severity(violations)
        assert result.action == "BLOCK"
        assert LABEL_SAFETY_CRITICAL in result.labels
        assert LABEL_PHANTOM_WORK in result.labels
        assert result.score > 20.0
