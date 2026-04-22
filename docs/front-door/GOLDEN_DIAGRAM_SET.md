# Golden diagram set: five Mermaid sources

## Scope and artifact owner

**Scope:** Required diagrams, purpose, labels, and Mermaid source ownership.  
**Artifact path:** `docs/front-door/GOLDEN_DIAGRAM_SET.md`  
**Invariant mapping:** INVARIANT_05 (canonical vocabulary).

## Diagram catalog

| ID | File | Purpose | Required labels / concepts |
|----|------|---------|----------------------------|
| D1 | `diagram-sources/system-context.mmd` | TLC repo in context of Commonwealth and external evidence | External reviewer, Commonwealth projects, TLC governance overlay, open interfaces |
| D2 | `diagram-sources/control-plane-architecture.mmd` | Major governance artifacts and flows | `STATUS.json`, verification chain, build contracts, invariant registry pointers |
| D3 | `diagram-sources/execution-loop.mmd` | Human and CI execution loop | Bootstrap, verifiers, attestation, maintenance-mode |
| D4 | `diagram-sources/system-graph.mmd` | Nodes for domains and key repo areas | Domains, `projects/`, `verification/`, `governance/constitution/core/` |
| D5 | `diagram-sources/ui-layout.mmd` | Four-panel UI layout | **system graph**, **status/truth panel**, **execution pane**, **verification stream** |

## Mermaid source ownership

- **Owner:** `docs/front-door/` transition package; edits go through normal PR review.  
- **Render:** Any Markdown consumer may embed these with Mermaid; diagrams are **sources of truth** for visual consistency.  
- **Drift:** If UI or architecture changes, update both this catalog and the `.mmd` files in the same change when possible.

## Verification hook

- Five files exist under `docs/front-door/diagram-sources/` with `.mmd` extension.  
- Vocabulary matches INVARIANT_05 across docs and diagrams.
