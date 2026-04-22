# ConsentChain Zero-Shot Build Contract

## Contract Metadata

| Field | Value |
|-------|-------|
| System | ConsentChain |
| Domain | Empirical Safety |
| Current Status | Partial |
| Target Status | Validated |
| Contract Type | Completion — scaffold exists, wiring and testing required |
| Repo Path | `/Users/coreyalejandro/Projects/consentchain/` |
| Stack | Next.js 15 (App Router), Turborepo, pnpm, Prisma 7 (SQLite), TypeScript 5.9, jose, better-sqlite3 |

## What Exists (Verified by Source Inspection)

### Monorepo Infrastructure
- Root `package.json` with Turborepo build/dev/lint/test scripts
- `pnpm-workspace.yaml` declaring `apps/*` and `packages/*`
- `turbo.json` with pipeline for build, dev, lint, test
- TypeScript 5.9, Prisma 7, better-sqlite3 at root level

### Application Layer (apps/web)
- Next.js App Router at `apps/web/src/app/`
- NextAuth/Auth0 route at `apps/web/src/app/api/auth/[...nextauth]/route.ts`
- Prisma client singleton at `apps/web/src/lib/prisma.ts` using BetterSqlite3 adapter
- `.env.local` with database URL and blank Auth0 credentials

### API Routes (All Implemented)
- `POST /api/agent/action` — full 7-stage gateway (168 lines, working)
- `POST /api/auth/step-up` — step-up challenge creation
- `POST /api/auth/step-up/verify` — step-up JWT verification
- `GET /api/ledger` — consent ledger query
- `POST /api/revoke` — consent revocation
- `POST /api/services/connect/google` — 501 placeholder

### Packages (All Scaffolded, All Build)
- `@consentchain/shared` — types.ts (50 lines), constants.ts
- `@consentchain/ledger` — signer.ts (48 lines): canonicalJson, sha256Hex, hmacSha256Hex, verifyHmacSha256Hex
- `@consentchain/policy-engine` — rules.ts (46 lines): evaluatePolicy with allowlists, risk classification, scope checks
- `@consentchain/idempotency` — store.ts (36 lines): IdempotencyStore class with check/reserve/complete
- `@consentchain/step-up` — legacy in-memory (superseded by DB-backed step-up in web app)
- `@consentchain/agent-sdk` — client SDK scaffold
- `@consentchain/vault-client` — throws until configured
- `@consentchain/google-executor` — mock executor

### Data Layer
- Prisma schema with 5 models: Agent, LedgerEntry, RevocationState, IdempotencyRecord, StepUpChallenge
- Migration history applied
- SQLite dev.db (77KB) with existing data

## What Does Not Exist (Gaps for Completion)

| Gap ID | Component | Current State | Required State |
|--------|-----------|---------------|----------------|
| G1 | Test suite | No tests in any package | Unit tests for all 8 packages, integration tests for API routes |
| G2 | Google executor | Mock returning 501 | Real Google Calendar API integration OR comprehensive mock with realistic responses |
| G3 | Vault client | Throws on any call | Functional secrets retrieval (at minimum, env-based fallback) |
| G4 | Agent SDK client | Scaffold only | Typed client with request builder, error handling, retry logic |
| G5 | Auth0 configuration | Blank env vars | Working Auth0 tenant OR alternative auth provider |
| G6 | UI layer | No frontend | Minimal consent dashboard: agent list, ledger viewer, revocation controls |
| G7 | CI/CD pipeline | None | GitHub Actions: lint, type-check, test, build |
| G8 | Error recovery | Basic try/catch | Structured error types, idempotency cleanup on failure |
| G9 | Ledger verification | Write-only | Verification endpoint: given a ledger entry, re-derive and check HMAC |
| G10 | Rate limiting | None | Per-agent rate limits on action gateway |

## Build Phases

### Phase 1: Test Foundation (Priority: Critical)

**Objective:** Achieve 80% coverage across all packages.

**File outputs:**
```
packages/ledger/src/__tests__/signer.test.ts
packages/policy-engine/src/__tests__/rules.test.ts
packages/idempotency/src/__tests__/store.test.ts
packages/shared/src/__tests__/types.test.ts
packages/step-up/src/__tests__/challenge.test.ts
apps/web/src/app/api/agent/action/__tests__/route.test.ts
apps/web/src/app/api/ledger/__tests__/route.test.ts
apps/web/src/app/api/revoke/__tests__/route.test.ts
apps/web/src/app/api/auth/step-up/__tests__/route.test.ts
vitest.config.ts (root)
packages/*/vitest.config.ts (per-package)
```

**Acceptance criteria:**
- `pnpm test` passes with exit code 0
- Coverage report shows >= 80% line coverage per package
- Signer tests verify canonical JSON stability, SHA-256 output, HMAC signing, timing-safe comparison
- Policy engine tests cover all 3 operations, scope validation, risk classification, step-up triggering
- Idempotency tests verify miss/reserve/hit/complete lifecycle with mock Prisma client
- Gateway integration tests verify all 7 stages with mocked Prisma and executor

### Phase 2: Agent SDK Completion (Priority: High)

**Objective:** Ship a typed client that agents can import and use.

