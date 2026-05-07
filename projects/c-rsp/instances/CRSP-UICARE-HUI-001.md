# BUILD CONTRACT INSTANCE
## Constitutionally-Regulated Single Pass Executable Prompt

> **Instance Status:** Active. This contract governs the hexagonal-architecture
> Behavioral Safety System monorepo for high-risk neurodivergent users. It does NOT
> claim clinical diagnostic capability, medical device status, or emergency-response
> functionality. The system is a local-first behavioral safety aid.

---
## 0. Instance Governance

- **Artifact Class:** Executable contract instance (Tier-2-Operational).
- **Canonical Expansion:** `C-RSP` = **Constitutionally-Regulated Single Pass** only (**INVARIANT_TERM_01**).
- **Schema Authority:** `projects/c-rsp/contract-schema.json` defines core section order; this file remains conformant.
- **Canonical master template:** `projects/c-rsp/BUILD_CONTRACT.md`
- **Outcome report shape:** `projects/c-rsp/CRSP_OUTCOME_TEMPLATE.md`
- **Governance overlay:** `projects/uicare-hui/BUILD_CONTRACT.md`

---
## 1. Contract Identity

- **Contract Title:** UICare-HUI — Behavioral Safety System for High-Risk Neurodivergent Users (Hexagonal Architecture Edition)
- **Contract ID:** CRSP-UICARE-HUI-001
- **Version:** v1.0.0
- **Schema Version:** 1.0.0
- **Status:** Active
- **Adoption Tier:** Tier-2-Operational
- **System Role:** Merges scattered UICare/HUI repositories into a single hexagonal-architecture monorepo that implements a fail-safe PWA behavioral safety system with consent-aware monitoring, local-first safety logic, and bounded non-clinical crisis-support behavior.
- **Primary Objective:** Produce a production-grade TypeScript monorepo where `packages/safety-core` is a pure, zero-dependency hexagonal core with deterministic safety logic, and `apps/pwa` is a Next.js 14 PWA that implements all core ports via concrete adapters.
- **Scope Boundary:** `/Users/coreyalejandro/Projects/uicare-hui` — all packages, apps, tests, docs, CI config, and governance artifacts within that monorepo. TLC overlay at `projects/uicare-hui/`. Source repos audited (not deleted): `UICare/`, `uicare-system/`, `HUI/`.
- **Not Claimed:** Not a medical device. Not an emergency-response system. Not a clinical diagnostic tool. No claim of production deployment. No claim that Azure OpenAI credentials are configured. No claim that `apps/pwa` next build passes CI. No claim that AuditLogger, DataLifecycle, or real SignalCollector adapters are implemented.

---
## 2. Contract Topology + Profile

- **Topology Mode:** Satellite
- **Profile Type:** Satellite
- **Profile Overlay Source:** `projects/uicare-hui/CLAUDE.md`
- **Verifier Class:** satellite-verifier
- **Authoritative Truth Surface:**
  - `projects/c-rsp/BUILD_CONTRACT.md` (canonical C-RSP master)
  - `projects/c-rsp/contract-schema.json`
  - `projects/c-rsp/instances/CRSP-UICARE-HUI-001.md` (this executed instance)
  - `projects/uicare-hui/STATUS.json`
  - `/Users/coreyalejandro/Projects/uicare-hui/STATUS.json` (implementation truth surface)
  - `/Users/coreyalejandro/Projects/uicare-hui/docs/governance-report.md`
- **Instance Artifact Path:** `projects/c-rsp/instances/CRSP-UICARE-HUI-001.md`
- **Governance Lock Path:** `projects/uicare-hui/STATUS.json`

### 2A. Profile Merge Rule

Base constitutional template governs this instance. No profile may override canonical
C-RSP terminology, section order, truth discipline, halt matrix, or acceptance criteria rigor.

### 2B. Instance Rule

Executable only when: no unresolved placeholders; acceptance criteria are objective;
evidence paths are concrete; commands are deterministic and runnable on macOS with the
repo's declared tooling (Node.js v22, npm 11, TypeScript 5).

---
## 3. Baseline State

- **Existing Repo / System:** `/Users/coreyalejandro/Projects/uicare-hui` — local monorepo, git initialized, initial commit landed. No GitHub remote yet.
- **Baseline Commit / Anchor:** Initial commit — "feat: C-RSP hexagonal architecture initial build"
- **Verified Existing Assets:**
  - `packages/safety-core/` built successfully (exit 0)
  - 72/72 automated tests passing (57 unit + 15 governance)
  - 7 port interfaces, full behavioral/safety/consent domain logic
  - 11 invariants implemented as typed assertion functions
  - PWA adapters, UI components, service worker written
  - CI workflow (5 jobs) written
  - 6 governance spec documents (5 APPROVED, governance-report.md DRAFT)
