# 📜 C-RSP Build Contract Template
## Constitutionally-Regulated Single Pass Executable Prompt (Framework)

> **Template Status:** Framework template only. Not executable until instantiated with all required fields, profile overlays, acceptance criteria, schema validation, and lifecycle controls.

---
## 0. Template Governance

- **Template Class:** Constitutional master template
- **Canonical Expansion:** Constitutionally-Regulated Single Pass
- **Invalidation Rule:** Any alternate expansion of C-RSP is governance drift and invalidates the contract instance.
- **Instance Requirement:** This template is not executable by itself. Every run must produce or reference an instantiated contract artifact.
- **Schema Authority:** `contract-schema.json` is the canonical machine-readable definition of contract shape.

### Global Constitutional Invariants

- **INVARIANT_TERM_01:** The canonical expansion of `C-RSP` must be exactly `Constitutionally-Regulated Single Pass`.
- **INVARIANT_SCHEMA_01:** Every executable instance must preserve the exact canonical section order, IDs, titles, and required fields defined by the contract schema.
- **INVARIANT_EXEC_01:** No unresolved placeholders may remain in an executable instance.
- **INVARIANT_EXEC_02:** Acceptance criteria must be concrete, objective, and testable.
- **INVARIANT_EXEC_03:** Preflight must pass before promotion.
- **INVARIANT_EXEC_04:** Topology mode and verifier class must be consistent.
- **INVARIANT_EXEC_05:** Authoritative truth surface must be declared.
- **INVARIANT_CTRL_01:** Any contract class capable of high-impact side effects, external execution, destructive mutation, identity/policy changes, or regulated enforcement must define explicit stop/override controls, authority to invoke them, safe-state behavior, and recovery procedure.
- **INVARIANT_LIFE_01:** Contract state transitions must follow the allowed state machine and emit evidence-bearing transition events.
- **INVARIANT_REC_01:** Tier-2+ contracts must define rollback and recovery semantics sufficient to return the governed system to a declared safe state after interruption or halt.

### Global Halt Conditions

The contract must halt if any of the following occur:

1. non-canonical C-RSP terminology is detected
2. schema shape differs from the canonical schema
3. unresolved placeholders remain in an executable instance
4. topology mode is undeclared or contradictory
5. verifier class and topology mode do not align
6. required acceptance criteria are absent
7. preflight fails
8. required truth surface is missing
9. required stop/override semantics are absent for an applicable risk class
10. illegal lifecycle transition is attempted
11. required rollback semantics are absent for Tier-2+

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

- **Topology Mode:** TLC-Core | Satellite | Dual-Topology
- **Profile Type:** Core | Satellite | Integrated Component | Standalone Application | Dual-Topology
- **Profile Overlay Source:** [path or N/A]
- **Verifier Class:** core-verifier | satellite-verifier | dual-topology-verifier
- **Authoritative Truth Surface:** [exact files]
- **Instance Artifact Path:** [REQUIRED]
- **Governance Lock Path:** `governance-template.lock.json`

### 2A. Profile Merge Rule

The base constitutional template governs all contract instances. Overlay profiles may specialize only the following:

- required file inventories
- verifier scope
- topology-specific promotion rules
- CI workflow requirements
- component-specific evidence requirements
- bounded customization blocks inside approved schema slots
- domain-specific payload inside customization zones

Overlay profiles may **not** override:

- canonical C-RSP terminology
- contract invalidation rules
- conflict severity classes
- acceptance criteria requirement
- preflight requirement
- truth-discipline requirement
- halt matrix semantics
- core section order, names, or IDs

### 2B. Instance Rule

A contract is executable only when all of the following exist:

1. base template fields are fully instantiated
2. referenced overlay profile fields are fully instantiated
3. unresolved placeholders are absent
4. acceptance criteria are concrete
5. generated artifacts and evidence paths are declared
6. preflight passes
7. schema validation passes
8. lifecycle state transition guards are satisfied

If any of the above are missing, the contract is invalid.

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
- **Dependency Policy:** All dependencies must be explicitly named; implicit dependency assumptions are invalid.

### 4A. Cross-Repo Governance Dependency Graph

Every Tier-2+ contract must declare linked governance relationships:

- **Parent Constitutional Source:** [REQUIRED]
- **Shared Overlay Profiles:** [REQUIRED or none]
- **Dual-Topology Linked Repos:** [REQUIRED or none]
- **Satellite Dependents:** [REQUIRED or none]
- **Drift Detection Scope:** [REQUIRED]

---
## 5. Risk + Control Classification

- **Risk Class:** Low | Moderate | High | Critical
- **Side-Effect Class:** None | Internal | External | Destructive | Regulated
- **External Action Scope:** [REQUIRED]
- **Stop/Override Required:** Yes | No
- **Recovery Mode:** Manual | Assisted | Automated | N/A

### 5A. Conditional Stop / Override Rule

If `Risk Class ∈ {High, Critical}` or `Side-Effect Class ∈ {External, Destructive, Regulated}`, then:

- stop/override semantics are mandatory
- a safe-state definition is mandatory
- a rollback/recovery section is mandatory
- failure to define them blocks promotion

---
## 6. Execution Model

- **Execution Mode:** Single-pass deterministic build contract
- **Decision Closure Rule:** No open-ended branch points inside executable sections
- **Fallback Rule:** Any unresolved ambiguity triggers halt or explicit escalation
- **Generated Artifacts:** [REQUIRED]
- **Promotion Target:** [REQUIRED]

### 6A. Dual-Topology Rule

If `Topology Mode = Dual-Topology`, the contract must define both paths explicitly:

