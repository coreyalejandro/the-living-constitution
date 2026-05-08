> MACHINE LAW NOTICE: Any obligation, restriction, halt condition, verifier, acceptance rule, or lifecycle rule stated in this Markdown but absent from the paired JSON is non-authoritative and shall not be enforced. The paired JSON at projects/c-rsp/instances/CRSP-TLC-TWO-PATHS-REFACTOR-001.json is the authoritative source of truth for this contract.

# CRSP-TLC-TWO-PATHS-REFACTOR-001

**Contract ID:** CRSP-TLC-TWO-PATHS-REFACTOR-001
**Schema version:** 4.0
**Status:** Active
**C-RSP expansion:** Constitutionally-Regulated Single Pass
**System:** The Living Constitution (TLC)
**Baseline commit:** 85c0c9a9a6f1f4d0f0d54f7d79941c03278b9faa

---

## Objective

Refactor TLC's public repository front-door into two explicit reviewer paths:

1. Research Path — for evaluating TLC as a hypothesis-driven AI safety research apparatus.
2. Build Path — for evaluating TLC as a runnable constitutional governance-as-code prototype.

The refactor clarifies what each path claims, what evidence each path exposes, and what claims remain unverified.

---

## Topology

- Mode: TLC-Core
- Profile: Front-Door Reviewer Path Refactor
- Verifier class: Static Documentation, Repository Structure, Truth Surface, and Evidence Routing Verifier

---

## Operations executed

| Step | Name | Status |
|------|------|--------|
| OP-001 | Verify C-RSP authority bundle | COMPLETE |
| OP-002 | Create two-path front-door | COMPLETE |
| OP-003 | Create Research Path document | COMPLETE |
| OP-004 | Create Build Path document | COMPLETE |
| OP-005 | Create or update truth surface | COMPLETE |
| OP-006 | Create validation plan scaffold | COMPLETE |
| OP-007 | Create runtime invariants index scaffold | COMPLETE |
| OP-008 | Create Contract Window examples scaffold | COMPLETE |
| OP-009 | Create reviewer guide | COMPLETE |
| OP-010 | Update README front-door references | COMPLETE |
| OP-011 | Write verification evidence | COMPLETE |

---

## Generated artifacts

| Path | Status |
|------|--------|
| docs/front-door/TWO_REVIEWER_PATHS.md | Created |
| docs/research/RESEARCH_PATH.md | Created |
| docs/build/BUILD_PATH.md | Created |
| docs/research/VALIDATION_PLAN.md | Created |
| docs/governance/RUNTIME_INVARIANTS_INDEX.md | Created |
| docs/examples/CONTRACT_WINDOW_EXAMPLES.md | Created |
| docs/review/REVIEWER_GUIDE.md | Created |
| STATUS.md | Updated — CRSP-TLC-TWO-PATHS-REFACTOR-001 truth surface section appended |
| README.md | Updated — two reviewer paths section added |
| projects/c-rsp/instances/CRSP-TLC-TWO-PATHS-REFACTOR-001.json | Created |
| projects/c-rsp/instances/CRSP-TLC-TWO-PATHS-REFACTOR-001.md | Created |
| verification/CRSP-TLC-TWO-PATHS-REFACTOR-001/ | Created |

---

## Predicate results summary

| Predicate | Result |
|-----------|--------|
| P-001 — exists(THE_LIVING_CONSTITUTION.md) | PASS |
| P-002 — exists(CLAUDE.md) | PASS |
| P-003 — exists(MASTER_PROJECT_INVENTORY.json) | PASS |
| P-004 — exists(projects/c-rsp/BUILD_CONTRACT.md) | PASS |
| P-005 — paired_artifact_exists | PASS |
| P-006 — markdown_has_disclaimer | PASS |
| P-007 — TWO_REVIEWER_PATHS.md in scope | PASS |
| P-008 — RESEARCH_PATH.md in scope | PASS |
| P-009 — BUILD_PATH.md in scope | PASS |
| P-010 — STATUS.md in scope | PASS |
| P-011 — not_exists(TLC_RENAME.md) | PASS |
| P-012 — no_forbidden_network_access | PASS |
| P-013 — evidence_written | PASS |
| P-014 — no_unresolved_in_required_fields | PARTIAL — verifier module sha256 for two new scripts remain unresolved; allowed per P-014 allowed_exception |

---

## Halt matrix summary

All 20 halt conditions: CLEAR.

---

## Unresolved field ledger

| Field | Reason |
|-------|--------|
| verifier_modules[1].sha256 | verify_two_path_front_door.sh does not yet exist |
| verifier_modules[2].sha256 | verify_truth_surface.sh does not yet exist |

---

## Not claimed

- H1, H2, H3 validated
- TLC is production-ready
- TLC is suitable as a production safety layer
- Contract Window effect is structural rather than attentional
- 59 invariants fully documented
- This contract performed any powered experiment, lay comprehension validation, inter-rater reliability study, security audit, or production hardening

---

## Constitutional authority files — not modified

- THE_LIVING_CONSTITUTION.md
- CLAUDE.md
- MASTER_PROJECT_INVENTORY.json
- contract-schema.json (projects/c-rsp/)
- CRSP_OUTCOME_TEMPLATE.md (projects/c-rsp/)
- scripts/verify_crsp_template_bundle.sh

---

## Truth surface

- STATUS.md — Exists / Not claimed / Unverified / Functional status sections
- verification/CRSP-TLC-TWO-PATHS-REFACTOR-001/outcome.md
- verification/CRSP-TLC-TWO-PATHS-REFACTOR-001/predicate-results.jsonl
- verification/CRSP-TLC-TWO-PATHS-REFACTOR-001/lifecycle.jsonl
- verification/CRSP-TLC-TWO-PATHS-REFACTOR-001/rollback.jsonl

---

> Paired JSON: projects/c-rsp/instances/CRSP-TLC-TWO-PATHS-REFACTOR-001.json
> Any obligation in this Markdown not present in that JSON is non-authoritative.
