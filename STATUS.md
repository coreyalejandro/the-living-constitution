# TLC repository status

> **Canonical JSON:** [`STATUS.json`](STATUS.json) — sole authoritative current-status artifact (PASS 10A).
> **PASS 11:** Governance truth is anchored to `truth_anchor` / `verification_target` (immutable tag + commit). `head_sha` is informational only.

| Field | Value |
|-------|-------|
| `project` | `coreyalejandro/the-living-constitution` |
| `series` | `B` |
| `status` | `active` |
| `verification_target` | `e5843d879918f97e2ce72690a7c2c502d81d9513` |
| `head_sha` | `e5843d879918f97e2ce72690a7c2c502d81d9513` |
| `last_verified_commit` | `e5843d879918f97e2ce72690a7c2c502d81d9513` |
| `last_verified_run_id` | `25234396495` |
| `tip_state_truth` | `tip_verified` |
| `workflow_sha` | `119f0e8e1f206c72a73d12822616d7f237c1016e0560b4d99385710635cc4a62` |
| `escalation_state` | `none` |
| `reviewer_status` | `approved` |
| `governance_contract_version` | `v1.9.0` |
| `inventory_meta_generated_at_utc` | `2026-05-01T21:55:00Z` |

## Immutable truth anchor (PASS 11)

- **type:** `git_tag`
- **tag:** `tlc-gov-verified-e5843d8`
- **commit:** `e5843d879918f97e2ce72690a7c2c502d81d9513`

## Historical / evidence anchors

- **ci_remote_record_captured_at_utc:** `2026-05-01T21:41:49Z`
- **regression_ledger_last_commit_sha:** `1a2ef808478b71e8bdbe40c86406ccc180180276`
- **regression_ledger_last_run_id:** `23757979228`
- **regression_ledger_last_timestamp_utc:** `2026-03-30T17:25:00Z`

## Cross-repo consistency (ConsentChain submodule)

- **state:** `aligned`

## Truth boundary

Epistemic closure inside the repo: current operational status is synthesized into STATUS.json from inventory ci_provenance, git HEAD, workflow identity, regression ledger tail, and remote evidence record; STATUS.md is a deterministic render. External parties receive only exported proofs and schema-valid artifacts listed under open_interfaces.

Policy: `verification/closed-epistemics-open-interfaces-policy.json`
