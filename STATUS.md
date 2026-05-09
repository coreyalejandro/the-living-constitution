# TLC repository status

> **Canonical JSON:** [`STATUS.json`](STATUS.json) — sole authoritative current-status artifact (PASS 10A).
> **PASS 11:** Governance truth is anchored to `truth_anchor` / `verification_target` (immutable tag + commit). `head_sha` is informational only.

| Field | Value |
|-------|-------|
| `project` | `coreyalejandro/the-living-constitution` |
| `series` | `B` |
| `status` | `active` |
| `verification_target` | `417d90547f142246a676bfb28284083f9cbf325d` |
| `head_sha` | `df26b0f89a4cc7811faa66752def7116ce71be46` |
| `last_verified_commit` | `417d90547f142246a676bfb28284083f9cbf325d` |
| `last_verified_run_id` | `25236308029` |
| `tip_state_truth` | `tip_verified` |
| `workflow_sha` | `119f0e8e1f206c72a73d12822616d7f237c1016e0560b4d99385710635cc4a62` |
| `escalation_state` | `none` |
| `reviewer_status` | `approved` |
| `governance_contract_version` | `v1.9.0` |
| `inventory_meta_generated_at_utc` | `2026-05-01T22:55:00Z` |

## Immutable truth anchor (PASS 11)

- **type:** `git_tag`
- **tag:** `tlc-gov-verified-417d905`
- **commit:** `417d90547f142246a676bfb28284083f9cbf325d`

## Historical / evidence anchors

- **ci_remote_record_captured_at_utc:** `2026-05-01T22:42:56Z`
- **regression_ledger_last_commit_sha:** `1a2ef808478b71e8bdbe40c86406ccc180180276`
- **regression_ledger_last_run_id:** `23757979228`
- **regression_ledger_last_timestamp_utc:** `2026-03-30T17:25:00Z`

## Cross-repo consistency (ConsentChain submodule)

- **state:** `aligned`

## Truth boundary

Epistemic closure inside the repo: current operational status is synthesized into STATUS.json from inventory ci_provenance, git HEAD, workflow identity, regression ledger tail, and remote evidence record; STATUS.md is a deterministic render. External parties receive only exported proofs and schema-valid artifacts listed under open_interfaces.

Policy: `verification/closed-epistemics-open-interfaces-policy.json`

---

## CRSP-TLC-TWO-PATHS-REFACTOR-001 Truth Surface

> Added by contract CRSP-TLC-TWO-PATHS-REFACTOR-001. These four categories are required by the contract's truth surface specification. They do not replace the authoritative STATUS.json above.

### Exists

- THE_LIVING_CONSTITUTION.md (constitutional specification, Articles I-V)
- CLAUDE.md (project-level agent behavior overrides)
- MASTER_PROJECT_INVENTORY.json (governed project registry)
- projects/c-rsp/BUILD_CONTRACT.md (C-RSP master contract hub)
- projects/c-rsp/contract-schema.json (JSON schema for C-RSP v4.0)
- projects/c-rsp/CRSP_OUTCOME_TEMPLATE.md (outcome document template)
- scripts/verify_crsp_template_bundle.sh (bundle verification script)
- SentinelOS invariants I1-I6 (defined; see research/evidence-ledger.md entry S2)
- C-RSP build contract instances (projects/c-rsp/instances/)
- Contract Window reference implementation (apps/contract-window/)
- Evidence Observatory pipeline (apps/evidence-observatory/)
- PROACTIVE epistemic safety agent (212/212 tests passing as of 2026-03-25)
- BicameralReview engine synthetic pilot (kappa 0.762)
- Research hypotheses H1, H2, H3 (defined in PROPOSAL.md)
- Two-path reviewer front-door (docs/front-door/TWO_REVIEWER_PATHS.md)

### Not claimed

- H1, H2, H3 have been empirically validated
- The Contract Window effect is structural rather than attentional
- TLC is production-ready
- TLC is suitable as a production safety layer
- All 59 runtime invariants are fully enforced
- CI/CD pipeline passes are verified in this document
- Security audit has been performed
- External peer review has been completed
- The due-diligence report that informed CRSP-TLC-TWO-PATHS-REFACTOR-001 was a complete source-code audit
- Lay comprehension study has been completed
- Inter-rater reliability has been established on real (non-synthetic) data

### Unverified

- Full implementation status of invariants I1-I6 beyond definition
- Implementation status of remaining 53 invariants (governance/constitution/core/invariant-registry.json requires direct inspection)
- CI/CD current pass status
- Contract Window effect size and mechanism (structural vs. attentional)
- Evidence Observatory full layer-by-layer audit
- External repo (cognitive-governance-lab) current test count and pass status

### Functional status

Implemented research system. Core constitutional structure, C-RSP build contracts, Evidence Observatory, and Contract Window reference implementation exist and are runnable. Key invariants (I1-I6) are defined and enforced. Production hardening and external validation are out of scope for the current release. TLC is a governance-as-code research system. It is not a claimed production safety layer.
