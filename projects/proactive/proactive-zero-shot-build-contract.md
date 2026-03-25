# PROACTIVE Zero-Shot Build Contract

## Objective

Complete the PROACTIVE implementation by wiring all existing layers into an integrated pipeline, fixing dependency declarations, and producing a demonstrable end-to-end review flow.

**Precondition:** All source modules exist and are individually tested. This contract integrates them.

---

## Phase 1: Dependency and Configuration Fixes

### Task 1.1: Fix pyproject.toml Dependencies

**Input:** `/Users/coreyalejandro/Projects/proactive-gitlab-agent/pyproject.toml`
**Output:** Updated `pyproject.toml` with correct dependencies

**Actions:**
1. Add `httpx>=0.27` to `[project.dependencies]`
2. Add `anthropic>=0.40` to `[project.optional-dependencies]` under a new `llm` extra
3. Add `httpx>=0.27` to `[project.optional-dependencies]` under a new `gitlab` extra
4. Create combined `all` extra that includes both `llm` and `gitlab`

**Acceptance criteria:**
- `pip install -e .` succeeds and `python -c "from proactive.validator import check_invariants"` returns 0
- `pip install -e ".[gitlab]"` succeeds and `python -c "from proactive.gitlab_client import GitLabClient"` returns 0
- `pip install -e ".[all]"` succeeds with both imports

### Task 1.2: Add __main__.py

**Input:** None
**Output:** `src/proactive/__main__.py`

**Content:**
```python
"""Allow `python -m proactive` invocation."""
from proactive.cli import main
main()
```

**Acceptance criteria:**
- `python -m proactive review --mr-data fixtures/sample.json` produces review output

---

## Phase 2: Pipeline Integration

### Task 2.1: Wire COL into CLI Pipeline

**Input:** `src/proactive/cli.py`, `src/proactive/col.py`
**Output:** Updated `cli.py` that calls `compile_intent()` before `analyze_mr()`

**Actions:**
1. After loading MR data, call `compile_intent(f"{title}. {description}")`
2. Store the `IntentReceipt` for downstream use
3. If `receipt.validation_status == "ambiguous"` and `--interactive` flag is set, invoke `interactive.run_interactive_review()`
4. Pass receipt to contract window creation

**Acceptance criteria:**
- CLI output includes intent receipt summary (action, target, confidence)
- Ambiguous intents are logged with a warning

### Task 2.2: Wire Contract Window into CLI Pipeline

**Input:** `src/proactive/cli.py`, `src/proactive/contract_window.py`
**Output:** Updated `cli.py` that creates and displays contract window state

**Actions:**
1. After COL compilation, call `create_contract_state(receipt)`
2. If `--format gitlab`, include `render_contract_markdown(state)` in output
3. Store contract state for drift detection

**Acceptance criteria:**
- `--format gitlab` output includes the persistent contract window markdown block
- Budget and agent needs are displayed correctly

### Task 2.3: Wire Drift Detection into CLI Pipeline

**Input:** `src/proactive/cli.py`, `src/proactive/drift_detector.py`
**Output:** Updated `cli.py` that runs drift detection when diff is present

**Actions:**
1. After COL compilation, if diff is non-empty, call `detect_drift(intent, diff, raw_context=description)`
2. If `drift_result.has_drift`, add drift warnings to the review output
3. Major drift elevates the review from APPROVED to FLAGGED

**Acceptance criteria:**
- MR with unrelated code additions receives drift warning
- MR with on-scope code additions shows no drift

### Task 2.4: Wire LLM Client into analyze_mr (Optional Path)

**Input:** `src/proactive/mr_analyzer.py`, `src/proactive/llm_client.py`
**Output:** Updated `mr_analyzer.py` with optional LLM augmentation

**Actions:**
1. Add optional `llm_client: LLMClient | None = None` parameter to `analyze_mr()`
2. If LLM is available, call `extract_claims_semantic()` and merge with regex claims
3. If LLM is available, call `check_invariants_semantic()` and merge with regex violations
4. Deduplicate violations by invariant + location

**Acceptance criteria:**
- With `ANTHROPIC_API_KEY` unset: behavior identical to current (regex only)
- With `ANTHROPIC_API_KEY` set: semantic claims and violations supplement regex results
- No failure when LLM returns None (graceful degradation maintained)

---

## Phase 3: CLI Enhancement

### Task 3.1: Add --interactive Flag

**Input:** `src/proactive/cli.py`
**Output:** Updated CLI with `--interactive` subcommand option

**Actions:**
1. Add `--interactive` flag to review subcommand
2. When set and intent is ambiguous, delegate to `interactive.run_interactive_review()`
3. When not set, proceed with standard analysis (current behavior)

**Acceptance criteria:**
- `python -m proactive review --mr-data mr.json --interactive` enters interactive mode for ambiguous MRs
- Non-ambiguous MRs proceed normally regardless of flag

