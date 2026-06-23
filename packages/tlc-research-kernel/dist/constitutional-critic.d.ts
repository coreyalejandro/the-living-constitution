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
    target: string;
    reviewed_at_utc: string;
    violations: CriticViolation[];
    pass: boolean;
    evidence_basis: EvidenceBasis;
}
/** Invariant rules mapped to check patterns */
export declare const INVARIANT_RULES: Record<InvariantId, string>;
/**
 * Checks a text blob for I2 phantom-work patterns.
 * Returns violations if completion language appears without evidence artifact.
 */
export declare function checkPhantomWork(text: string, location: string): CriticViolation[];
/**
 * Checks a text blob for missing evidence basis tags (I1).
 */
export declare function checkEvidenceBasisTags(text: string, location: string): CriticViolation[];
//# sourceMappingURL=constitutional-critic.d.ts.map