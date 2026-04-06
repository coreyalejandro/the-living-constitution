---
document_type: "Navigational"
id: "DOC-README-ROOT-001"
status: "Active"
canonical_path: "README.md"
next_file: "docs/instructions/FIRST_RUN.md"
last_verified:
  commit: "6219250"
  timestamp: "2026-04-06T02:11:20Z"
---

# The Living Constitution

[![Verify Living Constitution](https://github.com/coreyalejandro/the-living-constitution/actions/workflows/verify.yml/badge.svg)](https://github.com/coreyalejandro/the-living-constitution/actions/workflows/verify.yml)

## What this is

This repository is the **governance overlay** for the Safety Systems Design Commonwealth: the constitutional specification, zero-shot build contracts under `projects/`, verification evidence, and coordination so every claim stays aligned with what the repos actually contain. It is documentation and governance infrastructure first; product application code lives in sibling repositories.

## How this repo is organized

| Area | Role |
| --- | --- |
| `THE_LIVING_CONSTITUTION.md` | Constitutional specification (human-readable) |
| `docs/constitution/` | Documentation law (taxonomy, paths, allowlist, truth hierarchy) |
| `docs/operations/` | Executable operator procedures (bootstrap, verify, rollback) |
| `docs/evidence/` | Evidence maps and verification records |
| `governance/` | **Live** C-RSP governance artifacts (instance, lock, binding) — not under `docs/` |
| `projects/` | Per-project build contracts and overlays |
| `verification/` | Claim-to-evidence surfaces and verifier outputs |
| `scripts/` | Automation including `verify_document_constitution.py` |
| `STATUS.json` / `STATUS.md` | Authoritative current status (PASS 10A); README does not replace them |

**Quick start routing:** `docs/instructions/FIRST_RUN.md` → `docs/operations/BOOTSTRAP.md` → `docs/operations/VERIFY.md`.

**Lost?** Open `docs/HELP.md`.

## Governance and compliance

- Plain-language governance intro: [`governance/README.md`](governance/README.md)
- Documentation standard: [`docs/constitution/DOCUMENTATION_STANDARD.md`](docs/constitution/DOCUMENTATION_STANDARD.md)
- Compliance score artifact (generated locally or in CI): `verification/docs_compliance.json` after `python3 scripts/compliance_score_docs.py --root .`
- Global registry (machine-readable): [`projects/governance/registry.json`](projects/governance/registry.json)

**Compliance summary:** MVDS and extended paths are defined in `config/docs_governance.json`. Run `python3 scripts/compliance_score_docs.py --root .` for a computed score (not hand-waved).

## Current repo status (authoritative)

**Do not** assert operational status here independently of the status surface:

- Read [`STATUS.md`](STATUS.md) (human mirror) or authoritative [`STATUS.json`](STATUS.json).
- Regenerate after inventory or policy changes: `python3 scripts/render_status_surface.py --root .`

## Verification bootstrap

Before running full verification:

```bash
./scripts/bootstrap_repo.sh
```

Shallow clones are rejected until deepened, tags are fetched, and submodules are initialized (PASS 13 / INVARIANT_54–56).
