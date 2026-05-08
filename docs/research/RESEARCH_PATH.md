# Research Path — The Living Constitution

**Path type:** Research Reviewer Entry Point
**System:** The Living Constitution (TLC)
**Contract:** CRSP-TLC-TWO-PATHS-REFACTOR-001

---

## Research purpose

TLC is a constitutional governance-as-code research apparatus. Its primary research purpose is to test whether structured runtime interventions — a persistent Contract Window, bilateral intelligibility protocols, and accessibility-grade runtime invariants — improve measurable properties of human-AI interaction.

This is applied AI safety research. It is not a claim that the interventions work. It is a research program equipped to test whether they work.

---

## The three hypotheses

### H1 — Intent Fidelity

**Claim:** A persistent Contract Window improves intent fidelity in long-context AI interactions.

Intent fidelity: the degree to which model outputs over a session remain aligned with the user's original task intent rather than drifting toward model-convenient reframings.

**Status:** Hypothesis. Not empirically validated. No powered study completed.

---

### H2 — Bilateral Repair

**Claim:** Bilateral intelligibility protocols improve contestability. Users who can read and repair the system's current task interpretation will do so more accurately than users who cannot.

Bilateral repair: the capacity for both the user and the model to surface and correct misunderstandings about task scope, assumptions, and current state.

**Status:** Hypothesis. Not empirically validated. Synthetic pilot completed (BicameralReview kappa 0.762 on synthetic data). Powered study not completed.

---

### H3 — Accessibility

**Claim:** Accessibility-grade runtime invariants improve legibility for lay users, including neurodivergent users, without degrading legibility for expert users.

Accessibility-grade: meeting WCAG-adjacent reading-ease and plain-language criteria; designed for users with cognitive load constraints.

**Status:** Hypothesis. Not empirically validated. Lay comprehension study not completed.

---

## Contract Window

The Contract Window is the primary experimental instrument. It is a persistent, user-visible display of the active task agreement: what the system is currently trying to do, what assumptions it is operating under, and what its current truth-status is.

**What is known:**
- Contract Window prototype exists (9/9 tests passing in cognitive-governance-lab as of last check)
- Contract Window reference implementation in apps/contract-window/
- Contract Window is observable: it produces structured state at each interaction

**What is not known:**
- Whether the effect on intent fidelity is structural (caused by the governance constraint) or attentional (caused by the user reading the displayed state and adjusting behavior)
- Whether effect size is large enough to be practically significant
- Whether the effect holds across user populations

**Structural vs. attentional confound:** This is the primary unresolved question for H1. If the Contract Window improves intent fidelity, we cannot yet determine whether the mechanism is the governance structure enforcing constraint or the display prompting users to re-anchor their intent. The validation plan addresses this.

---

## Evidence Observatory

The Evidence Observatory is an 8-layer evidence pipeline that promotes raw AI interactions into governed, auditable transcripts.

**Layers (claimed — implementation status partially verified):**
1. Raw interaction capture
2. Metadata extraction
3. Invariant check log
4. V&T statement extraction
5. Claim classification
6. Evidence tagging
7. Adjudication record
8. Governed transcript output

**Location:** apps/evidence-observatory/

**Status:** Working. Full layer-by-layer evidence audit is UNRESOLVED REQUIRED INPUT.

---

## Validation requirements for H1-H3

See [docs/research/VALIDATION_PLAN.md](VALIDATION_PLAN.md) for the full scaffold.

Summary of what has and has not been done:

| Validation component | Status |
|---------------------|--------|
| Construct definitions operational | Exists (PROPOSAL.md) |
| BicameralReview inter-rater reliability tool | Synthetic pilot complete (kappa 0.762) |
| Powered study sample size | UNRESOLVED REQUIRED INPUT |
| Annotation protocol | Scaffold exists — full protocol UNRESOLVED REQUIRED INPUT |
| Baseline measurement | Not completed |
| Lay comprehension instrument | Not completed |
| Structural vs. attentional confound design | Scaffold in VALIDATION_PLAN.md |
| Pre-registration | Not completed |
| IRB or equivalent review | UNRESOLVED REQUIRED INPUT |

---

## Where the research lives

| Resource | Location | Status |
|----------|---------|--------|
| Full research proposal | PROPOSAL.md | Working |
| Research alignment with Anthropic work | research/research-alignment.md | Exists |
| Fellowship positioning document | research/fellowship-positioning.md | Exists |
| Experiment registry | research/registry/experiments.json | Exists |
| Eval suites registry | research/registry/eval_suites.json | Exists |
| Evidence ledger | research/evidence-ledger.md | Exists |
| TLC-CGL boundary document | research/TLC-CGL-BOUNDARY.md | Exists |
| Contract Window prototype | cognitive-governance-lab (external repo) | Prototype |
| BicameralReview engine | cognitive-governance-lab (external repo) | Synthetic pilot |

---

## What this path does not claim

- H1, H2, or H3 have been validated
- The Contract Window effect is structural rather than attentional
- Inter-rater reliability has been established on real data
- Lay comprehension has been validated
- TLC is suitable as a production safety layer
- The research has been peer reviewed
- The due-diligence report that informed this document was a complete source-code audit

---

> Truth surface: STATUS.md, verification/CRSP-TLC-TWO-PATHS-REFACTOR-001/outcome.md
> Contract: CRSP-TLC-TWO-PATHS-REFACTOR-001
