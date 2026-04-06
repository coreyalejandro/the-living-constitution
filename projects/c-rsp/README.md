# C-RSP folder — Constitutionally-Regulated Single Pass (TLC)

This directory is the **template system** for governed execution in The Living Constitution. **Do not infer authority from filenames alone.** Read the **single-page map** first:

## 1. Start here (mandatory)

| Step | Action |
|------|--------|
| 1 | Open **`CANONICAL_ROLE_MAP.md`** and read **Authority order** and **Downstream gate (A-1 and later)** end-to-end. |
| 2 | Open **`BUILD_CONTRACT.md`** and skim **Canonical Artifact Role** (strict precedence). |
| 3 | Only then open other files below, knowing which **role** each file has. |

If you skip step 1, you risk treating a **helper** or **executed instance** as the **canonical master template** — the mistake this README is designed to prevent.

## 2. What each kind of file is for

| You need… | Open… | Role |
|-----------|--------|------|
| Reusable structure, invariants, Blind Man rules | `BUILD_CONTRACT.md` | **Canonical master template** (highest authority) |
| A fill-in scaffold to draft a new contract | `BUILD_CONTRACT.instance.md` | **Guided instance template** (subordinate to master) |
| Machine-readable section IDs and validation rules | `contract-schema.json` | **Schema artifact** |
| Format for run outcomes / V&T reports | `CRSP_OUTCOME_TEMPLATE.md` | **Outcome artifact** |
| Process notes, PASS 8 profile, examples | `INSTANCE_PROCESS.md`, `PASS8_TEMPLATE.md`, `BUILD_CONTRACT.instance.example.md`, `BUILD_CONTRACT.instance.template.md` | **Helpers only** — not substitutes for the master template |
| Ergonomic scripts / pointers | `workflows/*` | **Helpers only** |
| LLM operator prompt + memory (read root index + C-RSP journal) | `AGENT_PROMPT.md`, `openmemory.md` (repo root), `projects/c-rsp/openmemory.md` | **Helpers only** — hybrid model in `AGENT_PROMPT.md` |
| A real contract for a concrete scope (yours or program work) | `projects/*/BUILD_CONTRACT*`, `instances/*.md`, `BUILD_CONTRACTS/*.md` | **Executed instances** — not reusable templates |

**Conflict rule:** If anything disagrees with **`BUILD_CONTRACT.md`**, the master template wins (unless the repo records a formal supersession).

## 3. How to author a new C-RSP contract (safe path)

1. Read **`CANONICAL_ROLE_MAP.md`** and **`BUILD_CONTRACT.md`** (§§1–6 at minimum).
2. Copy **`BUILD_CONTRACT.instance.md`** to a **new path** — e.g. `projects/<slug>/BUILD_CONTRACT.md`, `projects/c-rsp/instances/<CONTRACT_ID>.md`, or `projects/c-rsp/BUILD_CONTRACTS/<CONTRACT_ID>.md`.
3. Replace every placeholder with concrete values; align section titles with **`contract-schema.json`** `core_sections`.
4. Run preflight / structural checks your contract’s §14 names (e.g. `./scripts/verify_crsp_template_bundle.sh` when comparing to the TLC master template).
5. Emit outcomes with **`CRSP_OUTCOME_TEMPLATE.md`**.

**Do not** “start from” `PASS8_TEMPLATE.md`, `INSTANCE_PROCESS.md`, or `workflows/*` as if they were the master template. Use them only as **helpers** after the master + guided instance are understood.

## 4. Program contracts (A-1 and later)

- **Before A-1 (taxonomy canonicalization):** Re-read **`CANONICAL_ROLE_MAP.md`** → **Downstream gate**.
- **A-1 executed instance (draft):** `BUILD_CONTRACTS/CRSP-A1-TAXONOMY-CANONICALIZATION-001.md` — instantiated from the **master + guided** pattern, not from helper-only files.
- **Plan context:** `plans/master-plan.md` (Series A → A-1).

## 5. Related repo pointers

- Root operator context: `CLAUDE.md` (C-RSP authority table).
- Registry notes: `MASTER_PROJECT_INVENTORY.md` (c-rsp slug).
- Portable snapshot (non-authoritative): `crsp_refactor_bundle_final/projects/c-rsp/` (see bundle README).

---

**Canonical expansion:** `C-RSP` = **Constitutionally-Regulated Single Pass** only (`INVARIANT_TERM_01` in `BUILD_CONTRACT.md`).
