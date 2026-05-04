# TLC Research Workbench — Bounded Self-Improvement Loop

evidence_basis: CONSTRUCTED — derived from TLC-RDI-MVP-001 contract.

## The Constraint

This is a BOUNDED self-improvement loop. The bounds are:

1. Auto-apply ONLY to non-authoritative generated surfaces
2. NEVER auto-apply to constitutional surfaces:
   - THE_LIVING_CONSTITUTION.md
   - MASTER_PROJECT_INVENTORY.json
   - STATUS.json
   - docs/governance/doctrines/*
   - projects/c-rsp/BUILD_CONTRACT.md
3. Every proposal is logged to research/registry/improvement_proposals.json
4. Human MUST approve before execution
5. All rejected proposals are retained in the log (I4 traceability)

## The Loop

```
critic detects violation → proposer creates proposal → logged to registry
         ↓
human reviews proposal in /improvement UI
         ↓
approved → execute + commit + add provenance step
rejected → log rejection reason + close proposal
```

## Why This Matters for Anthropic

This loop demonstrates that TLC can improve its own governance surfaces under
constraint — the same constraint the research argues should govern AI systems.
The loop is not a demo. It is constitutional infrastructure eating its own
food. The BREAK_GLASS case-law artifacts from prior sessions are evidence of
the loop running under real constitutional pressure.

## BREAK_GLASS Protocol

If an improvement triggers two conflicting invariants, do not resolve silently.
File: artifacts/case-law/BREAK_GLASS_[DATE]_[DESCRIPTION].md
These are primary research data.
