# Execution roadmap: phases, deliverables, dependencies, stop conditions

## Scope and artifact owner

**Scope:** Phased execution for the front-door transition package and downstream product work.  
**Artifact path:** `docs/front-door/EXECUTION_ROADMAP.md`  
**Invariant mapping:** INVARIANT_03 (current vs intended), INVARIANT_12.

## Phase overview

| Phase | Name | Deliverables | Dependencies | Stop conditions |
|-------|------|--------------|--------------|-----------------|
| P0 | Documentation package | All `docs/front-door/*.md`, diagram sources | Baseline files readable; no constitutional edits | Missing required file paths |
| P1 | Control-plane scaffold | `apps/tlc-control-plane/` minimal App Router UI | Node and pnpm available; no repo-wide dependency conflict | Unresolvable scaffold deps: docs-only completion |
| P2 | Teaser video | `projects/teaser-video/` per contract | P0 narrative stable | Contract blockers in teaser project |
| P3 | Integration | Live verification and graph bindings | P1 UI patterns, CI agreements | Secrets or policy gaps: halt until resolved |

## Dependencies

- **Governance:** Maintenance-mode; no new TLC pass.  
- **Truth:** `STATUS.json` generation via `scripts/render_status_surface.py` when inventory or policy changes.  
- **Bootstrap:** `./scripts/bootstrap_repo.sh` before local verification.

## Governance mapping note

If `.c-rsp/governance-map.json` is extended, entries should reference **constitutional reference:** maintenance-mode and single truth surface; **invariant mapping:** INVARIANT_01–12 from the front-door contract; **verification hook:** file existence and local `pnpm build` for the app when scaffold exists.

## Intended versus current (honest)

| Item | Current | Intended |
|------|---------|----------|
| Front-door docs | Delivered when this folder is complete | Kept in sync with inventory and STATUS semantics |
| Control-plane UI | Shell with static snapshot | Wired reads from approved artifacts only |
| Teaser video | Project exists | Published asset per teaser contract |

---

## Appendix: contract completion record

**Contract:** TLC front-door transition package (C-RSP instance).  
**Contract version:** v1.0.0  
**Execution date:** 2026-03-30  
**Completion summary:**

- Created `docs/front-door/` index and eight strategy documents plus five Mermaid diagram sources under `docs/front-door/diagram-sources/`.  
- Scaffolded `apps/tlc-control-plane/` as a minimal Next.js App Router application with four panels: **system graph**, **status/truth panel**, **execution pane**, **verification stream**; non-wired UI labeled **Static shell scaffold — not yet wired**.  
- Did not modify `STATUS.json`, `THE_LIVING_CONSTITUTION.md`, or root `README.md`.  
- Extended `.c-rsp/governance-map.json` with front-door module entries; appended `.c-rsp/CONFLICT_LOG.md` with execution row.  
- Updated `openmemory.md` with front-door and control-plane scaffold entries.

**Environment note:** Pin versions in `apps/tlc-control-plane/package.json` at scaffold write time. Install inside `apps/tlc-control-plane` with `npm install` or `pnpm install`. Production build verified: `npm run build` completed successfully with Next.js **15.2.9**.

**Functional status:** Documentation package is specification-complete. UI shell is scaffold-only with static snapshot data derived from repository state at execution time.
