/**
 * Safety Systems Design — Four Safety Domains
 *
 * These four domains define the scope of all safety work
 * in the Commonwealth. Every project maps to one or more domains.
 */

export interface SafetyDomain {
  readonly id: string
  readonly name: string
  readonly focus: string
  readonly failureClass: string
}

export const SAFETY_DOMAINS: readonly SafetyDomain[] = [
  {
    id: "epistemic",
    name: "Epistemic Safety",
    focus: "Truth, claims, verification",
    failureClass:
      "System asserts something untrue; user acts on it",
  },
  {
    id: "human",
    name: "Human Safety",
    focus: "Behavior, decisions, intervention",
    failureClass:
      "System designed for median user; everyone else harmed",
  },
  {
    id: "cognitive",
    name: "Cognitive Safety",
    focus: "Understanding, learning, mental models",
    failureClass:
      "Learning environment produces false understanding",
  },
  {
    id: "empirical",
    name: "Empirical Safety",
    focus: "Measurement, evaluation, evidence",
    failureClass:
      "Described behavior \u2260 actual behavior; consent assumed",
  },
] as const
