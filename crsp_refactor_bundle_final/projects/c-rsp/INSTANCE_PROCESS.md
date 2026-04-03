# Instantiated Process
## Single-Instance, Verifier-Backed Governance Execution

### Objective

Instantiate governance through a fixed-shape, schema-validated, profile-derived contract artifact rather than a human mental merge.

### Process

1. Select constitutional master template.
2. Select overlay profile.
3. Generate `BUILD_CONTRACT.instance.md`.
4. Populate all required fields.
5. Validate against `contract-schema.json`.
6. Generate or verify `governance-template.lock.json`.
7. Run preflight.
8. Execute verifier class appropriate to topology.
9. Record lifecycle transition evidence.
10. Promote only when acceptance criteria and truth-surface evidence are satisfied.

### Deterministic Guards

- no placeholders
- canonical terminology only
- exact section order preserved
- topology and verifier class aligned
- risk/control block complete
- rollback/recovery present when required
- lifecycle transition legal
- lock manifest present for Tier-3

### State Machine

- Draft → Active → Frozen → Superseded

### Evidence Outputs

- instance artifact
- validation report
- preflight report
- verifier report
- lifecycle transition record
- rollback record if triggered

### Closeout Rule

The process is complete only when:

1. instance artifact exists
2. schema validation passes
3. preflight passes
4. verifier passes for the declared topology
5. lifecycle transition evidence is recorded
6. promotion status is truthfully declared

### Follow-on Implementation Notes

- Tier-1 repos may stop after schema-valid instance + preflight pass
- Tier-2 repos must include operational controls and rollback semantics
- Tier-3 repos must include dependency graphing, lock manifest, and audit-grade evidence ledger
