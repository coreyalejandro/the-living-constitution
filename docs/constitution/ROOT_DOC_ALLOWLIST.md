---
document_type: "Constitutional"
id: "DOC-ROOT-ALLOW-001"
repo_scope: "Cross-Repo"
authority_level: "L4"
truth_rank: 1
status: "Active"
canonical_path: "docs/constitution/ROOT_DOC_ALLOWLIST.md"
next_file: "docs/constitution/DOC_TRUTH_HIERARCHY.md"
last_verified:
  commit: "cb57d6f"
  timestamp: "2026-04-06T01:00:00Z"
metadata:
  est_time_minutes: 10
  cognitive_load: "Medium"
  requires_interruption_buffer: false
navigation:
  parent_index: "docs/INDEX.md"
  hierarchy_level: "TLC > Constitution > Root Allowlist"
---

# ROOT_DOC_ALLOWLIST

Machine enforcement reads the **literal** and **regex** sections below. Parsing rules are implemented in `scripts/verify_document_constitution.py`.

## Literal allowlist (root filenames)

These exact names may exist at repository root:

- README.md
- LICENSE
- LICENSE.md
- CLAUDE.md
- THE_LIVING_CONSTITUTION.md
- STATUS.md
- HANDOFF.md
- MASTER_PROJECT_INVENTORY.md
- openmemory.md
- ChatGPT-AI Governance Frameworks.md
- delegated-whistling-cherny.md
- AGENTS.md

## Regex allowlist (root path basename)

Patterns match the **entire** basename (anchored).

- `^.*\.json$`
- `^\.env\.example$`
- `^requirements.*\.txt$`

## Prohibited

- New substantive Markdown at root **not** matched by literal or regex sections.
- Shadow copies of canonical docs that belong under `docs/`.
- AI-emitted root guides that duplicate content that must live under `docs/`.

## Validation

Run:

```bash
python3 scripts/verify_document_constitution.py --root .
```
