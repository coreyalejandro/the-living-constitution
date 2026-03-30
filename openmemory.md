# OpenMemory guide — the-living-constitution

## Overview

Governance overlay / super-repo for Safety Systems Design Commonwealth: constitutional spec, build contracts per project, verification matrix.

## Components

- **`04-consentchain/`** — Canonical ConsentChain constitutional pack: `REPO_MAP.json`, `COMPONENT_REGISTRY.json`, CLAUDE/BUILD_CONTRACT, architecture and safety stubs. Distinct from `projects/consentchain/` git submodule. Registry path semantics (prior sibling vs TLC submodule): `04-consentchain/REGISTRY_PATH_MIGRATION.md`.

- **`MASTER_PROJECT_INVENTORY.json`** / **`MASTER_PROJECT_INVENTORY.md`** — Phase 0 master inventory: TLC `projects/` overlays (**13** slugs including `buildlattice` and `consent-gateway-auth0`), registry cross-refs, sibling path probes, explicit unknowns/anomalies. Source of truth for `scripts/verify_project_topology.py`. Rollout #3 (B.1): `buildlattice_overlay_script` (`projects_buildlattice_overlay_exists`, `expects_tlc_relative_paths` for `projects/buildlattice/*`).

- **`scripts/verify_consentchain_family.py`** — ConsentChain family verifier: required TLC files under `04-consentchain/`, cross-repo JSON checks, `projects/consentchain` + `projects/consent-gateway-auth0` (git submodules per `.gitmodules`), `require_submodule_entries`, optional `--fix-git` / `--update-existing`, reports under `verification/consentchain-family/`. Override via `--config` JSON.

- **`scripts/verify_project_topology.py`** — Validates `projects/` slug set, recorded path probes, `consentchain_family_script.projects_consent_gateway_auth0_overlay_exists`, and `buildlattice_overlay_script` (overlay dir + expected overlay files) against `MASTER_PROJECT_INVENTORY.json` (`--no-probes` for slug-only). Optional `--with-governance` runs `verify_governance_chain.py` after topology passes.

- **`scripts/verify_governance_chain.py`** — C-RSP governance chain (Pass 2–6): `jsonschema` Draft 2020-12 validates every `verification/evidence-ledger/*.json` record against `evidence-ledger.schema.json`; validates run artifact against `governance-verification-run.schema.json`; writes `verification/runs/<timestamp>-governance.json` (git commit, structured failures: `broken_chain_links`, `invariant_failures`, `missing_evidence_explicit`, `schema_validation_errors`); INVARIANT_01–INVARIANT_36; enforcement `invariant_ids` must cover all registry; `governance_artifacts.artifact_manifest` + `ci_verification_commands` parity with `.github/workflows/verify.yml`; **Pass 4:** `ci_provenance` in `MASTER_PROJECT_INVENTORY.json` (workflow sha256 drift, alignment with `ci-remote-evidence/record.json` when `status=verified`); **Pass 6:** `tip_state_truth`, `last_remote_qualifying_commit`, HEAD vs anchor, protected-surface diff via `scripts/tip_state_helpers.py` + `verification/tip-state-policy.json`; in GitHub Actions: `GITHUB_SHA`/`GITHUB_RUN_ID` binding and newest run file checks. **`scripts/ci_self_verify_governance_artifact.py`** — CI-only download-artifact self-check. **`scripts/sync_ci_provenance_tip_state.py`** — offline tip-field alignment helper (does not promote to verified). Dependencies: `requirements-verify.txt`.

- **`00-constitution/`** — `invariant-registry.json` (INVARIANT_01–10 + F1–F5 markdown paths), `doctrine-to-invariant.map.json` (doctrines/articles → invariant ids). Prose summaries: `constitution.md`, `articles.md`, `invariants/F*.md`.

## User Defined Namespaces

- (default) verification
