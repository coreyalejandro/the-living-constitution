# ConsentChain Agent Prompt Pack

## Purpose

This document contains self-contained prompts for uninterrupted build execution. Each prompt targets a specific phase of the ConsentChain zero-shot build contract. An agent receiving one of these prompts should be able to execute the phase without additional context or clarification.

---

## Prompt 1: Test Foundation

```
ROLE: TDD Guide Agent
PROJECT: ConsentChain — Empirical Safety authorization gateway
REPO: /Users/coreyalejandro/Projects/consentchain/
STACK: TypeScript 5.9, Turborepo, pnpm, Prisma 7 (SQLite), Vitest, jose

OBJECTIVE: Create comprehensive test suite achieving >= 80% coverage across all packages.

CONTEXT:
- Monorepo with 8 packages under packages/ and 1 app under apps/web/
- No tests exist anywhere in the repo
- All packages have "test": "echo no tests configured" in package.json

STEP 1: Install Vitest
- Add vitest, @vitest/coverage-v8 as root devDependencies
- Create root vitest.config.ts with workspace configuration
- Create per-package vitest.config.ts files
- Update each package.json "test" script to "vitest run --coverage"

STEP 2: Test packages/ledger/src/signer.ts
File: packages/ledger/src/__tests__/signer.test.ts
Test cases:
- canonicalJson produces identical output for objects with different key ordering
- canonicalJson handles arrays, nulls, booleans, numbers, nested objects
- sha256Hex produces consistent 64-character hex string for same input
- hmacSha256Hex produces consistent signature for same secret + message
- verifyHmacSha256Hex returns true for valid signature
- verifyHmacSha256Hex returns false for tampered message
- verifyHmacSha256Hex returns false for wrong secret
- stableStringify handles undefined, functions, symbols (edge cases)

STEP 3: Test packages/policy-engine/src/rules.ts
File: packages/policy-engine/src/__tests__/rules.test.ts
Test cases:
- evaluatePolicy allows listEvents with calendar.read scope (LOW risk)
- evaluatePolicy allows createEvent with calendar.write scope (MEDIUM risk)
- evaluatePolicy requires step-up for deleteAllEvents (HIGH risk)
- evaluatePolicy rejects unknown service
- evaluatePolicy rejects unknown operation for known service
- evaluatePolicy rejects missing scopes with descriptive reason
- evaluatePolicy returns specific missing scope names in reason string

STEP 4: Test packages/idempotency/src/store.ts
File: packages/idempotency/src/__tests__/store.test.ts
Test cases:
- Use mock PrismaClient (vi.fn() based)
- reserve() returns { kind: "miss" } for new actionId
- reserve() returns { kind: "hit", responseJson } for completed actionId
- reserve() returns { kind: "reserved" } for in-progress actionId
- check() returns { kind: "miss" } when no record exists
- check() returns { kind: "hit" } when record is COMPLETED
- complete() updates record status to COMPLETED with responseJson

STEP 5: Test apps/web gateway route
File: apps/web/src/app/api/agent/action/__tests__/route.test.ts
Test cases:
- Mock prisma, ledger, policy-engine, idempotency, google-executor
- Returns 401 when x-agent-key header missing
- Returns 401 when agent key not found in database
- Returns 403 when agent is DISABLED
- Returns 403 when service not in allowedServices
- Returns 409 when idempotency record is RESERVED
- Returns 200 with x-idempotent-replay when idempotency record is COMPLETED
- Returns 403 when service is revoked
- Returns 403 when policy denies with reason
- Returns 401 with challengeId when step-up required and no proof provided
- Returns 401 when step-up proof JWT is invalid
- Returns 200 and creates ledger entry for successful execution

STEP 6: Verify
- Run pnpm test from root
- Confirm all tests pass
- Confirm coverage >= 80% per package
- Run pnpm build to confirm nothing broke

CONSTRAINTS:
- No mutation patterns in test code. Use spread operators for test data.
- Each test file under 300 lines. Split into describe blocks per function.
- Mock Prisma client — do not use actual database in unit tests.
- Do not modify any existing source code unless fixing a type error exposed by tests.
```

---

## Prompt 2: Agent SDK Completion

