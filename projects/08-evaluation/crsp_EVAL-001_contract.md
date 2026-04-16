<!-- GENERATED FILE: edit JSON source instead.
     source: docs_json/sources/crsp_EVAL-001_contract.json
-->

# C-RSP Instance Contract: EVAL-001

## 1. Constitutional Context

**Binding Authority (Root Trinity):**

- `THE_LIVING_CONSTITUTION.md`
- `CLAUDE.md`
- `MASTER_PROJECT_INVENTORY.md`

**Project Authority:** `projects/08-evaluation/BUILD_CONTRACT.md` (BUILD-EVAL-001)  
**C-RSP Protocol Version:** 2.0  
**Invariant Registry:** `projects/c-rsp/invariant_registry.json` (read-only reference)

**Purpose:**  
EVAL-001 constitutes the Evidence Observatory, responsible for machine-verifiable failure analysis, invariant linkage verification, schema validation, recurrence detection, and CI emission.

## 2. Master Source of Truth

**Primary Source:** `BUILD-EVAL-001` (`projects/08-evaluation/BUILD_CONTRACT.md`)  
**Relationship:** This C-RSP instance derives scope, boundaries, and acceptance criteria from the master contract. Any conflict defers to BUILD-EVAL-001.

**Canonical References:**

- Scope: BUILD-EVAL-001 Section 3
- Asset Inventory: BUILD-EVAL-001 Section 5
- Entry Protocol: BUILD-EVAL-001 Section 7
- Halt Conditions: BUILD-EVAL-001 Section 9 (general) + this contract Section 8 (specific)

**Drift Detection:** If this contract contradicts BUILD-EVAL-001, HALT and escalate via `projects/c-rsp/RECOVERY_PROTOCOL.md`.

## 3. Ordered Operations

Phases execute strictly in order. No phase may proceed without prior PASS and evidence logging.

### Phase 0: Bootstrap Verification (CONSTANT)

**Trigger:** Every agent entry and every execution cycle  
**Operation:** `python3 src/guardian.py --health-check`  
**Expected Output:** `PASS` with JSON evidence  
**Evidence Destination:** `verification/crsp_EVAL-001_log.json`  
**Failure Action:** HALT (see Section 8)

### Phase 1: Asset Topology Validation

**Trigger:** Pre-execution, post-bootstrap  
**Ordered Steps:**

1. Verify `datasets/` and canonical dataset manifests
2. Verify `eval_specs/` and YAML specifications
3. Verify `tlc_evals/` package structure
4. Verify `pyproject.toml`
5. Verify docs (`README.md`, `evidence_summary.md`, `failure_taxonomy.md`, `pattern_analysis.md`)

**Evidence Surface:**

- Output: `verification/topology_validation_YYYYMMDD_HHMMSS.json`
- Retention: 90 days

**Failure Action:** Missing critical assets -> HALT (Section 8)

### Phase 2: Evaluation Suite Configuration

**Trigger:** Post-topology validation  
**Ordered Steps:**

1. Load `eval_specs/invariant_suite.yaml`
2. Load `eval_specs/f2_phantom_completion.yaml`
3. Validate spec files against canonical schemas
4. Verify `tlc_evals/evals/` implementations match specs
5. Load invariants from `tlc_evals/invariants/`

**Evidence Surface:**

- Output: `verification/suite_config_YYYYMMDD_HHMMSS.json`
- Retention: 90 days

**Failure Action:** Specification mismatch -> HALT (Section 8)

### Phase 3: Dataset Validation

**Trigger:** Post-suite configuration  
**Ordered Steps:**

1. Load `datasets/failure_cases.json`
2. Validate dataset schema and integrity
3. Record line-item precision validation results

**Evidence Surface:**

- Output: `verification/dataset_validation_YYYYMMDD_HHMMSS.json`
- Retention: 90 days

### Phase 4: Evaluation Execution

**Trigger:** Post-dataset validation  
**Ordered Steps:**

