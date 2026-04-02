# Sandbox Evidence Ledger (Gold Star)

Structured audit trail for Lower Sandbox actions. One row per execution event.

| Timestamp (ISO 8601) | Actor | Action | Result | Constitutional Hash (SHA-256) |
|----------------------|-------|--------|--------|--------------------------------|
| 2026-04-02T22:05:00Z | project_id: sandbox-runtime-001 | Initialized ledger | Success | `3d650ff9e6390b65db21a85c3de3dc9fbd6a386850994d330c54d7e4badd7590` |
| 2026-04-02T22:05:00Z | project_id: sandbox-runtime-001 | Executed samples/safe.py | Success | `3d650ff9e6390b65db21a85c3de3dc9fbd6a386850994d330c54d7e4badd7590` |
| 2026-04-02T22:05:00Z | project_id: sandbox-runtime-001 | Executed samples/evil_import.py | Fail | `3d650ff9e6390b65db21a85c3de3dc9fbd6a386850994d330c54d7e4badd7590` |
| 2026-04-02T22:25:06Z | project_id: sandbox-runtime-001 | Executed samples/breach_import.py (INVARIANT_05) | Fail | `3d650ff9e6390b65db21a85c3de3dc9fbd6a386850994d330c54d7e4badd7590` |
| 2026-04-02T22:25:06Z | project_id: sandbox-runtime-001 | Executed ../../../THE_LIVING_CONSTITUTION.md (INVARIANT_04) | Fail | `3d650ff9e6390b65db21a85c3de3dc9fbd6a386850994d330c54d7e4badd7590` |
| 2026-04-02T22:25:06Z | project_id: sandbox-runtime-001 | Executed samples/evil_import.py (INVARIANT_05) | Fail | `3d650ff9e6390b65db21a85c3de3dc9fbd6a386850994d330c54d7e4badd7590` |
| 2026-04-02T22:25:20Z | project_id: sandbox-runtime-001 | Executed samples/breach_import.py (INVARIANT_05) | Fail | `3d650ff9e6390b65db21a85c3de3dc9fbd6a386850994d330c54d7e4badd7590` |
| 2026-04-02T22:25:20Z | project_id: sandbox-runtime-001 | Executed ../../../THE_LIVING_CONSTITUTION.md (INVARIANT_04) | Fail | `3d650ff9e6390b65db21a85c3de3dc9fbd6a386850994d330c54d7e4badd7590` |
| 2026-04-02T22:25:20Z | project_id: sandbox-runtime-001 | Executed samples/evil_import.py (INVARIANT_05) | Fail | `3d650ff9e6390b65db21a85c3de3dc9fbd6a386850994d330c54d7e4badd7590` |
