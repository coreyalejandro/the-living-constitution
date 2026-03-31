/** Subset of root STATUS.json used by the control plane (read-only adapter). */
export type StatusJson = {
  schema_version?: string;
  project?: string;
  governance_contract_version?: string;
  tip_state_truth?: string;
  verification_target?: string;
  head_sha?: string;
  last_verified_commit?: string;
  last_verified_run_id?: string | number;
  escalation_state?: string;
  reviewer_status?: string;
  cross_repo_consistency?: { exit_code?: number; state?: string };
  truth_anchor?: { type?: string; value?: string; commit?: string };
  truth_boundary?: { policy_reference?: string; reason?: string };
  workflow_sha?: string;
  historical_state?: Record<string, unknown>;
  inventory_meta_generated_at_utc?: string;
};
