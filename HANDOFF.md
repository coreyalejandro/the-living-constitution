# Agent Handoff: The Living Constitution (base camp)

**Date:** 2026-03-30  
**Status:** PASS 6 tip-state exactness implemented (C-RSP v1.4.0)

## What Was Just Completed

- **PASS 6 (tip-state exactness):** `ci_provenance.tip_state_truth`, `last_remote_qualifying_commit`, INVARIANT_30–INVARIANT_36; `verification/tip-state-policy.json`; `scripts/tip_state_helpers.py`; `scripts/sync_ci_provenance_tip_state.py`; regression ledger schema 1.1.0 with `tip_state_truth` per row; `verify_governance_chain.py` checks HEAD vs anchor and protected-surface drift when `status=pending`; `review-escalation-policy.json` tip_state_transition_policy + R6/R7; inventory contract v1.4.0; governance artifacts include `tip_state_policy`.
- **Current tip posture:** `MASTER_PROJECT_INVENTORY.json` `ci_provenance` is `pending` / `tip_pending` with `review_required` while HEAD advances beyond last remote qualifying commit until the next green Actions run and manual record + inventory promotion per policy (no CI writeback).

## Recommended Next Steps

- After a qualifying green `Verify Living Constitution` run on the commit to certify: update `verification/ci-remote-evidence/record.json` and `MASTER_PROJECT_INVENTORY.json` `ci_provenance` to match that run, then set `status`/`tip_state_truth` to `verified`/`tip_verified` only when `HEAD` equals `last_verified_commit`.
- Optional: `python3 scripts/sync_ci_provenance_tip_state.py --root .` to refresh pending fields from git + record (does not set verified).

## Quick Reference

- **Tip policy:** `verification/tip-state-policy.json`  
- **Verifiers:** `verify_governance_chain.py`, `verify_institutionalization.py`, `verify_project_topology.py --with-governance`  

---

**Confidence:** High — full verifier pipeline exited 0 locally after PASS 6.
