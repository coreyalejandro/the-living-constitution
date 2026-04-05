# 📜 C-RSP Build Contract Instance
## Constitutionally-Regulated Single Pass Executable Prompt (Framework)

> **Instance Status:** Executable Tier-2 Operational — MVP documentation system closeout for TLC-Core. **Template authority:** `projects/c-rsp/BUILD_CONTRACT.md` (canonical section order preserved).

---

## 0. Template Governance

- **Template Class:** Constitutional master template (instantiated)
- **Canonical Expansion:** Constitutionally-Regulated Single Pass
- **Invalidation Rule:** Any alternate expansion of C-RSP is governance drift and invalidates the contract instance.
- **Instance Requirement:** This file is the executable instance for contract ID `tlc-docsys-mvp-closeout-001`.
- **Schema Authority:** `projects/c-rsp/contract-schema.json` is the canonical machine-readable definition of contract shape.

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

- **Contract Title:** TLC MVP Documentation System Closeout
- **Contract ID:** tlc-docsys-mvp-closeout-001
- **Version:** 1.0.0
- **Schema Version:** 1.0.0 (field `schema_version` in `projects/c-rsp/contract-schema.json`)
- **Status:** Active
- **Adoption Tier:** Tier-2-Operational
- **System Role:** Close all remaining gaps so the MVP documentation governance system declared in `config/docs_governance.json` is complete, verified, and evidenced; execution MUST continue under **CONTROL_RULE_KBC_01**, **CONTROL_RULE_DNSW_01** (`projects/document-system/BUILD_CONTRACT.instance.md`), and **CONTROL_RULE_VT_RIGOR_01** (`projects/c-rsp/BUILD_CONTRACT.md` Section 16) until acceptance criteria pass or a formal halt is recorded—no terminal “done” while Kanban cards for this contract remain open.
- **Primary Objective:** Bring the MVP documentation system to **complete** status: all MVDS and contract-declared closeout items implemented, verifiers green where required by acceptance criteria, evidence updated, `HANDOFF.md` §2 TODO cleared or formally waived with evidence, and automation-oriented work continued until the board is clear for this instance.
- **Scope Boundary:** Repository `coreyalejandro/the-living-constitution` only — `docs/`, `governance/`, `scripts/` (documentation tooling), `config/docs_governance.json`, `.github/workflows/verify.yml` (documentation job only unless coordinated), `projects/governance/registry.json`, `verification/docs_compliance.json`, `schemas/` (if added). No satellite product repos; no submodule content changes except where required to pass existing TLC verifiers already bound to this repo.
- **Not Claimed:** That downstream satellite repos inherit this MVP in this pass; that remote GitHub Actions has run at a specific run id unless recorded; that every historical markdown file without frontmatter is migrated; that “automatic” execution implies unattended access to GitHub secrets or external systems not available to the executor.

---

## 2. Contract Topology + Profile

- **Topology Mode:** TLC-Core
- **Profile Type:** Core
- **Profile Overlay Source:** N/A (not Satellite; no PASS8 overlay merge for this instance)
- **Verifier Class:** core-verifier
- **Authoritative Truth Surface:** `config/docs_governance.json`, `docs/constitution/DOCUMENTATION_STANDARD.md`, `docs/constitution/CANONICAL_PATHS.md`, `docs/constitution/ROOT_DOC_ALLOWLIST.md`, `docs/constitution/DOC_TRUTH_HIERARCHY.md`, `docs/constitution/TERMINOLOGY.md`, `governance/BUILD_CONTRACT.instance.md`, `governance/governance-template.lock.json`, `governance/GOVERNANCE_BINDING.md`, `scripts/verify_document_constitution.py`, `scripts/compliance_score_docs.py`, `verification/docs_compliance.json` (when generated), `HANDOFF.md` §1 Deliverables / §2 TODO, `projects/c-rsp/BUILD_CONTRACT.md`, `projects/c-rsp/CRSP_OUTCOME_TEMPLATE.md`, prior instance `projects/document-system/BUILD_CONTRACT.instance.md` (KBC/DNSW/VT cross-refs)
- **Instance Artifact Path:** `projects/document-system/BUILD_CONTRACT.instance.MVP-CLOSEOUT-001.md`
- **Governance Lock Path:** `governance/governance-template.lock.json` (repo root) and `projects/c-rsp/governance-template.lock.json` (reference)

### 2A. Profile Merge Rule

The base constitutional template governs all contract instances. This instance uses **Core** profile only; no Satellite PASS8 overlay fields are merged unless explicitly added by amendment.

### 2B. Instance Rule

A contract is executable only when all of the following exist:

1. base template fields are fully instantiated in this file
2. referenced overlay profile fields are N/A or fully instantiated
3. unresolved placeholders are absent (except `UNRESOLVED REQUIRED INPUT` — none at issuance)
4. acceptance criteria are concrete
5. generated artifacts and evidence paths are declared
6. preflight passes
7. schema validation passes (manual or scripted per preflight)
8. lifecycle state transition guards are satisfied

---

## 3. Baseline State

- **Existing Repo / System:** `the-living-constitution` (TLC governance overlay)
- **Baseline Commit / Anchor:** `e16c574f58adc4f7f74ebc49682eee2402d4b5d9` (short: `e16c574`)
- **Verified Existing Assets:** MVDS paths from `config/docs_governance.json`; `scripts/verify_document_constitution.py`; `scripts/compliance_score_docs.py`; `scripts/docs/tlc-gen.py`; `scripts/migrate_docs_legacy.py`; CI steps for doc verification in `.github/workflows/verify.yml`; `projects/governance/registry.json`; `HANDOFF.md` §1 Deliverables table; `HANDOFF.md` §2 TODO (open items listed there)
- **Known Constraints:** Remote CI requires push + GitHub; `verify_governance_chain.py` needs `pip install -r requirements-verify.txt` and successful `./scripts/bootstrap_repo.sh` for full pass; submodules may need `SUBMODULES_PAT` in CI; executor may be multi-session—continuation is via Kanban + KBC, not a single chat turn
- **Known Gaps:** Items in `HANDOFF.md` §2 TODO: full governance chain + remote CI proof; `--apply` migration; JSON Schema for frontmatter; external compliance badge URL
- **Legacy Migration Context:** `scripts/migrate_docs_legacy.py` produces `verification/docs_migration_report.json`; full `git mv` normalization may remain partial unless AC satisfied

---

## 4. Dependencies and Inputs

- **Required Inputs:** Git workspace at baseline or later; Python 3.12+; `requirements-verify.txt` installed; read access to paths in §2 Authoritative Truth Surface; ability to edit and commit files in this repo
- **External Dependencies:** GitHub Actions for remote verification (optional for local-only work but required for AC rows that demand CI green); npm/Node only if a badge or script requires it — **UNRESOLVED REQUIRED INPUT** if badge uses a third-party badge API URL you must supply
- **Governance Dependencies:** Prior work under `tlc-docsys-constitutionalization-001` (`projects/document-system/BUILD_CONTRACT.instance.md`); master template `projects/c-rsp/BUILD_CONTRACT.md`; outcome template `projects/c-rsp/CRSP_OUTCOME_TEMPLATE.md`
- **Forbidden Assumptions:** That MVP is complete without verifier exit codes; that “automatic” means infinite loop without state change (forbidden by DNSW); that another BUILD_CONTRACT instance is active concurrently (forbidden by KBC)
- **Dependency Policy:** All dependencies explicitly named above; no implicit registry of satellite repos for this pass

### 4A. Cross-Repo Governance Dependency Graph

- **Parent Constitutional Source:** `THE_LIVING_CONSTITUTION.md`, `docs/constitution/DOCUMENTATION_STANDARD.md`
- **Shared Overlay Profiles:** none for this Core instance
- **Dual-Topology Linked Repos:** none
- **Satellite Dependents:** none
- **Drift Detection Scope:** N/A for this closeout pass (TLC-Core only)

---

## 5. Risk + Control Classification

- **Risk Class:** Moderate
- **Side-Effect Class:** Internal (repo file edits, CI YAML, generated JSON)
- **External Action Scope:** Git push, GitHub Actions runs, optional PR — no production deployment
- **Stop/Override Required:** Yes
- **Recovery Mode:** Assisted

### 5A. Conditional Stop / Override Rule

Stop/override semantics apply (Tier-2, meaningful repo mutation). Safe-state and rollback are defined in §10.

---

## 6. Execution Model

- **Execution Mode:** Single-pass deterministic build contract (execution may span multiple agent sessions; each session advances Kanban until clear or halt)
- **Decision Closure Rule:** No open-ended branch points — each AC maps to a verifier or explicit waiver artifact
- **Fallback Rule:** Any ambiguity triggers halt and `verification/docs_constitution_failure.json` or governance run JSON review
- **Generated Artifacts:**
  - `verification/docs_compliance.json` (refreshed)
  - `verification/docs_migration_report.json` (if migration runs)
  - `schemas/docs_frontmatter_full.json` and `schemas/docs_frontmatter_minimal.json` (if AC for JSON Schema is met)
  - `HANDOFF.md` updated §2 TODO (cleared or waived rows)
  - Optional: `verification/mvp-closeout-evidence.md` summarizing commands and SHAs