1. Execute evaluation suite via `tlc_evals`
2. Capture outputs with full provenance
3. Generate metric evidence logs

**Evidence Surface:**

- Output: `verification/eval_results_YYYYMMDD_HHMMSS.json`
- Format: JSON with metric values, confidence intervals, and computation provenance
- Retention: 90 days

**Sandbox Constraints:**

- Timeout: 300 seconds per evaluation
- Memory limit: 4GB per process
- Network isolation: no external calls
- Filesystem: read-only `datasets/`, write-only `verification/`

### Phase 5: Recurrence Pattern Detection

**Trigger:** Post-evaluation execution  
**Ordered Steps:**

1. Load historical failure logs from `verification/`
2. Compare current results against historical patterns
3. Detect recurring failure signatures
4. Flag novel vs known failures

**Evidence Surface:**

- Output: `verification/recurrence_analysis_YYYYMMDD_HHMMSS.json`
- Retention: permanent

### Phase 6: CI Signal Emission

**Trigger:** Post-recurrence analysis  
**Ordered Steps:**

1. Aggregate all evidence from Phases 1-5
2. Compute constitutional compliance bit:
   - `1` (PASS): all phases complete, no halt
   - `0` (FAIL): non-critical validation failure(s)
   - `2` (HALT): critical failure
3. Emit CI-ready signal with evidence hashes
4. Write final execution log

**Evidence Surface:**

- Output log: `verification/crsp_EVAL-001_log.json` (updated)
- CI signal: `verification/ci_signal_YYYYMMDD_HHMMSS.json`
- Format: `{ "status": 1|0|2, "evidence_hash": "sha256:...", "phases_completed": [0-6], "timestamp": "ISO8601" }`
- Retention: permanent

## 4. Execution Flow Control

- Sequential enforcement: phases 0->6 only
- Checkpointing after each phase: `verification/checkpoint_phase{N}_*.json`
- Idempotency required for all phases

**Execution Modes:**

- `FULL_CYCLE`: phases 0-6
- `VALIDATION_ONLY`: phases 0-3
- `RECURRENCE_SCAN`: phases 0,1,2,5
- `RECOVERY_MODE`: resume from last checkpoint after HALT

## 5. Constraints and Controls

**Temporal Constraints:**

- Full cycle max time: 3600 seconds
- Evidence retention: 90 days (configurable to max 365 days)
- Checkpoint retention: 7 days

**Resource Controls:**

- Memory: 4GB max per evaluation process
- Disk: rotate evidence files >100MB
- CPU: throttled

**Data Controls:**

- Datasets are read-only during evaluation
- `invariant_registry.json` is read-only
- Writes to `verification/` are append-only

**Security Controls:**

- Sandbox execution required
- Input hash verification required before processing

## 6. Evidence Surface Definition

**Mandatory Evidence Files (per execution):**

1. `verification/crsp_EVAL-001_log.json` (master execution log)
2. `verification/topology_validation_*.json` (phase 1)
3. `verification/suite_config_*.json` (phase 2)
4. `verification/dataset_validation_*.json` (phase 3)
5. `verification/eval_results_*.json` (phase 4)
6. `verification/recurrence_analysis_*.json` (phase 5)
7. `verification/ci_signal_*.json` (phase 6)

**Schema Validation:** `projects/c-rsp/schemas/evidence_schema.json`  
**Hash Chain:** each evidence file includes `previous_hash`  
**Cross-Reference:** all evidence must include BUILD-EVAL-001 contract hash

## 7. Acceptance Criteria

- [x] AC-001: Bootstrap verification returns PASS with valid JSON log entry
- [x] AC-002: Asset topology validates all critical assets present
- [x] AC-003: Suite configuration validates all specifications
- [x] AC-004: Dataset validation processes all datasets
- [ ] AC-005: Evaluation execution completes within constraints
- [ ] AC-006: Recurrence detection classifies all failures
- [ ] AC-007: CI emission outputs valid signal
- [ ] AC-008: Evidence schema validation and unbroken hash chain
- [ ] AC-009: BUILD_CONTRACT hash referenced in all evidence
- [ ] AC-010: No halt conditions in full cycle

