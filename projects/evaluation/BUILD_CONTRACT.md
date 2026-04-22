# Build Contract: EVAL-001 Evidence Observatory

## 1. Current State (Honest)

`projects/evaluation/` contains the evaluation package (`tlc_evals/`), dataset artifacts (`datasets/`), evaluation specifications (`eval_specs/`), and supporting documentation (`README.md`, `evidence_summary.md`, `failure_taxonomy.md`, `pattern_analysis.md`, `pyproject.toml`).

`projects/evaluation/verification/` now contains full-cycle EVAL-001 evidence artifacts, including phase checkpoints, evaluation results, recurrence analysis, and CI signal output.

## 2. Target State (What This Contract Enables)

EVAL-001 operates as the constitutional Evidence Observatory for machine-verifiable failure analysis, invariant linkage verification, schema validation, recurrence detection, and CI emission.

## 3. Scope

This contract governs:

1. Topology validation for `projects/evaluation/` assets
2. Eval spec loading and implementation parity checks
3. Dataset schema/integrity validation
4. Evaluation execution with provenance and metric outputs
5. Historical recurrence detection
6. CI signal emission and constitutional compliance bit generation
7. Evidence schema and hash-chain integrity validation

Out of scope:

- Modifying constitutional root artifacts
- Mutating `projects/c-rsp/invariant_registry.json`
- External network-dependent evaluation workflows

## 4. Acceptance Criteria

- AC-001: Bootstrap verification returns PASS with JSON evidence
- AC-002: Asset topology validates all critical assets present
- AC-003: Suite configuration validates all specifications
- AC-004: Dataset validation processes all datasets
- AC-005: Evaluation execution completes within constraints
- AC-006: Recurrence detection classifies all failures
- AC-007: CI emission outputs valid signal
- AC-008: Evidence schema validation passes and hash chain is intact
- AC-009: BUILD_CONTRACT hash is referenced by evidence
- AC-010: No halt conditions are triggered in full cycle

## 5. Asset Inventory

Required assets:

- `projects/evaluation/datasets/failure_cases.json`
- `projects/evaluation/eval_specs/invariant_suite.yaml`
- `projects/evaluation/eval_specs/f2_phantom_completion.yaml`
- `projects/evaluation/tlc_evals/` (all subpackages)
- `projects/evaluation/pyproject.toml`
- `projects/evaluation/README.md`
- `projects/evaluation/evidence_summary.md`
- `projects/evaluation/failure_taxonomy.md`
- `projects/evaluation/pattern_analysis.md`

## 6. Evidence Required

Per execution, produce:

1. `verification/crsp_EVAL-001_log.json`
2. `verification/topology_validation_*.json`
3. `verification/suite_config_*.json`
4. `verification/dataset_validation_*.json`
5. `verification/eval_results_*.json`
6. `verification/recurrence_analysis_*.json`
7. `verification/ci_signal_*.json`

All evidence must validate against `projects/c-rsp/schemas/evidence_schema.json`.

## 7. Entry Protocol

Entry order is mandatory:

1. Run `python3 src/guardian.py --health-check` (Phase 0)
2. Validate topology (Phase 1)
3. Validate suite configuration (Phase 2)
4. Validate dataset(s) (Phase 3)
5. Execute evaluations (Phase 4)
6. Run recurrence detection (Phase 5)
7. Emit CI signal (Phase 6)

No phase skipping is permitted.

## 8. Implementation Spec

- Enforce sequential phase execution 0 -> 6
- Checkpoint after each phase into `verification/checkpoint_phase{N}_*.json`
- Use append-only writes for `verification/`
- Enforce evaluation sandbox constraints:
  - 300s timeout per evaluation
  - 4GB memory cap per process
  - no network access
  - read-only `datasets/`, write-only `verification/`
- Compute evidence hash chain via `previous_hash`
- Include BUILD-EVAL-001 source hash in all evidence

Execution modes:

- `FULL_CYCLE`: phases 0-6
- `VALIDATION_ONLY`: phases 0-3
- `RECURRENCE_SCAN`: phases 0,1,2,5
- `RECOVERY_MODE`: resume from last valid checkpoint

## 9. Halt Conditions

HALT on:

- Missing critical assets (`datasets/`, `eval_specs/`, `tlc_evals/`, required docs)
- Spec/implementation drift between eval specs and `tlc_evals/evals/`
- Invariant corruption or load failure
- Sandbox violation or determinism failure
- Evidence write failure
- Runtime over 3600 seconds for full cycle
- Use of stale checkpoints older than 7 days

Escalation path: `projects/c-rsp/RECOVERY_PROTOCOL.md`.
