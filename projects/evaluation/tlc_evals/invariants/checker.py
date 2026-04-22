"""
InvariantChecker — orchestrates all six constitutional invariant checks.

Runs all active invariants against a text and aggregates violations into
a structured report. The checker is the primary entry point for fast,
deterministic constitutional compliance checking without model inference.
"""

from __future__ import annotations

from tlc_evals.core.types import Invariant, InvariantViolation, Severity
from tlc_evals.invariants.i1_evidence_first import EvidenceFirstInvariant
from tlc_evals.invariants.i2_no_phantom_work import NoPhantomWorkInvariant
from tlc_evals.invariants.i3_confidence_verification import ConfidenceVerificationInvariant
from tlc_evals.invariants.i4_traceability import TraceabilityInvariant
from tlc_evals.invariants.i5_safety_over_fluency import SafetyOverFluencyInvariant
from tlc_evals.invariants.i6_fail_closed import FailClosedInvariant


_ALL_INVARIANTS = [
    EvidenceFirstInvariant(),
    NoPhantomWorkInvariant(),
    ConfidenceVerificationInvariant(),
    TraceabilityInvariant(),
    SafetyOverFluencyInvariant(),
    FailClosedInvariant(),
]


class CheckResult:
    """Result from InvariantChecker.check()."""

    def __init__(self, violations: list[InvariantViolation]) -> None:
        self.violations = violations

    @property
    def passed(self) -> bool:
        return all(v.severity != Severity.ERROR for v in self.violations)

    @property
    def error_count(self) -> int:
        return sum(1 for v in self.violations if v.severity == Severity.ERROR)

    @property
    def warning_count(self) -> int:
        return sum(1 for v in self.violations if v.severity == Severity.WARNING)

    @property
    def by_invariant(self) -> dict[Invariant, list[InvariantViolation]]:
        result: dict[Invariant, list[InvariantViolation]] = {}
        for v in self.violations:
            result.setdefault(v.invariant, []).append(v)
        return result

    def __repr__(self) -> str:
        return (
            f"CheckResult(passed={self.passed}, "
            f"errors={self.error_count}, "
            f"warnings={self.warning_count})"
        )


class InvariantChecker:
    """
    Orchestrates all constitutional invariant checks.

    Usage:
        checker = InvariantChecker()
        result = checker.check(agent_output, context={"actual_code": "..."})
        if not result.passed:
            for v in result.violations:
                print(v.invariant.value, v.description)
    """

    def __init__(
        self,
        active_invariants: list[Invariant] | None = None,
    ) -> None:
        if active_invariants:
            self._checkers = [c for c in _ALL_INVARIANTS if c.invariant in active_invariants]
        else:
            self._checkers = list(_ALL_INVARIANTS)

    def check(self, text: str, context: dict | None = None) -> CheckResult:
        """
        Run all active invariant checkers against text.

        Args:
            text: Agent output to check.
            context: Optional context dict (actual_code, filesystem_state,
                     test_run_output, known_issue, etc.)

        Returns:
            CheckResult with all violations aggregated.
        """
        all_violations: list[InvariantViolation] = []
        for checker in self._checkers:
            violations = checker.check(text, context=context)
            all_violations.extend(violations)
        return CheckResult(violations=all_violations)

    def check_invariant(
        self,
        invariant: Invariant,
        text: str,
        context: dict | None = None,
    ) -> list[InvariantViolation]:
        """Check a single invariant against text."""
        for checker in self._checkers:
            if checker.invariant == invariant:
                return checker.check(text, context=context)
        return []