### Task 3.2: Add --format sarif Output

**Input:** `src/proactive/cli.py`, `src/proactive/validator.py`
**Output:** CLI supports `--format sarif` for IDE integration

**Actions:**
1. Add `"sarif"` to format choices
2. When `--format sarif`, run analysis, build report, call `generate_sarif()`, print JSON

**Acceptance criteria:**
- `python -m proactive review --mr-data mr.json --format sarif` produces valid SARIF 2.1.0 JSON
- SARIF output can be consumed by VS Code SARIF Viewer extension

### Task 3.3: Add Live GitLab Review Mode

**Input:** `src/proactive/cli.py`, `src/proactive/gitlab_client.py`
**Output:** CLI supports `--live` flag that fetches MR context from GitLab API

**Actions:**
1. Add `--live` flag to review subcommand
2. When set, construct `GitLabConfig.from_env()` and `GitLabClient`
3. Call `fetch_mr_context()` to build MRContext
4. After analysis, call `post_review_comment()` with formatted review
5. Require `GITLAB_TOKEN` and `CI_PROJECT_ID` and `CI_MERGE_REQUEST_IID` environment variables

**Acceptance criteria:**
- `--live` with environment variables set fetches real MR data and posts review
- `--live` without required env vars prints clear error message and exits 1

---

## Phase 4: Test Completion

### Task 4.1: Integration Test for Full Pipeline

**Input:** All wired modules
**Output:** `tests/test_integration.py`

**Actions:**
1. Test the full path: JSON input -> COL compilation -> contract state -> drift check -> analyze_mr -> format
2. Use fixture MRs that exercise each path (clean, ambiguous, drifted, violated)
3. Assert end-to-end verdict matches expected

**Acceptance criteria:**
- 4+ integration test cases covering: clean pass, I2 phantom block, drift flagging, ambiguous intent
- All pass with `pytest tests/test_integration.py -v`

### Task 4.2: Update CI to Test All Extras

**Input:** `.gitlab-ci.yml`
**Output:** Updated CI that tests `.[dev]`, `.[gitlab]`, and `.[all]` extras

**Acceptance criteria:**
- CI runs pytest with `.[dev,gitlab,all]` dependencies installed
- Coverage report still generated

---

## Phase 5: Demo Preparation

### Task 5.1: Create Demo Fixture Set

**Input:** Existing `fixtures/` directory
**Output:** 5 demo fixtures with clear narrative

**Fixture set:**
1. `demo_clean_mr.json` -- Well-written MR, passes all checks (APPROVED)
2. `demo_phantom_completion.json` -- Claims "all tests pass" with no artifacts (BLOCKED, I2)
3. `demo_confident_lie.json` -- Claims O(1) for loop code (BLOCKED, I1)
4. `demo_scope_drift.json` -- Auth intent with email notification code (FLAGGED, drift)
5. `demo_mixed_signals.json` -- Hedging + certainty in same sentence (FLAGGED, I5)

**Acceptance criteria:**
- Each fixture produces the expected verdict when run through CLI
- Narratives are realistic and demonstrate specific failure modes

---

## Dependency Graph

```
Phase 1 (no dependencies)
  |
  v
Phase 2 (depends on Phase 1)
  2.1 COL wiring
  2.2 Contract Window wiring (depends on 2.1)
  2.3 Drift wiring (depends on 2.1)
  2.4 LLM wiring (independent of 2.1-2.3)
  |
  v
Phase 3 (depends on Phase 2)
  3.1 Interactive flag (depends on 2.1)
  3.2 SARIF output (independent)
  3.3 Live mode (depends on Phase 1 httpx fix)
  |
  v
Phase 4 (depends on Phase 2+3)
  |
  v
Phase 5 (depends on Phase 4)
```

---

## Estimated Effort

| Phase | Tasks | Estimate |
|-------|-------|----------|
| Phase 1: Dependency fixes | 2 | 15 minutes |
| Phase 2: Pipeline wiring | 4 | 90 minutes |
| Phase 3: CLI enhancement | 3 | 60 minutes |
| Phase 4: Test completion | 2 | 45 minutes |
| Phase 5: Demo preparation | 1 | 30 minutes |
| **Total** | **12** | **~4 hours** |

---

## V&T Statement

**Exists:** This build contract, based on verified source inspection of all 10 Python modules, 10 test files, and CI config in the proactive-gitlab-agent repository

**Non-existent:** The pipeline integration described in Phase 2, the CLI enhancements in Phase 3, the integration tests in Phase 4, and the demo fixtures in Phase 5

**Unverified:** Time estimates (based on code complexity assessment, not empirical measurement); whether existing tests still pass on current codebase state

**Functional status:** Pending -- This contract defines the work required to move PROACTIVE from Partial (validated modules, unwired pipeline) to Operational (integrated end-to-end review system)
