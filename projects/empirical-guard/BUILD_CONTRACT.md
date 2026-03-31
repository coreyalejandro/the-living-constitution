# 📜 C-RSP EXECUTABLE BUILD CONTRACT

## Constitutionally-Regulated Single Pass Executable Prompt

---

## TEMPLATE METADATA

* **Template Version:** v2.1.0
* **Contract Version:** C-RSP-EMG-MVP-v1.0.0
* **Contract Role:** Executable build contract
* **Contract Class:** Application Build
* **Status:** EXECUTION-READY
* **Applicable Domain:** Empirical Safety
* **Authority Source:** `projects/c-rsp/BUILD_CONTRACT.md`
* **Governance Substrate:** TLC AI Governance System
* **Execution Mode:** Single pass only
* **Retry Policy:** Forbidden

> This document is executable. It is not a framework description. Execute exactly as written. Do not rename products. Do not broaden scope. Do not perform a second-pass refinement.

---

## 1. IDENTITY & DOMAIN

* **System Name:** EmpiricalGuard
* **System Role:** Deterministic empirical safety engine that ingests interaction telemetry, computes behavioral signals over rolling windows, derives a MoodSignal, and emits MoodSignal plus AdaptiveUI flag to downstream subscribers.
* **Contract Class:** Application Build
* **TLC Domain:** Empirical
* **Primary Objective:** Build the first working EmpiricalGuard MVP in the implementation repository with deterministic telemetry ingestion, rule-based signal derivation, honest truth-status reporting, and file-backed verification evidence.

---

## 2. CURRENT STATE & ENVIRONMENT (BASELINE)

* **Verified Assets (Must Exist):**

  * `projects/empirical-guard/BUILD_CONTRACT.md`
  * `MASTER_PROJECT_INVENTORY.json`
  * `config/projects.ts`
* **Implementation Checkout Must Exist:**

  * `/Users/coreyalejandro/Projects/empirical-guard`
* **Must NOT Exist:**

  * mock telemetry generators presented as real telemetry
  * fake “AI mood inference” language
  * biometric or clinical diagnosis logic
  * network-dependent backend services outside the local app stack
* **Generated Artifacts (Expected):**

  * `/Users/coreyalejandro/Projects/empirical-guard/app/page.tsx`
  * `/Users/coreyalejandro/Projects/empirical-guard/app/layout.tsx`
  * `/Users/coreyalejandro/Projects/empirical-guard/app/api/events/route.ts`
  * `/Users/coreyalejandro/Projects/empirical-guard/app/api/stream/route.ts`
  * `/Users/coreyalejandro/Projects/empirical-guard/lib/schemas/behavior-observation.ts`
  * `/Users/coreyalejandro/Projects/empirical-guard/lib/telemetry/ingest.ts`
  * `/Users/coreyalejandro/Projects/empirical-guard/lib/telemetry/windowing.ts`
  * `/Users/coreyalejandro/Projects/empirical-guard/lib/signals/derive-mood-signal.ts`
  * `/Users/coreyalejandro/Projects/empirical-guard/lib/signals/derive-adaptive-ui-flag.ts`
  * `/Users/coreyalejandro/Projects/empirical-guard/lib/store/event-store.ts`
  * `/Users/coreyalejandro/Projects/empirical-guard/lib/store/observation-store.ts`
  * `/Users/coreyalejandro/Projects/empirical-guard/lib/logging/logger.ts`
  * `/Users/coreyalejandro/Projects/empirical-guard/prisma/schema.prisma`
  * `/Users/coreyalejandro/Projects/empirical-guard/tests/unit/derive-mood-signal.test.ts`
  * `/Users/coreyalejandro/Projects/empirical-guard/tests/unit/derive-adaptive-ui-flag.test.ts`
  * `/Users/coreyalejandro/Projects/empirical-guard/tests/integration/events-route.test.ts`
  * `/Users/coreyalejandro/Projects/empirical-guard/tests/integration/stream-route.test.ts`
  * `/Users/coreyalejandro/Projects/empirical-guard/docs/truth-status.md`
  * `/Users/coreyalejandro/Projects/empirical-guard/docs/verification/acceptance-report.md`
* **Hermetic Baseline Policy:**

  * Do not modify TLC governance files.
  * Do not modify invariant registry outside additive mapping already defined by TLC.
  * Build only inside `/Users/coreyalejandro/Projects/empirical-guard`.
* **Hard Dependencies:**

  * **Node:** `20.x`
  * **Package Manager:** `pnpm`
  * **Framework:** `next@15.x`
  * **Language:** `typescript@5.x`
  * **UI:** `tailwindcss@4.x`
  * **Validation:** `zod@3.x`
  * **Logging:** `pino@9.x`
  * **Database:** `prisma@6.x` with PostgreSQL
  * **Unit Test:** `vitest@3.x`
  * **E2E / integration tooling:** `playwright@1.x`

