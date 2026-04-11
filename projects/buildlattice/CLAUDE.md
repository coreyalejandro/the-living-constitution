# CLAUDE.md — BuildLattice Project Governance Overlay

## Identity

| Field | Value |
|-------|-------|
| **Name** | BuildLattice |
| **Type** | Execution Governance Engine |
| **Safety Domain** | Empirical Safety |
| **Status** | `prototype` |
| **Repo Path** | `../buildlattice` (sibling of this repository root) |

## Purpose

BuildLattice is the execution governance layer within The Living Constitution ecosystem. It converts constitutional principles and evidence-derived safeguards into machine-checkable software delivery contracts, policy decisions, and merge-boundary enforcement.

**One-sentence placement:** BuildLattice sits between constitutional interpretation (PROACTIVE) and runtime enforcement, ensuring that every software-changing action is admissible, constrained, approved, and traceable before it proceeds.

## TLC Ecosystem Placement

```
┌─────────────────────────────────────────────────────────────────┐
│                  THE LIVING CONSTITUTION                         │
│                                                                  │
│  Layer 1: EVIDENCE COLLECTION                                   │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │ Evidence Pipeline / Case Files                              │ │
│  │ Failure collection, verification, pattern extraction        │ │
│  └──────────────────────────┬─────────────────────────────────┘ │
│                              │ feeds                             │
│                              ▼                                   │
│  Layer 2: CONSTITUTIONAL ANALYSIS                               │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │ PROACTIVE                                                   │ │
│  │ Epistemic review, constitutional analysis, admissibility    │ │
│  └──────────────────────────┬─────────────────────────────────┘ │
│                              │ informs                           │
│                              ▼                                   │
│  Layer 3: INTERPRETATION / ADJUDICATION                         │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │ ★ BuildLattice (Contract Schema + Policy Engine)           │ │
│  │ Evidence → enforceable contracts, constitutional constraints │ │
│  └──────────────────────────┬─────────────────────────────────┘ │
│                              │ enforces                          │
│                              ▼                                   │
│  Layer 4: EXECUTION GOVERNANCE                                  │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │ ★ BuildLattice (Admissibility Gate + Enforcement Hooks)    │ │
│  │ PR gates, CI checks, merge-boundary enforcement             │ │
│  └──────────────────────────┬─────────────────────────────────┘ │
│                              │ produces                          │
│                              ▼                                   │
│  Layer 5: EVALUATION / PREVENTION                               │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │ Eval / Prevention Layer                                     │ │
│  │ Feedback loop from enforcement outcomes to new safeguards   │ │
│  └────────────────────────────────────────────────────────────┘ │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

## Relationship to Other Projects

| Project | Relationship to BuildLattice |
|---------|------------------------------|
| **PROACTIVE** | Determines whether something is constitutionally/epistemically sound. BuildLattice determines whether it is ALLOWED TO PROCEED as a software-changing action. |
| **Evidence Pipeline** | Feeds BuildLattice via policy generation (failures become new rules) and contract hardening (patterns become stronger constraints). |
| **SentinelOS** | Provides the constitutional invariants and safety domain definitions that BuildLattice encodes into machine-checkable contracts. |
| **Eval/Prevention Layer** | Consumes BuildLattice enforcement outcomes to close the feedback loop — blocked actions, escalations, and approvals feed future safeguards. |

## Constitutional Constraints

1. **Article I (Bill of Rights)** applies to every policy decision. No policy may violate the Right to Safety, Truth, Clarity, Dignity, or Accessibility.
2. **Article II (Execution Law)** governs all BuildLattice code: immutability, truth-status discipline, simplicity, minimal impact.
3. **Article III (Purpose Law)** requires every contract and policy to trace to a theory of change node. No enforcement without purpose.
4. **Article IV (Separation of Powers)** defines which agents can create, modify, and evaluate contracts. No agent may approve its own work.
5. **Article V (Amendment Process)** governs how policies evolve. Evidence of false positives/negatives triggers policy amendment through a structured process.

## First Scope

Govern software-changing actions at the **request, PR, CI, merge, and deployment boundary**:

1. **Build Contracts** — JSON Schema-validated contracts that declare what a software action requires, constrains, and produces
2. **PR Gates** — Policy-driven checks that evaluate PRs against constitutional constraints before merge
3. **Constitutional Check** — Admissibility evaluation that maps every proposed change to its applicable constitutional articles and evidence requirements

## Key Questions BuildLattice Answers

- Is this requested software action admissible?
- What constitutional constraints apply to it?
- What evidence must be present before it proceeds?
- What approval structure is required?
- What repo, path, branch, or deployment boundaries are allowed?
- What should be blocked, warned, escalated, or permitted?

## Rules (Inherited + Project-Specific)

1. All Living Constitution rules apply (Articles I-V, SOPs, Doctrines)
2. Every contract schema change requires a V&T Statement with before/after comparison
3. Every policy change requires evidence justification (which failure or pattern motivated it)
4. No policy may auto-approve — all approvals require at least one human confirmation
5. Enforcement hooks must be idempotent: running the same check twice produces the same decision
