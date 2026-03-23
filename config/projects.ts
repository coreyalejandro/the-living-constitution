/**
 * Commonwealth Project Registry — Domain Mapping
 *
 * Every project in the Commonwealth maps to one or more safety domains.
 * Unmapped projects are ungoverned projects (Census Doctrine).
 */

import type { SafetyDomain } from "./domains"

export type ProjectStatus =
  | "implemented"
  | "partial"
  | "prototype"
  | "planned"
  | "deployed"

export interface CommonwealthProject {
  readonly id: string
  readonly name: string
  readonly domainIds: readonly string[]
  readonly status: ProjectStatus
  readonly repoPath: string
  readonly resumeClaim: string
}

export const COMMONWEALTH_PROJECTS: readonly CommonwealthProject[] = [
  {
    id: "proactive",
    name: "PROACTIVE",
    domainIds: ["epistemic"],
    status: "implemented",
    repoPath: "/Users/coreyalejandro/Projects/proactive-gitlab-agent",
    resumeClaim:
      "Operational, 100% detection rate, 0% FP, validated 2026-01-24",
  },
  {
    id: "sentinelos",
    name: "SentinelOS",
    domainIds: ["epistemic", "human", "cognitive", "empirical"],
    status: "partial",
    repoPath: "/Users/coreyalejandro/Projects/sentinelos",
    resumeClaim:
      "Partial, ~1,500 LOC TypeScript, invariant enforcement platform",
  },
  {
    id: "consentchain",
    name: "ConsentChain",
    domainIds: ["empirical"],
    status: "partial",
    repoPath: "/Users/coreyalejandro/Projects/consentchain",
    resumeClaim:
      "Partial, 7-stage action gateway, Turborepo 8 packages, Prisma",
  },
  {
    id: "uicare",
    name: "UICare-System",
    domainIds: ["human"],
    status: "partial",
    repoPath: "/Users/coreyalejandro/Projects/uicare-system",
    resumeClaim:
      "Partial, GPT-4o-mini + Kubernetes, absence-over-presence signal",
  },
  {
    id: "docen",
    name: "Docen",
    domainIds: ["cognitive"],
    status: "deployed",
    repoPath: "/Users/coreyalejandro/Projects/docen",
    resumeClaim:
      "Deployed at docen-live-677222981446.us-central1.run.app",
  },
  {
    id: "portfolio",
    name: "Portfolio (coreyalejandro.com)",
    domainIds: ["epistemic", "human", "cognitive", "empirical"],
    status: "deployed",
    repoPath: "/Users/coreyalejandro/Projects/coreys-agentic-portfolio",
    resumeClaim: "Live at coreyalejandro.com",
  },
] as const
