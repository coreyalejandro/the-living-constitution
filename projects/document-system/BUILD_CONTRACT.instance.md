# C-RSP Build Contract Instance

**Constitutionally-Regulated Single Pass Executable Prompt (Framework)**

**Template Status:** Fully instantiated executable contract draft for the TLC document-system constitutionalization run.

---

## 0. Template Governance

- **Template Class:** Constitutional master template
- **Canonical Expansion:** Constitutionally-Regulated Single Pass
- **Invalidation Rule:** Any alternate expansion of C-RSP is governance drift and invalidates the contract instance.
- **Instance Requirement:** This template is not executable by itself. Every run must produce or reference an instantiated contract artifact.
- **Schema Authority:** `contract-schema.json` is the canonical machine-readable definition of contract shape.

### Global Constitutional Invariants

- **INVARIANT_TERM_01:** The canonical expansion of C-RSP must be exactly Constitutionally-Regulated Single Pass.
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

- **Contract Title:** TLC Document System Constitutionalization + Enforcement Hardening
- **Contract ID:** tlc-docsys-constitutionalization-001
- **Version:** 1.0.0-draft
- **Schema Version:** 1.0.0 (canonical: `projects/c-rsp/contract-schema.json` field `schema_version`)
- **Status:** Draft
- **Adoption Tier:** Tier-2-Operational
- **System Role:** TLC-Core governance document system repair, normalization, enforcement, and CI hardening
- **Primary Objective:** Fix the TLC document system by making document governance a first-class constitutional component with canonical path policy, root-document allowlist, truth hierarchy, terminology authority, normalization of root-level violations, executable verifier coverage, and hard-wired non-silent continuation semantics until acceptance criteria are satisfied or a formal halt condition is triggered.
- **Scope Boundary:** Changes are limited to the coreyalejandro/the-living-constitution repository and its governance/documentation surfaces, verification scripts, and CI workflow(s) required to enforce document-system constitutional rules. No downstream product repos are modified by this contract.
- **Not Claimed:** This contract does not claim that the document system is already fixed, that all repo-wide enforcement exists today, that external satellite repos are updated, that every historical document is perfectly normalized, or that any runtime/system daemon outside the TLC repo has been installed.

---

## 2. Contract Topology + Profile

- **Topology Mode:** TLC-Core
- **Profile Type:** Core
- **Profile Overlay Source:** N/A
- **Verifier Class:** core-verifier
- **Authoritative Truth Surface:** THE_LIVING_CONSTITUTION.md, CLAUDE.md, STATUS.json, STATUS.md, MASTER_PROJECT_INVENTORY.json, MASTER_PROJECT_INVENTORY.md, projects/c-rsp/BUILD_CONTRACT.md, docs/constitution/CANONICAL_PATHS.md, docs/constitution/ROOT_DOC_ALLOWLIST.md, docs/constitution/DOC_TRUTH_HIERARCHY.md, docs/constitution/TERMINOLOGY.md, normalization report artifact(s), verifier script artifact(s), .github/workflows/verify.yml
- **Instance Artifact Path:** projects/document-system/BUILD_CONTRACT.instance.md
- **Governance Lock Path:** projects/c-rsp/governance-template.lock.json

### 2A. Profile Merge Rule

The base constitutional template governs all contract instances.

Overlay profiles may specialize only the following:

- required file inventories
- verifier scope
- topology-specific promotion rules
- CI workflow requirements
- component-specific evidence requirements
- bounded customization blocks inside approved schema slots
- domain-specific payload inside customization zones

Overlay profiles may not override:

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

