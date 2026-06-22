"use strict";
/**
 * eval-runner.ts
 * Eval runner interface for TLC research workbench.
 *
 * Wraps the Python tlc_evals library (projects/evaluation/tlc_evals/)
 * and exposes results as typed objects for the Next.js control plane.
 *
 * evidence_basis: CONSTRUCTED — interface derived from tlc_evals CLI structure.
 */
Object.defineProperty(exports, "__esModule", { value: true });
exports.parseEvalOutput = parseEvalOutput;
/**
 * Parses a tlc-evals JSON output file into typed EvalSuiteResult.
 * Does not execute evals — parsing only (safe for server components).
 */
function parseEvalOutput(raw) {
    if (!raw || typeof raw !== "object")
        return null;
    const r = raw;
    if (!r.suite_id || !r.run_id)
        return null;
    return {
        suite_id: String(r.suite_id),
        run_id: String(r.run_id),
        started_at_utc: String(r.started_at_utc ?? ""),
        completed_at_utc: String(r.completed_at_utc ?? ""),
        total_cases: Number(r.total_cases ?? 0),
        passed: Number(r.passed ?? 0),
        failed: Number(r.failed ?? 0),
        pass_rate: Number(r.pass_rate ?? 0),
        cases: Array.isArray(r.cases) ? r.cases : [],
        evidence_basis: r.evidence_basis ?? "PENDING",
    };
}
//# sourceMappingURL=eval-runner.js.map