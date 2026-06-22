---
document_type: "Operational"
id: "DOC-STATUS-REPO-ENHANCEMENT-001"
status: "Active"
canonical_path: "MODULE_STATUS.md"
authority: "derived"
truth_surface: "derived"
machine_enforced: false
---

# Module Status

This document is a **derived status surface**. It summarizes current repository modules from listed source artifacts. It is **not standalone evidence** and must be checked against `/home/runner/work/the-living-constitution/the-living-constitution/STATUS.json`, `/home/runner/work/the-living-constitution/the-living-constitution/MASTER_PROJECT_INVENTORY.json`, the cited paths below, and fresh command output before any truth-state upgrade.

## Source metadata

- Primary authority for current repo status: `STATUS.json`
- Primary authority for project inventory: `MASTER_PROJECT_INVENTORY.json`
- Architecture framing: `PROGRAM_ARCHITECTURE.md`
- TUI implementation surface: `src/tui/index.js`

## Summary

| Module | Current framing | Source |
| --- | --- | --- |
| Governance core | Active constitutional and documentation governance surfaces exist | `THE_LIVING_CONSTITUTION.md`, `docs/constitution/`, `docs/governance/` |
| Verification scripts | Active verification tooling exists for governance and topology checks | `scripts/verify_governance_chain.py`, `scripts/verify_project_topology.py` |
| Control-plane web app | Existing separate web control-plane surface remains present | `apps/tlc-control-plane/` |
| Terminal UI prototype | Partial runnable repository-status prototype | `src/tui/index.js`, `src/interfaces/research-enablement.js` |
| Trust-surface documentation | Active descriptive guidance for artifact classes and non-claims | `PROGRAM_ARCHITECTURE.md`, `SOCIOTECHNICAL_CONSTITUTION.md`, `docs/governance/TRUST_SURFACE_GUIDE.md` |

## Reading rule

Use this file to orient yourself. Do **not** use it by itself to prove implementation completeness, research validity, accessibility effectiveness, or production readiness.
