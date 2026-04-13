"""
EvalRunner — orchestrates eval suite execution.

The runner is the top-level orchestration layer. It accepts an EvalSuite
and a "system" (a callable or string that maps EvalCase → agent output),
runs all graders, and returns an EvalSummary.

Execution modes:
  - Sequential: safe, predictable, suitable for debugging
  - Concurrent: asyncio gather for large suites
  - Batch: Anthropic Message Batches API for maximum throughput

The runner is intentionally system-agnostic: the "system under test" can
be a live API call, a cached response, a mock, or a hardcoded string.
"""

from __future__ import annotations

import asyncio
import time
from collections.abc import Callable
from datetime import datetime, timezone
from typing import Any

from tlc_evals.core.types import (
    EvalCase,
    EvalResult,
    EvalSummary,
    Severity,
    Verdict,
)
from tlc_evals.evals.base import BaseEval
from tlc_evals.evals.suite import EvalSuite

# Type alias: anything that turns an EvalCase into an agent output string
SystemCallable = Callable[[EvalCase], str]
AsyncSystemCallable = Callable[[EvalCase], Any]  # must return Awaitable[str]


class EvalRunner:
    """
    Orchestrates eval suite execution with configurable grading strategy.

    Quick start:
        runner = EvalRunner()
        suite = EvalSuite.from_evals(ConfidentFalseClaimsEval(), PhantomCompletionEval())
        summary = runner.run(suite, system=my_agent_fn)

    The `system` argument is a callable that receives an EvalCase and returns
    the agent output string to grade. If omitted, the runner uses the
    `agent_output` field from case.input (for offline/replay grading).
    """

    def __init__(
        self,
        eval_classes: list[BaseEval] | None = None,
        max_concurrency: int = 5,
        fail_fast: bool = False,
    ) -> None:
        self._eval_classes = eval_classes or []
        self.max_concurrency = max_concurrency
        self.fail_fast = fail_fast

    # ------------------------------------------------------------------
    # Synchronous run (sequential)
    # ------------------------------------------------------------------

    def run(
        self,
        suite: EvalSuite,
        system: SystemCallable | None = None,
    ) -> EvalSummary:
        """
        Run all cases in a suite sequentially.

        If `system` is None, uses case.input['agent_output'] as the response.
        """
        started_at = datetime.now(timezone.utc)
        t0 = time.monotonic()

        results: list[EvalResult] = []

        # Resolve which BaseEval instance handles each case
        eval_map = _build_eval_map(self._eval_classes)

        for case in suite.cases:
            agent_output = _resolve_output(case, system)
            eval_instance = eval_map.get(case.failure_type)

            if eval_instance is None:
                # No registered eval for this failure type — use base pattern grader
                from tlc_evals.evals.base import BaseEval as _BE
                from tlc_evals.graders.pattern_grader import PatternGrader
                pattern_result = PatternGrader().grade(case, agent_output)
                result = EvalResult(
                    case_id=case.id,
                    eval_name="pattern_only",
                    failure_type=case.failure_type,
                    verdict=pattern_result.verdict,
                    severity=pattern_result.violations[0].severity
                    if pattern_result.violations
                    else Severity.PASS,
                    score=pattern_result.score,
                    grader_results=[pattern_result],
                    violations=pattern_result.violations,
                    explanation=pattern_result.reasoning,
                )
            else:
                result = eval_instance.grade_case(case, agent_output)

            results.append(result)

            if self.fail_fast and result.failed:
                break

        total_ms = int((time.monotonic() - t0) * 1000)
        return _build_summary(
            suite_name=suite.name,
            results=results,
            started_at=started_at,
            total_ms=total_ms,
        )

    # ------------------------------------------------------------------
    # Async run (concurrent)
    # ------------------------------------------------------------------

    async def arun(
        self,
        suite: EvalSuite,
        system: AsyncSystemCallable | None = None,
    ) -> EvalSummary:
        """
        Run all cases concurrently using asyncio.gather with semaphore control.
        """
        started_at = datetime.now(timezone.utc)
        t0 = time.monotonic()

        semaphore = asyncio.Semaphore(self.max_concurrency)
        eval_map = _build_eval_map(self._eval_classes)

        async def _grade_case(case: EvalCase) -> EvalResult:
            async with semaphore:
                if system is not None:
                    output = await system(case)
                else:
                    output = _resolve_output(case, None)

                eval_instance = eval_map.get(case.failure_type)
                if eval_instance:
                    return await eval_instance.agrade_case(case, output)
                else:
                    from tlc_evals.graders.pattern_grader import PatternGrader
                    pattern_result = PatternGrader().grade(case, output)
                    return EvalResult(
                        case_id=case.id,
                        eval_name="pattern_only",
                        failure_type=case.failure_type,
                        verdict=pattern_result.verdict,
                        severity=pattern_result.violations[0].severity
                        if pattern_result.violations
                        else Severity.PASS,
                        score=pattern_result.score,
                        grader_results=[pattern_result],
                        violations=pattern_result.violations,
                        explanation=pattern_result.reasoning,
                    )

        tasks = [_grade_case(case) for case in suite.cases]
        results: list[EvalResult] = await asyncio.gather(*tasks, return_exceptions=False)

        total_ms = int((time.monotonic() - t0) * 1000)
        return _build_summary(
            suite_name=suite.name,
            results=list(results),
            started_at=started_at,
            total_ms=total_ms,
        )

    def run_async(self, suite: EvalSuite, system: Any = None) -> EvalSummary:
        """Convenience wrapper to run async from sync context."""
        return asyncio.run(self.arun(suite, system))

    # ------------------------------------------------------------------
    # Full suite run: all failure types
    # ------------------------------------------------------------------

    def run_full_suite(
        self,
        system: SystemCallable | None = None,
        model_graded: bool = True,
    ) -> EvalSummary:
        """
        Run the complete TLC evaluation suite (all F1–F5 evaluators).

        This is the canonical 'run everything' entry point.
        """
        from tlc_evals.evals.f1_confident_false_claims import ConfidentFalseClaimsEval
        from tlc_evals.evals.f2_phantom_completion import PhantomCompletionEval
        from tlc_evals.evals.f3_persistence_under_correction import PersistenceUnderCorrectionEval
        from tlc_evals.evals.f4_harm_risk_coupling import HarmRiskCouplingEval
        from tlc_evals.evals.f5_cross_episode_recurrence import CrossEpisodeRecurrenceEval

        all_evals = [
            ConfidentFalseClaimsEval(use_model_grader=model_graded),
            PhantomCompletionEval(use_model_grader=model_graded),
            PersistenceUnderCorrectionEval(use_model_grader=model_graded),
            HarmRiskCouplingEval(use_model_grader=model_graded),
            CrossEpisodeRecurrenceEval(use_model_grader=model_graded),
        ]

        suite = EvalSuite.from_evals(*all_evals, name="tlc_full_suite")
        runner = EvalRunner(eval_classes=all_evals)
        return runner.run(suite, system=system)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _build_eval_map(eval_classes: list[BaseEval]) -> dict:
    """Map FailureType → BaseEval instance."""
    return {ev.failure_type: ev for ev in eval_classes if ev.failure_type is not None}


def _resolve_output(case: EvalCase, system: SystemCallable | None) -> str:
    """Get agent output: call system if provided, else extract from case.input."""
    if system is not None:
        return str(system(case))
    return (
        case.input.get("agent_output")
        or case.input.get("post_correction_output")
        or case.input.get("prompt", "")
    )


def _build_summary(
    suite_name: str,
    results: list[EvalResult],
    started_at: datetime,
    total_ms: int,
) -> EvalSummary:
    # Attempt to get model_id from first model-graded result
    model_id = "unknown"
    for r in results:
        if r.model_id:
            model_id = r.model_id
            break

    summary = EvalSummary(
        eval_suite_name=suite_name,
        model_id=model_id,
        results=results,
        started_at=started_at,
        completed_at=datetime.now(timezone.utc),
        total_latency_ms=total_ms,
    )
    return summary.compute()
