# C-RSP Guided Instance Template
## Constitutionally-Regulated Single Pass Executable Prompt

## Artifact Role

This file is the **guided instance template** for C-RSP contract drafting.

- It is **not** the canonical master template.
- It is **subordinate** to `projects/c-rsp/BUILD_CONTRACT.md`, which alone defines reusable canonical structure, invariants, and authority order (see **Canonical Artifact Role** there).
- It must **compile down to** the section order, titles, and semantic rules of the canonical master template.
- If this file conflicts with the canonical master template, **the master template controls**.
- **INVARIANT_SEM_02:** This path is explicitly the guided instance template; it must not be treated as the highest-authority reusable C-RSP source.

> **Artifact role (operational):** Guided prompt skeleton only. This file is **not** an executed contract, contains **no** executed-state claims, and must **not** be cited as the active Tier-2+ execution scope for **CONTROL_RULE_KBC_01**. Copy to a new path under `projects/<slug>/BUILD_CONTRACT.md`, `projects/<slug>/BUILD_CONTRACT`, or `projects/c-rsp/instances/<CONTRACT_ID>.md`, replace every `{TOKEN}` / `[REQUIRED]` with concrete values, then run schema/preflight checks before execution claims.

> **Canonical master template:** `projects/c-rsp/BUILD_CONTRACT.md`  
> **Outcome report shape:** `projects/c-rsp/CRSP_OUTCOME_TEMPLATE.md`  
> **Schema:** `projects/c-rsp/contract-schema.json`

---
## 0. Instance Governance

- **Artifact class:** Guided instance template (workflow only).
- **Canonical expansion:** `C-RSP` = **Constitutionally-Regulated Single Pass** only (**INVARIANT_TERM_01**).
- **Authoring rule:** Fill placeholders; remove this callout box in the **saved executed copy**.
- **Schema authority:** Section order and titles must remain aligned with `contract-schema.json` (`core_sections`).

---
## 1. Contract Identity

- **Contract Title:** {Exact task title}
- **Contract ID:** {REQUIRED — stable id, e.g. CRSP-…}
- **Version:** {semver}
- **Schema Version:** {match contract-schema.json `schema_version` or overlay note}
- **Status:** Draft | Active | Frozen | Superseded
- **Adoption Tier:** Tier-1-MVG | Tier-2-Operational | Tier-3-Constitutional
- **System Role:** {one sentence}
- **Primary Objective:** {one exact sentence}
- **Scope Boundary:** {exact files / surfaces}
- **Not Claimed:** {explicit exclusions}

---
## 2. Contract Topology + Profile

- **Topology Mode:** TLC-Core | Satellite | Dual-Topology
- **Profile Type:** Core | Satellite | Integrated Component | Standalone Application | Dual-Topology
- **Profile Overlay Source:** {path or N/A}
- **Verifier Class:** core-verifier | satellite-verifier | dual-topology-verifier
- **Authoritative Truth Surface:** {exact file list}
- **Instance Artifact Path:** {path to **this executed file** after save — not this template path}
- **Governance Lock Path:** `governance-template.lock.json` or N/A

### 2A. Profile Merge Rule

{Reference master `BUILD_CONTRACT.md` §2A; specialization limits only.}

### 2B. Instance Rule

{Instantiation completeness per master §2B.}

---
## 3. Baseline State

- **Existing Repo / System:** {REQUIRED}
- **Baseline Commit / Anchor:** {REQUIRED}
- **Verified Existing Assets:** {REQUIRED}
- **Known Constraints:** {REQUIRED}
- **Known Gaps:** {REQUIRED}
- **Legacy Migration Context:** {REQUIRED or N/A}

---
## 4. Dependencies and Inputs

- **Required Inputs:** {REQUIRED}
- **External Dependencies:** {REQUIRED}
- **Governance Dependencies:** {REQUIRED}
- **Forbidden Assumptions:** {REQUIRED}

### 4A. Cross-Repo Governance Dependency Graph

- **Parent Constitutional Source:** {REQUIRED}
- **Shared Overlay Profiles:** {REQUIRED or none}
- **Dual-Topology Linked Repos:** {REQUIRED or none}
- **Satellite Dependents:** {REQUIRED or none}
- **Drift Detection Scope:** {REQUIRED}

