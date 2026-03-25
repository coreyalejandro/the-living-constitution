# Adapters Strategy
## Platform-Agnostic Architecture for Constitutional Governance

---

## Core Principle

The Living Constitution is platform-agnostic. Governance rules are defined once in TLC and SentinelOS. Platform-specific implementations are adapters — they implement ports defined in the core, they never define governance themselves.

This means: switching from Claude to GPT-4 to Gemini to a local model does not change the Constitution. It changes the adapter. The governance stays the same. The ports stay the same. The invariants stay the same.

---

## Hexagonal Architecture Foundation

SentinelOS uses hexagonal architecture (ports and adapters pattern). This is not an arbitrary architectural choice — it is a constitutional enforcement mechanism. The hexagon creates a hard boundary between governance logic (inside) and vendor execution (outside).

```
                    ┌─────────────────────────────────┐
                    │                                   │
    Claude Code ────┤    Port: AgentExecutionPort       │
                    │         │                         │
    OpenAI GPT ─────┤    ┌────┴────┐                   │
                    │    │  CORE   │                    │
    Google Gemini ──┤    │ Invari- │   Port: AuditPort ├──── Audit Log
                    │    │  ants   │         │         │
    Local LLM ──────┤    │ I1-I6  │   Port: ConsentPort├──── ConsentChain
                    │    └────┬────┘         │         │
                    │         │              │         │
    GitLab CI ──────┤    Port: CIEnforcementPort       │
                    │                                   │
                    └─────────────────────────────────┘
                           SentinelOS Core
```

**Inside the hexagon:** Constitutional invariants, safety domain definitions, truth-status rules, V&T Statement requirements. These never change based on vendor.

**Outside the hexagon:** Vendor-specific adapters that implement the ports. Each adapter translates between the core's governance requirements and the vendor's API, execution model, and capabilities.

---

## Port Definitions

Ports are interfaces defined in `sentinelos/packages/core/src/ports/`. Each port declares what the governance layer requires without specifying how any particular vendor implements it.

### AgentExecutionPort

**Purpose:** Execute a governed action through an AI agent.

**Contract:**
- Accept a validated, authorized, consented action request.
- Execute the action using the vendor's agent capabilities.
- Return a structured result with success/failure status and output.
- Never execute an action that has not passed through the governance pipeline.

**Adapters:** Claude Code adapter, OpenAI adapter, Gemini adapter, local model adapter.

### CIEnforcementPort

**Purpose:** Run constitutional compliance checks in a CI/CD pipeline.

**Contract:**
- Accept a set of files and claims to verify.
- Run verification checks (build, test, truth-status, documentation divergence).
- Return a structured report with pass/fail per check and evidence.

**Adapters:** GitLab CI adapter (PROACTIVE), GitHub Actions adapter (planned), local CI adapter (planned).

### AuditPort

**Purpose:** Record an immutable audit trail of governed actions.

**Contract:**
- Accept an audit record with action, identity, authorization, consent, and result.
- Persist the record immutably.
- Provide query access to historical records.

**Adapters:** Prisma/PostgreSQL adapter (ConsentChain), file-based adapter (development), cloud storage adapter (planned).

### ConsentPort

**Purpose:** Obtain informed consent from a user for a governed action.

**Contract:**
- Present a clear, accessible description of the action.
- Collect explicit approval or rejection.
- Record the consent decision with timestamp and scope.
- Respect revocation at any time.

**Adapters:** UICare web adapter, CLI adapter (planned), API adapter (planned).

### CognitiveLoadPort

**Purpose:** Assess cognitive load of an output before delivery to a user.

**Contract:**
- Accept an output and user context.
- Return a load score and recommended pacing.
- If load exceeds threshold, return a simplified version.

**Adapters:** GPT-4o-mini adapter (UICare), heuristic adapter (fallback), rule-based adapter (minimal).

---

## Adapter Rules

1. **Adapters implement ports. They do not define governance.** An adapter can translate, transform, and execute. It cannot add, remove, or modify constitutional rules.

2. **Adapters are replaceable.** If a vendor changes their API, the adapter is updated. The port contract does not change. If a vendor is deprecated, the adapter is removed and a new one is written for the replacement vendor. The core is untouched.

3. **Adapters are tested against port contracts.** Every adapter must pass the port's contract test suite. The test suite is defined by the port, not the adapter. This ensures that all adapters for the same port are behaviorally equivalent.

4. **Adapters must not leak vendor abstractions into the core.** The core must not reference OpenAI-specific types, Claude-specific message formats, or Gemini-specific configuration. All vendor-specific types are defined within the adapter and mapped to core types at the boundary.

5. **Adapters handle vendor failures gracefully.** If a vendor API is unavailable, the adapter returns a structured error. The core decides how to handle the error (retry, fallback, fail safely). The adapter does not make governance decisions about failures.

6. **New adapters require a port contract review.** Before writing a new adapter, verify that the existing port contract is sufficient. If the new vendor requires capabilities not covered by the port, the port contract is extended through the Article V amendment process — not by the adapter unilaterally adding functionality.

---

## Adapter Lifecycle

```
1. Port defined in SentinelOS core
       │
       ▼
2. Contract test suite written for port
       │
       ▼
3. Adapter written for specific vendor
       │
       ▼
4. Adapter passes contract test suite
       │
       ▼
5. Adapter registered in adapter registry
       │
       ▼
6. Adapter available for runtime selection
       │
       ▼
7. Vendor changes API → Adapter updated → Re-run contract tests
       │
       ▼
8. Vendor deprecated → Adapter removed → New adapter written → Contract tests pass
```

---

## Current Adapter Status

| Port | Adapter | Vendor | Status |
|------|---------|--------|--------|
| AgentExecutionPort | Claude Code adapter | Anthropic | Partial — Claude Code is the primary execution environment, adapter formalization pending |
| CIEnforcementPort | PROACTIVE GitLab adapter | GitLab | Implemented — operational at Tier 2 |
| AuditPort | Prisma adapter | PostgreSQL/Prisma | Partial — ConsentChain audit package exists, port formalization pending |
| ConsentPort | UICare web adapter | Next.js/Browser | Partial — UICare consent UI exists, port formalization pending |
| CognitiveLoadPort | GPT-4o-mini adapter | OpenAI | Partial — UICare brain module exists, port formalization pending |

---

## V&T Statement
- **Exists:** Adapters strategy document describing hexagonal architecture foundation; five port definitions with contracts; six adapter rules; adapter lifecycle; current adapter status table
- **Non-existent:** Formalized port interfaces in SentinelOS TypeScript code; contract test suites for ports; adapter registry; GitHub Actions CI adapter; CLI consent adapter; API consent adapter
- **Unverified:** Whether SentinelOS packages/core/src/ports/ directory exists with port definitions; whether the hexagonal architecture pattern described here matches the actual SentinelOS codebase structure
- **Functional status:** Adapters strategy is fully specified — one adapter (PROACTIVE/GitLab) is operational at Tier 2; four others are partial with existing implementations awaiting port formalization