### 2A. Dependency Policy

* **Conflict Resolution Rule:** If a dependency version differs materially from the pinned major version above, halt.
* **Availability Rule:** If a required package is unavailable, halt. No substitutions.
* **Vulnerability Rule:** Do not introduce known critical vulnerabilities. If install reports a critical vulnerability with no fix path, halt.

### 2B. Target Environment Profile

* **OS / Platform:** macOS development environment
* **Hardware Constraints:** N/A — no special hardware required
* **Network Policy:** Local development only; no external telemetry vendors

---

## 3. EXECUTION LOGIC (SINGLE-PASS PATH)

### Execution Steps

1. Confirm `/Users/coreyalejandro/Projects/empirical-guard` exists and is the only write target.
2. Initialize or normalize the repo as a Next.js App Router TypeScript application if not already structured that way.
3. Configure Tailwind, TypeScript strict mode, ESLint, Vitest, Playwright, Prisma, Zod, and Pino.
4. Create a Prisma schema for append-only raw telemetry events and derived behavior observations.
5. Implement Zod schemas for telemetry event input and final BehaviorObservation output.
6. Implement append-only raw event persistence.
7. Implement rolling 60-second window aggregation logic.
8. Implement deterministic computation for:

   * click velocity per minute
   * error rate per minute
   * longest idle seconds
   * rapid-sequence count
9. Implement deterministic MoodSignal derivation with exactly these levels:

   * `calm`
   * `stressed`
   * `crisis`
   * `unknown`
10. Implement deterministic AdaptiveUI flag derivation with exactly these values:

    * `standard`
    * `calm_mode`
    * `reduced_mode`

11. Implement `POST /api/events` to validate and persist incoming telemetry events.
12. Implement `GET /api/stream` as SSE for MoodSignal and AdaptiveUI emission.
13. Ensure graceful degradation when no subscribers are connected.
14. Build a minimal operator UI showing:

    * session behavior timeline
    * latest computed signals
    * latest MoodSignal
    * latest AdaptiveUI flag

15. Add JSON export capability for BehaviorObservation records.
16. Write unit and integration tests for deterministic rules, API validation, emission behavior, and degradation behavior.
17. Write `docs/truth-status.md` with honest current status only.
18. Write `docs/verification/acceptance-report.md` mapping every acceptance criterion to evidence.
19. Run tests and produce final verification artifacts.
20. Stop.

### 3A. Decision Closure

* **Allowed Decisions:**

  * choose exact folder placement within standard Next.js conventions
  * choose SSE over WebSocket for the first MVP
  * choose local PostgreSQL + Prisma implementation details
* **Prohibited Decisions:**

  * renaming EmpiricalGuard
  * changing TLC AI Governance System naming
  * introducing ML/LLM inference
  * using mock data as though it were real telemetry
  * changing MoodSignal taxonomy
  * changing AdaptiveUI flag taxonomy
  * adding backend microservices
  * modifying TLC governance files
* **Default on Ambiguity:** HALT
* **Retry Policy:** Forbidden

---

## 4. CONSTITUTIONAL INVARIANTS

### 4A. Invariant Categories

* Isolation Boundary
* Type / Schema Discipline
* Determinism / Idempotency
* Environment Constraints
* Security / Network Policy
* Data Handling / Privacy
* Observability / Evidence
* Naming Authority
* Terminology Authority

### 4B. Project-Specific Invariants

* **INVARIANT_NAME_01 — Product Naming Authority:** The product name is **EmpiricalGuard**. Do not rename it without explicit user approval.
* **INVARIANT_NAME_02 — Parent Platform Naming Authority:** Use **TLC AI Governance System** or approved shorthand **TLC** only. Do not substitute another canonical platform name.
* **INVARIANT_TERM_01 — C-RSP Canonical Expansion Authority:** C-RSP expands only to **Constitutionally-Regulated Single Pass** executable prompt.
* **INVARIANT_01 — Governance Isolation:** No modification to TLC governance files, STATUS.json, invariant registry, or constitutional source artifacts.
* **INVARIANT_02 — Deterministic Signal Derivation:** Same telemetry input and same baseline must always yield the same MoodSignal and AdaptiveUI flag.
* **INVARIANT_03 — Honest Status:** No implementation may claim clinical inference, biometric inference, or real-time psychological diagnosis.
* **INVARIANT_04 — Append-Only Raw Events:** Raw telemetry store is append-only.
* **INVARIANT_05 — Schema Discipline:** All inbound events and outbound observations must validate through Zod schemas.
* **INVARIANT_06 — Unknown on Insufficient Evidence:** Fewer than 10 events in window must yield `unknown`.
* **INVARIANT_07 — Local-First Evidence:** Verification evidence must be file-backed inside the implementation repo.
* **INVARIANT_08 — No Fake Liveness:** No UI may present simulated streaming, simulated telemetry, or simulated truth as real runtime output.
* **INVARIANT_09 — Graceful Degradation:** No subscriber connection may never cause runtime failure.
* **INVARIANT_10 — No Scope Expansion:** Build only the MVP defined in this contract.