- **Known Constraints:**
  - `apps/pwa` next build not CI-verified
  - AuditLogger IndexedDB adapter not written
  - DataLifecycle adapter not written
  - Real SignalCollector (wearable/UI events) not written
  - Playwright accessibility tests not written
  - GitHub remote not created; inventory not updated
- **Known Gaps:** Identified under "Not Claimed" above and in VERIFIED GAPS of original build contract.
- **Legacy Migration Context:** Code salvaged from `UICare/portfolio-uicare`, `uicare-system/web`, `HUI/packages/` and re-homed into appropriate adapter layers. `maniaService.ts` math → `risk-scorer.ts`. AES-256-GCM encryption → `encryption.ts` adapter. Azure OpenAI detect-loop logic → `AzureOpenAIAdvisor.ts` adapter.

---
## 4. Dependencies and Inputs

- **Required Inputs:** This instance file; `projects/c-rsp/*` canonical artifacts; local monorepo at `/Users/coreyalejandro/Projects/uicare-hui`.
- **External Dependencies:**
  - Node.js v22.11.0, npm 11.0.0
  - TypeScript 5 (devDependency of safety-core)
  - Vitest 1.6.1 (devDependency of safety-core)
  - Next.js 14, React 18 (apps/pwa — infrastructure adapters)
  - Optional: Azure OpenAI (env vars AZURE_OPENAI_ENDPOINT, AZURE_OPENAI_KEY, AZURE_OPENAI_DEPLOYMENT)
  - Optional: ENCRYPTION_KEY env var for AES-256-GCM
- **Governance Dependencies:** TLC constitutional articles for V&T discipline.
- **Forbidden Assumptions:**
  - Do not assume Azure credentials are configured.
  - Do not assume wearable hardware is available.
  - Do not assume `apps/pwa` builds without a Next.js-specific test run.
  - Do not assume `npm run lint:boundaries` has passed without running it.

### 4A. Cross-Repo Governance Dependency Graph

```
projects/c-rsp/BUILD_CONTRACT.md  [canonical master — supreme authority]
  └── projects/c-rsp/instances/CRSP-UICARE-HUI-001.md  [this instance]
        └── projects/uicare-hui/BUILD_CONTRACT.md  [governance overlay]
              └── /Users/coreyalejandro/Projects/uicare-hui/  [implementation]
```

---
## 5. Risk + Control Classification

| Risk | Severity | Control |
|------|----------|---------|
| Clinical language in user-facing copy | HIGH | INVARIANT_008 enforced in intervention copy docs + test |
| Safety gate bypass via AI failure | HIGH | NULL_AI_ADVISOR pattern — AI down never disables gates |
| Monitoring without consent | HIGH | INVARIANT_001 runtime enforcement in consent-enforcer.ts |
| Architectural drift (safety-core imports infra) | MEDIUM | INVARIANT_011 ESLint CI boundary lint |
| HARD_BLOCK override path | HIGH | INVARIANT_003 — no override at gate level 3 |
| Data retention / GDPR | MEDIUM | DataLifecycle port defined; adapter NOT YET WRITTEN |
| AuditLogger adapter gap | MEDIUM | Port defined, IndexedDB adapter pending |
| apps/pwa TypeScript regression | LOW | next build job in CI; not yet run |

---
## 6. Execution Model

- **Execution Mode:** Phased build (Phases 0–8)
- **Phase Status:** All 9 phases executed per build contract
- **Safety Specification Gate (Phase 1.5):** PASSED — 5 of 6 spec docs APPROVED; governance-report.md DRAFT
- **Test Gate:** PASSED — 72/72 tests
- **Build Gate:** PASSED — safety-core TypeScript exit 0
- **Boundary Lint Gate:** PENDING — `npm run lint:boundaries` not yet run locally
- **GitHub Remote Gate:** PENDING — no remote exists
- **Inventory Gate:** PENDING — MASTER_PROJECT_INVENTORY.json not yet updated

---
## 7. Lifecycle State Machine

```
DRAFT → SPEC_GATE_PASSED → TESTS_PASSING → BUILD_CLEAN → REMOTE_PUSHED → INVENTORY_REGISTERED → ACTIVE
```

Current state: `BUILD_CLEAN` (tests passing, build clean, boundary lint + remote pending)

---
## 8. Invariants

