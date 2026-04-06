---
document_type: "Constitutional"
id: "DOC-CONST-001"
repo_scope: "Cross-Repo"
authority_level: "L4"
truth_rank: 1
status: "Active"
canonical_path: "docs/constitution/DOCUMENTATION_STANDARD.md"
next_file: "docs/constitution/CANONICAL_PATHS.md"
last_verified:
  commit: "cc0b439"
  timestamp: "2026-04-06T02:07:33Z"
metadata:
  est_time_minutes: 45
  cognitive_load: "High"
  requires_interruption_buffer: true
navigation:
  parent_index: "docs/INDEX.md"
  hierarchy_level: "TLC > Constitution > Documentation Standard"
---

<!-- markdownlint-disable MD013 -->

# DOCUMENTATION_STANDARD

## 1. Purpose

This document defines the mandatory documentation system for The Living Constitution (TLC), its governed satellite repositories, and its dual-topology products.

This standard exists to eliminate the following documentation failures:

- ambiguity about what a document is
- hidden prerequisites
- mixed-purpose documents
- implied destinations
- missing operator steps
- naming drift
- contradictory sources of truth
- fake optionality
- examples that do not match real artifacts
- root-level documentation sprawl
- weak task analysis
- poor operator safety
- AI-generated documentation placed outside canonical paths

This standard is binding on:

- human authors
- AI agents
- scaffolding tools
- migration scripts
- validation tooling
- review processes
- continuous integration and enforcement systems

No repository governed by TLC may define a conflicting local documentation standard unless explicitly authorized by constitutional amendment.

## 2. Scope

This standard applies to:

1. TLC core repositories
2. governed satellite repositories
3. dual-topology products that exist both:
   - as integrated components inside TLC
   - as standalone repositories
4. repository migrations that relocate or normalize legacy documentation
5. automation that creates, edits, moves, links, validates, or indexes documentation

This standard governs:

- document classification
- document placement
- document naming
- document visibility
- navigation rules
- source-of-truth hierarchy
- task-analysis requirements
- evidence linkage
- migration behavior
- enforcement behavior

## 3. Constitutional Principles

The documentation system shall obey the following principles.

### 3.1 Predictability Over Cleverness

The system shall prefer repeated structure, fixed naming, explicit placement, and deterministic navigation over novelty or elegance.

### 3.2 Single Purpose Per Major Document

Every major document shall have one primary role. A major document shall not combine governance, explanation, execution, and evidence as equal purposes.

### 3.3 Explicitness Over Inference

A reader shall not be required to infer:

- where to start
- where to go next
- what folder to use
- what a file is for
- which document wins in a conflict
- whether a step is mandatory
- what success looks like
- how to recover from failure

### 3.4 Canonical Source First

All substantive documentation artifacts shall be created first in their canonical path. Discoverability elsewhere shall be provided by approved links, generated indices, or constitutionally approved pointer artifacts only.

### 3.5 Root Is Not a Drafting Surface

Repository root shall not be used as an uncontrolled documentation creation surface.

### 3.6 Truth Is Hierarchical

When documents conflict, the conflict shall be resolved by constitutional source-of-truth rank, not by interpretation, recency, aesthetics, or author preference.

### 3.7 Deep Task Analysis Is Mandatory

Operational and instructional documentation shall be deeply task analyzed according to the Blind Man's Test and the Default User Doctrine.

### 3.8 Explanation, Execution, Rollback, and Evidence Must Be Linked

No execution surface shall exist without rollback and verification linkage.

### 3.9 Optional Means Optional

If omitting a step can break correctness, safety, parity, verification, or expected outcome, that step shall not be labeled optional.

### 3.10 Examples Must Not Lie

Examples shall either:

- bind to real artifacts
- be explicitly labeled illustrative and non-binding

## 4. Definitions

For the purposes of this standard:

### 4.1 Major Document

A major document is any human-readable document that defines, routes, governs, explains, instructs, or proves part of the repository system.

### 4.2 Canonical Path

A canonical path is the constitutionally approved location for a given class of document.

### 4.3 Pointer Artifact

A pointer artifact is a minimal approved surface that exists only to route a user to the canonical document. A pointer artifact shall not become a shadow copy of the canonical content.

### 4.4 Root Documentation