```
ROLE: Builder Agent
PROJECT: ConsentChain — Empirical Safety authorization gateway
REPO: /Users/coreyalejandro/Projects/consentchain/
PACKAGE: packages/agent-sdk/

OBJECTIVE: Complete the Agent SDK with a typed client class that agents import to interact with ConsentChain.

CONTEXT:
- packages/agent-sdk/package.json exists with exports pointing to dist/client.js
- The gateway API is at POST /api/agent/action
- Supporting routes: GET /api/ledger, POST /api/revoke, POST /api/auth/step-up, POST /api/auth/step-up/verify
- Types are defined in packages/shared/src/types.ts

STEP 1: Create packages/agent-sdk/src/types.ts
Define:
- ConsentChainConfig: { baseUrl: string; agentKey: string; maxRetries?: number; retryDelayMs?: number }
- ExecuteActionParams: { actionId: string; service: string; operation: string; scopes: string[]; payload: unknown }
- ExecuteActionResult: { success: true; data: unknown; idempotentReplay: boolean } | { success: false; error: string; challengeId?: string }
- LedgerQueryParams: { agentId?: string; service?: string; limit?: number; offset?: number }
- RevokeParams: { agentId: string; service: string; reason?: string }

STEP 2: Create packages/agent-sdk/src/errors.ts
Define:
- ConsentChainError extends Error (base class with statusCode, errorCode)
- AuthenticationError (401 responses)
- AuthorizationError (403 responses)
- ConflictError (409 responses)
- StepUpRequiredError (401 with challengeId)
- ServerError (500 responses)

STEP 3: Create packages/agent-sdk/src/client.ts
ConsentChainClient class:
- Constructor takes ConsentChainConfig
- executeAction(params: ExecuteActionParams): Promise<ExecuteActionResult>
  - Sends POST to /api/agent/action with x-agent-key header
  - On 409: retry with exponential backoff up to maxRetries
  - On 401 with challengeId: throw StepUpRequiredError (caller handles step-up flow)
  - On 200: return { success: true, data, idempotentReplay: headers has x-idempotent-replay }
- queryLedger(params: LedgerQueryParams): Promise<LedgerEntry[]>
  - Sends GET to /api/ledger with query params
- revokeConsent(params: RevokeParams): Promise<void>
  - Sends POST to /api/revoke
- completeStepUp(challengeId: string, proof: string): Promise<string>
  - Sends POST to /api/auth/step-up/verify
  - Returns JWT for use in executeAction

STEP 4: Create tests
File: packages/agent-sdk/src/__tests__/client.test.ts
- Mock fetch globally
- Test executeAction happy path
- Test executeAction idempotent replay detection
- Test executeAction retry on 409
- Test executeAction throws StepUpRequiredError on 401 with challengeId
- Test queryLedger returns typed array
- Test revokeConsent sends correct payload

STEP 5: Verify
- pnpm build --filter=@consentchain/agent-sdk exits 0
- pnpm test --filter=@consentchain/agent-sdk exits 0 with >= 80% coverage

CONSTRAINTS:
- All methods are async. No synchronous I/O.
- No mutation. Config is readonly after construction.
- Client does not store state between calls (stateless).
- Retry logic uses immutable delay calculation: delay = baseDelay * 2^attempt.
```

---

## Prompt 3: Vault Client + Structured Errors

```
ROLE: Builder Agent
PROJECT: ConsentChain
REPO: /Users/coreyalejandro/Projects/consentchain/

OBJECTIVE: Replace placeholder vault client with env-based fallback. Add structured error hierarchy to shared package. Update gateway to use structured errors.

STEP 1: Create packages/shared/src/errors.ts
- ConsentChainError extends Error { statusCode: number; errorCode: string }
- ValidationError extends ConsentChainError (400)
- AuthenticationError extends ConsentChainError (401)
- AuthorizationError extends ConsentChainError (403)
- ConflictError extends ConsentChainError (409)
- ServerError extends ConsentChainError (500)
- Export all from packages/shared/src/index.ts

STEP 2: Update packages/vault-client/src/index.ts
- getSecret(key: string): string — reads from process.env, logs warning "vault not configured, using env fallback"
- getSecretOrThrow(key: string): string — reads from process.env, throws if missing
- isVaultConfigured(): boolean — returns false (env fallback mode)

STEP 3: Update apps/web/src/app/api/agent/action/route.ts
- Import error types from @consentchain/shared
- Replace inline { error: "string" } responses with structured error instances
- Use vault client for STEP_UP_SECRET and LEDGER_HMAC_SECRET retrieval
- Add idempotency cleanup: if execution fails, delete the reserved idempotency record

STEP 4: Tests for vault client and errors
- packages/vault-client/src/__tests__/vault.test.ts
- packages/shared/src/__tests__/errors.test.ts

STEP 5: Verify
- pnpm build exits 0
- pnpm test exits 0
- Gateway still handles all 7 stages correctly
```

---

## Prompt 4: Ledger Verification Endpoint

