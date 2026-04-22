# 2026-03-29 — Documentation Governance Rule (DGR)
## Doctrine 5 of The Living Constitution
### Single Source of Truth Enforcement

**Version:** DGR-v1.0
**Author:** Corey Alejandro, Constitutional Operator
**Scope:** All projects, sub-projects, and governance artifacts across the Safety Systems Design Commonwealth
**Authority:** THE_LIVING_CONSTITUTION.md — ratified under Article V
**Prerequisite:** Doctrine 4 (Blind Man's Test) — all governed documents must also pass BMT

---

## 1. The Problem

An audit of the `the-living-constitution` base camp repository on 2026-03-29 found **88 markdown files** distributed across 12+ directories. Multiple files described the same concepts with conflicting levels of detail, different terminology, and divergent status claims. Specific findings:

- `THE_LIVING_CONSTITUTION.md` and `governance/constitution/core/constitution.md` both claim to define the constitutional framework — neither references the other as canonical.
- `governance/constitution/core/articles.md` contains Article I-V implementation mapping tables that do not appear in `THE_LIVING_CONSTITUTION.md`.
- Failure taxonomy exists in three locations: `projects/evaluation/failure_taxonomy.md`, `projects/evaluation/datasets/failure_cases.json`, and inline within `THE_LIVING_CONSTITUTION.md` Section 4.
- Invariant definitions exist in both `governance/constitution/core/invariants/*.md` (individual files per invariant) and `THE_LIVING_CONSTITUTION.md` (inline summary).
- Build contracts reference file paths that do not exist in the session-accessible file tree.
- No document declares itself as the canonical source for its subject matter.

This is a Census Doctrine (Doctrine 3) violation: ungoverned documentation is undiscoverable documentation. It is also an Idempotency Doctrine (Doctrine 1) violation: the same query ("What are the TLC invariants?") returns different answers depending on which file the reader finds first.

---

## 2. The Rule

**Every subject in the Commonwealth has exactly one canonical document.** That document is the single source of truth for its subject. All other documents that reference the same subject must either (a) quote from the canonical document with an explicit path citation, or (b) link to it without restating its content.

Restating content from a canonical document in a non-canonical location is a DGR violation. The restatement will inevitably drift from the source, creating two truths. Two truths is zero truths.

---

## 3. Canonical Document Registry

Every project and sub-project maintains a **Canonical Document Registry** (CDR) — a single table that maps every governed subject to exactly one file path. The CDR lives in one location per project:

- **For the TLC base camp:** `the-living-constitution/CANONICAL_REGISTRY.md`
- **For each Commonwealth project:** `<project-root>/CANONICAL_REGISTRY.md`

### CDR Table Format

| Subject | Canonical Path | Owner | Last Verified |
|---------|---------------|-------|---------------|
| Constitutional specification | `THE_LIVING_CONSTITUTION.md` | Constitutional Operator | 2026-03-29 |
| Articles I-V (full text) | `governance/constitution/core/articles.md` | Constitutional Operator | 2026-03-29 |
| Failure taxonomy F1-F5 | `projects/evaluation/failure_taxonomy.md` | Constitutional Operator | 2026-03-29 |
| Invariant definitions I1-I6 | `governance/constitution/core/invariants/` | Constitutional Operator | 2026-03-29 |
| Sprint tracker | `tasks/todo.md` | Constitutional Operator | 2026-03-29 |
| Amendment log | `tasks/lessons.md` | Constitutional Operator | 2026-03-29 |
| Verification matrix | `verification/MATRIX.md` | Constitutional Operator | 2026-03-29 |
| Project registry | `CLAUDE.md` (Project Registry table) | Constitutional Operator | 2026-03-29 |

### CDR Rules

1. **No subject may appear in the CDR more than once.** If a subject maps to two files, one of them is wrong. Resolve it before proceeding.
2. **Every file that contains governed content must appear in the CDR.** Files not in the CDR are either (a) exempt documents (READMEs, amendment proposals, lessons.md entries — see BMT Section 5) or (b) DGR violations waiting to be caught.
3. **The CDR is the Census Doctrine applied to documentation.** You cannot govern what you have not registered.

---

## 4. The Four DGR Constraints

### DGR-1: One Canonical Location Per Subject

Every technical subject (architecture, API spec, schema definition, failure taxonomy, invariant definition, build contract, design system, SOP) has exactly one file that is its canonical source. That file's path is recorded in the project's CDR.

**Passes:** Failure taxonomy F1-F5 is defined in `projects/evaluation/failure_taxonomy.md`. The inline summary in `THE_LIVING_CONSTITUTION.md` Section 4 says: "See `projects/evaluation/failure_taxonomy.md` for the complete failure taxonomy. Summary: F1 (Confident False Claims), F2 (Phantom Completion), F3 (Persistence Under Correction), F4 (Harm-Risk Coupling), F5 (Cross-Episode Recurrence)."

**Fails:** Failure taxonomy F1-F5 is fully defined in both `projects/evaluation/failure_taxonomy.md` and `THE_LIVING_CONSTITUTION.md` Section 4, with different levels of detail and no cross-reference.

### DGR-2: No Content Duplication

Non-canonical documents may reference a canonical document by path and quote short excerpts (one paragraph or less) for context. They may not restate, paraphrase, or redefine the canonical content. If a reader needs the full content, they go to the canonical source.

**Passes:** A build contract says: "This project implements Invariant I2 (No Phantom Work), defined at `governance/constitution/core/invariants/I2.md`: 'No component, feature, or capability may be reported as complete unless it has been executed and its output independently verified.' The build contract's acceptance criteria operationalize I2 as follows: [project-specific criteria]."

**Fails:** A build contract says: "Invariant I2 means that nothing can be called done unless it's actually done and verified." (This is a paraphrase that will drift from the canonical definition over time.)

### DGR-3: Cross-Reference by Path, Not by Memory

Every reference to another document uses the exact relative file path from the project root. No "as discussed," no "see the constitution," no "per the standard." The path is the reference.

**Passes:** "The adjudication rubric (defined in `docs/research-methodology.md`, Section 4: Adjudication Rubric) maps each event type to one or more TLC Articles."

**Fails:** "The adjudication rubric (as described in the methodology doc) maps events to articles."

### DGR-4: Staleness Detection

Every canonical document includes a `Last Verified` date in its header or in the CDR. If the `Last Verified` date is more than 30 days old, the document is flagged as potentially stale. Stale documents must be re-verified before being used as build inputs.

**Passes:** Document header includes `Last Verified: 2026-03-29` and the CDR entry matches.

**Fails:** Document has no verification date. The CDR entry says "2025-12-01" and no one has checked it since.

---

## 5. DGR Violation Detection

The following patterns in any Commonwealth document are automatic DGR violations:

| Pattern | Violates | Example |
|---------|----------|---------|
| Same subject defined in two files with different content | DGR-1 | Invariant I3 defined differently in `invariants/I3.md` and `THE_LIVING_CONSTITUTION.md` |
| Full-paragraph restatement of canonical content | DGR-2 | Build contract restates the entire Census Doctrine instead of citing `governance/constitution/core/constitution.md` |
| Reference without file path | DGR-3 | "See the failure taxonomy" without specifying `projects/evaluation/failure_taxonomy.md` |
| "As discussed" / "as mentioned" / "per our earlier work" | DGR-3 | "As discussed, the pipeline has 5 layers" |
| Document with no `Last Verified` date and no CDR entry | DGR-4 | Any markdown file created more than 7 days ago with no verification trail |
| File not registered in the project CDR | DGR-1 | A new `ARCHITECTURE.md` created in a project root without a CDR entry |

---

## 6. Document Lifecycle

### 6.1 Creation

When a new document is created:

1. **Check the CDR.** Does a canonical document for this subject already exist? If yes, do not create a new file — update the existing canonical document instead.
2. **If no canonical document exists,** create the file in the correct directory (see Section 7: Directory Taxonomy).
3. **Add a CDR entry** with the subject, canonical path, owner, and today's date as `Last Verified`.
4. **The document must pass BMT** (Doctrine 4) if it is an execution spec (build contract, SOP, CLAUDE.md, API spec, research methodology). See BMT Section 5 for the exemption list.

### 6.2 Modification

When modifying a canonical document:

1. **Update the document content.**
2. **Update the `Last Verified` date** in both the document header and the CDR.
3. **Search for non-canonical references** to the modified content. If any exist, verify they still align with the updated canonical source. Update cross-references if the canonical document's path or section structure changed.

### 6.3 Deprecation

When a document is no longer needed:

1. **Do not delete it.** Move it to a `deprecated/` directory within the same project.
2. **Update the CDR** to mark it as deprecated with the deprecation date.
3. **Add a deprecation notice** at the top of the file: `⚠️ DEPRECATED as of [date]. Superseded by [canonical path]. Do not use this document as a build input.`

---

## 7. Directory Taxonomy

Every TLC project organizes documents into these standard directories. This is not a suggestion — it is a constraint.

| Directory | Contains | Examples |
|-----------|----------|----------|
| `/` (root) | Project identity files only | `CLAUDE.md`, `CANONICAL_REGISTRY.md`, `README.md`, `package.json` |
| `docs/` | All authored documents — reports, research, governance rules, dated deliverables | `2026-03-29_BLIND-MANS-TEST.md`, `research-methodology.md` |
| `docs/contracts/` | All C-RSP build contracts (**Constitutionally-Regulated Single Pass** executable prompt class; see `docs/2026-03-29_C-RSP-TERMINOLOGY-STANDARD.md`) | `C-RSP-TLC-v1.0.md`, `C-RSP-EO-v1.0.md` |
| `docs/sops/` | Standard operating procedures | `SOP-001.md` through `SOP-015.md` |
| `docs/deprecated/` | Superseded documents with deprecation notices | Any document moved out of active use |
| `schemas/` | JSON schemas and machine-readable governance registries | `ingestion_index.schema.json`, `tlc_principles.json` |
| `scripts/` | Executable pipeline and utility scripts | `layer0_ingest.py`, `run_pipeline.py` |
| `tests/` | Test files | `test_layer0.py`, `conftest.py` |
| `config/` | Configuration files (TypeScript, JSON, YAML) | `projects.ts`, `domains.ts` |
| `verification/` | Evidence and verification artifacts | `MATRIX.md`, per-project V&T statements |
| `analysis/` | Data analysis outputs and seed datasets | `tlc_failure_cases_seed.json` |

**Rule:** A file that does not fit into any of these directories must be discussed with the Constitutional Operator before creation. Ad hoc directories are DGR violations.

---

## 8. Relationship to Existing Doctrines

| Doctrine | How DGR enforces it |
|----------|-------------------|
| Idempotency (Doctrine 1) | One canonical source per subject means the same query always returns the same answer, regardless of which file the reader encounters first. |
| Calibrated Truth (Doctrine 2) | DGR-4 (Staleness Detection) prevents outdated documents from being treated as current truth. The `Last Verified` date is a calibration marker. |
| Census (Doctrine 3) | The CDR is the Census Doctrine applied to documentation. Every governed document is registered, counted, and tracked. Unregistered documents are ungoverned. |
| BMT (Doctrine 4) | DGR-3 (Cross-Reference by Path) enforces BMT-2 (Named Concreteness) at the document level. DGR-2 (No Content Duplication) prevents the ambiguity that BMT-3 (Decision Elimination) prohibits. |

DGR is proposed as **Doctrine 5 — Single Source of Truth.** It joins the four existing doctrines as the governance layer for documentation itself.

---

## 9. Constitutional Integration

### Amendment Proposal (Article V)

**Action:** ADD Doctrine 5 (Single Source of Truth / Documentation Governance Rule) to THE_LIVING_CONSTITUTION.md

**Because:** An 88-file audit of the TLC base camp repo found multiple conflicting sources for the same subjects (failure taxonomy, invariants, articles, project registry). This has caused agent confusion, status inflation, and instruction drift. DGR eliminates the root cause: unregistered, duplicated, and unreferenced documentation.

**Evidence:** The 88-file audit of 2026-03-29. Specific conflicts: `THE_LIVING_CONSTITUTION.md` vs `governance/constitution/core/constitution.md` (overlapping constitutional definitions), `projects/evaluation/failure_taxonomy.md` vs inline definitions in the main spec (divergent failure descriptions), `governance/constitution/core/invariants/*.md` vs inline invariant summaries (different levels of detail with no cross-reference).

**Preventing:** F1 (Confident False Claims from reading an outdated non-canonical source), F2 (Phantom Completion from referencing a document that describes planned rather than actual state), F3 (Instruction Drift from agents reading different files for the same subject).

### New Principle

**P12 — Single Source of Truth (Documentation Governance Rule)**

Every subject in the Commonwealth has exactly one canonical document registered in the project's Canonical Document Registry (CDR). Non-canonical documents may reference canonical documents by exact file path but may not restate their content. Four constraints (DGR-1 through DGR-4) govern creation, reference, and maintenance of all documentation.

**Violation:** Any document that defines a subject already canonically defined elsewhere, any reference that omits the canonical file path, any canonical document with a `Last Verified` date older than 30 days, any file not registered in the CDR.

**Evidence requirement:** Tier 1 (convention) — human review against DGR constraints and CDR completeness. Tier 2 (target) — automated CDR validation script that checks for duplicate subjects, missing paths, stale dates, and unregistered files.

### New Invariant

**I8 — Documentation Singularity**

No build session, agent session, or specification review may proceed using a document that is not registered in the project's CDR as the canonical source for its subject.

**Check:** Every document referenced in a build contract, CLAUDE.md, or agent prompt includes its CDR-registered canonical path. If a referenced document is not in the CDR, the session halts until the CDR is updated.

---

## 10. V&T Statement

**Exists:** Complete Documentation Governance Rule with problem statement (88-file audit findings), the core rule (one canonical document per subject), Canonical Document Registry (CDR) format and rules, 4 DGR constraints (DGR-1 through DGR-4) with pass/fail examples, violation detection patterns (6 patterns), document lifecycle (creation, modification, deprecation), directory taxonomy (10 standard directories), constitutional integration proposal (P12, I8), and relationship mapping to Doctrines 1-4.

**Non-existent:** Automated CDR validation script (Tier 2). Actual CANONICAL_REGISTRY.md files for the TLC base camp or any Commonwealth project. Migration plan for the 88 existing files into the DGR-compliant structure. Formal Article V ratification by Constitutional Operator.

**Unverified:** Whether the 10-directory taxonomy covers all file types across all 13 Commonwealth projects. Whether the 30-day staleness threshold is appropriate for all document types. Whether the 6 violation patterns are exhaustive.

**Functional status:** DGR is fully specified and ready for ratification. It has not yet been applied to any existing project. First application should be the TLC base camp repo — creating `CANONICAL_REGISTRY.md` and resolving the identified conflicts between `THE_LIVING_CONSTITUTION.md`, `governance/constitution/core/constitution.md`, and `governance/constitution/core/articles.md`.
