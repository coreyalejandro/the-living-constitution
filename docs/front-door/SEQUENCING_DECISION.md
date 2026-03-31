# Sequencing decision: UI first, teaser video second, integration third

## Scope and artifact owner

**Scope:** Resolved build order for transition and product surfaces.  
**Artifact path:** `docs/front-door/SEQUENCING_DECISION.md`  
**Invariant mapping:** INVARIANT_08, INVARIANT_12.

## Decision

Build order is explicitly:

1. **UI first** — Establish the TLC control-plane shell and documentation package so identity, IA, and panel semantics exist before dependent media or integrations.  
2. **Teaser video second** — Produce the Remotion deliverable under `projects/teaser-video/` per its build contract after the front-door UI and docs stabilize the narrative and sequencing language.  
3. **Product-surface integration third** — Connect live verification feeds, dynamic graphs, and project actions only after the static governance story and teaser asset exist.

## Rationale

- **Truth before motion:** UI and docs anchor canonical vocabulary (`control plane`, `status/truth panel`, `system graph`, `execution pane`, `verification stream`) before video script and shots reference them.  
- **Evidence discipline:** Integration work touches CI, artifacts, and possibly secrets; deferring it avoids claiming live capability prematurely.  
- **Maintenance-mode alignment:** Sequencing avoids implying a new governance pass; it is product and media execution only.

## Current state versus intended state

| Phase | Current state | Intended state |
| --- | --- | --- |
| UI first | Scaffold and `docs/front-door/` package delivered | Hardened UI with approved data bindings |
| Teaser video second | Project exists under `projects/teaser-video/` | Completed render aligned to contracts |
| Integration third | Not in scope for this contract | Wired streams and graph sources |

## Verification hook

- This file explicitly states **UI first, teaser video second** for AC-12.  
- Cross-read `EXECUTION_ROADMAP.md` for phased deliverables.
