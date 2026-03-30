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
  // ConsentChain repoPath: see 04-consentchain/REGISTRY_PATH_MIGRATION.md (TLC submodule vs prior sibling checkout).
  {
    id: "consentchain",
    name: "ConsentChain",
    domainIds: ["empirical"],
    status: "partial",
    repoPath: "/Users/coreyalejandro/Projects/the-living-constitution/projects/consentchain",
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
  {
    id: "instructional-integrity-studio",
    name: "Instructional Integrity Studio",
    domainIds: ["cognitive"],
    status: "partial",
    repoPath: "/Users/coreyalejandro/Projects/instructional-integrity-ui",
    resumeClaim:
      "Partial — cognitive safety evaluator, rule-based rubric, 15/15 unit tests passing; ZSB-IIS-v2.0 governs",
  },
  {
    id: "tlc-evidence-observatory",
    name: "TLC Evidence Observatory",
    domainIds: ["epistemic", "empirical"],
    status: "prototype",
    repoPath: "/Users/coreyalejandro/Projects/tlc-evidence-observatory",
    resumeClaim:
      "Prototype — forensic ingest pipeline, SHA-256 chain of custody, append-only evidence records",
  },
  {
    id: "buildlattice-guard",
    name: "BuildLattice Guard",
    domainIds: ["epistemic", "human", "cognitive", "empirical"],
    status: "planned",
    repoPath: "/Users/coreyalejandro/Projects/buildlattice",
    resumeClaim:
      "Planned — ZSB-BLG-v2.0 contract written; machine-checkable build contracts for agentic SDLC governance",
  },
  {
    id: "frostbyte-etl",
    name: "Frostbyte ETL",
    domainIds: ["empirical"],
    status: "partial",
    repoPath: "/Users/coreyalejandro/Projects/frostbyte-etl",
    resumeClaim:
      "Partial — ZSB-FBE-v1.0 contract written; 5-phase ETL pipeline (intake→parse→enrich→store→index); SHA-256 chain of custody; per-tenant isolation; dual-mode online/offline",
  },
  {
    id: "epistemic-guard",
    name: "EpistemicGuard Platform",
    domainIds: ["epistemic"],
    status: "planned",
    repoPath: "/Users/coreyalejandro/Projects/epistemic-guard",
    resumeClaim:
      "Planned — ZSB-EPG-v1.0 contract written; D1 integrated engine; ClaimAuditor, PII Masker, PolicyMapper, TruthRecord",
  },
  {
    id: "human-guard",
    name: "HumanGuard",
    domainIds: ["human"],
    status: "planned",
    repoPath: "/Users/coreyalejandro/Projects/human-guard",
    resumeClaim:
      "Planned — ZSB-HMG-v1.0 contract written; D2 integrated engine; SessionSafeguard, GroundingReset, HarmScanner, CrisisGate",
  },
  {
    id: "empirical-guard",
    name: "EmpiricalGuard",
    domainIds: ["empirical"],
    status: "planned",
    repoPath: "/Users/coreyalejandro/Projects/empirical-guard",
    resumeClaim:
      "Planned — ZSB-EMG-v1.0 contract written; D4 integrated engine; BehaviorObserver, MoodSignal Bus, AdaptiveUI Signal",
  },
] as const
