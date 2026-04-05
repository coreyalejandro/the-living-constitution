---
document_type: "Operational"
id: "DOC-GOV-BC-001"
repo_scope: "TLC-Core"
authority_level: "L3"
truth_rank: 2
status: "Active"
canonical_path: "governance/BUILD_CONTRACT.instance.md"
next_file: "docs/operations/BOOTSTRAP.md"
last_verified:
  commit: "af9dfb8"
  timestamp: "2026-04-04T12:00:00Z"
metadata:
  est_time_minutes: 10
  cognitive_load: "Medium"
  requires_interruption_buffer: false
navigation:
  parent_index: "docs/INDEX.md"
  hierarchy_level: "TLC-Core > Governance > Build Contract Instance"
---

# C-RSP instance (governance copy)

## Purpose

This file is the **root-level live governance** copy of the Tier-2 C-RSP instance for TLC documentation constitutionalization. Full section-by-section text lives in the canonical instance path below; this file ensures `governance/` satisfies placement rules without duplicating the entire contract body.

## Canonical instance (authoritative prose)

- **Path:** `projects/document-system/BUILD_CONTRACT.instance.md`
- **Contract ID:** `tlc-docsys-constitutionalization-001`
- **Execution discipline:** **CONTROL_RULE_KBC_01** (single active BUILD_CONTRACT, Kanban-first V&T, no terminal “done” while the board is open) — full text in that file under **Execution discipline — single BUILD_CONTRACT + Kanban-first V&T**. Master template: `projects/c-rsp/BUILD_CONTRACT.md` Section 16; outcome shape: `projects/c-rsp/CRSP_OUTCOME_TEMPLATE.md`.

## What was executed for MVDS + enforcement

The following repository artifacts exist and are enforced by CI:

- Typed YAML frontmatter on governed Markdown surfaces (see `docs/constitution/*` and `scripts/verify_document_constitution.py`).
- Minimum Viable Documentation Set paths listed in `config/docs_governance.json`.
- Root allowlist + validator (`docs/constitution/ROOT_DOC_ALLOWLIST.md`, `scripts/verify_document_constitution.py`).
- Scaffolding: `scripts/docs/tlc-gen.py`.
- Compliance scoring: `scripts/compliance_score_docs.py` (output `verification/docs_compliance.json` in CI).
- Global registry: `projects/governance/registry.json`.

## Next steps for operators

1. Read `governance/README.md` if you are new to C-RSP in this repo.
2. Follow journeys in `docs/INDEX.md` and `docs/HELP.md`.
3. Run documentation verification: `python3 scripts/verify_document_constitution.py --root .`
