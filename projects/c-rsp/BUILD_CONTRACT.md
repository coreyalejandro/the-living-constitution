# 📜 C-RSP Build Contract Template
## Constitutionally-Regulated Single Pass Executable Prompt (Framework)

> **Template Status:** Framework template only. Not executable until instantiated with all required fields, profile overlays, acceptance criteria, schema validation, and lifecycle controls.

---
## 0. Template Governance

- **Template Class:** Constitutional **canonical master template** (this file: `projects/c-rsp/BUILD_CONTRACT.md`)
- **Canonical Expansion:** Constitutionally-Regulated Single Pass
- **Invalidation Rule:** Any alternate expansion of C-RSP is governance drift and invalidates the contract instance.
- **Instance Requirement:** This template is not executable by itself. Every run must produce or reference an instantiated contract artifact (see **Artifact class map** below).
- **Schema Authority:** `contract-schema.json` is the canonical machine-readable definition of contract shape.

### Artifact class map (non-overlapping roles)

| Class | Definition | Examples in TLC |
|-------|------------|-----------------|
| **Constitutional truth surfaces** | Repo-wide status, inventory, constitution, and rendered mirrors that state what is true now | `README.md`, `STATUS.json`, `STATUS.md`, `THE_LIVING_CONSTITUTION.md`, root `CLAUDE.md`, `MASTER_PROJECT_INVENTORY.json`, `MASTER_PROJECT_INVENTORY.md`, `plans/master-plan.md` |
| **Canonical template artifacts** | Reusable structure and invariants; not executed state | `projects/c-rsp/BUILD_CONTRACT.md` (this file), `projects/c-rsp/contract-schema.json`, `projects/c-rsp/CRSP_OUTCOME_TEMPLATE.md` |
| **Workflow / router artifacts** | Prompt skeletons and pointers; no executed outcomes | `projects/c-rsp/BUILD_CONTRACT.instance.md` (**guided instance template** — placeholders only) |
| **Executed project contracts** | Fully or partially instantiated contracts for a concrete scope | `projects/*/BUILD_CONTRACT.md`, `projects/*/BUILD_CONTRACT`, `projects/c-rsp/instances/*.md` (named Tier-3 instances), other `BUILD_CONTRACT*.md` under `projects/` as authored |

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

**Canonical role:** Every **executable** C-RSP instance (Tier-1+ when claiming execution) must implement **Blind Man structural discipline** below. Global **Section 13 Halt Matrix** remains authoritative for halt classes; Sections **6B–6C** are the **instance-local** required articulation of halt, success, and ordered work for **this** contract. **Guided authoring surface** (`projects/c-rsp/BUILD_CONTRACT.instance.md`) is not an executed contract; it is a prompt skeleton only.

- **Execution Mode:** Single-pass deterministic build contract
- **Decision Closure Rule:** No open-ended branch points inside executable sections
- **Fallback Rule:** Any unresolved ambiguity triggers halt or explicit escalation
- **Generated Artifacts:** [REQUIRED]
- **Promotion Target:** [REQUIRED]

### 6A. Ordered Operations (Blind Man Test — mandatory for executable instances)

Every executable instance must define at least one ordered step. Use this table shape (repeat rows per step):

| **Step ID** | **Actor** | **Action** | **Inputs** | **Outputs** | **Verify** | **If Failure** |
|-------------|-----------|------------|------------|-------------|------------|----------------|
| OP-01 | human \| agent \| CI \| verifier | Exact command or exact file operation | Exact path(s) or artifact id(s) | Exact path(s), artifact(s), or observable console output | Exact command, diff, test, or inspection | Halt, rollback, or escalation action |

- **OP-ID discipline:** Step IDs must be **stable** within the contract revision (OP-01..OP-n); subordinate checks may use `OP-01a` only when the parent step explicitly declares them.

### 6B. Halt Conditions (instance-local)

| **Condition** | **Stop Reason** | **Next Action** |
|---------------|-----------------|-----------------|
| [exact failure state] | [why execution must stop] | [recovery / escalation] |

Executable instances must name at least **one** halt row that is **specific** to this contract (not generic prose alone). Cross-reference **Section 13 (Halt Matrix)** for global halt classes.

### 6C. Success Conditions

- **Success:** [objectively observable pass condition — e.g. verifier exit 0, evidence file updated, AC row satisfied]
- **Done:** [definition of contract-local closure — e.g. Kanban clear for this scope or formal halt recorded]

### 6D. Major Component Implementation Snippets

For **Build / Fix / Refactor** work that **materially changes** code-bearing components, each affected component must declare:

```markdown
#### Component: {NAME}
- **Path:** {EXACT_PATH}
- **Role:** {one sentence}
- **Interface Contract:** {inputs/outputs}
- **Snippet:** real code or structural stub
- **Verification:** {exact command or inspection}
- **Failure Signature:** {how breakage surfaces}
```

