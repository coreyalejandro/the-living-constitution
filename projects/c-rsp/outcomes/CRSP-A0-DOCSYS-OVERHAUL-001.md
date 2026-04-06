# C-RSP Build Contract : A-0 Documentation System Overhaul — C-RSP template system

## Constitutionally-Regulated Single Pass Executable Prompt (Framework)

**Contract instance:** `CRSP-A0-DOCSYS-OVERHAUL-001` (this outcome)  
**Run id / commit:** see **Verified against** below

---

## 1. Constitutional anchor (brief; before V&T)

| Source | Requirement |
|--------|-------------|
| **Article I — Right to Truth** | Outcome claims are scoped to files touched and commands run in this session. |
| **Article III — Verification Before Done** | Structural verification re-run for FDE bundle; path updates grep-checked. |

---

## 2. V&T Statement

### 2.1 Visual board (Kanban)

| **BACKLOG** | **IN PROGRESS** | **BLOCKED** | **DONE** |
|-------------|-------------------|-------------|----------|
| A-1 taxonomy canonicalization (not in A-0 scope) | — | — | A-0 role map + template repair; FDE instance relocation; script/lock/evidence alignment |

**Signals**

| Signal | Value |
|--------|-------|
| **Build result** | `PASS` (local structural + FDE verifiers) |
| **What moved** | Canonical master `BUILD_CONTRACT.md` (§0 artifact map, §6 Blind Man blocks, §16–17 role fix); guided `BUILD_CONTRACT.instance.md` replaced with placeholder template; executed FDE contract → `projects/c-rsp/instances/CRSP-FDE-CTRL-PLANE-GAPS-002.md`; `contract-schema.json` `validation_model.blind_man_execution`; root `CLAUDE.md`, `MASTER_PROJECT_INVENTORY.md`, `plans/master-plan.md`, `openmemory.md`, FDE docs/twin/evidence updates. |
| **What’s next** | User review; then instantiate A-1 only if template authority is accepted. |

### 2.2 Exists

**Exists**

- `projects/c-rsp/BUILD_CONTRACT.md` — canonical master template with explicit four-class artifact map and §6A–6E execution model (Blind Man + Dual-Topology).
- `projects/c-rsp/BUILD_CONTRACT.instance.md` — guided instance template (18 sections, placeholders only).
- `projects/c-rsp/instances/CRSP-FDE-CTRL-PLANE-GAPS-002.md` — executed Tier-3 FDE gap-closure instance (relocated from prior `BUILD_CONTRACT.instance.md` body).
- `projects/c-rsp/contract-schema.json` — includes `blind_man_execution` under `validation_model`.
- `projects/c-rsp/CRSP_OUTCOME_TEMPLATE.md` — updated for executed vs guided template language.
- `scripts/run_fde_control_plane_verification.sh` and `scripts/verify_fde_control_plane.py` — default instance path → `projects/c-rsp/instances/CRSP-FDE-CTRL-PLANE-GAPS-002.md`.
- `evidence/fde-control-plane/structural-diff-report.json`, `schema-validation-report.json`, `verifier-execution-report.json` — regenerated PASS.

### 2.3 Verified against

**Verified against**

- `python3 scripts/verify_crsp_structure.py --template projects/c-rsp/BUILD_CONTRACT.md --instance projects/c-rsp/instances/CRSP-FDE-CTRL-PLANE-GAPS-002.md` → exit 0, report PASS.
- `python3 scripts/verify_crsp_structure.py --template projects/c-rsp/BUILD_CONTRACT.md --instance projects/c-rsp/BUILD_CONTRACT.instance.md` → exit 0 (guided template preserves 18 section titles).
- `python3 scripts/verify_fde_control_plane.py` (schema + promotion-readiness) → exit 0, reports PASS.

### 2.4 Not claimed

**Not claimed**

- Full repo-wide content parity across every constitutional surface beyond the A-0 named list.
- A-1 taxonomy / domain assignment / Constitutional UI (explicitly out of scope for A-0).
- That every historical `BUILD_CONTRACT.instance.md` reference in the entire repo was updated (grep may still find chat exports or bundle copies).

### 2.5 Non-existent

**Non-existent**

- Automated JSON-schema validator that **enforces** §6A row presence for all Markdown instances (not implemented; structural check is `verify_crsp_structure.py` + human review).

### 2.6 Unverified

**Unverified**

- Remote CI green after push (not run here).
- `python3 scripts/verify_governance_chain.py --root .` full run after all edits (not run in this session).

### 2.7 Functional status

**Functional status**

- Local FDE verification bundle and structural checks PASS; A-0 template hierarchy is **operationally coherent** for the next agent if they use the paths in **Exists**.

---

*End of report.*
