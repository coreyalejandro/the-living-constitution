# BUILD CONTRACT INSTANCE
## Constitutionally-Regulated Single Pass Executable Prompt

> **Instance Status:** Draft. This contract defines the minimum governed build for a **structural world-model** ("semantic graph") engine and its integration points with TLC truth surfaces and Guardian enforcement. It does **not** claim full GraphDev feature parity (visualization, chat agent, GitLab triggers) and is intentionally CLI-first.

---
## 0. Instance Governance

- **Artifact Class:** Executable contract instance (Tier-3 constitutional).
- **Canonical Expansion:** `C-RSP` = **Constitutionally-Regulated Single Pass** only (**INVARIANT_TERM_01**).
- **Schema Authority:** `projects/c-rsp/contract-schema.json` defines core section order; this file remains conformant.

---
## 1. Contract Identity

- **Contract Title:** Establish Structural World-Model Engine (Semantic Graph) for TLC Governance
- **Contract ID:** CRSP-SEMGRAPH-001
- **Version:** v1.0.0-draft
- **Schema Version:** v1.0.0
- **Status:** Draft
- **Adoption Tier:** Tier-3-Constitutional
- **System Role:** Adds a deterministic structural world-model (code units + edges + ripple impact) so TLC governance is not blind to indirect architectural effects.
- **Primary Objective:** Produce schema-valid `ImpactReport` and `ShadowDrift` artifacts, plus a minimal CLI surface, and bind them into TLC’s verification/evidence surfaces.
- **Scope Boundary:** TLC base camp only: new `apps/tlc_semgraph/` skeleton; new schemas under `verification/semgraph/`; new verifier scripts under `scripts/`; optional Guardian read-only hook points only (no behavior change beyond emitting/recording evidence in this contract’s v1).
- **Not Claimed:** No 3D visualization; no Duo/Chat agent; no GitLab/GitHub PR automation; no cross-repo federation; no claim that all TLC sibling repos are graph-parsed; no claim of enforcement halts in `src/guardian.py` unless explicitly implemented and evidenced in a follow-on contract.

---
## 2. Contract Topology + Profile

- **Topology Mode:** TLC-Core
- **Profile Type:** Core
- **Profile Overlay Source:** N/A
- **Verifier Class:** core-verifier
- **Authoritative Truth Surface:**
  - `projects/c-rsp/BUILD_CONTRACT.md`
  - `projects/c-rsp/contract-schema.json`
  - `projects/c-rsp/instances/CRSP-SEMGRAPH-001.md` (this executed instance)
  - `STATUS.json`
  - `verification/` (truth surface outputs produced by this contract)
- **Instance Artifact Path:** `projects/c-rsp/instances/CRSP-SEMGRAPH-001.md`
- **Governance Lock Path:** N/A

### 2A. Profile Merge Rule

Base constitutional template governs this instance. No profile may override canonical C-RSP terminology, section order, truth discipline, halt matrix, or acceptance criteria rigor.

### 2B. Instance Rule

Executable only when: no unresolved placeholders; acceptance criteria are objective; evidence paths are concrete; commands are deterministic and runnable on macOS with the repo’s declared verification dependencies.

---
## 3. Baseline State

- **Existing Repo / System:** `coreyalejandro/the-living-constitution`
- **Baseline Commit / Anchor:** `STATUS.json` verification target (`STATUS.md` mirrors the canonical JSON).
- **Verified Existing Assets:** `src/guardian.py` exists as runtime enforcement surface; `verification/` exists as evidence surface; verifier scripts exist under `scripts/`.
- **Known Constraints:** Evidence-first discipline; `STATUS.json` is authoritative; no claims of safety enforcement without executed verifier evidence.
- **Known Gaps:** No structural world-model engine exists in-repo; no schema-defined `ImpactReport` or `ShadowDrift`; governance domain mapping is manual and not tied to dependency ripple analysis.
- **Legacy Migration Context:** N/A (greenfield subsystem addition within base camp).

---
## 4. Dependencies and Inputs

