# Repo Relationship Map
## How All Repositories Relate Under TLC Governance

---

## The Governance Hierarchy

```
the-living-constitution (BASE CAMP)
│
│  The supreme governing document. Not a code repo.
│  Contains: THE_LIVING_CONSTITUTION.md, build contracts,
│  verification matrix, project registry, domain mapping.
│
├── GOVERNANCE LAYER (spec + enforcement)
│   │
│   ├── sentinelos/
│   │   TypeScript invariant enforcement platform
│   │   Domain: All 4 safety domains
│   │   Status: Partial
│   │   Depends on: TLC specification (Articles I-V)
│   │   Implements: I1-I6 invariant checking, V&T generation,
│   │               truth-status engine, agent boundaries
│   │
│   └── proactive-gitlab-agent/
│       Python epistemic enforcement engine
│       Domain: Epistemic Safety
│       Status: Validated — 212/212 tests passing, submitted to GitLab hackathon (2026-03-25)
│       Depends on: TLC specification (Article I, invariants I1, I3, I5)
│       Implements: MR scanning for epistemic violations
│       Repos: GitLab (submission) + GitHub (active dev)
│
├── PRODUCT LAYER (domain-specific applications)
│   │
│   ├── consentchain/
│   │   Cryptographic consent ledger
│   │   Domain: Empirical Safety
│   │   Status: Partial
│   │   Depends on: TLC governance (Article II execution law)
│   │   Implements: 7-stage agent authorization gateway
│   │
│   ├── uicare-system/
│   │   Developer safety monitor
│   │   Domain: Human Safety
│   │   Status: Partial
│   │   Depends on: TLC governance (Article I bill of rights)
│   │   Implements: Absence-over-presence signal detection
│   │
│   ├── docen/
│   │   Document processing service
│   │   Domain: Cognitive Safety
│   │   Status: Operational (deployed on GCR)
│   │   Depends on: TLC governance (Article II execution law)
│   │   Implements: Safety-aware document transformation
│   │
│   └── MADMall-Production/
│       Virtual luxury mall & teaching clinic for Black women with Graves' disease
│       Domain: Human Safety, Cognitive Safety (primary); Empirical Safety (secondary)
│       Status: Partial — infrastructure mature (152K LOC), features Phase 1 of 4
│       Depends on: TLC governance (all Articles); ConsentChain (data consent);
│                   PROACTIVE (ML claims validation); UICare (cognitive load)
│       Implements: Healthcare AI with constitutional governance as primary TLC use case
│       Stack: Next.js 16, Turborepo, Prisma/PostgreSQL, Clerk, Stripe, Python ML
│
└── PRESENTATION LAYER
    │
    └── coreys-agentic-portfolio/
        Public portfolio (coreyalejandro.com)
        Domain: All 4 (presents the full system)
        Status: Operational (deployed on Vercel)
        Depends on: All products (presents their status honestly)
        Implements: Commonwealth as a unified narrative
```

---

## Dependency Flow

The dependency arrow always points toward the Constitution. No product depends on another product. Every product depends on the governance layer.

```
                    THE LIVING CONSTITUTION
                    (the-living-constitution/)
                            │
                ┌───────────┼───────────┐
                │           │           │
                ▼           ▼           ▼
           SentinelOS   PROACTIVE   Portfolio
           (enforce)    (detect)    (present)
                │           │
                │           │
    ┌───────────┼───────────┼───────────┐
    │           │           │           │
    ▼           ▼           ▼           ▼
ConsentChain  UICare     Docen     (future products)
(empirical)  (human)   (cognitive)

Arrow direction: product --> governance (depends on)
No arrows between products (no cross-dependencies)
```

---

## Platform and Location Map

| Repository | Platform | URL/Location | Language | Build Tool |
|-----------|----------|-------------|----------|-----------|
| the-living-constitution | GitHub | github.com/coreyalejandro/the-living-constitution | Markdown, TypeScript (config) | N/A (governance overlay) |
| sentinelos | GitHub | github.com/coreyalejandro/sentinelos | TypeScript | Turborepo + pnpm |
| proactive-gitlab-agent | GitLab (submission) + GitHub (active dev) | gitlab.com/gitlab-ai-hackathon/participants/28441830 + github.com/coreyalejandro/proactive-gitlab-agent | Python | pip + pytest |
| MADMall-Production | GitHub | github.com/coreyalejandro/MADMall-Production | TypeScript/Python | Turborepo + pnpm |
| consentchain | GitHub | github.com/coreyalejandro/consentchain | TypeScript | Turborepo + pnpm |
| uicare-system | GitHub | github.com/coreyalejandro/uicare-system | JavaScript/TypeScript | npm |
| docen | GitHub | github.com/coreyalejandro/docen | (deployed) | Google Cloud Run |
| coreys-agentic-portfolio | GitHub | github.com/coreyalejandro/coreys-agentic-portfolio | TypeScript (Next.js) | Vercel |

