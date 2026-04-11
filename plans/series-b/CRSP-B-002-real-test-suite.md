# CRSP-B-002: Real Test Suite

## Contract Identity

| Field | Value |
|-------|-------|
| Contract ID | CRSP-B-002 |
| Series | Series B — Fellowship-Ready Refactor |
| Title | Real Test Suite |
| Depends On | CRSP-B-001 |
| Completion Marker | `plans/series-b/.done-B-002` |
| Branch | `claude/refactor-repo-voice-UEFMp` |

## Pre-Flight Check

```bash
test -f plans/series-b/.done-B-001 || { echo "BLOCKED: CRSP-B-001 not complete"; exit 1; }
```

## Why This Contract Exists

The repo has zero executable tests. `tests/` contains 5 JSON fixtures. No pytest, no jest, nothing that runs. For a repo that claims to enforce safety invariants, having no test suite is a credibility gap. A fellowship reviewer who runs `pytest` and gets nothing back will move on.

This contract creates a real pytest suite that tests the real code: the Guardian Kernel, the Sandbox Engine, and the Governance Chain verifier.

## Pre-Flight Reads (MANDATORY)

1. `src/guardian.py` — the full file. Understand the state machine, bootstrap_trinity(), load_invariants(), evaluate_invariants()
2. `projects/sandbox-runtime/src/engine.py` — the full SandboxEngine class
3. `projects/sandbox-runtime/src/jail.py` — the full jail module: resolve_safe_script_path, safe_exec_script, _restricted_import
4. `projects/sandbox-runtime/src/governance_connector.py` — poll_halt_authority
5. `projects/sandbox-runtime/src/evidence_ledger.py` — append_entry, constitutional_hash
6. `tests/failure_modes/` — read all 5 JSON fixtures to understand the failure taxonomy
7. `requirements-dev.txt` — check what's already there

## Ordered Operations

### OP-1: Set up test infrastructure

Create/update `requirements-dev.txt`:
```
pytest>=8.0
pytest-cov>=5.0
```

Create `pytest.ini` at repo root:
```ini
[pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
```

Create directory structure:
```
tests/
  __init__.py
  test_guardian_bootstrap.py
  test_sandbox_jail.py
  test_sandbox_engine.py
  test_evidence_ledger.py
  test_failure_taxonomy.py
  failure_modes/          (already exists — keep the JSON fixtures)
```

### OP-2: Write test_guardian_bootstrap.py

Test the Guardian Kernel's Trinity bootstrap and invariant loading. These tests verify the core safety mechanism works.

**What to test (minimum 8 tests):**

1. `test_trinity_files_exist` — all three Trinity files exist in repo root
2. `test_trinity_files_not_empty` — none are zero bytes
3. `test_trinity_hashes_are_sha256` — bootstrap produces valid SHA-256 hex strings
4. `test_invariant_count_minimum` — at least 7 constitutional invariants loaded (the contract requirement)
5. `test_invariant_ids_unique` — no duplicate invariant IDs
6. `test_invariant_ids_have_required_fields` — every invariant has id, name, severity, rule
7. `test_read_only_files_defined` — CONSTITUTION_READ_ONLY_FILES is non-empty and contains the Trinity files
8. `test_agent_ids_defined` — AGENT_IDS contains the 6 expected agents
9. `test_guardian_state_machine_has_required_states` — all states in GuardianState enum exist (INIT through FAIL_HALT)
10. `test_agent_forbidden_tools_complete` — every agent in AGENT_IDS has an entry in INVARIANT_ARTICLE_IV_01's agent_forbidden_tools

**Implementation notes:**
- Import directly from `src.guardian` (the repo root has `src/guardian.py`)
- For bootstrap tests that would call `sys.exit()`, use `pytest.raises(SystemExit)` or test the underlying logic without calling the full bootstrap
- The MCP import (`from mcp.server.fastmcp import FastMCP`) may not be available in test env. Mock it or test around it. Check if `mcp` is in requirements first. If not installable, write tests that import the constants and data structures directly without triggering the MCP import at module level. One approach: read `src/guardian.py` as text and parse the constants, or restructure the import.

**Practical approach for MCP dependency:** If `from mcp.server.fastmcp import FastMCP` blocks import, create a minimal mock:
```python
# tests/conftest.py
import sys
from unittest.mock import MagicMock

# Mock MCP before guardian tries to import it
if "mcp" not in sys.modules:
    mcp_mock = MagicMock()
    sys.modules["mcp"] = mcp_mock
    sys.modules["mcp.server"] = mcp_mock.server
    sys.modules["mcp.server.fastmcp"] = mcp_mock.server.fastmcp
    mcp_mock.server.fastmcp.FastMCP = MagicMock()
```

### OP-3: Write test_sandbox_jail.py

Test the namespace jail — the actual security boundary of the sandbox.

**What to test (minimum 8 tests):**

