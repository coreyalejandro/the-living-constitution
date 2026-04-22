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
  commit: "7f42c11"
  timestamp: "2026-04-22T17:54:13Z"
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
| `docs/evidence/verification/2026-04-05-mvp-closeout-ci-run.md` | MVP closeout AC-05 — remote CI run id and commit | `projects/document-system/BUILD_CONTRACT.instance.MVP-CLOSEOUT-001.md` |
| `docs/evidence/verification/2026-04-05-mvp-ac06-frontmatter-schemas.md` | MVP closeout AC-06 — frontmatter JSON Schema enforcement | `projects/document-system/BUILD_CONTRACT.instance.MVP-CLOSEOUT-001.md` |
| `docs/evidence/verification/WAIVER-MVP-AC07.md` | MVP closeout AC-07 — waiver of automated migration `--apply` | `projects/document-system/BUILD_CONTRACT.instance.MVP-CLOSEOUT-001.md` |
| `verification/docs_compliance.json` | Repo compliance score artifact (CI) | MVDS + extended paths in `config/docs_governance.json` |
| `verification/MATRIX.md` | Resume and application claim mapping | TLC verification policy |

## Real verification entry points

1. Open `docs/evidence/verification/2026-04-04-docs-governance-smoke.md` for commit-bound smoke evidence.
2. Run `python3 scripts/compliance_score_docs.py --root .` for live scoring output.
