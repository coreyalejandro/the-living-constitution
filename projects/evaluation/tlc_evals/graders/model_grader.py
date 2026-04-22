"""
Model Grader — Claude-as-judge grading.

Thin adapter that delegates to ConstitutionalJudge and returns a GraderResult.
This module is the primary interface for model-graded evals.
"""

from __future__ import annotations

from tlc_evals.core.judge import ConstitutionalJudge
from tlc_evals.core.sampler import ModelSampler
from tlc_evals.core.types import EvalCase, GraderResult, Invariant, FailureType


class ModelGrader:
    """
    Grades agent outputs using Claude as the constitutional judge.

    This is Anthropic's canonical LLM-as-judge pattern, applied to
    constitutional invariant evaluation. The judge model is always
    claude-opus (most capable) for grading accuracy.
    """

    def __init__(self, sampler: ModelSampler | None = None) -> None:
        self._judge = ConstitutionalJudge(sampler=sampler)

    def grade(
        self,
        case: EvalCase,
        agent_output: str,
        invariants: list[Invariant] | None = None,
        failure_types: list[FailureType] | None = None,
    ) -> GraderResult:
        return self._judge.grade(
            case=case,
            agent_output=agent_output,
            invariants_to_check=invariants,
            failure_types_to_check=failure_types,
        )

    async def agrade(
        self,
        case: EvalCase,
        agent_output: str,
        invariants: list[Invariant] | None = None,
        failure_types: list[FailureType] | None = None,
    ) -> GraderResult:
        return await self._judge.agrade(
            case=case,
            agent_output=agent_output,
            invariants_to_check=invariants,
            failure_types_to_check=failure_types,
        )