1. `test_reject_absolute_path` — absolute paths raise SandboxJailError
2. `test_reject_traversal` — `../` in paths raises SandboxJailError
3. `test_resolve_safe_script_in_allowed_root` — a script under `projects/sandbox-runtime/samples/safe.py` resolves
4. `test_resolve_rejects_outside_allowed_roots` — a script path outside allowed roots raises SandboxJailError
5. `test_restricted_import_blocks_os` — importing `os` raises ImportError
6. `test_restricted_import_blocks_subprocess` — importing `subprocess` raises ImportError
7. `test_restricted_import_allows_math` — importing `math` succeeds
8. `test_restricted_import_allows_json` — importing `json` succeeds
9. `test_safe_exec_blocks_open` — `safe_exec_script("open('/etc/passwd')", "evil.py")` raises NameError or similar (open is not in safe builtins)
10. `test_safe_exec_runs_safe_code` — `safe_exec_script("x = 1 + 1", "safe.py")` returns globals with `x == 2`
11. `test_safe_exec_injects_extra_globals` — extra_globals are available inside executed code

**Import from:** `projects.sandbox-runtime.src.jail` — but note the hyphen in `sandbox-runtime` makes direct Python import impossible. Use `importlib` or `sys.path` manipulation:

```python
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent / "projects" / "sandbox-runtime"))
from src.jail import (
    SandboxJailError, resolve_safe_script_path, safe_exec_script,
    _restricted_import, _reject_traversal
)
```

### OP-4: Write test_sandbox_engine.py

Test the SandboxEngine execution substrate.

**What to test (minimum 5 tests):**

1. `test_engine_creates_evidence_file` — after emit_evidence, the evidence path file exists
2. `test_engine_evidence_is_jsonl` — each line in evidence file is valid JSON
3. `test_engine_halt_stops_loop` — calling halt() before run_execution_loop causes it to return "halted"
4. `test_engine_max_iterations` — loop with no halt returns "completed" after max_iterations
5. `test_engine_execute_script_safe` — executing `samples/safe.py` returns "success"
6. `test_engine_execute_script_blocked` — executing `samples/evil_import.py` raises an exception

**Import approach:** Same sys.path trick as OP-3.

### OP-5: Write test_evidence_ledger.py

Test the evidence ledger (Gold Star audit trail).

**What to test (minimum 4 tests):**

1. `test_constitutional_hash_returns_hex` — constitutional_hash returns a 64-char hex string
2. `test_ensure_initialized_creates_file` — in a temp directory with a dummy constitution file, ensure_initialized creates SANDBOX_LOG.md
3. `test_append_entry_adds_row` — after append_entry, the file has one more row
4. `test_append_entry_includes_invariant_tag` — when related_invariant is passed, the action field contains it

**Use `tmp_path` fixture** to create isolated test environments.

### OP-6: Write test_failure_taxonomy.py

Test that the failure taxonomy fixtures are valid and complete.

**What to test (minimum 5 tests):**

1. `test_all_failure_modes_have_cases` — F1 through F5 each have at least one case file
2. `test_case_schema_valid` — every JSON case has: caseId, failureType, input, expectedBehavior, actualBehavior, constitutionalRule, verdict
3. `test_failure_types_cover_all_domains` — F1 (Epistemic), F2 (Phantom), F3 (Persistence), F4 (Harm-risk), F5 (Cross-episode) all present
4. `test_verdicts_are_valid` — every verdict is one of: VIOLATION, FLAGGED, BLOCKED
5. `test_constitutional_rules_reference_invariants` — every constitutionalRule field references at least one I-number (I1-I6) or E

### OP-7: Run the test suite

```bash
pip install -r requirements-dev.txt
pytest tests/ -v --tb=short 2>&1 | tee plans/series-b/B-002-test-output.txt
```

**Minimum passing threshold:** 25 tests pass. If any tests fail due to environment issues (missing packages, path issues), fix them. Do not skip tests — fix them or document why they cannot run in this environment.

## Acceptance Criteria

| AC | Requirement | Verification |
|----|-------------|--------------|
| AC-001 | `pytest.ini` exists at repo root | `test -f pytest.ini` |
| AC-002 | At least 5 test files exist in `tests/` | `ls tests/test_*.py \| wc -l` >= 5 |
| AC-003 | `conftest.py` handles MCP mock | `test -f tests/conftest.py` |
| AC-004 | `pytest tests/ -v` runs with 25+ passes | Check test output |
| AC-005 | No test files import external packages beyond pytest and stdlib | grep for non-stdlib imports |
| AC-006 | Test output saved | `test -f plans/series-b/B-002-test-output.txt` |

## Completion

```bash
echo "CRSP-B-002 COMPLETE" > plans/series-b/.done-B-002
git add tests/ pytest.ini requirements-dev.txt plans/series-b/.done-B-002 plans/series-b/B-002-test-output.txt
git commit -m "test: add real pytest suite — guardian, sandbox, jail, evidence, taxonomy

Series B contract CRSP-B-002. 25+ tests covering Guardian Kernel bootstrap,
Sandbox jail security boundary, Engine execution, Evidence ledger, and
Failure taxonomy fixtures. Zero tests existed before this contract."
```
