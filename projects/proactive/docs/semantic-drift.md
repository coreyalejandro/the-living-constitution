# Semantic Drift Detection (Enhancement #4)

## Overview

Semantic drift detection enhances PROACTIVE's existing keyword-based drift detector with **TF-IDF cosine similarity analysis**. It compares the semantic content of MR changes against the stated intent to catch:

- **Unrelated code changes** mixed with feature work
- **Scope creep** across unrelated modules
- **Mixed-concern MRs** that should be split

## How It Works

1. **Intent extraction** — Builds a text representation from the COL layer's `IntentReceipt` (action, target, goal, constraints)
2. **Diff parsing** — Extracts added lines per file from the unified diff
3. **TF-IDF vectorization** — Converts both intent and diff text into TF-IDF vectors (no external dependencies)
4. **Cosine similarity** — Computes similarity between intent and diff vectors
5. **Per-file analysis** — Scores each changed file individually to detect mixed concerns
6. **Split detection** — Suggests splitting when high-similarity and low-similarity files coexist

## Scoring

| Similarity Score | Drift Level | Meaning |
|-----------------|-------------|----------|
| > 0.5 | `none` | Diff aligns with intent |
| 0.3 - 0.5 | `warning` | Low semantic overlap |
| < 0.3 | `critical` | Diff is semantically unrelated |

Per-file threshold: files with similarity < 0.2 are flagged as drifted.

## Integration with Existing Drift Detector

Semantic drift detection runs **alongside** the existing keyword-based detector in `drift_detector.py`. The results are combined:

- Keyword detector catches structural mismatches (wrong action/target keywords)
- Semantic detector catches content-level mismatches (unrelated code)
- Both results are reported in the drift section of the V&T statement

## Usage

### Programmatic

```python
from proactive.col import compile_intent
from proactive.semantic_drift_detector import detect_semantic_drift

receipt = compile_intent("Fix the login authentication bug")
result = detect_semantic_drift(receipt, diff_string)

print(result.similarity_score)  # 0.0 - 1.0
print(result.drift_level)       # "none", "warning", "critical"
print(result.file_scores)       # per-file similarity scores
print(result.should_split)      # True if MR should be split
```

### In the Pipeline

Semantic drift detection runs automatically as part of the PROACTIVE review pipeline. No additional configuration is needed.

## Design Decisions

- **No external ML dependencies** — Uses pure Python TF-IDF + cosine similarity for portability
- **Complements, doesn't replace** — Works alongside keyword-based detection
- **Per-file granularity** — Identifies exactly which files are drifted
- **Split suggestions** — Actionable feedback for developers

## Troubleshooting

**Low similarity on valid MRs:** The TF-IDF approach works best when intent descriptions use similar vocabulary to the code. If your MR description is very abstract, consider adding specific technical terms.

**False positives on refactoring MRs:** Refactoring often touches many files with different content. Use descriptive MR titles that mention the specific modules being refactored.
