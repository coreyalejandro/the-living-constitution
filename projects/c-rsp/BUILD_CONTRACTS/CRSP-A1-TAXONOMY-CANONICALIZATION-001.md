# C-RSP Build Contract : A-1 Taxonomy Canonicalization — TLC constitutional surfaces

## Constitutionally-Regulated Single Pass Executable Prompt

## 0. Instance Governance

- **Artifact class:** **Executed contract instance** (Draft — not Active until preflight and acceptance criteria are satisfied).
- **Authoring basis:** This file was drafted from **`projects/c-rsp/BUILD_CONTRACT.md`** (canonical master template) and **`projects/c-rsp/BUILD_CONTRACT.instance.md`** (guided instance template). It was **not** sourced from helper-only files (`PASS8_TEMPLATE.md`, `INSTANCE_PROCESS.md`, `workflows/*`) as authority.
- **Canonical expansion:** `C-RSP` = Constitutionally-Regulated Single Pass only (**INVARIANT_TERM_01**).
- **Mandatory pre-read:** `projects/c-rsp/CANONICAL_ROLE_MAP.md` (**Downstream gate** section) before execution or promotion.
- **Schema version:** 1.0.0 (`projects/c-rsp/contract-schema.json`).

---
## 1. Contract Identity

- **Contract Title:** A-1 Taxonomy Canonicalization — TLC constitutional surfaces
- **Contract ID:** CRSP-A1-TAXONOMY-CANONICALIZATION-001
- **Version:** 0.2.0
- **Schema Version:** 1.0.0
- **Status:** Draft
- **Adoption Tier:** Tier-3-Constitutional
- **System Role:** Align **Article / Domain / Institution / Project / Verification** taxonomy across `THE_LIVING_CONSTITUTION.md`, root `CLAUDE.md`, and `MASTER_PROJECT_INVENTORY.*` per Series A in `plans/master-plan.md`.
- **Primary Objective:** Produce three aligned, taxonomy-canonical truth surfaces plus registry/config updates without contradicting **INVARIANT_SEM_01–04** or the C-RSP authority order.
- **Scope Boundary:** Files listed in §11 and **Files to Modify** in `plans/master-plan.md` §A-1; **not** A-0 / A-0.1 role re-litigation.
- **Not Claimed:** A-2–A-4, Series B–D, product UI, non-TLC repos.

---
## 2. Contract Topology + Profile

- **Topology Mode:** TLC-Core
- **Profile Type:** Core
- **Profile Overlay Source:** `projects/c-rsp/BUILD_CONTRACT.md`
- **Verifier Class:** core-verifier
- **Authoritative Truth Surface:** `THE_LIVING_CONSTITUTION.md`, root `CLAUDE.md`, `MASTER_PROJECT_INVENTORY.json`, `MASTER_PROJECT_INVENTORY.md`, `config/domains.ts`, `config/projects.ts` (as modified by this contract)
- **Instance Artifact Path:** `projects/c-rsp/BUILD_CONTRACTS/CRSP-A1-TAXONOMY-CANONICALIZATION-001.md` (this file)
- **Governance Lock Path:** `projects/c-rsp/governance-template.lock.json` (repo standard; pin on promotion)

### 2A. Profile Merge Rule

Per master §2A. Specialization only for taxonomy/registry fields; **no** override of canonical terminology, section order, halt semantics, or **INVARIANT_SEM_01–04**.

### 2B. Instance Rule

Per master §2B. This instance is invalid until placeholders are resolved, preflight passes, and schema alignment is confirmed.

---
## 3. Baseline State

- **Existing Repo / System:** `/Users/coreyalejandro/Projects/the-living-constitution`
- **Baseline Commit / Anchor:** Record at execution start (`git rev-parse HEAD`).
- **Verified Existing Assets:** A-0 / A-0.1 / CRSP-A0-CRSP-FOLDER-CLEANUP-001 complete; `CANONICAL_ROLE_MAP.md` and `projects/c-rsp/README.md` describe roles.
- **Known Constraints:** Taxonomy must stay consistent with `governance/constitution/core/invariant-registry.json` and role separation of powers.
- **Known Gaps:** Draft — domain registry shape and Article VI text must be finalized in execution.
- **Legacy Migration Context:** N/A

---
## 4. Dependencies and Inputs

- **Required Inputs:** Master plan §A-1 (Files to Modify / Read); `projects/c-rsp/README.md`; `CANONICAL_ROLE_MAP.md`; `BUILD_CONTRACT.md`; `contract-schema.json` — **Dependencies**
- **External Dependencies:** none
- **Governance Dependencies:** `governance/constitution/core/invariant-registry.json`, `governance/constitution/core/role-registry.json`, `governance/constitution/core/doctrine-to-invariant.map.json`
- **Forbidden Assumptions:** Do not treat helpers as master template; do not assign domains without evidence.