Root documentation means any documentation artifact created directly at repository root.

### 4.5 Deep Task Analysis

Deep task analysis means breaking a task down so completely and concretely that the most vulnerable likely user can complete it safely, in order, without guessing, visual inference, hidden context, implied folder knowledge, or unstated decisions.

For documentation, the default calibration case is the Blind Man's Test.

### 4.6 Blind Man's Test

A document passes the Blind Man's Test only if the task can be completed in order by a vulnerable likely user without relying on visual inference, tacit repo knowledge, remembered context, or guesswork.

### 4.7 Governed Repository

A governed repository is a repository constitutionally bound to TLC governance, terminology, and verification expectations.

### 4.8 Dual-Topology Product

A dual-topology product is a product that exists both as:

- an integrated component within TLC
- a standalone governed repository

## 5. Document Type Taxonomy

Every major document shall declare exactly one Document Type.

Approved Document Types are:

### 5.1 Navigational

Purpose: orient the reader and route them to the correct document.

Examples:

- `README.md`
- `docs/INDEX.md`
- `docs/NAVIGATION.md`

### 5.2 Constitutional

Purpose: define binding rules, terminology, invariants, authority, and truth precedence.

Examples:

- `docs/constitution/DOCUMENTATION_STANDARD.md`
- `docs/constitution/TERMINOLOGY.md`
- `docs/constitution/DOC_TRUTH_HIERARCHY.md`

### 5.3 Architectural

Purpose: explain structure, topology, interfaces, boundaries, and relationships.

Examples:

- `docs/architecture/SYSTEM_ARCHITECTURE.md`
- `docs/architecture/DUAL_TOPOLOGY_MODEL.md`

### 5.4 Operational

Purpose: define how to perform real repository or system operations.

Examples:

- `docs/operations/BOOTSTRAP.md`
- `docs/operations/VERIFY.md`
- `docs/operations/ROLLBACK.md`

### 5.5 Instructional

Purpose: teach a human operator how to complete a task safely and sequentially.

Examples:

- `docs/instructions/FIRST_RUN.md`
- `docs/instructions/ADD_GOVERNED_REPO.md`

### 5.6 Evidence

Purpose: prove what was done, what passed, what failed, and against which standard.

Examples:

- `docs/evidence/EVIDENCE_MAP.md`
- `docs/evidence/verification/<record>.md` (commit-bound verification records)
- `verification/` (repo-level claim matrix and runs)

No other major document type is allowed unless added by constitutional amendment.

## 6. Source-of-Truth Hierarchy

The following source-of-truth order is binding:

1. Constitutional
2. Operational
3. Architectural
4. Instructional
5. Navigational

Evidence does not outrank Constitutional documents. Evidence proves conformance, failure, or drift relative to higher-order standards.

If a lower-ranked document conflicts with a higher-ranked document:

- the higher-ranked document governs
- the lower-ranked document is in drift
- the lower-ranked document must be corrected
- the conflict shall not be resolved by ad hoc interpretation

## 7. Required Universal Header Standard

Every major document shall begin with the following header fields:

```md
- Document Type: <Navigational | Constitutional | Architectural | Operational | Instructional | Evidence>
- Document ID: <DOC-...>
- Repo Scope: <TLC Core | Satellite Repo | Dual-Topology Product | Cross-Repo>
- Audience: <...>
- Primary Purpose: <one sentence>
- Use This When: <explicit trigger condition>
- Do Not Use This For: <misuse boundary>
- Authority Level: <L0-L4>
- Source of Truth Rank: <1-5 or N/A for evidence>
- Canonical Path: `<literal/path>`
- Requires: <prerequisites or None>
- Produces: <artifact/output/evidence or None>
- Next File: `<literal/path or None>`
- Related Files:
  - `<literal/path>`
- Last Verified Against:
  - Repo commit: `<sha/tag>`
  - Verification doc: `<literal/path>`
```

### 7.1 Authority Levels

- L4 = Constitutional
- L3 = Operational
- L2 = Architectural
- L1 = Instructional
- L0 = Navigational

### 7.2 Header Requirements

All header paths shall be literal, not implied.

Next File shall identify one primary continuation path only.

A document may list related files, but shall not declare multiple equal next destinations.

## 8. Canonical Documentation Placement Rules

