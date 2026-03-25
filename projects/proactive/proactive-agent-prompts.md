# PROACTIVE Agent Prompts

## Prompt Pack for Uninterrupted Claude Code Continuation

**Purpose:** Each prompt below is a self-contained instruction block for a Claude Code agent session. Copy-paste the relevant prompt to continue PROACTIVE work without re-reading the entire codebase.

---

## Prompt 1: Fix Dependencies and __main__.py

```
CONTEXT:
You are working in /Users/coreyalejandro/Projects/proactive-gitlab-agent/
This is a Python project with pyproject.toml build system.
The gitlab_client.py module imports httpx but httpx is NOT in pyproject.toml dependencies.
The llm_client.py module imports anthropic but anthropic is NOT in pyproject.toml dependencies.
There is no __main__.py, so `python -m proactive` does not work.

TASK:
1. Edit pyproject.toml:
   - Add httpx>=0.27 to [project.dependencies]
   - Add a [project.optional-dependencies] section with:
     llm = ["anthropic>=0.40"]
     gitlab = ["httpx>=0.27"]
     all = ["proactive[llm,gitlab]"]
   - Keep existing dev dependencies

2. Create src/proactive/__main__.py:
   """Allow python -m proactive invocation."""
   from proactive.cli import main
   main()

3. Verify: pip install -e ".[dev]" && python -m proactive --help

DO NOT modify any other files. DO NOT run tests yet.
```

---

## Prompt 2: Wire COL + Contract Window + Drift into CLI

```
CONTEXT:
You are working in /Users/coreyalejandro/Projects/proactive-gitlab-agent/
The following modules exist and are tested independently:
- src/proactive/col.py (compile_intent, parse_intent, assess_risk, extract_constraints)
- src/proactive/contract_window.py (create_contract_state, render_contract_markdown)
- src/proactive/drift_detector.py (detect_drift)
- src/proactive/cli.py (current: loads JSON, calls analyze_mr, formats output)

TASK:
Edit src/proactive/cli.py run_review() to add the following pipeline BEFORE analyze_mr():

1. Build intent text from MR title + description
2. Call compile_intent(intent_text) to get an IntentReceipt
3. Call create_contract_state(receipt) to get ContractWindowState
4. If diff is non-empty, call detect_drift(receipt.parsed_intent, diff, raw_context=description)
5. After analyze_mr(), if drift detected and drift_severity=="major", elevate verdict to FLAGGED
6. When --format is "gitlab", prepend render_contract_markdown(state) to the review output
7. Add --interactive flag; when set and receipt has ambiguities, delegate to interactive.run_interactive_review()

Import the necessary modules at the top of cli.py.
Use immutable patterns. Do not mutate existing data structures.

VERIFY: python -m proactive review --mr-data fixtures/sample.json (if fixture exists)
Then run: pytest tests/test_cli.py -v
```

---

## Prompt 3: Wire LLM Client into MR Analyzer

```
CONTEXT:
You are working in /Users/coreyalejandro/Projects/proactive-gitlab-agent/
- src/proactive/llm_client.py has LLMClient with extract_claims_semantic(), check_invariants_semantic()
- src/proactive/mr_analyzer.py has analyze_mr() that currently uses only regex-based checks
- The LLM client returns None when API key is not configured (graceful degradation)

TASK:
Edit src/proactive/mr_analyzer.py:

1. Add an optional parameter to analyze_mr(): llm_client: LLMClient | None = None
2. Import LLMClient type (use TYPE_CHECKING to avoid circular imports if needed)
3. After regex claim extraction, if llm_client is not None:
   a. Call llm_client.extract_claims_semantic(context.description)
   b. If result is not None, convert to Claim objects and merge with existing claims (deduplicate by text)
4. After regex invariant checks, if llm_client is not None:
   a. Call llm_client.check_invariants_semantic(context.description, "MR_DESCRIPTION")
   b. If result is not None, convert to Violation objects and append to violations (deduplicate by invariant+line)
5. Do NOT break the existing regex-only path. When llm_client is None, behavior must be identical.

VERIFY:
- pytest tests/test_mr_analyzer.py -v (existing tests must still pass)
- Manually verify: with ANTHROPIC_API_KEY unset, analyze_mr() produces same results as before
```

---

## Prompt 4: Add SARIF and Live Mode to CLI

