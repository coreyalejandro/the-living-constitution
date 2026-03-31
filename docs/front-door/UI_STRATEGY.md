# UI strategy: dense multi-panel control plane

## Scope and artifact owner

**Scope:** Conceptual UX for the TLC control-plane interface.  
**Artifact path:** `docs/front-door/UI_STRATEGY.md`  
**Invariant mapping:** INVARIANT_04 (non-wired surfaces labeled), INVARIANT_10 (App Router conventions for scaffold).

## Current state versus intended state

| Aspect | Current state | Intended state |
| --- | --- | --- |
| Implementation | If present, `apps/tlc-control-plane/` uses static snapshot data and explicit scaffold labels | Richer interactions: live status refresh from approved pipelines, navigable graph, filtered verification timeline |
| Visual density | Shell arranges four primary regions in a single viewport-style layout | Same IA with production polish: responsive breakpoints, keyboard focus order, reduced motion option |

## Design metaphor

The interface is modeled conceptually after an **AI studio** or **operations control plane**: a **dense, multi-panel** layout where governance truth, system topology, execution sequencing, and verification evidence are visible together. The goal is **situational awareness** for a maintainer or reviewer, not consumer-style minimalism.

## Panel roles (canonical vocabulary)

1. **System graph** — Shows nodes and edges for Commonwealth projects, domains, and key evidence paths. Scaffold stage: static diagram or simplified representation with explicit non-live labeling.
2. **Status/truth panel** — Displays selected fields from `STATUS.json` and pointers to policy files. Must remain subordinate to JSON authority.
3. **Execution pane** — Summarizes active sequencing (e.g., UI-first roadmap) and links to build contracts. Scaffold: static text derived from repo docs.
4. **Verification stream** — Lists verification artifacts and run identifiers as **documentation-backed** entries. Not presented as a real-time telemetry feed unless explicitly implemented.

## Non-functional regions

Any region that does not call verified services or read live data must be labeled per contract: **Static shell scaffold — not yet wired**.

## Accessibility and clarity

- Headings and panel titles use plain language.  
- Color is not the only channel for state; use text labels for panel identity.  
- Future work: focus order left-to-right or top-to-bottom matching visual priority.

## Verification hook

- Inspect `apps/tlc-control-plane/app/page.tsx` and panel components for four named regions and scaffold labels when scaffold exists.
