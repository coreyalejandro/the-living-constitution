# Build Contract: PROACTIVE

## Current State (Honest)

- Python + React codebase at `proactive-gitlab-agent/`
- GitLab AI Hackathon submission (gitlab.com/gitlab-ai-hackathon/participants/28441830)
- Branch: `feat/contract-window-v2`
- Last commit: Feb 19, 2026
- validation_results.json exists with claimed metrics
- **Tests broken**: Python version mismatch (system 3.9 vs requires >=3.11)
- `pytest` fails to collect tests

## Target State (What Resume Claims)

"Operational | Validated 2026-01-24 | 100% detection rate across 8 test cases (n=19 violations) | 0% false positive rate (validation report VR-V-15C6)"

## Acceptance Criteria

1. Python >=3.11 available and configured
2. `pip install -e ".[dev]"` succeeds
3. `pytest` collects and passes all tests
4. `validation_results.json` confirms: 8 test cases, 19 violations, 100% detection, 0% FP
5. CLAUDE.md installed in repo

## Evidence Required

```bash
cd /Users/coreyalejandro/Projects/proactive-gitlab-agent
python --version  # >= 3.11
pip install -e ".[dev]"
pytest -v
cat validation_results.json | python -m json.tool | grep -E "detection|false_positive"
```

## Implementation Spec

1. Check if Python 3.11+ is available via pyenv or homebrew
2. If not, install: `brew install python@3.11` or `pyenv install 3.11`
3. Create/activate venv with correct Python
4. Install package in dev mode
5. Run tests, fix any import/compatibility issues
6. Verify validation results match claims

## Repo Path

`/Users/coreyalejandro/Projects/proactive-gitlab-agent/`
