"""
Core type definitions for tlc_evals.

All eval inputs, outputs, and intermediate representations are strongly typed.
Pydantic v2 is used throughout for validation and serialization.
"""

from __future__ import annotations

import uuid
from datetime import datetime, timezone
from enum import Enum
from typing import Any

from pydantic import BaseModel, Field, field_validator


# ---------------------------------------------------------------------------
# Taxonomy enumerations
# ---------------------------------------------------------------------------


class FailureType(str, Enum):
    """Five constitutional failure categories derived from real evidence."""

    F1_CONFIDENT_FALSE_CLAIMS = "F1"
    F2_PHANTOM_COMPLETION = "F2"
    F3_PERSISTENCE_UNDER_CORRECTION = "F3"
    F4_HARM_RISK_COUPLING = "F4"
    F5_CROSS_EPISODE_RECURRENCE = "F5"


class Invariant(str, Enum):
    """Six constitutional invariants that evals enforce."""

    I1_EVIDENCE_FIRST = "I1"
    I2_NO_PHANTOM_WORK = "I2"
    I3_CONFIDENCE_VERIFICATION = "I3"
    I4_TRACEABILITY = "I4"
    I5_SAFETY_OVER_FLUENCY = "I5"
    I6_FAIL_CLOSED = "I6"


class Severity(str, Enum):
    ERROR = "ERROR"
    WARNING = "WARNING"
    INFO = "INFO"
    PASS = "PASS"


class Verdict(str, Enum):
    PASS = "PASS"
    FAIL = "FAIL"
    FLAGGED = "FLAGGED"
    SKIP = "SKIP"
    ERROR = "ERROR"


class GraderType(str, Enum):
    """Which grading mechanism produced this result."""

    PATTERN = "pattern"           # Deterministic regex / heuristic
    MODEL = "model"               # Claude-as-judge
    CONSTITUTIONAL_AI = "cai"     # CAI critique-revision loop
    CALIBRATION = "calibration"   # Confidence calibration probe
    COMPOSITE = "composite"       # Aggregated from multiple graders


# ---------------------------------------------------------------------------
# Eval input/output models
# ---------------------------------------------------------------------------


class EvalCase(BaseModel):
    """
    A single evaluation case: one (input, expected_behavior) pair.

    Mirrors Anthropic's evals format: every case has an `input` that goes
    to the model/system-under-test and an `ideal` that describes correct
    behavior. Additional metadata fields support constitutional grading.
    """

    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    failure_type: FailureType | None = None
    invariants: list[Invariant] = Field(default_factory=list)
    severity: Severity = Severity.ERROR

    # What is presented to the system-under-test
    input: dict[str, Any] = Field(
        description="Free-form input dict. Keys: 'prompt', 'context', 'diff', 'claim', etc."
    )

    # Human-authored description of correct behavior
    ideal: str = Field(
        description="Plain-language description of what a constitutionally-correct response looks like."
    )

    # Optional: ground-truth label for pattern-graded cases
    expected_verdict: Verdict | None = None

    # Provenance
    source_ref: str | None = None
    tags: list[str] = Field(default_factory=list)

    @field_validator("id")
    @classmethod
    def _validate_id(cls, v: str) -> str:
        return v.strip()


class InvariantViolation(BaseModel):
    """A single constitutional invariant violation detected in a response."""

    invariant: Invariant
    description: str
    evidence: str = ""
    severity: Severity = Severity.ERROR
    span: str | None = None  # The exact substring that triggered the violation


class GraderResult(BaseModel):
    """Raw output from a single grader."""

    grader_type: GraderType
    verdict: Verdict
    score: float = Field(ge=0.0, le=1.0, description="Normalized score: 1.0 = perfect pass.")
    reasoning: str = ""
    violations: list[InvariantViolation] = Field(default_factory=list)
    metadata: dict[str, Any] = Field(default_factory=dict)


class EvalResult(BaseModel):
    """
    Complete result for a single EvalCase.

    A result is the aggregation of one or more GraderResults into a final
    verdict with a V&T-compliant evidence chain.
    """

    case_id: str
    eval_name: str
    failure_type: FailureType | None = None

    verdict: Verdict
    severity: Severity
    score: float = Field(ge=0.0, le=1.0)

    # All grader outputs that contributed to this result
    grader_results: list[GraderResult] = Field(default_factory=list)

    # Consolidated violation list
    violations: list[InvariantViolation] = Field(default_factory=list)

    # Human-readable explanation of the verdict
    explanation: str = ""

    # Provenance
    model_id: str | None = None
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    latency_ms: int | None = None

    @property
    def passed(self) -> bool:
        return self.verdict == Verdict.PASS

    @property
    def failed(self) -> bool:
        return self.verdict in (Verdict.FAIL, Verdict.FLAGGED)


class EvalSummary(BaseModel):
    """
    Aggregated summary across all EvalResults in a run.

    This is the top-level artifact emitted by EvalRunner.run().
    """

    run_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    eval_suite_name: str
    model_id: str

    # Counts
    total: int = 0
    passed: int = 0
    failed: int = 0
    flagged: int = 0
    skipped: int = 0
    errors: int = 0

    # Score
    pass_rate: float = 0.0
    mean_score: float = 0.0

    # Breakdown by failure type
    by_failure_type: dict[str, dict[str, int]] = Field(default_factory=dict)

    # Breakdown by invariant
    by_invariant: dict[str, int] = Field(default_factory=dict)

    # All individual results
    results: list[EvalResult] = Field(default_factory=list)

    # Timing
    started_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    completed_at: datetime | None = None
    total_latency_ms: int | None = None

    def compute(self) -> "EvalSummary":
        """Recompute aggregate statistics from results list."""
        self.total = len(self.results)
        self.passed = sum(1 for r in self.results if r.verdict == Verdict.PASS)
        self.failed = sum(1 for r in self.results if r.verdict == Verdict.FAIL)
        self.flagged = sum(1 for r in self.results if r.verdict == Verdict.FLAGGED)
        self.skipped = sum(1 for r in self.results if r.verdict == Verdict.SKIP)
        self.errors = sum(1 for r in self.results if r.verdict == Verdict.ERROR)
        self.pass_rate = self.passed / self.total if self.total > 0 else 0.0
        self.mean_score = (
            sum(r.score for r in self.results) / self.total if self.total > 0 else 0.0
        )

        # Breakdown by failure type
        for r in self.results:
            if r.failure_type:
                key = r.failure_type.value
                bucket = self.by_failure_type.setdefault(key, {"pass": 0, "fail": 0, "flagged": 0})
                if r.verdict == Verdict.PASS:
                    bucket["pass"] += 1
                elif r.verdict == Verdict.FAIL:
                    bucket["fail"] += 1
                elif r.verdict == Verdict.FLAGGED:
                    bucket["flagged"] += 1

        # Breakdown by invariant
        for r in self.results:
            for v in r.violations:
                key = v.invariant.value
                self.by_invariant[key] = self.by_invariant.get(key, 0) + 1

        return self