- **Existing Repo / System:** coreyalejandro/the-living-constitution
- **Baseline Commit / Anchor:** `7cff059cd7bc643a07ce98923fd2a52a022c7d54` (branch `main`, recorded at instance materialization; supersede with activation-time tag if promotion uses a different anchor)
- **Verified Existing Assets:**
  - canonical master template exists at projects/c-rsp/BUILD_CONTRACT.md
  - CLAUDE.md declares TLC as a governance overlay and not a code repository
  - STATUS.json / STATUS.md exist as the current status pair
  - MASTER_PROJECT_INVENTORY.json / MASTER_PROJECT_INVENTORY.md exist as the current inventory pair
  - root repo currently contains additional root-level document files including ChatGPT-AI Governance Frameworks.md, HANDOFF.md, delegated-whistling-cherny.md, and openmemory.md
  - tasks/lessons.md exists under tasks/, not at root
  - current script surface includes bootstrap_repo.sh, render_status_surface.py, ci_self_verify_governance_artifact.py, verify_attestation.py, verify_consentchain_family.py, verify_cross_repo_consistency.py, verify_governance_chain.py, verify_institutionalization.py, verify_project_topology.py, verify_topology.py, and verify_ui_governance.py
  - .github/workflows/verify.yml exists
- **Known Constraints:**
  - canonical section order from the master template must be preserved exactly
  - no unresolved placeholders are permitted in an executable instance
  - authoritative truth surface must govern claims
  - TLC root is already carrying document sprawl
  - current verifier surface is real but dedicated document-constitution enforcement is not yet proven
- **Known Gaps:**
  - docs/constitution/ companion files are not yet proven present in the live repo
  - root-document allowlist is not yet active
  - dedicated document-system verifier coverage is not yet proven
  - normalization of unauthorized root documents is not yet executed
  - explicit hard-wired "do not silently stop work" control semantics are not yet codified in the document system
- **Legacy Migration Context:** Existing root-level docs and historical governance materials must be normalized into constitutional namespaces without losing traceability; unauthorized root docs must be either relocated, absorbed, archived, or explicitly exempted through constitutional amendment.

---

## 4. Dependencies and Inputs

- **Required Inputs:**
  - projects/c-rsp/BUILD_CONTRACT.md
  - THE_LIVING_CONSTITUTION.md
  - CLAUDE.md
  - STATUS.json
  - STATUS.md
  - MASTER_PROJECT_INVENTORY.json
  - MASTER_PROJECT_INVENTORY.md
  - current repo root listing
  - current docs/ tree listing
  - current scripts/ tree listing
  - current .github/workflows/verify.yml
  - verified root violation candidates: ChatGPT-AI Governance Frameworks.md, HANDOFF.md, delegated-whistling-cherny.md, openmemory.md
- **External Dependencies:**
  - GitHub-hosted repository state for coreyalejandro/the-living-constitution
  - Python 3 runtime for verifier scripts
  - shell environment capable of running repo bootstrap and verification commands
- **Governance Dependencies:**
  - projects/c-rsp/BUILD_CONTRACT.md as constitutional master template
  - existing status truth policy anchored in STATUS.json / STATUS.md
  - existing governance verification surface under scripts/
  - current repo-operating controls in CLAUDE.md
- **Forbidden Assumptions:**
  - do not assume dedicated document-system enforcement already exists
  - do not assume all root docs are legitimate because they are present
  - do not assume README or ad hoc root files can override constitutional policy
  - do not assume "temporary" root docs are exempt
  - do not assume work may stop on first failure without entering bounded troubleshooting/recovery logic
- **Dependency Policy:** All dependencies must be explicitly named; implicit dependency assumptions are invalid.

### 4A. Cross-Repo Governance Dependency Graph

Every Tier-2+ contract must declare linked governance relationships:

- **Parent Constitutional Source:** THE_LIVING_CONSTITUTION.md
- **Shared Overlay Profiles:** none
- **Dual-Topology Linked Repos:** none
- **Satellite Dependents:** none
- **Drift Detection Scope:** TLC root documentation surfaces, constitutional doc-policy namespace, verifier scripts, verify workflow, normalization artifacts, README/CLAUDE/status/inventory references to canonical document system

