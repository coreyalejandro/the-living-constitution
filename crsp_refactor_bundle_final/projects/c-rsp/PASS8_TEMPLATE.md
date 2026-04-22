# PASS 8 — Satellite Institutionalization Profile
## C-RSP Satellite Governance Overlay

> **Profile Status:** Overlay profile only. Not executable by itself.
> **Base Dependency:** Must be instantiated through the constitutional master template in `projects/c-rsp/BUILD_CONTRACT.md`.

---
## 0. Profile Identity

- **Profile Type:** Satellite
- **Topology Mode:** Satellite
- **Verifier Class:** satellite-verifier
- **Purpose:** Institutionalize C-RSP governance in a satellite repository using `packages/tlc-governance-kit/` from The Living Constitution.
- **Boundary Rule:** TLC itself keeps its own `scripts/` and full topology verifier. Satellites omit `verify_project_topology.py` unless they adopt TLC-style `projects/` overlays.
- **Not Claimed:** This profile does not by itself produce an executable build contract, dual-topology governance, or TLC-core parity.

---
## 1. Required Files

The satellite instance must define or generate all of the following:

- `governance/constitution/core/invariant-registry.json`
- `governance/constitution/core/doctrine-to-invariant.map.json`
- `governance/constitution/core/invariants/F1–F5.md`
- `governance/enforcement/core/enforcement-map.json`
- `governance/agents/core/agent-capabilities.json`
- `verification/evidence-ledger.schema.json`
- `verification/evidence-ledger/seed.json`
- `verification/governance-verification.template.json`
- `verification/governance-verification-run.schema.json`
- `verification/ci-remote-evidence/record.json`
- `verification/regression-ledger.schema.json`
- `verification/regression-ledger/ledger.json`
- `verification/review-escalation-policy.json`
- `verification/tip-state-policy.json`
- `verification/pass7-branch-verification-policy.json`
- `verification/GOVERNANCE_SYSTEM_CARD.md`
- `verification/independent-review/last-review.json`
- `verification/MATRIX.md`
- `MASTER_PROJECT_INVENTORY.json`
- `MASTER_PROJECT_INVENTORY.md`
- `requirements-verify.txt`
- `scripts/` from governance kit
- `.github/workflows/verify.yml`

---
## 2. Profile Merge Rules

This overlay may specialize only the following for satellite repos:

- file inventories
- verifier scope
- CI command requirements
- satellite-specific invariants
- promotion constraints derived from satellite topology
- evidence expectations specific to a satellite repo

This overlay may not override:

- canonical terminology
- core section order or names
- lifecycle state names
- constitutional invalidation rules
- base halt semantics
- base truth-discipline requirements

---
## 3. Required CI Steps

Minimum commands:

- `python3 scripts/verify_governance_chain.py --root .`
- `python3 scripts/verify_institutionalization.py --root .`

Recommended pipeline order:

1. `verify_governance_chain.py`
2. `append_regression_ledger.py` (GitHub Actions only)
3. `verify_institutionalization.py`
4. `governance_failure_injection_tests.py`
5. upload `verification/runs/*.json`
6. self-verify downloaded artifact with `ci_self_verify_governance_artifact.py`

Required workflow triggers:

- `workflow_dispatch`
- `push`
- `pull_request`
- `schedule`

---
## 4. Satellite-Specific Invariants

- **INVARIANT_SAT_01:** Satellite must use governance kit as declared source.
- **INVARIANT_SAT_02:** Satellite must not claim TLC-core verifier scope.
- **INVARIANT_SAT_03:** `verify_project_topology.py` must be absent unless TLC-style `projects/` overlays are adopted.
- **INVARIANT_SAT_04:** Inventory and workflow commands must match required governance commands.
- **INVARIANT_SAT_05:** Invariant registry must define exactly required institutionalization invariants for this profile scope.
- **INVARIANT_SAT_06:** Satellite truth claims must not exceed satellite evidence scope.
- **INVARIANT_SAT_07:** Promotion state must follow frozen-context rule.
- **INVARIANT_SAT_08:** No CI writeback to governance anchors on default branch.
- **INVARIANT_SAT_09:** Satellite instances must validate against the canonical contract schema.

---
## 5. Satellite Acceptance Criteria Addendum

| ID | Requirement | Verification Method | Pass Condition |
|---|---|---|---|
| AC-SAT-01 | Satellite file inventory complete | filesystem verification | all required files present |
| AC-SAT-02 | Required CI commands present | substring workflow verification | exact required substrings present |
| AC-SAT-03 | Satellite verifier scope correct | preflight + verifier output | no TLC-core verifier claims |
| AC-SAT-04 | Frozen-context promotion rule enforced | governance verification run | mutable branch tips do not claim verified provenance |
| AC-SAT-05 | No-CI-writeback rule enforced | workflow audit | no writeback behavior on default branch |
| AC-SAT-06 | Contract schema valid | schema verifier | all required sections/fields match schema |

---
## 6. Lifecycle / Promotion Semantics

`ci_provenance.status=verified` and `tip_state_truth=tip_verified` are valid only on frozen verification contexts:

- detached HEAD at anchor
- branch matching `provenance/verified-*`
- tag matching configured `tag_glob`

On mutable tips, inventory must use pending states even if HEAD equals last qualifying commit.

Canonical verified history remains:

- `verification/ci-remote-evidence/record.json`
- `verification/regression-ledger/ledger.json`

---
## 7. Satellite Halt Conditions

The satellite contract instance must halt if:

- required files are missing
- wrong verifier class is declared
- topology mode is not `Satellite`
- `verify_project_topology.py` is present without overlay adoption justification
- canonical term drift is detected
- workflow command inventory mismatches occur
- schema validation fails
- frozen-context promotion rule is violated
- CI writeback attempts to mutate governance anchors on default branch

---
## 8. Evidence Expectations

Every Tier-2+ satellite instance must declare:

- constitutional parent source
- overlay profile source
- shared governance lock manifest
- linked repos, if any
- drift detection cadence
- evidence paths for verifier runs
- evidence paths for lifecycle transitions
- evidence paths for rollback/recovery if applicable

---
## 9. Operator Notes

Adoption sequence:

1. scaffold satellite files from governance kit
2. instantiate base contract with this profile
3. validate against schema
4. run preflight
5. run verification workflow locally and remotely
6. inspect evidence outputs
7. promote only through qualifying frozen context

Reference implementation: `coreyalejandro/consentchain` after PASS 8.
