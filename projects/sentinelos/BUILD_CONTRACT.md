# Build Contract: SentinelOS

## Current State (Honest)

- ~404 LOC TypeScript embedded across `/Users/coreyalejandro/Projects/coreys-agentic-portfolio/`:
  - `config/sentinel/truthStatus.ts` (127 LOC) — types + module registry
  - `docs/SentinelOS_ARCHITECTURE.md` (132 lines) — architecture spec
  - `docs/SentinelOS_INCIDENT_LIFECYCLE.md` (132 lines) — incident lifecycle spec
  - `docs/SentinelOS_SAFETY_CASE.md` (110 lines) — safety case skeleton
  - `docs/SentinelOS_TRUTH_STATUS.md` — truth-status matrix
- NO standalone repository
- NO standalone build, NO tests, NO package.json

## Target State (What Resume Claims)

"TypeScript framework (~1,500 LOC) enforcing six safety invariants at every API boundary. Designed as reusable scaffolding for red-team evaluations and interpretability experiments. Build passes; types verified."

Status: **Partial**

## Acceptance Criteria

1. Standalone repo at `/Users/coreyalejandro/Projects/sentinelos/` pushed to GitHub
2. Turborepo monorepo with 8 packages (hex8 architecture)
3. ~1,500 LOC TypeScript (measured by `find packages -name '*.ts' | xargs wc -l`)
4. `pnpm install && pnpm build` succeeds (build passes)
5. `pnpm test` passes with 80%+ coverage
6. Types verified: `pnpm exec tsc --noEmit` clean
7. Six invariants (I1-I6) defined and enforceable
8. Hexagonal architecture: ports in core, adapters in article packages

## Evidence Required

```bash
# Repo exists and builds
cd /Users/coreyalejandro/Projects/sentinelos
pnpm install && pnpm build && pnpm test

# LOC count
find packages -name '*.ts' -not -path '*/node_modules/*' | xargs wc -l
# Expected: ~1,500 LOC

# Type check clean
pnpm exec tsc --noEmit

# Package count
ls packages/
# Expected: core, article-i, article-ii, article-iii, article-iv, article-v, incident, safety-case (8 packages)
```

## Implementation Spec

### Repo Initialization

```bash
mkdir -p sentinelos && cd sentinelos
pnpm init
pnpm add -Dw turbo typescript vitest @types/node
```

### Turborepo Config

- `turbo.json`: pipeline for build, test, lint, typecheck
- `tsconfig.base.json`: shared TS config (strict, ES2022, NodeNext)
- `pnpm-workspace.yaml`: `packages/*`

### Package Structure (8 packages)

#### 1. `packages/core` — Shared Kernel
Ports (interfaces) + types + constants. NO adapters. NO implementation logic.

```typescript
// src/ports/invariant-checker.port.ts
export interface InvariantChecker {
  readonly check: (claim: Claim) => InvariantResult
  readonly checkAll: (claims: readonly Claim[]) => readonly InvariantResult[]
}

// src/ports/truth-status.port.ts
export interface TruthStatusEngine {
  readonly getStatus: (moduleId: string) => SentinelStatus
  readonly validateTransition: (from: SentinelStatus, to: SentinelStatus) => TransitionResult
}

// src/ports/vt-statement.port.ts
export interface VTStatementGenerator {
  readonly generate: (context: VTContext) => VTStatement
  readonly validate: (statement: VTStatement) => ValidationResult
}

// src/ports/domain-registry.port.ts
export interface DomainRegistry {
  readonly getDomain: (id: string) => SafetyDomain | undefined
  readonly getAll: () => readonly SafetyDomain[]
  readonly getModulesForDomain: (domainId: string) => readonly SentinelModule[]
}

// src/ports/incident-handler.port.ts
export interface IncidentHandler {
  readonly create: (event: IncidentEvent) => Incident
  readonly transition: (incident: Incident, action: IncidentAction) => Incident
  readonly getLifecycle: () => readonly IncidentState[]
}

// src/ports/amendment-engine.port.ts
export interface AmendmentEngine {
  readonly propose: (trigger: AmendmentTrigger) => Amendment
  readonly evaluate: (amendment: Amendment) => EvalResult
  readonly ratify: (amendment: Amendment) => RatifiedAmendment
}

// src/types/index.ts — ALL shared types
export type SentinelStatus = "implemented" | "partial" | "prototype" | "planned"
export type InvariantId = "I1" | "I2" | "I3" | "I4" | "I5" | "I6"

export interface Invariant {
  readonly id: InvariantId
  readonly name: string
  readonly description: string
  readonly check: string  // human-readable check description
}

export interface Claim { ... }
export interface InvariantResult { ... }
export interface VTStatement { ... }
export interface VTContext { ... }
export interface SafetyDomain { ... }
export interface SentinelModule { ... }
export interface Incident { ... }
export interface Amendment { ... }
// etc.

// src/constants/invariants.ts — I1-I6 definitions
export const INVARIANTS: readonly Invariant[] = [
  { id: "I1", name: "Epistemic Qualification", description: "Every claim must be qualified with evidence level", check: "Claim has evidence reference" },
  { id: "I2", name: "Artifact Verification", description: "Referenced artifacts must exist and be accessible", check: "Artifact path resolves to real file" },
  { id: "I3", name: "Confidence Grounding", description: "Confidence levels must match available evidence", check: "Confidence <= evidence strength" },
  { id: "I4", name: "Traceability", description: "Every decision must trace to a governance rule", check: "Decision has rule ID" },
  { id: "I5", name: "Fluency Conflict Detection", description: "Fluent language must not mask uncertainty", check: "No hedging without explicit uncertainty marker" },
  { id: "I6", name: "Fail-Closed Behavior", description: "Ambiguous cases must fail closed (block, not pass)", check: "Ambiguous input -> rejection, not approval" },
]

// src/constants/domains.ts — 4 safety domains
export const SAFETY_DOMAINS: readonly SafetyDomain[] = [
  { id: "epistemic", name: "Epistemic Safety", focus: "Truth, claims, verification", failureClass: "System asserts something untrue" },
  { id: "human", name: "Human Safety", focus: "Behavior, decisions, intervention", failureClass: "System designed for median user" },
  { id: "cognitive", name: "Cognitive Safety", focus: "Understanding, learning, mental models", failureClass: "Learning environment produces false understanding" },
  { id: "empirical", name: "Empirical Safety", focus: "Measurement, evaluation, evidence", failureClass: "Described behavior != actual behavior" },
]
```

