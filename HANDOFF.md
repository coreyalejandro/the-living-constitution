# Agent Handoff: The Living Constitution (base camp)

**Date:** 2026-03-30  
**Status:** **PASS 14** closed on green CI run [23774310879](https://github.com/coreyalejandro/the-living-constitution/actions/runs/23774310879), closure head SHA `30805eed1d51ca78107294376c1b783275e484aa`. **PASS 15** normalization recorded. **PASS 16** (C-RSP): canonical CI attestation replay via `--verification-runs-dir` and `verification/ci-remote-evidence/replay/` — no manual swap of ambient `verification/runs/`.

## What Was Just Completed

- **PASS 16 (C-RSP):** `scripts/verify_attestation.py` accepts `--verification-runs-dir` for isolated governance JSON (default remains `verification/runs`). Committed replay inputs for PASS 14 anchor: `verification/ci-remote-evidence/replay/23774310879/` (from artifact `governance-verification-runs-23774310879-1`). `verification/ci-remote-evidence/record.json` includes `attestation_replay` with `verify_command`. `.c-rsp/governance-map.json` and append-only `.c-rsp/CONFLICT_LOG.md` updated.
- **PASS 14 / 15 (historical):** Submodule blocker remediated via `SUBMODULES_PAT`; attestation chain on run `23774310879`. PASS 15 continuity runs `23774580455`, `23774596954` success.

## Recommended Next Steps

- Keep `STATUS.json` / `STATUS.md` renderer-only (`python3 scripts/render_status_surface.py --root .`).
- For mutable `main` tip-state claims, follow `verification/tip-state-policy.json`.

## Quick Reference

- **PASS 16 replay verify:** `python3 scripts/verify_attestation.py --root . --attestation verification/attestations/23774310879-1.json --verification-runs-dir verification/ci-remote-evidence/replay/23774310879` — requires `git HEAD` = `30805eed1d51ca78107294376c1b783275e484aa` (detached or worktree) and local attestation file (gitignored; from CI artifact `supply-chain-attestation-23774310879-1`). See `verification/ci-remote-evidence/replay/README.md`.
- **PASS 14 closure run:** `23774310879` @ `30805eed1d51ca78107294376c1b783275e484aa`
- **Bootstrap:** `./scripts/bootstrap_repo.sh`

---

**Confidence:** High for PASS 16 mechanism and committed replay inputs; post-push CI must be observed after merge to `main`.
