#!/usr/bin/env python3
"""
PROACTIVE Ablation Study Runner

Usage:
    python -m research.run_ablation
    python -m research.run_ablation --output results.md
    python -m research.run_ablation --variant proactive-full
"""

import argparse
import json
import sys

from research.ablation_config import VARIANTS, get_variant
from research.ablation_runner import run_ablation
from research.ablation_evaluator import evaluate_all, compare_variants
from research.ablation_report import generate_report
from research.test_data import ALL_CASES


def main() -> int:
    parser = argparse.ArgumentParser(description="Run PROACTIVE ablation study")
    parser.add_argument("--output", "-o", help="Output file for report (default: stdout)")
    parser.add_argument("--variant", "-v", help="Run only a specific variant")
    parser.add_argument("--json", action="store_true", help="Output raw JSON metrics")
    args = parser.parse_args()

    # Select variants
    if args.variant:
        config = get_variant(args.variant)
        variants = {args.variant: config}
    else:
        variants = VARIANTS

    print(f"Running ablation study with {len(variants)} variant(s) and {len(ALL_CASES)} test cases...", file=sys.stderr)

    # Run ablation
    runs = run_ablation(ALL_CASES, variants)

    # Evaluate
    metrics = evaluate_all(runs, ALL_CASES)
    comparison = compare_variants(metrics)

    if args.json:
        output = json.dumps({
            "metrics": [{
                "variant": m.variant_name,
                "accuracy": m.accuracy,
                "precision": m.precision,
                "recall": m.recall,
                "f1_score": m.f1_score,
                "false_positive_rate": m.false_positive_rate,
                "avg_latency_ms": m.avg_latency_ms,
                "tp": m.true_positive_count,
                "tn": m.true_negative_count,
                "fp": m.false_positive_count,
                "fn": m.false_negative_count,
            } for m in metrics],
            "comparison": comparison,
        }, indent=2)
    else:
        output = generate_report(metrics)

    if args.output:
        with open(args.output, "w") as f:
            f.write(output)
        print(f"Report written to {args.output}", file=sys.stderr)
    else:
        print(output)

    # Print summary to stderr
    print("\n=== Summary ===", file=sys.stderr)
    for m in sorted(metrics, key=lambda x: x.f1_score, reverse=True):
        print(f"  {m.variant_name}: F1={m.f1_score:.3f} Acc={m.accuracy:.1%} FPR={m.false_positive_rate:.1%}", file=sys.stderr)

    return 0


if __name__ == "__main__":
    sys.exit(main())
