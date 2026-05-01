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
  pattern_only: boolean; // true = no LLM judge, deterministic only
  repo_root: string;
  output_format: "json" | "sarif" | "vt";
}

/**
 * Parses a tlc-evals JSON output file into typed EvalSuiteResult.
 * Does not execute evals — parsing only (safe for server components).
 */
export function parseEvalOutput(raw: unknown): EvalSuiteResult | null {
  if (!raw || typeof raw !== "object") return null;
  const r = raw as Record<string, unknown>;
  if (!r.suite_id || !r.run_id) return null;
  return {
    suite_id: String(r.suite_id),
    run_id: String(r.run_id),
    started_at_utc: String(r.started_at_utc ?? ""),
    completed_at_utc: String(r.completed_at_utc ?? ""),
    total_cases: Number(r.total_cases ?? 0),
    passed: Number(r.passed ?? 0),
    failed: Number(r.failed ?? 0),
    pass_rate: Number(r.pass_rate ?? 0),
    cases: Array.isArray(r.cases) ? (r.cases as EvalCaseResult[]) : [],
    evidence_basis: (r.evidence_basis as EvidenceBasis) ?? "PENDING",
  };
}
