"""Tests for PROACTIVE severity scorer."""

import pytest
from proactive.severity_scorer import (
    SeverityResult,
    LABEL_SAFETY_CRITICAL,
    LABEL_EPISTEMIC_RISK,
    LABEL_PHANTOM_WORK,
    LABEL_PROACTIVE_PASS,
    score_severity,
)
from proactive.validator import Violation


def _make_violation(invariant: str, severity: str = "ERROR", message: str = "test") -> Violation:
    return Violation(
        violation_id=f"V-{invariant}-0001-TEST",
        invariant=invariant,
        severity=severity,
        location={"file": "test.py", "line": 1},
        message=message,
        rule_id=f"{invariant}_test",
    )


class TestScoreSeverityNoViolations:
    def test_no_violations_returns_pass(self):
        result = score_severity([])
        assert result.action == "ALLOW"
        assert LABEL_PROACTIVE_PASS in result.labels
        assert result.score == 0.0

    def test_no_violations_summary(self):
        result = score_severity([])
        assert "No violations" in result.summary


class TestScoreSeverityI6:
    def test_i6_error_blocks_merge(self):
        violations = [_make_violation("I6", "ERROR")]
        result = score_severity(violations)
        assert result.action == "BLOCK"
        assert LABEL_SAFETY_CRITICAL in result.labels

    def test_i6_has_highest_score(self):
        violations = [_make_violation("I6", "ERROR")]
        result = score_severity(violations)
        assert result.score >= 10.0

    def test_i6_warning_still_labels(self):
        violations = [_make_violation("I6", "WARNING")]
        result = score_severity(violations)
        assert LABEL_SAFETY_CRITICAL in result.labels


class TestScoreSeverityI2:
    def test_i2_error_labels_phantom_work(self):
        violations = [_make_violation("I2", "ERROR")]
        result = score_severity(violations)
        assert LABEL_PHANTOM_WORK in result.labels

    def test_i2_error_blocks_merge(self):
        violations = [_make_violation("I2", "ERROR")]
        result = score_severity(violations)
        assert result.action == "BLOCK"

    def test_i2_warning_labels_epistemic_risk(self):
        violations = [_make_violation("I2", "WARNING")]
        result = score_severity(violations)
        assert LABEL_EPISTEMIC_RISK in result.labels


class TestScoreSeverityI1I3I4I5:
    def test_i1_error_labels_epistemic_risk(self):
        violations = [_make_violation("I1", "ERROR")]
        result = score_severity(violations)
        assert LABEL_EPISTEMIC_RISK in result.labels

    def test_i3_warning_labels_epistemic_risk(self):
        violations = [_make_violation("I3", "WARNING")]
        result = score_severity(violations)
        assert LABEL_EPISTEMIC_RISK in result.labels

    def test_i4_warning_warns(self):
        violations = [_make_violation("I4", "WARNING")]
        result = score_severity(violations)
        assert result.action == "WARN"

    def test_i5_warning_labels_epistemic_risk(self):
        violations = [_make_violation("I5", "WARNING")]
        result = score_severity(violations)
        assert LABEL_EPISTEMIC_RISK in result.labels


class TestScoreSeverityMultiple:
    def test_multiple_violations_accumulate_score(self):
        violations = [
            _make_violation("I1", "ERROR"),
            _make_violation("I2", "ERROR"),
            _make_violation("I4", "WARNING"),
        ]
        result = score_severity(violations)
        assert result.score > 10.0

    def test_i6_plus_i2_gets_both_labels(self):
        violations = [
            _make_violation("I6", "ERROR"),
            _make_violation("I2", "ERROR"),
        ]
        result = score_severity(violations)
        assert LABEL_SAFETY_CRITICAL in result.labels
        assert LABEL_PHANTOM_WORK in result.labels

    def test_all_invariants_violated(self):
        violations = [
            _make_violation("I1", "ERROR"),
            _make_violation("I2", "ERROR"),
            _make_violation("I3", "WARNING"),
            _make_violation("I4", "WARNING"),
            _make_violation("I5", "WARNING"),
            _make_violation("I6", "ERROR"),
        ]
        result = score_severity(violations)
        assert result.action == "BLOCK"
        assert LABEL_SAFETY_CRITICAL in result.labels
        assert LABEL_PHANTOM_WORK in result.labels
        assert LABEL_EPISTEMIC_RISK in result.labels


class TestScoreSeverityViolationCounts:
    def test_counts_by_invariant_and_severity(self):
        violations = [
            _make_violation("I1", "ERROR"),
            _make_violation("I1", "WARNING"),
            _make_violation("I2", "ERROR"),
        ]
        result = score_severity(violations)
        assert result.violation_counts.get("I1_ERROR") == 1
        assert result.violation_counts.get("I1_WARNING") == 1
        assert result.violation_counts.get("I2_ERROR") == 1


class TestScoreSeveritySummary:
    def test_summary_includes_action(self):
        violations = [_make_violation("I6", "ERROR")]
        result = score_severity(violations)
        assert "BLOCK" in result.summary

    def test_summary_includes_labels(self):
        violations = [_make_violation("I2", "ERROR")]
        result = score_severity(violations)
        assert "phantom-work" in result.summary

    def test_summary_includes_counts(self):
        violations = [
            _make_violation("I1", "ERROR"),
            _make_violation("I4", "WARNING"),
        ]
        result = score_severity(violations)
        assert "1 error" in result.summary
        assert "1 warning" in result.summary
