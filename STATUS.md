# TLC repository status

> **Canonical JSON:** [`STATUS.json`](STATUS.json) — sole authoritative current-status artifact (PASS 10A).
> **PASS 11:** Governance truth is anchored to `truth_anchor` / `verification_target` (immutable tag + commit). `head_sha` is informational only.

| Field | Value |
|-------|-------|
| `project` | `coreyalejandro/the-living-constitution` |
| `series` | `B` |
| `status` | `active` |
| `verification_target` | `e56fc0753955901ee18bca44ae73181f9999b9db` |
| `head_sha` | `af7ec64d93ab80c59d99c0cc068ee5614a72cefb` |
| `last_verified_commit` | `30805eed1d51ca78107294376c1b783275e484aa` |
| `last_verified_run_id` | `23774310879` |
| `tip_state_truth` | `tip_pending` |
| `workflow_sha` | `3db5931f6722dc631aea92a7a0da0892dfd40707bc0d309a65760c189053a5c8` |
| `escalation_state` | `review_required` |
| `reviewer_status` | `pending` |
| `governance_contract_version` | `v1.9.0` |
| `inventory_meta_generated_at_utc` | `2026-04-22T16:16:17Z` |

## Immutable truth anchor (PASS 11)

- **type:** `git_tag`
- **tag:** `tlc-gov-verified-e56fc07`
- **commit:** `e56fc0753955901ee18bca44ae73181f9999b9db`

## Historical / evidence anchors

- **ci_remote_record_captured_at_utc:** `2026-03-31T01:15:00Z`
- **regression_ledger_last_commit_sha:** `1a2ef808478b71e8bdbe40c86406ccc180180276`
- **regression_ledger_last_run_id:** `23757979228`
- **regression_ledger_last_timestamp_utc:** `2026-03-30T17:25:00Z`

## Cross-repo consistency (ConsentChain submodule)

- **state:** `aligned`

## Truth boundary

Epistemic closure inside the repo: current operational status is synthesized into STATUS.json from inventory ci_provenance, git HEAD, workflow identity, regression ledger tail, and remote evidence record; STATUS.md is a deterministic render. External parties receive only exported proofs and schema-valid artifacts listed under open_interfaces.

Policy: `verification/closed-epistemics-open-interfaces-policy.json`
