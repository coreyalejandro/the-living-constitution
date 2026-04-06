# BUILD CONTRACT INSTANCE
## Constitutionally-Regulated Single Pass Executable Prompt

> **Artifact role:** **Generator/template helper** — structural scaffold for producing instances. **Not** `projects/c-rsp/BUILD_CONTRACT.md` (canonical master), **not** `BUILD_CONTRACT.instance.md` (guided instance template). Subordinate to the master template.
>
> **Instance Status:** Executable only when every `[REQUIRED]` is resolved, schema validation passes, preflight passes, and topology matches verifier class per `contract-schema.json`.

---
## 0. Instance Governance (maps to schema: template_governance)

- **Artifact Class:** Executable contract instance (not the constitutional framework template).
- **Canonical Expansion:** `C-RSP` = Constitutionally-Regulated Single Pass only; any other expansion invalidates the instance.
- **Schema Authority:** `contract-schema.json` defines immutable core section order and titles; this file must remain conformant.
- **Profile Merge:** Overlay content may only specialize declared customization zones; it may not contradict base halt, terminology, or core section order (see master `BUILD_CONTRACT.md` §2A).

---
## 1. Contract Identity

- **Contract Title:** [REQUIRED]
- **Contract ID:** [REQUIRED]
- **Version:** [REQUIRED]
- **Schema Version:** [REQUIRED]
- **Status:** Draft | Active | Frozen | Superseded
- **Adoption Tier:** Tier-1-MVG | Tier-2-Operational | Tier-3-Constitutional
- **System Role:** [REQUIRED]
- **Primary Objective:** [REQUIRED]
- **Scope Boundary:** [REQUIRED]
- **Not Claimed:** [REQUIRED]

---
## 2. Contract Topology + Profile

- **Topology Mode:** [REQUIRED]
- **Profile Type:** [REQUIRED]
- **Profile Overlay Source:** [REQUIRED]
- **Verifier Class:** [REQUIRED]
- **Authoritative Truth Surface:** [REQUIRED]
- **Instance Artifact Path:** [this file]
- **Governance Lock Path:** `governance-template.lock.json`

---
## 3. Baseline State

- **Existing Repo / System:** [REQUIRED]
- **Baseline Commit / Anchor:** [REQUIRED]
- **Verified Existing Assets:** [REQUIRED]
- **Known Constraints:** [REQUIRED]
- **Known Gaps:** [REQUIRED]
- **Legacy Migration Context:** [REQUIRED or N/A]

---
## 4. Dependencies and Inputs

- **Required Inputs:** [REQUIRED]
- **External Dependencies:** [REQUIRED]
- **Governance Dependencies:** [REQUIRED]
- **Forbidden Assumptions:** [REQUIRED]

### 4A. Cross-Repo Governance Dependency Graph

- **Parent Constitutional Source:** [REQUIRED]
- **Shared Overlay Profiles:** [REQUIRED or none]
- **Dual-Topology Linked Repos:** [REQUIRED or none]
- **Satellite Dependents:** [REQUIRED or none]
- **Drift Detection Scope:** [REQUIRED]

---
## 5. Risk + Control Classification

- **Risk Class:** [REQUIRED]
- **Side-Effect Class:** [REQUIRED]
- **External Action Scope:** [REQUIRED]
- **Stop/Override Required:** [REQUIRED]
- **Recovery Mode:** [REQUIRED]

### 5A. Conditional Stop / Override Rule

If `Risk Class` is High or Critical, or `Side-Effect Class` is External, Destructive, or Regulated, then stop/override semantics, safe-state definition, and rollback/recovery must be fully specified or promotion is blocked.

---
## 6. Execution Model

- **Execution Mode:** Single-pass deterministic build contract
- **Decision Closure Rule:** No open-ended branch points inside executable sections
- **Fallback Rule:** Any unresolved ambiguity triggers halt or explicit escalation
- **Generated Artifacts:** [REQUIRED]
- **Promotion Target:** [REQUIRED]

### 6A. Dual-Topology Rule

If `Topology Mode = Dual-Topology`, declare both internal and standalone paths explicitly.

---
## 7. Lifecycle State Machine

- **Current State:** Draft | Active | Frozen | Superseded
- **Target State:** [REQUIRED]
- **Transition Guard Conditions:** [REQUIRED]
- **Transition Evidence Paths:** [REQUIRED]

Allowed transitions (invalid transitions halt): `Draft → Active → Frozen → Superseded`. Each transition must emit or update a lifecycle record and link to verifier/preflight evidence on the truth surface.

---
## 8. Invariants

- **INVARIANT_TERM_01**
- **INVARIANT_SCHEMA_01**
- **INVARIANT_EXEC_01**
- **INVARIANT_EXEC_02**
- **INVARIANT_EXEC_03**
- **INVARIANT_EXEC_04**
- **INVARIANT_EXEC_05**
- **INVARIANT_CTRL_01**
- **INVARIANT_LIFE_01**
- **INVARIANT_REC_01**
- [profile-specific invariants]

---
## 9. Acceptance Criteria

| ID | Requirement | Verification Method | Pass Condition |
|---|---|---|---|
| AC-01 | [REQUIRED] | [REQUIRED] | [REQUIRED] |
| AC-02 | [REQUIRED] | [REQUIRED] | [REQUIRED] |
| AC-03 | [REQUIRED] | [REQUIRED] | [REQUIRED] |

---
## 10. Rollback & Recovery

- **Safe-State Definition:** [REQUIRED or N/A by tier]
- **Rollback Procedure:** [REQUIRED or N/A by tier]
- **Recovery Authority:** [REQUIRED or N/A by tier]
- **Rollback Evidence Paths:** [REQUIRED or N/A by tier]
- **Partial Execution Handling:** [REQUIRED]

---
## 11. Evidence + Truth Surface

- **Primary Evidence Paths:** [REQUIRED]
- **Generated Reports:** [REQUIRED]
- **Audit Artifacts:** [REQUIRED]
- **Evidence Boundary:** [REQUIRED]
- **Truth Discipline:** Contract claims must not exceed evidence declared in the truth surface.

---
## 12. Conflict Matrix

| Conflict Type | Example | Severity | Resolution |
|---|---|---|---|
| [REQUIRED] | [REQUIRED] | [REQUIRED] | [REQUIRED] |

---
## 13. Halt Matrix

- [REQUIRED]
- [REQUIRED]
- [REQUIRED]

---
## 14. Preflight

**Commands:**

```bash
[REQUIRED]
```

Preflight must verify:

- no unresolved placeholders
- correct profile overlay
- correct topology mode
- correct verifier class
- evidence paths declared
- acceptance criteria complete
- schema validation pass
- risk/control block complete
- lifecycle transition valid

---
## 15. Adoption Tiers

- **Tier-1-MVG:** identity + topology + schema-valid instance + no placeholders
- **Tier-2-Operational:** Tier-1 + acceptance criteria + risk/control + rollback/recovery + lifecycle evidence
- **Tier-3-Constitutional:** Tier-2 + invariant registry + lock manifest + dependency graph + audit-grade evidence

---
## 16. Output Format

Every execution summary must end with:

- **Exists**
- **Non-existent**
- **Unverified**
- **Functional status**

No stronger claim may be made outside that truth surface.

---
## 17. Instance Declaration

This file is the authoritative executable instance for the governed run. It supersedes ad hoc merge of the constitutional master template and any overlay profile. The lock manifest (`governance-template.lock.json`) must reference the same base template, profile, schema, and verifier class as declared in this instance.
