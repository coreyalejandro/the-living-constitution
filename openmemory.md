# OpenMemory guide — the-living-constitution

## Overview

Governance overlay / super-repo for Safety Systems Design Commonwealth: constitutional spec, build contracts per project, verification matrix.

## Components

- **`04-consentchain/`** — Canonical ConsentChain constitutional pack: `REPO_MAP.json`, `COMPONENT_REGISTRY.json`, CLAUDE/BUILD_CONTRACT, architecture and safety stubs. Distinct from `projects/consentchain/` git submodule. Registry path semantics (prior sibling vs TLC submodule): `04-consentchain/REGISTRY_PATH_MIGRATION.md`.

- **`MASTER_PROJECT_INVENTORY.json`** / **`MASTER_PROJECT_INVENTORY.md`** — Phase 0 master inventory: TLC `projects/` overlays (**13** slugs including `buildlattice` and `consent-gateway-auth0`), registry cross-refs, sibling path probes, explicit unknowns/anomalies. Source of truth for `scripts/verify_project_topology.py`. Rollout #3 (B.1): `buildlattice_overlay_script` (`projects_buildlattice_overlay_exists`, `expects_tlc_relative_paths` for `projects/buildlattice/*`).

- **`scripts/verify_consentchain_family.py`** — ConsentChain family verifier: required TLC files under `04-consentchain/`, cross-repo JSON checks, `projects/consentchain` + `projects/consent-gateway-auth0` (git submodules per `.gitmodules`), `require_submodule_entries`, optional `--fix-git` / `--update-existing`, reports under `verification/consentchain-family/`. Override via `--config` JSON.

- **`scripts/verify_project_topology.py`** — Validates `projects/` slug set, recorded path probes, `consentchain_family_script.projects_consent_gateway_auth0_overlay_exists`, and `buildlattice_overlay_script` (overlay dir + expected overlay files) against `MASTER_PROJECT_INVENTORY.json` (`--no-probes` for slug-only). Optional `--with-governance` runs `verify_governance_chain.py` after topology passes.

- **`STATUS.json`** / **`STATUS.md`** — PASS 10A sole authoritative current-status surface; `STATUS.md` is rendered only via **`scripts/render_status_surface.py`**. **PASS 11:** Immutable verification anchor via `MASTER_PROJECT_INVENTORY.json` `ci_provenance.verification_anchor_tag` + `verification_anchor_commit` (tag `tlc-gov-verified-<shortsha>`); `STATUS.json` carries `truth_anchor`, `verification_target`, and informational `head_sha`. Verifiers use `tip_state_helpers.git_resolve_ref` (peels annotated tags) + `git_is_ancestor`; INVARIANT_42 compares aggregate to disk excluding `head_sha` (no render required for correctness). Policy: `verification/closed-epistemics-open-interfaces-policy.json`. INVARIANT_38–INVARIANT_42 enforced in `verify_governance_chain.py`. **PASS 10C:** Remote CI adjudication for INVARIANT_43–50: `verification/ci-remote-evidence/record.json` + `ci_provenance` align to GitHub run id and artifact `artifact_commit_hash`; per-invariant IDs appear in uploaded `*-governance.json` `invariants_verified` (stdout is summary-only).

- **PASS 11 invariant lattice** — `00-constitution/invariant-registry.json` (domain, failure_mode, severity, enforcement_hook, evidence_hook, escalation per INVARIANT_01–56); `verification/invariant-failure-map.json` (entries[] failure_mode ↔ registry); `verification/invariant-risk-model.json` (`severity_levels` for critical/high/medium/low); `03-enforcement/enforcement-map.json` (`invariant_risk_bindings`). Completeness enforced in `scripts/verify_governance_chain.py`. PASS 10C repair (2026-03-30) restored missing failure-map/risk-model and registry PASS 11 fields.

- **PASS 12 anchor hardening** — INVARIANT_51–53: `git fetch --tags --force --prune` before checks; local `git rev-parse tag^{commit}`; remote peeled commit via `git ls-remote origin refs/tags/<tag>^{}`; `tip_state_helpers.verification_anchor_pass12_errors`; CI `verify.yml` lists tags for visibility. No HEAD substitute for anchor resolution.

- **PASS 13 distribution** — INVARIANT_54–56: `./scripts/bootstrap_repo.sh` (unshallow, tags, submodules); CI invokes it before verifiers; `assert_not_shallow` + per-`.gitmodules`-path submodule drift checks; ConsentChain bootstrap also refreshes sibling `the-living-constitution/` in CI.

- **`00-constitution/role-registry.json`** — PASS 10B separation of powers: each governance path maps to exactly one role (LEGISLATIVE, EXECUTIVE, JUDICIAL, RECORD, INTERFACE); `scripts/verify_governance_chain.py` loads it for INVARIANT_43–50 (completeness, duplicate paths, judicial write regex, executive legislative-write scan).

- **`scripts/verify_governance_chain.py`** — C-RSP governance chain (Pass 2–13): `jsonschema` Draft 2020-12 validates every `verification/evidence-ledger/*.json` record against `evidence-ledger.schema.json`; validates run artifact against `governance-verification-run.schema.json`; writes `verification/runs/<timestamp>-governance.json` (git commit, structured failures: `broken_chain_links`, `invariant_failures`, `missing_evidence_explicit`, `schema_validation_errors`); INVARIANT_01–INVARIANT_56; PASS 11 invariant completeness + failure-map + risk-model + `invariant_risk_bindings`; enforcement `invariant_ids` must cover all registry; `governance_artifacts.artifact_manifest` + `ci_verification_commands` parity with `.github/workflows/verify.yml`; **Pass 4:** `ci_provenance` in `MASTER_PROJECT_INVENTORY.json` (workflow sha256 drift, alignment with `ci-remote-evidence/record.json` when `status=verified`); **Pass 6:** `tip_state_truth`, `last_remote_qualifying_commit`, protected-surface diff via `scripts/tip_state_helpers.py` + `verification/tip-state-policy.json`; **Pass 7:** `verification/pass7-branch-verification-policy.json` — mutable branch tips must use `pending`+`tip_pending`; `tip_verified` only on frozen contexts (detached HEAD, `provenance/verified-*`, `tlc-gov-verified-*` tag at anchor); INVARIANT_37; **Pass 10A:** STATUS aggregate vs committed files + MD mirror; GitHub Actions: `GITHUB_SHA`/`GITHUB_RUN_ID` binding and newest run file checks. **`scripts/ci_self_verify_governance_artifact.py`** — CI-only download-artifact self-check. **`scripts/sync_ci_provenance_tip_state.py`** — offline tip-field alignment helper (does not promote to verified). Dependencies: `requirements-verify.txt`.

- **`00-constitution/`** — `invariant-registry.json` (INVARIANT_01–50 + F1–F5 markdown paths; PASS 11 taxonomy fields), `doctrine-to-invariant.map.json` (doctrines/articles → invariant ids). Prose summaries: `constitution.md`, `articles.md`, `invariants/F*.md`.

## User Defined Namespaces

- (default) verification
