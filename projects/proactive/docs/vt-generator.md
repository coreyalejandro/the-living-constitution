# Interactive V&T Statement Generator (Enhancement #5)

## Overview

The V&T (Verification & Truth) Statement Generator is a standalone tool that analyzes MR descriptions and diffs to produce structured V&T statements with confidence breakdowns. It runs a lightweight version of the PROACTIVE pipeline without requiring API keys.

## Features

- **Claim extraction** with type classification (completion, performance, correctness, security, metric, absolute)
- **Per-claim confidence scoring** based on evidence status
- **V&T statement generation** with EXISTS, VERIFIED AGAINST, NOT CLAIMED, and STATUS sections
- **Multiple output formats**: Markdown and JSON
- **CLI command**: `python -m proactive.cli vt-generate`
- **Web UI**: Interactive browser-based interface
- **JSON API**: Programmatic access at `/api/generate`

## CLI Usage

```bash
# Markdown output (default)
python -m proactive.cli vt-generate --description "Fix the login bug. All tests pass."

# JSON output
python -m proactive.cli vt-generate --description "Fix the login bug." --format json

# With title and diff
python -m proactive.cli vt-generate \
  --title "Fix login auth" \
  --description "Fixes the authentication bug. Implementation complete." \
  --diff-file changes.diff

# From a file
python -m proactive.cli vt-generate --description-file mr_description.txt
```

## Web UI Usage

### Start the server

```bash
# Requires Flask: pip install flask
python -m proactive.web_ui
# Opens at http://localhost:5000
```

### API Endpoint

```bash
curl -X POST http://localhost:5000/api/generate \
  -H "Content-Type: application/json" \
  -d '{"description": "Fix the login bug. All tests pass.", "title": "Fix login"}'
```

## Programmatic Usage

```python
from proactive.vt_generator import generate_vt_statement

result = generate_vt_statement(
    description="Fix the login bug. All tests pass.",
    diff="+++ b/src/auth.py\n+def login(): pass",
    title="Fix login",
)

print(result.overall_confidence)   # 0.0 - 1.0
print(result.total_claims)         # number of claims found
print(result.vt_statement.status)  # PASS, WARN, or BLOCK
print(result.markdown)             # formatted markdown
print(result.as_json)              # JSON string
```

## Confidence Scoring

| Evidence Status | Confidence | Meaning |
|----------------|-----------|----------|
| `verified` | 0.9 - 1.0 | Claim backed by artifacts |
| `inferred` | 0.5 - 0.7 | Claim plausible but not proven |
| `unverified` | 0.2 - 0.3 | Claim lacks evidence |
| `phantom` | 0.1 | Completion claim with no artifacts |

## V&T Statement Structure

Every generated statement includes:

- **EXISTS**: What was analyzed and checked
- **VERIFIED AGAINST**: What sources were used
- **NOT CLAIMED**: What was NOT done (limitations)
- **STATUS**: PASS / WARN / BLOCK with detail
