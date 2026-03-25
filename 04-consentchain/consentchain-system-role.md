# ConsentChain System Role in The Living Constitution

## Identity

ConsentChain is the **authorization gateway** for AI agent actions within the Safety Systems Design Commonwealth. It occupies the Empirical Safety domain, transforming "we had consent" from a claim into a verifiable, auditable evidence chain. No agent action occurs without passing through ConsentChain's pipeline. No consent is assumed. Every authorization decision is recorded, revocable, and cryptographically signed.

## Safety Domain

**Domain:** Empirical Safety
**Failure class addressed:** A system's described behavior does not match its actual behavior. Consent is assumed but not recorded. Agent actions cannot be audited after the fact.

## Constitutional Invariants Enforced

| Invariant | How ConsentChain Enforces It |
|-----------|------------------------------|
| I1: Evidence-First | Consent requires evidence (ledger entry), not assumption. Every action produces a signed record. |
| I4: Traceability Mandatory | Every agent action flows through a 7-stage pipeline and is recorded in the cryptographic ledger. |
| I6: Fail Closed | Missing consent blocks the action. Missing agent key returns 401. Revoked service returns 403. Missing scopes return 403. |
| Idempotency Doctrine | Duplicate action requests return the same response. The IdempotencyStore prevents double-execution. Same input, same output, every time. |

## Role Within the Commonwealth

ConsentChain is the "write" side of Empirical Safety. It answers five questions for every agent action:

1. **Was consent given?** Agent validation confirms an active, registered agent with a hashed API key.
2. **By whom?** The Agent model records identity, status, and allowed services.
3. **For what action and scope?** The request body specifies service, operation, scopes, and payload. The policy engine evaluates authorization.
4. **Can it be revoked?** The RevocationState model allows per-agent, per-service revocation at any time.
5. **Was it revoked?** Every request checks revocation state before proceeding to execution.

The planned Empirical Safety Engine (ESE) is the "read" side — it would analyze patterns, detect consent drift, and measure whether safety interventions reduce harm. Together they complete the evidence loop.

## The 7-Stage Action Gateway

Every agent request flows through the following pipeline. No stage is skippable. Each stage either passes the request forward or terminates it with an explicit error.

```
Stage 1: Agent Validation
  Input:  x-agent-key header
  Action: SHA-256 hash the key, look up Agent record in Prisma
  Fail:   401 (invalid agent key) or 403 (agent disabled / service not allowed)

Stage 2: Canonicalization + Idempotency
  Input:  actionId, service, operation, scopes, payload
  Action: Canonical JSON serialization (sorted keys, stable stringify)
          SHA-256 hash of canonical request
          IdempotencyStore.reserve() — if actionId already completed, return cached response
  Fail:   409 (action already in progress) or 200 with x-idempotent-replay header

Stage 3: Revocation Check
  Input:  agentId + service
  Action: Query RevocationState for matching revocation record
  Fail:   403 (service revoked)

Stage 4: Policy Evaluation
  Input:  service, operation, scopes
  Action: Rules-based evaluation: operation allowlist, risk classification, scope requirements
  Output: PolicyDecision { allowed, risk, reason, stepUpRequired }
  Fail:   403 (operation not allowed / missing scopes)

Stage 5: Step-Up Authentication
  Input:  PolicyDecision with stepUpRequired flag + optional stepUpProofJwt
  Action: For HIGH-risk operations, require JWT proof of step-up challenge
          Challenge is single-use (usedAt field prevents replay)
          JWT verified with STEP_UP_SECRET via jose library
  Fail:   401 (step-up required — returns challengeId) or 401 (invalid step-up proof)

Stage 6: Execution
  Input:  Authorized request + mock access token
  Action: Route to service executor (currently Google executor mock)
          Supported operations: listEvents, createEvent, deleteAllEvents
  Fail:   400 (unsupported service or operation)

Stage 7: Ledger Write
  Input:  Request canonical + response canonical
  Action: SHA-256 hash both, HMAC-SHA-256 sign the concatenated hashes
          Create LedgerEntry with full audit trail
          Complete idempotency record with response JSON
  Output: 200 with execution result
```

## Architecture Position

### Monorepo Structure

ConsentChain is a Turborepo monorepo with pnpm workspaces. The architecture separates concerns into 8 focused packages:

| Package | Role | Key File |
|---------|------|----------|
| `@consentchain/shared` | Types and constants shared across all packages | `types.ts`, `constants.ts` |
| `@consentchain/ledger` | Cryptographic consent ledger: canonical JSON, SHA-256, HMAC signing | `signer.ts` |
| `@consentchain/policy-engine` | Rules-based authorization: allowlists, risk classification, scope checks | `rules.ts` |
| `@consentchain/idempotency` | Duplicate action prevention via Prisma-backed store | `store.ts` |
| `@consentchain/step-up` | Step-up authentication for sensitive operations | `index.ts` |
| `@consentchain/agent-sdk` | Client SDK for agent integration | `client.ts` |
| `@consentchain/vault-client` | Secrets management (placeholder — throws until configured) | `index.ts` |
| `@consentchain/google-executor` | Google services executor (mock — returns 501) | `index.ts` |

### Data Layer

Prisma ORM with SQLite (better-sqlite3 driver adapter). Five models:

| Model | Purpose | Key Fields |
|-------|---------|------------|
| `Agent` | Registered agent identity | id, name, status (ACTIVE/DISABLED), apiKeyHash, allowedServices |
| `LedgerEntry` | Cryptographic consent record | actionId, agentId, service, operation, requestHash, responseHash, signature |
| `RevocationState` | Per-agent per-service revocation | agentId, service, revokedAt, reason |
| `IdempotencyRecord` | Duplicate prevention | actionId, agentId, status (RESERVED/COMPLETED), requestHash, responseJson |
| `StepUpChallenge` | Single-use step-up authentication challenges | challengeId, actionId, createdAt, usedAt |

### API Surface

| Route | Method | Purpose |
|-------|--------|---------|
| `/api/agent/action` | POST | Full 7-stage gateway pipeline |
| `/api/auth/step-up` | POST | Initiate step-up authentication challenge |
| `/api/auth/step-up/verify` | POST | Verify step-up challenge with JWT proof |
| `/api/ledger` | GET | Query consent ledger entries |
| `/api/revoke` | POST | Revoke agent consent for a service |
| `/api/services/connect/google` | POST | Google executor (501 placeholder) |

## Relationship to Other Commonwealth Systems

| System | Relationship |
|--------|-------------|
| **SentinelOS** | ConsentChain provides the authorization evidence that SentinelOS governance requires for agent orchestration |
| **UICare** | UICare's cognitive safety patterns inform how consent prompts and step-up challenges are presented to users |
| **ProActive** | ProActive agents would route actions through ConsentChain before executing on behalf of users |
| **MADMall** | Healthcare actions require the highest consent assurance — ConsentChain's ledger is the evidence chain for HIPAA-grade authorization |

## Design Principles

1. **Fail closed.** Missing consent, missing keys, missing scopes, expired challenges — all terminate the request. The default is denial.
2. **Idempotency is constitutional.** The same request sent twice produces the same result. No duplicate execution. No double-charges. No phantom calendar events.
3. **Revocation is immediate.** A revoked service blocks the next request. There is no grace period. There is no "revocation pending."
4. **Signatures are tamper-evident.** HMAC-SHA-256 over request + response hashes. If the ledger entry is modified after creation, the signature no longer verifies.
5. **Step-up is single-use.** Each challenge can only be used once. The `usedAt` field prevents replay. The JWT is verified with a server-side secret.
6. **Canonicalization prevents ambiguity.** Stable JSON stringify with sorted keys ensures that equivalent requests produce identical hashes regardless of property ordering.

## What ConsentChain Proves

ConsentChain is the concrete answer to: "How do you know the AI had permission?"

Not "we configured it." Not "the user agreed to terms of service." Not "we assumed opt-in."

The answer is: "Here is the ledger entry. Here is the cryptographic signature. Here is the exact request and response. Here is the agent identity. Here is the timestamp. Here is whether it was revoked. Run the HMAC yourself."

That is Empirical Safety. The described state matches the actual state. The evidence exists. The claim is verifiable.

---

V&T Statement
Exists: ConsentChain system role definition, 7-stage gateway architecture, 8 package descriptions, 5 Prisma model descriptions, 6 API route descriptions, relationship mapping to Commonwealth systems, design principles grounded in inspected source code
Non-existent: Empirical Safety Engine (ESE) read-side integration, production deployment, real Google API integration, vault client integration
Unverified: Runtime behavior under concurrent load, HMAC verification across full audit trail, step-up challenge expiration policies
Functional status: Document is COMPLETE and grounded in verified source inspection of the ConsentChain repository