---

## 5. Risk + Control Classification

- **Risk Class:** High
- **Side-Effect Class:** Internal
- **External Action Scope:** Internal repo mutations only: create constitutional doc-policy artifacts, relocate/normalize unauthorized root docs, modify scripts/workflows, update references and truth surfaces
- **Stop/Override Required:** Yes
- **Recovery Mode:** Assisted

### 5A. Conditional Stop / Override Rule

If Risk Class in {High, Critical} or Side-Effect Class in {External, Destructive, Regulated}, then:

- stop/override semantics are mandatory
- a safe-state definition is mandatory
- a rollback/recovery section is mandatory
- failure to define them blocks promotion

---

## 6. Execution Model

- **Execution Mode:** Single-pass deterministic build contract
- **Decision Closure Rule:** No open-ended branch points inside executable sections
- **Fallback Rule:** Any unresolved ambiguity triggers halt or explicit escalation
- **Generated Artifacts:**
  - projects/document-system/BUILD_CONTRACT.instance.md
  - docs/constitution/CANONICAL_PATHS.md
  - docs/constitution/ROOT_DOC_ALLOWLIST.md
  - docs/constitution/DOC_TRUTH_HIERARCHY.md
  - docs/constitution/TERMINOLOGY.md
  - docs/constitution/NORMALIZATION_REPORT.md
  - docs/constitution/ROOT_DOC_VIOLATIONS.json
  - scripts/verify_document_constitution.py
  - updates to .github/workflows/verify.yml to invoke document-constitution verification
  - targeted updates to README.md, CLAUDE.md, and any truth-surface references required to point to the new constitutional document system
  - relocation map artifact such as docs/constitution/NORMALIZATION_MAP.md if files are moved
- **Promotion Target:** Merge-ready TLC-Core governance state with active document-system constitution and passing document-constitution verifier in CI

### 6A. Dual-Topology Rule

If Topology Mode = Dual-Topology, the contract must define both paths explicitly:

- integrated/internal path
- standalone/external path

No change is complete unless:

1. both paths are updated, or
2. the contract explicitly records why one path is intentionally out of scope

---

## 7. Lifecycle State Machine

### Allowed States

- Draft
- Active
- Frozen
- Superseded

### Transition Rules

- Draft to Active requires: no placeholders, schema validation pass, preflight pass, required fields complete
- Active to Frozen requires: acceptance criteria satisfied, evidence recorded, promotion rules satisfied
- Frozen to Superseded requires: successor instance exists and references the superseded contract
- any invalid transition halts and records an audit event

### Transition Evidence

Each transition must emit or update:

- lifecycle transition record
- associated verifier/preflight report
- evidence links to the truth surface

---

## 8. Invariants

### Required Global Invariants

- INVARIANT_TERM_01
- INVARIANT_SCHEMA_01
- INVARIANT_EXEC_01
- INVARIANT_EXEC_02
- INVARIANT_EXEC_03
- INVARIANT_EXEC_04
- INVARIANT_EXEC_05
- INVARIANT_CTRL_01
- INVARIANT_LIFE_01
- INVARIANT_REC_01

### Profile Invariants

