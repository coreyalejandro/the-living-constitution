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
    action: string;
    actor: string;
    tool?: string;
    commit_sha?: string;
    timestamp_utc: string;
    invariant_category?: string;
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
export declare function startProvenance(artifact_path: string, artifact_type: ProvenanceRecord["artifact_type"], actor: string, tool?: string): ProvenanceRecord;
/**
 * Adds a step to an existing provenance record.
 */
export declare function addProvenanceStep(record: ProvenanceRecord, action: string, actor: string, opts?: Partial<ProvenanceStep>): ProvenanceRecord;
//# sourceMappingURL=provenance.d.ts.map