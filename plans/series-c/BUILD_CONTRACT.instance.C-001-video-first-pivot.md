# Build Contract Instance: C-001 Video-First Pivot
## Constitutionally-Regulated Single Pass Instance (Series C)

---
## 0. Template Governance

- **Template Class:** Executable instance derived from C-RSP constitutional master template
- **Canonical Expansion:** Constitutionally-Regulated Single Pass
- **Invalidation Rule:** Any non-canonical C-RSP expansion invalidates this instance
- **Schema Authority:** `projects/c-rsp/contract-schema.json`

### Global Constitutional Invariants

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

---
## 1. Contract Identity

- **Contract Title:** Series C Video-First Pivot
- **Contract ID:** C-001-VIDEO-FIRST-PIVOT
- **Version:** 1.0.0
- **Schema Version:** 1.0.0
- **Status:** Active
- **Adoption Tier:** Tier-2-Operational
- **System Role:** TLC roadmap and governance boundary pivot
- **Primary Objective:** Move post-B007 execution priority to teaser-video-remotion impact while preparing clean extraction of video repos from TLC.
- **Scope Boundary:** Planning and governance artifacts only (no destructive extraction in this instance).
- **Not Claimed:** Standalone repository migration completion, final video quality completion, fellowship acceptance outcome.

---
## 2. Contract Topology + Profile

- **Topology Mode:** TLC-Core
- **Profile Type:** Core
- **Profile Overlay Source:** N/A
- **Verifier Class:** core-verifier
- **Authoritative Truth Surface:** `plans/series-c/*`, `projects/README.md`, `HANDOFF.md`
- **Instance Artifact Path:** `plans/series-c/BUILD_CONTRACT.instance.C-001-video-first-pivot.md`
- **Governance Lock Path:** `governance-template.lock.json`

### 2A. Profile Merge Rule

Base constitutional template governs this instance; no overlay specialization is applied.

### 2B. Instance Rule

This instance is executable for planning and governance updates only because:

1. required sections are fully instantiated
2. no unresolved placeholders remain
3. acceptance criteria are concrete
4. evidence paths are declared
5. preflight commands are declared

---
## 3. Baseline State

- **Existing Repo / System:** `coreyalejandro/the-living-constitution`
- **Baseline Commit / Anchor:** `6805c558d786002129c55289e5cf4287d1c0f539` (B-007 merge)
- **Verified Existing Assets:** Series B contracts `B-001` through `B-007`; `projects/teaser-video-remotion/`; `projects/im-just-a-build/`; `projects/teaser-video/`.
- **Known Constraints:** CI and governance verifiers must remain green; no unverifiable status claims.
- **Known Gaps:** Video extraction is not executed; no standalone repos created in this instance.
- **Legacy Migration Context:** Video folders currently live inside TLC and are coupled to current inventory/status surfaces.

---
## 4. Dependencies and Inputs

- **Required Inputs:** User directive to prioritize video impact and extraction planning; post-B007 clean `main`.
- **External Dependencies:** GitHub repos for future extraction; video production tooling in `projects/teaser-video-remotion`.
- **Governance Dependencies:** `scripts/verify_document_constitution.py`, `HANDOFF.md`, `projects/README.md`.
- **Forbidden Assumptions:** Do not assume extraction completed; do not assume fellowship visibility without distribution work.
- **Dependency Policy:** All dependency assertions must be path-backed in TLC artifacts.

### 4A. Cross-Repo Governance Dependency Graph

- **Parent Constitutional Source:** `THE_LIVING_CONSTITUTION.md`
- **Shared Overlay Profiles:** none
- **Dual-Topology Linked Repos:** none in this instance
- **Satellite Dependents:** planned standalone repos for `im-just-a-build`, `teaser-video`, `teaser-video-remotion`
- **Drift Detection Scope:** series-c plans + projects classification + handoff status text

---
## 5. Risk + Control Classification

- **Risk Class:** Moderate
- **Side-Effect Class:** Internal
- **External Action Scope:** Planning only; no external mutation
- **Stop/Override Required:** No
- **Recovery Mode:** Manual

### 5A. Conditional Stop / Override Rule

Not triggered in this instance because this contract executes documentation and planning updates only.

---
## 6. Execution Model

- **Execution Mode:** Single-pass deterministic contract execution
- **Decision Closure Rule:** Ambiguous extraction states are documented as pending, not implied complete
- **Fallback Rule:** If verifier disagreement occurs, halt and patch artifacts before PR
- **Generated Artifacts:** `plans/series-c/README.md`, `plans/series-c/C-001-*.md`, `plans/series-c/C-002-*.md`, `plans/series-c/C-003-*.md`, `plans/series-c/C-004-*.md`, `plans/series-c/C-010-*.md`
- **Promotion Target:** Merge Series C kickoff planning PR

