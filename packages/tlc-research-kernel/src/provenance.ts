/**
 * provenance.ts
 * Provenance tracker — records the origin, transformation, and chain of custody
 * for every artifact produced in the TLC research workbench.
 *
 * Every artifact surfaced in the control plane must have a ProvenanceRecord.
 * This satisfies I4 (traceability) and I1 (evidence basis).
 *
 * evidence_basis: CONSTRUCTED — derived from AGENTS.md I4 and TLC contract spec.
 */

import { EvidenceBasis } from "./experiment-schema";

/** Transformation step in an artifact's chain of custody */
export interface ProvenanceStep {
  step: number;
  action: string; // "generated" | "patched" | "reviewed" | "committed"
  actor: string; // agent ID or "human:corey"
  tool?: string;
  commit_sha?: string;
  timestamp_utc: string;
  invariant_category?: string; // which invariant this step addresses
}

/** Full provenance record for an artifact */
export interface ProvenanceRecord {
  artifact_id: string;
  artifact_path: string;
  artifact_type: "file" | "registry_entry" | "eval_result" | "proposal" | "session_outcome";
  created_at_utc: string;
  evidence_basis: EvidenceBasis;
  chain: ProvenanceStep[];
}

/**
 * Creates an initial provenance record for a new artifact.
 */
export function startProvenance(
  artifact_path: string,
  artifact_type: ProvenanceRecord["artifact_type"],
  actor: string,
  tool?: string
): ProvenanceRecord {
  const now = new Date().toISOString();
  return {
    artifact_id: `PROV-${Date.now()}`,
    artifact_path,
    artifact_type,
    created_at_utc: now,
    evidence_basis: "CONSTRUCTED",
    chain: [
      {
        step: 1,
        action: "generated",
        actor,
        tool,
        timestamp_utc: now,
        invariant_category: "I4",
      },
    ],
  };
}

/**
 * Adds a step to an existing provenance record.
 */
export function addProvenanceStep(
  record: ProvenanceRecord,
  action: string,
  actor: string,
  opts?: Partial<ProvenanceStep>
): ProvenanceRecord {
  return {
    ...record,
    chain: [
      ...record.chain,
      {
        step: record.chain.length + 1,
        action,
        actor,
        timestamp_utc: new Date().toISOString(),
        ...opts,
      },
    ],
  };
}
