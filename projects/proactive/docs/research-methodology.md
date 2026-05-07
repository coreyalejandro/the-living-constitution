# PROACTIVE Ablation Study Methodology

## Overview

This document describes the ablation study design for evaluating the PROACTIVE constitutional AI safety framework. The study compares 4 variants to measure the contribution of each component to epistemic safety detection.

## Research Question

**How does each component of the PROACTIVE framework contribute to detecting epistemic failures in merge requests?**

## Variants

### 1. PROACTIVE (Full)
- **Components:** COL + Contract Window + Validator (I1-I6) + Drift Detector
- **Blocking:** Errors only
- **Hypothesis:** Best overall detection with balanced precision/recall

### 2. PROACTIVE-lite
- **Components:** COL + Contract Window + Validator (I1-I5 only)
- **Excluded:** Drift Detector, I6 invariant
- **Hypothesis:** Good detection but misses error suppression and drift

### 3. PROACTIVE-strict
- **Components:** All of PROACTIVE
- **Blocking:** Both errors AND warnings
- **Hypothesis:** Highest precision but lower developer experience

### 4. Baseline
- **Components:** None (no safety checks)
- **Blocking:** Never
- **Hypothesis:** Zero detection (control group)

## Test Data

### Composition

| Category | Count | Description |
|----------|-------|-------------|
| Failure cases | 50 | MRs with epistemic failures (F1-F5) |
| Clean cases | 50 | MRs with no violations |
| Edge cases | 20 | Boundary conditions and ambiguous cases |
| **Total** | **120** | |

### Failure Class Distribution

| Class | Count | Description |
|-------|-------|-------------|
| F1 | 10 | Confident false claims |
| F2 | 10 | Phantom completion |
| F3 | 10 | Persistence under correction |
| F4 | 10 | Harm-risk coupling |
| F5 | 10 | Cross-episode drift |

### Clean Case Design

All 50 clean cases:
- Include issue references ("Fixes #NNN")
- Use hedged language (no absolute claims)
- Describe specific, scoped changes
- Do not contain error suppression patterns

### Edge Case Design

20 edge cases test boundary conditions:
- Empty descriptions
- Very short descriptions
- Very long descriptions
- Properly tagged claims ([verified], [inferred])
- Mixed hedging and certainty
- Code blocks in descriptions
- Multiple issue references

## Evaluation Metrics

| Metric | Formula | Description |
|--------|---------|-------------|
| Accuracy | (TP + TN) / Total | Overall correctness |
| Precision | TP / (TP + FP) | % of flags that are real |
| Recall | TP / (TP + FN) | % of real issues flagged |
| F1 Score | 2 * P * R / (P + R) | Harmonic mean of P and R |
| FPR | FP / (FP + TN) | False positive rate |
| Latency | avg(time per case) | Processing speed |

### Classification Rules

- **True Positive (TP):** Failure case correctly flagged/blocked
- **True Negative (TN):** Clean case correctly approved
- **False Positive (FP):** Clean case incorrectly flagged/blocked
- **False Negative (FN):** Failure case incorrectly approved

## Running the Study

```bash
# Run full ablation study
python -m research.run_ablation

# Output to file
python -m research.run_ablation --output results.md

# Run single variant
python -m research.run_ablation --variant proactive-full

# Output raw JSON metrics
python -m research.run_ablation --json
```

## Expected Results

### Hypothesis

| Variant | Expected Accuracy | Expected Recall | Expected FPR |
|---------|-------------------|-----------------|---------------|
| Full | >85% | >80% | <10% |
| Lite | >75% | >70% | <10% |
| Strict | >80% | >80% | <15% |
| Baseline | ~50% | 0% | 0% |

### Key Predictions

1. **Full > Lite:** Drift detector and I6 add meaningful detection
2. **Strict >= Full (recall):** Same detection, more blocking
3. **Strict > Full (FPR):** Warnings become blocks, more false positives
4. **Baseline = 0 recall:** No checks means no detection
5. **Full best F1:** Best balance of precision and recall

## Limitations

- **Regex-only:** LLM augmentation disabled for reproducibility
- **Synthetic data:** Test cases are synthetic, not from real MRs
- **Single run:** No statistical significance testing (future work)
- **No runtime testing:** Only static analysis of MR descriptions

## Reproducibility

All test data is defined in `research/test_data.py`. The ablation runner uses deterministic regex-based analysis (no LLM calls) to ensure reproducible results across runs.

```bash
# Verify reproducibility
python -m research.run_ablation --json > run1.json
python -m research.run_ablation --json > run2.json
diff run1.json run2.json  # Should be identical
```

## V&T Statement

- **EXISTS:** Ablation framework, 4 variants, 120 test cases, evaluation metrics
- **VERIFIED AGAINST:** Test data definitions, variant configurations, metric formulas
- **NOT CLAIMED:** LLM-augmented detection, real-world MR data, statistical significance
- **STATUS:** COMPLETE
