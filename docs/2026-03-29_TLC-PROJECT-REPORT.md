# 2026-03-29 — TLC Project Report

## What The Living Constitution Is

The Living Constitution (TLC) is the supreme governing document and operational infrastructure for the Safety Systems Design Commonwealth — a portfolio of AI safety systems built by Corey Alejandro, submitted as the work product for the Anthropic Safety Fellows Program (July 2026 cohort).

It is three things at once.

**A governance framework.** Three doctrines and five articles that govern every line of code, every agent decision, and every claim across all projects. The doctrines are the Idempotency Doctrine (same input, same output, always — specifically designed so that a neurodivergent user who restarts or retries cannot break the system), the Calibrated Truth Doctrine (every claim's assurance level must match its verification method — convention, machine-checkable, or formal proof), and the Census Doctrine (you cannot govern what you haven't counted — every module has a declared truth-status, no inflation). The five articles are the Bill of Rights (Article I), Execution Law (Article II), Purpose Law (Article III), Separation of Powers (Article IV), and the Amendment Process (Article V).

**A Commonwealth of 13 projects**, each mapped to one or more of four safety domains — Epistemic, Human, Cognitive, Empirical.

| Project | Domain(s) | Status | Key Evidence |
|---------|-----------|--------|-------------|
| PROACTIVE | Epistemic | Implemented | 212/212 tests, 0% FP, GitLab hackathon submitted |
| SentinelOS | All 4 | Partial | 1,037 LOC TypeScript, 6 invariants (I1-I6) defined |
| ConsentChain | Empirical | Partial | 7-stage action gateway, 8 Turborepo packages, Prisma |
| UICare-System | Human | Partial | GPT-4o-mini + Kubernetes, absence-over-presence signal |
| Docen | Cognitive | Deployed | Live at GCR, HTTP 200 verified |
| Portfolio | All 4 | Deployed | Live at coreyalejandro.com |
| Instructional Integrity Studio | Cognitive | Partial | 15/15 unit tests passing |
| TLC Evidence Observatory | Epistemic + Empirical | Prototype | 5-layer pipeline, 49/49 tests, Vellum UI built |
| MADMall | Human + Cognitive + Empirical | Partial | 6 apps, 22 packages, ~152K LOC, Clerk/Stripe/Prisma |
| BuildLattice Guard | All 4 | Planned | C-RSP-BLG-v2.0 contract written |
| Frostbyte ETL | Empirical | Partial | 5-phase ETL pipeline, SHA-256 chain of custody |
| EpistemicGuard Platform | Epistemic | Planned | C-RSP-EPG-v1.0 contract written |
| HumanGuard | Human | Planned | C-RSP-HMG-v1.0 contract written |
| EmpiricalGuard | Empirical | Planned | C-RSP-EMG-v1.0 contract written |

**A personal system of care.** The constitution defines the "default user" as a neurodivergent adult with autism, bipolar I disorder with psychotic features, ADHD, OCD, and trauma history — high intellectual capacity, poor spatial reasoning, Stanford-educated. The barrier is never comprehension, it is presentation. SOP-013 (Session Recovery) exists specifically for cognitive overwhelm and manic episode onset: all agents pause, work is saved, a calm close message appears, and on return one next step is offered at cognitive load Level 1. This is not a special mode. It is the default.

## Infrastructure

The `the-living-constitution` repository is the base camp — governance overlay, not code. It holds the spec (`THE_LIVING_CONSTITUTION.md`), build contracts for every project (`projects/<name>/BUILD_CONTRACT.md`), the verification matrix (`verification/MATRIX.md`), and the amendment log. Code lives in the project repos it governs.

The Constitutional Enforcement Stack runs from the human orchestrator at the top, through the Orchestration Cortex (Claude Code + CLAUDE.md), the Agent Republic (Planner, Builder, Sentinel, TDD Guide, Code Reviewer, Data Scientist), the Tool/MCP Republic, the Neurodivergent Access Infrastructure, to the Evidence and Change Foundation at the bottom.

## Verification Status

The Verification Matrix shows 21 of 24 resume claims verified, 1 partial (GitHub repo count: 257 verified vs. ~340 claimed), 1 pending (SentinelOS build). Two resume items flagged for update: SentinelOS LOC (1,037 actual, not ~1,500) and GitHub repo count.

## V&T Statement

**Exists:** This report, sourced entirely from files in the `the-living-constitution` repository. THE_LIVING_CONSTITUTION.md (full spec). 00-constitution/articles.md (Articles I-V with implementation mapping). 00-constitution/constitution.md (summary with doctrines). config/projects.ts (13 projects registered). config/domains.ts (4 safety domains). verification/MATRIX.md (24 claims tracked). tasks/todo.md (sprint tracker). evaluation/ (failure taxonomy F1-F5, evidence summary, pattern analysis, 18 failure cases). 11 BUILD_CONTRACT.md files across projects/.

**Non-existent:** Tier 2 machine-checkable enforcement of constitutional rules. Formal proofs (Tier 3). Data Scientist agent instruction file. Runtime SentinelOS enforcement.

**Unverified:** Whether all agent instruction files still exist at declared paths. Whether truth-status sync is current across all repos. Whether THE_LIVING_CONSTITUTION.md and 00-constitution/constitution.md are in sync.

**Functional status:** Governance framework is complete and enforced at Tier 1 (convention). Commonwealth projects range from deployed to planned. Verification matrix is 87.5% verified (21/24). System is operational but Tier 2 automation is the primary gap.
