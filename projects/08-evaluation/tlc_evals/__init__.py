"""
tlc_evals — Automated evaluation library for The Living Constitution.

Built on Anthropic's Constitutional AI methodology and Claude-as-judge grading.
Evaluates epistemic safety, constitutional invariant compliance, and failure
taxonomy detection across AI agent interactions.

Usage:
    from tlc_evals import EvalRunner, EvalSuite
    from tlc_evals.evals import PhantomCompletionEval, ConfidentFalseClaimsEval
    from tlc_evals.invariants import EvidenceFirstInvariant

    runner = EvalRunner()
    suite = EvalSuite.from_yaml("eval_specs/f2_suite.yaml")
    results = await runner.run(suite)
"""

from tlc_evals._version import __version__
from tlc_evals.core.runner import EvalRunner
from tlc_evals.core.types import (
    EvalCase,
    EvalResult,
    EvalSummary,
    FailureType,
    InvariantViolation,
    Severity,
    Verdict,
)
from tlc_evals.evals.suite import EvalSuite

__all__ = [
    "__version__",
    "EvalRunner",
    "EvalSuite",
    "EvalCase",
    "EvalResult",
    "EvalSummary",
    "FailureType",
    "InvariantViolation",
    "Severity",
    "Verdict",
]
