# BUILD CONTRACT INSTANCE
## Constitutionally-Regulated Single Pass Executable Prompt

> **Instance Status:** Draft. Standalone path is **RESOLVED** to `projects/backboardai-fde/` (see `evidence/fde-control-plane/standalone-path-resolution.json`). Promotion to Active remains blocked until lifecycle/preflight gates for **Active** are satisfied (this contract does not claim Active). All verification steps are runnable via `./scripts/run_fde_control_plane_verification.sh`.

---
## 0. Instance Governance

- **Artifact Class:** Executable contract instance (Tier-3 constitutional).
- **Canonical Expansion:** `C-RSP` = **Constitutionally-Regulated Single Pass** only (**INVARIANT_TERM_01**).
- **Schema Authority:** `projects/c-rsp/contract-schema.json` defines core section order; this file remains conformant.
- **Profile Merge:** Dual-topology specialization is limited to approved schema slots (see master `BUILD_CONTRACT.md` §2A).

---
## 1. Contract Identity

- **Contract Title:** Close Remaining Constitutional Gaps for FDE Control Plane Draft
- **Contract ID:** CRSP-FDE-CTRL-PLANE-GAPS-002
- **Version:** v1.0.0-draft
- **Schema Version:** v2.1.0
- **Status:** Draft
- **Adoption Tier:** Tier-3-Constitutional
- **System Role:** Constitutional remediation contract for the FDE control plane artifact set to resolve dual-topology incompleteness, verifier-class alignment drift, and missing automated verification required for stronger promotion readiness.
- **Primary Objective:** Produce the governance, path, verifier, and automation artifacts necessary to close the remaining constitutional gaps in the existing FDE control plane Draft so that the artifact set can advance from structurally authored Draft toward promotion-ready Draft with executed verification evidence.
- **Scope Boundary:** This contract governs only the gap-closure step for the existing FDE control plane Draft artifact set: resolve the standalone twin path, align governance lock and verifier scope to dual-topology-verifier, create and execute automated structural/schema/verifier checks, and update truth-surface evidence accordingly.
- **Not Claimed:** This contract does not claim runtime Backboard deployment, live FDE control plane operation, application-feature delivery, production CI success, or Active promotion. It does not claim that the standalone twin repo already exists unless resolved during execution.

---
## 2. Contract Topology + Profile

- **Topology Mode:** Dual-Topology
- **Profile Type:** Dual-Topology
- **Profile Overlay Source:** N/A
- **Verifier Class:** dual-topology-verifier
- **Authoritative Truth Surface:**
  - `projects/c-rsp/BUILD_CONTRACT.md`
  - `projects/c-rsp/BUILD_CONTRACT.instance.md` (guided instance template — workflow only)
  - `projects/c-rsp/instances/CRSP-FDE-CTRL-PLANE-GAPS-002.md` (this executed instance)
  - `projects/c-rsp/NEXT_CRSP_BUILD.json`
  - `projects/c-rsp/governance-template.lock.json`
  - `docs/fde-control-plane/Refactored-FDE-Control-Plane-Plan.md`
  - `docs/fde-control-plane/BUILD_TO_OPERATE_LIFECYCLE_SPEC.md`
  - `governance-rules/fde-lifecycle-invariants.yaml`
  - `schemas/fde-lifecycle.schema.json`
  - `schemas/blind-man-execution.schema.json`
  - `evidence/fde-control-plane/contract-refactor-evidence.json`
  - `evidence/fde-control-plane/preflight-report.json`
  - `evidence/fde-control-plane/lifecycle-transition-contract-record.json`
  - `evidence/fde-control-plane/rollback-report.json`
  - `evidence/fde-control-plane/failure-audit.json`
  - `evidence/fde-control-plane/structural-diff-report.json`
  - `evidence/fde-control-plane/schema-validation-report.json`
  - `evidence/fde-control-plane/verifier-execution-report.json`
  - `evidence/fde-control-plane/standalone-path-resolution.json`
  - `STATUS.json`
