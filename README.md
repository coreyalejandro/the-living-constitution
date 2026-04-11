---
document_type: "Navigational"
id: "DOC-README-ROOT-001"
status: "Active"
canonical_path: "README.md"
next_file: "docs/instructions/FIRST_RUN.md"
last_verified:
  commit: "cdde092"
  timestamp: "2026-04-06T02:14:24Z"
---

# The Living Constitution

[![Verify Living Constitution](https://github.com/coreyalejandro/the-living-constitution/actions/workflows/verify.yml/badge.svg)](https://github.com/coreyalejandro/the-living-constitution/actions/workflows/verify.yml)

## Research-First Landing

This repository is a governance and research control plane, not a monolithic app.
It houses constitutional specifications, evidence rules, build contracts, and
verification automation used to govern work across the Commonwealth.

Start here if your goal is understanding and evidence:

- `THE_LIVING_CONSTITUTION.md` — constitutional source text.
- `STATUS.json` — authoritative current status surface (machine truth).
- `MASTER_PROJECT_INVENTORY.json` — project census and governance artifact map.
- `docs/operations/VERIFY.md` — operator verification flow.
- `verification/MATRIX.md` — claim-to-evidence ledger.

## Honest Status: Built vs Specified

| Surface | Built Now (verified in repo) | Specified / Target State |
| --- | --- | --- |
| Constitutional specification | `THE_LIVING_CONSTITUTION.md` and constitutional companion docs exist and are versioned. | Continue iterative refinement via amendment process and governed updates. |
| Governance automation | CI `verify.yml` and verifier scripts under `scripts/` are implemented in-repo; operational state is tracked in CI evidence and `STATUS.json`. | Maintain full green verification chain as changes land. |
| Status truth surface | `STATUS.json` and deterministic `STATUS.md` renderer exist (`scripts/render_status_surface.py`). | Keep status aligned with inventory, CI provenance, and truth-boundary policy. |
| Project overlays and contracts | `projects/` contains per-project overlays/build contracts and C-RSP artifacts. | Keep contracts current with real implementation state and evidence. |
| Application implementations | Most product/runtime implementations live in sibling repos or submodules; this repo is primarily governance overlay. | Continue governed execution in target repos without overstating completion in this repo. |
| Research and evidence synthesis | Evidence docs and policy artifacts exist in `docs/` and `verification/`. | Expand with stronger cross-project evidence bundles and reproducible audits. |

## Repo Map

| Area | Role |
| --- | --- |
| `THE_LIVING_CONSTITUTION.md` | Constitutional specification (human-readable) |
| `docs/constitution/` | Documentation law (taxonomy, paths, allowlist, truth hierarchy) |
| `docs/operations/` | Executable operator procedures (bootstrap, verify, rollback) |
| `docs/evidence/` | Evidence maps and verification records |
| `governance/` | Live C-RSP governance artifacts (instance, lock, binding) |
| `projects/` | Per-project build contracts and overlays |
| `verification/` | Claim-to-evidence surfaces and verifier outputs |
| `scripts/` | Automation and verifiers |
| `STATUS.json` / `STATUS.md` | Current status truth surface (authoritative = `STATUS.json`) |

## Operator Routing

- First run: `docs/instructions/FIRST_RUN.md`
- Bootstrap: `docs/operations/BOOTSTRAP.md`
- Verify: `docs/operations/VERIFY.md`
- Recovery: `docs/operations/ROLLBACK.md`
- Help index: `docs/HELP.md`

## Governance and compliance

- Plain-language governance intro: [`governance/README.md`](governance/README.md)
- Documentation standard: [`docs/constitution/DOCUMENTATION_STANDARD.md`](docs/constitution/DOCUMENTATION_STANDARD.md)
- Compliance score artifact (generated locally or in CI): `verification/docs_compliance.json` after `python3 scripts/compliance_score_docs.py --root .`
- Global registry (machine-readable): [`projects/governance/registry.json`](projects/governance/registry.json)

**Compliance summary:** MVDS and extended paths are defined in `config/docs_governance.json`. Run `python3 scripts/compliance_score_docs.py --root .` for a computed score (not hand-waved).

## Status Discipline

Do not treat this README as the canonical status source:

- Read [`STATUS.md`](STATUS.md) (human mirror) or authoritative [`STATUS.json`](STATUS.json).
- Regenerate after inventory or policy changes: `python3 scripts/render_status_surface.py --root .`

## Verification Bootstrap

Before running full verification:

```bash
./scripts/bootstrap_repo.sh
```

Shallow clones are rejected until deepened, tags are fetched, and submodules are initialized (PASS 13 / INVARIANT_54–56).
