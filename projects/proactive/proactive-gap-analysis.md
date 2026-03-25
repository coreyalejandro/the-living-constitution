# PROACTIVE Gap Analysis

## What Exists, What's Missing, What's Broken

**Date:** 2026-03-23
**Source repo:** `/Users/coreyalejandro/Projects/proactive-gitlab-agent/`
**Assessment method:** Direct source code inspection, test file enumeration, CI config review

---

## 1. What Exists (Verified)

### Core Validation Engine (Operational)

| Module | File | Lines | Status |
|--------|------|-------|--------|
| `validator.py` | `src/proactive/validator.py` | ~719 | Operational |
| `mr_analyzer.py` | `src/proactive/mr_analyzer.py` | ~192 | Operational |
| `report_formatter.py` | `src/proactive/report_formatter.py` | ~78 | Operational |
| `cli.py` | `src/proactive/cli.py` | ~90 | Operational |

**Details:**
- Six invariant checkers (I1-I6) implemented as pure functions with regex pattern matching
- Frozen dataclasses (`Violation`, `ValidationResult`) enforce immutability
- `check_invariants()` aggregator runs all six checks in sequence
- SARIF output generation for IDE integration
- `generate_report()` produces structured JSON with gate pass/fail logic

### Cognitive Operating Layer (Operational)

| Module | File | Lines | Status |
|--------|------|-------|--------|
| `col.py` | `src/proactive/col.py` | ~440 | Operational |
| `contract_window.py` | `src/proactive/contract_window.py` | ~251 | Operational |
| `drift_detector.py` | `src/proactive/drift_detector.py` | ~189 | Operational |

**Details:**
- `parse_intent()` extracts action, target, goal from natural language via regex heuristics
- `compile_intent()` produces a frozen `IntentReceipt` with risk assessment, constraints, and trace ID
- `ContractWindowState` renders persistent bidirectional intent display in GitLab Markdown
- `detect_drift()` compares new definitions in diffs against intent-derived relevance keywords
- Domain keyword expansion for auth, payment, email, analytics, database, test domains

### LLM-Augmented Analysis (Partial)

| Module | File | Lines | Status |
|--------|------|-------|--------|
| `llm_client.py` | `src/proactive/llm_client.py` | ~225 | Partial |

**Details:**
- Anthropic Claude SDK integration with graceful degradation (returns `None` when no API key)
- Three semantic analysis methods: `extract_claims_semantic`, `check_invariants_semantic`, `assess_drift_semantic`
- Three prompt templates in `src/proactive/prompts/`: `extract_claims.txt`, `check_invariants.txt`, `assess_drift.txt`
- Degradation path: LLM unavailable -> falls back to regex-based analysis
- **Gap:** LLM methods are not yet wired into `analyze_mr()` pipeline; regex path is the only active path

### GitLab Integration (Partial)

| Module | File | Lines | Status |
|--------|------|-------|--------|
| `gitlab_client.py` | `src/proactive/gitlab_client.py` | ~159 | Partial |
| `interactive.py` | `src/proactive/interactive.py` | ~120 | Partial |

**Details:**
- `GitLabClient` uses `httpx` to fetch MR context, changes, notes, and pipelines from GitLab API
- `post_review_comment()` posts markdown review to MR notes
- Config reads `GITLAB_TOKEN`, `CI_PROJECT_ID`, `CI_MERGE_REQUEST_IID` from environment
- **Gap:** `httpx` is not in `pyproject.toml` dependencies; will fail on fresh install
- `interactive.py` handles ambiguity resolution via stdin dialogue but is not wired into `cli.py`

### Test Suite (Validated)

| Test File | Covers |
|-----------|--------|
| `test_validator.py` | I1-I6 checks, report generation, SARIF |
| `test_mr_analyzer.py` | Claim extraction, MR analysis, phantom detection |
| `test_report_formatter.py` | Markdown formatting |
| `test_cli.py` | CLI entry point |
| `test_col.py` | Intent parsing, risk assessment, compile_intent |
| `test_contract_window.py` | Contract state creation, markdown rendering |
| `test_drift_detector.py` | Drift detection |
| `test_gitlab_client.py` | GitLab API client |
| `test_llm_client.py` | LLM client with mocked Anthropic |
| `test_fixtures.py` | Fixture validation |

**Claimed:** 58 tests, 83% coverage (README claim). Bytecode present for Python 3.11, 3.12, 3.13.

### CI/CD (.gitlab-ci.yml) (Validated)

- Two stages: `test` (pytest with coverage) and `review` (PROACTIVE MR review on merge_request_event)
- Image: `python:3.11-slim`
- Coverage parsing regex configured

### Validation Evidence (Validated)

- `docs/evidence/validation_results.json`: 8 test cases, 19 violations detected across I1-I6
- 100% detection rate, 0% false positive rate
- Clean sample (tc07) correctly produced zero violations
- Multi-violation sample (tc08) correctly detected 5 violations across I1 and I2

