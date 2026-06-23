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
    baseline_pass_rate: number;
    regression_threshold: number;
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
export declare const DEFAULT_GATE_CONFIG: RegressionGateConfig;
/**
 * Runs the regression gate against a new eval result.
 */
export declare function runRegressionGate(result: EvalSuiteResult, config?: RegressionGateConfig): GateResult;
//# sourceMappingURL=regression-gate.d.ts.map