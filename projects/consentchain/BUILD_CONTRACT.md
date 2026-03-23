# Build Contract: ConsentChain

## Current State (Honest)

- Turborepo monorepo at `consentchain/`
- 7 packages: shared, ledger, idempotency, policy-engine, vault-client, google-executor, step-up
- 1 app: apps/web (Next.js App Router)
- Total: 7 packages + 1 app = "8 packages" (matches claim if counting app)
- Prisma schema with SQLite: Agent, LedgerEntry, RevocationState, IdempotencyRecord, StepUpChallenge
- 7-stage gateway implemented: validation -> idempotency -> revocation -> policy -> step-up -> exec -> ledger
- Gateway curl-tested per HANDOFF.md
- Last commit: Mar 17, 2026

## Target State (What Resume Claims)

"Partial | 7-stage action gateway | Turborepo monorepo (8 packages) | Prisma schema | NextAuth/Auth0 | Docker deployment"

## Acceptance Criteria

1. `pnpm install` succeeds at repo root
2. `pnpm exec next dev --port 3000` starts in apps/web
3. Gateway curl tests from HANDOFF.md pass (idempotency, step-up, revocation)
4. Package count verified: 7 packages + 1 app
5. Prisma schema has required models

## Evidence Required

```bash
cd /Users/coreyalejandro/Projects/consentchain
pnpm install
ls packages/  # 7 packages
ls apps/      # 1 app (web)
cat prisma/schema.prisma | grep "^model"
# Test gateway
pnpm exec next dev --port 3000 &
curl -X POST http://localhost:3000/api/agent/action -H "Content-Type: application/json" -d '{"agentId":"test","action":"test","payload":{}}'
```

## Implementation Spec

No new code needed. Verification only.

## Repo Path

`/Users/coreyalejandro/Projects/consentchain/`