## 8. Halt Conditions (EVAL-001 Specific)

In addition to BUILD-EVAL-001 Section 9, HALT on:

**Critical Asset Absence:**

- `datasets/` missing or empty
- `eval_specs/` missing
- `tlc_evals/` missing
- Core documentation missing

**Configuration Drift:**

- Spec mismatch with `tlc_evals/evals/`
- Corrupt invariant definitions

**Execution Violations:**

- Sandbox escape
- Determinism failure
- Evidence write failure

**Temporal Violations:**

- Full cycle exceeds 3600 seconds
- Referencing checkpoints older than 7 days

## 9. Recovery Protocol (EVAL-001 Specific)

- **Mode A (Resume from Checkpoint):** non-critical halt -> resume from last valid checkpoint
- **Mode B (Validation-Only Reset):** schema drift -> execute `VALIDATION_ONLY`
- **Mode C (Full Re-constitutionalization):** major drift -> archive corrupted evidence, re-bootstrap, execute `FULL_CYCLE`
- **Mode D (Emergency Stand-down):** catastrophic failure -> halt all operations and set SUSPENDED status

## 10. Drift Detection and Correction

**Continuous Monitoring:**

- Guardian health check before every phase
- Hash chain verification at phase transitions
- Asset manifest parity against BUILD-EVAL-001 Section 5

**Auto-correction (minor):**

- Checkpoint cleanup
- Evidence rotation
- Manifest regeneration

**Manual correction (major):**

- Specification updates require human review
- Invariant remapping requires review
- Metric changes require version bump

## 11. Operational Assurance

- Determinism guarantee: identical inputs produce identical evidence hashes (±0.001% variance)
- Integrity guarantee: SHA-256 input hashes included in evidence
- Availability target: 99.9% excluding scheduled maintenance
- Constitutional guarantee: all executions reference BUILD-EVAL-001 hash

## 12. Verification and Traceability

**Audit Trail Requirements:**

- Every operation logs timestamp, phase, operation type, input/output hashes, and agent identifier
- Chain of custody via `previous_evidence_hash`
- Optional GPG signing where keys are available

**Verification Commands:**

```bash
python3 src/guardian.py --verify-evidence projects/08-evaluation/verification/
python3 src/guardian.py --check-compliance EVAL-001
cat verification/crsp_EVAL-001_log.json | jq '.status'
```

## 13. Audit Trail and Change Log

**Contract Versioning:**

- `1.0.0-CONSTITUTIONAL` (2026-04-12): Initial constitutionalization

**Historical Context:**

- Prior state: improvised governance under root `08-evaluation/`
- EVAL-001 state: constitutionalized governance under `projects/08-evaluation/`

## 14. V&T Statement (Verified and True)

**Verification Timestamp:** 2026-04-12 20:40 UTC  
**Verified By:** Guardian Kernel + Principal AI Safety Engineer  
**Master Source Hash:** `5b3f5aefda194314f3b4ea8ef5826a92fb75e86908538197e04378db50bf37df` (BUILD-EVAL-001)

**Existence Verified:**

- Master BUILD_CONTRACT present: CONFIRMED
- Trinity alignment: CONFIRMED
- C-RSP template conformance: CONFIRMED (v2.0)
- Operational phases defined: CONFIRMED

**Truth Claims:**

- This C-RSP instance derives from BUILD-EVAL-001
- Ordered operations provide deterministic, verifiable harness behavior
- Evidence surfaces satisfy C-RSP schema expectations
- Halt conditions preserve constitutional integrity
- Recovery logic addresses non-critical, major, and catastrophic scenarios
- All 14 sections are completed in this instance contract

**Contract Hash (SHA-256):** `be50479b98ce2c45038e10351076d4a34c9c1c9a2e3d7018309501768b87d032`

---

This document is legally void on its own. Its authority derives from the constitutional order of the `the-living-constitution` repository.
