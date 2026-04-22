/**
 * Fallback snapshot and static lists used when repo root cannot be resolved or
 * files are unreadable. Prefer `lib/adapters/status-json-adapter` live read of
 * STATUS.json when the app runs with the monorepo root discoverable.
 */
export const TLC_STATUS_SNAPSHOT = {
  project: "coreyalejandro/the-living-constitution",
  schema_version: "1.1.0",
  governance_contract_version: "v1.9.0",
  tip_state_truth: "tip_pending",
  verification_target: "e56fc0753955901ee18bca44ae73181f9999b9db",
  truth_anchor: {
    type: "git_tag",
    value: "tlc-gov-verified-e56fc07",
    commit: "e56fc0753955901ee18bca44ae73181f9999b9db",
  },
  head_sha: "6d0f565ba2b313fd640a1e854618e6bac9993421",
  last_verified_commit: "30805eed1d51ca78107294376c1b783275e484aa",
  last_verified_run_id: "23774310879",
  escalation_state: "review_required",
  reviewer_status: "pending",
  truth_boundary_policy:
    "verification/closed-epistemics-open-interfaces-policy.json",
} as const;

export const VERIFICATION_STREAM_ENTRIES = [
  {
    id: "local-matrix",
    label: "Verification matrix",
    path: "verification/MATRIX.md",
  },
  {
    id: "governance-chain",
    label: "Governance chain verifier",
    path: "scripts/verify_governance_chain.py",
  },
  {
    id: "ci-record",
    label: "Remote CI evidence record",
    path: "verification/ci-remote-evidence/record.json",
  },
] as const;

export const SYSTEM_GRAPH_NODES = [
  { id: "projects", label: "projects/", kind: "overlay" },
  { id: "verification", label: "verification/", kind: "evidence" },
  { id: "constitution", label: "governance/constitution/core/", kind: "law" },
  { id: "docs-front-door", label: "docs/front-door/", kind: "documentation" },
] as const;
