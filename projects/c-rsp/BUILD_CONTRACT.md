# Build Contract: C-RSP

## Overview

Below is a **fully refactored C-RSP template** redesigned explicitly as a **framework template (not an executable contract)**. It incorporates all recommended improvements:

* mandatory vs optional labeling
* template prompt vs example separation
* invariant / conflict / acceptance taxonomies
* author guidance embedded
* completion quality enforcement
* contract class support
* N/A-with-reason pattern
* corrected naming + consistency
* clear distinction between template vs instance authority

This is now a **meta-specification template** for generating high-quality executable contracts.

---

## Steps

### New Template

````markdown
# 📜 C-RSP Build Contract Template
## Contractually Constrained Deterministic Single-Pass Executable Prompt (Framework)

---

## TEMPLATE METADATA

* **Template Version:** v2.0.0
* **Template Role:** Meta-specification framework for generating executable build contracts
* **Intended Use:** Authoring deterministic, governance-aligned contracts
* **Applicable Domains:** Software / Data / ML / Infra / Safety Systems
* **Contract Classes Supported:**
  - Application Build
  - Data Pipeline
  - Evaluation Pipeline
  - Infrastructure Provisioning
  - Migration
  - Safety Enforcement Layer
  - Research Workflow

> **Template Rule:** This document defines structure, completion standards, and governance grammar.  
> It is NOT executable until fully instantiated with concrete values.

---

## STATUS

* **Status:** [DRAFT | SPEC-COMPLETE | PREFLIGHT-READY | EXECUTION-READY | EXECUTED | VERIFIED | BREACHED]
* **Contract Version:** [vX.X.X]

---

## COMPLETION STANDARD (MANDATORY)

A contract instance is INVALID if it contains:

- unresolved placeholders `[ ... ]`
- vague or non-concrete nouns
- unverifiable claims
- missing verification methods
- undefined conflict resolutions
- evidence references without paths
- contradictions across sections

---

## FIELD SYNTAX CONVENTIONS

- `[Required Value]`
- `(Choose one: A | B | C)`
- `N/A — reason required`
- `Example:` indicates non-binding sample

---

## 1. IDENTITY & DOMAIN

**Requirement Level:** REQUIRED

**Template Prompt:** Define the system identity and governing purpose.

* **System Role:** [Concrete system description]
* **Contract Class:** (Choose one from metadata list)
* **TLC Domain:** (Choose: Epistemic | Human | Cognitive | Empirical)
* **Primary Objective:** [Single sentence describing system law]

<!-- Author Guidance:
Use exact system type. Avoid aspirational language.
Objective must be testable or observable.
-->

---

## 2. CURRENT STATE & ENVIRONMENT (BASELINE)

**Requirement Level:** REQUIRED

**Template Prompt:** Define the verified starting state.

* **Verified Assets (Must Exist):**
  - [Exact file paths]
* **Must NOT Exist:**
  - [Forbidden artifacts]
* **Generated Artifacts (Expected):**
  - [Outputs of build]

* **Hermetic Baseline Policy:**
  - [Describe cleaning strategy OR N/A — reason]

* **Hard Dependencies:**
  - **Runtime:** [Exact versions]
  - **Core Packages:** [Pinned versions]

---

### 2A. Dependency Policy

**Requirement Level:** REQUIRED

* **Conflict Resolution Rule:** [Define]
* **Availability Rule:** [Exact fallback OR "halt"]
* **Vulnerability Rule:** [Define CVE policy]

<!-- Author Guidance:
Do not allow implicit upgrades unless explicitly defined.
-->

---

### 2B. Target Environment Profile

**Requirement Level:** CONDITIONAL

* **OS / Platform:** [e.g., Linux x86_64]
* **Hardware Constraints:** [e.g., AVX2 | GPU | N/A — reason]

---

## 3. EXECUTION LOGIC (SINGLE-PASS PATH)

**Requirement Level:** REQUIRED

**Template Prompt:** Define ordered execution steps.

**Allowed Forms:**
- Layered (Hexagonal)
- Pipeline
- DAG
- Event-driven
- Migration
- Service bootstrap

**Execution Steps:**

1. [Step 1]
2. [Step 2]
3. [Step N]

---

### 3A. Decision Closure

**Requirement Level:** REQUIRED

* **Allowed Decisions:**
  - [Explicit list]
* **Prohibited Decisions:**
  - [Explicit list]
