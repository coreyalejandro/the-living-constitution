# Build Contract: TLC Golden Sandbox (sandbox-runtime-001)

## Current State (Honest)

- Integrated overlay at `projects/sandbox-runtime/` with `PROJECT_TOPOLOGY.json`, `build_contract.md`, and `src/*.py` (Python 3 governed execution cell: engine, jail, governance connector, evidence ledger).
- Standalone mirror at `standalone/tlc-sandbox-app/` with `.tlc/PROJECT_TOPOLOGY.json`, `README.md`, and `core/*.py` (byte-identical to `src/` under `--strict`).
- Dual-topology verification: `scripts/verify_topology.py` (optional `--strict` for INVARIANT_16 core parity).
- **INVARIANT_04:** `src/jail.py` — path boundary under `projects/sandbox-runtime/` and `standalone/tlc-sandbox-app/`; whitelisted imports (`math`, `json`, `time`) for `safe_exec_script`.
- **Halt plane:** `src/governance_connector.py` reads repo-root `STATUS.json`; if `sandbox_operational_state` is `OFF` or `QUARANTINE`, process exits with log `HALT_BY_CONSTITUTIONAL_AUTHORITY` (stderr). If your workflow regenerates `STATUS.json` via `scripts/render_status_surface.py`, coordinate how that key is preserved or use env/sentinel halt (`TLC_HALT_AUTHORITY`, `TLC_HALT_SENTINEL_FILE`) for tests without mutating the rendered surface.
- **INVARIANT_06:** `verification/SANDBOX_LOG.md` — Gold Star ledger (timestamp, actor, action, result, SHA-256 of `THE_LIVING_CONSTITUTION.md`).
- **R&D loop:** `propose_invariant.py` writes drafts under `03-enforcement/drafts/`.

## Target State (What Governance Claims)

- **Dual topology:** `project_id` identical in integrated and standalone identity files; `topology_status` complete in registry; strict mirror of `src/` and `core/`.
- **Lower Sandbox:** Constitutional halt + in-process halt; namespace jail for script paths and imports; append-only JSONL evidence; CPU/memory ceilings via `resource` module.

## Acceptance Criteria

1. `python3 scripts/verify_topology.py --root <tlc-root>` exits 0 when both `PROJECT_TOPOLOGY.json` files exist and `project_id` matches.
2. `python3 scripts/verify_topology.py --root <tlc-root> --strict` exits 0 when `src/*.py` and `core/*.py` are byte-identical.
3. `cd projects/sandbox-runtime && PYTHONPATH=. python3 -m src` runs without error and writes evidence lines under the system temp directory.
4. `SandboxEngine.execute_script("samples/safe.py")` succeeds; traversal outside jail and `samples/evil_import.py` are blocked; ledger rows appended.
5. `SandboxEngine.halt()` stops the execution loop when invoked (or when `TLC_HALT_AUTHORITY` is truthy).

## Evidence Required

```bash
python3 scripts/verify_topology.py --root . --strict
cd projects/sandbox-runtime && PYTHONPATH=. python3 -m src
# Optional: halt via environment
TLC_HALT_AUTHORITY=1 PYTHONPATH=projects/sandbox-runtime python3 -c "from src.engine import SandboxEngine; e=SandboxEngine(); print(e.run_execution_loop(lambda i: None, max_iterations=5))"
# Optional: constitutional halt (add to STATUS.json): "sandbox_operational_state": "OFF"
```

## Implementation Spec

- **Halt:** `SandboxEngine.halt()`, `TLC_HALT_AUTHORITY`, optional `TLC_HALT_SENTINEL_FILE`; `STATUS.json` key `sandbox_operational_state` (`ON` default if omitted; `OFF` / `QUARANTINE` => immediate `sys.exit(0)` after `HALT_BY_CONSTITUTIONAL_AUTHORITY`).
- **Evidence:** JSON lines in `tempfile.gettempdir()/tlc_sandbox_evidence.jsonl`; markdown ledger `verification/SANDBOX_LOG.md` with constitutional SHA-256.
- **Ceilings:** `RLIMIT_CPU` (60s soft/hard), `RLIMIT_AS` or `RLIMIT_DATA` (512 MiB) best-effort.
- **Module entry:** `python -m src` from `projects/sandbox-runtime`; `python -m core` from `standalone/tlc-sandbox-app` (both require `PYTHONPATH=.`).

## Repo Path

- **Integrated:** `projects/sandbox-runtime` (this overlay).
- **Standalone:** `standalone/tlc-sandbox-app` (in-TLC mirror; may be split to its own remote later).