- **INVARIANT_DOCSYS_01:** All root-level documentation files must be either allowlisted or classified as violation candidates in normalization artifacts.
- **INVARIANT_DOCSYS_02:** docs/constitution/ is the canonical namespace for document-governance policy artifacts.
- **INVARIANT_DOCSYS_03:** README.md may orient and link but may not outrun STATUS.json, MASTER_PROJECT_INVENTORY.json, or constitutional document policy.
- **INVARIANT_DOCSYS_04:** STATUS.json remains the machine-authoritative current-status truth surface.
- **INVARIANT_DOCSYS_05:** MASTER_PROJECT_INVENTORY.json remains the machine-authoritative inventory/topology truth surface.
- **INVARIANT_DOCSYS_06:** TERMINOLOGY.md is the canonical terminology authority for document-governance language.
- **INVARIANT_DOCSYS_07:** Unauthorized root surfaces must not persist unclassified after normalization execution.
- **INVARIANT_DOCSYS_08:** Document-system enforcement must run in CI through an explicit verifier invocation.
- **INVARIANT_DOCSYS_09:** Work may not silently stop after the first verifier or migration failure; bounded troubleshooting must continue until acceptance criteria pass or a named halt condition is triggered and recorded.
- **INVARIANT_DOCSYS_10:** The "DO NOT STOP WORK" control is bounded, not infinite: it authorizes repeated troubleshooting, diagnosis, and corrective iteration inside this scope, but it does not permit bypass of constitutional halt conditions, truth discipline, or safe-state requirements.
- **INVARIANT_DOCSYS_11:** Any relocation or normalization must preserve traceability through explicit mapping artifacts and updated references.
- **INVARIANT_DOCSYS_12:** No root-level document policy may exist outside the allowlisted root surfaces and docs/constitution/ once this contract is promoted.

---

## 9. Acceptance Criteria

| ID | Requirement | Verification Method | Pass Condition |
|----|-------------|----------------------|----------------|
| AC-01 | The four constitutional companion files exist in docs/constitution/ with canonical filenames and internally consistent policy | file existence check + markdown lint + manual content diff against contract requirements | All four files exist exactly at docs/constitution/CANONICAL_PATHS.md, docs/constitution/ROOT_DOC_ALLOWLIST.md, docs/constitution/DOC_TRUTH_HIERARCHY.md, and docs/constitution/TERMINOLOGY.md |
| AC-02 | The repo root documentation surface is inventoried and normalized | root scan + normalization report + violations JSON | docs/constitution/NORMALIZATION_REPORT.md and docs/constitution/ROOT_DOC_VIOLATIONS.json enumerate every root-level documentation file and classify each as allowlisted, relocated, absorbed, archived, or violation |
| AC-03 | All currently known unauthorized root-level docs are resolved or explicitly classified for resolution | file scan + normalization map + git diff | ChatGPT-AI Governance Frameworks.md, HANDOFF.md, delegated-whistling-cherny.md, and openmemory.md are no longer ambiguous; each has a constitutional disposition recorded and implemented or blocked with explicit evidence |
| AC-04 | A dedicated document-constitution verifier exists | file existence + script execution | scripts/verify_document_constitution.py exists and exits successfully against the normalized repo state |
| AC-05 | CI enforces the document constitution | workflow inspection + CI command verification | .github/workflows/verify.yml or an equivalent active workflow invokes scripts/verify_document_constitution.py as part of verification |
| AC-06 | Truth-surface references are updated to the new document system | targeted grep / link check / manual review | README.md, CLAUDE.md, and any other touched truth surfaces do not contradict the new document constitution and correctly point to the governing artifacts |
| AC-07 | Hard-wired "DO NOT STOP WORK" troubleshooting semantics are embedded in the contract and executable enforcement path | contract review + verifier/help text + failure-mode test | The contract and verifier behavior require continued bounded troubleshooting on recoverable failures and only permit stop on explicit halt conditions, producing recorded evidence for both retries and halts |
| AC-08 | Preflight, normalization, and verifier evidence is recorded | artifact existence + command logs | Preflight report, normalization artifacts, and verifier outputs exist at declared evidence paths and support all claims made |
| AC-09 | No unresolved placeholders remain in the executable instance or generated constitutional files | placeholder scan | Zero occurrences of [REQUIRED], TODO, or unresolved placeholder markers remain in contract or generated policy files |
| AC-10 | Repo enters a safe normalized state without root-document policy drift | full verifier run + manual repo root inspection | Root doc surface matches allowlist policy and document-constitution verifier passes |

All acceptance criteria must be executable, objective, and mapped to evidence.

