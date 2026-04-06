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
- **Version:** 0.1.0
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
- **Known Constraints:** Taxonomy must stay consistent with `00-constitution/invariant-registry.json` and role separation of powers.
- **Known Gaps:** Draft — domain registry shape and Article VI text must be finalized in execution.
- **Legacy Migration Context:** N/A

---
## 4. Dependencies and Inputs

- **Required Inputs:** Master plan §A-1 (Files to Modify / Read); `projects/c-rsp/README.md`; `CANONICAL_ROLE_MAP.md`; `BUILD_CONTRACT.md`; `contract-schema.json` — **Dependencies**
- **External Dependencies:** none
- **Governance Dependencies:** `00-constitution/invariant-registry.json`, `00-constitution/role-registry.json`, `00-constitution/doctrine-to-invariant.map.json`
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

### 6B. Halt Conditions (instance-local)

| **Condition** | **Stop Reason** | **Next Action** |
|---------------|-----------------|-----------------|
| Any surface contradicts another on canonical domain | Drift | Reconcile before continuing |
| Verifier non-zero | Evidence failure | Fix and re-run |

### 6C. Success Conditions

- **Success:** `verify_governance_chain.py` and `verify_project_topology.py --with-governance` exit 0; three surfaces agree on taxonomy layers.
- **Done:** A-1 outcome artifact exists; status → Frozen per lifecycle.

### 6D. Major Component Implementation Snippets

**N/A** — governance prose and registry edits; no material code-bearing component in the sense of §6D unless config TS counts; then add per-component blocks when implementing.

### 6E. Dual-Topology Rule

N/A — TLC-Core only.

---
## 7–17. Lifecycle, Invariants, Acceptance, Rollback, Evidence, Matrices, Preflight, Tiers, Output, Declaration

**Acceptance criteria (minimum):** Align with `plans/master-plan.md` §Verification (A-1): governance chain 0, topology 0, three surfaces + taxonomy parity.

**Output format:** `projects/c-rsp/CRSP_OUTCOME_TEMPLATE.md` — cite **CONTROL_RULE_KBC_01** in the saved executed copy.

**Instance Declaration:** This Draft must be completed (no placeholders), preflight-valid, and moved to **Active** before execution claims. **Do not** cite `BUILD_CONTRACT.instance.md` as the executed scope — cite **this path** after save.

---

**End of Draft instance** — expand §7–§15 fully before Tier-3 promotion, or merge content from `BUILD_CONTRACT.instance.md` sections as you instantiate.
