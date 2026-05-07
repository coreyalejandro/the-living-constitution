"""
PROACTIVE Ablation Runner — Execute Variants Against Test Data

Runs each variant against a set of test MR examples and collects
results for evaluation. Supports parallel execution and error handling.
"""

from __future__ import annotations

import logging
import time
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from proactive.validator import Violation, check_invariants
from proactive.col import compile_intent
from proactive.drift_detector import detect_drift
from research.ablation_config import VariantConfig, VARIANTS

logger = logging.getLogger(__name__)

__all__ = [
    "TestCase",
    "VariantResult",
    "AblationRun",
    "run_variant",
    "run_ablation",
]


@dataclass
class TestCase:
    """A single test MR for ablation testing."""

    id: str
    description: str
    diff: str = ""
    expected_violations: List[str] = field(default_factory=list)
    expected_verdict: str = "APPROVED"
    category: str = "clean"  # clean, failure, edge_case
    failure_class: str = ""  # F1-F5 or empty


@dataclass
class VariantResult:
    """Result of running a single variant on a single test case."""

    test_id: str
    variant_name: str
    violations_found: List[str]
    verdict: str
    blocked: bool
    latency_ms: float
    error: Optional[str] = None


@dataclass
class AblationRun:
    """Complete ablation run results."""

    variant_name: str
    results: List[VariantResult] = field(default_factory=list)
    total_time_ms: float = 0.0


def _filter_violations_by_config(
    violations: List[Violation],
    config: VariantConfig,
) -> List[Violation]:
    """Filter violations based on variant config."""
    return [
        v for v in violations
        if v.invariant in config.invariants_enabled
    ]


def _determine_verdict(
    violations: List[Violation],
    config: VariantConfig,
) -> tuple[str, bool]:
    """Determine verdict and block status based on variant config."""
    if not violations:
        return "APPROVED", False

    has_errors = any(v.severity == "ERROR" for v in violations)
    has_warnings = any(v.severity == "WARNING" for v in violations)

    if config.block_on_errors and has_errors:
        return "BLOCKED", True
    if config.block_on_warnings and has_warnings:
        return "BLOCKED", True
    if has_errors or has_warnings:
        return "FLAGGED", False
    return "APPROVED", False


def run_variant(
    config: VariantConfig,
    test_case: TestCase,
) -> VariantResult:
    """Run a single variant against a single test case.

    Args:
        config: Variant configuration.
        test_case: Test case to evaluate.

    Returns:
        VariantResult with violations, verdict, and timing.
    """
    start = time.monotonic()

    try:
        # Baseline: no checks
        if not config.use_validator:
            latency = (time.monotonic() - start) * 1000
            return VariantResult(
                test_id=test_case.id,
                variant_name=config.name,
                violations_found=[],
                verdict="APPROVED",
                blocked=False,
                latency_ms=round(latency, 2),
            )

        # Run validator (regex-only for ablation, no LLM)
        all_violations: List[Violation] = []

        # COL layer
        intent_dict = None
        if config.use_col:
            receipt = compile_intent(test_case.description)
            intent_dict = {
                "action": receipt.parsed_intent.action,
                "target": receipt.parsed_intent.target,
                "scope": receipt.parsed_intent.scope,
                "goal": receipt.parsed_intent.goal,
                "constraints": receipt.parsed_intent.constraints,
                "ambiguities": receipt.parsed_intent.ambiguities,
            }

        # Validator layer
        violations = check_invariants(
            test_case.description,
            "MR_DESCRIPTION",
            intent=intent_dict,
        )
        filtered = _filter_violations_by_config(violations, config)
        all_violations.extend(filtered)

        # Drift detector layer
        if config.use_drift_detector and config.use_col and test_case.diff:
            receipt = compile_intent(test_case.description)
            drift = detect_drift(receipt, test_case.diff)
            if drift.has_drift:
                all_violations.append(Violation(
                    violation_id="V-DRIFT-0001",
                    invariant="I5",
                    severity="WARNING",
                    location={"file": "DRIFT", "line": 0},
                    message=f"Drift detected: {drift.suggestion}",
                    rule_id="drift_detected",
                ))

        verdict, blocked = _determine_verdict(all_violations, config)
        latency = (time.monotonic() - start) * 1000

        return VariantResult(
            test_id=test_case.id,
            variant_name=config.name,
            violations_found=[v.invariant for v in all_violations],
            verdict=verdict,
            blocked=blocked,
            latency_ms=round(latency, 2),
        )

    except Exception as e:
        latency = (time.monotonic() - start) * 1000
        logger.error("Variant %s failed on %s: %s", config.name, test_case.id, e)
        return VariantResult(
            test_id=test_case.id,
            variant_name=config.name,
            violations_found=[],
            verdict="ERROR",
            blocked=False,
            latency_ms=round(latency, 2),
            error=str(e),
        )


def run_ablation(
    test_cases: List[TestCase],
    variants: Optional[Dict[str, VariantConfig]] = None,
) -> List[AblationRun]:
    """Run all variants against all test cases.

    Args:
        test_cases: List of test cases to evaluate.
        variants: Optional dict of variants. Defaults to all VARIANTS.

    Returns:
        List of AblationRun results, one per variant.
    """
    if variants is None:
        variants = VARIANTS

    runs = []
    for name, config in variants.items():
        logger.info("Running variant: %s (%d test cases)", name, len(test_cases))
        start = time.monotonic()

        results = []
        for tc in test_cases:
            result = run_variant(config, tc)
            results.append(result)

        total_time = (time.monotonic() - start) * 1000
        runs.append(AblationRun(
            variant_name=name,
            results=results,
            total_time_ms=round(total_time, 2),
        ))

    return runs