### Architectural Invariant (INVARIANT_011)
`packages/safety-core` must contain zero runtime dependencies. It must not import from
`apps/*`, `packages/*` (other than itself), or any browser/Node.js-specific module.
Enforced by CI ESLint boundary lint. Violations halt the build.

### Runtime Safety Invariants (INVARIANT_001 through INVARIANT_010)
Defined and enforced in `packages/safety-core/src/invariants.ts`.
Tested in `packages/safety-core/tests/invariants.test.ts` (24 tests) and
`tests/governance/invariants.test.ts` (15 end-to-end tests).

Key invariants:
- INVARIANT_001: Monitoring requires ConsentRecord.status === 'GRANTED'
- INVARIANT_003: HARD_BLOCK state has no override path
- INVARIANT_008: Zero clinical language in user-facing copy
- INVARIANT_009: AI unavailability must not disable local safety gates

### TLC Invariant (INVARIANT_TERM_01)
C-RSP = Constitutionally-Regulated Single Pass. No other expansion permitted.

---
## 9. Acceptance Criteria

1. [VERIFIED] `packages/safety-core` builds with zero runtime dependencies — `npm run build` exit 0
2. [VERIFIED] 72/72 automated tests pass
3. [PENDING] CI boundary lint confirms INVARIANT_011 — `npm run lint:boundaries` must exit 0
4. [PARTIAL] Safety Specification gate — 5/6 docs APPROVED; governance-report.md DRAFT
5. [PENDING] GitHub remote created and all commits pushed
6. [PENDING] `uicare-hui` slug registered in MASTER_PROJECT_INVENTORY.json
7. [PENDING] CLAUDE.md Project Registry table updated
8. [PENDING] governance-report.md signed off (SPEC_006 → APPROVED)
9. [PENDING] `apps/pwa` next build verified

---
## 10. Rollback & Recovery

Per-phase git tags strategy (as defined in original build contract):
- `phase-0-scaffold`, `phase-1-migration`, `phase-2-safety-core`, etc.
- Core regressions can be isolated to `packages/safety-core` commits
- Recovery: `git checkout <phase-tag>` in implementation repo
- TLC overlay files are independent of implementation repo — rollback does not affect overlay

---
## 11. Evidence + Truth Surface

| Artifact | Path | Status |
|----------|------|--------|
| Safety-core build output | `/Users/coreyalejandro/Projects/uicare-hui/packages/safety-core/dist/` | VERIFIED — exit 0 |
| Unit test results | `/Users/coreyalejandro/Projects/uicare-hui/packages/safety-core/tests/` | VERIFIED — 57/57 |
| Governance test results | `/Users/coreyalejandro/Projects/uicare-hui/tests/governance/` | VERIFIED — 15/15 |
| Behavioral state spec | `/Users/coreyalejandro/Projects/uicare-hui/docs/behavioral-state-spec.md` | APPROVED |
| Consent flow spec | `/Users/coreyalejandro/Projects/uicare-hui/docs/consent-flow-spec.md` | APPROVED |
| Intervention copy | `/Users/coreyalejandro/Projects/uicare-hui/docs/intervention-copy.md` | APPROVED |
| Not-claimed boundary | `/Users/coreyalejandro/Projects/uicare-hui/docs/not-claimed-boundary.md` | APPROVED |
| Hexagonal boundaries | `/Users/coreyalejandro/Projects/uicare-hui/docs/hexagonal-boundaries.md` | APPROVED |
| Governance report | `/Users/coreyalejandro/Projects/uicare-hui/docs/governance-report.md` | DRAFT |
| Port interfaces | `/Users/coreyalejandro/Projects/uicare-hui/packages/safety-core/src/ports/` | VERIFIED — 7 ports |
| Implementation STATUS | `/Users/coreyalejandro/Projects/uicare-hui/STATUS.json` | ACTIVE |
| TLC overlay STATUS | `projects/uicare-hui/STATUS.json` | ACTIVE |
| CI workflow | `/Users/coreyalejandro/Projects/uicare-hui/.github/workflows/ci.yml` | WRITTEN — not yet run on remote |

---
## 12. Conflict Matrix

| Conflict | Resolution |
|----------|-----------|
| AI advisor returns null vs gate must decide | NULL_AI_ADVISOR: gate uses local-only assessment |
| Cold-start window vs gate evaluation | Gates suppressed during COLD_START_OBSERVATION_WINDOW_MS (1h) |
| Consent revoked mid-session vs active monitoring | consent-enforcer.ts applyRevocation() halts all signal collection immediately |
| HARD_BLOCK override request vs INVARIANT_003 | INVARIANT_003 wins — no override path at gate level 3 |
| TLC canonical master vs this instance | Canonical master controls (C-RSP authority order §0) |

