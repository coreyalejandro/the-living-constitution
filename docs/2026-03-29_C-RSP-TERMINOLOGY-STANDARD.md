# 2026-03-29 — C-RSP Terminology Standard
## Canonical Naming Convention for TLC Build Methodology

**Version:** C-RSP-TS-v2.0
**Author:** Corey Alejandro, Constitutional Operator
**Scope:** All projects, contracts, and documentation across the Safety Systems Design Commonwealth
**Authority:** THE_LIVING_CONSTITUTION.md — ratified under Article V
**Effective:** Immediately upon ratification (supersedes C-RSP-TS-v1.0 for expansion authority)

---

## 1. Definition (Authoritative)

**C-RSP** = **Constitutionally-Regulated Single Pass** executable prompt.

**INVARIANT_TERM_01 — C-RSP Canonical Expansion Authority:** The term **C-RSP** must only expand to **Constitutionally-Regulated Single Pass** executable prompt. The following expansions are prohibited everywhere as authoritative meaning unless quoted and marked `Deprecated historical terminology — not authoritative`:

* Contractually Constrained
* Contractually Restrained
* Constitutionally Constrained
* Any variant combining those phrases with deterministic / executable / prompt language as canonical meaning

C-RSP is inspired by and gives a structural nod to **CRISP-DM** (Cross-Industry Standard Process for Data Mining), the industry-standard methodology for data science project management. Where CRISP-DM governs the lifecycle of data projects, C-RSP governs the lifecycle of agentic build execution.

---

## 2. Load-Bearing Properties

A C-RSP executable prompt / build contract instance encodes these properties. All must be present for a valid C-RSP-class artifact.

| Property | Definition | Enforcement (examples) |
|----------|-----------|------------------------|
| **Constitutionally-Regulated** | Obligations and boundaries are explicit, verifiable, and aligned with TLC governance — not implied or ad hoc. | BMT-1 (Sequential Completeness), BMT-3 (Decision Elimination), DGR-1 (One Canonical Location) |
| **Single Pass** | Executable in one ordered pass — repeatable (same input → same output), versioned, transmissible without prior context. | BMT-1, BMT-2 (Named Concreteness), BMT-4 (State Explicitness), Doctrine 1 (Idempotency) |
| **Executable prompt** | The artifact is machine-executable instruction form (deterministic builder/agent input), not aspirational prose alone. | Preflight, verification mapping, evidence paths |

---

## 3. Legacy Terminology Mapping

C-RSP replaces the legacy term **"Zero-Shot Build Contract" (ZSB)**. The following mapping applies:

| Legacy Term | C-RSP Equivalent | Notes |
|------------|-------------------|-------|
| Zero-Shot Build Contract | C-RSP Build Contract | Full replacement. "Zero-shot" described only the single-pass property. C-RSP captures governance + single-pass + executable form. |
| ZSB-TLC-v1.0 | C-RSP-TLC-v1.0 | Master contract version identifier. Version number preserved. |
| ZSB-EPG-v1.0 | C-RSP-EPG-v1.0 | EpistemicGuard contract. |
| ZSB-HMG-v1.0 | C-RSP-HMG-v1.0 | HumanGuard contract. |
| ZSB-EMG-v1.0 | C-RSP-EMG-v1.0 | EmpiricalGuard contract. |
| ZSB-BLG-v2.0 | C-RSP-BLG-v2.0 | BuildLattice Guard contract. |
| ZSB-FBE-v1.0 | C-RSP-FBE-v1.0 | Frostbyte ETL contract. |
| ZSB-IIS-v2.0 | C-RSP-IIS-v2.0 | Instructional Integrity Studio contract. |
| ZSB-EO-v1.0 | C-RSP-EO-v1.0 | Evidence Observatory contract. |
| SOP-004: Zero-Shot Build Contract Creation | SOP-004: C-RSP Build Contract Creation | SOP title update. |

---

## 4. Why the Name (C-RSP)

"Zero-Shot Build Contract" described only one property — single-pass execution. C-RSP-TS-v2.0 fixes **expansion authority**: the acronym **C-RSP** expands only to **Constitutionally-Regulated Single Pass** executable prompt, so terminology cannot drift into prohibited paraphrases as canonical meaning.

The CRISP-DM nod remains intentional: governed methodology for agentic builds, not ad hoc execution.

---

## 5. Migration Plan

### Phase 1: Canonical Documents (Immediate)

All new documents authored from 2026-03-29 onward use C-RSP terminology exclusively per this standard.

### Phase 2: Base Camp Legacy Files (Next Sprint)

The TLC base camp repository may still contain ZSB/zero-shot references in older files. These will be migrated in a governed pass per the mapping table in Section 3.

Until Phase 2 is complete, any document containing "ZSB" or "zero-shot build contract" should be read as synonymous with the C-RSP artifact class. The terminology is different; the methodology is aligned.

### Interim Compatibility Rule

**Any document that uses "ZSB" or "Zero-Shot Build Contract" is valid and enforceable until the Phase 2 migration replaces it.** The terminology change does not invalidate existing contracts. It renames them.

---

## 6. Deprecated Historical Terminology — Not Authoritative

The following described **C-RSP-TS-v1.0** expansion and three-word breakdown. It is **not** authoritative for C-RSP acronym expansion under C-RSP-TS-v2.0:

* **C-RSP** ~~stands for **Contractually-Restrained Single-Pass**~~ (superseded; prohibited as canonical expansion).
* The v1.0 rationale bullets **Contractually** / **Restrained** / **Single-Pass** as the spelled meaning of **C-RSP** — **Deprecated historical terminology — not authoritative.**

Historical documents may retain v1.0 wording only when marked explicitly as above.

---

## 7. V&T Statement

**Exists:** C-RSP-TS-v2.0 with authoritative definition (Constitutionally-Regulated Single Pass executable prompt), INVARIANT_TERM_01, load-bearing properties table, legacy ZSB mapping, deprecated v1.0 expansion block, and migration notes.

**Non-existent:** Exhaustive migration of every legacy file in all Commonwealth repos.

**Unverified:** Whether every external Commonwealth document outside this audit scope has been updated.

**Functional status:** C-RSP canonical expansion is **Constitutionally-Regulated Single Pass** executable prompt for all authoritative new and updated documentation.
