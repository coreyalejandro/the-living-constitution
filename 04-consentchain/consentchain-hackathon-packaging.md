# ConsentChain Hackathon Packaging

## Elevator Pitch

ConsentChain is an authorization gateway that makes AI agent consent verifiable, auditable, and revocable. It transforms "we had permission" from a claim into a cryptographic evidence chain. Every agent action flows through a 7-stage pipeline: validation, canonicalization, idempotency, revocation check, policy evaluation, execution, and ledger recording. The result is a tamper-evident audit trail that answers: who authorized what, when, for what scope, and whether it was later revoked.

## Problem Statement (2 minutes)

AI agents act on behalf of users every day. They schedule meetings, access calendars, read emails, and execute tasks. But when something goes wrong — an unwanted meeting, a deleted calendar, a data access violation — the question is always the same: "Did the user consent to this?"

The answer today is almost always: "We configured it that way" or "The user agreed to our terms of service." That is not consent. That is assumption. There is no audit trail. There is no revocation mechanism. There is no evidence chain.

This is an Empirical Safety failure. The described state of the system ("user consented") does not match the actual state ("we assumed consent and never recorded it").

ConsentChain closes that gap.

## Solution Demo Flow (5 minutes)

### Demo 1: The Happy Path

```
1. Register an agent with ConsentChain (show Agent model in Prisma)
2. Agent requests: "List calendar events for user"
   - Show x-agent-key header authentication
   - Show policy engine evaluating: service=google, operation=listEvents, scopes=[calendar.read]
   - Policy returns: allowed=true, risk=LOW
   - Execution succeeds
   - Show ledger entry created with cryptographic signature
3. Query the ledger: show the full evidence chain
   - actionId, agentId, service, operation
   - requestHash, responseHash, HMAC signature
   - Timestamp
```

### Demo 2: Revocation

```
1. Revoke the agent's access to google service
   - POST /api/revoke with agentId + service
   - Show RevocationState record created
2. Agent tries the same request again
   - Pipeline reaches Stage 3 (Revocation Check)
   - Returns 403: "service revoked"
   - No execution. No ledger entry. Fail closed.
3. The question "did the user consent?" has an answer:
   - Yes, they did — here is the ledger entry from Demo 1
   - Then they revoked it — here is the revocation record
   - The agent was blocked — here is the 403 response
```

### Demo 3: High-Risk Step-Up

```
1. Agent requests: "Delete all calendar events"
   - Policy engine evaluates: operation=deleteAllEvents, risk=HIGH
   - Returns: stepUpRequired=true
   - Gateway returns 401 with challengeId
2. Show step-up challenge flow:
   - Challenge created in StepUpChallenge table (single-use)
   - User completes verification (simulated)
   - JWT proof generated and signed with STEP_UP_SECRET
3. Agent retries with stepUpProofJwt
   - JWT verified, challenge marked as used (usedAt set)
   - Execution proceeds
   - Ledger entry created
4. Try to reuse the same step-up proof
   - Returns 401: "challenge already used"
   - Single-use enforcement prevents replay attacks
```

### Demo 4: Idempotency

```
1. Agent sends an action request with actionId "abc-123"
   - IdempotencyStore reserves the actionId
   - Execution runs, ledger entry created
   - IdempotencyStore marked COMPLETED with responseJson
2. Agent sends the exact same request again (same actionId)
   - IdempotencyStore finds COMPLETED record
   - Returns cached response with x-idempotent-replay: true header
   - No duplicate execution. No duplicate ledger entry.
3. Constitutional principle demonstrated:
   - Same input, same output, every time
   - The user cannot break things by trying again
```

## Architecture Slide

```
┌─────────────────────────────────────────────────────────────┐
│                    ConsentChain Architecture                  │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  Agent Request (x-agent-key + action payload)                │
│       │                                                       │
│       ▼                                                       │
│  ┌──────────────────────────────────────────────────────┐    │
│  │           7-Stage Action Gateway                      │    │
│  │                                                       │    │
│  │  1. Agent Validation     SHA-256 key lookup          │    │
│  │  2. Canonicalization     Stable JSON + idempotency   │    │
│  │  3. Revocation Check     Per-agent, per-service      │    │
│  │  4. Policy Evaluation    Allowlists + risk + scopes  │    │
│  │  5. Step-Up Auth         JWT challenges (single-use) │    │
│  │  6. Execution            Service executor dispatch    │    │
│  │  7. Ledger Write         HMAC-signed evidence chain  │    │
│  │                                                       │    │
│  └──────────────────────────────────────────────────────┘    │
│       │                                                       │
│       ▼                                                       │
│  ┌──────────────────────────────────────────────────────┐    │
│  │                   Data Layer (Prisma/SQLite)          │    │
│  │                                                       │    │
│  │  Agent           Identity + status + allowed services │    │
│  │  LedgerEntry     Cryptographic consent record         │    │
│  │  RevocationState Per-service revocation               │    │
│  │  IdempotencyRec  Duplicate prevention                 │    │
│  │  StepUpChallenge Single-use auth challenges           │    │
│  │                                                       │    │
│  └──────────────────────────────────────────────────────┘    │
│                                                               │
├─────────────────────────────────────────────────────────────┤
│  8 Packages (Turborepo):                                     │
│  shared | ledger | policy-engine | idempotency | step-up    │
│  agent-sdk | vault-client | google-executor                  │
└─────────────────────────────────────────────────────────────┘
```

## Talking Points by Audience

