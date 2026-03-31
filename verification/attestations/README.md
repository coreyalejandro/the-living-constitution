# Supply-chain attestations (PASS 14)

CI writes one JSON attestation per run under this directory:

- Filename: `{GITHUB_RUN_ID}-{GITHUB_RUN_ATTEMPT}.json` (not committed; ignored by git).
- Upload: GitHub Actions artifact `supply-chain-attestation-{run_id}-{run_attempt}` alongside governance run artifacts.

Third parties verify a downloaded attestation with:

```bash
python3 scripts/verify_attestation.py --root . --attestation verification/attestations/<file>.json
```

Schema: `verification/supply-chain-attestation.schema.json`.
