# TLC repository status

> **Canonical JSON:** [`STATUS.json`](STATUS.json) — sole authoritative current-status artifact (PASS 10A).
> **Git HEAD:** use `git rev-parse HEAD` at checkout; `head_sha` in JSON is render-time (verifier normalizes to live HEAD for INVARIANT_42).

| Field | Value |
|-------|-------|
| `project` | `coreyalejandro/the-living-constitution` |
| `last_verified_commit` | `f0414d36a9a9a4e39acb2fee4c62c910069b88a4` |
| `last_verified_run_id` | `23761679469` |
| `tip_state_truth` | `tip_pending` |
| `workflow_sha` | `0e5bb8c32d13ba351441ee8ae0258d2dc684ca5e7c77b2277cce6d7512f99a63` |
| `escalation_state` | `review_required` |
| `reviewer_status` | `pending` |
| `governance_contract_version` | `v1.8.0` |
| `inventory_meta_generated_at_utc` | `2026-03-30T19:00:00Z` |

## Invariant system (PASS 11)

INVARIANTS: 50 total
- Critical: 0
- High: 0
- Medium: 0
- Low: 0
Violations: 0

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
