---
document_type: "Evidence"
id: "DOC-EVID-SMOKE-001"
repo_scope: "TLC-Core"
authority_level: "L3"
truth_rank: 2
status: "Active"
canonical_path: "docs/evidence/verification/2026-04-04-docs-governance-smoke.md"
next_file: "docs/evidence/EVIDENCE_MAP.md"
last_verified:
  commit: "af7ec64"
  timestamp: "2026-04-22T17:18:42Z"
metadata:
  est_time_minutes: 4
  cognitive_load: "Low"
  requires_interruption_buffer: false
navigation:
  parent_index: "docs/evidence/EVIDENCE_MAP.md"
  hierarchy_level: "TLC > Evidence > Verification > Smoke"
---

# Documentation governance smoke verification

## What was validated

- `scripts/verify_document_constitution.py` executes against the repository tree.
- MVDS paths declared in `config/docs_governance.json` exist.
- Root Markdown allowlist rules apply without false positives for known root files.

## Standard

- `docs/constitution/DOCUMENTATION_STANDARD.md`
- `config/docs_governance.json` (MVDS list)

## Commit

- **Recorded HEAD:** `e16c574f58adc4f7f74ebc49682eee2402d4b5d9` (short: `e16c574`)

## Result

- **Outcome:** PASS — verifier exits 0 when run as:

```bash
python3 scripts/verify_document_constitution.py --root .
```

- **Recorded at:** `2026-04-04T12:00:00Z` (declared; re-run after any doc governance change)

## Evidence chain

- Map: `docs/evidence/EVIDENCE_MAP.md`
- Compliance artifact (generated): `verification/docs_compliance.json` after running `scripts/compliance_score_docs.py`
