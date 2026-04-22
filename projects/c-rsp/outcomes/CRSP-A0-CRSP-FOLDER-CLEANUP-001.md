# C-RSP Build Contract : A-0 C-RSP Folder Cleanup and Canonical Role Normalization — TLC C-RSP System

## Constitutionally-Regulated Single Pass Executable Prompt (Framework)

**Contract ID:** CRSP-A0-CRSP-FOLDER-CLEANUP-001  
**Contract instance:** `projects/c-rsp/BUILD_CONTRACTS/CRSP-A0-CRSP-FOLDER-CLEANUP-001.md`  
**Run id / commit:** Record at promotion time via `git rev-parse HEAD` on branch `claude/restructure-tlc-enterprise-LxIXt` (not embedded here; avoids stale hash).

---

## 1. Constitutional anchor (brief; before V&T)

| Source | Requirement |
|--------|-------------|
| **Article I — Right to Truth** (`governance/constitution/core/articles.md`) | Claims in this outcome are scoped to files edited and commands run in this cleanup pass. |
| **Article III — Verification Before Done** (`governance/constitution/core/articles.md`) | Structural verification via `scripts/verify_crsp_template_bundle.sh` where applicable. |
| **Section 16 Output Format** (`projects/c-rsp/BUILD_CONTRACT.md`) | Kanban-first **V&T** per this template; no narrative after **Functional status**. |

---

## 2. V&T Statement

### 2.1 Visual board (Kanban)

| **BACKLOG** | **IN PROGRESS** | **BLOCKED** | **DONE** |
|-------------|-----------------|-------------|----------|
| — | — | — | A-0 folder cleanup; non-workflow helper boundaries; schema `required_core_section_ids`; BUILD_CONTRACTS convention; guidance/inventory/plan alignment |

**Signals (required, one line each)**

| Signal | Value |
|--------|--------|
| **Build result** | `PASS` |
| **What moved** | C-RSP folder role normalization + schema + inventory/plan + executed instance path |
| **What’s next** | Push branch; confirm CI; proceed to A-1 only per plan gates |

### 2.2 Exists

**Exists**

- Canonical master template role explicit in `projects/c-rsp/BUILD_CONTRACT.md` (**Canonical Artifact Role**); guided instance role explicit in `projects/c-rsp/BUILD_CONTRACT.instance.md` (**Artifact Role**).
- Non-workflow helpers under `projects/c-rsp/` explicitly bounded (same band as `workflows/*`).
- `projects/c-rsp/BUILD_CONTRACTS/CRSP-A0-CRSP-FOLDER-CLEANUP-001.md` as executed instance record for this contract id.
- Schema alignment: `required_core_section_ids` matches `core_sections` ids; authority metadata extended without contradicting master template.

### 2.3 Verified against

**Verified against**

- `./scripts/verify_crsp_template_bundle.sh` → **PASS** (template vs guided vs FDE instance structural compare).
- `python3 -c "import json; json.load(open('projects/c-rsp/contract-schema.json'))"` → **PASS**.
- GitHub Actions **Verify Living Constitution** run **`24015419165`** on commit **`9b260720beec1e71cb71c732f4e38b2a11b16002` → **success** (full verifier suite including C-RSP structural step).

### 2.4 Not claimed

**Not claimed**

- Downstream A-1 program execution, taxonomy edits to `THE_LIVING_CONSTITUTION.md`, or repo-wide parity beyond named surfaces in Section 11 of the governing contract text.

### 2.5 Non-existent

**Non-existent**

- **N/A** — no requirement for a new verifier script solely for this cleanup; existing bundle script remains the structural gate.

### 2.6 Unverified

**Unverified**

- Whether **future** commits after `9b26072` pass CI until each is built (not applicable to this outcome’s closure for `9b26072`).

### 2.7 Functional status

**Functional status**

- **PASS** for A-0 cleanup scope: roles are explicit in text; helpers outside `workflows/` are labeled; executed instances include optional `BUILD_CONTRACTS/` path; inventory and plan do not contradict the repaired hierarchy.

---

*End of report.*
