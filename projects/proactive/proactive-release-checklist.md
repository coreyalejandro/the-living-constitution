# PROACTIVE Release Checklist

## Pre-Release Validation Checklist

**Target:** PROACTIVE v0.1.0 release-ready state
**Source repo:** `/Users/coreyalejandro/Projects/proactive-gitlab-agent/`

---

## 1. Dependencies and Installation

- [ ] `pyproject.toml` lists all runtime dependencies (`pyyaml`, `httpx`)
- [ ] `pyproject.toml` optional dependencies include `anthropic` under `[llm]` extra
- [ ] `pip install -e .` succeeds in a clean virtual environment (Python 3.11)
- [ ] `pip install -e ".[dev]"` installs `pytest` and `pytest-cov`
- [ ] `pip install -e ".[all]"` installs all optional dependencies
- [ ] `python -m proactive --help` prints usage information
- [ ] `python -c "from proactive.validator import check_invariants; print('OK')"` succeeds
- [ ] `python -c "from proactive.gitlab_client import GitLabClient; print('OK')"` succeeds with httpx installed
- [ ] No pinned version conflicts between dependencies

## 2. Test Suite

- [ ] `pytest tests/ -v` runs without import errors
- [ ] All existing tests pass (58 tests baseline)
- [ ] New integration tests pass (`tests/test_integration.py`)
- [ ] Coverage meets 80% threshold: `pytest tests/ --cov=proactive --cov-report=term-missing`
- [ ] Coverage report shows no critical modules below 70% individually:
  - [ ] `validator.py` >= 80%
  - [ ] `mr_analyzer.py` >= 80%
  - [ ] `col.py` >= 70%
  - [ ] `contract_window.py` >= 70%
  - [ ] `drift_detector.py` >= 70%
  - [ ] `cli.py` >= 70%
  - [ ] `llm_client.py` >= 60% (most paths require mocking)
  - [ ] `gitlab_client.py` >= 60% (requires API mocking)
- [ ] No test uses `time.sleep()` or non-deterministic behavior
- [ ] Tests run in under 30 seconds total

## 3. Invariant Validation

- [ ] All 6 invariants produce correct results against known test cases:
  - [ ] I1: Catches "definitely", "certainly", "guaranteed" without epistemic tags
  - [ ] I2: Catches completion claims when `test_artifacts_exist=False`
  - [ ] I2: Catches claimed files that do not exist on disk
  - [ ] I3: Catches confidence >= 0.8 without verification keywords
  - [ ] I4: Catches decision statements without trace chain references
  - [ ] I5: Catches hedging + certainty in same passage
  - [ ] I6: Catches `try: ... except: pass` and error bypass patterns
- [ ] Clean input produces zero violations (tc07_clean_output verified)
- [ ] Multi-violation input produces correct count (tc08_multi_violation verified)
- [ ] `docs/evidence/validation_results.json` matches current validator behavior

## 4. Pipeline Integration

- [ ] COL compilation produces valid `IntentReceipt` from MR title + description
- [ ] Contract Window renders correct markdown for `--format gitlab`
- [ ] Drift detection flags unrelated code additions
- [ ] Drift detection passes on-scope code additions
- [ ] LLM client returns `None` gracefully when `ANTHROPIC_API_KEY` is unset
- [ ] LLM client supplements regex results when API key is set (manual test)
- [ ] Interactive mode activates on ambiguous intent with `--interactive` flag

## 5. CLI Functionality

- [ ] `python -m proactive review --mr-data <file>` produces formatted output
- [ ] `--format text` produces human-readable review
- [ ] `--format json` produces parseable JSON report
- [ ] `--format gitlab` produces GitLab-flavored markdown with contract window
- [ ] `--format sarif` produces valid SARIF 2.1.0 JSON
- [ ] Exit code 0 for APPROVED and FLAGGED verdicts
- [ ] Exit code 1 for BLOCKED verdict
- [ ] `--strict true` blocks on any ERROR-level violation
- [ ] Invalid `--mr-data` path produces clear error message

## 6. CI/CD Configuration

- [ ] `.gitlab-ci.yml` defines `test` and `review` stages
- [ ] `unit-tests` job uses `python:3.11-slim` image
- [ ] `proactive-review` job triggers only on `merge_request_event`
- [ ] `allow_failure: false` ensures MR is blocked on violations
- [ ] Coverage regex matches pytest output format

## 7. Demo Readiness

- [ ] Demo fixtures exist and produce expected verdicts:
  - [ ] `demo_clean_mr.json` -> APPROVED
  - [ ] `demo_phantom_completion.json` -> BLOCKED
  - [ ] `demo_confident_lie.json` -> BLOCKED or FLAGGED
  - [ ] `demo_scope_drift.json` -> FLAGGED (drift detected)
  - [ ] `demo_mixed_signals.json` -> FLAGGED (I5 warning)
- [ ] Demo can be run without network access (no live API calls)
- [ ] Demo output is clean and presentation-ready
- [ ] Demo script (`proactive-demo-script.md`) matches actual CLI output

## 8. Documentation

- [ ] README.md accurately reflects current module set and capabilities
- [ ] README.md Quick Start instructions work on clean install
- [ ] Architecture diagram matches actual data flow
- [ ] Invariant table in README matches validator.py patterns
- [ ] Validation evidence section links to correct file
- [ ] No stale references to removed or renamed modules
- [ ] AGENTS.md instructions are current

## 9. Code Quality

- [ ] No `console.log` or `print()` statements in production code (except CLI output)
- [ ] No hardcoded secrets or API keys
- [ ] All dataclasses use `frozen=True` for immutability
- [ ] All public functions have docstrings
- [ ] No unused imports (run `python -m py_compile` on all modules)
- [ ] File sizes within limits (no module exceeds 800 lines)
- [ ] `from __future__ import annotations` in all modules

## 10. Security

- [ ] `GITLAB_TOKEN` read from environment only, never logged
- [ ] `ANTHROPIC_API_KEY` read from environment only, never logged
- [ ] No sensitive data in test fixtures
- [ ] No API keys in `.gitlab-ci.yml` (uses CI/CD variables)
- [ ] Error messages do not leak internal paths or tokens

---

## Sign-Off

| Reviewer | Date | Status |
|----------|------|--------|
| Automated (pytest) | | Pending |
| Code Review (agent) | | Pending |
| Human (Corey) | | Pending |

---

## V&T Statement

**Exists:** This release checklist with 10 categories and 70+ individual check items, derived from actual source code inspection of the proactive-gitlab-agent repository

**Non-existent:** Completion of checklist items (all are currently Pending), sign-off from automated tests or human review

**Unverified:** Whether all checklist items are achievable with current codebase (some depend on build contract Phase 2+ completion)

**Functional status:** Operational as checklist -- ready for use once build contract phases are complete
