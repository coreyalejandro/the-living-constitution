# tlc_semgraph

Structural world-model engine for TLC governance (v0).

## Current capabilities

- Builds a file-level import graph for TS/TSX/JS/JSX under a `--source-root`.
- Computes BFS ripple closure for a git diff between two refs.
- Emits schema-valid `ImpactReport` artifacts under `verification/semgraph/runs/`.