All substantive documentation artifacts shall be created in constitutionally approved canonical paths only.

Canonical paths shall be defined in:

`docs/constitution/CANONICAL_PATHS.md`

At minimum, the following path classes shall exist where applicable:

- `docs/constitution/`
- `docs/architecture/`
- `docs/operations/`
- `docs/instructions/`
- `docs/evidence/`

For governed repositories, live governance artifacts shall use the top-level canonical path:

- `governance/`

No other canonical path for live governance artifacts is allowed in governed repositories.

No author, AI agent, or script may create a substantive document outside approved canonical paths unless explicitly allowlisted by constitutional rule.

## 9. Root Documentation Deny Rule

### 9.1 Invariant

No new substantive documentation artifact may be created at repository root unless its filename is listed in:

`docs/constitution/ROOT_DOC_ALLOWLIST.md`

Repository root is not an uncontrolled drafting surface.

### 9.2 Allowed Root Documents

Allowed root documents shall be explicitly enumerated in the allowlist.

Typical examples may include:

- `README.md`
- `LICENSE`
- `SECURITY.md`
- `CONTRIBUTING.md`
- `CODE_OF_CONDUCT.md`

No file is allowed at root by habit, precedent, convenience, or AI default behavior.

### 9.3 Prohibited Behavior

The following are prohibited:

- drafting new substantive governance or documentation files at root
- copying a canonical doc to root for convenience
- pasting modified duplicates of canonical docs at root
- allowing AI tools to emit new root-level markdown files outside the allowlist
- leaving migration leftovers at root

### 9.4 Root Discoverability Exception

Visibility at root shall be provided through allowlisted entrypoint documents, primarily README.md, using links to canonical documents.

Visibility does not authorize duplicate root content.

## 10. README Placement Rule

A README.md shall exist:

1. at repository root
2. at any folder that is a human navigation boundary
3. at any folder that is an execution boundary
4. at any folder that is an ownership or integration boundary
5. at any folder that an external or internal user may enter directly and need orientation

A README.md should not be added to folders that are:

- trivial leaf folders
- generated folders
- purely internal implementation folders with no navigation or execution role
- one-file utility folders that do not require orientation

A folder does not receive a README.md merely because it exists. It receives a README.md because it is a meaningful entrypoint.

## 11. Governance Artifact Placement and Visibility Rule

### 11.1 Canonical Framework Visibility

The canonical C-RSP framework shall remain visible in TLC under its approved canonical path:

- `projects/c-rsp/`

This is the canonical framework source. It is not the live instance location for governed repositories.

### 11.2 Live Instance Placement

Every governed repository shall store its live governance artifacts only in the top-level canonical governance path:

- `governance/`

Required live governance artifact paths are:

- `governance/BUILD_CONTRACT.instance.md`
- `governance/governance-template.lock.json`
- `governance/GOVERNANCE_BINDING.md`

If additional live governance artifacts are required, they shall also live under `governance/`.

### 11.3 Live Contract Visibility

Every governed repository must expose its live build contract as a visible first-order repository artifact.

The live contract must:

- exist at `governance/BUILD_CONTRACT.instance.md`
- be linked from root README.md
- be linked from the local `governance/README.md` or from `docs/INDEX.md`
- be identified unambiguously as the active live instance contract

### 11.4 Root Restriction

The live build contract shall not be created at repository root unless explicitly allowlisted by constitutional exception.

## 12. Navigation Model

### 12.1 Required Entrypoints

Every repository shall provide:

- root README.md
- `docs/INDEX.md`
- truth-hierarchy visibility through constitutional docs

### 12.2 One Primary Next File Rule

Every major document shall state exactly one primary Next File.

A reader shall not be forced to infer the continuation path from prose.

### 12.3 No Circular Start-Here Loops

Documentation shall not contain circular routing such as:

- README -> INDEX -> README
- NAVIGATION -> README -> NAVIGATION

unless one is clearly marked as a parent index and the other as a local entrypoint, with no ambiguity.

### 12.4 Role-Based and Task-Based Routing

`docs/INDEX.md` shall provide:

- role-based reading paths
- task-based reading paths
- repo-type declaration
- pointer to truth hierarchy
- pointer to canonical governance surfaces

## 13. Deep Task Analysis Standard

### 13.1 Requirement