---

## 5. CONFLICT RESOLUTION MATRIX

| Conflict Type                  | Protocol                                                                       | Severity | Action |
| ------------------------------ | ------------------------------------------------------------------------------ | -------: | ------ |
| Naming Authority Conflict      | Restore canonical product/platform naming and halt                             | Critical | Halt   |
| Terminology Authority Conflict | Restore canonical C-RSP expansion and halt                                     | Critical | Halt   |
| Dependency Conflict            | If pinned major versions are violated, halt                                    | Critical | Halt   |
| Schema Conflict                | If event/observation schemas diverge from contract taxonomy, halt              | Critical | Halt   |
| Runtime / Infra Conflict       | If implementation requires added backend services beyond local app stack, halt | Critical | Halt   |
| Security / Compliance Conflict | If code implies diagnosis, biometric inference, or unsafe claims, halt         | Critical | Halt   |
| Verification Conflict          | If any acceptance criterion lacks evidence, halt                               | Critical | Halt   |
| Truth-State Conflict           | If docs overclaim implementation status, halt                                  | Critical | Halt   |
| Contract Drift                 | If execution broadens beyond MVP scope, halt                                   | Critical | Halt   |

---

## 6. ACCEPTANCE CRITERIA (THE GAVEL)

| ID    | Category            | Requirement                                                                                                              | Verification Method                       |
| ----- | ------------------- | ------------------------------------------------------------------------------------------------------------------------ | ----------------------------------------- |
| AC-01 | Functional          | `POST /api/events` validates and persists supported telemetry events                                                     | integration test                          |
| AC-02 | Functional          | Rolling 60-second window computation works for click velocity, error rate, idle, and rapid sequence count                | unit test                                 |
| AC-03 | Functional          | MoodSignal derives exactly `calm`, `stressed`, `crisis`, or `unknown` using deterministic rules                          | unit test                                 |
| AC-04 | Functional          | AdaptiveUI flag derives exactly `standard`, `calm_mode`, or `reduced_mode`                                               | unit test                                 |
| AC-05 | Functional          | `GET /api/stream` emits derived signal updates through SSE                                                               | integration test                          |
| AC-06 | Functional          | Session behavior timeline renders from persisted observations                                                            | UI test or screenshot-backed verification |
| AC-07 | Functional          | BehaviorObservation export returns valid JSON                                                                            | integration test                          |
| AC-08 | Determinism         | Same input fixture executed 3 times yields identical derived outputs                                                     | repeated hash/value comparison            |
| AC-09 | Governance          | All product references use `EmpiricalGuard`; all parent-platform references use `TLC AI Governance System` or `TLC` only | string audit                              |
| AC-10 | Governance          | C-RSP expansion uses only Constitutionally-Regulated Single Pass                                                         | string audit                              |
| AC-11 | Safety / Governance | Documentation contains no clinical, biometric, or overclaimed psychological inference language                           | manual text audit                         |
| AC-12 | Safety / Governance | `< 10` events in window yields `unknown` with no false calm assumption                                                   | unit test                                 |
| AC-13 | Reliability         | No subscribers connected does not cause stream or derivation failure                                                     | integration test                          |
| AC-14 | Evidence            | `docs/truth-status.md` exists and honestly states built vs not built                                                     | file presence + text audit                |
| AC-15 | Evidence            | `docs/verification/acceptance-report.md` maps every acceptance criterion to evidence                                     | file presence + content audit             |
| AC-16 | Verification        | All required tests pass                                                                                                  | test run                                  |
| AC-17 | Scope Control       | No TLC governance files were modified                                                                                    | git diff audit                            |

---

## 7. PRE-FLIGHT VALIDATION (GATEKEEPER)

* **Validator Path:** local execution against this contract plus repository file checks
* **Execution Rule:** Must run before build

### Preflight Checks

* [ ] `/Users/coreyalejandro/Projects/empirical-guard` exists
* [ ] TLC governance files are outside write scope
* [ ] pinned toolchain versions are available
* [ ] PostgreSQL is available locally or via existing local configuration
* [ ] no forbidden backend service requirement has been introduced
* [ ] no placeholder text remains in execution artifacts

