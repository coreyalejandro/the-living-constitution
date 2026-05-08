# Validation Plan — H1, H2, H3

**Document type:** Research Validation Plan Scaffold
**System:** The Living Constitution (TLC) / cognitive-governance-lab (CGL)
**Contract:** CRSP-TLC-TWO-PATHS-REFACTOR-001

> This is a scaffold. Fields marked UNRESOLVED REQUIRED INPUT must be completed before any study begins. This document does not constitute pre-registration. No study has been conducted.

---

## Hypotheses

### H1 — Intent Fidelity

**Full statement:** A persistent Contract Window improves intent fidelity in long-context AI interactions compared to sessions without a Contract Window.

**Operationalization:** Intent fidelity is measured by annotator agreement that the final session output matches the user's initial stated intent, scored on a defined rubric.

**Direction of prediction:** Sessions with Contract Window active will show higher annotated intent fidelity scores than matched sessions without Contract Window.

**Falsification condition:** If the difference in annotated intent fidelity scores between conditions is not statistically significant at the pre-specified alpha level, H1 is not supported.

---

### H2 — Bilateral Repair

**Full statement:** Bilateral intelligibility protocols increase the rate of successful user-initiated corrections to model task interpretation.

**Operationalization:** Bilateral repair rate is measured by counting user-initiated correction events per session and scoring whether the model's subsequent output reflected the correction.

**Direction of prediction:** Sessions with bilateral intelligibility features active will show higher bilateral repair rates than matched sessions without those features.

**Falsification condition:** If the repair rate difference is not statistically significant at the pre-specified alpha level, H2 is not supported.

---

### H3 — Accessibility

**Full statement:** Accessibility-grade runtime invariants improve legibility for lay users without degrading legibility for expert users.

**Operationalization:** Legibility is measured by reading comprehension instrument and subjective clarity ratings in a lay comprehension study.

**Direction of prediction:** Lay users will show higher comprehension scores in sessions with accessibility-grade invariants active. Expert users will not show significantly lower satisfaction scores.

**Falsification condition:** If lay comprehension scores do not differ significantly, or if expert satisfaction scores are significantly lower, H3 is not supported.

---

## Structural vs. attentional confound

This is the primary unresolved confound for H1.

**The confound:** If the Contract Window improves intent fidelity, two mechanisms are possible:
1. **Structural mechanism:** The Contract Window governance structure enforces constraints on the model's behavior, producing better outputs regardless of whether the user reads it.
2. **Attentional mechanism:** The Contract Window display prompts users to re-read and re-anchor their intent at each interaction, producing better behavior because of the user's changed attention, not the model's constrained behavior.

**Why this matters:** A structural effect is evidence for the governance-as-code approach. An attentional effect is evidence for display design, not governance. They may co-occur.

**Proposed confound-handling design:** UNRESOLVED REQUIRED INPUT. One candidate design: a three-arm study with (a) Contract Window active and visible, (b) Contract Window active but hidden from user, (c) no Contract Window. Comparing arms (a) and (b) isolates attentional from structural effects. Comparing arms (b) and (c) isolates structural effects.

**Status:** No study design finalized. Confound is documented but not controlled for.

---

## Annotation protocol

**BicameralReview engine:** The annotation engine exists in cognitive-governance-lab. Synthetic pilot completed with kappa 0.762.

**Real-data protocol:** UNRESOLVED REQUIRED INPUT. Required elements:
- Annotator qualification criteria
- Training procedure
- Annotation rubric (intent fidelity scoring)
- Adjudication procedure for disagreements
- Ground truth definition

**Adjudication:** UNRESOLVED REQUIRED INPUT. Candidates: majority vote, expert adjudication panel, evidence-based tie-breaking.

---

## Sample size

**Required sample:** UNRESOLVED REQUIRED INPUT. Factors:
- Effect size estimate (none available — no baseline)
- Alpha level (UNRESOLVED REQUIRED INPUT)
- Power target (UNRESOLVED REQUIRED INPUT)
- Number of annotators per item

**Pilot study:** Not completed on real data. Synthetic pilot only.

---

## Baseline measurement

**Current baseline:** Not measured. No pre-intervention intent fidelity scores exist for a comparison population.

**Required baseline protocol:** UNRESOLVED REQUIRED INPUT. Must include session sampling criteria, user population definition, and annotator protocol before Contract Window is applied.

---

## Metrics

| Hypothesis | Primary metric | Secondary metrics |
|------------|---------------|-----------------|
| H1 | Annotated intent fidelity score (rubric TBD) | Session drift index, user-reported satisfaction |
| H2 | Bilateral repair rate | Correction accuracy, correction latency |
| H3 | Lay comprehension score | Expert satisfaction, reading ease measure |

**Rubric definitions:** UNRESOLVED REQUIRED INPUT.

---

## Lay comprehension instrument

**Status:** Not built. Required for H3.

**Required components:**
- Reading passage drawn from Contract Window outputs
- Comprehension questions (multiple-choice or short answer)
- Scoring rubric
- Pilot test population definition
- Passing threshold definition

---

## Inter-rater reliability standard

**Target kappa:** UNRESOLVED REQUIRED INPUT. Minimum acceptable kappa before study launch.

**Current synthetic pilot result:** kappa 0.762 on BicameralReview synthetic data.

**Real-data reliability study:** Not completed.

---

## Pre-registration

**Status:** Not pre-registered. No IRB or equivalent ethics review submitted.

**Required before powered study:** UNRESOLVED REQUIRED INPUT.

---

## What this plan does not claim

- Any study has been conducted
- H1-H3 have been validated
- Sample size is sufficient for the planned analysis
- The annotation protocol produces reliable results on real data
- IRB approval has been obtained

---

> Contract: CRSP-TLC-TWO-PATHS-REFACTOR-001
> Status: Scaffold — not an executed research protocol
