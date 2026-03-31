# Supply-chain attestations (PASS 14)

CI writes one JSON attestation per run under this directory:

- Filename: `{GITHUB_RUN_ID}-{GITHUB_RUN_ATTEMPT}.json` (not committed; ignored by git).
- Upload: GitHub Actions artifact `supply-chain-attestation-{run_id}-{run_attempt}` alongside governance run artifacts.

Third parties verify a downloaded attestation with:

```bash
python3 scripts/verify_attestation.py --root . --attestation verification/attestations/<file>.json
```

PASS 16 — replay CI governance evidence **without** replacing `verification/runs/`: pass `--verification-runs-dir` to a directory containing the same `*.json` set the CI run attested (e.g. committed under `verification/ci-remote-evidence/replay/<run_id>/`). `git HEAD` must equal the attestation `commit` field. See `verification/ci-remote-evidence/replay/README.md` and `verification/ci-remote-evidence/record.json` (`attestation_replay`).

Schema: `verification/supply-chain-attestation.schema.json`.
