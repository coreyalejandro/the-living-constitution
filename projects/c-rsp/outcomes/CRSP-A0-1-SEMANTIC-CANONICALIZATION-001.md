# C-RSP Build Contract : A-0.1 Semantic Canonicalization — C-RSP artifact roles

## Constitutionally-Regulated Single Pass Executable Prompt (Framework)

**Contract ID:** CRSP-A0-1-SEMANTIC-CANONICALIZATION-001

---

## 2. V&T Statement

### 2.1 Visual board (Kanban)

| **BACKLOG** | **IN PROGRESS** | **BLOCKED** | **DONE** |
|-------------|-------------------|-------------|----------|
| — | — | — | A-0.1 semantic role map; authority order; surface alignment |

### 2.2 Exists

**Exists**

- `projects/c-rsp/BUILD_CONTRACT.md` — **Canonical Artifact Role** section + **INVARIANT_SEM_01–04**; updated artifact class map.
- `projects/c-rsp/BUILD_CONTRACT.instance.md` — **Artifact Role** section (subordinate to master; disclaims canonical-master authority).
- `projects/c-rsp/CANONICAL_ROLE_MAP.md` — standalone role map artifact.
- `projects/c-rsp/workflows/README.md` — bounds `workflows/` as helpers only (INVARIANT_SEM_03).
- `projects/c-rsp/contract-schema.json` — `validation_model.authority_order_crsp_a0_1`.
- `projects/c-rsp/CRSP_OUTCOME_TEMPLATE.md` — outcome-artifact role line.
- Root `CLAUDE.md` — numbered authority table 1–6.
- `MASTER_PROJECT_INVENTORY.md` + `MASTER_PROJECT_INVENTORY.json` — c-rsp notes aligned.
- `plans/master-plan.md` — A-0.1 session + subsection.

### 2.3 Verified against

**Verified against**

- `python3 scripts/verify_crsp_structure.py` (template vs `BUILD_CONTRACT.instance.md` and vs FDE instance) → PASS.
- `python3 scripts/verify_project_topology.py --root . --no-probes` → OK.

### 2.4 Not claimed

**Not claimed**

- Taxonomy / domain assignment / `THE_LIVING_CONSTITUTION.md` rewrite (out of scope for A-0.1).

### 2.5 Non-existent

**Non-existent**

- Non-README files under `projects/c-rsp/workflows/` beyond `README.md` (folder scaffold only).

### 2.6 Unverified

**Unverified**

- Post-push remote CI (not run here).

### 2.7 Functional status

**Functional status**

- **PASS** for local structural + topology checks; authority order is **explicit in text** without relying on filename intuition alone.

---

*End of report.*
