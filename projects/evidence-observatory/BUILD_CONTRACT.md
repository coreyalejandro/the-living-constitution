# Build Contract: TLC Evidence Observatory

## Research Question

How can heterogeneous real-world AI interaction artifacts be converted into admissible, auditable, and reproducible case files that support measurement of model failures?

## The 10 Pillars

| # | Pillar | Responsibility |
| --- | --- | --- |
| 1 | Forensic Ingest | Accept raw artifacts (screenshots, chat exports, API logs, text) with full provenance metadata |
| 2 | Normalization | Convert heterogeneous inputs into a unified canonical schema without modifying originals |
| 3 | Event Extraction | Identify discrete events (claims, state assertions, contradictions) within normalized artifacts |
| 4 | Admissibility Gate | Apply constitutional admissibility criteria — chain of custody, provenance, completeness |
| 5 | TLC Adjudication | Map events to constitutional violations (Article I-V) and assign severity |
| 6 | Case Files | Package adjudicated events into structured, citable case files |
| 7 | Benchmarks | Generate reproducible evaluation benchmarks from case files |
| 8 | Evals | Run model evaluations against benchmarks; measure failure rates |
| 9 | Prevention | Derive prevention hypotheses and mitigation patterns from eval results |
| 10 | Research Workbench | Next.js UI for browsing evidence, case files, benchmarks, and eval results |

## First Slice Scope

Three failure classes for end-to-end demonstration:

- **unsupported_claim** — Model asserts a fact without evidence or citation
- **fabricated_state** — Model describes a system state that does not match reality
- **contradiction** — Model makes two incompatible claims within the same interaction

## Mandatory Principles

1. **Immutability of raw evidence.** Raw artifacts are stored as-is. Every transformation creates a new artifact with a traceable lineage pointer back to the original. No exceptions.
2. **Full provenance chain.** Every derived artifact (normalized event, case file, benchmark) carries metadata tracing it to exact source spans in the original evidence.
3. **Honest status declarations.** Every pillar declares its truth-status (`implemented`, `partial`, `prototype`, `planned`). No inflation.
4. **Constitutional grounding.** Every adjudication decision references specific Article and Section of The Living Constitution.
5. **Reproducibility.** Given the same raw input and the same pipeline version, the output must be identical. Idempotency doctrine applies end-to-end.

## Deliverable Standard

| Deliverable | Acceptance Criteria |
| --- | --- |
| Python pipeline | Ingest through Prevention pillars functional; accepts at least 3 input formats (screenshot, chat export, text) |
| Case files | Structured JSON case files with provenance metadata, constitutional violation mapping, and severity |
| Benchmarks | At least 3 benchmarks generated from seed data covering the 3 first-slice failure classes |
| Eval results | At least one model evaluated against generated benchmarks with measurable failure rates |
| Research UI | Next.js shell that renders case files, benchmarks, and eval results in a browsable interface |
| Seed data | End-to-end demonstration: raw artifact in, case file + benchmark + eval result out |
| Documentation | README, architecture doc, research methodology — all reflecting actual (not aspirational) state |

## Repo Path

`/Users/coreyalejandro/Projects/the-living-constitution/projects/evaluation/`
