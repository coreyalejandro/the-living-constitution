# PROACTIVE MR Triage Flow

## Overview

The PROACTIVE MR Triage Flow automatically reviews every merge request for epistemic safety. It runs the full PROACTIVE pipeline, scores severity, assigns labels, posts review comments, and blocks merges on critical violations.

## How It Works

```
MR Event
  ↓
[1] Fetch MR Context
  ├─ Get MR description, diff, changed files
  └─ Extract user intent
  ↓
[2] Run PROACTIVE Validator
  ├─ Check I1-I6 invariants
  ├─ Detect F1-F5 failure classes
  └─ Generate V&T statement
  ↓
[3] Score Severity
  ├─ Calculate weighted violation score
  ├─ Determine labels
  └─ Set merge action (ALLOW/WARN/BLOCK)
  ↓
[4] Assign Labels
  ├─ Create labels if needed
  ├─ Remove old PROACTIVE labels
  └─ Assign new labels to MR
  ↓
[5] Post Review Comment
  ├─ Format V&T statement
  ├─ Include severity info
  └─ Post to MR discussion
  ↓
End
```

## Severity Labels

| Label | Color | Meaning | Action |
|-------|-------|---------|--------|
| `safety-critical` | Red | I6 violation detected | BLOCK merge |
| `epistemic-risk` | Yellow | I1-I5 violations | WARN (review needed) |
| `phantom-work` | Orange | F2 phantom completion | WARN (verify implementation) |
| `proactive-pass` | Green | No violations | ALLOW merge |

## Scoring Algorithm

### Invariant Weights

| Invariant | Base Weight | Description |
|-----------|-------------|-------------|
| I1 | 5 | Evidence-First |
| I2 | 7 | No Phantom Work |
| I3 | 6 | Confidence-Verification |
| I4 | 5 | Traceability |
| I5 | 5 | Safety Over Fluency |
| I6 | 10 | Fail Closed |

### Severity Multipliers

- **ERROR:** 1.0x (full weight)
- **WARNING:** 0.5x (half weight)

### Decision Rules

- **Score >= 10 (I6 ERROR):** BLOCK merge, label `safety-critical`
- **Score >= 7 (I2 ERROR):** BLOCK merge, label `phantom-work`
- **Score >= 5 (I1-I5):** WARN, label `epistemic-risk`
- **Score = 0:** ALLOW merge, label `proactive-pass`

## Example Outputs

### Clean Code (PASS)

```
## PROACTIVE Constitutional Review

✅ Verdict: APPROVED
Trust Score: 100%

### Invariant Checks
✅ No violations detected.

Labels: proactive-pass
Action: ALLOW MERGE
```

### Phantom Completion (BLOCK)

```
## PROACTIVE Constitutional Review

🚫 Verdict: BLOCKED
Trust Score: 15%

### Invariant Violations

ERRORS:
- ❌ [I2] Phantom completion detected. Claims "fully implemented"
  but no implementation files exist.

Labels: phantom-work
Action: BLOCK MERGE
```

## Configuration

The flow is defined in `.gitlab/duo/flows/proactive-triage.yml`.

### Environment Variables

| Variable | Purpose |
|----------|---------|
| `ANTHROPIC_API_KEY` | API key for Claude models |
| `GITLAB_TOKEN` | GitLab API token for label assignment |
| `CI_PROJECT_ID` | Project ID (auto-set in CI) |
| `CI_MERGE_REQUEST_IID` | MR IID (auto-set in CI) |

## Troubleshooting

### Flow doesn't trigger
- Check that the flow is registered in `.gitlab/duo/flows/`
- Verify GitLab Duo Flows are enabled for the project

### Labels not assigned
- Check `GITLAB_TOKEN` has API access
- Verify the token has permission to create/assign labels

### False positives
- Review the V&T statement for specific violations
- Check if claims are properly tagged with evidence levels
- Add `[verified]` or `[inferred]` tags to claims

## Related Documentation

- [Agent Usage Guide](agent-usage.md)
- [PROACTIVE Framework](../NARRATIVE.md)
- [Research Methodology](research-methodology.md)