- **Required Inputs:** This instance file; `projects/c-rsp/*` canonical artifacts; existing TLC repo tree.
- **External Dependencies:** Python 3; repo verification requirements in `requirements-verify.txt`; any additional deps introduced by this contract must be explicitly added with justification.
- **Governance Dependencies:** TLC constitutional articles for V&T discipline (`governance/constitution/core/articles.md`).
- **Forbidden Assumptions:** Do not assume a sibling repo (e.g. PROACTIVE) is available on disk; do not assume tree-sitter tooling is already installed; do not assume TypeScript parsing coverage beyond evidenced results.

### 4A. Cross-Repo Governance Dependency Graph

- **Parent Constitutional Source:** `THE_LIVING_CONSTITUTION.md` and `governance/constitution/core/articles.md`
- **Shared Overlay Profiles:** none
- **Dual-Topology Linked Repos:** none (TLC-Core scope)
- **Satellite Dependents:** none
- **Drift Detection Scope:** Graph snapshot schema stability; schema validation for emitted reports; mismatch between emitted drift severity and STATUS truth anchor not introduced in this contract version.

---
## 5. Risk + Control Classification

- **Risk Class:** Moderate
- **Side-Effect Class:** Internal
- **External Action Scope:** Adds new app skeleton and verification artifacts; does not modify external systems.
- **Stop/Override Required:** Yes
- **Recovery Mode:** Assisted

### 5A. Conditional Stop / Override Rule

Stop if: schemas are ambiguous, unverifiable, or not produced by deterministic commands; new code introduces linter failures; verification scripts cannot be executed locally. Override authority: human repo owner, with rationale recorded in the run outcome.

---
## 6. Execution Model

- **Execution Mode:** Single-pass deterministic build contract
- **Decision Closure Rule:** No open-ended branch points inside executable sections
- **Fallback Rule:** If the intended pilot repo is unavailable, run the P1 spike against a local TLC-contained codebase directory (e.g. `apps/tlc-control-plane/`) and record that limitation explicitly.
- **Generated Artifacts:**
  - `projects/c-rsp/instances/CRSP-SEMGRAPH-001.md` (this file)
  - `verification/semgraph/ImpactReport.schema.json`
  - `verification/semgraph/ShadowDrift.schema.json`
  - `apps/tlc_semgraph/` skeleton with `api/contracts.py`
  - `verification/semgraph/runs/P1-build-<sha>.json` (spike evidence)
  - `scripts/verify_semgraph_integrity.py` (schema validation for produced artifacts)
- **Promotion Target:** Draft → Draft with executed P1 evidence and schema-valid artifacts; enforcement integration (Guardian halt gates) is explicitly deferred to a follow-on contract.

### 6A. Ordered Operations (Blind Man Test)

| **Step ID** | **Actor** | **Action** | **Inputs** | **Outputs** | **Verify** | **If Failure** |
|-------------|-----------|------------|------------|-------------|------------|----------------|
| OP-01 | agent | Create C-RSP instance file | `projects/c-rsp/BUILD_CONTRACT.instance.md` | `projects/c-rsp/instances/CRSP-SEMGRAPH-001.md` | File exists + no placeholders | Halt; revert file |
| OP-02 | agent | Add schemas + skeleton | repo tree | schemas + `apps/tlc_semgraph` | JSON schema parse succeeds | Halt; fix schemas/paths |
| OP-03 | agent | Run P1 spike build | target dir | `verification/semgraph/runs/P1-build-<sha>.json` | script exits 0 + schema-valid run JSON | Halt; record limitation |

### 6B. Halt Conditions (instance-local)

| **Condition** | **Stop Reason** | **Next Action** |
|---------------|-----------------|-----------------|
| Unresolved placeholders | Instance not executable | Fix instantiation; re-run |
| Schema invalid | Evidence artifacts cannot be trusted | Fix schema or output generator |
| Spike cannot run | No evidence possible | Narrow scope, change pilot, or add dependency with proof |

### 6C. Success Conditions

- **Success:** Schemas exist; skeleton exists; at least one spike run JSON exists and validates against a declared schema.
- **Done:** Contract scope satisfied with an outcome report (follow-on report uses `CRSP_OUTCOME_TEMPLATE.md`).

### 6D. Major Component Implementation Snippets

N/A for this contract instance text; implementation snippets live in the created skeleton and verifier scripts.

---
## 7. Lifecycle State Machine

### Allowed States

