# OpenMemory guide — the-living-constitution

## Overview

Governance overlay / super-repo for Safety Systems Design Commonwealth: constitutional spec, build contracts per project, verification matrix.

## Components

- **`04-consentchain/`** — Canonical ConsentChain constitutional pack: `REPO_MAP.json`, `COMPONENT_REGISTRY.json`, CLAUDE/BUILD_CONTRACT, architecture and safety stubs. Distinct from `projects/consentchain/` git submodule. Registry path semantics (prior sibling vs TLC submodule): `04-consentchain/REGISTRY_PATH_MIGRATION.md`.

- **`MASTER_PROJECT_INVENTORY.json`** / **`MASTER_PROJECT_INVENTORY.md`** — Phase 0 master inventory: TLC `projects/` overlays (**13** slugs including `buildlattice` and `consent-gateway-auth0`), registry cross-refs, sibling path probes, explicit unknowns/anomalies. Source of truth for `scripts/verify_project_topology.py`. Rollout #3 (B.1): `buildlattice_overlay_script` (`projects_buildlattice_overlay_exists`, `expects_tlc_relative_paths` for `projects/buildlattice/*`).

- **`scripts/verify_consentchain_family.py`** — ConsentChain family verifier: required TLC files under `04-consentchain/`, cross-repo JSON checks, `projects/consentchain` + `projects/consent-gateway-auth0` (git submodules per `.gitmodules`), `require_submodule_entries`, optional `--fix-git` / `--update-existing`, reports under `verification/consentchain-family/`. Override via `--config` JSON.

- **`scripts/verify_project_topology.py`** — Validates `projects/` slug set, recorded path probes, `consentchain_family_script.projects_consent_gateway_auth0_overlay_exists`, and `buildlattice_overlay_script` (overlay dir + expected overlay files) against `MASTER_PROJECT_INVENTORY.json` (`--no-probes` for slug-only). Optional `--with-governance` runs `verify_governance_chain.py` after topology passes.

- **`scripts/verify_governance_chain.py`** — C-RSP governance chain: requires `00-constitution/invariant-registry.json`, `doctrine-to-invariant.map.json`, `03-enforcement/enforcement-map.json`, `02-agents/agent-capabilities.json`, `verification/evidence-ledger.schema.json`, `verification/evidence-ledger/seed.json`, `verification/governance-verification.template.json`; checks `MASTER_PROJECT_INVENTORY.json#governance_artifacts.canonical_paths` and `meta.generated_at_utc` appears in `MASTER_PROJECT_INVENTORY.md`.

- **`00-constitution/`** — `invariant-registry.json` (INVARIANT_01–10 + F1–F5 markdown paths), `doctrine-to-invariant.map.json` (doctrines/articles → invariant ids). Prose summaries: `constitution.md`, `articles.md`, `invariants/F*.md`.

## User Defined Namespaces

- (default) verification