---

## 10. Rollback & Recovery

- **Safe-State Definition:** The repo remains in a truthful, buildable governance state where pre-existing authoritative files (THE_LIVING_CONSTITUTION.md, CLAUDE.md, STATUS.json, STATUS.md, MASTER_PROJECT_INVENTORY.json, MASTER_PROJECT_INVENTORY.md, existing verification scripts, and workflow files) remain intact, unauthorized document relocations are reversible via explicit mapping, and no claims exceed the evidence surface.
- **Rollback Procedure:**
  1. preserve a pre-change commit anchor and file inventory before mutation
  2. if normalization or verifier integration corrupts truth surfaces or breaks verification, revert mutated files to the pre-change anchor
  3. restore any moved root docs to original locations only if necessary to recover truthful continuity
  4. retain generated normalization artifacts and failure reports in a non-promoted state for diagnosis
  5. rerun preflight to confirm return to prior safe state
- **Recovery Authority:** TLC repo operator with constitutional authority to modify the TLC-Core governance repo
- **Rollback Evidence Paths:** docs/constitution/NORMALIZATION_REPORT.md, docs/constitution/NORMALIZATION_MAP.md, pre-change file inventory artifact, git diff, verifier failure logs, rollback commit reference
- **Partial Execution Handling:** Partial execution is not promotable. If companion files are created but normalization or enforcement is incomplete, the run must continue bounded troubleshooting under INVARIANT_DOCSYS_09 until acceptance criteria pass or a named halt condition is triggered. Silent abandonment is invalid. If halt is triggered, the repo must be left in the declared safe state with explicit evidence of incomplete promotion.

---

## 11. Evidence + Truth Surface

- **Primary Evidence Paths:**
  - projects/document-system/BUILD_CONTRACT.instance.md
  - docs/constitution/CANONICAL_PATHS.md
  - docs/constitution/ROOT_DOC_ALLOWLIST.md
  - docs/constitution/DOC_TRUTH_HIERARCHY.md
  - docs/constitution/TERMINOLOGY.md
  - docs/constitution/NORMALIZATION_REPORT.md
  - docs/constitution/ROOT_DOC_VIOLATIONS.json
  - docs/constitution/NORMALIZATION_MAP.md
  - scripts/verify_document_constitution.py
  - .github/workflows/verify.yml
  - preflight report artifact
  - verifier output artifact
  - git diff / commit evidence
- **Generated Reports:**
  - preflight report
  - normalization report
  - root violation inventory JSON
  - document-constitution verifier report
  - CI verification output
- **Audit Artifacts:**
  - lifecycle transition record
  - rollback/recovery record if applicable
  - failure-mode logs for recoverable troubleshooting attempts
  - acceptance-criteria checklist result
- **Evidence Boundary:** Only artifacts listed in the authoritative truth surface and evidence paths may be used to claim the document system is fixed, normalized, enforced, or first-class.
- **Truth Discipline:** Claims in the contract may not exceed evidence declared in the truth surface.

---

## 12. Conflict Matrix

| Conflict Type | Example | Severity | Resolution |
|---------------|---------|----------|------------|
| Terminology Authority Conflict | Non-canonical C-RSP expansion | Critical | Halt |
| Profile Drift Conflict | Overlay contradicts base constitutional rules | Critical | Halt |
| Topology Misclassification | Satellite treated as TLC-Core or vice versa | Critical | Halt |
| Incomplete Instance Conflict | Missing required instance fields | Critical | Halt |
| Evidence Gap Conflict | Claim not anchored to evidence path | High | Block promotion |
| Verifier Scope Conflict | Wrong verifier class for topology | High | Block promotion |
| Schema Drift Conflict | Core section shape differs from schema | Critical | Halt |
| Lifecycle Conflict | Illegal state transition | High | Block promotion |
| Recovery Conflict | Required rollback semantics missing | High | Block promotion |
| Document Sprawl Conflict | Root-level doc exists outside allowlist and is not classified | High | Block promotion |
| Silent Stop Conflict | Work halts on recoverable failure without entering bounded troubleshooting and recording evidence | Critical | Halt |
| Root Truth Conflict | README or ad hoc root doc claims stronger authority than constitutional truth surfaces | High | Block promotion |

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
- a recoverable failure is misclassified as success
- the run attempts to bypass the "DO NOT STOP WORK" troubleshooting rule by ending without acceptance or formal halt evidence
- normalization would destroy traceability or authoritative truth surfaces without recovery evidence
- exact execution anchor commit remains unset at activation time

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