---

## Domain Coverage Matrix

Which repos serve which safety domains:

| Repository | Epistemic | Human | Cognitive | Empirical |
|-----------|-----------|-------|-----------|-----------|
| the-living-constitution | X | X | X | X |
| sentinelos | X | X | X | X |
| proactive-gitlab-agent | X | | | |
| consentchain | | | | X |
| uicare-system | | X | | |
| MADMall-Production | | X | X | X |
| docen | | | X | |
| coreys-agentic-portfolio | X | X | X | X |

**Coverage update**: MADMall-Production strengthens Human Safety (healthcare UX for chronically ill users), Cognitive Safety (ML-backed health education), and Empirical Safety (consent-governed data collection). Cognitive Safety domain is now covered by both Docen and MADMall.

---

## Data Flow Between Repos

There is currently no runtime data flow between repositories. Each product operates independently. The governance relationship is structural (shared specification), not operational (API calls between services).

```
the-living-constitution
    │
    │ (specification flows down via CLAUDE.md files
    │  and build contracts -- NOT runtime API calls)
    │
    ├── sentinelos:     reads TLC spec, implements as TypeScript invariants
    ├── proactive:      reads TLC invariant definitions, applies to MR scanning
    ├── consentchain:   follows TLC Article II execution law in its gateway design
    ├── uicare:         follows TLC Article I bill of rights in its monitoring design
    ├── docen:          follows TLC Article II execution law
    └── portfolio:      presents TLC governance narrative
```

**Future state**: SentinelOS would become a shared runtime dependency, providing invariant checking as a service that other products consume via API. This is specified but not built.

---

## Build Contract Relationship

Every project has a build contract in the base camp that governs its development:

```
the-living-constitution/
  projects/
    sentinelos/
      CLAUDE.md           --> governance overlay
      BUILD_CONTRACT.md   --> zero-shot build spec
    proactive/
      CLAUDE.md           --> governance overlay
      BUILD_CONTRACT.md   --> zero-shot build spec
    consentchain/
      CLAUDE.md           --> governance overlay
      BUILD_CONTRACT.md   --> zero-shot build spec
    uicare/
      CLAUDE.md           --> governance overlay
      BUILD_CONTRACT.md   --> zero-shot build spec
```

The build contract points to the external repo where implementation lives. The base camp does NOT duplicate code. It governs code.

---

## Status Summary

| Repository | Status | Last Verified |
|-----------|--------|--------------|
| the-living-constitution | Operational | Active (governance hub) |
| sentinelos | Partial | 9 packages, 1,037 LOC, hexagonal arch. Build verification pending. |
| proactive-gitlab-agent | Validated | 212/212 tests passing. Submitted to GitLab hackathon 2026-03-25. |
| MADMall-Production | Partial | Infrastructure mature (152K LOC). Features Phase 1 of 4. |
| consentchain | Partial | Gateway curl-tested, last commit 2026-03-17 |
| uicare-system | Partial | Components exist, last commit 2026-03-17 |
| docen | Operational | Deployed on GCR |
| coreys-agentic-portfolio | Operational | Live on Vercel |

---

## V&T Statement

Exists: Complete repository relationship map with governance hierarchy, dependency flow, platform locations, domain coverage matrix, data flow documentation, and build contract relationships. Seven repositories mapped with honest status labels.

Non-existent: Runtime data flow between repositories (currently structural governance only, no API integration). MADMall repository (healthcare/wellness product not yet built). Automated dependency graph generation.

Unverified: Whether all GitHub/GitLab repo URLs are currently accessible. Whether PROACTIVE's GitLab repo is public or private.

Functional status: Relationship map complete. All repos documented with dependencies, domains, and honest status. Coverage gaps identified (Cognitive Safety domain is thin).
