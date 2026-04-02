# Stress Test Report (SANDBOX-BREACH-SIM)

- **TLC root:** `/Users/coreyalejandro/Projects/the-living-constitution`
- **Constitutional SHA-256:** `3d650ff9e6390b65db21a85c3de3dc9fbd6a386850994d330c54d7e4badd7590`
- **New FAIL rows (since driver start):** 3 (require >= 3)
- **HALT circuit:** PASS (exit 0)

## Breach scripts

- **breach_import blocked (ImportError):** PASS — import of 'os' is not permitted (whitelist: ['json', 'math', 'time'])
- **breach_path constitution traversal blocked:** PASS — path traversal is forbidden in the Lower Sandbox
- **evil_import blocked (ImportError):** PASS — import of 'os' is not permitted (whitelist: ['json', 'math', 'time'])

## Halt subprocess

```
HALT_BY_CONSTITUTIONAL_AUTHORITY
```

## Ledger checks

- Three new FAIL rows: yes
- INVARIANT_04 present: yes
- INVARIANT_05 present: yes
- Constitutional hash in log: yes

**Overall:** PASS

