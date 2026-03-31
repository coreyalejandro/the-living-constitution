# C-RSP Build Contract

## Contractually Constrained Deterministic Single-Pass Executable Prompt

---

## TEMPLATE METADATA

- **Template Version:** v2.0.0
- **Contract Version:** v1.0.0
- **Status:** EXECUTION-READY
- **Contract Class:** Data Pipeline
- **TLC Domain:** Empirical
- **System Role:** Research-grade ETL and retrieval pipeline for document ingestion, chunking, embedding, vector storage, auditability, and observatory export
- **Primary Objective:** Build a Docker Compose–based Frostbyte pipeline that produces real embeddings, chunk-level Qdrant storage, append-only audit evidence, adapter-pinned ingest provenance, and non-blocking Observatory handoff with deterministic swap controls.

---

## 1. CURRENT STATE & ENVIRONMENT (BASELINE)

### Verified Assets (Must Exist)

- `docker-compose.yml`
- `pyproject.toml`
- `pipeline/`
- `packages/admin-dashboard/`
- existing SSE endpoint and Redis pub/sub wiring
- PostgreSQL tables already present
- Qdrant available as vector store target
- `sentence-transformers` installed
- Frostbyte design spec approved for implementation

### Must NOT Exist

- zero-vector stub embeddings in active ingest path
- in-memory-only document truth path as final persistence layer
- per-document vector storage in place of per-chunk storage
- implicit adapter swaps affecting in-flight documents
- blocking sink behavior for optional sinks
- dimension-mismatched embedder/store pairings at startup or swap time

### Generated Artifacts (Expected)

- `pipeline/pipeline/embedding/encoder.py`
- adapter protocol and loader wiring
- startup validation path
- real chunked embeddings
- Qdrant chunk upserts
- append-only audit events from legacy text intake path
- `FrostbyteExportRecord` writer
- Observatory sink implementation
- DLQ files and replay tooling
- updated dashboard healthcheck/proxy wiring
- conformance tests
- `.env.example` updates
- operator-visible SSE events for control/data/export/eval planes

### Hermetic Baseline Policy

- Docker Compose is the primary execution substrate.
- No Kubernetes work is authorized in this contract.
- No hidden retries outside explicitly defined retry policies.
- All adapter choices must resolve from environment configuration at startup.

### Hard Dependencies

- **Runtime:** Python 3.11+, Docker Compose, Redis, PostgreSQL, Qdrant, MinIO
- **Embedding Model:** `nomic-ai/nomic-embed-text-v1.5`
- **Parser Backend:** `unstructured`
- **Vector Store:** `qdrant`
- **Deployment Form:** Docker Compose only
- **Admin UI Runtime:** existing dashboard container with corrected healthcheck and proxy

---

## 2. DEPENDENCY POLICY

- **Conflict Resolution Rule:** pinned adapters and explicit environment resolution win over implicit discovery.
- **Availability Rule:** if any required backend fails healthcheck or compatibility validation, halt startup.
- **Vulnerability Rule:** no dependency upgrade is permitted during execution unless explicitly pinned in the contract revision.
- **Model Loading Rule:** `nomic-embed-text-v1.5` must load during FastAPI lifespan startup; first-request lazy load is forbidden.
- **Dimension Rule:** embedder dimensions must equal vector store expected dimensions before startup completes and before any swap is accepted.

### Target Environment Profile

- **OS / Platform:** Linux containerized runtime via Docker Compose
- **Hardware Constraints:** CPU-friendly target; 4 GB RAM minimum for model loading is assumed but must be measured
- **Network Constraints:** internal service-to-service networking only; Docker service names, not `localhost`, used in inter-container proxying

---

## 3. EXECUTION LOGIC (SINGLE-PASS PATH)

### Execution Form

Pipeline

### Ordered Execution Steps

