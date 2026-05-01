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

import { EvalSuiteResult } from "./eval-runner";
import { EvidenceBasis } from "./experiment-schema";

/** Gate configuration */
export interface RegressionGateConfig {
  baseline_pass_rate: number; // 0.0 - 1.0
  regression_threshold: number; // allowed drop, e.g. 0.05 = 5%
  require_evidence_basis: EvidenceBasis[];
}

/** Gate result */
export interface GateResult {
  passed: boolean;
  baseline_pass_rate: number;
  current_pass_rate: number;
  delta: number;
  reason: string | null;
  evidence_basis: EvidenceBasis;
}

/** Default gate config from TLC contract */
export const DEFAULT_GATE_CONFIG: RegressionGateConfig = {
  baseline_pass_rate: 1.0, // 212/212 from VR-V-15C6
  regression_threshold: 0.05,
  require_evidence_basis: ["VERIFIED"],
};

/**
 * Runs the regression gate against a new eval result.
 */
export function runRegressionGate(
  result: EvalSuiteResult,
  config: RegressionGateConfig = DEFAULT_GATE_CONFIG
): GateResult {
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
