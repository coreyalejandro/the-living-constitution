# BUILD CONTRACT INSTANCE
## Constitutionally-Regulated Single Pass Executable Prompt

- **Contract Title:** [REQUIRED]
- **Contract ID:** [REQUIRED]
- **Version:** [REQUIRED]
- **Schema Version:** [REQUIRED]
- **Status:** Draft | Active | Frozen | Superseded
- **Adoption Tier:** [REQUIRED]

---
## 1. Identity

- **System Role:** [REQUIRED]
- **Primary Objective:** [REQUIRED]
- **Scope Boundary:** [REQUIRED]
- **Not Claimed:** [REQUIRED]

---
## 2. Topology + Profile

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