---
## 13. Halt Matrix

| Condition | Halt Action |
|-----------|------------|
| `packages/safety-core` found to have runtime dependency | CI lint fails build; merge blocked |
| Core cannot be tested without browser/Node stubs | Build contract violation; halt execution |
| governance-report.md not signed before SPEC_006 APPROVED claimed | SPEC_006 remains DRAFT; gate blocks behavioral-state implementation |
| MASTER_PROJECT_INVENTORY.json not updated | TLC topology verifier fails; drift flagged |
| AI adapter imports into safety-core | INVARIANT_011 ESLint violation; CI blocks merge |
| HARD_BLOCK state override attempted | INVARIANT_003 assertion fires; override rejected |
| ConsentRecord.status !== 'GRANTED' at monitoring activation | INVARIANT_001 assertion fires; monitoring blocked |

---
## 14. Preflight

Before executing any new work on this contract:

1. Confirm `/Users/coreyalejandro/Projects/uicare-hui` is on expected branch
2. Run `npm run test` from monorepo root — confirm 72/72
3. Run `npm run build` in `packages/safety-core` — confirm exit 0
4. Check `projects/uicare-hui/STATUS.json` — confirm `status: active`
5. Run `python3 scripts/verify_project_topology.py --root . --no-probes` from TLC root — confirm exit 0

---
## 15. Adoption Tiers

- **Tier-1-MVG:** `packages/safety-core` builds + 72/72 tests pass — ACHIEVED
- **Tier-2-Operational:** GitHub remote pushed + inventory registered + governance-report.md signed — PENDING
- **Tier-3-Constitutional:** Full CI run on remote (all 5 jobs green) + Playwright tests + AuditLogger/DataLifecycle adapters — FUTURE

---
## 16. Output Format

Governance artifacts:
- `projects/uicare-hui/CLAUDE.md` — governance overlay (written)
- `projects/uicare-hui/BUILD_CONTRACT.md` — project-scope overlay (written)
- `projects/uicare-hui/STATUS.json` — TLC-side status (written)
- `projects/c-rsp/instances/CRSP-UICARE-HUI-001.md` — this executed instance (written)
- MASTER_PROJECT_INVENTORY.json — to be updated with `uicare-hui` slug
- CLAUDE.md Project Registry table — to be updated

Implementation artifacts documented in `/Users/coreyalejandro/Projects/uicare-hui/`.

---
## 17. Instance Declaration

This file is an **executed contract instance** of the C-RSP canonical master template.
It governs the UICare-HUI behavioral safety system monorepo under TLC authority.

- Executed by: Hermes Agent (coreyalejandro session)
- Execution date: 2026-05-07
- TLC repository: coreyalejandro/the-living-constitution
- Implementation repository: /Users/coreyalejandro/Projects/uicare-hui (GitHub remote pending)
- Governing articles: THE_LIVING_CONSTITUTION.md Articles I–V
- Authority chain: TLC supreme → C-RSP canonical → this instance → governance overlay

---

## V&T Statement

EXISTS (verified present):
- `projects/uicare-hui/CLAUDE.md` — governance overlay
- `projects/uicare-hui/BUILD_CONTRACT.md` — project scope overlay
- `projects/uicare-hui/STATUS.json` — TLC status
- `projects/c-rsp/instances/CRSP-UICARE-HUI-001.md` — this instance
- `/Users/coreyalejandro/Projects/uicare-hui/` — implementation monorepo, local git commit

VERIFIED AGAINST:
- `projects/c-rsp/contract-schema.json` schema section order (18 sections, §0–§17)
- Existing executed instances (CRSP-SEMGRAPH-001.md format reference)
- Build contract build/test results: 72/72 passing, safety-core exit 0

NOT CLAIMED:
- GitHub remote does not exist yet
- `uicare-hui` not yet in MASTER_PROJECT_INVENTORY.json
- governance-report.md is DRAFT — SPEC_006 not APPROVED
- `apps/pwa` next build not CI-verified
- AuditLogger, DataLifecycle, real SignalCollector adapters not written
- Playwright tests not written
- `npm run lint:boundaries` not yet run

FUNCTIONAL STATUS:
- Tier-1-MVG achieved (build + tests)
- Tier-2-Operational pending (remote + inventory + governance sign-off)
- TLC governance overlay written and ready to commit to TLC repo
