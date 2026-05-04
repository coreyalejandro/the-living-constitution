# TLC Research Workbench Architecture

evidence_basis: CONSTRUCTED — derived from TLC-RDI-MVP-001 contract and TLC-CGL-BOUNDARY.md.

## The One-Line Rule

TLC governs the arc. CGL runs the experiment.

This workbench is a READ surface for CGL outputs, not a research instrument itself.

## Component Map

```
the-living-constitution/
├── apps/tlc-control-plane/         # Next.js control plane (UI)
│   └── app/
│       ├── research/               # Research workbench — experiment registry viewer
│       ├── experiments/            # Session outcomes from CGL
│       ├── evals/                  # Constitutional eval suite results
│       ├── evidence/               # Evidence ledger viewer
│       ├── corpus/                 # Corpus governance viewer
│       └── improvement/            # Bounded self-improvement proposals
├── packages/tlc-research-kernel/   # TypeScript kernel (types + utilities)
│   └── src/
│       ├── experiment-schema.ts    # Types: ExperimentRecord, SessionOutcome, etc.
│       ├── eval-runner.ts          # EvalSuiteResult parser (read-only)
│       ├── constitutional-critic.ts # I1-I6 violation checker
│       ├── improvement-proposer.ts # Proposal creation + protected surface guard
│       ├── regression-gate.ts      # pass_rate regression checker
│       └── provenance.ts           # I4 traceability chain
└── research/registry/              # JSON evidence registries
    ├── baseline_inventory.json     # Pre-flight truth anchor
    ├── experiments.json            # Registered CGL experiments
    ├── eval_suites.json            # Eval suite run history
    ├── corpora.json                # Corpus provenance + consent records
    └── improvement_proposals.json  # Pending proposals (human approval required)
```

## Dependency Arrow

cognitive-governance-lab --> the-living-constitution

CGL runs the experiments. TLC provides the constitutional framework and surfaces
the results. TLC does not run experiments. TLC does not contain research claims.

## The Boundary (authoritative: research/TLC-CGL-BOUNDARY.md)

TLC MAY:
- Add research workbench UI for VIEWING CGL outputs and evidence
- Add eval runner for RUNNING constitutional compliance checks on TLC itself
- Add governance surfaces that VALIDATE CGL methodology against constitutional rules

TLC MUST NOT:
- Move governance-kernel, experiment harness, or proposal content from CGL into TLC
- Create a tlc-research-kernel that duplicates CGL's governance-kernel
- Blur the enforcement/research boundary in any STATUS surface

## Navigation (from control plane)

/             — STATUS.json truth surface + system graph
/research     — Research workbench (experiment registry)
/experiments  — Session outcome history
/evals        — Constitutional eval suite results
/evidence     — Evidence ledger viewer
/corpus       — Corpus governance
/improvement  — Bounded self-improvement proposals
