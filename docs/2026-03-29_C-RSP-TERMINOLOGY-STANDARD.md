# 2026-03-29 — C-RSP Terminology Standard
## Canonical Naming Convention for TLC Build Methodology

**Version:** C-RSP-TS-v1.0
**Author:** Corey Alejandro, Constitutional Operator
**Scope:** All projects, contracts, and documentation across the Safety Systems Design Commonwealth
**Authority:** THE_LIVING_CONSTITUTION.md — ratified under Article V
**Effective:** Immediately upon ratification

---

## 1. Definition

**C-RSP** stands for **Contractually-Restrained Single-Pass**. It is the name of the deterministic prompt engineering methodology used across the Safety Systems Design Commonwealth to transform natural language instructions into machine-executable build contracts.

C-RSP is inspired by and gives a structural nod to **CRISP-DM** (Cross-Industry Standard Process for Data Mining), the industry-standard methodology for data science project management. Where CRISP-DM governs the lifecycle of data projects, C-RSP governs the lifecycle of agentic build execution.

---

## 2. The Three Properties

A C-RSP build contract has exactly three properties. All three must be present. A contract missing any one property is not a C-RSP contract.

| Property | Definition | Enforcement |
|----------|-----------|-------------|
| **Contractual** | Every output obligation is explicitly stated, verifiable, and enforceable. There are no implied deliverables. What the contract says is what gets built — nothing more, nothing less. | BMT-1 (Sequential Completeness), BMT-3 (Decision Elimination), DGR-1 (One Canonical Location) |
| **Restrained** | Hard-coded constraints and behavioral boundaries with defined and detectable violations. The contract tells the builder what they cannot do, not just what they must do. Violation patterns are enumerated. | BMT-5 (Failure Path Coverage), I1 (Evidence-First), I5 (Safety Over Fluency) |
| **Single-Pass** | The contract is executable in one pass — top to bottom, no iteration required, no clarification needed. It is repeatable (same input → same output), versioned (every change increments the version), and transmissible (any operator or agent can execute it without prior context). | BMT-1 (Sequential Completeness), BMT-2 (Named Concreteness), BMT-4 (State Explicitness), Doctrine 1 (Idempotency) |

---

## 3. Legacy Terminology Mapping

C-RSP replaces the legacy term **"Zero-Shot Build Contract" (ZSB)**. The following mapping applies:

| Legacy Term | C-RSP Equivalent | Notes |
|------------|-------------------|-------|
| Zero-Shot Build Contract | C-RSP Build Contract | Full replacement. "Zero-shot" described only the single-pass property. C-RSP captures all three properties. |
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

## 4. Why the Name Changed

"Zero-Shot Build Contract" described only one of three properties — the single-pass execution model (no iteration, no clarification). It said nothing about the contractual obligations or the behavioral restraints. The name was technically incomplete.

C-RSP encodes all three load-bearing properties in the name itself:

- **Contractually** → obligations are explicit and enforceable (not just "instructions")
- **Restrained** → constraints and violation boundaries are defined (not just "do this")
- **Single-Pass** → one execution, repeatable, versioned, transmissible (the "zero-shot" property, stated precisely)

The CRISP-DM nod is intentional. CRISP-DM established that data projects need a governed methodology, not ad hoc execution. C-RSP establishes the same for agentic builds.

---

## 5. Migration Plan

### Phase 1: Canonical Documents (Immediate)

All new documents authored from 2026-03-29 onward use C-RSP terminology exclusively. The three documents authored in this session have been updated:

- `docs/2026-03-29_BLIND-MANS-TEST.md` — uses C-RSP
- `docs/2026-03-29_DOCUMENTATION-GOVERNANCE-RULE.md` — uses C-RSP
- `docs/2026-03-29_TLC-PROJECT-REPORT.md` — uses C-RSP

### Phase 2: Base Camp Legacy Files (Next Sprint)

The TLC base camp repository contains 94 occurrences of ZSB/zero-shot terminology across 34 files. These will be migrated in a governed pass:

1. Each file is read, the ZSB references are replaced with C-RSP equivalents per the mapping table in Section 3.
2. Each modified file gets a `Last Verified` date update per DGR-4 (Staleness Detection).
3. The CDR is updated to reflect the current canonical state.
4. A single commit captures the entire migration with the message: `refactor: ZSB → C-RSP terminology migration per C-RSP-TS-v1.0`.

Until Phase 2 is complete, any document containing "ZSB" or "zero-shot build contract" should be read as synonymous with C-RSP. The terminology is different; the methodology is identical.

### Interim Compatibility Rule

**Any document that uses "ZSB" or "Zero-Shot Build Contract" is valid and enforceable until the Phase 2 migration replaces it.** The terminology change does not invalidate existing contracts. It renames them.

---

## 6. V&T Statement

**Exists:** Complete C-RSP Terminology Standard with definition, three properties (Contractual, Restrained, Single-Pass), legacy ZSB → C-RSP mapping table (9 contract identifiers + 1 SOP), rationale for the name change, CRISP-DM lineage, and two-phase migration plan.

**Non-existent:** Phase 2 migration (34 files, 94 occurrences in the base camp repo). Updated SOP-004 title. Formal Article V ratification.

**Unverified:** Whether any Commonwealth documents outside the audited directories contain ZSB references (e.g., project repos at `/Users/coreyalejandro/Projects/*`). Whether the 9-contract mapping table is exhaustive.

**Functional status:** C-RSP is the canonical term effective immediately for all new documents. Legacy ZSB terminology remains valid until Phase 2 migration. No existing contract is invalidated by this change.
