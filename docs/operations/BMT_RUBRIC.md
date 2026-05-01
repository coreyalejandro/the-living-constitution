# BMT Rubric — Transparent Evaluation Criteria

**Document:** The exact rules used by `bmt_watcher.py` to flag and fix documents.
**Purpose:** You should know exactly what gets flagged, why, and how the fix works.
**Doctrine source:** `/Users/coreyalejandro/Projects/the-living-constitution/docs/2026-03-29_BLIND-MANS-TEST.md`

---

## What is the Blind Man's Test?

The Blind Man's Test (BMT) is a readability and accessibility standard for research documents.
The standard: any smart adult with zero prior knowledge of AI research, statistics, or TLC
governance must be able to read the document and understand what is being claimed, why it matters,
and what the evidence is. No prior exposure required. No jargon tolerance.

This is not a dumbing-down exercise. It is a precision exercise.
A concept you cannot explain to a newcomer is a concept you do not fully understand.

---

## Three Requirements Enforced by bmt_watcher.py

---

### BMT-1 — Abbreviation and Jargon Expansion

**Rule:** Every abbreviation or specialized term must be spelled out in parentheses on its
first use in the document. Every subsequent use may use the short form.

**Trigger condition:** The term appears in the document without a parenthetical expansion
`(...)` of at least 10 characters on the same line, AND the expansion has not appeared
earlier in the document.

**How the fix works:**
The watcher finds the first occurrence of the term and rewrites it as:
  TERM (full meaning here)
All later occurrences are left unchanged.

**Current glossary — every term the watcher knows about:**

| Term | Expansion Applied |
|------|------------------|
| LLM | large language model — an AI system trained on vast text, such as GPT, Claude, or Gemini |
| frontier model | a state-of-the-art AI system at the edge of current capability |
| Constitutional AI | a training method where an AI evaluates its own outputs against a written set of principles before showing them to the user |
| Contract Window | a structured record of what a human-AI session is trying to accomplish, what has been verified, and who is responsible for fixing errors |
| Bicameral Review | two independent review channels that must both approve an output before it reaches the user |
| Insight Atrophy | the gradual erosion of a person's ability to question AI outputs, caused by repeated exposure to fluent but wrong answers |
| Intent Fidelity | whether the AI is still serving the user's actual purpose |
| Invariant Status | whether the hard behavioral rules the AI committed to are still being honored |
| monotropic | a cognitive style characterized by deep, sustained focus on a single task — associated with autistic cognition |
| polytropic | a cognitive style characterized by broad, parallel engagement across many tasks simultaneously |
| mechanistic interpretability | a field of AI research that studies what is happening inside a model's internal computations |
| sparse autoencoder | a tool used in interpretability research to decompose a model's internal representations |
| scalable oversight | a research area focused on how humans can supervise AI systems even when those systems become more capable |
| superposition | in AI: when a model represents more concepts than it has dedicated internal dimensions |
| CRISP-DM | Cross-Industry Standard Process for Data Mining — a standard workflow for data analysis projects |
| Flesch-Kincaid | a readability score — Grade 8 means a typical 8th-grader can understand the text |
| Cohen's kappa | a statistical measure of agreement between two raters — values above 0.70 indicate strong agreement |
| Mann-Whitney | a statistical test that compares two groups without assuming the data follows a normal distribution |
| Tukey HSD | a statistical test comparing every pair of groups after an ANOVA, while controlling for false positives |
| ANOVA | Analysis of Variance — a statistical test checking whether the means of three or more groups differ significantly |
| V&T | Verification and Truth — a statement that separates what is confirmed from what is proposed |
| TLC | The Living Constitution — the runtime enforcement system built alongside this research |
| MCP | Model Context Protocol — an open standard that lets AI models connect to external tools |
| SIAC | Session Intent and Accountability Contract — the structured record co-authored at the start of a session |
| CGL | Cognitive Governance Lab — the research initiative producing this work |
| CAI | Constitutional AI — Anthropic's method for training AI systems to follow behavioral principles |
| CRP | Code-Switching and Representation Practices — the sociolinguistic literature on language adaptation across social contexts |
| MVS | Minimum Viable Sample — the smallest sample size that gives adequate statistical power |
| DPO | Direct Preference Optimization — a technique for training AI systems without a separate reward model |
| RLHF | Reinforcement Learning from Human Feedback — a training method using human evaluators to score model outputs |
| API | Application Programming Interface — a set of rules that lets software programs talk to each other |
| RAG | Retrieval-Augmented Generation — where an AI searches a knowledge base before generating an answer |

**Adding new terms:** Edit the JARGON_GLOSSARY list in `scripts/bmt_watcher.py`.
Each entry is a two-item tuple: (regex_pattern, full_expansion_string).

---

### BMT-2 — Concept-Level Plain Language Explanation

**Rule:** Every concept, governance rule, claim, methodology, or specialized idea introduced
in the document must be followed by at least one plain-language explanatory sentence.
A parenthetical abbreviation expansion (BMT-1) is necessary but NOT sufficient for BMT-2.

The reader must understand:
  1. What the concept is
  2. Why it matters in this specific context
  3. What problem it solves or describes

**Trigger condition:** Semantic analysis via Claude Haiku (Bedrock). The model reads each
section and identifies concepts introduced without adequate follow-up explanation.
The standard applied in the prompt: "readable by a smart adult with zero prior knowledge
of AI research, statistics, or the governance system being described."

**How the fix works:**
The watcher inserts a blockquote immediately after the sentence that introduces the concept:

  > **Plain language:** [1-3 sentence explanation generated by the semantic pass]

The explanation is generated by Claude Haiku and inserted in place. The original text is
not modified — only the explanation is added.