### Preflight Command(s)

```text
./scripts/bootstrap_repo.sh
python3 scripts/verify_governance_chain.py
python3 scripts/verify_institutionalization.py
python3 scripts/verify_topology.py
python3 scripts/verify_project_topology.py
python3 scripts/verify_cross_repo_consistency.py
python3 scripts/render_status_surface.py --root .
python3 scripts/verify_document_constitution.py
```

---

## 15. Adoption Tiers

**Tier 1 — Minimum Viable Governance**

Requires:

- identity block
- topology selection
- canonical terminology
- placeholder-free instance artifact
- schema-valid structure

**Tier 2 — Operational**

Requires Tier 1 plus:

- acceptance criteria
- risk/control classification
- CI verifier integration
- rollback/recovery semantics
- lifecycle transition evidence

**Tier 3 — Constitutional**

Requires Tier 2 plus:

- full invariant registry
- dual-topology support where applicable
- governance lockfiles
- evidence ledger and dependency graph
- audit-grade promotion evidence

---

## 16. Output Format

All execution summaries must end with:

- Exists
- Non-existent
- Unverified
- Functional status

No stronger claim may be made outside that truth surface.

---

## 17. Instance Declaration

This framework becomes executable only through a fully instantiated contract document, typically: BUILD_CONTRACT.instance.md

---

## Execution Payload

### Exact Objective Resolution

Establish the TLC document system as a first-class constitutional subsystem by creating canonical document-governance policy files, normalizing unauthorized root documentation, adding dedicated verifier coverage, integrating that verifier into CI, and hard-wiring bounded troubleshooting semantics that prohibit silent stop-work until the system is fixed or a formal halt condition is reached.

### System / Repo Being Changed

coreyalejandro/the-living-constitution

### Topology Mode Resolution

TLC-Core

### Profile Type Resolution

Core

### Verifier Class Resolution

core-verifier

### Baseline State / Current Known Assets Resolution

The repo already contains the constitutional master template, status/inventory truth surfaces, existing governance verification scripts, and multiple non-allowlisted root-level docs; dedicated document-system constitution artifacts and enforcement are not yet proven.

### Concrete Scope Boundary Resolution

**In-scope:**

- create and ratify the four docs/constitution/ companion files
- scan and normalize root-level document surfaces
- produce normalization artifacts
- create dedicated document-system verifier logic
- wire verifier into CI
- update root/truth-surface references that must point to the new document constitution
- embed hard-wired bounded troubleshooting semantics

**Out-of-scope:**

- downstream satellite repo changes
- non-document product feature work
- redesign of unrelated governance systems
- claims of full ecosystem-wide propagation

### Explicitly Not Claimed Resolution

This contract does not claim the document system is already fixed, perfect, propagated to all other repos, or enforced outside TLC-Core today.

### Execution discipline — single BUILD_CONTRACT + Kanban-first V&T

**CONTROL_RULE_KBC_01 — SINGLE ACTIVE BUILD CONTRACT + KANBAN-FIRST V&T + NO TERMINAL "DONE" WHILE THE BOARD IS OPEN**

