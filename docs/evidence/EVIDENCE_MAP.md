---
document_type: "Evidence"
id: "DOC-EVID-MAP-001"
repo_scope: "TLC-Core"
authority_level: "L3"
truth_rank: 2
status: "Active"
canonical_path: "docs/evidence/EVIDENCE_MAP.md"
next_file: "docs/operations/VERIFY.md"
last_verified:
  commit: "af9dfb8"
  timestamp: "2026-04-04T12:00:00Z"
metadata:
  est_time_minutes: 8
  cognitive_load: "Low"
  requires_interruption_buffer: false
navigation:
  parent_index: "docs/INDEX.md"
  hierarchy_level: "TLC > Evidence > Map"
---

# Evidence map

| Artifact | What it proves | Standard |
| --- | --- | --- |
| `docs/evidence/verification/2026-04-04-docs-governance-smoke.md` | Documentation verifier ran with recorded result | `docs/constitution/DOCUMENTATION_STANDARD.md` |
| `verification/docs_compliance.json` | Repo compliance score artifact (CI) | MVDS + extended paths in `config/docs_governance.json` |
| `verification/MATRIX.md` | Resume and application claim mapping | TLC verification policy |

## Real verification entry points

1. Open `docs/evidence/verification/2026-04-04-docs-governance-smoke.md` for commit-bound smoke evidence.
2. Run `python3 scripts/compliance_score_docs.py --root .` for live scoring output.
