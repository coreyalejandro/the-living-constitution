---
document_type: "Architectural"
id: "DOC-ARCH-REPO-ENHANCEMENT-001"
status: "Active"
canonical_path: "PROGRAM_ARCHITECTURE.md"
authority: "narrative"
truth_surface: "descriptive"
machine_enforced: false
---

# Program Architecture

This document is a narrative architecture guide for the repository. It is not a binding or canonical authority. Canonical governance authority remains in `THE_LIVING_CONSTITUTION.md`, and authoritative operational status remains in `STATUS.json`.

## What this repository contains

The repository operates across three layers that should be read separately:

1. **Governance layer** — constitutional rules, truth hierarchy, build contracts, and verification doctrine.
2. **Research layer** — hypotheses, evidence artifacts, experiments, and evaluation framing.
3. **Product and operator layer** — runnable interfaces, scripts, and control surfaces used to inspect or exercise the governed system.

## Layer map

| Layer | Primary purpose | Main paths | Trust class |
| --- | --- | --- | --- |
| Governance | Declare what is binding and how claims are checked | `THE_LIVING_CONSTITUTION.md`, `projects/c-rsp/`, `docs/constitution/`, `docs/governance/` | Canonical or descriptive depending on file |
| Research | Record hypotheses, evidence, and open questions | `research/`, `experiments/`, `verification/`, `docs/research/` | Mixed: evidence, narrative, and derived |
| Product and operator | Provide runnable interfaces and verification entry points | `src/`, `apps/`, `scripts/` | Implementation or operator surface |

## Trust boundaries

- **Canonical artifacts** define binding rules or authoritative machine-readable state.
- **Narrative artifacts** explain structure, intent, or usage, but do not win conflicts against canonical sources.
- **Derived artifacts** summarize other sources and must be checked back against those sources before being cited as evidence.

## Repository interaction model

| Surface | Role | Notes |
| --- | --- | --- |
| `STATUS.json` | Authoritative operational status | Machine-readable truth anchor |
| `STATUS.md` | Human-readable mirror | Deterministic render of `STATUS.json` |
| `MASTER_PROJECT_INVENTORY.json` | Authoritative project census | Machine-readable inventory truth |
| `PROGRAM_ARCHITECTURE.md` | Architecture explainer | This file is descriptive only |
| `MODULE_STATUS.md` | Derived module summary | Useful orientation, insufficient as standalone evidence |
| `src/tui/` | Terminal interaction prototype | Plain-English local operator surface |
| `scripts/verify_repo_enhancement.py` | Contract-focused verifier | Checks trust metadata and TUI entry point |

## What is not claimed here

- This document does not certify production readiness.
- This document does not upgrade any research claim beyond its existing evidence.
- This document does not replace contract review, evidence inspection, or manual truth-state upgrades.
