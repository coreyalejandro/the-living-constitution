# Zero-Shot Build Contract: Frostbyte ETL
## Contract Version: ZSB-FBE-v1.0
## Domain: D4 — Empirical Safety
## Parent Ecosystem: The Living Constitution (TLC)
## Date: 2026-03-27

---

## §1 System Identity

**Frostbyte ETL** is TLC's D4 Empirical Safety document ingestion engine.

It receives raw documents from untrusted sources, enforces a 5-phase provenance pipeline (intake → parse → enrich → store → index), produces a SHA-256-linked chain of custody, and emits per-tenant `DocumentRecord` artifacts with append-only audit trails.

**External descriptor:** Multi-Tenant Document ETL Pipeline with Chain-of-Custody Governance
**Primary Component:** `IngestionPipeline`

---

## §2 Role in TLC

Within TLC, Frostbyte ETL translates:

- P5 Empirical Accountability → every processing phase is measured, hashed, and recorded; described processing matches actual processing
- P6 Idempotency → same document hash produces same chunk IDs and same audit trail entries on re-ingest
- H4 Empirical Harm class → missing provenance, unverified chain of custody, cross-tenant data leakage

It does not own: behavioral signal derivation (D4 EmpiricalGuard), session safety (D2), cognitive evaluation (D3), claim verification (D1).

Frostbyte ETL is the **evidence substrate** — it produces the document records that upstream systems (EpistemicGuard, TLC Evidence Observatory) audit and query.

---

## §3 Current Status

| Dimension | Status |
|-----------|--------|
| ZSB contract (v1.0) | Written — 2026-03-27 |
| Implementation | Partial (~core pipeline exists) |
| Build | Partial |
| Tests | Partial |
| Predecessors | TLC Evidence Observatory (prototype) |

---