1. **Single active BUILD_CONTRACT:** Exactly one BUILD_CONTRACT instance is the **active execution scope** at a time until that contract is **clear**—meaning all in-scope acceptance criteria for **this** instance are satisfied by evidence and verifiers required by this instance pass, **or** a **formal halt** is recorded under **Global Halt Conditions** / Section 13 with a named condition and safe-state evidence. Starting a different `BUILD_CONTRACT.instance.md` as active scope before the current one is clear is **not allowed** except where an instance explicitly defines supersession.

2. **Kanban-first V&T:** Every **V&T Statement** (interim or final) MUST follow `projects/c-rsp/CRSP_OUTCOME_TEMPLATE.md`: the **first** content inside **§2 V&T Statement** MUST be **§2.1 Visual board (Kanban)** (table + signals). No **Exists**, **Verified against**, **Not claimed**, **Non-existent**, **Unverified**, or **Functional status** line may appear **above** the Kanban. Omitting the board or reordering is an **invalid** outcome report.

3. **No stop while required work remains on the board:** If the Kanban shows required scope for **this** contract still in **BACKLOG**, **IN PROGRESS**, or **BLOCKED** (cards that represent unfinished ACs, failing verifiers, or unresolved blockers for **this** instance), the executor MUST NOT treat the run as complete, MUST NOT emit a terminal “build finished” claim, and MUST continue execution, remediation, or explicit handoff within this contract until those columns are clear for required work **or** a formal halt is recorded. **What’s next** may point to a **follow-on** BUILD_CONTRACT only **after** the current contract is clear for its declared scope.

**Cross-reference:** **CONTROL_RULE_DNSW_01** requires continued iteration on recoverable failures until pass or formal halt; **CONTROL_RULE_KBC_01** adds the **visible Kanban** and **single-active-BC** constraints so “stopped” cannot be mistaken for “done” while cards remain. **CONTROL_RULE_VT_RIGOR_01** (`projects/c-rsp/BUILD_CONTRACT.md` Section 16) forbids lazy V&T: each of **Exists** through **Functional status** must carry substantive bullets (paths, methods, explicit disclaimers)—not empty headings.

### DO NOT STOP WORK Provision

**CONTROL_RULE_DNSW_01 — DO NOT STOP WORK ON RECOVERABLE FAILURE:**

If the run encounters a recoverable failure inside scope—such as path mismatches, unauthorized root docs, broken references, failing document verifier assertions, markdown hygiene failures, or CI wiring defects—the run must continue bounded troubleshooting and corrective iteration until one of two states is reached:

1. all acceptance criteria pass and promotion is lawful, or
2. a named halt condition in Section 13 is triggered and recorded with evidence.

This rule forbids:

- silent abandonment
- premature "done" claims
- stopping after first failure without diagnosis
- treating partial normalization as completion
- omitting retry/recovery evidence

This rule does not authorize:

- bypass of constitutional halt conditions
- destructive mutation without rollback semantics
- invented evidence
- infinite looping without state change

**SYSTEM_HARDWIRE_REQUIREMENT_DNSW_02:**

The dedicated document verifier must fail the run if a partial/incomplete document-system execution ends without either:

- passing all acceptance criteria, or
- recording a formal halt artifact naming the triggered halt condition and current safe state.

---

## Materialization footer (instance record)

**Exists**

- This file at projects/document-system/BUILD_CONTRACT.instance.md
- Resolved schema version 1.0.0 and baseline anchor 7cff059cd7bc643a07ce98923fd2a52a022c7d54 (main)
- Canonical governance lock path projects/c-rsp/governance-template.lock.json

**Non-existent**

- Claims that AC-01 through AC-10 are satisfied in the live repo before the listed generated artifacts and verifier exist and pass

**Unverified**

- Whether docs/constitution/ companions, normalization JSON/report, and verify_document_constitution.py exist at HEAD after further commits

**Functional status**

- Instance record is materialized; contract remains Draft until preflight and acceptance criteria close
