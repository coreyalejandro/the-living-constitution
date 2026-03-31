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
| **PASS 15 continuity** | Post-normalization push `e22d37bc0f65e42efceca37d7e0ff97642dadc25`: GitHub Actions run `23774580455` — **success** ([run URL](https://github.com/coreyalejandro/the-living-constitution/actions/runs/23774580455)). |

## 2026-03-30 — PASS 16 attestation replay determinism (C-RSP)

| Field | Value |
|-------|--------|
| **Weakness** | `scripts/verify_attestation.py` always read `verification/runs/*.json`; replaying CI attestation required **temporary replacement** of that tree with CI artifact contents (see PASS 14 closure notes). |
| **Resolution** | Added `--verification-runs-dir` to `scripts/verify_attestation.py` so aggregate and `governance_run_basename` resolve against an **explicit** directory (default unchanged: `verification/runs`). Canonical committed inputs: `verification/ci-remote-evidence/replay/23774310879/*.json` from artifact `governance-verification-runs-23774310879-1`. |
| **Rationale** | INVARIANT_57–59 unchanged; PASS 16 satisfies C-RSP **isolated staging / explicit inputs** without mutating ambient historical `verification/runs/`. |
| **record.json** | `schema_version` `1.1.0`; `attestation_replay` block with `verify_command` and paths. |
| **Enforcement** | Local: `verify_attestation.py` exit 0 with `--verification-runs-dir` at closure commit `30805eed` (HEAD must match attestation `commit`; see `replay/README.md`). CI: workflow unchanged — uses default runs dir on fresh CI `verification/runs`. |

## 2026-03-30 — FINAL_STOP_CONDITION (C-RSP v1.0.0) adjudication

| Field | Value |
|-------|--------|
| **Contract** | `projects/c-rsp/BUILD_CONTRACT.md` v1.0.0 — executable stop-condition pass |
| **Baseline verified** | PASS 14 anchored to run `23774310879` / commit `30805eed1d51ca78107294376c1b783275e484aa` (`verification/ci-remote-evidence/record.json`, prior log entries). PASS 15 continuity recorded in PASS 14 closure row. PASS 16 anchored to commit `4c38fa9659bdb016bf5cf1b3b9a429df70aab9f3`, CI run `23774969505` **success** (`gh run view 23774969505`). |
| **Stop-condition capabilities** | See adjudication table below. |

### Adjudication table (six capabilities)

| # | Capability | Governing evidence | Verification | Truth-state |
|---|------------|-------------------|--------------|-------------|
| 1 | Source of truth stabilized | `THE_LIVING_CONSTITUTION.md`, `MASTER_PROJECT_INVENTORY.json`, renderer output `STATUS.json` / `STATUS.md` (not hand-edited) | Files present; `render_status_surface.py` is canonical generator | **met** |
| 2 | Invariant enforcement stabilized | `scripts/verify_governance_chain.py`, `scripts/verify_project_topology.py` | `python3 scripts/verify_governance_chain.py --root .` exit 0; `python3 scripts/verify_project_topology.py --root . --with-governance` exit 0 | **met** |
| 3 | Remote CI and attestation proven | `verification/ci-remote-evidence/record.json`; PASS 14 / PASS 16 anchors | `gh run view 23774310879` (historical success); `gh run view 23774969505` conclusion success | **met** |
| 4 | Canonical remote-evidence record established | `verification/ci-remote-evidence/record.json` | File exists; schema_version 1.1.0 | **met** |
| 5 | Deterministic replay path established | `scripts/verify_attestation.py` `--verification-runs-dir`; `verification/ci-remote-evidence/replay/23774310879/` | `git worktree` at `30805eed` + PASS 16 script from tip + absolute `--attestation` + replay dir: **exit 0** (`OK: supply-chain attestation verified`) | **met** |
| 6 | Build-readiness adjudication without manual repair | This pass | `./scripts/bootstrap_repo.sh` exit 0; verifiers + renderer run without workaround | **met** |

| **Outcome** | **STOP CONDITION MET — GOVERNANCE FREEZE** (transition to maintenance-mode governance for product/repo buildout; no residual constitutional gap named). |
| **Residual gap** | N/A — explicit reason: all six capabilities evidenced. |

**Protocol:** `append-only` row; does not rewrite prior PASS rows.

## 2026-03-30 — Front-door transition package (C-RSP instance)

| Field | Value |
|-------|--------|
| **Contract** | TLC front-door transition package — documentation + optional `apps/tlc-control-plane/` scaffold |
| **Conflict** | N/A — explicit reason: no collision with protected paths; root `README.md` not overwritten per contract |
| **Artifacts** | `docs/front-door/*`, `docs/front-door/diagram-sources/*.mmd`, `apps/tlc-control-plane/*` |
| **Governance** | No new TLC pass; `STATUS.json` not modified; maintenance-mode preserved |
| **Scaffold** | Created self-contained Next.js app under `apps/tlc-control-plane/` with pnpm and pinned dependencies |