### 4A. Cross-Repo Governance Dependency Graph

- **Parent Constitutional Source:** `projects/c-rsp/BUILD_CONTRACT.md`
- **Shared Overlay Profiles:** none
- **Dual-Topology Linked Repos:** N/A for this scope
- **Satellite Dependents:** none
- **Drift Detection Scope:** Parity across the three truth surfaces + config TS files

---
## 5. Risk + Control Classification

- **Risk Class:** High
- **Side-Effect Class:** Internal
- **External Action Scope:** none
- **Stop/Override Required:** Yes
- **Recovery Mode:** Controlled

### 5A. Conditional Stop / Override Rule

Per master §5A when triggers apply: user stop/override; safe state = no promotion of taxonomy claims until all three surfaces agree.

---
## 6. Execution Model

- **Execution Mode:** Single-pass deterministic build contract
- **Decision Closure Rule:** No open-ended branches in executable sections
- **Fallback Rule:** Ambiguity → halt or escalation
- **Generated Artifacts:** Updated constitution article, registry tables, config TS, `CRSP_OUTCOME_TEMPLATE.md` outcome for A-1
- **Promotion Target:** Frozen A-1 with verifier exit 0 and evidence recorded

### 6A. Ordered Operations (Blind Man Test)

| **Step ID** | **Actor** | **Action** | **Inputs** | **Outputs** | **Verify** | **If Failure** |
|-------------|-----------|------------|------------|-------------|------------|----------------|
| OP-01 | human \| agent | Read `CANONICAL_ROLE_MAP.md` (full) + `projects/c-rsp/README.md` | Paths above | Confirmed role map understanding | Text Q&A or checklist | HALT — do not edit truth surfaces |
| OP-02 | human \| agent | Diff `plans/master-plan.md` §A-1 vs current three surfaces | plan + constitution + CLAUDE + inventory | Gap list | Diff / table | HALT if scope unclear |
| OP-03 | human \| agent | Author `Article VI` / taxonomy section per plan | `THE_LIVING_CONSTITUTION.md` | Patched constitution | Read + peer review | Rollback |
| OP-04 | human \| agent | Update Project Registry + registry JSON/MD + config | Listed files | Aligned surfaces | `verify_project_topology.py`, `verify_governance_chain.py` | HALT on verifier failure |
| OP-05 | human \| agent | Structural preflight (instance vs master template) | `BUILD_CONTRACT.md`, this instance | `verification/c-rsp-structure/structural-a1-taxonomy.json` | `python3 scripts/verify_crsp_structure.py` (see §14) | HALT on FAIL |

### 6B. Halt Conditions (instance-local)

| **Condition** | **Stop Reason** | **Next Action** |
|---------------|-----------------|-----------------|
| Any surface contradicts another on canonical domain | Drift | Reconcile before continuing |
| Verifier non-zero | Evidence failure | Fix and re-run |

### 6C. Success Conditions

- **Success:** `verify_governance_chain.py` and `verify_project_topology.py --with-governance` exit 0; three surfaces agree on taxonomy layers.
- **Done:** A-1 outcome artifact exists; status → Frozen per lifecycle.

### 6D. Major Component Implementation Snippets

**Governance / registry only:** Material edits are Markdown constitution surfaces, `MASTER_PROJECT_INVENTORY.*`, and TypeScript config (`config/domains.ts`, `config/projects.ts`). Use the **Component** block shape from master §6D only if a change introduces non-trivial new interfaces; otherwise state **N/A** for this run and cite exact file paths in §11.

### 6E. Dual-Topology Rule

N/A — TLC-Core only (no integrated/standalone twin path for A-1).

---
## 7. Lifecycle State Machine

### Allowed States

- **Draft**
- **Active**
- **Frozen**
- **Superseded**

### Transition Rules

- **Draft → Active** requires: §§7–17 present with no `[REQUIRED]` / TBD placeholders; `verify_crsp_structure.py` PASS (§14); executor attests `CANONICAL_ROLE_MAP.md` (**Downstream gate**) read; risk/control block complete.
- **Active → Frozen** requires: all §9 acceptance criteria satisfied; `verify_governance_chain.py` and `verify_project_topology.py --with-governance` exit 0 after truth-surface edits; A-1 outcome artifact saved under `projects/c-rsp/outcomes/` using `CRSP_OUTCOME_TEMPLATE.md`.
- **Frozen → Superseded** requires: successor contract instance references this Contract ID.
- Any invalid transition **halts** and records rationale in evidence.

### Transition Evidence

