# C-RSP canonical role map (A-0 + A-0.1)

**Contracts:** CRSP-A0-1-SEMANTIC-CANONICALIZATION-001; **CRSP-A0-CRSP-FOLDER-CLEANUP-001** (folder cleanup + non-workflow helper boundaries + `BUILD_CONTRACTS/` convention).  
**Purpose:** Single reference for **artifact roles** and **authority order** so executors need not infer from filenames alone.

## Downstream gate (A-1 and later)

Use **this file** as the **single-page authority map** before **A-1** (taxonomy / constitution alignment), any new C-RSP contract, or any change that could blur template vs helper vs executed instance:

1. Read the **Authority order** table (rows 1–6) and **Conflict rule** in full.
2. Do **not** treat row **5** (helpers) or row **6** (executed contracts) as the canonical master template (row **1**).
3. If a proposed change contradicts the table, stop and amend **`projects/c-rsp/BUILD_CONTRACT.md`** first (or record a formal supersession path there).

## Authority order (strict)

| Order | Path | Role |
|------:|------|------|
| 1 | `projects/c-rsp/BUILD_CONTRACT.md` | **Canonical master template** — highest reusable authority for C-RSP structure. |
| 2 | `projects/c-rsp/BUILD_CONTRACT.instance.md` | **Guided instance template** — subordinate; compiles to row 1. |
| 3 | `projects/c-rsp/contract-schema.json` | **Schema artifact** — structural validation surface. |
| 4 | `projects/c-rsp/CRSP_OUTCOME_TEMPLATE.md` | **Outcome artifact** — canonical V&T reporting shape. |
| 5 | `projects/c-rsp/workflows/*` **and** `INSTANCE_PROCESS.md`, `PASS8_TEMPLATE.md`, `BUILD_CONTRACT.instance.example.md`, `BUILD_CONTRACT.instance.template.md` (under `projects/c-rsp/`) | **Workflow / profile / example helpers** — peers; helpers only; not truth surfaces. |
| 6 | `projects/*/BUILD_CONTRACT*`, `projects/c-rsp/instances/*.md`, `projects/c-rsp/BUILD_CONTRACTS/*.md` | **Executed project contracts** — scope-specific instances; not reusable templates. |

**Conflict rule:** Lower-numbered rows prevail over higher-numbered rows when semantics conflict (full prose: `BUILD_CONTRACT.md` **Canonical Artifact Role**).

## Memory surfaces (hybrid — LLM / session continuity)

Read **`projects/c-rsp/AGENT_PROMPT.md`** for full rules. Summary:

| Surface | Path | Role |
|---------|------|------|
| TLC index | `openmemory.md` (repo root) | Long-lived project index. |
| C-RSP journal | `projects/c-rsp/openmemory.md` | Append-only log of C-RSP contract sessions. |
| System prompt | `projects/c-rsp/AGENT_PROMPT.md` | Helper (row 5) — pre-flight reads and where to append at session close. |

**Invariant:** C-RSP session appends go to **`projects/c-rsp/openmemory.md`** only; the root file is not the C-RSP run log.

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
- **INVARIANT_SEM_03** — Row 5 (`workflows/*` and listed non-workflow helpers) is helpers only.
- **INVARIANT_SEM_04** — Executed contracts are instances, not canonical templates.

## Non-canonical mirrors (do not use as authority)

| Location | Role |
|----------|------|
| `ChatGPT-AI Governance Frameworks.md` | Chat export; banner marks it non-canonical. |
| `crsp_refactor_bundle_final/projects/c-rsp/` | Portable snapshot; see `crsp_refactor_bundle_final/README.md`. |

Path parity with root `projects/c-rsp/` is **not** maintained automatically. Grep hits in these trees are **historical** unless reconciled to `CANONICAL_ROLE_MAP.md`.

## A-1 and constitution taxonomy (explicit exclusion)

**Not in scope** for A-0 / A-0.1: taxonomy canonicalization, domain assignment, `THE_LIVING_CONSTITUTION.md` edits, or Constitutional UI. Those are separate contracts (e.g. A-1 program); absence here is **contract boundary**, not unmet A-0.1 acceptance.

## CI verification

**Structural:** `scripts/verify_crsp_template_bundle.sh` (also run in `.github/workflows/verify.yml`) compares section titles between the master template and the guided instance + FDE executed instance. Successful runs upload artifact **`c-rsp-structure-<run_id>-<attempt>`** (`verification/c-rsp-structure/*.json`; directory is gitignored locally). **Not automated:** full Markdown validation of §6A ordered-operations table *content* (human review + Blind Man discipline).