- **Promotion Target:** MVP documentation system **complete** per AC table; instance may transition Draft→Active→Frozen per §7 when evidence attaches

### 6A. Dual-Topology Rule

**N/A** — Topology Mode is TLC-Core, not Dual-Topology.

---

## 7. Lifecycle State Machine

### Allowed States

- **Draft**
- **Active**
- **Frozen**
- **Superseded**

### Transition Rules

- `Draft → Active` requires: this instance free of placeholders, preflight pass, AC table complete
- `Active → Frozen` requires: all AC pass or formal halt with evidence
- `Frozen → Superseded` requires: successor instance path if any
- any invalid transition halts and records an audit event

### Transition Evidence

Each transition must emit or update: commit SHA, `verification/docs_compliance.json` or governance run artifact, and pointer in `HANDOFF.md` or `docs/evidence/EVIDENCE_MAP.md`

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

- **INVARIANT_DOC_MVDS_01:** Every path in `mvds_paths` in `config/docs_governance.json` exists as a file at repo root when this instance closes Active→Frozen.
- **INVARIANT_DOC_VERIFIER_01:** `python3 scripts/verify_document_constitution.py --root .` exits 0 before Frozen.
- **INVARIANT_KBC_OUTCOME_01:** Session outcome reports for this work use `CRSP_OUTCOME_TEMPLATE.md` with Kanban first in §2 V&T and satisfy **CONTROL_RULE_VT_RIGOR_01**.
- **INVARIANT_NO_STOP_OPEN_KANBAN_01:** No promotion to Frozen while HANDOFF §2 TODO rows remain open without waiver artifact signed in `docs/evidence/verification/` (markdown record naming waived AC id and reason).

---

## 9. Acceptance Criteria

| ID | Requirement | Verification Method | Pass Condition |
|---|---|---|---|
| AC-01 | MVDS paths all present | `python3 scripts/compliance_score_docs.py --root . --json-out verification/docs_compliance.json` | `missing_mvds` is empty array |
| AC-02 | Doc constitution verifier passes | `python3 scripts/verify_document_constitution.py --root .` | Exit code 0; stdout contains `DOCUMENT_CONSTITUTION_OK` |
| AC-03 | Full governance chain passes locally | `./scripts/bootstrap_repo.sh` then `pip install -r requirements-verify.txt` then `python3 scripts/verify_governance_chain.py --root .` | Exit code 0 |
| AC-04 | Project topology + governance passes | `python3 scripts/verify_project_topology.py --root . --with-governance` | Exit code 0 |
| AC-05 | Remote CI green | Push to branch; GitHub Actions `Verify Living Constitution` workflow | Workflow success on latest commit for this change (screenshot or run URL in evidence file) |
| AC-06 | JSON Schema for governed frontmatter | Files `schemas/docs_frontmatter_full.json` and `schemas/docs_frontmatter_minimal.json` exist; `scripts/verify_document_constitution.py` validates YAML against them OR helper script | Exit 0; schema validation errors fail verifier |
| AC-07 | Migration `--apply` OR formal waiver | Either `scripts/migrate_docs_legacy.py --apply` performs documented moves with report update, OR `docs/evidence/verification/WAIVER-MVP-AC07.md` states waiver | Waiver lists AC-07 and maintainer sign-off line |
| AC-08 | External compliance badge | README or `HANDOFF.md` contains badge URL OR `docs/evidence/verification/WAIVER-MVP-AC08.md` waives pending badge URL | **UNRESOLVED REQUIRED INPUT:** exact shields.io or CI badge URL if not waived |
| AC-09 | HANDOFF §2 TODO cleared | Edit `HANDOFF.md` — each row resolved or linked to waiver | No unresolved TODO rows without waiver path |
| AC-10 | Registry updated | `projects/governance/registry.json` reflects `mvds_status` complete and compliance path | JSON validates; fields consistent with `verification/docs_compliance.json` |

---

## 10. Rollback & Recovery

- **Safe-State Definition:** Last green commit on branch before this instance’s bulk edits; working tree clean or stashed; `verify_document_constitution.py` exit 0 at safe-state tag
- **Rollback Procedure:** `git revert` or `git reset --hard` to safe SHA; re-run `pip install -r requirements-verify.txt`; run AC-02 verifier
- **Recovery Authority:** Repository maintainer; agents execute under maintainer-approved branch
- **Rollback Evidence Paths:** Git reflog; `docs/operations/ROLLBACK.md`; optional `verification/mvp-closeout-rollback-notes.md`
- **Partial Execution Handling:** If AC-03 fails mid-run, fix governance inputs before continuing; do not declare Frozen; record failure JSON from `verification/runs/*-governance.json`

