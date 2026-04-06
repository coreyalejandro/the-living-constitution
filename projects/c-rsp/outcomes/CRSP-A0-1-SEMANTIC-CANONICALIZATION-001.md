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

- `./scripts/verify_crsp_template_bundle.sh` → PASS (same checks as CI **Verify C-RSP template structure**).
- `python3 scripts/verify_project_topology.py --root . --no-probes` → OK.
- `gh run list -R coreyalejandro/the-living-constitution`: recent **Verify Living Constitution** run on `main` **push** `24009221693` **success** (2026-04-05); proves remote workflow can pass (not a claim about unmerged local commits).

### 2.4 Not claimed

**Not claimed**

- **N/A — explicit A-0.1 contract exclusion:** taxonomy canonicalization, domain assignment, `THE_LIVING_CONSTITUTION.md` taxonomy edits, A-1 program work, Constitutional UI. Documented as out-of-scope in `projects/c-rsp/CANONICAL_ROLE_MAP.md` (A-1 and constitution taxonomy).
- **N/A — non-authoritative archives:** grep parity across `ChatGPT-AI Governance Frameworks.md` and `crsp_refactor_bundle_final/` is not required for A-0.1; those trees are labeled **non-canonical** (HTML comment banner + bundle README). Executors must use `CANONICAL_ROLE_MAP.md`.

### 2.5 Non-existent

**Non-existent**

- **N/A — addressed by follow-up fix:** additional workflow docs (`projects/c-rsp/workflows/SCOPE.md`); CI step **Verify C-RSP template structure** in `.github/workflows/verify.yml` running `scripts/verify_crsp_template_bundle.sh`; `verification/c-rsp-structure/` reports gitignored as generated output.

### 2.6 Unverified

**Unverified**

- **This commit’s** CI result on `origin` after you push the changes in this fix (run id unknown until GitHub completes). **Partial evidence:** `gh run list` shows the **Verify Living Constitution** workflow **succeeding** on a recent `main` push; new steps are not yet exercised on remote until merged.

### 2.7 Functional status

**Functional status**

- **PASS** locally for structural + topology checks; authority order is **explicit in text**; archives and A-1 scope are **bounded** in `CANONICAL_ROLE_MAP.md`; **CI enforces** C-RSP structural alignment on `main` / PRs when the workflow runs.

---

*End of report.*
