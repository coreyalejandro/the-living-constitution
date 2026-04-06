# `projects/c-rsp/workflows/` — workflow helpers only

**Artifact role:** **Workflow / router artifacts** (see `projects/c-rsp/BUILD_CONTRACT.md` **Canonical Artifact Role**).

This directory holds **ergonomic helpers** (scripts, checklists, or pointers) that assist authors. It does **not** define governing C-RSP structure.

**Subordination (INVARIANT_SEM_03):**

- Files here **must not** override `projects/c-rsp/BUILD_CONTRACT.md` (canonical master template).
- Files here **must not** override `projects/c-rsp/BUILD_CONTRACT.instance.md`’s role as guided instance template (that file lives at the repo path above, not in this folder).
- Files here **must not** substitute for `projects/c-rsp/contract-schema.json` or `projects/c-rsp/CRSP_OUTCOME_TEMPLATE.md`.

If a workflow helper conflicts with rows 1–4 of the authority order in the master template, **the master template wins**.
