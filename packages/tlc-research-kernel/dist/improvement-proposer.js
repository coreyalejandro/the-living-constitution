"use strict";
/**
 * improvement-proposer.ts
 * Bounded self-improvement proposer with mandatory human approval gate.
 *
 * The improvement loop is strictly bounded:
 * - Auto-apply ONLY to non-authoritative generated surfaces
 * - Never apply to: THE_LIVING_CONSTITUTION.md, MASTER_PROJECT_INVENTORY.json,
 *   STATUS.json, docs/governance/doctrines/*, canonical C-RSP artifacts
 * - Every proposal is logged to research/registry/improvement_proposals.json
 * - Human must approve before execution
 *
 * evidence_basis: CONSTRUCTED — derived from TLC-RDI-MVP-001 contract spec.
 */
Object.defineProperty(exports, "__esModule", { value: true });
exports.PROTECTED_SURFACES = void 0;
exports.isProtectedSurface = isProtectedSurface;
exports.createProposal = createProposal;
/** Authoritative surfaces that can NEVER be auto-modified */
exports.PROTECTED_SURFACES = new Set([
    "THE_LIVING_CONSTITUTION.md",
    "MASTER_PROJECT_INVENTORY.json",
    "STATUS.json",
    "docs/governance/doctrines",
    "projects/c-rsp/BUILD_CONTRACT.md",
]);
/**
 * Checks if a target surface is protected from auto-modification.
 */
function isProtectedSurface(target) {
    for (const surface of exports.PROTECTED_SURFACES) {
        if (target.includes(surface))
            return true;
    }
    return false;
}
/**
 * Creates a new improvement proposal record.
 * Always creates with status: pending_review.
 * Caller must write to research/registry/improvement_proposals.json.
 */
function createProposal(params) {
    const isProtected = isProtectedSurface(params.target_surface);
    return {
        ...params,
        id: `IMP-${Date.now()}`,
        is_authoritative_surface: isProtected || params.is_authoritative_surface,
        status: "pending_review",
        proposed_at_utc: new Date().toISOString(),
    };
}
//# sourceMappingURL=improvement-proposer.js.map