```
ROLE: Builder Agent
PROJECT: ConsentChain
REPO: /Users/coreyalejandro/Projects/consentchain/

OBJECTIVE: Add a verification endpoint that proves ledger entries have not been tampered with.

STEP 1: Create packages/ledger/src/verifier.ts
- verifyLedgerEntry(entry: { requestCanon: string; responseCanon: string; signature: string }, secret: string): { verified: boolean; reason?: string }
- Re-derive: sha256Hex(requestCanon) + "." + sha256Hex(responseCanon), then verifyHmacSha256Hex
- Return { verified: true } or { verified: false, reason: "signature_mismatch" }

STEP 2: Create apps/web/src/app/api/ledger/verify/route.ts
- POST handler accepting { entryId: string }
- Fetch LedgerEntry from Prisma by ID
- If not found: 404
- Call verifyLedgerEntry with LEDGER_HMAC_SECRET from vault client
- Return { verified, entry, reason }

STEP 3: Tests
- packages/ledger/src/__tests__/verifier.test.ts
- apps/web/src/app/api/ledger/verify/__tests__/route.test.ts

STEP 4: Verify
- pnpm build exits 0
- pnpm test exits 0
```

---

## Prompt 5: CI Pipeline

```
ROLE: Builder Agent
PROJECT: ConsentChain
REPO: /Users/coreyalejandro/Projects/consentchain/

OBJECTIVE: Create GitHub Actions CI pipeline.

STEP 1: Create .github/workflows/ci.yml
- name: ConsentChain CI
- on: push (main), pull_request (main)
- jobs:
  - quality:
    - runs-on: ubuntu-latest
    - steps: checkout, setup-node (20), setup-pnpm, install, lint, typecheck (tsc --noEmit), test (with coverage), build
    - cache pnpm store
    - fail on any step failure

STEP 2: Verify YAML is valid
- Check indentation
- Confirm all script names match package.json scripts

CONSTRAINTS:
- Single workflow file under 100 lines
- No secrets required for CI (SQLite is local, no Auth0 needed for tests)
```

---

## Prompt 6: Minimal Consent Dashboard UI

```
ROLE: Builder Agent
PROJECT: ConsentChain
REPO: /Users/coreyalejandro/Projects/consentchain/

OBJECTIVE: Build minimal consent dashboard for hackathon demonstration.

CONTEXT:
- Next.js App Router at apps/web/src/app/
- API routes already exist for ledger, revoke, and agent action
- No UI components exist yet
- Tailwind CSS available via Next.js defaults

STEP 1: Dashboard layout
- apps/web/src/app/layout.tsx — root layout with nav sidebar
- apps/web/src/app/page.tsx — dashboard home: agent count, recent entries, revocation count

STEP 2: Agent management
- apps/web/src/app/agents/page.tsx — list registered agents with status badges
- apps/web/src/components/AgentCard.tsx — single agent display

STEP 3: Ledger viewer
- apps/web/src/app/ledger/page.tsx — paginated ledger entries
- apps/web/src/components/LedgerTable.tsx — table with signature verification indicator
- apps/web/src/components/LedgerEntryRow.tsx — single row with expand for details

STEP 4: Revocation controls
- apps/web/src/app/revocations/page.tsx — active revocations + revoke form
- apps/web/src/components/RevocationPanel.tsx — revoke/restore controls

STEP 5: Accessibility
- All interactive elements have aria-labels
- Keyboard navigation for all controls
- Color contrast meets WCAG AA
- Focus indicators visible

STEP 6: Verify
- pnpm build exits 0
- Pages render without errors in dev mode
- All components under 200 lines

CONSTRAINTS:
- Server components by default. Client components only where interactivity is required.
- Fetch data from existing API routes. No direct Prisma imports in components.
- Immutable state: useState with spread, never direct mutation.
- No external UI libraries. Tailwind only.
```

---

## Prompt Usage Guide

| Phase | Prompt | Agent Type | Estimated Scope |
|-------|--------|------------|-----------------|
| 1 | Test Foundation | TDD Guide | 8-10 test files, vitest config |
| 2 | Agent SDK | Builder | 4 source files, 1 test file |
| 3 | Vault + Errors | Builder | 3 source files, 2 test files, 1 route update |
| 4 | Ledger Verification | Builder | 2 source files, 2 test files |
| 5 | CI Pipeline | Builder | 1 workflow file |
| 6 | Minimal UI | Builder | 8-10 component/page files |

Each prompt is self-contained. No prompt depends on reading another prompt. Dependencies between phases are sequential: Phase 1 must complete before Phase 2, etc. (See dependency graph in the build contract.)

An agent should execute one prompt at a time. After completing a prompt, verify acceptance criteria before proceeding to the next prompt.

---

V&T Statement
Exists: 6 self-contained agent prompts covering all phases of the ConsentChain build contract, with step-by-step instructions, file outputs, test cases, acceptance criteria, and constraints grounded in verified source code
Non-existent: Prompt execution results, test files, SDK client, vault implementation, CI pipeline, UI components
Unverified: Whether mock patterns described in test prompts will work with actual Prisma 7 typings, whether Next.js App Router test utilities are compatible with vitest
Functional status: Prompt pack is COMPLETE and ready for agent dispatch
