# `projects/c-rsp/workflows/` — workflow helpers only

**Artifact role:** **Workflow / router artifacts** (see `projects/c-rsp/BUILD_CONTRACT.md` **Canonical Artifact Role**).

This directory holds **ergonomic helpers** (scripts, checklists, or pointers) that assist authors. It does **not** define governing C-RSP structure.

**Related:** Profile/process helpers that live **outside** this directory but still under `projects/c-rsp/` (for example `INSTANCE_PROCESS.md`, `PASS8_TEMPLATE.md`) are the **same authority band** as this folder — see **`Canonical Artifact Role`** row 5 in `projects/c-rsp/BUILD_CONTRACT.md`.

**Subordination (INVARIANT_SEM_03):**

- Files here **must not** override `projects/c-rsp/BUILD_CONTRACT.md` (canonical master template).
- Files here **must not** override `projects/c-rsp/BUILD_CONTRACT.instance.md`’s role as guided instance template (that file lives at the repo path above, not in this folder).
- Files here **must not** substitute for `projects/c-rsp/contract-schema.json` or `projects/c-rsp/CRSP_OUTCOME_TEMPLATE.md`.

If a workflow helper conflicts with rows 1–4 of the authority order in the master template, **the master template wins**.

See also **`SCOPE.md`** in this folder (non-canonical mirrors and grep parity).
