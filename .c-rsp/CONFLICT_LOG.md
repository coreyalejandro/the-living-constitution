# C-RSP Conflict Log — The Living Constitution

**Purpose:** Append-only operational log for governance repair decisions and conflict resolution under the PASS 14 closure contract.

## 2026-03-30 — PASS 14 governance integrity repair (pre-CI)

| Field | Value |
|-------|--------|
| **Conflict** | INVARIANT_21 — `ci_provenance.verify_workflow_sha256` drifted from `sha256(.github/workflows/verify.yml)` after workflow updates |
| **Resolution** | Updated `MASTER_PROJECT_INVENTORY.json` `ci_provenance.verify_workflow_sha256` to match current workflow file on disk |
| **Conflict** | INVARIANT_42 — `STATUS.json` / `STATUS.md` behind `aggregate_status()` (workflow SHA and related aggregate fields) |
| **Resolution** | Regenerated via `python3 scripts/render_status_surface.py --root .` |
| **Artifacts added** | `.c-rsp/governance-map.json`, `.c-rsp/CONFLICT_LOG.md` (C-RSP mapping contract) |
| **Historical field** | `verify_workflow_sha256_at_last_remote_run` left documenting workflow identity at last recorded remote run (`record.json`); not overwritten by tip repair |

**Protocol:** Per conflict matrix — workflow SHA mismatch → update inventory to current workflow; STATUS drift → run render script. No CI skip; remote proof required for PASS 14 closure post-push.
