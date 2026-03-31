# Information architecture: routes, panels, access model

## Scope and artifact owner

**Scope:** Route map, panel responsibilities, product access model, and truth-surface authority.  
**Artifact path:** `docs/front-door/INFORMATION_ARCHITECTURE.md`  
**Invariant mapping:** INVARIANT_01, INVARIANT_05 (canonical terms), INVARIANT_08 (claims map to paths).

## Truth-surface authority

| Layer | Authority | Notes |
| --- | --- | --- |
| Operational status | `STATUS.json` | Single authoritative current-status artifact (PASS 10A). |
| Human mirror | `STATUS.md` | Generated only via `scripts/render_status_surface.py`. |
| Constitutional law | `THE_LIVING_CONSTITUTION.md`, `00-constitution/` | Not altered by front-door work. |
| This IA document | Descriptive | Describes intended UX and routes; does not override JSON. |

## Route map (control-plane app)

For `apps/tlc-control-plane/` (App Router):

- **Route:** `/` — **Responsibility:** single-page control plane with **system graph**, **status/truth panel**, **execution pane**, and **verification stream**.

Future expansion (not implemented in this contract): nested routes such as `/projects/[slug]` linking to build contracts remain documentation-first until wired.

## Panel responsibilities

| Panel | Primary content | Data source (intended) |
| --- | --- | --- |
| System graph | Topology of domains and project overlays | Static scaffold or graph derived from checked-in inventory; live graph is future |
| Status/truth panel | `tip_state_truth`, anchor, escalation, workflow identity | Snapshot aligned to `STATUS.json` in scaffold; live read is future |
| Execution pane | Phases, C-RSP contracts, sequencing | `docs/front-door/EXECUTION_ROADMAP.md` and `projects/*/BUILD_CONTRACT.md` pointers |
| Verification stream | Run IDs, attestation pointers, matrix | `verification/` paths; not simulated live events |

## Product access model

- **Internal builders:** Read governance docs, run verifiers locally, use scaffold UI as a visual aid.  
- **External reviewers:** Rely on exported evidence and public positioning language; UI scaffold is optional and non-authoritative.  
- **No elevated claim:** The scaffold does not grant operational control over CI or remote systems.

## Verification hook

- Confirm four panel names appear in `apps/tlc-control-plane/` when scaffold exists.  
- Confirm no panel asserts live backend connectivity without implementation.
