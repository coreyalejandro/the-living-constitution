# BUILD CONTRACT INSTANCE
## Constitutionally-Regulated Single Pass Executable Prompt

> **Instance Status:** Draft. This contract wires TLC Guardian into the structural world-model evidence surface by requiring a schema-valid `ImpactReport` to be generated and attached as **evidence** for any non-read-only action. Enforcement is **advisory-first** (log + review-required) in this instance; halting gates are deferred to a follow-on contract once impact semantics stabilize.

---
## 0. Instance Governance

- **Artifact Class:** Executable contract instance (Tier-3 constitutional).
- **Canonical Expansion:** `C-RSP` = **Constitutionally-Regulated Single Pass** only (**INVARIANT_TERM_01**).
- **Schema Authority:** `projects/c-rsp/contract-schema.json` defines core section order; this file remains conformant.

---
## 1. Contract Identity

- **Contract Title:** Bind Guardian Pre-Action Evidence to Semgraph ImpactReport
- **Contract ID:** CRSP-SEMGRAPH-GUARDIAN-001
- **Version:** v1.0.0-draft
- **Schema Version:** v1.0.0
- **Status:** Draft
- **Adoption Tier:** Tier-3-Constitutional
- **System Role:** Prevent “blind enforcer” governance by forcing every substantive action to carry a structural impact evidence artifact.
- **Primary Objective:** Add a Guardian-side evidence verifier that validates a referenced `ImpactReport` and records its presence in Guardian logs.
- **Scope Boundary:** `src/guardian.py` only; `verification/semgraph/*` is treated as read-only evidence surface.
- **Not Claimed:** No hard halts based on ripple results; no domain-cluster binding; no clustering; no LLM judge packet wiring; no GitHub/GitLab automation.

---
## 2. Contract Topology + Profile

- **Topology Mode:** TLC-Core
- **Profile Type:** Core
- **Profile Overlay Source:** N/A
- **Verifier Class:** core-verifier
- **Authoritative Truth Surface:**
  - `projects/c-rsp/BUILD_CONTRACT.md`
  - `projects/c-rsp/contract-schema.json`
  - `projects/c-rsp/instances/CRSP-SEMGRAPH-GUARDIAN-001.md` (this executed instance)
  - `src/guardian.py`
  - `verification/semgraph/ImpactReport.schema.json`
- **Instance Artifact Path:** `projects/c-rsp/instances/CRSP-SEMGRAPH-GUARDIAN-001.md`
- **Governance Lock Path:** N/A

### 2A. Profile Merge Rule

Base constitutional template governs this instance. No profile may override canonical section order or V&T rigor.

### 2B. Instance Rule

Executable only when: Guardian changes are minimal, deterministic, and testable via CLI; evidence validation uses the canonical schema; no claims beyond executed checks.

---
## 3. Baseline State

- **Existing Repo / System:** `coreyalejandro/the-living-constitution`
- **Baseline Commit / Anchor:** `STATUS.json` verification target.
- **Verified Existing Assets:** `src/guardian.py` already validates evidence directories against JSON Schema for EVAL-001.
- **Known Constraints:** Guardian must remain safe-by-default; avoid adding tool-specific assumptions.
- **Known Gaps:** Guardian does not currently validate or require structural impact evidence for actions that mutate code.
- **Legacy Migration Context:** N/A.

---
## 4. Dependencies and Inputs

- **Required Inputs:** `verification/semgraph/ImpactReport.schema.json`; `scripts/verify_semgraph_integrity.py` (for local verification).
- **External Dependencies:** `jsonschema` already present (`requirements-verify.txt`).
- **Governance Dependencies:** Article I truth discipline; Article III verification-before-done.
- **Forbidden Assumptions:** Do not assume git refs are available inside Guardian; Guardian should validate a provided evidence path only.

### 4A. Cross-Repo Governance Dependency Graph

- **Parent Constitutional Source:** `governance/constitution/core/articles.md`
- **Shared Overlay Profiles:** none
- **Dual-Topology Linked Repos:** none
- **Satellite Dependents:** none
- **Drift Detection Scope:** If the ImpactReport schema changes, Guardian validation must be updated in a follow-on contract with evidence.

---
## 5. Risk + Control Classification

- **Risk Class:** High
- **Side-Effect Class:** Internal
- **External Action Scope:** Modifies Guardian enforcement behavior for tool calls by adding an evidence validation step (advisory).
- **Stop/Override Required:** Yes
- **Recovery Mode:** Assisted

### 5A. Conditional Stop / Override Rule

Stop if Guardian begins failing health checks or blocks read-only workflows. Override authority: human repo owner with explicit rationale in Guardian log or outcome report.

---
## 6. Execution Model

- **Execution Mode:** Single-pass deterministic build contract
- **Decision Closure Rule:** No open-ended branch points inside executable sections
- **Fallback Rule:** If semgraph evidence path is missing, Guardian records `review_required` but does not halt (v1 advisory-only).
- **Generated Artifacts:**
  - Updated `src/guardian.py` with ImpactReport validation helper
  - Guardian log entries extended to include `impact_report_evidence` presence/validation result (when provided)