```
CONTEXT:
You are working in /Users/coreyalejandro/Projects/proactive-gitlab-agent/
- src/proactive/cli.py has the review subcommand with --format (text, json, gitlab)
- src/proactive/validator.py has generate_sarif() that converts a report to SARIF 2.1.0
- src/proactive/gitlab_client.py has GitLabClient with fetch_mr_context() and post_review_comment()

TASK:
Edit src/proactive/cli.py:

1. Add "sarif" to --format choices
2. When --format sarif:
   a. Run analysis as normal
   b. Build report via generate_report()
   c. Call generate_sarif(report)
   d. Print JSON output

3. Add --live flag to review subcommand (store_true, default False)
4. When --live is set:
   a. Call GitLabConfig.from_env()
   b. If None, print error about missing env vars and sys.exit(1)
   c. Create GitLabClient(config) using context manager
   d. Call client.fetch_mr_context() to get MRContext
   e. Run normal analysis pipeline
   f. Call client.post_review_comment(formatted_review)
   g. Print: "Review posted to MR !{mr_iid}"

5. When --live is NOT set, require --mr-data as before

VERIFY:
- python -m proactive review --mr-data fixtures/sample.json --format sarif | python -m json.tool
- pytest tests/test_cli.py -v
```

---

## Prompt 5: Integration Tests and Demo Fixtures

```
CONTEXT:
You are working in /Users/coreyalejandro/Projects/proactive-gitlab-agent/
All pipeline wiring is complete. Need integration tests and demo fixtures.

TASK:

1. Create tests/test_integration.py with these test cases:
   a. test_clean_mr_approved: MR with no violations -> APPROVED, trust_score=1.0
   b. test_phantom_completion_blocked: MR claiming "all tests pass" with test_artifacts_exist=False -> BLOCKED, I2 violation
   c. test_scope_drift_flagged: MR with auth intent but email code in diff -> drift detected
   d. test_ambiguous_intent: MR with "do stuff" -> receipt.validation_status == "ambiguous"
   e. test_full_pipeline: Clean MR through COL -> Contract Window -> Validator -> Report

2. Create 5 demo fixture files in fixtures/:
   a. demo_clean_mr.json: {"title": "Refactor auth module", "description": "Extract auth logic into separate service. Tests updated.", "diff": "def auth_service():\n    pass", "test_artifacts_exist": true, "comments": []}
   b. demo_phantom_completion.json: {"title": "Add feature X", "description": "All tests pass. Implementation complete.", "diff": "def feature(): pass", "test_artifacts_exist": false, "comments": []}
   c. demo_confident_lie.json: {"title": "Optimize lookup", "description": "This is definitely O(1) complexity. I am certain the implementation is correct.", "diff": "def lookup(items):\n    for item in items:\n        if item.match: return item", "test_artifacts_exist": false, "comments": []}
   d. demo_scope_drift.json: {"title": "Implement user authentication", "description": "Add login endpoint with JWT tokens", "diff": "def send_welcome_email(user):\n    pass\ndef send_notification(msg):\n    pass", "test_artifacts_exist": true, "comments": []}
   e. demo_mixed_signals.json: {"title": "Update config", "description": "It seems like this is probably the correct approach with high confidence.", "diff": "config = {}", "test_artifacts_exist": true, "comments": []}

VERIFY:
- pytest tests/test_integration.py -v
- python -m proactive review --mr-data fixtures/demo_phantom_completion.json (should BLOCK)
- python -m proactive review --mr-data fixtures/demo_clean_mr.json (should APPROVE)
```

---

## Prompt 6: Full Test Suite Run and Coverage

```
CONTEXT:
You are working in /Users/coreyalejandro/Projects/proactive-gitlab-agent/
All development work is complete. This is the final validation pass.

TASK:
1. Install all dependencies: pip install -e ".[dev]"
2. Run full test suite: pytest tests/ -v --cov=proactive --cov-report=term-missing
3. If any tests fail, fix the failing tests (fix implementation, not tests, unless tests are wrong)
4. Target: 80%+ coverage
5. If coverage is below 80%, identify uncovered lines and add targeted tests
6. Run once more to confirm: pytest tests/ -v --cov=proactive

REPORT: List all test results, coverage percentage, and any fixes applied.
```

---

## V&T Statement

**Exists:** Six agent prompts covering the complete PROACTIVE build pipeline from dependency fixes through final validation, based on verified source code structure

**Non-existent:** Execution of these prompts (they are instructions, not completed work)

**Unverified:** Whether prompts produce expected results when executed (dependent on current codebase state)

**Functional status:** Operational as instruction set -- prompts are deterministic, ordered, and independently executable
