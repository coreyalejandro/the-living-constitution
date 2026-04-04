---
document_type: "Constitutional"
id: "DOC-AMEND-001"
repo_scope: "Cross-Repo"
authority_level: "L4"
truth_rank: 1
status: "Active"
canonical_path: "docs/constitution/AMENDMENT_PROCESS.md"
next_file: "docs/constitution/DOCUMENTATION_CHANGELOG.md"
last_verified:
  commit: "af9dfb8"
  timestamp: "2026-04-04T12:00:00Z"
metadata:
  est_time_minutes: 15
  cognitive_load: "Medium"
  requires_interruption_buffer: true
navigation:
  parent_index: "docs/INDEX.md"
  hierarchy_level: "TLC > Constitution > Amendments"
---

# Amendment process (documentation constitution)

## Propose

1. Open a change branch.
2. Add `docs/constitution/amendments/AMENDMENT-DRAFT-<YYYYMMDD>-<slug>.md` describing:
   - problem statement
   - exact files touched
   - enforcement impact (verifiers, CI)
   - rollback plan

## Decide

- Maintainers review for conflicts with `DOCUMENTATION_STANDARD.md` and C-RSP invariants.
- Merge only when `scripts/verify_document_constitution.py` and governance verifiers are green or updated in the same change.

## Log accepted amendments

- Append to `docs/constitution/DOCUMENTATION_CHANGELOG.md` with date, commit, and downstream doc list.

## Downstream flagging

- Any file listed in the amendment’s “downstream” section must receive a frontmatter bump or explicit edit in the same PR, or a tracked follow-up issue linked from the changelog entry.

## SOS

If you are lost, use `docs/HELP.md` and return to `docs/INDEX.md`.
