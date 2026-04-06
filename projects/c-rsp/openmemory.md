# C-RSP Open Memory — execution journal

**Artifact role:** Helper only (row 5 in `CANONICAL_ROLE_MAP.md`). Does not override `projects/c-rsp/BUILD_CONTRACT.md` or `contract-schema.json`.

## Relationship to root `openmemory.md`

- **`openmemory.md`** (repository root) — Long-lived **TLC project index**: components, patterns, and repo-wide continuity. **Read this first** for super-repo context.
- **`projects/c-rsp/openmemory.md`** (this file) — **Append-only C-RSP run log**: short entries per contract session. Do not replace or duplicate the root guide here.

## Rules

- Append new entries under **Active log**; do not rewrite prior entries.
- Each entry uses the template in `AGENT_PROMPT.md` (Session Close).
- Optional: when a run touches only C-RSP paths, one line may point readers to root `openmemory.md` for TLC-wide updates.

## Active log

### 2026-04-06T00:00:00Z — HYBRID-MEMORY-SEED — manual

- **Contract:** (governance hygiene — no single executed instance)
- **Outcome:** PASS
- **Key decisions:** Adopted hybrid memory: root `openmemory.md` = TLC index; this file = C-RSP append-only journal. `AGENT_PROMPT.md` pre-flight updated to require both reads; session appends stay on this path only.
- **Unresolved:** None for this seed.
- **Files touched:** `projects/c-rsp/openmemory.md`, `projects/c-rsp/AGENT_PROMPT.md`
- **Next:** See `projects/c-rsp/NEXT_CRSP_BUILD.json`
