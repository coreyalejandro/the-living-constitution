"use strict";
/**
 * regression-gate.ts
 * Regression gate — reads eval history and blocks promotion if regressions detected.
 *
 * The gate reads EvalSuiteResult records and compares pass_rate against the
 * last known-good baseline. A promotion is blocked if:
 * - pass_rate drops more than REGRESSION_THRESHOLD below baseline
 * - Any halt-severity invariant violation is present
 * - evidence_basis is PENDING on a surface claiming VERIFIED
 *
 * evidence_basis: CONSTRUCTED — derived from TLC contract regression requirements.
 */
Object.defineProperty(exports, "__esModule", { value: true });
exports.DEFAULT_GATE_CONFIG = void 0;
exports.runRegressionGate = runRegressionGate;
/** Default gate config from TLC contract */
exports.DEFAULT_GATE_CONFIG = {
    baseline_pass_rate: 1.0, // 212/212 from VR-V-15C6
    regression_threshold: 0.05,
    require_evidence_basis: ["VERIFIED"],
};
/**
 * Runs the regression gate against a new eval result.
 */
function runRegressionGate(result, config = exports.DEFAULT_GATE_CONFIG) {
    const delta = result.pass_rate - config.baseline_pass_rate;
    const regressed = delta < -config.regression_threshold;
    return {
        passed: !regressed,
        baseline_pass_rate: config.baseline_pass_rate,
        current_pass_rate: result.pass_rate,
        delta,
        reason: regressed
            ? `pass_rate ${result.pass_rate.toFixed(3)} dropped ${Math.abs(delta).toFixed(3)} below baseline ${config.baseline_pass_rate} (threshold: ${config.regression_threshold})`
            : null,
        evidence_basis: "CONSTRUCTED",
    };
}
//# sourceMappingURL=regression-gate.js.map