### Cleaning Policy

* **Dry Run Required:** YES
* **Protected Paths:**

  * `STATUS.json`
  * `projects/c-rsp/BUILD_CONTRACT.md`
  * all TLC governance files
* **Backup Required:** YES

### Logging

* **Log Path:** `/Users/coreyalejandro/Projects/empirical-guard/.c-rsp/CONFLICT_LOG.md`

---

## 8. VERIFICATION MAPPING (EVIDENCE MATRIX)

| Claim                                               | Evidence                               | Artifact Path                                                       |
| --------------------------------------------------- | -------------------------------------- | ------------------------------------------------------------------- |
| EmpiricalGuard MVP was built in implementation repo | app routes, libs, tests, prisma schema | `/Users/coreyalejandro/Projects/empirical-guard/*`                  |
| Telemetry ingestion is schema-validated             | Zod schemas + route tests              | `lib/schemas/*`, `tests/integration/events-route.test.ts`           |
| MoodSignal derivation is deterministic              | unit tests with repeated fixtures      | `tests/unit/derive-mood-signal.test.ts`                             |
| AdaptiveUI derivation is deterministic              | unit tests                             | `tests/unit/derive-adaptive-ui-flag.test.ts`                        |
| Streaming emission works                            | SSE route + integration tests          | `app/api/stream/route.ts`, `tests/integration/stream-route.test.ts` |
| Truth-status is honest                              | truth-status document audit            | `docs/truth-status.md`                                              |
| Acceptance is evidence-backed                       | acceptance report                      | `docs/verification/acceptance-report.md`                            |
| Naming authority preserved                          | string audit results                   | repository-wide scan within implementation repo                     |
| C-RSP terminology preserved                         | string audit results                   | repository-wide scan within implementation repo                     |
| TLC governance remained untouched                   | git diff audit                         | git status / diff evidence                                          |

---

## 9. GOVERNANCE MAPPING

* **Mapping File:** `/Users/coreyalejandro/Projects/empirical-guard/.c-rsp/governance-map.json`

Each module must define:

* constitutional reference
* invariant mapping
* verification hook

Minimum mappings:

* telemetry ingest → empirical accountability
* signal derivation → determinism / honest evidence
* stream emission → observability
* truth-status docs → status honesty
* verification report → evidence law

---

## 10. VERIFICATION ARTIFACT SCHEMA

```json
{
  "contract_version": "C-RSP-EMG-MVP-v1.0.0",
  "project_name": "EmpiricalGuard",
  "commit_hash": "",
  "environment": {
    "node": "20.x",
    "package_manager": "pnpm",
    "framework": "next@15.x"
  },
  "preflight_passed": true,
  "acceptance_results": [],
  "invariants_verified": [],
  "artifact_hashes": {},
  "exceptions": []
}
```

---

## 11. BREACH TAXONOMY

| Code     | Description                                        |
| -------- | -------------------------------------------------- |
| BREACH-A | Unauthorized execution outside implementation repo |
| BREACH-B | Invariant violation                                |
| BREACH-C | Unverifiable claim                                 |
| BREACH-D | Dependency deviation                               |
| BREACH-E | Non-determinism                                    |
| BREACH-F | Unauthorized rename                                |
| BREACH-G | Non-canonical C-RSP expansion                      |
| BREACH-H | Fake liveness or simulated truth presented as real |
| BREACH-I | Governance substrate modification                  |

---

## 12. HALT / PROCEED MATRIX

| Condition                                   | Severity | Action   |
| ------------------------------------------- | -------: | -------- |
| Placeholder present in executable artifacts | Critical | Halt     |
| Implementation repo missing                 | Critical | Halt     |
| Pinned dependency major version mismatch    | Critical | Halt     |
| TLC governance file enters diff             | Critical | Halt     |
| Unauthorized rename detected                | Critical | Halt     |
| Non-canonical C-RSP expansion detected      | Critical | Halt     |
| Required acceptance evidence missing        | Critical | Halt     |
| Fake telemetry presented as real            | Critical | Halt     |
| Optional UI polish missing                  |  Warning | Continue |
| Non-blocking styling inconsistency          |  Warning | Continue |

---

## 13. N/A DECLARATION RULE

All omitted sections must be filled as `N/A — explicit reason`. Silent omission is forbidden.

---

## 14. EXECUTION DIRECTIVE

Execute this build contract in one pass inside `/Users/coreyalejandro/Projects/empirical-guard`. Build the MVP only. Do not modify TLC governance artifacts. Do not rename products. Do not introduce external backend services. Do not simulate live systems. Do not perform retries or second-pass refinement. Stop immediately after the final verification artifacts are produced.

---

## END OF CONTRACT
