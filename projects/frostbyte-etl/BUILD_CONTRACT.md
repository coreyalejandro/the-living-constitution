# Build Contract: Frostbyte ETL
## Contract Version: ZSB-FBE-v1.0
## Domain: D4 — Empirical Safety
## Parent Ecosystem: The Living Constitution (TLC)

> The canonical full contract text lives at:
> `docs/prompts/ZERO_SHOT_BUILD_CONTRACT__FROSTBYTE_ETL.md`
> in this repository.

---

## System Identity

**Frostbyte ETL** is TLC's D4 Empirical Safety document ingestion engine.

It enforces a 5-phase provenance pipeline (intake → parse → enrich → store → index), produces SHA-256-linked chains of custody, and emits per-tenant `DocumentRecord` artifacts with append-only audit trails.

**External descriptor:** Multi-Tenant Document ETL Pipeline with Chain-of-Custody Governance
**Primary Component:** `IngestionPipeline`

---

## Role in TLC

Within TLC, Frostbyte ETL translates:
- P5 Empirical Accountability → every processing phase is measured, hashed, and recorded
- P6 Idempotency → same document hash produces same chunk IDs and same audit trail
- H4 Empirical Harm class → missing provenance, unverified chain of custody

It is the **evidence substrate** for EpistemicGuard (D1) and TLC Evidence Observatory (D4).

---

## Current Status

| Dimension | Status |
|-----------|--------|
| ZSB contract (v1.0) | Written — 2026-03-27 |
| Implementation | Partial — core pipeline exists, not contract-reconciled |
| Build | Partial |
| Tests | Partial |
| Predecessor | TLC Evidence Observatory (prototype) |

---

## First-Class Object

```json
{
  "record_id": "string (UUID)",
  "tenant_id": "string",
  "document_hash": "string (SHA-256 of raw bytes)",
  "intake_receipt": {
    "received_at": "string (ISO 8601)",
    "original_filename": "string",
    "mime_type": "string",
    "byte_size": "number",
    "malware_scanned": "boolean",
    "malware_result": "clean | detected | error"
  },
  "provenance_chain": [
    {
      "phase": "intake | parse | enrich | store | index",
      "completed_at": "string (ISO 8601)",
      "phase_hash": "string (SHA-256 of phase output)"
    }
  ],
  "audit_status": "ingesting | parsed | embedded | indexed | failed",
  "vendor_acceptance_report": "string (MinIO path) | null"
}
```

---

## Required MVP Features (17)

See full contract for complete specification.

1. Accept document via API (file upload, multipart form)
2. Malware scan on ingest (ClamAV sidecar)
3. MIME type validation and allowlist enforcement
4. SHA-256 hash of raw document bytes on intake
5. Store raw document to per-tenant MinIO bucket
6. Parse document via Docling + Unstructured
7. Chunk document with deterministic, stable chunk IDs
8. Detect and redact PII in chunk content
9. Embed chunks in online mode (OpenRouter)
10. Embed chunks in offline mode (Nomic embed-text, air-gapped)
11. Write vectors to per-tenant Qdrant collection
12. Record every pipeline phase transition to append-only audit log
13. Produce VendorAcceptanceReport JSON artifact on ingest completion
14. Provide per-tenant semantic search endpoint
15. Export DocumentRecord as signed JSON bundle
16. Per-tenant isolation — no cross-tenant data access
17. Documentation does not overclaim

---

## Required Stack

| Concern | Technology |
|---------|------------|
| Language | Python 3.12+ |
| API framework | FastAPI + Uvicorn |
| Validation | Pydantic v2 |
| Relational DB | PostgreSQL ≥16 via SQLAlchemy 2.0 |
| Vector store | Qdrant |
| Object storage | MinIO |
| Task queue | Celery + Redis |
| Tests | pytest + pytest-asyncio |

**Language note:** Python-first. This differs from other TLC engines (Next.js/TypeScript).

---

## Acceptance Criteria

- [ ] Product name is Frostbyte ETL on all surfaces
- [ ] Build contract at `docs/prompts/ZERO_SHOT_BUILD_CONTRACT__FROSTBYTE_ETL.md`
- [ ] SHA-256 recorded at intake and every phase transition
- [ ] Malware scan blocks upload on `detected` result
- [ ] PII detection confirmed by tests
- [ ] Online/offline modes produce identical DocumentRecord schema
- [ ] Same document re-ingested → same chunk IDs (idempotency test)
- [ ] Per-tenant isolation confirmed (two-tenant isolation test)
- [ ] Append-only audit log confirmed (UPDATE/DELETE rejected by trigger)
- [ ] VendorAcceptanceReport produced on ingest completion
- [ ] `docs/truth-status.md` exists and is honest
- [ ] All tests pass (≥80% line coverage)

---

## Forbidden Claims

- HIPAA compliance certification
- GDPR compliance certification
- Exhaustive PII detection
- Malware guarantee (ClamAV catches known signatures only)
- Air-gap security certification

---

## TLC Mapping

| TLC Principle | Responsibility |
|--------------|----------------|
| P5 Empirical Accountability | Primary domain |
| P6 Idempotency | Same document → same chunk IDs (deterministic) |
| H4 Empirical Harm class | Primary harm class prevented |
| I2 Status Honesty | Cannot claim `indexed` without 5-phase provenance chain |
