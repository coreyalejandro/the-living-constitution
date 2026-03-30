# TLC governance kit (C-RSP institutionalization template)

Reusable package extracted from **The Living Constitution** for satellite repositories. The Living Constitution continues to use its root `scripts/` unchanged; this directory is the canonical copy for **replication** (PASS 8).

## Contents

| Path | Purpose |
|------|---------|
| `constitution/` | `invariant-registry.json`, `doctrine-to-invariant.map.json`, `invariants/F*.md` |
| `enforcement/` | `enforcement-map.tlc-reference.json` (full TLC map), `enforcement-map.satellite.json` (no topology/consentchain-family modules) |
| `agents/` | `agent-capabilities.json` |
| `verification/` | JSON Schemas, policies (`tip-state-policy.json`, `pass7-branch-verification-policy.json`, `review-escalation-policy.json`), template `GOVERNANCE_SYSTEM_CARD.md`, `MATRIX.md` |
| `scripts/` | `verify_governance_chain.py` (**inventory-driven CI parity**), `verify_institutionalization.py`, `append_regression_ledger.py`, `ci_self_verify_governance_artifact.py`, `governance_failure_injection_tests.py`, `tip_state_helpers.py` |
| `requirements-verify.txt` | `jsonschema` for Draft 2020-12 validation |

## Satellite vs TLC

- **TLC** inventory `ci_verification_commands` includes `verify_project_topology.py --with-governance`.
- **Satellite** repos typically list only `verify_governance_chain.py` and `verify_institutionalization.py`. The kit `verify_governance_chain.py` reads required command lines from `MASTER_PROJECT_INVENTORY.json`, not a hardcoded list.

## Layout

Satellite repos use the same relative paths as TLC by default: `00-constitution/`, `02-agents/`, `03-enforcement/`, `verification/`, `MASTER_PROJECT_INVENTORY.json`, `MASTER_PROJECT_INVENTORY.md`.

## Contract

See `projects/c-rsp/PASS8_TEMPLATE.md` in the Living Constitution repo.