If a contract is **Governance / Discovery** only with **no** material code change, **explicitly** state `Major component snippets: N/A — one line justification` in the execution model or acceptance criteria.

### 6E. Dual-Topology Rule

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

**Mandatory report shape:** Use `projects/c-rsp/CRSP_OUTCOME_TEMPLATE.md` — **Title block first** (`# C-RSP Build Contract : {BUILD_CONTRACT_TITLE} — {COMPONENT}` + subtitle `Constitutionally-Regulated Single Pass Executable Prompt (Framework)`), then **§1 Constitutional anchor**, then **§2 V&T Statement**.

**CONTROL_RULE_KBC_01 (normative for all Tier-2+ instances; cite in the active **executed** contract file — e.g. `projects/<slug>/BUILD_CONTRACT.md`, `projects/<slug>/BUILD_CONTRACT`, or `projects/c-rsp/instances/<CONTRACT_ID>.md` — not in the guided template `projects/c-rsp/BUILD_CONTRACT.instance.md`):**

1. **Single active BUILD_CONTRACT:** At most one BUILD_CONTRACT instance is the **active execution scope** at a time until that contract is **clear** (all in-scope acceptance criteria for that instance are satisfied by evidence, or a **formal halt** is recorded in the instance halt matrix).
2. **Kanban-first V&T:** Inside **§2 V&T Statement**, the **Visual board (Kanban)** subsection MUST appear **first**, before **Exists**, **Verified against**, **Not claimed**, **Non-existent**, **Unverified**, or **Functional status**. No long prose before the board; no truth line above the board.
3. **No terminal “done” while the board is open:** If the Kanban still places required work for **this** contract in **BACKLOG**, **IN PROGRESS**, or **BLOCKED**, the run MUST NOT be treated as complete and MUST NOT stop as if the build were finished—continue until the board is clear for this contract, or record a **formal halt** with evidence. (Follow-on work that is a **different** BUILD_CONTRACT is queued only after the current contract is clear; then use **What’s next** + `NEXT_CRSP_BUILD.json` as below.)

**V&T constitutional basis:**

- **Article I — Right to Truth** (`00-constitution/articles.md`): evidence-bound claims; the V&T block enforces this.
- **Article III — Verification Before Done** (`00-constitution/articles.md`): completion requires proof against acceptance criteria.

All execution summaries must close **§2 V&T Statement** with the truth lines (after the Kanban):

- **Exists**
- **Verified against** (when claims reference artifacts/commits)
- **Not claimed**
- **Non-existent**
- **Unverified**
- **Functional status**

No stronger claim may be made outside that truth surface.

**CONTROL_RULE_VT_RIGOR_01 — V&T MUST NOT BE LAZY**

Each of **Exists**, **Verified against**, **Not claimed**, **Non-existent**, **Unverified**, and **Functional status** (§2.2–2.7 in `CRSP_OUTCOME_TEMPLATE.md`) MUST contain **at least one substantive bullet** under that heading for this run (not a heading alone, not “TBD”, not placeholder ellipsis).

| Heading | Minimum rigor |
|--------|----------------|
| **Exists** | Every bullet names a **concrete path**, **commit SHA**, **run id**, or **artifact filename** that is present now. |
| **Verified against** | Every bullet names **how** it was checked (command, CI job, diff, read) and **what** matched (exit code, log line, hash). If no new verification occurred, one bullet states that and why. |
| **Not claimed** | States what stronger claims are **not** being made; use `Not claimed: none beyond listed Exists` only when true. |
| **Non-existent** | States what was looked for and **not** found, or `N/A` with one line justifying no absence-check this run. |
| **Unverified** | Names each item that **cannot** be proven here (e.g. remote-only, secrets, not yet merged). |
| **Functional status** | **One** sentence tying outcome to Kanban **Build result** or to a **formal halt** id. |

Empty or label-only V&T subsections are **invalid** C-RSP outcomes.

**Follow-on C-RSP build:** When the Kanban **What’s next** implies another contract run **after** the current instance is clear, record it in `projects/c-rsp/NEXT_CRSP_BUILD.json` (`status: pending`) and run `./scripts/crsp_next_build.sh` to surface the auto-launch instruction for the next session (Section 16 + template must stay aligned).

---
## 17. Instance Declaration

This framework becomes executable only through a **fully instantiated executed contract** (no unresolved `[REQUIRED]` / forbidden placeholders), typically:

- **Project overlay:** `projects/<slug>/BUILD_CONTRACT.md` or `projects/<slug>/BUILD_CONTRACT` (repo convention per overlay)
- **Named C-RSP instance (Tier-3):** `projects/c-rsp/instances/<CONTRACT_ID>.md` when the active work is tracked as a standalone instance file

The file `projects/c-rsp/BUILD_CONTRACT.instance.md` is the **guided instance template** (workflow artifact) only; it is **not** an execution-ready contract until copied, filled, and saved as a separate executed path.
