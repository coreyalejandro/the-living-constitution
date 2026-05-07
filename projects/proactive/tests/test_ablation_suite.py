"""Tests for PROACTIVE ablation testing framework."""

import pytest
from research.ablation_config import (
    VariantConfig, VariantName, VARIANTS, get_variant, list_variants,
)
from research.ablation_runner import (
    TestCase, VariantResult, AblationRun, run_variant, run_ablation,
)
from research.ablation_evaluator import (
    VariantMetrics, evaluate_variant, evaluate_all, compare_variants,
)
from research.test_data import FAILURE_CASES, CLEAN_CASES, EDGE_CASES, ALL_CASES


# ---------------------------------------------------------------------------
# Config tests
# ---------------------------------------------------------------------------

class TestVariantConfig:
    def test_four_variants_defined(self):
        assert len(VARIANTS) == 4

    def test_full_variant_has_all_layers(self):
        v = VARIANTS[VariantName.FULL]
        assert v.use_col is True
        assert v.use_contract_window is True
        assert v.use_validator is True
        assert v.use_drift_detector is True

    def test_lite_variant_no_drift(self):
        v = VARIANTS[VariantName.LITE]
        assert v.use_drift_detector is False
        assert "I6" not in v.invariants_enabled

    def test_strict_variant_blocks_warnings(self):
        v = VARIANTS[VariantName.STRICT]
        assert v.block_on_warnings is True

    def test_baseline_has_no_checks(self):
        v = VARIANTS[VariantName.BASELINE]
        assert v.use_col is False
        assert v.use_validator is False
        assert v.use_drift_detector is False
        assert len(v.invariants_enabled) == 0

    def test_full_variant_has_all_invariants(self):
        v = VARIANTS[VariantName.FULL]
        assert v.invariants_enabled == {"I1", "I2", "I3", "I4", "I5", "I6"}

    def test_get_variant_by_name(self):
        v = get_variant(VariantName.FULL)
        assert v.name == VariantName.FULL

    def test_get_variant_unknown_raises(self):
        with pytest.raises(ValueError):
            get_variant("nonexistent")

    def test_list_variants_returns_all(self):
        names = list_variants()
        assert len(names) == 4

    def test_variant_to_dict_roundtrip(self):
        v = VARIANTS[VariantName.FULL]
        d = v.to_dict()
        v2 = VariantConfig.from_dict(d)
        assert v2.name == v.name
        assert v2.use_col == v.use_col

    def test_variant_to_json(self):
        v = VARIANTS[VariantName.FULL]
        j = v.to_json()
        assert "proactive-full" in j


# ---------------------------------------------------------------------------
# Test data tests
# ---------------------------------------------------------------------------

class TestTestData:
    def test_120_total_cases(self):
        assert len(ALL_CASES) == 120

    def test_50_failure_cases(self):
        assert len(FAILURE_CASES) == 50

    def test_50_clean_cases(self):
        assert len(CLEAN_CASES) == 50

    def test_20_edge_cases(self):
        assert len(EDGE_CASES) == 20

    def test_failure_cases_have_failure_class(self):
        for tc in FAILURE_CASES:
            assert tc.failure_class in ("F1", "F2", "F3", "F4", "F5"), f"{tc.id} missing failure_class"

    def test_clean_cases_are_clean(self):
        for tc in CLEAN_CASES:
            assert tc.category == "clean", f"{tc.id} not clean"

    def test_all_cases_have_unique_ids(self):
        ids = [tc.id for tc in ALL_CASES]
        assert len(ids) == len(set(ids)), "Duplicate test case IDs found"

    def test_f1_cases_count(self):
        f1 = [tc for tc in FAILURE_CASES if tc.failure_class == "F1"]
        assert len(f1) == 10

    def test_f2_cases_count(self):
        f2 = [tc for tc in FAILURE_CASES if tc.failure_class == "F2"]
        assert len(f2) == 10


# ---------------------------------------------------------------------------
# Runner tests
# ---------------------------------------------------------------------------

class TestAblationRunner:
    def test_baseline_approves_everything(self):
        config = VARIANTS[VariantName.BASELINE]
        tc = TestCase(id="test-1", description="All tests pass. Fully implemented.", category="failure")
        result = run_variant(config, tc)
        assert result.verdict == "APPROVED"
        assert result.blocked is False

    def test_full_detects_phantom_completion(self):
        config = VARIANTS[VariantName.FULL]
        tc = TestCase(id="test-2", description="All tests pass. Implementation is complete.", category="failure")
        result = run_variant(config, tc)
        assert len(result.violations_found) > 0

    def test_full_detects_absolute_claims(self):
        config = VARIANTS[VariantName.FULL]
        tc = TestCase(id="test-3", description="This is absolutely guaranteed to work.", category="failure")
        result = run_variant(config, tc)
        assert "I1" in result.violations_found

    def test_full_passes_clean_code(self):
        config = VARIANTS[VariantName.FULL]
        tc = TestCase(id="test-4", description="Fixes #100. Updated the login function.", category="clean")
        result = run_variant(config, tc)
        i4 = [v for v in result.violations_found if v == "I4"]
        assert len(i4) == 0  # Has issue reference

    def test_strict_blocks_on_warnings(self):
        config = VARIANTS[VariantName.STRICT]
        tc = TestCase(id="test-5", description="This will definitely probably work.", category="failure")
        result = run_variant(config, tc)
        if result.violations_found:
            assert result.blocked is True

    def test_lite_ignores_i6(self):
        config = VARIANTS[VariantName.LITE]
        tc = TestCase(id="test-6", description="except:\n    pass", category="failure")
        result = run_variant(config, tc)
        assert "I6" not in result.violations_found

    def test_result_has_latency(self):
        config = VARIANTS[VariantName.FULL]
        tc = TestCase(id="test-7", description="Simple test.", category="clean")
        result = run_variant(config, tc)
        assert result.latency_ms >= 0

    def test_run_ablation_returns_all_variants(self):
        cases = [TestCase(id="t1", description="Fixes #1. Simple fix.", category="clean")]
        runs = run_ablation(cases)
        assert len(runs) == 4

    def test_run_ablation_each_run_has_results(self):
        cases = [TestCase(id="t1", description="Fixes #1. Simple fix.", category="clean")]
        runs = run_ablation(cases)
        for run in runs:
            assert len(run.results) == 1


