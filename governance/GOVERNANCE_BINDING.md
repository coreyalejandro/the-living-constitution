---
document_type: "Constitutional"
id: "DOC-GOV-BIND-001"
repo_scope: "TLC-Core"
authority_level: "L3"
truth_rank: 2
status: "Active"
canonical_path: "governance/GOVERNANCE_BINDING.md"
next_file: "governance/README.md"
last_verified:
  commit: "af9dfb8"
  timestamp: "2026-04-04T12:00:00Z"
metadata:
  est_time_minutes: 5
  cognitive_load: "Low"
  requires_interruption_buffer: false
navigation:
  parent_index: "docs/INDEX.md"
  hierarchy_level: "TLC-Core > Governance > Binding"
---

# Governance binding (TLC core)

This file declares that **live governance artifacts** for this repository are bound to the paths under top-level `governance/` as required by `docs/constitution/DOCUMENTATION_STANDARD.md`.

## Binding statements

1. The active C-RSP instance narrative and acceptance criteria for the documentation system build are recorded in `projects/document-system/BUILD_CONTRACT.instance.md`.
2. The **operational** copy that satisfies root `governance/` placement rules is `governance/BUILD_CONTRACT.instance.md` (summary + pointer to the full instance).
3. `docs/governance/` is **not** used for live governance artifacts in this repository.
4. Amendments to documentation constitutional law follow `docs/constitution/AMENDMENT_PROCESS.md`.

## Verification

| Check | Result |
| --- | --- |
| Governance directory present | Required |
| `scripts/verify_document_constitution.py` | Must exit 0 on clean tree |
