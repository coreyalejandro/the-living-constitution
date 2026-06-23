"use strict";
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
Object.defineProperty(exports, "__esModule", { value: true });
exports.startProvenance = startProvenance;
exports.addProvenanceStep = addProvenanceStep;
/**
 * Creates an initial provenance record for a new artifact.
 */
function startProvenance(artifact_path, artifact_type, actor, tool) {
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
function addProvenanceStep(record, action, actor, opts) {
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
//# sourceMappingURL=provenance.js.map