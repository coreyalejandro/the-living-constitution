/**
 * experiment-schema.ts
 * Type definitions for Contract Window experiments.
 *
 * These types represent the schema that CGL experiments emit.
 * TLC reads these to surface experiment state in the research workbench UI.
 *
 * evidence_basis on all records: CONSTRUCTED — schema derived from CGL proposal structure.
 * No empirical experiments running yet (PENDING empirical validation).
 */

/** I1-I6 invariant identifiers */
export type InvariantId = "I1" | "I2" | "I3" | "I4" | "I5" | "I6";

/** Evidence basis tag required on all output surfaces (I1) */
export type EvidenceBasis = "VERIFIED" | "CONSTRUCTED" | "PENDING";

/** Truth status for a claim */
export interface TruthStatus {
  verified: string[];
  contested: string[];
  unknown: string[];
}

/** A single Contract Window field state */
export interface ContractWindowState {
  task_state: string;
  invariant_status: Record<InvariantId, "active" | "satisfied" | "violated" | "unknown">;
  repair_obligations: string[];
  truth_status: TruthStatus;
}

/** Experiment condition — one arm of a multi-arm study */
export interface ExperimentCondition {
  id: string;
  label: string;
  description: string;
  has_contract_window: boolean;
  session_count: number;
}

/** Registered experiment record */
export interface ExperimentRecord {
  id: string;
  title: string;
  proposal_ref: "Proposal-I" | "Proposal-II" | "Proposal-III";
  research_question: string;
  hypotheses: string[];
  conditions: ExperimentCondition[];
  status: "planned" | "running" | "complete" | "halted";
  evidence_basis: EvidenceBasis;
  registered_at_utc: string;
  cgl_path?: string;
}

/** Session outcome from a completed experiment session */
export interface SessionOutcome {
  session_id: string;
  experiment_id: string;
  condition_id: string;
  intent_drift_score: number | null;
  insight_atrophy_index: number | null;
  bicameral_kappa: number | null;
  contract_window_state: ContractWindowState | null;
  evidence_basis: EvidenceBasis;
  recorded_at_utc: string;
}