* **Default on Ambiguity:** [HALT | PROCEED WITH RULE]
* **Retry Policy:** [Allowed | Forbidden]

---

## 4. CONSTITUTIONAL INVARIANTS

---

### 4A. Invariant Categories (TEMPLATE TAXONOMY)

* Isolation Boundary
* Type / Schema Discipline
* Determinism / Idempotency
* Environment Constraints
* Security / Network Policy
* Licensing / Compliance
* Data Handling / Privacy
* Observability / Evidence

---

### 4B. Project-Specific Invariants

**Requirement Level:** REQUIRED

* **INVARIANT_01:** [Define]
* **INVARIANT_02:** [Define]
* **INVARIANT_N:** [Define]

<!-- Author Guidance:
Each invariant must be enforceable and testable.
-->

---

## 5. CONFLICT RESOLUTION MATRIX

**Requirement Level:** REQUIRED

### Conflict Categories (Template)

- Dependency Conflict
- Schema Conflict
- Architecture Conflict
- Runtime / Infra Conflict
- Security / Compliance Conflict
- Verification Conflict
- Truth-State Conflict
- Contract Drift

---

### Resolution Table

| Conflict Type | Protocol | Severity | Action |
|---------------|----------|----------|--------|
| [Type] | [Resolution] | [Critical/Warning] | [Halt/Continue] |

---

## 6. ACCEPTANCE CRITERIA (THE GAVEL)

---

### Required Categories

- Functional
- Verification
- Safety / Governance
- Determinism
- Evidence

---

### Optional Categories

- Performance
- Accessibility
- Security
- Cost
- Migration Integrity

---

### Criteria Table

| ID | Category | Requirement | Verification Method |
|----|----------|------------|---------------------|
| AC-1 | Functional | [Define] | [Command/Test] |
| AC-2 | Determinism | [Define] | [Hash comparison] |

---

## 7. PRE-FLIGHT VALIDATION (GATEKEEPER)

**Requirement Level:** REQUIRED

* **Validator Path:** [Path]
* **Execution Rule:** Must run before build

---

### Preflight Checks

- [ ] Environment parity verified
- [ ] Dependency lock verified
- [ ] Required assets exist
- [ ] Forbidden artifacts absent

---

### Cleaning Policy

* **Dry Run Required:** YES / NO
* **Protected Paths:** [List]
* **Backup Required:** YES / NO

---

### Logging

* **Log Path:** `./.c-rsp/CONFLICT_LOG.md`

---

## 8. VERIFICATION MAPPING (EVIDENCE MATRIX)

**Requirement Level:** REQUIRED

| Claim | Evidence | Artifact Path |
|------|----------|--------------|
| [Claim] | [Proof] | [Path] |

---

## 9. GOVERNANCE MAPPING

**Requirement Level:** REQUIRED

* **Mapping File:** `./.c-rsp/governance-map.json`

Each module must define:
- constitutional reference
- invariant mapping
- verification hook

---

## 10. VERIFICATION ARTIFACT SCHEMA

**Requirement Level:** REQUIRED

Example:

```json
{
  "contract_version": "",
  "project_name": "",
  "commit_hash": "",
  "environment": {},
  "preflight_passed": true,
  "acceptance_results": [],
  "invariants_verified": [],
  "artifact_hashes": {},
  "exceptions": []
}
```

---

## 11. BREACH TAXONOMY

| Code     | Description            |
| -------- | ---------------------- |
| BREACH-A | Unauthorized execution |
| BREACH-B | Invariant violation    |
| BREACH-C | Unverifiable claim     |
| BREACH-D | Dependency deviation   |
| BREACH-E | Non-determinism        |

---

## 12. HALT / PROCEED MATRIX

| Condition                   | Severity | Action   |
| --------------------------- | -------- | -------- |
| Placeholder present         | Critical | Halt     |
| Lockfile mismatch           | Critical | Halt     |
| Optional constraint missing | Warning  | Continue |

---

## 13. N/A DECLARATION RULE

All omitted sections must be filled as:

`N/A — [explicit reason]`

---

## 14. AUTHOR GUIDELINES (APPENDIX)

* Use concrete paths and values
* Avoid vague language
* Separate current vs intended state
* Ensure every claim has evidence
* Prefer measurable verification
* Record uncertainty explicitly

---

## END OF TEMPLATE

````