All Operational and Instructional documents shall be deeply task analyzed.

### 13.2 Deep Task Analysis Criteria

A deeply task-analyzed document must:

1. define the starting state
2. define the ending state
3. define all prerequisites explicitly
4. specify exact working directory where applicable
5. specify exact filenames and paths where applicable
6. break actions into atomic sequential steps
7. eliminate discretionary decisions unless the document's purpose is decision-making
8. identify expected outputs or checkpoints after critical steps
9. define failure conditions
10. define recovery or rollback paths
11. avoid reliance on visual inference, tacit repo knowledge, remembered context, or obvious conventions
12. avoid compound steps that bundle multiple hidden sub-actions
13. avoid fake optionality
14. be readable and executable by the most vulnerable likely user

### 13.3 Blind Man's Test Criteria

A document fails the Blind Man's Test if the reader must:

- infer where a file goes
- guess what command to run next
- rely on screen layout or visual placement
- choose between unexplained alternatives
- remember hidden prerequisites
- interpret vague phrases such as put this where appropriate
- recover from failure without explicit help

### 13.4 Default User Doctrine Binding

Documentation authors shall calibrate task analysis to the most vulnerable likely user, as defined by TLC doctrine.

The barrier shall be treated as presentation, sequence, and inference burden, not presumed lack of intelligence.

## 14. Explanation, Execution, Rollback, and Evidence Linkage

No execution surface shall stand alone.

Every Operational document shall link to:

- the governing standard or rule it implements
- the rollback or recovery document
- the verification or evidence document

Every Instructional document shall link to:

- the operational canonical source it teaches or wraps
- the rollback or failure path
- the evidence or success check surface

Every Evidence document shall identify:

- what rule or operation it evaluates
- what artifact, system, or repo state it tested
- the result
- the relevant governing source

## 15. Examples and Artifact Truthfulness

### 15.1 Bound Examples

A bound example references real artifacts, real paths, real filenames, or real commands that exist in the repository or governed system.

Bound examples shall remain synchronized with actual artifacts.

### 15.2 Illustrative Examples

An illustrative example is non-binding and exists only to demonstrate form or concept.

Illustrative examples must be labeled explicitly as illustrative.

### 15.3 Prohibition

An example shall not appear concrete while silently failing to map to real artifacts.

Examples shall not create false confidence.

## 16. Naming Discipline

All documentation names, terms, product identities, and contract names shall conform to canonical terminology authority.

No document may introduce:

- variant naming for canonical products
- alternate expansions of constitutional acronyms
- inconsistent folder names for canonical doc classes
- shadow titles that imply separate authority

Terminology authority shall be defined in:

`docs/constitution/TERMINOLOGY.md`

## 17. Required Minimum Documentation Sets by Repository Class

The minimum documentation set for each repository class shall be defined and maintained as constitutional requirement.

### 17.1 TLC Core Minimum

TLC core shall include, at minimum:

- root README.md
- `docs/INDEX.md`
- constitutional docs
- architectural docs
- operations docs
- instructions docs
- evidence mapping docs
- visible governance framework surfaces

### 17.2 Governed Satellite Repo Minimum

A governed satellite repository shall include, at minimum:

- root README.md
- `docs/INDEX.md`
- local governance binding
- architecture orientation
- operations docs
- instructions docs
- evidence map
- visible live contract linkage
- top-level `governance/` directory with required live governance artifacts

### 17.3 Dual-Topology Product Minimum

A dual-topology product shall include, at minimum:

- root README.md
- `docs/INDEX.md`
- product identity doc
- dual-topology binding doc
- integrated and standalone architecture docs
- integrated and standalone operational docs where behavior differs
- parity verification or parity mapping surface
- visible live contract linkage
- top-level `governance/` directory with required live governance artifacts

Detailed file-level requirements may be enumerated in companion constitutional files.

## 18. Migration Rules for Legacy Repositories

This standard applies retroactively to legacy repositories.

### 18.1 Legacy Inventory Requirement

Before migration, all existing documentation artifacts shall be classified as:

- canonical root document
- misplaced canonical document
- obsolete document
- duplicate document
- pointer-candidate document

### 18.2 Migration Requirement

Misplaced documentation shall be moved to canonical paths.

Where discoverability is still needed, the old surface may be replaced with:

