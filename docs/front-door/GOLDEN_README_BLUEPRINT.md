# Golden README blueprint (authoritative structure for a future flagship README)

## Scope and artifact owner

**Scope:** Target outline for replacing the current root `README.md` in a **future, explicit** edit. This contract **does not** overwrite the root README.  
**Artifact path:** `docs/front-door/GOLDEN_README_BLUEPRINT.md`  
**Invariant mapping:** INVARIANT_06 (root governance files not weakened), INVARIANT_09 (no overstated capability).

## Purpose

Provide a **portfolio-grade, governance-faithful** narrative structure that:

- Leads with mission and Commonwealth role.  
- Points to `STATUS.json` / `STATUS.md` as the only operational status entry.  
- Explains verification bootstrap (`./scripts/bootstrap_repo.sh`) and key verifiers.  
- Surfaces `projects/` build contracts and `verification/MATRIX.md` without duplicating implementation code.  
- States maintenance-mode governance honestly.

## Proposed section order

1. **Title and one-line mission** — The Living Constitution as governance overlay for the Safety Systems Design Commonwealth.  
2. **Status callout** — Single block linking `STATUS.md` and `STATUS.json`; instruction to regenerate via `python3 scripts/render_status_surface.py --root .`.  
3. **What this repository is** — Constitution, contracts, verification, sprint coordination (aligned to root `CLAUDE.md`).  
4. **Control plane concept** — Short explanation of governance control plane versus product repos; link to `docs/front-door/FRONT_DOOR_STRATEGY.md`.  
5. **Quick start for contributors** — Bootstrap, then verifier commands (exact commands from `CLAUDE.md` or verification docs).  
6. **Project registry pointer** — `MASTER_PROJECT_INVENTORY.md` or `config/projects.ts` as appropriate.  
7. **Verification and evidence** — `verification/MATRIX.md`, governance chain, closed-epistemics policy pointer.  
8. **Optional UI** — If `apps/tlc-control-plane/` exists, describe it as scaffold or product with accurate capability statement.  
9. **License and contact** — As applicable to the repo.

## Current README versus golden README

| Aspect | Current root README (verified present) | Golden README |
|--------|----------------------------------------|---------------|
| Length | Short, status-first | Expanded narrative while preserving status authority |
| Control plane | Not named explicitly | Names control plane and links front-door docs |

## Verification hook

- Root `README.md` remains unchanged until a maintainer applies this blueprint in a separate commit.  
- No placeholder brackets: this blueprint is complete prose.
