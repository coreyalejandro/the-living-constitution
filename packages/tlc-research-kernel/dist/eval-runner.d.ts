/**
 * eval-runner.ts
 * Eval runner interface for TLC research workbench.
 *
 * Wraps the Python tlc_evals library (projects/evaluation/tlc_evals/)
 * and exposes results as typed objects for the Next.js control plane.
 *
 * evidence_basis: CONSTRUCTED — interface derived from tlc_evals CLI structure.
 */
import { EvidenceBasis } from "./experiment-schema";
/** Single eval case result */
export interface EvalCaseResult {
    case_id: string;
    suite_id: string;
    passed: boolean;
    score: number | null;
    invariant_violations: string[];
    notes: string;
    evidence_basis: EvidenceBasis;
}
/** Summary of a full eval suite run */
export interface EvalSuiteResult {
    suite_id: string;
    run_id: string;
    started_at_utc: string;
    completed_at_utc: string;
    total_cases: number;
    passed: number;
    failed: number;
    pass_rate: number;
    cases: EvalCaseResult[];
    evidence_basis: EvidenceBasis;
}
/** Eval runner configuration */
export interface EvalRunnerConfig {
    suite_ids: string[];
    pattern_only: boolean;
    repo_root: string;
    output_format: "json" | "sarif" | "vt";
}
/**
 * Parses a tlc-evals JSON output file into typed EvalSuiteResult.
 * Does not execute evals — parsing only (safe for server components).
 */
export declare function parseEvalOutput(raw: unknown): EvalSuiteResult | null;
//# sourceMappingURL=eval-runner.d.ts.map