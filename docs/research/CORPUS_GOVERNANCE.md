# TLC Research Workbench — Corpus Governance

evidence_basis: CONSTRUCTED — derived from TLC-RDI-MVP-001 provenance policy.

## Policy

All corpora in research/registry/corpora.json must have:
- source: path or URL of origin data
- consent_status: "synthetic", "consented", "public-domain", or "IRB-approved"
- evidence_basis: VERIFIED | CONSTRUCTED | PENDING

No corpus may be used in an experiment with evidence_basis: PENDING if the
experiment's claims will be presented as VERIFIED.

## Current Corpora

### PILOT-SYNTHETIC-001 (CONSTRUCTED)
- 10 synthetic sessions (PILOT-S001 through PILOT-S010)
- Location: cognitive-governance-lab/datasets/pilot/
- kappa: 0.6267 — BELOW 0.70 gate threshold
- Gate status: FAILED — empirical validation pending

## Adding a Corpus

1. Confirm consent_status with data owner
2. Add entry to research/registry/corpora.json
3. Set evidence_basis: CONSTRUCTED until kappa gate is passed
4. Pass kappa >= 0.70 to promote to VERIFIED

## Human Subjects (IRB)

For RQ3 in Proposal III (neurodivergent user alignment), IRB approval is
required before collecting human subject data. This is a Year 2 deliverable.
No human subjects data may be added to corpora.json without an IRB approval
reference.
