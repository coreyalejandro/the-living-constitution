# BUILD CONTRACT INSTANCE
## Constitutionally-Regulated Single Pass Executable Prompt

> **Artifact role:** **Example / helper only** — illustrative executed-instance shape for review. **Not** the canonical master template, **not** the guided instance template path (`BUILD_CONTRACT.instance.md`). Subordinate to `projects/c-rsp/BUILD_CONTRACT.md`.
>
> **Example only:** Illustrative PASS 8 / ConsentChain-style satellite instance for bundle review. Preflight command names are placeholders unless the repo ships matching scripts.

---
## 0. Instance Governance (maps to schema: template_governance)

- **Artifact Class:** Executable contract instance (example).
- **Canonical Expansion:** `C-RSP` = Constitutionally-Regulated Single Pass only.
- **Schema Authority:** `contract-schema.json` (version as declared below).
- **Profile Merge:** Satellite overlay (`PASS8_TEMPLATE.md`) specializes inventory, CI, and satellite invariants only; base halt and terminology are not overridden.

---
## 1. Contract Identity

- **Contract Title:** PASS 8 Satellite Institutionalization for ConsentChain
- **Contract ID:** CRSP-PASS8-CONSENTCHAIN-001
- **Version:** 1.0.0
- **Schema Version:** 1.0.0
- **Status:** Draft
- **Adoption Tier:** Tier-2-Operational
- **System Role:** Institutionalize satellite governance using TLC governance kit
- **Primary Objective:** Create a schema-valid, verifier-backed satellite governance contract for ConsentChain
- **Scope Boundary:** ConsentChain satellite governance artifacts, CI, evidence, and promotion controls
- **Not Claimed:** This instance does not claim TLC-core topology or dual-topology parity

---
## 2. Contract Topology + Profile

- **Topology Mode:** Satellite
- **Profile Type:** Satellite
- **Profile Overlay Source:** projects/c-rsp/PASS8_TEMPLATE.md
- **Verifier Class:** satellite-verifier
- **Authoritative Truth Surface:** verification/ci-remote-evidence/record.json; verification/regression-ledger/ledger.json; BUILD_CONTRACT.instance.md
- **Instance Artifact Path:** BUILD_CONTRACT.instance.md
- **Governance Lock Path:** governance-template.lock.json

---
## 3. Baseline State

- **Existing Repo / System:** consentchain
- **Baseline Commit / Anchor:** c719bdb
- **Verified Existing Assets:** governance kit adoption target, repo path, satellite profile
- **Known Constraints:** satellite does not use TLC-core topology verifier by default
- **Known Gaps:** final verifier outputs not yet recorded in this example
- **Legacy Migration Context:** internal integrated component being institutionalized as governed satellite

---
## 4. Dependencies and Inputs

- **Required Inputs:** governance kit, satellite profile, canonical schema, lock manifest
- **External Dependencies:** Python 3, CI runner, filesystem access
- **Governance Dependencies:** BUILD_CONTRACT.md, PASS8_TEMPLATE.md, contract-schema.json, governance-template.lock.json
- **Forbidden Assumptions:** no assumption of TLC-core verifier scope; no placeholder promotion

### 4A. Cross-Repo Governance Dependency Graph

- **Parent Constitutional Source:** the-living-constitution
- **Shared Overlay Profiles:** PASS8_TEMPLATE.md
- **Dual-Topology Linked Repos:** none
- **Satellite Dependents:** none
- **Drift Detection Scope:** weekly comparison of lock manifest and overlay version

---
## 5. Risk + Control Classification

- **Risk Class:** Moderate
- **Side-Effect Class:** Internal
- **External Action Scope:** none
- **Stop/Override Required:** No
- **Recovery Mode:** Manual

### 5A. Conditional Stop / Override Rule

Not triggered at Moderate / Internal with no external scope; if risk or side-effect class escalates, stop/override and expanded rollback become mandatory.

---
## 6. Execution Model

- **Execution Mode:** Single-pass deterministic build contract
- **Decision Closure Rule:** No open-ended branch points
- **Fallback Rule:** Any ambiguity halts
- **Generated Artifacts:** BUILD_CONTRACT.instance.md; validation report; preflight report; verifier report
- **Promotion Target:** Active upon successful preflight and schema validation