---
## 5. Risk + Control Classification

- **Risk Class:** Low | Moderate | High | Critical
- **Side-Effect Class:** None | Internal | External | Destructive | Regulated
- **External Action Scope:** {REQUIRED}
- **Stop/Override Required:** Yes | No
- **Recovery Mode:** Manual | Assisted | Automated | N/A

### 5A. Conditional Stop / Override Rule

{Per master §5A when triggers apply.}

---
## 6. Execution Model

- **Execution Mode:** Single-pass deterministic build contract
- **Decision Closure Rule:** No open-ended branch points inside executable sections
- **Fallback Rule:** Unresolved ambiguity triggers halt or explicit escalation
- **Generated Artifacts:** {REQUIRED — list concrete paths}
- **Promotion Target:** {REQUIRED or N/A}

### 6A. Ordered Operations (Blind Man Test)

| **Step ID** | **Actor** | **Action** | **Inputs** | **Outputs** | **Verify** | **If Failure** |
|-------------|-----------|------------|------------|-------------|------------|----------------|
| OP-01 | human \| agent \| CI \| verifier | {exact command or file op} | {paths} | {paths / output} | {command / inspection} | {halt / rollback} |

{Add rows OP-02… as needed.}

### 6B. Halt Conditions (instance-local)

| **Condition** | **Stop Reason** | **Next Action** |
|---------------|-----------------|-----------------|
| {failure state} | {reason} | {recovery} |

### 6C. Success Conditions

- **Success:** {observable pass condition}
- **Done:** {closure definition}

### 6D. Major Component Implementation Snippets

{Per master §6D — or state `N/A` with one-line justification for governance-only work.}

### 6E. Dual-Topology Rule

{If Dual-Topology: integrated vs standalone paths; else `N/A`.}

---
## 7. Lifecycle State Machine

### Allowed States

{Draft; Active; Frozen; Superseded}

### Transition Rules

{Per master §7}

### Transition Evidence

{Per master §7}

---
## 8. Invariants

### Required Global Invariants

{List INVARIANT_TERM_01 … INVARIANT_REC_01 as applicable}

### Profile Invariants

{Profile-specific}

---
## 9. Acceptance Criteria

| ID | Requirement | Verification Method | Pass Condition |
|----|-------------|---------------------|----------------|
| AC-01 | {REQUIRED} | {REQUIRED} | {REQUIRED} |

---
## 10. Rollback & Recovery

- **Safe-State Definition:** {REQUIRED for Tier-2+}
- **Rollback Procedure:** {REQUIRED for Tier-2+}
- **Recovery Authority:** {REQUIRED for Tier-2+}
- **Rollback Evidence Paths:** {REQUIRED for Tier-2+}
- **Partial Execution Handling:** {REQUIRED}

---
## 11. Evidence + Truth Surface

- **Primary Evidence Paths:** {REQUIRED}
- **Generated Reports:** {REQUIRED}
- **Audit Artifacts:** {REQUIRED}
- **Evidence Boundary:** {REQUIRED}

---
## 12. Conflict Matrix

| Conflict Type | Example | Severity | Resolution |
|---------------|---------|----------|------------|
| {row} | {example} | {Critical|High|…} | {Halt|…} |

---
## 13. Halt Matrix

{Instance-specific halt bullets; align with §6B and master §13.}

---
## 14. Preflight

{Checklist per master §14}

**Preflight Command(s):** {REQUIRED — exact commands or `UNRESOLVED REQUIRED INPUT`}

---
## 15. Adoption Tiers

{Tier alignment per master §15}

---
## 16. Output Format

Mandatory report shape: `projects/c-rsp/CRSP_OUTCOME_TEMPLATE.md` — cite **CONTROL_RULE_KBC_01** in the **saved executed** file path, not in this guided stub.

---
## 17. Instance Declaration

After filling this template, save as a **new** executed contract path; remove unresolved `{…}` / `[REQUIRED]` tokens; then declare promotion state only when preflight + evidence support it.
