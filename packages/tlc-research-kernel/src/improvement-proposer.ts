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

import { EvidenceBasis } from "./experiment-schema";

/** Approval status of a proposal */
export type ProposalStatus = "pending_review" | "approved" | "rejected" | "executed" | "rolled_back";

/** A single improvement proposal */
export interface ImprovementProposal {
  id: string;
  title: string;
  description: string;
  target_surface: string; // file or surface being improved
  is_authoritative_surface: boolean; // if true, HALT — never auto-apply
  proposed_change: string;
  rationale: string;
  invariant_addressed: string;
  status: ProposalStatus;
  proposed_at_utc: string;
  reviewed_at_utc?: string;
  reviewer?: string;
  evidence_basis: EvidenceBasis;
}

/** Authoritative surfaces that can NEVER be auto-modified */
export const PROTECTED_SURFACES = new Set([
  "THE_LIVING_CONSTITUTION.md",
  "MASTER_PROJECT_INVENTORY.json",
  "STATUS.json",
  "docs/governance/doctrines",
  "projects/c-rsp/BUILD_CONTRACT.md",
]);

/**
 * Checks if a target surface is protected from auto-modification.
 */
export function isProtectedSurface(target: string): boolean {
  for (const surface of PROTECTED_SURFACES) {
    if (target.includes(surface)) return true;
  }
  return false;
}

/**
 * Creates a new improvement proposal record.
 * Always creates with status: pending_review.
 * Caller must write to research/registry/improvement_proposals.json.
 */
export function createProposal(params: Omit<ImprovementProposal, "id" | "status" | "proposed_at_utc">): ImprovementProposal {
  const isProtected = isProtectedSurface(params.target_surface);
  return {
    ...params,
    id: `IMP-${Date.now()}`,
    is_authoritative_surface: isProtected || params.is_authoritative_surface,
    status: "pending_review",
    proposed_at_utc: new Date().toISOString(),
  };
}
