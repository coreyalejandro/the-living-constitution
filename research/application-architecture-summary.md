# Application Architecture Summary
## The Living Constitution as Constitutional OS for AI Safety

### What This Document Is

I provide a complete architectural summary of the Safety Systems Design Commonwealth: a constitutional governance-as-code platform for AI safety. I wrote this document for Anthropic reviewers evaluating design coherence, not marketing language.

---

## The Commonwealth: Five Layers

I call the system the **Safety Systems Design Commonwealth**. It is a political metaphor applied to software with structural precision. I organize it into five layers, each with a clear analogy and implementation surface.

```
Layer 1: The Living Constitution    (Supreme law — Articles I-V)
Layer 2: SentinelOS                 (Enforcement platform — the federal government)
Layer 3: Four Safety Domains        (Departments — Epistemic, Human, Cognitive, Empirical)
Layer 4: Products                   (Agencies — PROACTIVE, UICare, ConsentChain, Docen)
Layer 5: The Agent Republic         (Civil servants — Planner, Builder, Sentinel, TDD, Reviewer, DataSci)
```

---

## Layer 1: The Living Constitution

The governing specification. Five articles modeled on the U.S. Constitution, encoded into CLAUDE.md files, CI hooks, and agent prompts.

| Article | Name | Function |
|---------|------|----------|
| I | Bill of Rights | Safety, accessibility, dignity, clarity, truth — for every user and agent interaction |
| II | Execution Law | Immutability, truth-status discipline, file organization, security, error handling |
| III | Purpose Law | Every action maps to a theory of change node with measurable outcomes |
| IV | Separation of Powers | What each agent can and cannot do without human approval |
| V | Amendment Process | Structured self-evolution: trigger, observation, proposal, evaluation, ratification |

Key doctrines encoded alongside the Articles:
- **Idempotency Doctrine**: `f(f(x)) = f(x)`. Every operation produces the same result when repeated.
- **Calibrated Truth Doctrine**: Three tiers of assurance (convention, machine-checkable, formal proof). Never claim higher assurance than the method supports.
- **Census Doctrine**: You cannot govern what you have not counted. Every component inventoried, every module truth-status declared.
- **Default User Doctrine**: Design for the most vulnerable user first. Neurodivergent-accessible by default, not by toggle.

**Implementation**: The Constitution is encoded directly in `~/.claude/CLAUDE.md` (global) and project-level CLAUDE.md files. It governs every Claude Code session, every agent interaction, every commit.

---

## Layer 2: SentinelOS — Invariant Enforcement Platform

**Status: Partial**

SentinelOS is the enforcement engine. It translates constitutional articles into executable TypeScript code.

**Architecture**: Turborepo monorepo, hexagonal (ports and adapters), 8 packages.

```
              +--------------------+
              |    core/ports      |
              | (interfaces only)  |
              +---------+----------+
                        | implements
   +--------+-----------+-----------+--------+--------+
   |        |           |           |        |        |
 art-i    art-ii     art-iii     art-iv    art-v   incident
(I1-I6)  (status)  (evidence)  (agents) (amend)  (lifecycle)
                                                    |
                                              safety-case
```

**Six Invariants (I1-I6)**:

| ID | Name | What It Checks |
|----|------|---------------|
| I1 | Epistemic Qualification | Every claim has an evidence level |
| I2 | Artifact Verification | Referenced artifacts exist and are accessible |
| I3 | Confidence Grounding | Confidence levels do not exceed available evidence |
| I4 | Traceability | Every decision traces to a governance rule |
| I5 | Fluency Conflict Detection | Fluent language does not mask uncertainty |
| I6 | Fail-Closed Behavior | Ambiguous cases block rather than pass |

**What exists**: 9 packages (core + 7 adapters), 1,037 LOC source, 994 LOC tests. Hexagonal architecture correctly implemented with zero cross-adapter dependencies. 180+ Object.freeze calls enforcing immutability. 7 of 8 adapters implemented with comprehensive tests.

