# Front-door strategy: TLC as governance control plane

## Scope and artifact owner

**Scope:** Identity and positioning of TLC for internal builders and external reviewers.  
**Artifact path:** `docs/front-door/FRONT_DOOR_STRATEGY.md`  
**Invariant mapping:** INVARIANT_01 (STATUS.json authority), INVARIANT_12 (maintenance-mode legibility).

## Current state versus intended state

| Dimension | Current state (verified) | Intended state (product direction) |
|-----------|---------------------------|--------------------------------------|
| Truth surface | `STATUS.json` is sole authoritative status; `STATUS.md` is deterministic render | Unchanged: control plane reads and reflects truth surface, never replaces it |
| Public narrative | Root `README.md` links to status; concise governance framing | Flagship README aligned to `GOLDEN_README_BLUEPRINT.md` when explicitly executed |
| Interactive UI | Optional scaffold under `apps/tlc-control-plane/` (static mock data, labeled scaffold) | Wired product surfaces that consume verified artifacts and respect governance hooks |

## Definition: governance control plane

**The Living Constitution** repository operates as a **governance control plane**: it holds constitutional law, build contracts, verification evidence, and status synthesis. **Embedded product execution surfaces** (documentation, diagrams, and UI shells) **display** governance state and **prepare** execution; they do **not** rewrite constitutional rules or pass history.

Canonical terms used consistently across this package:

- **Control plane** — the TLC repo’s governance overlay: contracts, verification, status, enforcement scripts.
- **Status/truth panel** — presentation of `STATUS.json` fields and policy pointers.
- **System graph** — relationship view among domains, projects, and evidence paths.
- **Execution pane** — human-facing sequencing of build steps and contract execution (documentation-first today).
- **Verification stream** — narrative and pointers to verification artifacts, CI evidence, and attestations (not a live stream unless wired).

## Front-door responsibilities

1. **Identity:** Make clear that TLC is governance-first, evidence-bound, and Commonwealth-coordinating.  
2. **Control:** Surface where truth lives (`STATUS.json`) and what must not be hand-waved.  
3. **Sequencing:** Route attention to UI-first build order, then teaser video, then deeper product integration (see `SEQUENCING_DECISION.md`).  
4. **No new pass:** Transition work does not authorize a new TLC governance pass.

## Verification hook

- File inspection: this document exists at the path above.  
- Cross-check: `STATUS.json` unchanged by this strategy document; strategy does not claim superseding authority.