- integrated/internal path
- standalone/external path

No change is complete unless:

1. both paths are updated, or
2. the contract explicitly records why one path is intentionally out of scope

---
## 7. Lifecycle State Machine

### Allowed States

- **Draft**
- **Active**
- **Frozen**
- **Superseded**

### Transition Rules

- `Draft → Active` requires: no placeholders, schema validation pass, preflight pass, required fields complete
- `Active → Frozen` requires: acceptance criteria satisfied, evidence recorded, promotion rules satisfied
- `Frozen → Superseded` requires: successor instance exists and references the superseded contract
- any invalid transition halts and records an audit event

### Transition Evidence

Each transition must emit or update:

- lifecycle transition record
- associated verifier/preflight report
- evidence links to the truth surface

---
## 8. Invariants

### Required Global Invariants

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

### Profile Invariants

[REQUIRED: profile-specific invariants inserted here]

---
## 9. Acceptance Criteria

| ID | Requirement | Verification Method | Pass Condition |
|---|---|---|---|
| AC-01 | [REQUIRED] | [REQUIRED] | [REQUIRED] |
| AC-02 | [REQUIRED] | [REQUIRED] | [REQUIRED] |
| AC-03 | [REQUIRED] | [REQUIRED] | [REQUIRED] |

All acceptance criteria must be executable, objective, and mapped to evidence.

---
## 10. Rollback & Recovery

- **Safe-State Definition:** [REQUIRED for Tier-2+; otherwise N/A]
- **Rollback Procedure:** [REQUIRED for Tier-2+; otherwise N/A]
- **Recovery Authority:** [REQUIRED for Tier-2+; otherwise N/A]
- **Rollback Evidence Paths:** [REQUIRED for Tier-2+; otherwise N/A]
- **Partial Execution Handling:** [REQUIRED]

---
## 11. Evidence + Truth Surface

- **Primary Evidence Paths:** [REQUIRED]
- **Generated Reports:** [REQUIRED]
- **Audit Artifacts:** [REQUIRED]
- **Evidence Boundary:** [REQUIRED]
- **Truth Discipline:** Claims in the contract may not exceed evidence declared in the truth surface.

---
## 12. Conflict Matrix

| Conflict Type | Example | Severity | Resolution |
|---|---|---|---|
| Terminology Authority Conflict | Non-canonical C-RSP expansion | Critical | Halt |
| Profile Drift Conflict | Overlay contradicts base constitutional rules | Critical | Halt |
| Topology Misclassification | Satellite treated as TLC-Core or vice versa | Critical | Halt |
| Incomplete Instance Conflict | Missing required instance fields | Critical | Halt |
| Evidence Gap Conflict | Claim not anchored to evidence path | High | Block promotion |
| Verifier Scope Conflict | Wrong verifier class for topology | High | Block promotion |
| Schema Drift Conflict | Core section shape differs from schema | Critical | Halt |
| Lifecycle Conflict | Illegal state transition | High | Block promotion |
| Recovery Conflict | Required rollback semantics missing | High | Block promotion |

---
## 13. Halt Matrix

The contract must halt if any of the following occur:

- unresolved placeholders remain
- profile overlay is missing but referenced
- topology mode is undeclared or contradictory
- canonical terminology drift is detected
- verifier class and topology mode do not align
- required acceptance criteria are absent
- preflight fails
- required truth surface is missing
- schema validation fails
- illegal lifecycle transition is attempted
- required rollback semantics are absent for Tier-2+

---
## 14. Preflight

Preflight must verify at minimum:

- no unresolved placeholders
- canonical terminology only
- topology mode present
- profile type present
- verifier class present
- instance artifact exists
- required evidence paths exist or are creatable
- acceptance criteria table is complete
- schema validation passes
- lifecycle declaration is valid
- risk/control block is present

**Preflight Command(s):** [REQUIRED]

---
## 15. Adoption Tiers

### Tier 1 — Minimum Viable Governance
Requires:
- identity block
- topology selection
- canonical terminology
- placeholder-free instance artifact
- schema-valid structure

### Tier 2 — Operational
Requires Tier 1 plus:
- acceptance criteria
- risk/control classification
- CI verifier integration
- rollback/recovery semantics
- lifecycle transition evidence

### Tier 3 — Constitutional
Requires Tier 2 plus:
- full invariant registry
- dual-topology support where applicable
- governance lockfiles
- evidence ledger and dependency graph
- audit-grade promotion evidence

---
## 16. Output Format

**Mandatory report shape:** Use `projects/c-rsp/CRSP_OUTCOME_TEMPLATE.md` — **Kanban board first**, then constitutional anchor, then **V&T Statement** (no long prose before the board).

**V&T constitutional basis:**

- **Article I — Right to Truth** (`00-constitution/articles.md`): evidence-bound claims; the V&T block enforces this.
- **Article III — Verification Before Done** (`00-constitution/articles.md`): completion requires proof against acceptance criteria.

All execution summaries must end with:

- **Exists**
- **Verified against** (when claims reference artifacts/commits)
- **Not claimed**
- **Non-existent**
- **Unverified**
- **Functional status**

No stronger claim may be made outside that truth surface.

**Follow-on C-RSP build:** When the Kanban **What’s next** column implies another contract run, record it in `projects/c-rsp/NEXT_CRSP_BUILD.json` (`status: pending`) and run `./scripts/crsp_next_build.sh` to surface the auto-launch instruction for the next session (Section 16 + template must stay aligned).

---
## 17. Instance Declaration

This framework becomes executable only through a fully instantiated contract document, typically:

`BUILD_CONTRACT.instance.md`