# ---------------------------------------------------------------------------
# Evaluator tests
# ---------------------------------------------------------------------------

class TestAblationEvaluator:
    def _make_run(self, name, results):
        return AblationRun(variant_name=name, results=results)

    def _make_result(self, test_id, verdict, violations=None, blocked=False):
        return VariantResult(
            test_id=test_id, variant_name="test",
            violations_found=violations or [], verdict=verdict,
            blocked=blocked, latency_ms=1.0,
        )

    def test_perfect_detection(self):
        cases = [
            TestCase(id="f1", description="", category="failure"),
            TestCase(id="c1", description="", category="clean"),
        ]
        results = [
            self._make_result("f1", "BLOCKED", ["I2"]),
            self._make_result("c1", "APPROVED"),
        ]
        run = self._make_run("test", results)
        m = evaluate_variant(run, cases)
        assert m.accuracy == 1.0
        assert m.precision == 1.0
        assert m.recall == 1.0

    def test_all_false_negatives(self):
        cases = [
            TestCase(id="f1", description="", category="failure"),
            TestCase(id="f2", description="", category="failure"),
        ]
        results = [
            self._make_result("f1", "APPROVED"),
            self._make_result("f2", "APPROVED"),
        ]
        run = self._make_run("test", results)
        m = evaluate_variant(run, cases)
        assert m.recall == 0.0

    def test_all_false_positives(self):
        cases = [
            TestCase(id="c1", description="", category="clean"),
            TestCase(id="c2", description="", category="clean"),
        ]
        results = [
            self._make_result("c1", "BLOCKED", ["I1"]),
            self._make_result("c2", "FLAGGED", ["I4"]),
        ]
        run = self._make_run("test", results)
        m = evaluate_variant(run, cases)
        assert m.false_positive_rate == 1.0

    def test_evaluate_all_returns_metrics_per_variant(self):
        cases = [TestCase(id="c1", description="", category="clean")]
        runs = [
            self._make_run("v1", [self._make_result("c1", "APPROVED")]),
            self._make_run("v2", [self._make_result("c1", "FLAGGED", ["I1"])]),
        ]
        metrics = evaluate_all(runs, cases)
        assert len(metrics) == 2

    def test_compare_variants_returns_ranking(self):
        m1 = VariantMetrics(variant_name="v1", accuracy=0.9, f1_score=0.85)
        m2 = VariantMetrics(variant_name="v2", accuracy=0.7, f1_score=0.6)
        comparison = compare_variants([m1, m2])
        assert comparison["ranking"][0]["variant"] == "v1"

    def test_compare_empty_returns_empty(self):
        assert compare_variants([]) == {}


# ---------------------------------------------------------------------------
# Integration: full ablation run
# ---------------------------------------------------------------------------

class TestAblationIntegration:
    def test_full_ablation_runs_without_error(self):
        """Run the complete ablation study on all 120 test cases."""
        runs = run_ablation(ALL_CASES)
        assert len(runs) == 4
        for run in runs:
            assert len(run.results) == 120
            assert run.total_time_ms > 0

    def test_full_variant_beats_baseline(self):
        """Full PROACTIVE should detect more failures than baseline."""
        runs = run_ablation(ALL_CASES)
        metrics = evaluate_all(runs, ALL_CASES)
        full = next(m for m in metrics if m.variant_name == VariantName.FULL)
        baseline = next(m for m in metrics if m.variant_name == VariantName.BASELINE)
        assert full.recall > baseline.recall

    def test_baseline_has_zero_recall(self):
        """Baseline should detect nothing."""
        runs = run_ablation(ALL_CASES)
        metrics = evaluate_all(runs, ALL_CASES)
        baseline = next(m for m in metrics if m.variant_name == VariantName.BASELINE)
        assert baseline.recall == 0.0

    def test_strict_blocks_more_than_full(self):
        """Strict should block at least as many as full."""
        runs = run_ablation(ALL_CASES)
        full_run = next(r for r in runs if r.variant_name == VariantName.FULL)
        strict_run = next(r for r in runs if r.variant_name == VariantName.STRICT)
        full_blocked = sum(1 for r in full_run.results if r.blocked)
        strict_blocked = sum(1 for r in strict_run.results if r.blocked)
        assert strict_blocked >= full_blocked
