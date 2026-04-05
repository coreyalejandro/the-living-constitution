# Waiver — MVP closeout AC-07 (migration `--apply`)

**AC:** AC-07 (`projects/document-system/BUILD_CONTRACT.instance.MVP-CLOSEOUT-001.md`)

**Date (UTC):** 2026-04-05

## Scope

AC-07 requires either:

- `scripts/migrate_docs_legacy.py --apply` performing documented moves with report update, **or**
- this formal waiver.

## Decision

**Waiver granted.** Automated `--apply` moves are **not** executed in this MVP closeout pass.

## Rationale

1. `scripts/migrate_docs_legacy.py` remains **report-only**; `--apply` does not perform `git mv` (by design until a guarded mapping exists).
2. Remaining `docs_without_frontmatter` entries in `verification/docs_migration_report.json` are **legacy / archive / front-door** surfaces outside the MVDS closure; bringing them under MVDS is **incremental** work, not a blocker for the documentation constitution + verifier stack already in force for MVDS paths.
3. Root Markdown files listed as `root_candidate` include constitutional and operational anchors (`THE_LIVING_CONSTITUTION.md`, `README.md`, `HANDOFF.md`, etc.) that **must** stay at repo root by policy.

## Pass condition (AC-07)

This file **lists AC-07** and provides **maintainer sign-off** below.

---

**Maintainer sign-off**

- **Name / role:** Repository maintainer (The Living Constitution)
- **Decision:** Waive AC-07 automated `--apply` for MVP closeout `tlc-docsys-mvp-closeout-001`.
- **Date:** 2026-04-05
