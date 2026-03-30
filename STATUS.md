# TLC repository status

> **Canonical JSON:** [`STATUS.json`](STATUS.json) — sole authoritative current-status artifact (PASS 10A).

| Field | Value |
|-------|-------|
| `project` | `coreyalejandro/the-living-constitution` |
| `head_sha` | `f12d2cb6817388945fca0e6e99758056594cfba1` |
| `last_verified_commit` | `1a2ef808478b71e8bdbe40c86406ccc180180276` |
| `last_verified_run_id` | `23757979228` |
| `tip_state_truth` | `tip_pending` |
| `workflow_sha` | `0e5bb8c32d13ba351441ee8ae0258d2dc684ca5e7c77b2277cce6d7512f99a63` |
| `escalation_state` | `review_required` |
| `reviewer_status` | `pending` |
| `governance_contract_version` | `v1.6.0` |
| `inventory_meta_generated_at_utc` | `2026-03-30T18:00:00Z` |

## Historical / evidence anchors

- **ci_remote_record_captured_at_utc:** `2026-03-30T17:25:00Z`
- **regression_ledger_last_commit_sha:** `1a2ef808478b71e8bdbe40c86406ccc180180276`
- **regression_ledger_last_run_id:** `23757979228`
- **regression_ledger_last_timestamp_utc:** `2026-03-30T17:25:00Z`

## Cross-repo consistency (ConsentChain submodule)

- **state:** `aligned`

## Truth boundary

Epistemic closure inside the repo: current operational status is synthesized into STATUS.json from inventory ci_provenance, git HEAD, workflow identity, regression ledger tail, and remote evidence record; STATUS.md is a deterministic render. External parties receive only exported proofs and schema-valid artifacts listed under open_interfaces.

Policy: `verification/closed-epistemics-open-interfaces-policy.json`
