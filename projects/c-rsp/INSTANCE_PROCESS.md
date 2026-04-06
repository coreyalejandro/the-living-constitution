# Instantiated Process
## Single-Instance, Verifier-Backed Governance Execution

**Artifact role:** **Workflow / helper only** — describes an optional authoring process. **Not** the canonical master template (`projects/c-rsp/BUILD_CONTRACT.md`), **not** a truth surface, **not** authoritative over `contract-schema.json` or `CRSP_OUTCOME_TEMPLATE.md`. Same subordination as `projects/c-rsp/workflows/*` (**INVARIANT_SEM_03**).

### Objective

Instantiate governance through a fixed-shape, schema-validated, profile-derived contract artifact rather than a human mental merge.

### Process

1. Select constitutional master template (`BUILD_CONTRACT.md`).
2. Select overlay profile (e.g. `PASS8_TEMPLATE.md` for satellites).
3. Generate `BUILD_CONTRACT.instance.md` from `BUILD_CONTRACT.instance.template.md` (or equivalent generator).
4. Populate all required fields; resolve every `[REQUIRED]` before calling the instance executable.
5. Validate against `contract-schema.json` (section order, titles, required fields, topology/verifier alignment).
6. Generate or verify `governance-template.lock.json` (pins must match declared paths and versions in the instance).
7. Run preflight (placeholders resolved, terminology, topology, verifier class, evidence paths, risk/control consistency).
8. Execute the verifier class appropriate to topology (see **Verifier invocation** below).
9. Record lifecycle transition evidence on the declared truth surface.
10. Promote only when acceptance criteria and truth-surface evidence are satisfied and frozen-context rules allow verified claims.

### Outcome report (required)

Emit each execution summary from `projects/c-rsp/CRSP_OUTCOME_TEMPLATE.md`: **H1** `C-RSP Build Contract : {BUILD_CONTRACT_TITLE} — {COMPONENT}`, **H2** `Constitutionally-Regulated Single Pass Executable Prompt (Framework)`, then Kanban, anchor, V&T. `BUILD_CONTRACT_TITLE` must match the governing contract’s title (instance Section 1, or zero-shot `# Build Contract: …` tail).

### Profile / topology branching

| Topology Mode   | Verifier class             | Typical extra checks                          |
|-----------------|----------------------------|-----------------------------------------------|
| TLC-Core        | core-verifier              | Full TLC topology + governance chain          |
| Satellite       | satellite-verifier         | Institutionalization + no illicit core claims |
| Dual-Topology   | dual-topology-verifier     | Both integrated and standalone paths explicit |

If `Topology Mode` and `Verifier Class` disagree with `contract-schema.json` `topology_verifier_alignment`, halt.

### Verifier invocation (reference)

- **Satellite (PASS 8):** `python3 scripts/verify_governance_chain.py --root .` then `python3 scripts/verify_institutionalization.py --root .` (see profile for full CI ordering).
- **TLC-Core:** use TLC’s full verifier suite including topology as defined in the parent repo; do not use satellite shortcuts.

Commands must match what the governed repo actually ships; the instance’s Preflight section must name the real entrypoints.

### Deterministic Guards

- no placeholders in executable instance
- canonical terminology only (`C-RSP` expansion fixed)
- exact core section order and titles per schema
- topology and verifier class aligned
- risk/control block complete and consistent with conditional stop/override rule
- rollback/recovery present when tier or risk/side-effect triggers require it
- lifecycle transition legal per `lifecycle_transitions` in schema
- lock manifest present and consistent for Tier-3; recommended for Tier-2 satellites using pins

### State Machine

- Draft → Active → Frozen → Superseded

### Evidence Outputs

- instance artifact
- validation report
- preflight report
- verifier report
- lifecycle transition record
- rollback record if triggered

### Failure branches

| Failure                         | Default behavior                                      |
|---------------------------------|-------------------------------------------------------|
| Schema validation error         | Halt; remain Draft; no promotion claims               |
| Preflight failure               | Halt; fix inputs; re-run preflight                    |
| Verifier failure                | Halt; capture report on truth surface; no promotion   |
| Illegal lifecycle transition    | Halt; audit event; revert state declaration if needed |
| Placeholder detected late       | Treat as schema/preflight failure                    |

### Rollback trigger flow

1. Detect halt or failed promotion (verifier or policy).
2. Execute rollback procedure declared in instance §10 (safe state, authority, evidence path).
3. Write rollback evidence to declared path; set contract status truthfully (typically Draft or prior Frozen).
4. Do not assert verified provenance on mutable branch tips until re-qualified.

### Closeout Rule

The process is complete only when:

1. instance artifact exists
2. schema validation passes
3. preflight passes
4. verifier passes for the declared topology
5. lifecycle transition evidence is recorded
6. promotion status is truthfully declared on the truth surface (frozen-context rules respected for verified claims)

### Follow-on Implementation Notes

- Tier-1 repos may stop after schema-valid instance + preflight pass
- Tier-2 repos must include operational controls and rollback semantics
- Tier-3 repos must include dependency graphing, lock manifest, and audit-grade evidence ledger