## §4 First-Class Object

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
  "parse_output": {
    "chunk_count": "number",
    "page_count": "number",
    "pii_detections": [{ "type": "string", "redacted": "boolean" }]
  },
  "embedding_record": {
    "model": "string",
    "mode": "online | offline",
    "vector_count": "number",
    "collection_id": "string"
  },
  "audit_status": "ingesting | parsed | embedded | indexed | failed",
  "vendor_acceptance_report": "string (MinIO path) | null"
}
```

---

## §5 Required MVP Features (17)

1. Accept document via API (file upload, multipart form)
2. Malware scan on ingest (ClamAV sidecar) — block upload on `detected` result
3. MIME type validation and allowlist enforcement
4. Generate SHA-256 hash of raw document bytes on intake
5. Store raw document to per-tenant MinIO bucket (encrypted at rest)
6. Parse document via Docling + Unstructured (layout-aware, structure-preserving)
7. Chunk document into normalized segments with deterministic, stable chunk IDs
8. Detect and redact PII in chunk content before storage
9. Embed chunks in online mode (OpenRouter — configurable model)
10. Embed chunks in offline mode (Nomic embed-text, air-gapped — no outbound network)
11. Write vectors to per-tenant Qdrant collection (collection-level isolation)
12. Record every pipeline phase transition to append-only audit log
13. Produce VendorAcceptanceReport JSON artifact on ingest completion
14. Provide per-tenant semantic search endpoint (retrieval)
15. Export DocumentRecord as signed JSON bundle
16. Per-tenant isolation — no cross-tenant data access paths in any query
17. Documentation does not overclaim

---

## §6 Required Stack

| Concern | Technology |
|---------|------------|
| Language | Python 3.12+ |
| API framework | FastAPI + Uvicorn |
| Validation | Pydantic v2 |
| Relational DB | PostgreSQL ≥16 via SQLAlchemy 2.0 + asyncpg |
| Migrations | Alembic |
| Document parsing | Docling + Unstructured |
| Online embeddings | OpenRouter (httpx client) |
| Offline embeddings | Nomic embed-text (local container) |
| Vector store | Qdrant (per-tenant collection) |
| Object storage | MinIO (S3-compatible, per-tenant bucket) |
| Task queue | Celery + Redis |
| Malware scan | ClamAV (sidecar container) |
| Audit logging | structlog + PostgreSQL append-only table |
| Container orchestration | Docker Compose (online and offline) |
| Tests | pytest + pytest-asyncio + pytest-cov |

**Language boundary (non-negotiable):** This engine is Python-first. TypeScript is not used. This differs from other TLC engines (EpistemicGuard, HumanGuard, EmpiricalGuard) which use Next.js/TypeScript.

---

## §7 Acceptance Criteria

- [ ] Product name is Frostbyte ETL on all surfaces
- [ ] Build contract at `docs/prompts/ZERO_SHOT_BUILD_CONTRACT__FROSTBYTE_ETL.md`
- [ ] SHA-256 hash recorded at intake and at every phase transition
- [ ] Malware scan blocks upload on `detected` result (test: upload EICAR test string)
- [ ] PII detection confirmed by tests (email, name, phone, SSN fixtures)
- [ ] Online mode (OpenRouter) and offline mode (Nomic) produce identical `DocumentRecord` schema
- [ ] Same document re-ingested → same chunk IDs (idempotency test)
- [ ] Per-tenant isolation confirmed — no cross-tenant data access (test: two tenants, verify isolation)
- [ ] Append-only audit log confirmed — UPDATE/DELETE attempts rejected by trigger
- [ ] VendorAcceptanceReport produced and stored on ingest completion
- [ ] `docs/truth-status.md` exists and is honest
- [ ] All tests pass (≥80% line coverage)

---

## §8 Forbidden Claims

- HIPAA compliance (the pipeline implements PII detection, not HIPAA certification)
- GDPR compliance certification
- Exhaustive PII detection (no NER model achieves 100% recall)
- Malware guarantee (ClamAV catches known signatures; unknown malware is not claimed to be blocked)
- Air-gap security certification

---

## §9 Pipeline Phase Specification

| Phase | Input | Output | Failure Behavior |
|-------|-------|--------|-----------------|
| Intake | Raw file upload | SHA-256 hash, MinIO path, malware result | Reject on malware detected; reject on MIME mismatch |
| Parse | Raw file from MinIO | Chunk list (text + metadata + chunk_id) | Fail record to `failed`; log phase_hash = null |
| Enrich | Chunk list | PII annotations, redacted chunks | Enrich errors are non-blocking; log detections |
| Store | Redacted chunks | Vector embeddings in Qdrant | Fail record to `failed`; preserve parse output |
| Index | Vectors in Qdrant | Collection indexed, retrieval available | Index errors are retried 3× before `failed` |

---

## §10 Per-Tenant Isolation Rules

1. Every database query MUST include `WHERE tenant_id = :tenant_id` or use RLS policy
2. Every MinIO operation MUST address a bucket scoped to `tenant-{tenant_id}`
3. Every Qdrant operation MUST address a collection scoped to `tenant-{tenant_id}`
4. The control plane NEVER constructs cross-tenant queries
5. Violation of any rule above is a CRITICAL defect — block release

---

## §11 TLC Mapping

| TLC Principle | Responsibility |
|--------------|----------------|
| P5 Empirical Accountability | Primary domain — every phase produces measurable, recorded evidence |
| P6 Idempotency | Same document → same chunk IDs → same audit entries (deterministic) |
| H4 Empirical Harm class | Primary harm class prevented — ungoverned ingestion, missing chain of custody |
| I2 Status Honesty | Cannot claim `indexed` without completed 5-phase provenance chain |

---

## §12 Signal Responsibilities

| Signal | Direction | Consumer |
|--------|-----------|---------|
| DocumentRecord | Produces → | TLC Evidence Observatory (D4), EpistemicGuard (D1) |
| VendorAcceptanceReport | Produces → | External auditors, tenant admins |
| PII-redacted document chunks | Produces → | EpistemicGuard (D1) for claim auditing |

---

## V&T Statement (Contract Time: 2026-03-27)

Exists: ZSB-FBE-v1.0 written; partial Python implementation in `frostbyte-etl` repo; STACK.md research complete; product vision (3 verticals: VeritasVault, FoundationRAG, MediTrace) documented
Non-existent: Full 5-phase pipeline (partial), test coverage report, chain-of-custody acceptance tests, cross-tenant isolation tests
Unverified: SHA-256 provenance chain (partial implementation — not tested end-to-end); idempotency under re-ingest; offline/online mode parity
Functional status: Contract-only for TLC governance purposes. Partial implementation predates contract. Build must be reconciled against this contract before status upgrades to `implemented`.
