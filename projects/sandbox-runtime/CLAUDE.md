# CLAUDE.md — TLC Golden Sandbox

## What This Is

Governance overlay for **sandbox-runtime-001**: governed Python execution cell (`src/engine.py`) with halt authority, **namespace jail** (`src/jail.py`), **STATUS.json** halt polling (`src/governance_connector.py`), **Gold Star ledger** (`verification/SANDBOX_LOG.md` via `src/evidence_ledger.py`), evidence JSONL, and resource ceilings.

## Dual Topology

- Integrated: `projects/sandbox-runtime/PROJECT_TOPOLOGY.json`
- Standalone: `standalone/tlc-sandbox-app/.tlc/PROJECT_TOPOLOGY.json`

Verify with `python3 scripts/verify_topology.py --root <tlc-root>` (add `--strict` for byte-identical `src/` vs `core/`).

## Run

```bash
cd projects/sandbox-runtime && PYTHONPATH=. python3 -m src
```

## Living Constitution

Articles I–V apply. This package does not claim remote CI success; evidence is local append-only JSONL under the system temp directory plus repo-root `verification/SANDBOX_LOG.md` when `tlc_root` resolves to the TLC checkout.
