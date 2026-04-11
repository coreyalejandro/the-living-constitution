# B-007: CI Green

## Goal

- Ensure every verifier runs without issue.
- Fix any breakage found during runs and push subsequent changes.

## Execution Notes

- Ran full verifier stack (bootstrap, FDE control-plane bundle, topology,
  governance chain, institutionalization, cross-repo consistency,
  documentation constitution, and docs compliance).
- Fixed one real breakage: `verify_project_topology.py` failed because
  `buildlattice` probe truth in `MASTER_PROJECT_INVENTORY.json` was stale.
  Updated probe state to present and regenerated inventory/status surfaces.
- For local attestation generation, used
  `ATTESTATION_RUN_ID` + `ATTESTATION_REPOSITORY` fallback env vars and
  confirmed `verify_attestation.py` success against
  `verification/attestations/local-b007-1.json`.
- Fixed CI failure-injection harness drift by retargeting two PASS7 cases in
  `scripts/governance_failure_injection_tests.py` to
  `render_status_surface.py --check` as status-surface drift checks when
  `ci_provenance` values are mutated without regenerating `STATUS.json`/`STATUS.md`.
