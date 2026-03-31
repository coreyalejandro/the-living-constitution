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

## 2026-03-31 — PASS 14 remote CI blocked (submodule access)

| Field | Value |
|-------|--------|
| **Evidence** | GitHub Actions run `23773602359` (and subsequent pushes `23773613714`, `23773617617`) failed at `actions/checkout@v4` before any verifier or attestation steps. |
| **Root cause** | Submodule `projects/consent-gateway-auth0` → `https://github.com/coreyalejandro/consent-gateway-auth0.git` is **private**. Default `GITHUB_TOKEN` cannot clone private sibling repos; error text: `repository 'https://github.com/coreyalejandro/consent-gateway-auth0.git/' not found` / clone failed. |
| **Workflow binding** | `.github/workflows/verify.yml` uses `token: ${{ secrets.SUBMODULES_PAT \|\| secrets.GITHUB_TOKEN }}`. |
| **Local verification** | After `./scripts/bootstrap_repo.sh`: `python3 scripts/verify_governance_chain.py` exit 0; `python3 scripts/verify_project_topology.py --with-governance` exit 0; `python3 scripts/render_status_surface.py --root .` updated `STATUS.json` / `STATUS.md` (`head_sha` → current `HEAD`). |
| **Secret inventory** | `gh secret list --repo coreyalejandro/the-living-constitution` returned no rows in this environment (either no secrets configured or listing not permitted). **Required for CI:** repository secret `SUBMODULES_PAT` — fine-grained PAT with `contents:read` on `coreyalejandro/consent-gateway-auth0` (and any other private submodules). |
| **PASS 14** | **NOT CLOSED** — no successful remote run; no `governance-verification-runs` / `supply-chain-attestation` artifacts; `scripts/verify_attestation.py` not executed against a CI-produced attestation file. |
| **Retry** | One bounded re-run after access repair: push `main` after `SUBMODULES_PAT` is present, then re-download artifacts and run `verify_attestation.py` per contract. |

## 2026-03-31 — PASS 14 closure (green CI + attestation verified)

| Field | Value |
|-------|--------|
| **Closure anchor** | GitHub Actions run `23774310879` — **success** — head SHA `30805eed1d51ca78107294376c1b783275e484aa` ([run URL](https://github.com/coreyalejandro/the-living-constitution/actions/runs/23774310879)). |
| **Submodule access blocker** | Prior runs (`23773602359`, `23773613714`, `23773617617`) failed at `actions/checkout` — private submodule `projects/consent-gateway-auth0` not cloneable with default `GITHUB_TOKEN`. |
| **Remediation** | Repository secret `SUBMODULES_PAT` (or equivalent) — workflow uses `token: ${{ secrets.SUBMODULES_PAT \|\| secrets.GITHUB_TOKEN }}`; green run confirms checkout path unblocked. |
| **Artifacts (closure)** | `governance-verification-runs-23774310879-1`, `supply-chain-attestation-23774310879-1` (verified via `gh api .../actions/runs/23774310879/artifacts`). |
| **Attestation verification** | `python3 scripts/verify_attestation.py --root . --attestation verification/attestations/23774310879-1.json` → **exit 0**, stdout `OK: supply-chain attestation verified` (after temporary swap of `verification/runs/*.json` to CI artifact contents matching attested aggregate; then **restored** full local `verification/runs/` tree). |
| **Workspace restoration** | Confirmed: `verification/runs/` repopulated from backup after attestation step; no permanent CI-only substitution remains. |
| **PASS 14** | **CLOSED** — closure anchored to successful run `23774310879` and commit `30805eed1d51ca78107294376c1b783275e484aa`. |
| **PASS 15** | Normalization / constitutional record update (this commit); continuity CI observed post-push. |
