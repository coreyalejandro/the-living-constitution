# ConsentChain Mapping
## How ConsentChain Maps to TLC Enforcement Controls

---

## What ConsentChain Is

ConsentChain is the authorization gateway of the Commonwealth. It ensures that no agent action executes without proper authorization and informed consent. Every action passes through a 7-stage pipeline. Failed stages block the action entirely. There is no bypass.

**Repository:** `/Users/coreyalejandro/Projects/consentchain`
**Technology:** TypeScript, Turborepo monorepo, Prisma ORM
**Safety domain:** Empirical Safety (primary), Human Safety (secondary)
**Architecture:** 8 packages across `apps/` and `packages/` directories

---

## The 7-Stage Action Pipeline

ConsentChain processes every agent action through seven sequential stages. Each stage is a gate. If any gate fails, the action is rejected. The pipeline is not advisory — it is blocking.

### Stage 1: Validate

**Purpose:** Ensure the action request is well-formed and structurally valid.

**What is checked:**
- The action has a valid schema (required fields present, types correct).
- The action references a real target (the resource or system the action affects exists).
- The action payload does not exceed size limits.

**TLC mapping:** Article II (Execution Law) — input validation is mandatory. No action proceeds with malformed input.

### Stage 2: Authenticate

**Purpose:** Verify the identity of the requesting agent or user.

**What is checked:**
- The requester has a valid identity token (JWT, API key, or session).
- The token has not expired.
- The token signature is valid (not forged or tampered).

**TLC mapping:** Article II (Security) — authentication is required for all operations that affect state.

### Stage 3: Authorize

**Purpose:** Verify the requester has permission to perform this specific action.

**What is checked:**
- The requester's role permits this action type.
- The requester has access to the target resource.
- The action does not exceed the requester's permission scope.

**TLC mapping:** Article IV (Separation of Powers) — agents have defined capabilities and constraints. The authorize stage enforces these boundaries at runtime.

### Stage 4: Consent

**Purpose:** Ensure informed consent has been obtained from all affected parties.

**What is checked:**
- The user has been presented with a clear description of what the action will do.
- The user has explicitly approved the action (no implicit consent, no pre-checked boxes).
- The consent record includes a timestamp and the exact scope of what was approved.
- For actions affecting multiple parties, each party's consent is independently verified.

**TLC mapping:** Article I (Right to Dignity, Right to Clarity) — consent must be informed, explicit, and revocable. The Default User doctrine requires that consent flows are accessible and not cognitively overwhelming.

### Stage 5: Rate-Limit

**Purpose:** Prevent abuse, accidental loops, and resource exhaustion.

**What is checked:**
- The requester has not exceeded their action quota for this time window.
- The target resource has not been subjected to excessive actions recently.
- The action rate is consistent with normal usage patterns (anomaly detection).

**TLC mapping:** Article I (Right to Safety) — rate limiting prevents harm from runaway agents or compromised credentials.

### Stage 6: Execute

**Purpose:** Perform the authorized, consented action.

**What happens:**
- The action is dispatched to the target system.
- Execution is monitored for errors.
- If execution fails, the failure is captured with a detailed error message.
- If execution succeeds, the result is captured for the audit stage.

**TLC mapping:** Article III (Verification Before Done) — execution is monitored, not fire-and-forget. The result is verified, not assumed.

### Stage 7: Audit

**Purpose:** Create an immutable record of what happened, who approved it, and what the outcome was.

**What is recorded:**
- The complete action request (stage 1 input).
- The authentication result (who requested it).
- The authorization result (what permissions were checked).
- The consent record (who approved it and when).
- The execution result (what happened).
- The timestamp of each stage.

**TLC mapping:** Article I (Right to Truth) — the audit log is the truth record. It is immutable (Article II) and evidence-bound (Article III).

---

## Pipeline Flow Diagram

```
Action Request
      │
      ▼
┌──────────┐    FAIL
│ Validate  ├─────────► REJECT (malformed input)
└────┬─────┘
     │ PASS
     ▼
┌──────────────┐    FAIL
│ Authenticate  ├─────────► REJECT (identity invalid)
└────┬─────────┘
     │ PASS
     ▼
┌───────────┐    FAIL
│ Authorize  ├─────────► REJECT (insufficient permissions)
└────┬──────┘
     │ PASS
     ▼
┌──────────┐    FAIL
│ Consent   ├─────────► REJECT (consent not obtained)
└────┬─────┘
     │ PASS
     ▼
┌────────────┐    FAIL
│ Rate-Limit  ├─────────► REJECT (quota exceeded)
└────┬───────┘
     │ PASS
     ▼
┌──────────┐    FAIL
│ Execute   ├─────────► LOG ERROR + REJECT
└────┬─────┘
     │ SUCCESS
     ▼
┌──────────┐
│  Audit    ├─────────► IMMUTABLE RECORD CREATED
└──────────┘
```

---

## ConsentChain Package Structure

| Package | Purpose | TLC Mapping |
|---------|---------|-------------|
| `apps/web` | Web application hosting the action gateway API | Execution layer |
| `packages/core` | Shared types, constants, and pipeline logic | Article II (code governance) |
| `packages/auth` | Authentication and authorization modules | Stages 2-3 |
| `packages/consent` | Consent management and record keeping | Stage 4 |
| `packages/audit` | Immutable audit log | Stage 7, Article I (Right to Truth) |
| `packages/rate-limit` | Rate limiting and anomaly detection | Stage 5 |
| `packages/prisma` | Database schema and Prisma client | Data persistence |
| `packages/config` | Shared configuration | Cross-cutting |

---

## Invariant Enforcement Through ConsentChain

ConsentChain's 7-stage pipeline directly prevents several TLC failure modes:

| Failure Mode | ConsentChain Prevention |
|-------------|------------------------|
| F1 (Confident False Claims) | The audit stage records actual outcomes, creating evidence that contradicts false claims about what actions were taken. |
| F2 (Phantom Completion) | The execute stage verifies action results. A failed execution is logged as a failure, not swallowed as a success. |
| F4 (Harm-Risk Coupling) | The consent stage ensures that actions affecting users have explicit approval. Cross-domain harm requires bypassing consent — which the pipeline blocks. |

---

## V&T Statement
- **Exists:** ConsentChain mapping document describing all 7 pipeline stages with TLC article mappings; pipeline flow diagram; package structure table; invariant enforcement mapping for F1, F2, F4
- **Non-existent:** Automated ConsentChain-to-SentinelOS invariant cross-validation; runtime telemetry dashboard for pipeline stage metrics; consent revocation flow
- **Unverified:** Whether the 8-package structure described matches the current ConsentChain repo exactly; whether the route handler at `apps/web/src/app/api/agent/action/route.ts` implements all 7 stages as described
- **Functional status:** ConsentChain is partial — core pipeline logic and Prisma schema exist; full 7-stage runtime enforcement is not yet verified end-to-end
