"""
PROACTIVE Ablation Evaluator — Metrics Calculation

Calculates evaluation metrics for each variant:
  - Accuracy: % of correct verdicts
  - Precision: % of flagged issues that are real
  - Recall: % of real issues that are flagged
  - False Positive Rate: % of clean cases incorrectly flagged
  - Average Latency: mean time per test case
  - F1 Score: harmonic mean of precision and recall
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List

from research.ablation_runner import AblationRun, TestCase, VariantResult

__all__ = [
    "VariantMetrics",
    "evaluate_variant",
    "evaluate_all",
    "compare_variants",
]


@dataclass
class VariantMetrics:
    """Evaluation metrics for a single variant."""

    variant_name: str
    accuracy: float = 0.0
    precision: float = 0.0
    recall: float = 0.0
    f1_score: float = 0.0
    false_positive_rate: float = 0.0
    true_positive_count: int = 0
    true_negative_count: int = 0
    false_positive_count: int = 0
    false_negative_count: int = 0
    avg_latency_ms: float = 0.0
    total_cases: int = 0
    error_count: int = 0


def _is_correct_detection(result: VariantResult, test_case: TestCase) -> bool:
    """Check if the variant correctly identified the test case."""
    if test_case.category == "clean":
        return result.verdict == "APPROVED" and not result.violations_found
    else:
        return result.verdict in ("BLOCKED", "FLAGGED") and len(result.violations_found) > 0


def evaluate_variant(
    run: AblationRun,
    test_cases: List[TestCase],
) -> VariantMetrics:
    """Calculate metrics for a single variant run.

    Args:
        run: AblationRun with results.
        test_cases: Original test cases (for ground truth).

    Returns:
        VariantMetrics with all calculated metrics.
    """
    tc_map = {tc.id: tc for tc in test_cases}

    tp = fp = tn = fn = 0
    total_latency = 0.0
    errors = 0

    for result in run.results:
        tc = tc_map.get(result.test_id)
        if not tc:
            continue

        if result.error:
            errors += 1
            continue

        total_latency += result.latency_ms
        is_failure_case = tc.category != "clean"
        detected = result.verdict in ("BLOCKED", "FLAGGED") or len(result.violations_found) > 0

        if is_failure_case and detected:
            tp += 1
        elif is_failure_case and not detected:
            fn += 1
        elif not is_failure_case and detected:
            fp += 1
        elif not is_failure_case and not detected:
            tn += 1

    total = tp + fp + tn + fn
    accuracy = (tp + tn) / total if total > 0 else 0.0
    precision = tp / (tp + fp) if (tp + fp) > 0 else 0.0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0.0
    f1 = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0.0
    fpr = fp / (fp + tn) if (fp + tn) > 0 else 0.0
    avg_latency = total_latency / total if total > 0 else 0.0

    return VariantMetrics(
        variant_name=run.variant_name,
        accuracy=round(accuracy, 4),
        precision=round(precision, 4),
        recall=round(recall, 4),
        f1_score=round(f1, 4),
        false_positive_rate=round(fpr, 4),
        true_positive_count=tp,
        true_negative_count=tn,
        false_positive_count=fp,
        false_negative_count=fn,
        avg_latency_ms=round(avg_latency, 2),
        total_cases=total,
        error_count=errors,
    )


def evaluate_all(
    runs: List[AblationRun],
    test_cases: List[TestCase],
) -> List[VariantMetrics]:
    """Evaluate all variant runs."""
    return [evaluate_variant(run, test_cases) for run in runs]


def compare_variants(metrics: List[VariantMetrics]) -> Dict[str, Dict]:
    """Compare variants and produce a summary."""
    if not metrics:
        return {}

    best_accuracy = max(metrics, key=lambda m: m.accuracy)
    best_precision = max(metrics, key=lambda m: m.precision)
    best_recall = max(metrics, key=lambda m: m.recall)
    best_f1 = max(metrics, key=lambda m: m.f1_score)
    lowest_fpr = min(metrics, key=lambda m: m.false_positive_rate)
    fastest = min(metrics, key=lambda m: m.avg_latency_ms)

    return {
        "best_accuracy": {"variant": best_accuracy.variant_name, "value": best_accuracy.accuracy},
        "best_precision": {"variant": best_precision.variant_name, "value": best_precision.precision},
        "best_recall": {"variant": best_recall.variant_name, "value": best_recall.recall},
        "best_f1": {"variant": best_f1.variant_name, "value": best_f1.f1_score},
        "lowest_fpr": {"variant": lowest_fpr.variant_name, "value": lowest_fpr.false_positive_rate},
        "fastest": {"variant": fastest.variant_name, "value": fastest.avg_latency_ms},
        "ranking": [
            {"variant": m.variant_name, "f1": m.f1_score, "accuracy": m.accuracy}
            for m in sorted(metrics, key=lambda m: m.f1_score, reverse=True)
        ],
    }
