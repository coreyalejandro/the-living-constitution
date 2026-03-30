# Build Contract: EpistemicGuard Platform
## Contract Version: ZSB-EPG-v1.0
## Domain: D1 — Epistemic Safety
## Parent Platform: SentinelOS
## Parent Ecosystem: The Living Constitution (TLC)

> The canonical full contract text lives at:
> `docs/prompts/ZERO_SHOT_BUILD_CONTRACT__EPISTEMIC_GUARD.md`
> in this repository (once created) or at the TLC repo until then.

---

## System Identity

**EpistemicGuard** is TLC's D1 Epistemic Safety integrated domain engine.

It receives text artifacts, audits claims for verifiability, scrubs PII, grounds evaluation in policy documents, and emits a signed, versioned `ClaimAuditRecord`.

**External descriptor:** Epistemic Auditing Platform for Instructional and Operational Content
**Primary Component:** `ClaimAuditor`

---

## Role in TLC

Within TLC, EpistemicGuard translates:
- constitutional P2 (Epistemic Integrity) → machine-checkable claim verification
- H1 Epistemic Harm class → PII detection, fabrication detection, policy drift detection
- T1/T2/T3 evidence tiers → per-claim tier labels on every audit record

It does not own: cognitive evaluation (D3), session safety (D2), behavioral telemetry (D4).

---

## Current Status

| Dimension | Status |
|-----------|--------|
| ZSB contract (v1.0) | Written — 2026-03-27 |
| Implementation | Planned |
| Build | Not started |
| Tests | Not started |

---

## First-Class Object

```json
{
  "audit_id": "string (UUID)",
  "artifact_hash": "string (SHA-256)",
  "claims_detected": [{ "excerpt": "string", "truth_tier": "T1|T2|T3", "verified": "boolean" }],
  "pii_detections": [{ "type": "string", "redacted": "boolean" }],
  "policy_rules_applied": ["string"],
  "overall_verdict": "verified | unverified | mixed | insufficient_evidence",
  "truth_record": { "record_id": "string", "signed_at": "string", "immutable": true }
}
```

---

## Required MVP Features (17)

1. Submit artifact for epistemic audit
2. Hash artifact on ingest (SHA-256)
3. Detect claims in text (rule-based)
4. Assign truth tier to each claim (T1/T2/T3)
5. Verify claims against submitted sources
6. Detect PII (email, name, phone, SSN, institutional ID)
7. Redact PII before downstream processing
8. Ingest policy document (PDF or text)
9. Map policy rules to evaluation grounding
10. Produce deterministic ClaimAuditRecord
11. Produce explicit verdict
12. Sign and version TruthRecord (append-only)
13. Persist ClaimAuditRecord
14. List audit history
15. Open audit record detail
16. Export audit record as JSON
17. Documentation does not overclaim

---

## Required Stack

| Concern | Technology |
|---------|-----------|
| Framework | Next.js App Router |
| Language | TypeScript |
| Validation | Zod |
| Database | PostgreSQL via Prisma |
| Tests | Vitest + Playwright |

---

## Acceptance Criteria

- [ ] Product name is EpistemicGuard on all surfaces
- [ ] Build contract at `docs/prompts/ZERO_SHOT_BUILD_CONTRACT__EPISTEMIC_GUARD.md`
- [ ] Claim detection is deterministic
- [ ] PII detection and redaction confirmed by tests
- [ ] TruthRecord is append-only (no update/delete path)
- [ ] `docs/truth-status.md` exists and is honest
- [ ] All tests pass

---

## Forbidden Claims

- Formal verification of logical completeness
- Exhaustive PII detection
- FERPA or GDPR compliance certification

---

## TLC Mapping

| TLC Principle | Responsibility |
|--------------|---------------|
| P2 Epistemic Integrity | Primary domain |
| H1 Epistemic Harm class | Primary harm class prevented |
| I2 Status Honesty | Cannot claim T3 without test evidence |