1. Resolve environment configuration for parser, embedder, vector store, sinks, tenant, registry version.
2. Start Docker Compose services.
3. Load and validate adapter registry.
4. Run required adapter healthchecks.
5. Validate compatibility rules, especially embedding dimension ↔ vector store dimension.
6. Warm-load `nomic-embed-text-v1.5` during application lifespan.
7. Refuse startup on any required adapter failure or dimension mismatch.
8. Accept intake through `/api/v1/intake`.
9. Store raw file/object in MinIO with SHA-256.
10. Insert PostgreSQL document row for text intake path.
11. Parse with `unstructured`.
12. Chunk using 512-token window, 64-token overlap, minimum 50 tokens.
13. Capture adapter triplet and chunk provenance at `RECEIVED`.
14. Encode each chunk with `search_document:` prefix using `nomic-embed-text-v1.5`.
15. Verify per-chunk norm and classify drift subtype when threshold fails.
16. Upsert each chunk independently into Qdrant.
17. Emit append-only audit events for each completed stage.
18. Derive retrieval status and evidence status independently.
19. Build `FrostbyteExportRecord`.
20. HMAC-sign export payload.
21. Dispatch to Observatory sink non-blockingly.
22. On filesystem write failure, place signed record into DLQ.
23. Emit SSE events for control, data, export, and eval planes.
24. Expose corrected dashboard `/stream` view with adapter bar, pinning, and sink state.
25. Run conformance tests and end-to-end verification.

### Decision Closure

#### Allowed Decisions

- parser backend = `unstructured`
- embedding backend = `nomic`
- vector store = `qdrant`
- sink list includes `observatory`
- optional sink failures degrade sink state but do not fail core pipeline unless explicitly required
- hot-swap affects only next document, never in-flight documents

#### Prohibited Decisions

- swapping adapters mid-document
- accepting dimension mismatch
- re-embedding during DLQ replay
- treating SSE as authoritative forensic truth
- storing one vector per document instead of one per chunk
- silent fallback from required adapter failure to an unvalidated adapter

#### Default on Ambiguity

HALT

#### Retry Policy

- Core pipeline retries only where explicitly defined
- Observatory Phase 5a filesystem handoff: retry only on write failure conditions
- Qdrant retry: up to 3 attempts
- Parse retry on exception: up to 2 attempts
- No hidden retries

---

## 4. CONSTITUTIONAL INVARIANTS

### Invariant Categories

- Isolation Boundary
- Type / Schema Discipline
- Determinism / Idempotency
- Environment Constraints
- Security / Network Policy
- Data Handling / Privacy
- Observability / Evidence

### Project-Specific Invariants

- **INVARIANT_01:** Docker Compose is the only deployment target in this contract.
- **INVARIANT_02:** `PARSER_BACKEND=unstructured` at execution time.
- **INVARIANT_03:** `EMBEDDING_BACKEND=nomic` resolves to `nomic-embed-text-v1.5`.
- **INVARIANT_04:** `VECTOR_STORE=qdrant` resolves to the active store.
- **INVARIANT_05:** embedder output dimension must equal Qdrant collection expected dimension.
- **INVARIANT_06:** all adapter selections are captured at `RECEIVED` and pinned for the full document lifecycle.
- **INVARIANT_07:** hot-swap changes apply only to documents received after the swap event.
- **INVARIANT_08:** no document may mix parser/embedder/store outputs from different adapter sets.
- **INVARIANT_09:** chunking policy is fixed at 512/64/min-50 for this contract revision.
- **INVARIANT_10:** every chunk must be encoded with the `search_document:` prefix.
- **INVARIANT_11:** query encoding must use `search_query:` and is a separate path from ingestion.
- **INVARIANT_12:** each chunk is stored as its own Qdrant point.
- **INVARIANT_13:** PostgreSQL audit events are append-only.
- **INVARIANT_14:** stage transitions are monotonic.
- **INVARIANT_15:** idempotency key is `sha256(tenant_id + ":" + content_sha256)`.
- **INVARIANT_16:** duplicate intake behavior must follow the defined state rules.
- **INVARIANT_17:** SSE is derived operational telemetry only; PostgreSQL audit log and Redis-backed event sources remain authoritative.
- **INVARIANT_18:** Observatory sink is non-blocking by default.
- **INVARIANT_19:** DLQ replay replays signed export records only; no re-parse and no re-embed.
- **INVARIANT_20:** HMAC verification is required before DLQ replay.
- **INVARIANT_21:** filesystem handoff writes must be atomic.
- **INVARIANT_22:** document IDs must be sanitized before DLQ path construction.
- **INVARIANT_23:** dashboard healthcheck must be valid in-container and proxy must target Docker service names.
- **INVARIANT_24:** conformance tests must exist for parser, embedder, vector store, and sink behavior.