- **Instance Artifact Path:** `projects/c-rsp/instances/CRSP-FDE-CTRL-PLANE-GAPS-002.md`
- **Governance Lock Path:** `projects/c-rsp/governance-template.lock.json`

### 2A. Profile Merge Rule

Base constitutional template governs this instance. Overlay profiles may not override canonical C-RSP terminology, invalidation rules, conflict severity, acceptance criteria, preflight, truth discipline, halt matrix, or core section order.

### 2B. Instance Rule

Executable only when: base template fields instantiated; dual-topology fields instantiated or marked `UNRESOLVED REQUIRED INPUT`; acceptance criteria objective; generated artifacts and evidence paths declared; preflight passes; schema validation passes; lifecycle guards satisfied.

---
## 3. Baseline State

- **Existing Repo / System:** `coreyalejandro/the-living-constitution`
- **Baseline Commit / Anchor:** `32acf248b0cfd9fd87436f5b327b26cf100a9a45`
- **Verified Existing Assets:** Prior instance `CRSP-FDE-CTRL-PLANE-LIFECYCLE-001` artifacts: `docs/fde-control-plane/`, `governance-rules/fde-lifecycle-invariants.yaml`, `schemas/fde-lifecycle.schema.json`, `schemas/blind-man-execution.schema.json`, `evidence/fde-control-plane/` JSON set, `projects/c-rsp/NEXT_CRSP_BUILD.json`.
- **Known Constraints:** Canonical section order preserved; Blind Man’s Rule binding; automated verification must be evidenced, not assumed.
- **Known Gaps (pre-gap-closure):** (Historical) satellite lock, unresolved standalone path, no executed reports — **remediated** by CRSP-FDE-CTRL-PLANE-GAPS-002 execution; see current evidence JSON under `evidence/fde-control-plane/`.
- **Legacy Migration Context:** Existing FDE control plane work is already authored as a Draft artifact set. This contract is remediation, not greenfield.

---
## 4. Dependencies and Inputs

- **Required Inputs:** `projects/c-rsp/BUILD_CONTRACT.md` (canonical master template); `projects/c-rsp/BUILD_CONTRACT.instance.md` (guided instance template); this file `projects/c-rsp/instances/CRSP-FDE-CTRL-PLANE-GAPS-002.md` (executed instance); FDE Draft artifact set under `docs/fde-control-plane/`, `governance-rules/`, `schemas/`, `evidence/fde-control-plane/`; repo root `STATUS.json`; explicit standalone twin repo path when available.
- **External Dependencies:** Git; Python 3; `jsonschema` (see `requirements-verify.txt`); POSIX shell; CI or local runner for scripts.
- **Governance Dependencies:** `projects/c-rsp/governance-template.lock.json`; `projects/c-rsp/NEXT_CRSP_BUILD.json`; `governance-rules/fde-lifecycle-invariants.yaml`; schemas listed in Section 2.
- **Forbidden Assumptions:** Do not assume standalone twin path; do not assume lock already aligned; do not assume grep/json.load alone satisfies promotion readiness; do not assume CI wiring exists unless created by this contract.

### 4A. Cross-Repo Governance Dependency Graph

- **Parent Constitutional Source:** `projects/c-rsp/BUILD_CONTRACT.md`
- **Shared Overlay Profiles:** none
- **Dual-Topology Linked Repos:**
  - Integrated: `the-living-constitution/projects/c-rsp/`, `the-living-constitution/docs/fde-control-plane/`, `the-living-constitution/governance-rules/`, `the-living-constitution/schemas/`, `the-living-constitution/evidence/fde-control-plane/`
  - Standalone: `the-living-constitution/projects/backboardai-fde/` (evidenced: `evidence/fde-control-plane/standalone-path-resolution.json`; twin contract file `projects/backboardai-fde/BUILD_CONTRACT`)
