---
document_type: "Constitutional"
id: "DOC-CANON-PATH-001"
repo_scope: "Cross-Repo"
authority_level: "L4"
truth_rank: 1
status: "Active"
canonical_path: "docs/constitution/CANONICAL_PATHS.md"
next_file: "docs/constitution/ROOT_DOC_ALLOWLIST.md"
last_verified:
  commit: "f22fd8d"
  timestamp: "2026-04-06T02:09:08Z"
metadata:
  est_time_minutes: 12
  cognitive_load: "Medium"
  requires_interruption_buffer: false
navigation:
  parent_index: "docs/INDEX.md"
  hierarchy_level: "TLC > Constitution > Canonical Paths"
---

# CANONICAL_PATHS

This file defines **where substantive documentation and governance artifacts must live** in repositories governed by The Living Constitution.

## Authority

- Parent standard: `docs/constitution/DOCUMENTATION_STANDARD.md`
- Root policy companion: `docs/constitution/ROOT_DOC_ALLOWLIST.md`

## Canonical locations

| Class | Path | Notes |
| --- | --- | --- |
| Constitution | `docs/constitution/` | Documentation law, terminology, truth hierarchy, allowlist |
| Architecture | `docs/architecture/` | System structure (create when needed) |
| Operations | `docs/operations/` | Executable operator procedures |
| Instructions | `docs/instructions/` | Tutorials and first-run paths |
| Evidence | `docs/evidence/` | Evidence maps and verification records |
| Navigation | `docs/INDEX.md`, `docs/HELP.md` | Entry and triage |
| Live governance | `governance/` **only** | Build contract instance, lock, binding |
| Amendment records | `docs/constitution/amendments/` | Proposed and accepted amendment packets |
| Changelog surfaces | `docs/constitution/DOCUMENTATION_CHANGELOG.md` | Standard and downstream impact |
| Help / SOS | `docs/HELP.md` | Escape hatch and triage |

## Governance placement rule

- **Valid:** top-level `governance/` for live governance artifacts in governed repos.
- **Invalid:** `docs/governance/` as a canonical home for live governance artifacts (do not place `BUILD_CONTRACT.instance.md`, locks, or binding files there).

## Portfolio / TLC core

- Global registry: `projects/governance/registry.json`
- Verification outputs may land under `verification/` per existing TLC conventions.

## Blind Man’s Test

A reader must be able to answer “where is live governance?” without guessing: **`governance/` at repository root**.
