<!-- markdownlint-disable MD013 -->
# C-RSP Build Contract : `CRSP-SEMGRAPH-001` — `apps/tlc_semgraph` (Semantic Graph Engine, P1)
## Constitutionally-Regulated Single Pass Executable Prompt (Framework)

**Artifact role:** Outcome artifact for the semantic graph engine base-camp contract. Subordinate to `projects/c-rsp/BUILD_CONTRACT.md`.

**Contract instance:** `projects/c-rsp/instances/CRSP-SEMGRAPH-001.md`
**Run id / commit:** `c350af4`

### Quick V&T lines (minimum contract closure)

- **Exists:** `apps/tlc_semgraph/` Python package (engine + CLI), `verification/semgraph/ImpactReport.schema.json`, `verification/semgraph/ShadowDrift.schema.json`, two schema-valid `verification/semgraph/runs/*.json` artifacts produced by the CLI.
- **Verified against:** `python3 -m apps.tlc_semgraph.api.cli` produced `ImpactReport-diff-d51a62d36498.json` and `P1-build-71b8bb50b522.json`; `python3 scripts/semgraph_p1_spike.py` validated both artifacts against `ImpactReport.schema.json` exit 0.
- **Not claimed:** No claim of AST-level precision. The P1 engine is regex import-graph only and operates at file granularity.
- **Non-existent:** No tree-sitter parser, no cross-language resolver, no hot-reload watcher, no Guardian strict enforcement (delivered under `CRSP-SEMGRAPH-GUARDIAN-001`).
- **Unverified:** Large-repo scalability, non-Python import idioms, non-regular import syntaxes.
- **Functional status:** **PASS** for the declared P1 scope: descriptive structural evidence surface exists, is schema-governed, and is produced deterministically by a CLI.

---

## 1. Constitutional anchor (brief; before V&T)

| Source | Requirement |
|--------|-------------|
| **Article I — Right to Truth** | ImpactReport is the evidence surface; no stronger claim than what the schema validates. |
| **Article III — Verification Before Done** | Acceptance requires schema-valid artifacts produced by the engine, not narrative. |
| **Section 16 Output Format** | Kanban-first V&T; single executed contract. |

---

## 2. V&T Statement

### 2.1 Visual board (Kanban) — REQUIRED FIRST

```text
┌─────────────────────────────┬───────────────────┬──────────────────────────────────────────┬────────────┐
│           BACKLOG           │    IN PROGRESS    │                  DONE                    │  BLOCKED   │
├─────────────────────────────┼───────────────────┼──────────────────────────────────────────┼────────────┤
│ tree-sitter unit-level      │ (none)            │ ImpactReport.schema.json                 │ (none)     │
│ ripple                      │                   │ ShadowDrift.schema.json                  │            │
│ cross-language resolver     │                   │ apps/tlc_semgraph engine + CLI            │            │
│ hot-reload watcher          │                   │ two schema-valid runs under              │            │
│                             │                   │ verification/semgraph/runs/              │            │
└─────────────────────────────┴───────────────────┴──────────────────────────────────────────┴────────────┘
```

**Signals (required, one line each)**

| Signal | Value |
|--------|-------|
| **Build result** | `PASS` |
| **What moved** | Semantic graph P1 engine shipped; `ImpactReport` surface live and schema-governed. |
| **What's next** | Guardian binding delivered in `CRSP-SEMGRAPH-GUARDIAN-001`. No further semgraph expansion is claimed in this contract. |

### 2.2 Exists

**Exists**

- `apps/tlc_semgraph/engine/import_graph.py` — regex import-graph builder (file-level).
- `apps/tlc_semgraph/engine/ripple.py` — BFS ripple computation over the import graph.
- `apps/tlc_semgraph/api/cli.py` — CLI producing `build` snapshot and `diff` ImpactReport artifacts.
- `verification/semgraph/ImpactReport.schema.json` — JSON Schema (Draft 2020-12) with optional `meta` object.
- `verification/semgraph/ShadowDrift.schema.json` — drift artifact schema.
- `verification/semgraph/runs/ImpactReport-diff-d51a62d36498.json` — schema-valid diff run.
- `verification/semgraph/runs/P1-build-71b8bb50b522.json` — schema-valid build run.

### 2.3 Verified against

**Verified against**

- `python3 -m apps.tlc_semgraph.api.cli diff --base HEAD~1 --head HEAD` → wrote `ImpactReport-diff-*.json` exit 0.
- `python3 -m apps.tlc_semgraph.api.cli build` → wrote `P1-build-*.json` exit 0.
- `python3 scripts/semgraph_p1_spike.py` → validated both artifacts against `ImpactReport.schema.json` exit 0.

### 2.4 Not claimed

**Not claimed**

- No claim of symbol-level (function/class) ripple accuracy.
- No claim of behavioral equivalence with a tree-sitter implementation.
- No claim of coverage for dynamic imports (`importlib`, string-based import), wildcard re-exports, or C extensions.

### 2.5 Non-existent

**Non-existent**

- Tree-sitter parser: not implemented in this contract.
- Cross-language (TS/Go/Rust) resolver: not implemented.
- Daemonized file watcher: not implemented.

### 2.6 Unverified

**Unverified**

- Scalability on large monorepos (>10k files) — not measured.
- Non-ASCII path handling — not stressed.

### 2.7 Functional status

**Functional status**

- `PASS` for declared P1 scope: deterministic structural evidence surface exists, is schema-governed, and is produced by a CLI anyone can run.

---

*End of report. No narrative after **Functional status**.*
