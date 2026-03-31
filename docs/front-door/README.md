# TLC front-door transition package

This directory is the **index** for the governance-faithful transition package that defines TLC as a **governance control plane** with embedded product execution surfaces, without authorizing any new constitutional pass.

## Artifact owner

**Scope:** Epistemic domain documentation and UI specification for the repository front door.  
**Owner:** TLC base-camp governance overlay (`coreyalejandro/the-living-constitution`).

## Truth surface

Authoritative operational status remains **`STATUS.json`** (rendered mirror: `STATUS.md`). No document in this folder supersedes that truth surface.

## Index of generated artifacts

| Artifact | Purpose |
| --- | --- |
| [FRONT_DOOR_STRATEGY.md](./FRONT_DOOR_STRATEGY.md) | TLC as governance control plane; embedded execution surfaces |
| [UI_STRATEGY.md](./UI_STRATEGY.md) | Dense multi-panel control-plane UX (AI-studio style) |
| [INFORMATION_ARCHITECTURE.md](./INFORMATION_ARCHITECTURE.md) | Routes, panels, product access model, truth authority |
| [SEQUENCING_DECISION.md](./SEQUENCING_DECISION.md) | Build order: UI first, teaser video second, integration third |
| [GOLDEN_README_BLUEPRINT.md](./GOLDEN_README_BLUEPRINT.md) | Authoritative structure for a future flagship root README |
| [GOLDEN_DIAGRAM_SET.md](./GOLDEN_DIAGRAM_SET.md) | Five diagrams: purpose, labels, Mermaid ownership |
| [PUBLIC_POSITIONING.md](./PUBLIC_POSITIONING.md) | Portfolio, GitHub, LinkedIn language and prerequisites |
| [EXECUTION_ROADMAP.md](./EXECUTION_ROADMAP.md) | Phases, deliverables, dependencies, stop conditions, completion record |
| [diagram-sources/system-context.mmd](./diagram-sources/system-context.mmd) | Mermaid: system context |
| [diagram-sources/control-plane-architecture.mmd](./diagram-sources/control-plane-architecture.mmd) | Mermaid: control-plane architecture |
| [diagram-sources/execution-loop.mmd](./diagram-sources/execution-loop.mmd) | Mermaid: execution loop |
| [diagram-sources/system-graph.mmd](./diagram-sources/system-graph.mmd) | Mermaid: system graph |
| [diagram-sources/ui-layout.mmd](./diagram-sources/ui-layout.mmd) | Mermaid: UI layout |

## Related implementation (scaffold)

Minimal Next.js App Router shell (static mock data only; non-wired regions labeled):

- `apps/tlc-control-plane/` — see `apps/tlc-control-plane/README.md`

## Maintenance-mode note

Product and documentation work proceed under **maintenance-mode governance**. This package does not constitute a new TLC governance pass.