**Estimated LOC: ~200**

#### 2. `packages/article-i` — Bill of Rights (Invariant Enforcement + V&T)
Adapters implementing `InvariantChecker` and `VTStatementGenerator` ports.

- `src/adapters/invariant-checker.adapter.ts` — Checks claims against I1-I6
- `src/adapters/vt-statement.adapter.ts` — Generates and validates V&T statements
- `__tests__/invariant-checker.test.ts` — Test all 6 invariants with known-good and known-bad inputs
- `__tests__/vt-statement.test.ts` — Test generation + validation

**Estimated LOC: ~200**

#### 3. `packages/article-ii` — Execution Law (Truth-Status Engine)
Adapters implementing `TruthStatusEngine` port.

- `src/adapters/truth-status-engine.adapter.ts` — Status transitions, upgrade validation
- `src/adapters/code-governance.adapter.ts` — File size checks, immutability patterns
- `__tests__/truth-status-engine.test.ts` — Test valid/invalid transitions

**Estimated LOC: ~180**

#### 4. `packages/article-iii` — Purpose Law (Evidence Chains)
Adapters implementing evidence chain validation.

- `src/adapters/evidence-chain.adapter.ts` — Validate claim -> evidence -> artifact chains
- `src/adapters/toc-validator.adapter.ts` — Theory of Change node alignment
- `__tests__/evidence-chain.test.ts`

**Estimated LOC: ~150**

#### 5. `packages/article-iv` — Separation of Powers (Agent Boundaries)
Adapters implementing `DomainRegistry` port + agent power enforcement.

- `src/adapters/agent-registry.adapter.ts` — Register agents, define capabilities
- `src/adapters/power-boundary.adapter.ts` — Check if action is within agent's power
- `__tests__/agent-registry.test.ts`
- `__tests__/power-boundary.test.ts`

**Estimated LOC: ~180**

#### 6. `packages/article-v` — Amendment Process (Self-Evolution)
Adapters implementing `AmendmentEngine` port.

- `src/adapters/amendment-engine.adapter.ts` — Propose, evaluate, ratify amendments
- `src/adapters/lesson-tracker.adapter.ts` — Track lessons, detect patterns
- `__tests__/amendment-engine.test.ts`

**Estimated LOC: ~150**

#### 7. `packages/incident` — Incident Lifecycle (Cross-Cutting)
Adapters implementing `IncidentHandler` port.

- `src/adapters/lifecycle.adapter.ts` — 5-step incident pipeline state machine
- `src/adapters/severity.adapter.ts` — Severity classification
- `src/types.ts` — Incident-specific types
- `__tests__/lifecycle.test.ts`

**Estimated LOC: ~180**

#### 8. `packages/safety-case` — Safety Case Skeleton (Cross-Cutting)
Safety case structure as typed data.

- `src/adapters/safety-case.adapter.ts` — Build safety case from module evidence
- `__tests__/safety-case.test.ts`

**Estimated LOC: ~100**

### LOC Budget

| Package | Estimated LOC |
|---------|--------------|
| core | 200 |
| article-i | 200 |
| article-ii | 180 |
| article-iii | 150 |
| article-iv | 180 |
| article-v | 150 |
| incident | 180 |
| safety-case | 100 |
| **Total** | **~1,340 + config/test setup ~160 = ~1,500** |

### Hexagonal Architecture Rules

1. `core/` contains ONLY ports (interfaces) and types. Zero implementation logic.
2. Each `article-*/` package depends ONLY on `core/`. Never on another article package.
3. Adapters implement ports. The dependency arrow points inward (adapter -> port).
4. Tests in each package test ONLY that package's adapters against the port contract.
5. No circular dependencies. Turborepo enforces this at build time.

```
              ┌──────────────────────┐
              │      core/ports      │
              │  (interfaces only)   │
              └──────────┬───────────┘
                         │ implements
    ┌────────┬───────────┼───────────┬────────┬────────┐
    │        │           │           │        │        │
  art-i    art-ii     art-iii     art-iv    art-v   incident
 (I1-I6)  (status)  (evidence)  (agents) (amend)  (lifecycle)
```

## Repo Path

`/Users/coreyalejandro/Projects/sentinelos/`
GitHub: `github.com/coreyalejandro/sentinelos`
