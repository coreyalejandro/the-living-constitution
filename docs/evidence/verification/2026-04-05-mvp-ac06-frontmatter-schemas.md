# MVP closeout — AC-06 frontmatter JSON Schemas

**Date (UTC):** 2026-04-05

| Field | Value |
| --- | --- |
| AC | AC-06 |
| Schemas | `schemas/docs_frontmatter_minimal.json`, `schemas/docs_frontmatter_full.json` (Draft 2020-12) |
| Enforcement | `scripts/verify_document_constitution.py` — `Draft202012Validator` after YAML parse; tier chosen by `document_type` vs `config/docs_governance.json` → `header_tiers.minimal` / `header_tiers.full` |
| Failure codes | `FRONTMATTER_SCHEMA_SETUP`, `FRONTMATTER_DOCUMENT_TYPE_UNKNOWN`, `FRONTMATTER_SCHEMA_VIOLATION` |

**Verification:** `python3 scripts/verify_document_constitution.py --root .` → exit `0`, stdout `DOCUMENT_CONSTITUTION_OK`.