Draft; Active; Frozen; Superseded

### Transition Rules

- Draft → Active requires: all AC satisfied with executed evidence; verifier scripts runnable; evidence recorded.

### Transition Evidence

`verification/semgraph/runs/` evidence bundle and verifier execution logs.

---
## 8. Invariants

### Required Global Invariants

INVARIANT_TERM_01; INVARIANT_SCHEMA_01; INVARIANT_EXEC_01–05; INVARIANT_CTRL_01; INVARIANT_REC_01

### Profile Invariants

- **INVARIANT_TRUTH_01:** No claim that enforcement exists unless Guardian integration is implemented and verified.
- **INVARIANT_BLIND_01:** Every step references exact paths and pass/fail outputs.

---
## 9. Acceptance Criteria

| ID | Requirement | Verification Method | Pass Condition |
|----|-------------|---------------------|----------------|
| AC-01 | `ImpactReport` schema exists | Read file | `verification/semgraph/ImpactReport.schema.json` exists |
| AC-02 | `ShadowDrift` schema exists | Read file | `verification/semgraph/ShadowDrift.schema.json` exists |
| AC-03 | `tlc-semgraph` skeleton exists | `ls apps/tlc_semgraph` | directory present with `api/contracts.py` |
| AC-04 | Spike run produced | Read run file | `verification/semgraph/runs/P1-build-<sha>.json` exists |
| AC-05 | Spike run validates | `python3 scripts/verify_semgraph_integrity.py --run <path>` | exits 0 |

---
## 10. Rollback & Recovery

- **Safe-State Definition:** No semgraph subsystem present; repo returns to baseline without new directories/files.
- **Rollback Procedure:** Remove newly created semgraph paths and revert any modified files; preserve run artifacts only if they are schema-valid and explicitly referenced.
- **Recovery Authority:** Human repo owner.
- **Rollback Evidence Paths:** Outcome report (if rollback executed) using `CRSP_OUTCOME_TEMPLATE.md`.
- **Partial Execution Handling:** Partial artifacts are non-authoritative; must be marked as partial in outcome V&T.

---
## 11. Evidence + Truth Surface

- **Primary Evidence Paths:**
  - `verification/semgraph/ImpactReport.schema.json`
  - `verification/semgraph/ShadowDrift.schema.json`
  - `verification/semgraph/runs/P1-build-<sha>.json`
- **Generated Reports:** P1 build run JSON; verifier output (terminal logs).
- **Audit Artifacts:** Outcome report per `CRSP_OUTCOME_TEMPLATE.md` (not generated in this contract step).
- **Evidence Boundary:** Evidence applies only to the local pilot directory parsed during P1 spike.

---
## 12. Conflict Matrix

| Conflict Type | Example | Severity | Resolution |
|---------------|---------|----------|------------|
| Scope creep | Attempt to add visualization/agent automation | High | Halt; defer to follow-on contract |
| Truth overreach | Claim Guardian enforcement without evidence | Critical | Halt; correct V&T |
| Non-determinism | Output depends on network without recording inputs | High | Halt; pin inputs or record evidence |

---
## 13. Halt Matrix

Halt on: unresolved placeholders; schema ambiguity; inability to produce spike evidence; verifier script failures; claims exceeding evidence surface.

---
## 14. Preflight

Preflight verifies: no placeholders; schemas exist; skeleton exists; spike run exists; spike run validates.

**Preflight Command(s):**

```bash
python3 scripts/verify_semgraph_integrity.py --self-check
```

---
## 15. Adoption Tiers

Tier 1 — identity + preflight.

Tier 2 — acceptance criteria + rollback + evidence.

Tier 3 — invariants + conflict + halt matrices.

This instance is Tier-3.

---
## 16. Output Format

Mandatory report shape: `projects/c-rsp/CRSP_OUTCOME_TEMPLATE.md`.

V&T constitutional basis: Article I — Right to Truth; Article III — Verification Before Done (`governance/constitution/core/articles.md`).

---
## 17. Instance Declaration

This contract is executable only through this instantiated document: `projects/c-rsp/instances/CRSP-SEMGRAPH-001.md`. Status remains **Draft** until acceptance criteria are satisfied with executed evidence and a corresponding outcome report is written.