- a pointer artifact
- an index entry
- an approved entrypoint link

Shadow copies shall not remain.

Legacy live governance artifacts shall be migrated into:

- `governance/`

if they are currently located elsewhere.

### 18.3 History Preservation

Migration should preserve history using repository-native move operations where possible.

### 18.4 Post-Migration Lock

After migration, the deny and validation rules shall be enabled so the drift does not recur.

## 19. Automation and AI Generation Rules

All automation that creates or edits documentation shall comply with this standard.

This includes:

- AI coding assistants
- scaffolding tools
- repo generators
- migration scripts
- formatting tools
- doc-sync scripts

Automation shall not:

- create substantive docs at root outside the allowlist
- invent undocumented paths
- emit mixed-purpose docs without declared type
- omit required header fields
- generate duplicate shadow documents
- generate examples that do not match real artifacts when presented as concrete
- place live governance artifacts anywhere except `governance/`

Automation should:

- create docs in canonical paths only
- apply the universal header
- maintain link integrity
- update index and navigation surfaces where required
- preserve canonical terminology

## 20. Validation and Enforcement Requirements

This standard shall be enforced by tooling, not memory alone.

### 20.1 Required Validation Capabilities

Validation shall check, at minimum:

1. required header presence
2. valid Document Type
3. valid Authority Level
4. valid Source of Truth Rank
5. literal path validity for Canonical Path, Next File, and related files where applicable
6. root-level deny rule compliance
7. canonical path compliance
8. terminology compliance
9. duplicate or shadow doc detection where detectable
10. required minimum doc set presence by repo class
11. link visibility for live build contracts
12. rollback and evidence linkage for operational and instructional docs
13. required governed repo presence of `governance/`
14. required governed repo presence of mandatory live governance artifacts

### 20.2 Enforcement Layers

Enforcement should occur at:

- scaffold time
- local validation time
- pre-commit time
- pull request review time
- CI time
- migration time

### 20.3 Failure Policy

A documentation policy failure shall block merge when it violates:

- constitutional placement
- truth hierarchy
- missing required docs
- missing live contract visibility
- missing header
- prohibited root doc creation
- canonical terminology drift
- critical task-analysis safety rules
- missing or misplaced live governance artifacts

## 21. Pointer Artifact Rule

A pointer artifact is allowed only when constitutionally useful for discoverability.

A pointer artifact must:

- clearly identify itself as a pointer
- point to the canonical path
- avoid becoming a shadow copy
- remain short, stable, and unambiguous

A pointer artifact shall not contain substantive alternate content that can drift from the canonical source.

## 22. Document Lifecycle States

Every major document should be treated as existing in one of the following states:

- Draft
- Active
- Deprecated
- Superseded
- Archived

If lifecycle state is used, it shall be explicit and machine-checkable where possible.

A deprecated or superseded document must identify the canonical successor.

## 23. Exceptions and Amendments

Exceptions to this standard are prohibited unless authorized by constitutional amendment or explicit constitutional exception record.

Convenience, habit, tool default behavior, urgency, or author preference are not valid exception grounds.

## 24. Non-Compliance

A repository, document, migration, or automation surface is non-compliant if it violates any binding requirement in this standard.

Non-compliance shall be classified as:

- Critical
- Major
- Minor

Critical non-compliance includes, at minimum:

- root-level prohibited doc creation
- source-of-truth collision
- misleading live contract placement
- missing required constitutional docs
- unsafe task-analysis failure in operational or instructional docs
- missing `governance/` in a governed repository
- live governance artifacts outside `governance/`

## 25. Implementation Order

This standard shall be implemented in the following order:

1. establish canonical path authority
2. establish root-doc allowlist authority
3. normalize terminology authority
4. create or migrate constitutional docs
5. create or migrate index and navigation surfaces
6. migrate legacy docs into canonical paths
7. migrate legacy live governance artifacts into `governance/`
8. install creation scaffolds
9. install validation and enforcement tooling
10. enable CI blocking
11. maintain drift prevention as standard repo hygiene

## 26. Final Constitutional Rule

No future documentation system, repository, migration, or automation governed by TLC may bypass this standard by improvising document purpose, placement, naming, visibility, or authority.

Documentation is a governed system surface.

Its structure is not optional.
