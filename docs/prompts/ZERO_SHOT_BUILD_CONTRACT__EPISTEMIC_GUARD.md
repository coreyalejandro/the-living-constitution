# ZERO-SHOT BUILD CONTRACT

## Project: EpistemicGuard Platform
## Contract Version: ZSB-EPG-v1.0
## Domain: D1 — Epistemic Safety
## Parent Platform: SentinelOS
## Parent Ecosystem: The Living Constitution (TLC)
## Issued: 2026-03-27

---

You are building **EpistemicGuard** — TLC's epistemic safety platform.

EpistemicGuard ensures that every content artifact processed by a Commonwealth system has been verified against its claimed sources, is free of exposed PII, and is grounded in applicable policy before any downstream engine consumes it.

Without EpistemicGuard, Commonwealth systems emit unverified claims. Unverified claims produce false understanding. False understanding is cognitive harm. This is the chain EpistemicGuard breaks at the source.

---

## 0. Core Thesis

Epistemic safety fails in three distinct ways:

1. **Fabrication** — a claim is made without any supporting evidence
2. **PII leakage** — an artifact contains personally identifiable information that should not be processed or stored
3. **Policy drift** — an evaluation uses rules that have no grounding in the applicable institutional or constitutional policy

EpistemicGuard addresses all three. It does not prevent all errors. It makes errors visible, auditable, and recoverable.

---

## 1. System Identity

**EpistemicGuard** is TLC's D1 Epistemic Safety integrated domain engine.

It receives instructional or operational text artifacts, audits claims for verifiability, scrubs PII, grounds evaluation logic in policy documents, and emits a signed, versioned `ClaimAuditRecord` that downstream engines can trust.

**External descriptor:** Epistemic Auditing Platform for Instructional and Operational Content
**Category:** Safety Infrastructure — Epistemic Domain
**Integrated Engine for:** D1 Epistemic Safety
**Primary Component:** `ClaimAuditor`

---

## 2. Role in TLC

Within TLC, EpistemicGuard translates:

- P2 Epistemic Integrity → machine-checkable claim verification with evidence tier assignment
- H1 Epistemic Harm class → PII detection, fabrication detection, policy drift detection
- T1/T2/T3 evidence tiers → per-claim tier labels on every audit record
- Institutional policy documents → grounding rules applied during evaluation

EpistemicGuard does **not** own: cognitive safety evaluation (D3), session safety (D2), behavioral telemetry (D4), or build contract enforcement (BuildLattice Guard).

---

## 3. Current Status

| Dimension | Status |
|-----------|--------|
| ZSB contract (v1.0) | Written — 2026-03-27 |
| Implementation | Planned — repo at `/Users/coreyalejandro/Projects/epistemic-guard` |
| Build | Not started |
| Tests | Not started |

---

## 4. First-Class Object

The **ClaimAuditRecord** is the canonical output object:

```json
{
  "audit_id": "string (UUID)",
  "artifact_hash": "string (SHA-256 of input)",
  "artifact_title": "string",
  "claims_detected": [
    {
      "excerpt": "string",
      "confidence": "number (0.0–1.0)",
      "verified": "boolean",
      "source": "string | null",
      "truth_tier": "T1 | T2 | T3"
    }
  ],
  "pii_detections": [
    {
      "type": "email | name | phone | ssn | institutional_id | other",
      "redacted": "boolean",
      "location": "string (paragraph or line reference)"
    }
  ],
  "policy_rules_applied": ["string (rule IDs from loaded policy)"],
  "overall_verdict": "verified | unverified | mixed | insufficient_evidence",
  "truth_record": {
    "record_id": "string (UUID)",
    "version": "string (semver)",
    "engine_version": "string",
    "signed_at": "string (ISO 8601)",
    "immutable": true
  },
  "created_at": "string (ISO 8601)",
  "provenance": {
    "actor_id": "string",
    "engine_version": "string",
    "timestamp_utc": "string (ISO 8601)"
  }
}
```

---

## 5. Required MVP Features (17)