- Git commits touching listed files in `plans/master-plan.md` §**Files to Modify (A-1)**.
- `verification/c-rsp-structure/structural-a1-taxonomy.json` (structural preflight).
- Governance run artifact under `verification/runs/` from `verify_governance_chain.py`.

---
## 8. Invariants

### Required Global Invariants

- **INVARIANT_TERM_01** — C-RSP expands only to *Constitutionally-Regulated Single Pass*.
- **INVARIANT_SCHEMA_01** — Instance aligns to `contract-schema.json` core section ids.
- **INVARIANT_EXEC_01–05** — Executable sections name paths, verifiers, and halt behavior.
- **INVARIANT_CTRL_01** — Risk class and stop/override recorded.
- **INVARIANT_LIFE_01** — Lifecycle states and transitions explicit.
- **INVARIANT_REC_01** — Evidence and rollback hooks declared.

### Profile Invariants (A-1 — taxonomy / authority)

- **INVARIANT_SEM_01** — Canonical master remains `projects/c-rsp/BUILD_CONTRACT.md`; taxonomy work does not replace it.
- **INVARIANT_SEM_02** — Guided instance `BUILD_CONTRACT.instance.md` stays subordinate; A-1 executed scope is **this file**.
- **INVARIANT_SEM_03** — Helpers (`PASS8_TEMPLATE.md`, `INSTANCE_PROCESS.md`, `workflows/*`) are not cited as authority for taxonomy edits.
- **INVARIANT_SEM_04** — This file is an **executed instance**, not a new reusable master template.
- **INVARIANT_TAXO_01** — The five layers **Article → Domain → Institution → Project → Verification** appear consistently across `THE_LIVING_CONSTITUTION.md`, root `CLAUDE.md`, and `MASTER_PROJECT_INVENTORY.*` after execution.
- **INVARIANT_TAXO_02** — Domain assignments and institution→project mapping are evidence-backed (inventory / build contracts / probes), not invented in a single surface only.

---
## 9. Acceptance Criteria

| ID | Requirement | Verification Method | Pass Condition |
|----|-------------|---------------------|----------------|
| AC-01 | Structural alignment of this instance to master template | `python3 scripts/verify_crsp_structure.py --template projects/c-rsp/BUILD_CONTRACT.md --instance projects/c-rsp/BUILD_CONTRACTS/CRSP-A1-TAXONOMY-CANONICALIZATION-001.md --report verification/c-rsp-structure/structural-a1-taxonomy.json` | `overall` = `PASS` in report JSON |
| AC-02 | Governance chain after truth-surface edits | `python3 scripts/verify_governance_chain.py --root .` | Exit 0 |
| AC-03 | Project topology + governance | `python3 scripts/verify_project_topology.py --root . --with-governance` | Exit 0 |
| AC-04 | Constitution + CLAUDE + inventory taxonomy parity | Diff / table review per `plans/master-plan.md` §Verification items 4–5 | Same layer names and domain assignments on all three surfaces |
| AC-05 | Files-to-modify completeness | Checklist vs `plans/master-plan.md` §**Files to Modify (A-1)** | Every listed file either updated or explicitly scoped out with halt record |
| AC-06 | Cross-repo governance (ConsentChain submodule) | `python3 scripts/verify_cross_repo_consistency.py --canonical-root . --target-root projects/consentchain` | Exit 0 when submodule is in scope for the branch |
| AC-07 | Outcome artifact | Saved run using `projects/c-rsp/CRSP_OUTCOME_TEMPLATE.md`; cites **CONTROL_RULE_KBC_01** | File exists under `projects/c-rsp/outcomes/` with matching Contract ID |
| AC-08 | Status honesty | Instance **Status** field | **Draft** until AC-01–05 satisfied for **Active**; **Frozen** only after execution closure |

---
## 10. Rollback & Recovery

- **Safe-State Definition:** Repo state at `git rev-parse HEAD` immediately before first taxonomy edit in this execution (tag or branch backup recommended for Tier-3).
- **Rollback Procedure:** Revert or restore `THE_LIVING_CONSTITUTION.md`, root `CLAUDE.md`, `MASTER_PROJECT_INVENTORY.json`, `MASTER_PROJECT_INVENTORY.md`, `config/domains.ts`, `config/projects.ts` to safe-state commit; re-run AC-02–AC-03; do not claim Frozen until verifiers pass.
- **Recovery Authority:** Human constitutional maintainer or delegated agent with merge rights.
- **Rollback Evidence Paths:** Git revert SHA or branch name recorded in A-1 outcome **Verified against** section.
- **Partial Execution Handling:** Partial edits to only one truth surface are **invalid** for promotion — reconcile or rollback per §6B.

---
## 11. Evidence + Truth Surface