### Documentation (Validated)

- `docs/compliance/`: 3 review documents (codebase, prompt, stakeholder)
- `docs/evidence/`: validation results + research survey
- `docs/foundations/`: framework guide, PRD, research kit, theory of action, theory of change
- `docs/plans/`: 3 planning documents including a 3-day production launch plan

---

## 2. What's Missing

### Critical Gaps

| Gap | Impact | Severity |
|-----|--------|----------|
| `httpx` not in `pyproject.toml` dependencies | `gitlab_client.py` import fails on clean install | Critical |
| `anthropic` not in `pyproject.toml` dependencies | `llm_client.py` import fails (currently handled by try/except) | Medium |
| LLM path not wired into `analyze_mr()` | Semantic checks (O(1) for loop code, etc.) never execute | High |
| No `__main__.py` | `python -m proactive` does not work without it | Medium |
| Interactive mode not accessible from CLI | `interactive.py` exists but `cli.py` has no `--interactive` flag | Medium |
| No end-to-end integration test with real GitLab API | `gitlab_client.py` only tested with mocks | Medium |
| No `py.typed` marker | Type checkers cannot verify downstream consumers | Low |

### Feature Gaps

| Feature | Description | Priority |
|---------|-------------|----------|
| GitLab Duo agent prompt | `.gitlab/duo/prompts/proactive-system-prompt.md` referenced in README but not verified as present | High |
| Live MR review mode | CLI currently reads from JSON file only; no `--live` flag to fetch from GitLab API | High |
| Contract Window persistence | Rendered as markdown but not posted back to MR as pinned comment | Medium |
| Drift detection in CLI pipeline | `drift_detector.py` exists but is not called from `cli.py` or `analyze_mr()` | Medium |
| COL compilation in CLI pipeline | `col.py` exists but `compile_intent()` is not called from `cli.py` main path | Medium |
| SARIF output from CLI | `generate_sarif()` exists but CLI does not expose `--format sarif` | Low |

---

## 3. What's Broken

### Python Version Issue

`pyproject.toml` specifies `requires-python = ">=3.11"`. Bytecode cache shows compilation for 3.11, 3.12, and 3.13. This is consistent and not broken per se, but:
- The CI image uses `python:3.11-slim` only
- No matrix testing across 3.12/3.13
- Type hint `tuple[str, ...]` syntax (used in `drift_detector.py`, `col.py`) requires 3.9+ (safe)
- `str | None` union syntax (used in `col.py`) requires 3.10+ (safe given >=3.11 requirement)
- `from __future__ import annotations` is correctly applied in all modules

**Verdict:** Not broken, but CI only validates one Python version.

### Dependency Declaration

The `gitlab_client.py` module imports `httpx` at the top level, but `httpx` is not listed in `pyproject.toml` dependencies. On a fresh `pip install -e .`, the import will succeed only if `httpx` is coincidentally installed. This is a real bug that would manifest in production.

### Pipeline Wiring Gaps

The three-layer architecture (COL -> Contract Window -> Validator) is documented and each layer is independently implemented, but they are not wired together in the CLI pipeline:

```
Current CLI path:
  cli.py -> mr_analyzer.analyze_mr() -> validator.check_invariants() -> report_formatter

Missing connections:
  cli.py -X-> col.compile_intent()
  cli.py -X-> contract_window.create_contract_state()
  cli.py -X-> drift_detector.detect_drift()
  cli.py -X-> llm_client (semantic analysis)
  cli.py -X-> interactive mode
```

---

## 4. Inventory Summary

| Category | Count | Status |
|----------|-------|--------|
| Python source modules | 10 | 7 operational, 3 partial |
| Prompt templates | 3 | Operational (not yet wired) |
| Test files | 10 | Operational |
| Documentation files | 11 | Validated |
| CI/CD config | 1 | Operational |
| Validation evidence | 1 JSON | 8 test cases, 19 violations |

---

## V&T Statement

**Exists:** 10 Python modules (validator, mr_analyzer, report_formatter, cli, col, contract_window, drift_detector, gitlab_client, llm_client, interactive), 10 test files, 3 LLM prompt templates, .gitlab-ci.yml, validation_results.json with 100% detection rate, 11 documentation files, pyproject.toml with dev dependencies

**Non-existent:** Full pipeline integration (COL -> Contract Window -> Validator chain is not wired in CLI), live GitLab MR review mode, SARIF CLI output, interactive mode CLI flag, GitLab Duo agent deployment

**Unverified:** Actual test pass rate on current codebase (bytecache present but not executed in this session), httpx import success on clean install, LLM semantic analysis quality against real MRs

**Functional status:** Partial -- Core validator engine is operational and validated. Supporting layers (COL, Contract Window, Drift, LLM) are implemented but not integrated into the execution pipeline. httpx dependency is missing from pyproject.toml.
