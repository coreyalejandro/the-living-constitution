# TLC Research Workbench — First Run Guide

evidence_basis: CONSTRUCTED — derived from TLC-RDI-MVP-001 contract.

## Prerequisites

- Node.js 20+, pnpm 9.15+
- Python 3.11+ for eval runner
- CGL repo cloned at ../cognitive-governance-lab/ (sibling of TLC)

## Start the control plane

```bash
cd apps/tlc-control-plane
pnpm install
pnpm dev
# Open http://localhost:3000
```

## Run research workbench smoke test

```bash
# From TLC root
pnpm research:smoke
```

This runs: governance chain verifier + topology verifier + guardian health check.

## Run evals

```bash
# Pattern-only (deterministic, no API key required)
pnpm research:eval

# Full model eval (requires ANTHROPIC_API_KEY)
cd projects/evaluation
tlc-evals run --suite invariant_suite.yaml
```

## Register a CGL experiment

Add an entry to research/registry/experiments.json:

```json
{
  "id": "CW-EXP-001",
  "title": "Contract Window intent-drift pilot",
  "proposal_ref": "Proposal-I",
  "research_question": "Does CW reduce intent-drift >= 25%?",
  "hypotheses": ["H1: drift reduction >= 25%"],
  "conditions": [{"id": "control", "has_contract_window": false, "session_count": 0}],
  "status": "planned",
  "evidence_basis": "CONSTRUCTED",
  "registered_at_utc": "2026-05-01T00:00:00Z",
  "cgl_path": "../cognitive-governance-lab/governance-kernel/"
}
```

## Rollback

See docs/research/ROLLBACK.md.
All workbench UI is additive — rollback = delete the app/[route] dir.
Constitutional surfaces (THE_LIVING_CONSTITUTION.md, STATUS.json) are never touched by workbench ops.