### For Engineers

- **Cryptographic ledger:** HMAC-SHA-256 signatures over canonical JSON. Tamper-evident. Timing-safe comparison. Not blockchain — this is a practical evidence chain using standard cryptography.
- **Idempotency:** Reserve-execute-complete pattern with Prisma-backed store. Prevents double-execution at the database level. Same input, same output, always.
- **Policy engine:** Declarative rules with operation allowlists, risk classification (LOW/MEDIUM/HIGH), and scope requirements. Extensible to any service beyond Google.
- **Step-up auth:** JWT-based single-use challenges with jose library. Challenge-response pattern where the challenge is consumed on first use. Prevents replay.
- **Stable canonicalization:** Custom stable stringify with sorted keys. Ensures equivalent JSON objects produce identical hashes regardless of property ordering.

### For Product / Business

- **Regulatory compliance:** ConsentChain produces the audit trail that GDPR, HIPAA, and SOC 2 require for automated data processing. "Did we have consent?" becomes a query, not a claim.
- **Liability reduction:** When an AI agent misbehaves, the ledger proves exactly what was authorized, by whom, and when. It also proves when consent was revoked.
- **User trust:** Users can see their consent history, revoke access at any time, and know that revocation takes effect immediately. No grace periods. No "your request is being processed."
- **Zero-duplication guarantee:** The idempotency layer means that network retries, user double-clicks, and system restarts never produce duplicate actions. Financial operations, scheduling operations, and data mutations are safe.

### For Safety / Ethics Reviewers

- **Empirical Safety:** ConsentChain addresses the gap between "we had consent" (claim) and "here is the evidence of consent" (proof). This is the Calibrated Truth Doctrine applied to authorization: the assurance level of the consent claim matches the method used to verify it.
- **Fail-closed design:** Missing consent, missing keys, expired challenges, revoked access — all terminate the request. The default is denial. This is the correct default for safety-critical authorization.
- **Traceability:** Every action that passes through the gateway produces a ledger entry. Every entry has a cryptographic signature. Every signature can be independently verified. The audit trail is complete and tamper-evident.
- **Revocability:** Consent is not a one-time event. It is an ongoing relationship. ConsentChain makes revocation immediate and enforceable. This matters because consent given under one context may not apply under a changed context.

## Presentation Timeline

| Segment | Duration | Content |
|---------|----------|---------|
| Problem statement | 2 min | Why "we had consent" is not enough |
| Architecture overview | 2 min | 7-stage pipeline, 8 packages, 5 models |
| Demo: Happy path | 2 min | Agent action through full pipeline to ledger entry |
| Demo: Revocation | 1 min | Revoke access, show blocked request |
| Demo: Step-up | 2 min | High-risk operation requiring additional authentication |
| Demo: Idempotency | 1 min | Same request twice, same response, no duplication |
| Safety framing | 2 min | Empirical Safety domain, Calibrated Truth Doctrine |
| Questions | 3 min | Open discussion |
| **Total** | **15 min** | |

## Repository Quick Start for Judges / Reviewers

```bash
# Clone and install
cd /Users/coreyalejandro/Projects/consentchain
pnpm install

# Start development server
pnpm exec next dev --port 3000

# Inspect the schema
cat prisma/schema.prisma

# Inspect the gateway (168 lines, full 7-stage pipeline)
cat apps/web/src/app/api/agent/action/route.ts

# Inspect the ledger signer (cryptographic functions)
cat packages/ledger/src/signer.ts

# Inspect the policy engine (authorization rules)
cat packages/policy-engine/src/rules.ts

# Inspect the idempotency store
cat packages/idempotency/src/store.ts

# Query the SQLite database
sqlite3 dev.db ".tables"
sqlite3 dev.db "SELECT * FROM LedgerEntry LIMIT 5;"
```

## Key Differentiators

| Feature | ConsentChain | Typical Auth Systems |
|---------|-------------|---------------------|
| Consent evidence | Cryptographic ledger entry per action | "User agreed to ToS" (one-time) |
| Revocation | Immediate, per-service, queryable | "Submit a support ticket" |
| Audit trail | HMAC-signed, tamper-evident | Server logs (mutable, lossy) |
| Idempotency | Database-backed, per-action | Application-level at best |
| Risk classification | Per-operation with step-up auth | Binary allow/deny |
| Scope enforcement | Declared per-request, evaluated by policy engine | Configured globally at registration |

## What is Honest About Current State

ConsentChain is a **partial implementation**. The architecture, data model, API routes, and core packages are real and functional in local development. What is not real:

- No production deployment
- Google executor is a mock (returns placeholder data)
- Vault client is a placeholder (throws until configured)
- No test suite (tests are the first phase of the build contract)
- Auth0 credentials are blank (auth flow not end-to-end)

This honesty is intentional. ConsentChain demonstrates the engineering design and safety architecture of an authorization gateway. It does not claim to be production-ready. The V&T Statement at the bottom of every document enforces this honesty.

---

V&T Statement
Exists: Hackathon packaging document with elevator pitch, 4-demo flow, architecture diagram, audience-specific talking points, 15-minute presentation timeline, quick start guide, differentiator comparison, and honest current-state disclosure
Non-existent: Slide deck, video recording, live demo environment, production deployment
Unverified: Whether SQLite dev.db contains sufficient demo data for all 4 demo scenarios, whether dev server starts cleanly after fresh pnpm install
Functional status: Packaging guide is COMPLETE and ready for presentation preparation