---

## 5. INPUT CONTRACT

### Environment Inputs

- `EMBEDDING_BACKEND=nomic`
- `VECTOR_STORE=qdrant`
- `PARSER_BACKEND=unstructured`
- `PIPELINE_SINKS=observatory`
- `SINK_OBSERVATORY_REQUIRED=false`
- `OBSERVATORY_INPUT_DIR=[required path]`
- `OBSERVATORY_SHARED_SECRET=[required secret >= 32 bytes]`
- `OBSERVATORY_TIMEOUT_SECONDS=30`
- `OBSERVATORY_MAX_RETRIES=3`
- `REGISTRY_VERSION=1`

### Request Inputs

- file/document submitted to `/api/v1/intake`
- tenant identifier
- content hash inputs needed for idempotency

### Input Validation Rules

- missing required env vars for resolved adapters = startup halt
- invalid secret length = startup halt
- invalid dimension pairing = startup halt
- invalid sink path permissions = sink degraded or failed depending on required/optional status
- empty or parse-zero document = fail parse stage with explicit control event

---

## 6. OUTPUT CONTRACT

### Core Outputs

- MinIO raw object with SHA-256
- PostgreSQL document row
- append-only audit events
- parsed chunk set
- chunk provenance metadata
- chunk embeddings
- Qdrant chunk points
- retrieval/evidence status fields
- signed `FrostbyteExportRecord`
- optional DLQ artifact on sink failure
- SSE event stream for operational visibility

### Required Output Semantics

- core pipeline result reported separately from sink dispatch result
- retrieval status and evidence status reported separately
- per-sink state reported independently
- swap events reported as control-plane events
- evaluation provenance includes gold-set SHA and adapter versioning when enabled

---

## 7. ADAPTER REGISTRY RULES

### Resolution Rules

- resolve exactly one active parser backend
- resolve exactly one active embedding backend
- resolve exactly one active vector store
- resolve zero-to-many sinks
- every resolved adapter must declare capabilities and registry version

### Startup Validation Sequence

1. load env configuration
2. resolve adapter classes
3. run healthchecks
4. validate capability compatibility
5. emit control-plane startup events
6. halt on required adapter failure
7. continue with warning on optional sink failure only

### Adapter Pinning Rules

- pin `(parser, embedder, vector_store)` at intake receipt
- persist pinned versions in document metadata, Qdrant payload, and export record
- prohibit re-resolution for later stages of the same document

### Dimension Swap Rules

- before accepting embedder swap, assert `new_embedder.dimensions == current_vector_store.expected_dimensions`
- on mismatch, reject swap and emit control-plane rejection event
- on accepted swap, mark it effective for next document only
- eval trend discontinuity marker must be emitted on model change
- no regression comparison across discontinuity boundary

---

## 8. OBSERVATORY HANDOFF RULES

### Delivery Mode

- current contract mode = filesystem handoff only
- write JSON to `OBSERVATORY_INPUT_DIR`
- success = atomic file write completed
- REST delivery is out of scope for this contract revision

### Export Rules