- **Promotion Target:** Draft → Draft with evidence that Guardian validates a referenced ImpactReport via CLI.

### 6A. Ordered Operations (Blind Man Test)

| **Step ID** | **Actor** | **Action** | **Inputs** | **Outputs** | **Verify** | **If Failure** |
|-------------|-----------|------------|------------|-------------|------------|----------------|
| OP-01 | agent | Add Guardian helper: validate semgraph impact report | `src/guardian.py`, schema path | updated `src/guardian.py` | `python3 src/guardian.py --health-check` | Halt; revert |
| OP-02 | agent | Add CLI entrypoint for checking an ImpactReport file | `src/guardian.py` | new CLI flag | run command exits 0 on valid artifact | Halt; fix |

### 6B. Halt Conditions (instance-local)

| **Condition** | **Stop Reason** | **Next Action** |
|---------------|-----------------|-----------------|
| Guardian health check fails | Safety regression | Revert changes |
| Evidence validation crashes | Unsafe validation | Fix to fail-soft + record |

### 6C. Success Conditions

- **Success:** Guardian can validate a provided ImpactReport path against `verification/semgraph/ImpactReport.schema.json`.
- **Done:** Advisory evidence binding exists and is verifiable by command output.

### 6D. Major Component Implementation Snippets

N/A in contract text; changes are limited to Guardian helper + CLI flag.

---
## 7. Lifecycle State Machine

### Allowed States

Draft; Active; Frozen; Superseded

### Transition Rules

Draft → Active requires: validated run evidence proving Guardian accepts valid ImpactReport and rejects invalid ones without crashing.

### Transition Evidence

Verification command outputs captured in a C-RSP outcome report.

---
## 8. Invariants

### Required Global Invariants

INVARIANT_TERM_01; INVARIANT_SCHEMA_01; INVARIANT_ARTICLE_I_01; INVARIANT_ARTICLE_III_01; INVARIANT_REC_01

### Profile Invariants

- **INVARIANT_FAILSOFT_01:** Evidence validation failures must not crash Guardian; they must yield a deterministic FAIL payload.

---
## 9. Acceptance Criteria

| ID | Requirement | Verification Method | Pass Condition |
|----|-------------|---------------------|----------------|
| AC-01 | Guardian health check unchanged | `python3 src/guardian.py --health-check` | exit 0 |
| AC-02 | Guardian validates a real ImpactReport artifact | `python3 src/guardian.py --verify-impact-report <path>` | prints PASS, exit 0 |
| AC-03 | Guardian rejects malformed artifact deterministically | `python3 src/guardian.py --verify-impact-report <badpath>` | prints FAIL, exit non-zero |

---
## 10. Rollback & Recovery

- **Safe-State Definition:** Guardian returns to pre-contract behavior (no semgraph validation).
- **Rollback Procedure:** Revert Guardian helper + CLI additions; re-run `--health-check`.
- **Recovery Authority:** Human repo owner.
- **Rollback Evidence Paths:** Outcome report notes rollback.
- **Partial Execution Handling:** Partial wiring is non-authoritative; must be marked as partial in V&T.

---
## 11. Evidence + Truth Surface

- **Primary Evidence Paths:** `verification/semgraph/ImpactReport.schema.json`; a concrete ImpactReport run under `verification/semgraph/runs/`.
- **Generated Reports:** Guardian CLI verification output.
- **Audit Artifacts:** Outcome report per `projects/c-rsp/CRSP_OUTCOME_TEMPLATE.md`.
- **Evidence Boundary:** Only validates structure/schema, not semantic correctness of risk scoring.

---
## 12. Conflict Matrix

| Conflict Type | Example | Severity | Resolution |
|---------------|---------|----------|------------|
| Over-enforcement | Halting on missing evidence in v1 | High | Halt and defer to follow-on contract |
| Schema drift | Guardian validates against outdated schema | High | Block promotion until updated |

---
## 13. Halt Matrix

Halt on: Guardian health-check regression; non-deterministic validation; crashes on missing/invalid evidence.

---
## 14. Preflight

Preflight verifies: schema file exists; Guardian health check passes; sample ImpactReport exists.

**Preflight Command(s):**

```bash
python3 src/guardian.py --health-check
```

---
## 15. Adoption Tiers

Tier 1 — identity.

Tier 2 — acceptance criteria + rollback.

Tier 3 — invariants + halt/conflict matrices.

This instance is Tier-3.

---
## 16. Output Format

Mandatory report shape: `projects/c-rsp/CRSP_OUTCOME_TEMPLATE.md`.

---
## 17. Instance Declaration

This contract is executable only through this instantiated document: `projects/c-rsp/instances/CRSP-SEMGRAPH-GUARDIAN-001.md`. Status remains **Draft** until acceptance criteria are satisfied with executed evidence and a corresponding outcome report is written.