**What the semantic pass does NOT flag:**
- Common everyday words (study, data, test, result)
- Terms already explained earlier in the document
- Author names, dates, citations
- Abbreviations that already have a parenthetical gloss (those are BMT-1 territory)

**Benchmark used to calibrate this standard:**
ChatGPT's translation of the "Sample Size Decision" section of research-plan.md.
That translation demonstrated the gap between abbreviation expansion and actual concept
explanation. The BMT-2 pass is calibrated to close that gap.

The benchmark translation showed:
- Each section header got a plain-language summary of what that section is doing
- Each governance rule (I2: No Phantom Work) got explained as "do not write a plan that
  depends on imaginary capacity"
- Each statistical term got WHY it matters, not just what it stands for
- The overall section purpose was stated before the details were given

BMT-2 is enforced to that standard.

---

### BMT-4 — Status Label Legend

**Rule:** If a document uses CONSTRUCTED, VERIFIED, PENDING, or UNKNOWN tags, a legend
defining those tags must appear at or near the top of the document. These are TLC-internal
codes. An outside reader (fellowship committee, conference reviewer) has no way to know
what they mean without the legend.

**Trigger condition:** Any of `[CONSTRUCTED]`, `[VERIFIED]`, `[PENDING]`, `[UNKNOWN]`
appears in the document AND the legend text "VERIFIED =" and "CONSTRUCTED =" are both absent.

**How the fix works:**
The legend block is inserted immediately after the first top-level heading in the document.
If no heading exists, it is inserted at the top. The legend text:

  > **Status labels used throughout this document:**
  > VERIFIED = confirmed by direct evidence (artifact, transcript, test result).
  > CONSTRUCTED = reasoned and plausible, but not yet tested in a controlled experiment.
  > PENDING = planned as a future deliverable; does not exist yet.
  > UNKNOWN = genuinely uncertain — no evidence either way.
  > These labels appear in brackets throughout. They are not hedging — they are precision.

---

## What bmt_watcher.py Does NOT Check

These items are NOT currently automated and require manual review:

| Gap | Why not automated | How to handle manually |
|-----|------------------|------------------------|
| Overclaims (e.g., "100%", "first", "revolutionary") | Requires claim-vs-evidence matching, not just text analysis | Use `overclaim_checker.py` (separate script) |
| Citation accuracy | Requires external database lookup | Use crossref_verify.py or manual DOI check |
| Observation label discipline (Obs 1 through Obs N must include full description each time) | Requires structural understanding of the paper | Manual audit pass |
| Logical consistency between sections | Requires cross-section reasoning | Manual or LLM review pass |
| BMT-3 (sentence length / grade level) | Not yet implemented | Target Flesch-Kincaid Grade ≤ 10 |
| BMT-5 (visual elements — tables/figures need captions) | Not yet implemented | Manual audit |

---

## How the Two-Phase Pipeline Works

Every time you save a .md file in a watched directory:

**Phase 1 — AUDIT:**
  Pass A (regex, ~0.1s): checks all terms in the glossary against the document.
    Every term without an inline expansion = BMT-1 violation.
    Status tags without a legend = BMT-4 violation.
  Pass B (semantic, ~10-30s per doc): sends each section to Claude Haiku via Bedrock.
    Model returns JSON array of concepts introduced without explanation.
    Each item = BMT-2 violation.
  Sidecar report written: `<filename>.bmt-report.md` next to the original.
  Case-law log entry appended: `artifacts/case-law/bmt-violations.log`.

**Phase 2 — FIX:**
  BMT-4 fix: legend inserted after first heading.
  BMT-1 fix: parenthetical expansion added on first occurrence of each flagged term.
  BMT-2 fix: plain-language blockquote inserted after each flagged concept's sentence.
  Original file patched in place.
  Pipeline continues regardless of violation count.

---

## Separate Script: overclaim_checker.py

BMT does not check for overclaims. Overclaims are a different failure category:
a claim may be perfectly readable (passes BMT) but still unsubstantiated.

`scripts/overclaim_checker.py` handles this separately. It checks for:
  - Quantitative claims without cited evidence (percentages, n=, test counts)
  - Temporal superlatives ("first", "most", "revolutionary", "only")
  - Causal claims without mechanistic explanation
  - Status claims ("validated", "proven", "complete") without artifact reference
  - Internal inconsistencies (same claim stated differently in two places)

Each flag includes: the claim, the violation type, and the correction required.

---

## To Run the Watcher

Single file:
  cd /Users/coreyalejandro/Projects/the-living-constitution
  python3 scripts/bmt_watcher.py --root . --watch docs --run-once /path/to/file.md

Full live watch (runs continuously while you write):
  python3 scripts/bmt_watcher.py --root . --watch /Users/coreyalejandro/cognitive-governance-lab/proposal /Users/coreyalejandro

Regex only (no API cost, no BMT-2):
  python3 scripts/bmt_watcher.py --root . --watch docs --run-once /path/to/file.md --no-semantic

---

V&T:
EXISTS — this rubric document, bmt_watcher.py with Pass A/B/fix logic, JARGON_GLOSSARY with 30 terms.
VERIFIED AGAINST — source code at /Users/coreyalejandro/Projects/the-living-constitution/scripts/bmt_watcher.py; doctrine at docs/2026-03-29_BLIND-MANS-TEST.md.
NOT CLAIMED — overclaim_checker.py exists as a spec in this document; the script itself is written separately.
FUNCTIONAL STATUS — bmt_watcher.py operational and tested on research-plan.md (5 BMT-1 + 108 BMT-2 violations found and fixed, 2026-05-01).