- export schema must include chunk list, adapter versions, registry version, collection name, and HMAC signature
- payload signature derived from null-byte-separated fields
- filesystem write must use temp-file then atomic rename
- sink dispatch must not block core pipeline completion for optional sink

### DLQ Rules

- replay signed record only
- re-verify HMAC before replay
- sanitize file names
- DLQ directory must not be web-accessible
- replay must be idempotent with downstream dedupe by SHA-256

---

## 9. VERIFICATION PLAN

### Required Tests

- embedder conformance
- parser conformance
- vector store conformance
- sink conformance
- startup canary probes
- duplicate intake behavior
- monotonic audit state enforcement
- dashboard healthcheck validity
- proxy routing validity
- end-to-end ingest → export handoff
- DLQ replay acceptance
- corrupted DLQ rejection

### Acceptance Gates

- real embeddings produced, not zero vectors
- chunk storage in Qdrant succeeds at chunk granularity
- legacy text intake path writes PostgreSQL records and audit events
- startup fails on dimension mismatch
- accepted swap affects only next document
- Observatory handoff succeeds through filesystem path
- optional sink failure does not erase core success
- SSE stream exposes enriched event payloads
- dashboard container reports healthy with corrected healthcheck

---

## 10. IMPLEMENTATION ORDER

1. Fix PostgreSQL writes in text intake path
2. Implement idempotency and duplicate policy
3. Implement `encoder.py` with `nomic-embed-text-v1.5`
4. Implement chunking and chunk provenance
5. Add norm checks, drift subtype classification, and canary probes
6. Replace stub embedding path with real encoder
7. enforce append-only audit semantics
8. implement adapter protocols and loader
9. implement startup validation and pinning
10. fix dashboard healthcheck and proxy
11. implement `FrostbyteExportRecord` and HMAC signing
12. implement non-blocking Observatory sink and DLQ
13. add conformance tests
14. enrich SSE payloads and dashboard stream console
15. add eval path and trend discontinuity handling

---

## 11. FAILURE POLICY

- Required adapter failure at startup → HALT
- Dimension mismatch at startup or swap → HALT / REJECT SWAP
- Parse zero chunks → FAILED_PARSE
- All chunks degenerate → FAILED_EMBED
- Partial embedding failure → degraded retrieval or incomplete evidence per state model
- Qdrant partial upsert → degraded retrieval, incomplete evidence
- Audit write failure → retrieval may remain ready, evidence becomes incomplete
- Observatory write failure in filesystem mode → sink failure/DLQ; core pipeline unaffected

---

## 12. EVIDENCE REQUIREMENTS

The execution is not complete unless evidence exists for:

- startup adapter resolution
- model warm-load result
- canary probe outcome
- MinIO store
- PostgreSQL insert
- parse completion
- embed completion
- Qdrant write
- audit append
- export record generation
- HMAC creation
- sink delivery or DLQ placement
- healthcheck success
- conformance test results

---

## 13. V&T STATEMENT

**Exists:** An approved Frostbyte research-grade design spec defining Docker Compose, `nomic-embed-text-v1.5`, Qdrant, `unstructured`, adapter registry behavior, Observatory handoff, and dimension swap controls. The C-RSP template structure used for this refactor exists in TLC. :contentReference[oaicite:2]{index=2} :contentReference[oaicite:3]{index=3}

**Non-existent:** Verified production implementation of this full contract, verified passing conformance suite, and verified operational end-to-end execution evidence were not provided in the current request context. :contentReference[oaicite:4]{index=4}

**Unverified:** Actual memory sufficiency for `nomic-embed-text-v1.5` in the target Docker environment, actual GID alignment for shared Observatory volume, and current codebase parity with every contract step remain unverified from the supplied materials. :contentReference[oaicite:5]{index=5}

**Functional status:** This output is a refactored executable build contract text, not a code execution result. It is ready to be used as a build/run contract for implementation work, but it has not itself built or verified the system.