---

## 11. Evidence + Truth Surface

- **Primary Evidence Paths:** `verification/docs_compliance.json`, `verification/docs_constitution_failure.json` (absent on success), `verification/runs/*.json`, `docs/evidence/EVIDENCE_MAP.md`, `docs/evidence/verification/` (smoke + waivers)
- **Generated Reports:** `verification/docs_migration_report.json`, compliance JSON, optional `verification/mvp-closeout-evidence.md`
- **Audit Artifacts:** Git commit SHAs; GitHub Actions run id; `MASTER_PROJECT_INVENTORY.json` unchanged unless in scope
- **Evidence Boundary:** Claims in this instance may not exceed files and command outputs listed; remote CI must be cited by run URL or id
- **Truth Discipline:** Frozen promotion requires AC table satisfied or halt artifact with named condition

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

- unresolved placeholders remain (including **UNRESOLVED REQUIRED INPUT** for AC-08 if neither badge nor waiver is provided)
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
- operator declares halt with evidence file in `docs/evidence/verification/HALT-mvp-closeout.md`

---

## 14. Preflight

Preflight must verify at minimum:

- no unresolved placeholders in this instance file (except AC-08 badge URL marked **UNRESOLVED REQUIRED INPUT** until you supply URL or waiver)
- canonical terminology only
- topology mode present: TLC-Core
- profile type present: Core
- verifier class present: core-verifier
- instance artifact exists: this file
- required evidence paths exist or are creatable
- acceptance criteria table is complete
- schema validation passes (when schemas added)
- lifecycle declaration is valid
- risk/control block is present

**Preflight Command(s):**

```bash
python3 scripts/verify_document_constitution.py --root .
python3 scripts/compliance_score_docs.py --root .
```

---

## 15. Adoption Tiers

### Tier 1 — Minimum Viable Governance

Satisfied by identity, topology, terminology, this instance artifact.

### Tier 2 — Operational

**This instance is Tier-2** — requires acceptance criteria, risk/control, CI integration, rollback, lifecycle evidence.

### Tier 3 — Constitutional

Not required for this MVP closeout unless explicitly expanded.

---

## 16. Output Format

Execution summaries for this contract MUST use `projects/c-rsp/CRSP_OUTCOME_TEMPLATE.md` — **Kanban-first §2 V&T**, **CONTROL_RULE_VT_RIGOR_01** substantive bullets, **CONTROL_RULE_KBC_01** (no done while board open). Follow-on: `projects/c-rsp/NEXT_CRSP_BUILD.json` only after this instance is clear.

---

## 17. Instance Declaration

This framework is instantiated by this file at:

`projects/document-system/BUILD_CONTRACT.instance.MVP-CLOSEOUT-001.md`

Canonical governing template: `projects/c-rsp/BUILD_CONTRACT.md`.

---

## Resolved preamble (per authoring requirements)

| Field | Value |
|---|---|
| **Exact objective** | Close MVP documentation system gaps per AC table; continue work until Kanban clear or formal halt |
| **System/repo** | `coreyalejandro/the-living-constitution` |
| **Topology mode** | TLC-Core |
| **Profile type** | Core |
| **Verifier class** | core-verifier |
| **Baseline / assets** | Anchor `e16c574f58adc4f7f74ebc49682eee2402d4b5d9`; MVDS + verifiers + HANDOFF §2 TODO as listed in §3 |
| **Scope boundary** | §1 Scope Boundary |
| **Not claimed** | §1 Not Claimed |
| **Prior dependency** | `projects/document-system/BUILD_CONTRACT.instance.md` (constitutionalization-001); KBC/DNSW/VT rules |

---

## V&T Statement (instance issuance)

**Exists**

- `projects/document-system/BUILD_CONTRACT.instance.MVP-CLOSEOUT-001.md` — this instantiated Tier-2 contract on disk at issuance commit `e16c574f58adc4f7f74ebc49682eee2402d4b5d9`.

**Non-existent**

- Frozen lifecycle state for this instance — not yet earned until AC satisfied.

**Unverified**

- AC-08 badge URL or waiver — **UNRESOLVED REQUIRED INPUT** until maintainer supplies URL or signs waiver file.

**Verified (post-issuance execution)**

- AC-05 remote CI: GitHub Actions run `23996150764` **success** on commit `a2fe364`; evidence `docs/evidence/verification/2026-04-05-mvp-closeout-ci-run.md`.

**Functional status**

- This contract instance is **materialized and Active** as an executable artifact; execution outcomes remain **unverified** until AC table closes or halt is recorded.
