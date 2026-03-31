# CI attestation replay (PASS 16)

Canonical **isolated** governance JSON for recomputing `verification_runs_aggregate_sha256` without replacing ambient `verification/runs/*.json`.

## PASS 14 closure anchor

| Field | Value |
|-------|--------|
| Run ID | `23774310879` |
| Artifact | `governance-verification-runs-23774310879-1` |
| Artifact commit | `30805eed1d51ca78107294376c1b783275e484aa` |
| Replay directory | `verification/ci-remote-evidence/replay/23774310879/` |

## Verification

`scripts/verify_attestation.py` requires `git HEAD` to equal the attestation `commit` field. For historical replay, use a **detached checkout** at `30805eed1d51ca78107294376c1b783275e484aa`, then overlay this `replay/` tree and the PASS 16 `verify_attestation.py` from `main` if needed, **or** use a second worktree at that commit with paths copied from `main`.

Attestation JSON is produced by CI and may be gitignored locally; obtain it from artifact `supply-chain-attestation-23774310879-1` or keep a copy at `verification/attestations/23774310879-1.json`.

```bash
# Example (from repo root; adjust paths if using a worktree at 30805eed)
python3 scripts/verify_attestation.py --root . \
  --attestation verification/attestations/23774310879-1.json \
  --verification-runs-dir verification/ci-remote-evidence/replay/23774310879
```

Expected stdout includes `OK: supply-chain attestation verified` and `OK: used verification runs directory: ...`.

## Populate from GitHub Actions

```bash
gh run download 23774310879 -n governance-verification-runs-23774310879-1 -D /tmp/gov-art
# Copy *.json into verification/ci-remote-evidence/replay/23774310879/
```

Do not replace `verification/runs/` for replay; use `--verification-runs-dir` only.