- **Satellite Dependents:** none
- **Drift Detection Scope:** Canonical master vs executed instance section order; guided template vs filled instance; lock vs verifier class; integrated vs standalone artifact sets; evidence vs executed results; `NEXT_CRSP_BUILD.json` vs actual blockers.

---
## 5. Risk + Control Classification

- **Risk Class:** High
- **Side-Effect Class:** Internal
- **External Action Scope:** May create or update governance artifacts, lock files, scripts, CI workflows, evidence reports, and dual-topology path records affecting future promotion decisions.
- **Stop/Override Required:** Yes
- **Recovery Mode:** Assisted

### 5A. Conditional Stop / Override Rule

**Stop authority:** human repo owner; designated constitutional maintainer; verifier scripts on structural/schema/verifier failure.

**Override authority:** human repo owner only, with rationale in `evidence/fde-control-plane/failure-audit.json`.

**Safe-state rule:** Last known schema-valid Draft remains authoritative; no updated lock, script, workflow, or evidence file counts as promotion evidence unless execution completes with PASS; unresolved standalone path stays explicit until resolved.

---
## 6. Execution Model

- **Execution Mode:** Single-pass deterministic build contract
- **Decision Closure Rule:** No open-ended branch points inside executable sections
- **Fallback Rule:** Unresolved ambiguity triggers halt or explicit escalation
- **Generated Artifacts:**
  - `projects/c-rsp/instances/CRSP-FDE-CTRL-PLANE-GAPS-002.md` (this file)
  - `projects/c-rsp/governance-template.lock.json`
  - `projects/c-rsp/NEXT_CRSP_BUILD.json`
  - `scripts/run_fde_control_plane_verification.sh` (orchestrates resolve + structural + schema + promotion)
  - `scripts/mirror_fde_artifacts.sh` (optional: sync integrated FDE docs/evidence/schemas into `projects/backboardai-fde/`; dry-run default, `--apply` writes)
  - `scripts/verify_crsp_structure.py`
  - `scripts/verify_fde_control_plane.py`
  - `scripts/resolve_fde_standalone_path.sh`
  - `.github/workflows/fde-control-plane-verify.yml`
  - `evidence/fde-control-plane/structural-diff-report.json`
  - `evidence/fde-control-plane/schema-validation-report.json`
  - `evidence/fde-control-plane/verifier-execution-report.json`
  - `evidence/fde-control-plane/standalone-path-resolution.json`
  - `evidence/fde-control-plane/blind-man-step-sample.json`
  - `evidence/fde-control-plane/preflight-report.json` (updated)
  - `evidence/fde-control-plane/contract-refactor-evidence.json` (updated)
- **Promotion Target:** Promotion-ready Draft with dual-topology path resolved or deterministically re-blocked with evidence, lock aligned to dual-topology-verifier, and automated verification reports executed with PASS.

### 6A. Dual-Topology Rule

- **Integrated path:** `the-living-constitution/projects/c-rsp/`, `docs/fde-control-plane/`, `governance-rules/`, `schemas/`, `evidence/fde-control-plane/`.
- **Standalone path:** **RESOLVED** — `projects/backboardai-fde/` (see `evidence/fde-control-plane/standalone-path-resolution.json`). Re-run `./scripts/run_fde_control_plane_verification.sh` after changing twin `BUILD_CONTRACT` or integrated FDE artifacts so evidence stays current.

### Blind Man’s Rule (binding)

Every instruction must name exact paths, artifacts, and pass/fail conditions; no visual inference or omitted navigation (**INVARIANT_BLIND_01**).

---
## 7. Lifecycle State Machine

### Allowed States

Draft; Active; Frozen; Superseded

### Transition Rules

