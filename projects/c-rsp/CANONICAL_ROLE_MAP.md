# C-RSP canonical role map (A-0.1)

**Contract:** CRSP-A0-1-SEMANTIC-CANONICALIZATION-001  
**Purpose:** Single reference for **artifact roles** and **authority order** so executors need not infer from filenames alone.

## Authority order (strict)

| Order | Path | Role |
|------:|------|------|
| 1 | `projects/c-rsp/BUILD_CONTRACT.md` | **Canonical master template** — highest reusable authority for C-RSP structure. |
| 2 | `projects/c-rsp/BUILD_CONTRACT.instance.md` | **Guided instance template** — subordinate; compiles to row 1. |
| 3 | `projects/c-rsp/contract-schema.json` | **Schema artifact** — structural validation surface. |
| 4 | `projects/c-rsp/CRSP_OUTCOME_TEMPLATE.md` | **Outcome artifact** — canonical V&T reporting shape. |
| 5 | `projects/c-rsp/workflows/*` | **Workflow / router artifacts** — helpers only; not truth surfaces. |
| 6 | `projects/*/BUILD_CONTRACT*`, `projects/c-rsp/instances/*.md` | **Executed project contracts** — scope-specific instances; not reusable templates. |

**Conflict rule:** Lower-numbered rows prevail over higher-numbered rows when semantics conflict (full prose: `BUILD_CONTRACT.md` **Canonical Artifact Role**).

## Vocabulary

| Term | Meaning |
|------|---------|
| Canonical master template | Row 1 only. |
| Guided instance template | Row 2 only (`BUILD_CONTRACT.instance.md`). |
| Schema artifact | Row 3. |
| Outcome artifact | Row 4. |
| Workflow / router | Row 5; optional scripts/checklists; subordinate. |
| Executed contract | Row 6; filled, scope-bound. |

## Semantic invariants (short)

- **INVARIANT_SEM_01** — Master path explicit (row 1).
- **INVARIANT_SEM_02** — Guided instance subordinate to master (row 2).
- **INVARIANT_SEM_03** — `workflows/` is helpers only.
- **INVARIANT_SEM_04** — Executed contracts are instances, not canonical templates.