### 6A. Dual-Topology Rule

Not applicable for this instance.

---
## 7. Lifecycle State Machine

### Allowed States

- Draft
- Active
- Frozen
- Superseded

### Transition Rules

- `Draft → Active`: completed when required sections were instantiated and verification commands passed.
- `Active → Frozen`: requires PR merge and handoff update acknowledging Series C kickoff.
- `Frozen → Superseded`: requires successor Series C instance with explicit replacement note.

### Transition Evidence

- Git commits and PR references for this instance
- Verifier output for documentation constitution checks
- Updated handoff status text

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

- **INVARIANT_SERIESC_01:** Series C kickoff must explicitly prioritize `teaser-video-remotion`.
- **INVARIANT_SERIESC_02:** Planned extraction targets must be named without claiming migration completion.
- **INVARIANT_SERIESC_03:** Handoff status must reflect post-B007 state accurately.

---
## 9. Acceptance Criteria

| ID | Requirement | Verification Method | Pass Condition |
|---|---|---|---|
| AC-01 | Series C roadmap exists | `test -f plans/series-c/README.md` | File exists with C-001..C-004 sequence |
| AC-02 | C-001 executable instance exists | `test -f plans/series-c/BUILD_CONTRACT.instance.C-001-video-first-pivot.md` | File exists and includes sections 0–17 |
| AC-03 | Extraction intent declared | Review `projects/README.md` | Lists three video folders as planned extraction targets |
| AC-04 | Documentation constitution holds | `python3 scripts/verify_document_constitution.py --root .` | Exit code 0 |
| AC-05 | Handoff reflects series transition | Review `HANDOFF.md` | States Series B complete and Series C active |

---
## 10. Rollback & Recovery

- **Safe-State Definition:** Revert Series C planning docs if contradictions or governance drift are detected.
- **Rollback Procedure:** `git revert` Series C kickoff commits on branch before merge.
- **Recovery Authority:** Repository maintainer / human operator.
- **Rollback Evidence Paths:** Git history and PR timeline.
- **Partial Execution Handling:** If only subset of docs updated, block merge until all AC criteria are satisfied.

---
## 11. Evidence + Truth Surface

- **Primary Evidence Paths:** `plans/series-c/*.md`, `projects/README.md`, `HANDOFF.md`
- **Generated Reports:** PR diff and verifier output from `verify_document_constitution.py`
- **Audit Artifacts:** Git commit metadata + PR URL
- **Evidence Boundary:** Planning statements only; no claim of migration completion or final video production quality in this instance.
- **Truth Discipline:** All claims remain bounded to changed files and verifier outputs.

---
## 12. Conflict Matrix

| Conflict Type | Example | Severity | Resolution |
|---|---|---|---|
| Terminology Authority Conflict | Non-canonical C-RSP phrase | Critical | Halt |
| Incomplete Instance Conflict | Missing required section | Critical | Halt |
| Evidence Gap Conflict | Claim extraction completed without migration evidence | High | Block promotion |
| Verifier Scope Conflict | Skip doc constitution check | High | Block promotion |
| Lifecycle Conflict | Mark Frozen before PR merge | High | Block promotion |

---
## 13. Halt Matrix

Halt execution if:

- required section is missing
- unresolved placeholders remain
- extraction completion is claimed without evidence
- `verify_document_constitution.py` fails
- handoff status conflicts with merged-series reality

---
## 14. Preflight

Preflight checks:

- instance file exists and is fully instantiated
- series-c roadmap files exist
- extraction targets are declared as planned, not completed
- handoff series status is coherent
- documentation constitution verification passes

**Preflight Command(s):**

- `python3 scripts/verify_document_constitution.py --root .`
- `git status -sb`

---
## 15. Adoption Tiers

### Tier 1 — Minimum Viable Governance
- identity, topology, terminology, and instantiated artifact present

### Tier 2 — Operational
- acceptance criteria, risk classification, verifier command, and rollback semantics present

### Tier 3 — Constitutional
- deferred to later Series C instances with extraction execution and enterprise hardening

---
## 16. Output Format

Execution summaries must end with:

- **Exists**
- **Non-existent**
- **Unverified**
- **Functional status**

No stronger claim may be made outside that truth surface.

---
## 17. Instance Declaration

This document is the executable instance artifact for C-001:

`plans/series-c/BUILD_CONTRACT.instance.C-001-video-first-pivot.md`