- **Draft → Active** requires: no stray placeholders except explicit `UNRESOLVED REQUIRED INPUT`; schema validation pass; preflight pass; dual-topology path resolved or explicitly blocked with evidence; lock and instance aligned to dual-topology-verifier; structural/schema/verifier reports PASS.
- **Active → Frozen:** acceptance criteria satisfied; evidence recorded; promotion rules satisfied.
- **Frozen → Superseded:** successor instance references superseded contract.
- Invalid transitions halt and record audit.

### Transition Evidence

Lifecycle record; preflight; truth-surface links; standalone path-resolution report; lock alignment; structural/schema/verifier execution reports.

---
## 8. Invariants

### Required Global Invariants

INVARIANT_TERM_01; INVARIANT_SCHEMA_01; INVARIANT_EXEC_01–05; INVARIANT_CTRL_01; INVARIANT_LIFE_01; INVARIANT_REC_01

### Profile invariants

- **INVARIANT_DUAL_01–03:** Dual-Topology paths explicit or `UNRESOLVED REQUIRED INPUT`; no false completion; resolution evidenced.
- **INVARIANT_VERIFIER_01–02:** Lock and instance name `dual-topology-verifier` consistently with verifier execution report.
- **INVARIANT_VERIFY_01–03:** Structural diff, schema validation, and verifier execution are all required promotion evidence classes; failures block promotion.
- **INVARIANT_TRUTH_01:** Claims do not exceed executed reports.
- **INVARIANT_BLIND_01:** Path resolution, lock alignment, and verification satisfy Blind Man’s Rule.
- **INVARIANT_NEXT_01:** `NEXT_CRSP_BUILD.json` reflects actual remaining work.

---
## 9. Acceptance Criteria

| ID | Requirement | Verification Method | Pass Condition |
|----|-------------|---------------------|----------------|
| AC-01 | Standalone twin path resolved or re-blocked | `evidence/fde-control-plane/standalone-path-resolution.json` | One exact path or `UNRESOLVED REQUIRED INPUT` with rationale |
| AC-02 | Governance lock aligns to dual-topology-verifier | compare lock, instance, verifier report | All name `dual-topology-verifier` |
| AC-03 | Canonical structural diff automated | `scripts/verify_crsp_structure.py` | `structural-diff-report.json` PASS |
| AC-04 | Schema validation automated | `scripts/verify_fde_control_plane.py` | `schema-validation-report.json` PASS |
| AC-05 | Promotion-readiness verifier automated | `scripts/verify_fde_control_plane.py --promotion-readiness` | `verifier-execution-report.json` PASS |
| AC-06 | Preflight references executed results | `preflight-report.json` | Lists executed reports |
| AC-07 | `NEXT_CRSP_BUILD.json` accurate | file review | Pending work only |
| AC-08 | Instance claims match evidence | compare instance vs reports | No stronger claim than evidence |
| AC-09 | Rollback path ready | `rollback-report.json` | Procedure executable |
| AC-10 | Draft unless all blockers closed | instance status + reports | Remains Draft until AC-01–09 pass for Active |

---
## 10. Rollback & Recovery

- **Safe-State Definition:** Schema-valid Draft at baseline `32acf248b0cfd9fd87436f5b327b26cf100a9a45` if path-resolution, lock alignment, or verification fails.
- **Rollback Procedure:** Stop on first failed check; do not promote; restore prior `projects/c-rsp/instances/CRSP-FDE-CTRL-PLANE-GAPS-002.md`, `governance-template.lock.json`, `NEXT_CRSP_BUILD.json`; preserve failed reports; write `failure-audit.json` and `rollback-report.json`.
- **Recovery Authority:** Human repo owner or designated constitutional maintainer.
- **Rollback Evidence Paths:** `evidence/fde-control-plane/rollback-report.json`, `evidence/fde-control-plane/failure-audit.json`
- **Partial Execution Handling:** Partial artifacts are non-authoritative until AC for stronger readiness pass.

---
## 11. Evidence + Truth Surface

