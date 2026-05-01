# TLC Research Workbench — Eval Suites

evidence_basis: CONSTRUCTED — derived from TLC-RDI-MVP-001 and projects/evaluation/.

## Current Suites

### F1-F5 Invariant Suite (VERIFIED)
- Location: projects/evaluation/tlc_evals/
- Cases: 26 built-in cases grounded in FC-001 through FC-018
- Status: 212/212 tests passing (VR-V-15C6, validated 2026-01-24)
- evidence_basis: VERIFIED

### I1-I6 Checker (VERIFIED)
- Location: projects/evaluation/tlc_evals/invariants/
- Checks: deterministic pattern checks for all 6 TLC invariants
- Status: VERIFIED — passes on clean surfaces

## Running Evals

```bash
# Install
cd projects/evaluation
pip install -e .

# Pattern-only (no API key, deterministic)
tlc-evals check --invariant I1 --file research/evidence-ledger.md

# Full suite
tlc-evals run --suite eval_specs/invariant_suite.yaml --pattern-only

# SARIF output for CI
tlc-evals run --suite eval_specs/invariant_suite.yaml --output sarif > verification/evals.sarif
```

## Regression Gate

The regression gate in packages/tlc-research-kernel/src/regression-gate.ts
blocks promotion if pass_rate drops more than 5% below baseline (1.0).
Baseline: 212/212 passing (evidence_basis: VERIFIED, VR-V-15C6).

## Adding New Evals

1. Create a YAML spec in projects/evaluation/tlc_evals/eval_specs/
2. Add an entry to research/registry/eval_suites.json
3. Run the suite and update evidence_basis field
4. evidence_basis must be VERIFIED before adding to promotion gates
