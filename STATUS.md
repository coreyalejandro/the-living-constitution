# TLC repository status

> **Canonical JSON:** [`STATUS.json`](STATUS.json) — sole authoritative current-status artifact (PASS 10A).
> **PASS 11:** Governance truth is anchored to `truth_anchor` / `verification_target` (immutable tag + commit). `head_sha` is informational only.

| Field | Value |
|-------|-------|
| `project` | `coreyalejandro/the-living-constitution` |
| `verification_target` | `e56fc0753955901ee18bca44ae73181f9999b9db` |
| `head_sha` | `2d236b79e64fe167d80ca50814c84dcb0ba9879b` |
| `last_verified_commit` | `f0414d36a9a9a4e39acb2fee4c62c910069b88a4` |
| `last_verified_run_id` | `23761679469` |
| `tip_state_truth` | `tip_pending` |
| `workflow_sha` | `567a70acb3cc4db659b9a2e29d25834c8bcfded829fa3b04381df9496bf54781` |
| `escalation_state` | `review_required` |
| `reviewer_status` | `pending` |
| `governance_contract_version` | `v1.9.0` |
| `inventory_meta_generated_at_utc` | `2026-03-30T19:00:00Z` |

## Immutable truth anchor (PASS 11)

- **type:** `git_tag`
- **tag:** `tlc-gov-verified-e56fc07`
- **commit:** `e56fc0753955901ee18bca44ae73181f9999b9db`

## Historical / evidence anchors

- **ci_remote_record_captured_at_utc:** `2026-03-30T19:00:00Z`
- **regression_ledger_last_commit_sha:** `1a2ef808478b71e8bdbe40c86406ccc180180276`
- **regression_ledger_last_run_id:** `23757979228`
- **regression_ledger_last_timestamp_utc:** `2026-03-30T17:25:00Z`

## Cross-repo consistency (ConsentChain submodule)

- **state:** `aligned`

## Truth boundary

Epistemic closure inside the repo: current operational status is synthesized into STATUS.json from inventory ci_provenance, git HEAD, workflow identity, regression ledger tail, and remote evidence record; STATUS.md is a deterministic render. External parties receive only exported proofs and schema-valid artifacts listed under open_interfaces.

Policy: `verification/closed-epistemics-open-interfaces-policy.json`
