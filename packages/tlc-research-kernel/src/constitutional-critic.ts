/**
 * constitutional-critic.ts
 * Constitutional critic — validates research outputs against I1-I6 invariants.
 *
 * The critic is the bridge between TLC governance rules and CGL research outputs.
 * It does not evaluate CGL's science. It evaluates whether CGL's claims respect
 * TLC's epistemic standards (I1: evidence tags, I2: no phantom work, etc.).
 *
 * evidence_basis: CONSTRUCTED — derived from AGENTS.md I1-I6 invariant spec.
 */

import { EvidenceBasis, InvariantId } from "./experiment-schema";

/** A single invariant violation found by the critic */
export interface CriticViolation {
  invariant: InvariantId;
  severity: "halt" | "warn";
  location: string;
  description: string;
  repair_suggestion: string;
}

/** Result of a critic review */
export interface CriticReview {
  target: string; // file path or claim identifier
  reviewed_at_utc: string;
  violations: CriticViolation[];
  pass: boolean; // true only if zero halt-severity violations
  evidence_basis: EvidenceBasis;
}

/** Invariant rules mapped to check patterns */
export const INVARIANT_RULES: Record<InvariantId, string> = {
  I1: "Every claim must carry VERIFIED | CONSTRUCTED | PENDING tag",
  I2: "No completion claims without showing the work",
  I3: "Hedged language (likely/probably) does not satisfy I1",
  I4: "All changes traceable to stated reason",
  I5: "Correct response wins over fluent response",
  I6: "When in doubt, fail closed — flag and halt",
};

/**
 * Checks a text blob for I2 phantom-work patterns.
 * Returns violations if completion language appears without evidence artifact.
 */
export function checkPhantomWork(text: string, location: string): CriticViolation[] {
  const violations: CriticViolation[] = [];
  const phantomPatterns = [
    /(complete[d]?|finished|done|implemented|delivered)(?!.*(test|commit|sha|artifact|evidence))/gi,
    /100%(?!.*(tests passing|verified))/gi,
  ];
  for (const pattern of phantomPatterns) {
    if (pattern.test(text)) {
      violations.push({
        invariant: "I2",
        severity: "warn",
        location,
        description: "Completion language detected without evidence artifact reference",
        repair_suggestion: "Add commit SHA, test count, or explicit evidence_basis tag",
      });
    }
  }
  return violations;
}

/**
 * Checks a text blob for missing evidence basis tags (I1).
 */
export function checkEvidenceBasisTags(text: string, location: string): CriticViolation[] {
  const violations: CriticViolation[] = [];
  const claimPatterns = [/shows?|demonstrates?|proves?|confirms?/gi];
  const evidenceTagPattern = /VERIFIED|CONSTRUCTED|PENDING/;
  for (const pattern of claimPatterns) {
    if (pattern.test(text) && !evidenceTagPattern.test(text)) {
      violations.push({
        invariant: "I1",
        severity: "warn",
        location,
        description: "Claim language detected without VERIFIED/CONSTRUCTED/PENDING tag",
        repair_suggestion: "Add evidence_basis field: VERIFIED | CONSTRUCTED | PENDING",
      });
    }
  }
  return violations;
}