1. Submit text artifact for epistemic audit
2. Hash artifact on ingest (SHA-256) — input identity is immutable
3. Detect claims in submitted text (rule-based pattern matching)
4. Assign truth tier to each detected claim (T1 convention / T2 test / T3 validated)
5. Verify claims against submitted source documents (T2/T3 paths)
6. Detect PII: email, name, phone, SSN, institutional ID (regex + pattern library)
7. Redact PII in-place before any downstream processing
8. Ingest institutional policy document (PDF or plain text)
9. Map policy rules to evaluation grounding parameters
10. Produce deterministic ClaimAuditRecord per submission
11. Produce explicit overall verdict (`verified` / `unverified` / `mixed` / `insufficient_evidence`)
12. Sign and version TruthRecord (append-only, never mutated)
13. Persist ClaimAuditRecord to append-only store
14. List audit history (GET /api/audits)
15. Open audit record detail (GET /api/audits/[id])
16. Export audit record as machine-readable JSON
17. Documentation does not overclaim

---

## 6. Required Stack

| Concern | Technology |
|---------|-----------|
| Framework | Next.js App Router |
| Language | TypeScript |
| UI | ShadCN UI + Tailwind |
| Claim detection | Rule-based (regex + pattern) — optional Claude API for LLM path |
| PII detection | Regex pattern library — optional spaCy via API |
| Policy ingestion | pdf-parse (PDF) + plain text |
| Hashing | Node.js `crypto` (SHA-256) |
| Validation | Zod |
| Database | PostgreSQL via Prisma |
| Tests | Vitest + Playwright |

---

## 7. Acceptance Criteria

- [ ] Product name is EpistemicGuard on all surfaces
- [ ] Build contract file exists at `docs/prompts/ZERO_SHOT_BUILD_CONTRACT__EPISTEMIC_GUARD.md` in repo
- [ ] README explicitly links to build contract
- [ ] SHA-256 artifact hash computed on every submission
- [ ] Claim detection runs deterministically (same input → same output)
- [ ] PII detection and redaction confirmed by tests
- [ ] Policy ingestion produces grounding rules applied during audit
- [ ] ClaimAuditRecord persisted and retrievable
- [ ] Audit history list and detail views work
- [ ] JSON export works
- [ ] TruthRecord is append-only (no update/delete path)
- [ ] `docs/truth-status.md` exists and is honest
- [ ] All tests pass
- [ ] Documentation does not claim formal verification, exhaustive PII detection, or provable epistemic completeness

---

## 8. Forbidden Claims

Do NOT claim:

- Formal verification of logical completeness
- Exhaustive PII detection (best-effort pattern matching, not a legal guarantee)
- Provably correct claim extraction
- Real-time LLM-speed verification (rule-based path is default)
- FERPA or GDPR compliance certification (implementation responsibility of deployer)

---

## 9. Evidence Required

```bash
# Build passes
pnpm install && pnpm build

# Tests pass
pnpm test

# Type check clean
npx tsc --noEmit

# Claim audit is deterministic (run 3× on same input)
pnpm test -- determinism

# PII redaction confirmed
pnpm test -- pii

# Audit record persists and is retrievable
pnpm test:e2e -- audit-flow
```

---

## 10. TLC Mapping

| TLC Article / Principle | EpistemicGuard Responsibility |
|------------------------|-------------------------------|
| P2 Epistemic Integrity | Primary domain — all claims must carry an evidence tier |
| P5 Empirical Accountability | Audit records are evidence; they must not be mutated |
| P10 Evidence-Bound Action | Every audit verdict traces to detected claims and sources |
| H1 Epistemic Harm class | Primary harm class this engine prevents |
| I1 Domain Coverage | Must provide full D1 coverage |
| I2 Status Honesty | Cannot claim T3 (validated) without test evidence |
| Article II §2 | TruthRecord is immutable — no update/delete paths |
| Article III §3 | Every output traces to a policy rule or detected evidence |

---

## 11. Signal Responsibilities

EpistemicGuard **produces**:

| Signal | Consumed by |
|--------|------------|
| `ClaimAuditRecord` | D3 CognitiveGuard (grounding) |
| `TruthRecord` | D4 EmpiricalGuard (audit evidence) |
| `pii_redacted_artifact` | D3 CognitiveGuard (safe artifact input) |

EpistemicGuard **consumes**:

| Signal | Produced by |
|--------|------------|
| `PolicyDocument` | Operator upload (no engine dependency) |
| Constitutional principles | TLC ZSB-TLC-v1.0 |

---

## V&T Statement (at contract writing)

**Exists:** ZSB-EPG-v1.0 contract written; ClaimAuditRecord schema defined; 17 MVP features enumerated; TLC signal mapping specified.

**Non-existent:** Repo, implementation, tests, deployed artifact.

**Unverified:** Claim detection accuracy; PII pattern library coverage; policy ingestion fidelity.

**Functional status:** Contract only. Build not started.
