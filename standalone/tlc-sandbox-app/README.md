# tlc-sandbox-app

Standalone mirror of the **TLC Golden Sandbox** execution substrate (`project_id`: `sandbox-runtime-001`).

## Topology

Identity lives at `.tlc/PROJECT_TOPOLOGY.json` and must match the integrated overlay:

- Integrated: `projects/sandbox-runtime/PROJECT_TOPOLOGY.json` (in the Living Constitution repo)

## Run the engine

From this directory (package root on `PYTHONPATH`):

```bash
PYTHONPATH=. python3 -m core
```

Evidence is appended to `$TMPDIR/tlc_sandbox_evidence.jsonl` (or the platform temp directory). The Gold Star ledger at repo-root `verification/SANDBOX_LOG.md` is written when using the engine from the full TLC checkout.

## Halt authority

- Call `SandboxEngine.halt()` from a TLC script, or
- Set environment variable `TLC_HALT_AUTHORITY=1`, or
- Set `TLC_HALT_SENTINEL_FILE` to a path; if that path exists as a file, the next loop iteration halts.
- Repository-root `STATUS.json`: set `"sandbox_operational_state": "OFF"` or `"QUARANTINE"` to trigger immediate process exit with `HALT_BY_CONSTITUTIONAL_AUTHORITY` on the next poll (stderr).

## Verification

From the Living Constitution repository root:

```bash
python3 scripts/verify_topology.py --root .
python3 scripts/verify_topology.py --root . --strict
```

Exit code `1` indicates a broken dual topology or **Constitutional Breach** (missing identity on either side). `--strict` additionally requires byte-identical `projects/sandbox-runtime/src/*.py` and `standalone/tlc-sandbox-app/core/*.py`.
