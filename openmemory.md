# OpenMemory guide — the-living-constitution

## Overview

Governance overlay / super-repo for Safety Systems Design Commonwealth: constitutional spec, build contracts per project, verification matrix.

## Components

- **`04-consentchain/`** — Canonical ConsentChain constitutional pack: `REPO_MAP.json`, `COMPONENT_REGISTRY.json`, CLAUDE/BUILD_CONTRACT, architecture and safety stubs. Distinct from `projects/consentchain/` git submodule. Registry path semantics (prior sibling vs TLC submodule): `04-consentchain/REGISTRY_PATH_MIGRATION.md`.

- **`MASTER_PROJECT_INVENTORY.json`** / **`MASTER_PROJECT_INVENTORY.md`** — Phase 0 master inventory: TLC `projects/` overlays (**13** slugs including `consent-gateway-auth0`), registry cross-refs, sibling path probes, explicit unknowns/anomalies. Source of truth for `scripts/verify_project_topology.py`.

- **`scripts/verify_consentchain_family.py`** — ConsentChain family verifier: required TLC files under `04-consentchain/`, cross-repo JSON checks, `projects/consentchain` + `projects/consent-gateway-auth0` (git submodules per `.gitmodules`), `require_submodule_entries`, optional `--fix-git` / `--update-existing`, reports under `verification/consentchain-family/`. Override via `--config` JSON.

- **`scripts/verify_project_topology.py`** — Validates `projects/` slug set and recorded path probes against `MASTER_PROJECT_INVENTORY.json` (`--no-probes` for slug-only).

## User Defined Namespaces

- (default) verification
