# Runtime Invariants Index — Scaffold

**Document type:** Reviewer-Facing Invariant Index Scaffold
**System:** The Living Constitution (TLC)
**Contract:** CRSP-TLC-TWO-PATHS-REFACTOR-001

> This is a scaffold. Only invariant details that are present in the repository are documented here. Fields marked UNRESOLVED REQUIRED INPUT indicate details not found in the repository at time of contract execution. No invariant details have been invented.

---

## About this index

The Living Constitution claims 59 runtime invariants across the constitutional layer. This index provides a reviewer-facing entry point. It documents the six SentinelOS invariants (I1-I6) that are explicitly defined in the repository. The remaining invariants are referenced in plans/master-plan.md and governance/constitution/core/invariant-registry.json but their full specifications require source inspection beyond what this scaffold can confirm.

---

## SentinelOS Invariants — I1 through I6

These six invariants are explicitly defined in research-alignment.md and the build contracts.

---

### I1 — Epistemic Qualification

| Field | Value |
|-------|-------|
| Invariant ID | I1 |
| Name | Epistemic Qualification |
| Purpose | Ensure claims are qualified by confidence tier before being surfaced to users |
| Failure mode addressed | Unqualified assertions that users may act on as if they were verified facts |
| Machine-readable location | projects/sentinelos/ (implementation status: partially verified) |
| Human-readable explanation | Every claim the system makes must declare its confidence level using the Calibrated Truth Doctrine tiers. A claim cannot be presented as certain if the evidence does not support certainty. |
| Verifier status | Defined. Enforcement code status: Partial (see evidence-ledger.md entry S2) |

---

### I2 — Artifact Verification

| Field | Value |
|-------|-------|
| Invariant ID | I2 |
| Name | Artifact Verification |
| Purpose | Artifacts must be verified before citation |
| Failure mode addressed | Citing artifacts that do not exist, have been modified, or were not produced by the claimed process |
| Machine-readable location | projects/sentinelos/ (implementation status: partially verified) |
| Human-readable explanation | Before citing a file, test result, or output artifact, the system must confirm it exists and matches the expected state. Citing a non-existent artifact is an epistemic safety violation. |
| Verifier status | Defined. Enforcement code status: Partial |

---

### I3 — Confidence Grounding

| Field | Value |
|-------|-------|
| Invariant ID | I3 |
| Name | Confidence Grounding |
| Purpose | Confidence scores must map to evidence, not to linguistic convention |
| Failure mode addressed | Stating high confidence because the phrasing is confident, not because evidence supports it |
| Machine-readable location | projects/sentinelos/ (implementation status: partially verified) |
| Human-readable explanation | Saying something confidently and having evidence for it are not the same thing. Confidence scores must trace to specific evidence, not to how the system is phrasing a claim. |
| Verifier status | Defined. Enforcement code status: Partial |

---

### I4 — Traceability

| Field | Value |
|-------|-------|
| Invariant ID | I4 |
| Name | Traceability |
| Purpose | Every claim must trace to a source |
| Failure mode addressed | Claims with no traceable origin that accumulate across a session as if they were established facts |
| Machine-readable location | projects/sentinelos/ (implementation status: partially verified) |
| Human-readable explanation | Every claim the system makes must have a traceable source. If the source cannot be cited, the claim must be marked as inference or hypothesis. |
| Verifier status | Defined. Enforcement code status: Partial |

---

### I5 — Fluency Conflict Detection

| Field | Value |
|-------|-------|
| Invariant ID | I5 |
| Name | Fluency Conflict Detection |
| Purpose | Fluent language that masks uncertainty must be flagged |
| Failure mode addressed | F3 — Cognitive safety failure: a learning environment produces false understanding because fluent output implies certainty |
| Machine-readable location | projects/sentinelos/ (implementation status: partially verified) |
| Human-readable explanation | A system can produce grammatically fluent, confident-sounding text about something it does not actually know. I5 flags cases where the system's output reads as certain but the underlying state is uncertain. |
| Verifier status | Defined. Enforcement code status: Partial |

---

### I6 — Fail-Closed Behavior

| Field | Value |
|-------|-------|
| Invariant ID | I6 |
| Name | Fail-Closed Behavior |
| Purpose | Ambiguous cases must fail closed — block, not pass |
| Failure mode addressed | Alignment faking surface: a system uncertain about rule application defaults to a self-serving interpretation and proceeds |
| Machine-readable location | projects/sentinelos/ (implementation status: partially verified) |
| Human-readable explanation | When the system cannot determine whether an action complies with a rule, it stops. It does not proceed with a guess. This directly addresses the alignment faking problem: uncertainty defaults to halt, not to optimistic continuation. |
| Verifier status | Defined. Enforcement code status: Partial |

---

## Remaining 53 invariants

**Count claimed:** 59 total (per plans/master-plan.md)
**Count documented here:** 6 (I1-I6, SentinelOS)
**Count remaining:** 53

**Location of full registry:** governance/constitution/core/invariant-registry.json

**Status of full registry:** UNRESOLVED REQUIRED INPUT. The file path is referenced in plans/master-plan.md but full content inspection is required to confirm each invariant's specification, machine-readable location, and verifier status.

**Reviewer note:** Do not treat the 53 remaining invariants as fully documented. They are claimed in the master plan but this index cannot confirm their full specification without reading invariant-registry.json directly. Read the source file before citing these invariants in an evaluation.

---

## How to use this index

1. Start with I1-I6 above — these are the most verified invariants.
2. For the remaining 53, read governance/constitution/core/invariant-registry.json directly.
3. For each invariant you want to verify: find the machine-readable location, read the source code, and confirm the enforcement is present.
4. Do not assume enforcement exists because a definition exists. Definition and enforcement are different things.

---

> Contract: CRSP-TLC-TWO-PATHS-REFACTOR-001
> Status: Scaffold — source inspection required for full coverage