- **Primary Evidence Paths:** `evidence/fde-control-plane/standalone-path-resolution.json`, `structural-diff-report.json`, `schema-validation-report.json`, `verifier-execution-report.json`, `preflight-report.json`, `contract-refactor-evidence.json`, `rollback-report.json`, `failure-audit.json`
- **Generated Reports:** As listed in Section 6.
- **Audit Artifacts:** Lifecycle transition record; failure audit; rollback report when applicable.
- **Evidence Boundary:** Does not include runtime Backboard or external sync unless separately evidenced.
- **Truth Discipline:** Claims may not exceed evidence on the truth surface.

---
## 12. Conflict Matrix

| Conflict Type | Example | Severity | Resolution |
|---------------|---------|----------|------------|
| Terminology Authority Conflict | Non-canonical C-RSP expansion | Critical | Halt |
| Profile Drift Conflict | Lock contradicts dual-topology | Critical | Halt |
| Topology Misclassification | Dual work treated as core-only | Critical | Halt |
| Incomplete Instance Conflict | Missing gap-closure fields | Critical | Halt |
| Evidence Gap Conflict | Verification without executed report | High | Block promotion |
| Verifier Scope Conflict | Lock names non-dual verifier | High | Block promotion |
| Schema Drift Conflict | Section order drift | Critical | Halt |
| Lifecycle Conflict | Stronger status without PASS reports | High | Block promotion |
| Recovery Conflict | Rollback not executable | High | Block promotion |

---
## 13. Halt Matrix

Halt on: stray placeholders; missing overlay; topology contradiction; terminology drift; verifier/topology mismatch; missing AC; preflight fail; missing truth surface; schema failure; illegal lifecycle; missing Tier-2+ rollback; promotion attempted with unresolved standalone path; lock misalignment; missing structural/schema/verifier reports.

---
## 14. Preflight

Preflight verifies: placeholders; terminology; topology; profile; verifier; instance exists; evidence paths; AC table; schema validation; lifecycle; risk/control; standalone path step; lock alignment step; automated structural/schema/verifier steps declared.

**Preflight Command(s):**

```bash
./scripts/run_fde_control_plane_verification.sh
```

Equivalent granular commands (same order as the bundle: resolve, structural, schema, promotion) remain documented in `scripts/run_fde_control_plane_verification.sh` and `projects/c-rsp/governance-template.lock.json`. Use `./scripts/run_fde_control_plane_verification.sh --skip-resolve` only when `standalone-path-resolution.json` is unchanged and you need a faster structural/schema/promotion pass.

**Recorded result:** `evidence/fde-control-plane/preflight-report.json`

---
## 15. Adoption Tiers

Tier 1 — identity, topology, terminology, placeholder discipline, schema-valid structure.

Tier 2 — Tier 1 + AC, risk/control, CI verifier integration, rollback/recovery, lifecycle evidence.

Tier 3 — Tier 2 + full invariant registry, dual-topology, governance lockfiles, evidence ledger, audit-grade promotion.

This instance is Tier-3.

---
## 16. Output Format

Mandatory report shape: `projects/c-rsp/CRSP_OUTCOME_TEMPLATE.md` — title block first, then Kanban, then constitutional anchor, then V&T Statement.

**V&T constitutional basis:** Article I — Right to Truth; Article III — Verification Before Done (`00-constitution/articles.md`).

Execution summaries close with: Exists; Verified against; Not claimed; Non-existent; Unverified; Functional status.

**Follow-on C-RSP build:** If standalone path remains unresolved, record in `projects/c-rsp/NEXT_CRSP_BUILD.json` with `status: pending`.

---
## 17. Instance Declaration

This framework is executable only through this instantiated document: `projects/c-rsp/instances/CRSP-FDE-CTRL-PLANE-GAPS-002.md`. Status remains **Draft** until all promotion guards and evidence for Active status are satisfied.