**File outputs:**
```
packages/agent-sdk/src/client.ts        — ConsentChainClient class
packages/agent-sdk/src/types.ts         — Request/response types
packages/agent-sdk/src/errors.ts        — Typed error classes
packages/agent-sdk/src/__tests__/client.test.ts
```

**Acceptance criteria:**
- `ConsentChainClient` class with typed methods: `executeAction()`, `queryLedger()`, `revokeConsent()`
- Automatic retry on 409 (action in progress) with exponential backoff
- Step-up flow handled: client detects 401 with challengeId, calls step-up verify, retries with JWT
- All methods return typed responses matching `@consentchain/shared` types
- Tests cover happy path, error paths, retry logic, step-up flow

### Phase 3: Vault Client + Error Recovery (Priority: Medium)

**Objective:** Replace placeholder vault client with functional secrets retrieval. Add structured error handling.

**File outputs:**
```
packages/vault-client/src/index.ts      — Env-based fallback with vault readiness
packages/vault-client/src/types.ts      — Secret types
packages/vault-client/src/__tests__/vault.test.ts
packages/shared/src/errors.ts           — ConsentChainError hierarchy
apps/web/src/app/api/agent/action/route.ts — Updated with structured errors
```

**Acceptance criteria:**
- Vault client reads from env vars as fallback, logs warning about vault not configured
- ConsentChainError base class with subtypes: ValidationError, AuthorizationError, PolicyError, LedgerError, IdempotencyError
- Gateway route uses structured errors instead of inline string messages
- Idempotency cleanup on execution failure (mark record as failed, allow retry)

### Phase 4: Ledger Verification Endpoint (Priority: Medium)

**Objective:** Add read-side verification to complement write-side ledger.

**File outputs:**
```
apps/web/src/app/api/ledger/verify/route.ts  — Verification endpoint
packages/ledger/src/verifier.ts               — Verification logic
packages/ledger/src/__tests__/verifier.test.ts
```

**Acceptance criteria:**
- `POST /api/ledger/verify` accepts a ledger entry ID
- Re-derives HMAC from stored requestCanon + responseCanon
- Returns `{ verified: true/false, entry: LedgerEntry }`
- If signature does not match, returns `{ verified: false, reason: "signature_mismatch" }`
- Tests cover valid entry, tampered entry, missing entry

### Phase 5: CI Pipeline (Priority: Medium)

**Objective:** Automated quality gates on every push.

**File outputs:**
```
.github/workflows/ci.yml
```

**Acceptance criteria:**
- Triggers on push to main and pull requests
- Steps: install, lint, type-check (tsc --noEmit), test (with coverage), build
- Fails on type errors, lint errors, test failures, or coverage below 80%
- Caches pnpm store for performance

### Phase 6: Minimal UI (Priority: Low)

**Objective:** Consent dashboard for demonstration and hackathon presentation.

**File outputs:**
```
apps/web/src/app/page.tsx                    — Dashboard landing
apps/web/src/app/agents/page.tsx             — Agent list
apps/web/src/app/ledger/page.tsx             — Ledger viewer
apps/web/src/app/revocations/page.tsx        — Revocation controls
apps/web/src/components/AgentCard.tsx
apps/web/src/components/LedgerTable.tsx
apps/web/src/components/RevocationPanel.tsx
```

**Acceptance criteria:**
- Dashboard shows agent count, recent ledger entries, active revocations
- Agent list shows registered agents with status badges
- Ledger viewer shows paginated entries with signature verification status
- Revocation panel allows revoking and restoring agent-service pairs
- All components use immutable state patterns
- Accessible: keyboard navigation, screen reader labels, sufficient contrast

## Dependency Order

```
Phase 1 (Tests)
    |
    v
Phase 2 (Agent SDK) -----> Phase 3 (Vault + Errors)
    |                            |
    v                            v
Phase 4 (Verification) --> Phase 5 (CI)
                                |
                                v
                          Phase 6 (UI)
```

## Execution Rules

1. No phase starts without the prior phase's acceptance criteria met.
2. Every file created must have a corresponding test file (except config files).
3. No mutation patterns. Immutable state everywhere.
4. Every API route handles errors comprehensively with user-friendly messages.
5. No hardcoded secrets. All sensitive values from environment variables.
6. Files stay under 400 lines. Extract when approaching 300.
7. Run `pnpm build` after each phase. Build must pass.
8. Run `pnpm test` after each phase. All tests must pass.

## Success Definition

ConsentChain is **Validated** when:
- All 6 phases complete with acceptance criteria met
- `pnpm build` exits 0 across all packages
- `pnpm test` exits 0 with >= 80% coverage
- The 7-stage gateway passes end-to-end integration test
- Ledger entries can be independently verified via the verification endpoint
- Agent SDK can execute a full action lifecycle: create agent, execute action, query ledger, verify entry, revoke consent

---

V&T Statement
Exists: Zero-shot build contract with 6 phases, 10 identified gaps, file output lists, acceptance criteria, dependency ordering, and execution rules grounded in verified source inspection
Non-existent: Test suite, real Google executor, functional vault client, agent SDK client, Auth0 configuration, UI layer, CI pipeline, ledger verification endpoint
Unverified: Build times for full monorepo CI, coverage achievability for gateway integration tests with mocked Prisma
Functional status: Contract is COMPLETE and ready for zero-shot execution by a build agent