**What does not exist**: DomainRegistry adapter (port defined, no implementation). Integration tests across adapters. Production deployment. API documentation. Build verification pending (node PATH issue in worktree).

---

## Layer 3: Four Safety Domains

Every project maps to one or more domains. Unmapped projects are ungoverned.

| Domain | Focus | Failure Class | Primary Product |
|--------|-------|---------------|----------------|
| Epistemic Safety | Truth, claims, verification | System asserts something untrue; user acts on it | PROACTIVE |
| Human Safety | Behavior, decisions, intervention | System designed for median user; everyone else harmed | UICare |
| Cognitive Safety | Understanding, learning, mental models | Learning environment produces false understanding | Docen |
| Empirical Safety | Measurement, evaluation, evidence | Described behavior differs from actual behavior; consent assumed | ConsentChain |

---

## Layer 4: Products

### PROACTIVE — Constitutional AI Safety Agent
- **Domain**: Epistemic Safety
- **Status**: Validated — 212/212 tests passing, submitted to GitLab AI Hackathon (2026-03-25)
- **Stack**: Python, GitLab CI, Claude Code agents
- **What it does**: Scans merge requests for epistemic safety violations. Detects claims without evidence, confidence inflation, missing uncertainty markers.
- **Evidence**: 100% detection rate across 8 test cases (n=19 violations), 0% false positive rate. Validation report VR-V-15C6. 212/212 tests passing (verified 2026-03-25).
- **Known issue**: `httpx` missing from `pyproject.toml` — works in dev but fails clean install.
- **Repos**: GitLab (hackathon submission): gitlab.com/gitlab-ai-hackathon/participants/28441830 | GitHub (active dev): github.com/coreyalejandro/proactive-gitlab-agent

### ConsentChain — Cryptographic Consent Ledger
- **Domain**: Empirical Safety
- **Status**: Partial
- **Stack**: Turborepo (8 packages), Next.js, Prisma (SQLite), NextAuth/Auth0
- **What it does**: 7-stage action gateway for AI agent authorization: validation, idempotency, revocation, policy, step-up, execution, ledger. Every agent action passes through all 7 stages before execution.
- **Evidence**: Gateway curl-tested. Prisma schema with Agent, LedgerEntry, RevocationState, IdempotencyRecord, StepUpChallenge models.

### UICare-System — Developer Safety Monitor
- **Domain**: Human Safety
- **Status**: Partial
- **Stack**: Next.js, GPT-4o-mini, Kubernetes, Docker, memory-bank architecture
- **What it does**: Monitors Docker containers for stalled developer workflows. Uses absence-over-presence signal detection (what the developer is NOT doing is the signal, not what they are doing).
- **Evidence**: Web UI exists, AI service with GPT-4o-mini integration, Kubernetes deployment.yaml, Docker configuration, brain/memory-bank module.

### Docen — Document Processing Service
- **Domain**: Cognitive Safety
- **Status**: Operational (deployed)
- **Stack**: Google Cloud Run
- **What it does**: Document processing with safety-aware transformations.
- **Evidence**: Deployed at Google Cloud Run, returns HTTP 200.

### MADMall-Production — Virtual Luxury Mall & Teaching Clinic
- **Domain**: Human Safety, Cognitive Safety (primary); Empirical Safety (secondary)
- **Status**: Partial — infrastructure mature, features Phase 1 of 4
- **Stack**: Next.js 16 (next-forge), Turborepo, React 19, Prisma/PostgreSQL, Clerk, Stripe, Python ML
- **What it does**: Virtual luxury outdoor mall and teaching clinic for Black women living with Graves' disease. Combines dignified UX modeled after real luxury malls with healthcare AI/ML infrastructure. The primary TLC use case: constitutional governance integrated into data collection, ML claims validation, and user-facing consent flows.
- **Evidence**: 6 apps, 22 packages, ~152K LOC. Clerk auth, Stripe payments, Prisma DB, Sentry observability all wired. ML Python package with CRISP-DM methodology. Infinite canvas with cursor-centered zoom. Phase 3 specs: 1,200+ lines covering Sisterhood Lounge, Event Scheduling, Service Booking, User Profiles, Content Moderation.
- **Repo**: github.com/coreyalejandro/MADMall-Production