### 6A. Dual-Topology Rule

Not applicable. This is a Satellite instance.

---
## 7. Lifecycle State Machine

- **Current State:** Draft
- **Target State:** Active
- **Transition Guard Conditions:** no placeholders; schema validation pass; preflight pass; required fields complete
- **Transition Evidence Paths:** verification/runs/schema-validation.json; verification/runs/preflight.json

Allowed transitions: `Draft → Active → Frozen → Superseded`. Invalid transitions halt and require an audit record on the truth surface.

---
## 8. Invariants

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
- **INVARIANT_SAT_01**
- **INVARIANT_SAT_02**
- **INVARIANT_SAT_03**
- **INVARIANT_SAT_04**
- **INVARIANT_SAT_05**
- **INVARIANT_SAT_06**
- **INVARIANT_SAT_07**
- **INVARIANT_SAT_08**
- **INVARIANT_SAT_09**

---
## 9. Acceptance Criteria

| ID | Requirement | Verification Method | Pass Condition |
|---|---|---|---|
| AC-01 | Instance is schema-valid | schema validator | no errors |
| AC-02 | Instance has no unresolved placeholders in executable fields | placeholder scan | zero placeholders |
| AC-03 | Satellite verifier scope is correct | preflight + verifier | no TLC-core claims |

---
## 10. Rollback & Recovery

- **Safe-State Definition:** Contract remains Draft with no promotion claims
- **Rollback Procedure:** Revert generated instance artifacts and reset status to Draft
- **Recovery Authority:** human maintainer
- **Rollback Evidence Paths:** verification/runs/rollback.json
- **Partial Execution Handling:** halt and record partial state without promotion

---
## 11. Evidence + Truth Surface

- **Primary Evidence Paths:** verification/runs/schema-validation.json; verification/runs/preflight.json; verification/runs/verifier.json
- **Generated Reports:** validation report; preflight report; verifier report
- **Audit Artifacts:** lifecycle transition record; lock manifest
- **Evidence Boundary:** claims limited to generated reports and named truth surfaces
- **Truth Discipline:** Claims may not exceed evidence on declared paths.

---
## 12. Conflict Matrix

| Conflict Type | Example | Severity | Resolution |
|---|---|---|---|
| Schema Drift Conflict | Instance shape differs from schema | Critical | Halt |
| Topology Misclassification | Satellite claims core verifier | Critical | Halt |
| Placeholder Conflict | Required field unresolved | Critical | Halt |

---
## 13. Halt Matrix

- schema validation fails
- unresolved placeholders remain
- wrong verifier class is declared
- topology mode is not Satellite while claiming satellite-verifier
- `verify_project_topology.py` present without TLC-style `projects/` overlay adoption (per PASS8)
- frozen-context promotion rule violated (verified provenance on mutable tip)
- CI writeback to governance anchors on default branch
- required rollback semantics missing if tier/risk requires them

---
## 14. Preflight

**Commands (placeholders — replace with repo’s actual validators or TLC kit scripts):**

```bash
# Example intent: structural check + governance preflight
python3 scripts/validate_contract_schema.py --root .
python3 scripts/preflight_contract.py --root .
# In a governed satellite with kit installed, typically:
# python3 scripts/verify_governance_chain.py --root .
# python3 scripts/verify_institutionalization.py --root .
```

Preflight must verify:

- no unresolved placeholders
- correct profile overlay
- correct topology mode
- correct verifier class
- evidence paths declared
- acceptance criteria complete
- schema validation pass
- risk/control block complete
- lifecycle transition valid

---
## 15. Adoption Tiers

- **Tier-1-MVG:** identity + topology + schema-valid instance + no placeholders
- **Tier-2-Operational:** Tier-1 + acceptance criteria + risk/control + rollback/recovery + lifecycle evidence
- **Tier-3-Constitutional:** Tier-2 + invariant registry + lock manifest + dependency graph + audit-grade evidence

---
## 16. Output Format

Every execution summary must end with:

- **Exists**
- **Non-existent**
- **Unverified**
- **Functional status**

No stronger claim may be made outside that truth surface.

---
## 17. Instance Declaration

This example file is the declared executable instance shape for the described ConsentChain satellite run. Operational truth requires matching `governance-template.lock.json` pins and successful verifier outputs on the paths named in section 11.