- **Primary Evidence Paths:** Patches/commits for files in `plans/master-plan.md` §**Files to Modify (A-1)**; `verification/c-rsp-structure/structural-a1-taxonomy.json`; `verification/runs/*-governance.json`; optional `projects/c-rsp/outcomes/CRSP-A1-TAXONOMY-CANONICALIZATION-001.md` (or id-matched outcome filename).
- **Generated Reports:** Structural JSON (§14); governance chain JSON; `MASTER_PROJECT_INVENTORY` sync artifacts as applicable.
- **Audit Artifacts:** Outcome file per **CRSP_OUTCOME_TEMPLATE.md**; CI run id when **Verify Living Constitution** is used.
- **Evidence Boundary:** Does not assert product-repo behavior outside TLC; sibling paths in inventory remain **probes** unless this contract explicitly changes them.
- **Truth Discipline:** No stronger claim than verifier exit codes and file diffs allow (**Article I / III**).

---
## 12. Conflict Matrix

| Conflict Type | Example | Severity | Resolution |
|---------------|---------|----------|------------|
| Terminology Authority Conflict | Non-canonical C-RSP expansion in a truth surface | Critical | Halt; fix wording |
| Taxonomy drift | Domain X in constitution but not in inventory | Critical | Reconcile before Frozen |
| Profile drift | `config/*.ts` contradicts `MASTER_PROJECT_INVENTORY.json` | Critical | Halt |
| Incomplete instance | Missing §§7–17 or failed structural verify | Critical | Halt |
| Evidence gap | Frozen claimed without AC-07 outcome | High | Block promotion |
| Verifier failure | Non-zero governance or topology exit | Critical | Halt per §6B |
| Cross-repo drift | `projects/consentchain` role-registry out of sync | High | Sync per `openmemory.md` / README workflow |

---
## 13. Halt Matrix

Halt if: placeholders remain in executable sections; taxonomy layers inconsistent across the three surfaces; `verify_crsp_structure` FAIL; `verify_governance_chain` or `verify_project_topology --with-governance` non-zero; `verify_cross_repo_consistency` fails when required for the branch; illegal lifecycle transition; preflight commands not run; evidence paths missing; contradiction with **INVARIANT_SEM_01–04**.

---
## 14. Preflight

Preflight verifies: section completeness §§0–17; canonical terminology; TLC-Core topology; **core-verifier** class; instance path matches this file; acceptance criteria table complete; risk/control present; no unresolved `[REQUIRED]` in this instance.

**Preflight command(s):**

```bash
mkdir -p verification/c-rsp-structure
python3 scripts/verify_crsp_structure.py \
  --template projects/c-rsp/BUILD_CONTRACT.md \
  --instance projects/c-rsp/BUILD_CONTRACTS/CRSP-A1-TAXONOMY-CANONICALIZATION-001.md \
  --report verification/c-rsp-structure/structural-a1-taxonomy.json
```

Post-edit verification (after truth-surface work, not required for Draft→Active structural gate alone):

```bash
python3 scripts/verify_governance_chain.py --root .
python3 scripts/verify_project_topology.py --root . --with-governance
python3 scripts/verify_cross_repo_consistency.py --canonical-root . --target-root projects/consentchain
```

---
## 15. Adoption Tiers

### Tier 1 — Minimum Viable Governance

Identity block; TLC-Core topology; canonical C-RSP terminology; placeholder-free instance; schema-disciplined sections §§0–17.

### Tier 2 — Operational

Tier 1 plus: acceptance criteria (§9); risk/control (§5); rollback (§10); CI verifiers listed; lifecycle evidence.

### Tier 3 — Constitutional

Tier 2 plus: full §8 invariant binding; evidence + conflict/halt matrices; audit-grade promotion; governance lock path referenced (`projects/c-rsp/governance-template.lock.json` on promotion as repo standard).

**This instance:** Tier-3-Constitutional.

---
## 16. Output Format

**Mandatory report shape:** `projects/c-rsp/CRSP_OUTCOME_TEMPLATE.md` — **Title block first**, then Kanban, constitutional anchor, then **§2 V&T Statement** with **CONTROL_RULE_KBC_01** and **CONTROL_RULE_VT_RIGOR_01** honored in the saved executed copy.

**V&T constitutional basis:** Article I — Right to Truth; Article III — Verification Before Done (`governance/constitution/core/articles.md`).

---
## 17. Instance Declaration

Executable A-1 scope is **only** this path: `projects/c-rsp/BUILD_CONTRACTS/CRSP-A1-TAXONOMY-CANONICALIZATION-001.md`. **Status** remains **Draft** until structural preflight (§14) PASS and human/agent promotion to **Active**; do not cite `BUILD_CONTRACT.instance.md` as the executed contract. After successful execution and AC closure, set **Status** to **Frozen** in a follow-on revision or successor record per lifecycle rules.