### Portfolio — coreyalejandro.com
- **Domain**: All four
- **Status**: Operational (deployed)
- **Stack**: Next.js, Vercel
- **What it does**: Public-facing portfolio presenting the Commonwealth as a unified system.
- **Evidence**: Live at coreyalejandro.com.

---

## Layer 5: The Agent Republic

Six agent roles with constitutionally defined powers and boundaries (Article IV):

| Agent | Can Do Without Approval | Needs Human Approval |
|-------|------------------------|---------------------|
| Planner | Write plans, break down tasks, draft specs | Change architectural decisions |
| Builder | Write code, write tests, create files | Deploy to production, modify DB schema |
| Sentinel | Run safety checks, raise STOP signals, write audit logs | Override other agents, modify its own rules |
| TDD Guide | Write tests first, run suites, flag coverage gaps | Skip RED phase, ship below 80% coverage |
| Code Reviewer | Flag issues, suggest fixes, approve low-risk | Auto-fix critical issues, approve own work |
| Data Scientist | Update metrics, generate reports, sync knowledge base | Redefine theory-of-change nodes |

---

## How It All Connects

```
User Intent
    |
    v
The Living Constitution (CLAUDE.md enforcement)
    |
    v
SentinelOS (invariant checking at every boundary)
    |
    +---> PROACTIVE (epistemic checks on MR/PR content)
    +---> ConsentChain (authorization checks on agent actions)
    +---> UICare (human safety monitoring on workflows)
    +---> Docen (cognitive safety on document processing)
    |
    v
Agent Republic (execution within constitutional bounds)
    |
    v
Verified Output (safe, compliant, accessible, evidence-bound)
```

The key architectural insight: the Constitution does not live in one place. It is distributed across CLAUDE.md files, agent prompts, CI hooks, and SentinelOS invariant checks. Enforcement happens at every layer, not at a single gateway.

---

## Technical Specifications

| Specification | Value |
|--------------|-------|
| Primary languages | TypeScript, Python |
| Monorepo tooling | Turborepo (SentinelOS, ConsentChain), pnpm workspaces |
| Architecture pattern | Hexagonal (ports and adapters) |
| Database | Prisma + SQLite (ConsentChain) |
| Deployment targets | Vercel (portfolio), Google Cloud Run (Docen), GitLab CI (PROACTIVE) |
| Agent orchestration | Claude Code with CLAUDE.md constitutional enforcement |
| Total GitHub repos | 257 (verified via API 2026-03-25; resume claims ~340, discrepancy under investigation) |

---

## V&T Statement

Exists: The Living Constitution specification (Articles I-V, all doctrines). Four safety domain definitions with TypeScript types. Project registry mapping every product to domains. PROACTIVE validated with 212/212 tests passing, submitted to GitLab hackathon. ConsentChain with 7-stage gateway and Prisma schema. UICare with GPT-4o-mini integration and Kubernetes config. Docen deployed on GCR. Portfolio live on Vercel. Agent republic defined with power boundaries. SentinelOS with 9 packages, 1,037 LOC, hexagonal architecture. MADMall-Production with 6 apps, 22 packages, ~152K LOC, production infrastructure wired.

Non-existent: SentinelOS production deployment and DomainRegistry adapter. MADMall Phase 2-4 features. Formal Lean 4 proofs of constitutional invariants. Automated Tier 2 verification. TLC→MADMall governance integration layer.

Unverified: SentinelOS full build (node PATH issue). Full integration test coverage across all packages.

Functional status: The Commonwealth architecture is specified and partially implemented. PROACTIVE is validated and submitted. MADMall is the primary TLC use case with mature infrastructure. Three products are partial with working components. The constitutional specification is complete and actively enforced through CLAUDE.md files.
