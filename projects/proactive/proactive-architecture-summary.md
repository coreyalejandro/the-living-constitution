# PROACTIVE Architecture Summary

## Components, Data Flow, and Integration Points

**Source repo:** `/Users/coreyalejandro/Projects/proactive-gitlab-agent/`
**Language:** Python 3.11+
**Build system:** pyproject.toml (PEP 621)

---

## 1. System Architecture

### Three-Layer Pipeline

PROACTIVE operates as a three-layer pipeline that transforms a merge request into a safety verdict:

```
Layer 1: Intent Capture (COL)
  Input: MR title + description (natural language)
  Output: IntentReceipt (structured intent, constraints, risk, trace ID)

Layer 2: Contract Window
  Input: IntentReceipt + budget state
  Output: ContractWindowState (bidirectional intent, agent needs, risk display)

Layer 3: Validation Engine
  Input: MR description + diff + test artifact status
  Output: MRAnalysisResult (violations, claims, trust score, verdict)
```

### Full Data Flow

```
                    Merge Request JSON
                         |
                    +----+----+
                    |         |
               title+desc    diff
                    |         |
            [col.compile_intent()]
                    |
              IntentReceipt
             /      |       \
            /       |        \
[contract_window   [drift_      [mr_analyzer
 .create_contract   detector     .analyze_mr()]
  _state()]         .detect_     /       \
     |              drift()]   regex    LLM (optional)
     |                |       checks    checks
     |                |         \       /
     |                |     MRAnalysisResult
     |                |          |
     |                |    [report_formatter
     |                |     .format_review_comment()]
     |                |          |
     +-------+--------+----------+
             |
       CLI Output / GitLab Comment
```

---

## 2. Module Inventory

### Core Modules (src/proactive/)

| Module | Lines | Purpose | Dependencies |
|--------|-------|---------|-------------|
| `validator.py` | 719 | I1-I6 invariant checks via regex pattern matching | stdlib only |
| `mr_analyzer.py` | 192 | Claim extraction from MR text + phantom detection | validator |
| `report_formatter.py` | 78 | GitLab-flavored markdown review comments | mr_analyzer |
| `cli.py` | 90 | CLI entry point with argparse | mr_analyzer, report_formatter |
| `col.py` | 440 | Cognitive Operating Layer: intent parsing, risk, constraints | stdlib only |
| `contract_window.py` | 251 | Persistent contract display with agent needs tracking | col |
| `drift_detector.py` | 189 | Scope drift detection comparing diff to intent | col |
| `gitlab_client.py` | 159 | GitLab REST API client for MR operations | httpx, mr_analyzer |
| `llm_client.py` | 225 | Anthropic Claude semantic analysis with degradation | anthropic (optional) |
| `interactive.py` | 120 | Interactive contract negotiation for ambiguous MRs | col, mr_analyzer |
| `__init__.py` | 3 | Package marker with version | none |

### Prompt Templates (src/proactive/prompts/)

| File | Purpose | Used By |
|------|---------|---------|
| `extract_claims.txt` | Instruct LLM to extract verifiable claims from MR text | `llm_client.extract_claims_semantic()` |
| `check_invariants.txt` | Instruct LLM to check I1-I6 at semantic level | `llm_client.check_invariants_semantic()` |
| `assess_drift.txt` | Instruct LLM to detect scope drift between intent and diff | `llm_client.assess_drift_semantic()` |

### Test Modules (tests/)

| File | Covers | Test Count |
|------|--------|-----------|
| `test_validator.py` | I1-I6 checks, report, SARIF | ~15 |
| `test_mr_analyzer.py` | Claim extraction, MR analysis | ~10 |
| `test_report_formatter.py` | Markdown formatting | ~5 |
| `test_cli.py` | CLI entry point | ~5 |
| `test_col.py` | Intent parsing, risk, compile | ~8 |
| `test_contract_window.py` | Contract state, rendering | ~5 |
| `test_drift_detector.py` | Drift detection | ~5 |
| `test_gitlab_client.py` | API client (mocked) | ~3 |
| `test_llm_client.py` | LLM client (mocked) | ~3 |
| `test_fixtures.py` | Fixture validation | ~2 |

---

## 3. Data Structures

All data structures use frozen dataclasses for immutability.

### Validation Layer

```python
@dataclass(frozen=True)
class Violation:
    violation_id: str       # "V-XXXX" unique identifier
    invariant: str          # "I1" through "I6"
    severity: str           # "ERROR" or "WARNING"
    location: Dict          # {file, line, context}
    message: str            # Human-readable violation description
    suggested_fix: str      # Actionable remediation
    evidence: Dict          # Pattern match evidence
    rule_id: str            # Machine-readable rule identifier

@dataclass(frozen=True)
class Claim:
    text: str               # The claim sentence
    claim_type: str         # "completion", "performance", "correctness", "existence"
    source: str             # "description", "comment", "diff_comment"

@dataclass(frozen=True)
class MRContext:
    title: str
    description: str
    diff: str
    test_artifacts_exist: bool
    comments: List[str]
    linked_issues: List[str]
```

### COL Layer

```python
@dataclass(frozen=True)
class ParsedIntent:
    action: str             # "create", "modify", "delete", etc.
    target: str             # Target entity
    goal: str               # Inferred purpose
    confidence: float       # 0.0-1.0
    ambiguities: tuple[str, ...]

@dataclass(frozen=True)
class IntentReceipt:
    id: str                 # "col-{timestamp}-{uuid}"
    timestamp: str
    raw_input: str
    parsed_intent: ParsedIntent
    constraints: tuple[Constraint, ...]
    risk_assessment: RiskAssessment
    trace_id: str           # "trace-{uuid}"
    validation_status: str  # "valid", "ambiguous", "rejected"

@dataclass(frozen=True)
class ContractWindowState:
    user_intent_human: str
    user_intent_machine: ParsedIntent
    working_budget: WorkingBudget
    agent_needs: AgentNeeds
    risk_assessment: RiskAssessment
    constraints: tuple[Constraint, ...]
    status: str             # "pending", "confirmed", "executing", etc.
```

---

## 4. Integration Points

### GitLab CI/CD

```yaml
# Trigger: merge_request_event
# Input: MR JSON context file
# Output: Exit code 0 (pass) or 1 (block)
# Stage: review (after test stage)
```

### GitLab REST API (via gitlab_client.py)

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/projects/{id}/merge_requests/{iid}` | GET | Fetch MR details |
| `/projects/{id}/merge_requests/{iid}/changes` | GET | Fetch diff |
| `/projects/{id}/merge_requests/{iid}/notes` | GET | Fetch comments |
| `/projects/{id}/merge_requests/{iid}/pipelines` | GET | Check test artifacts |
| `/projects/{id}/merge_requests/{iid}/notes` | POST | Post review comment |

### Anthropic Claude API (via llm_client.py)

| Method | Model | Purpose |
|--------|-------|---------|
| `extract_claims_semantic()` | claude-sonnet-4-6 | Semantic claim extraction |
| `check_invariants_semantic()` | claude-sonnet-4-6 | Semantic I1-I6 checking |
| `assess_drift_semantic()` | claude-sonnet-4-6 | Semantic drift assessment |

Model can be overridden per-method via `PROACTIVE_MODEL_CLAIMS`, `PROACTIVE_MODEL_INVARIANTS`, `PROACTIVE_MODEL_DRIFT` environment variables.

### SARIF Output (for IDE integration)

The validator generates SARIF 2.1.0 format output consumable by:
- VS Code SARIF Viewer
- GitHub Code Scanning
- Any SARIF-compatible security tool

---

## 5. Invariant Specification

### Pattern-Based Detection (Regex Layer)

| Invariant | Pattern Strategy | Severity |
|-----------|-----------------|----------|
| I1 | Match absolute terms, check 300-char window for epistemic tags | ERROR |
| I2 (file) | Extract quoted filenames from creation claims, stat filesystem | ERROR |
| I2 (artifact) | Match completion+all patterns, check 150-char window for evidence | ERROR |
| I3 | Extract confidence float, compare to 0.8 threshold, check for verification keywords | WARNING |
| I4 | Match decision verbs, check 400-char window for trace references | ERROR |
| I5 | Match hedging+certainty in same regex capture | WARNING |
| I6 | Match error bypass patterns, bare except:pass, empty catch blocks | ERROR |

### Semantic Detection (LLM Layer, Optional)

The LLM layer supplements regex with understanding:
- O(1) claims for loop-containing code (I1 -- regex cannot detect this)
- "Handles all edge cases" without enumeration (I2 -- requires semantic understanding)
- Performance claims contradicted by algorithmic complexity (I1 -- requires code comprehension)

### Gate Logic

```python
gate_result = "PASS"
if fail_on_error and errors > 0:
    gate_result = "FAIL"
elif fail_on_warning and warnings > 0:
    gate_result = "FAIL"
elif warnings > warning_threshold:  # default: 5
    gate_result = "FAIL"
```

---

## 6. Configuration

### Default Configuration (in validator.py)

The `DEFAULT_CONFIG` dict contains all invariant patterns, severity levels, gate thresholds, and logging settings. No external config file is required. Configuration is passed as an optional parameter to all check functions, enabling customization without mutation.

### Environment Variables

| Variable | Required | Purpose |
|----------|----------|---------|
| `GITLAB_TOKEN` or `CI_JOB_TOKEN` | For live mode | GitLab API authentication |
| `CI_PROJECT_ID` | For live mode | Target project |
| `CI_MERGE_REQUEST_IID` | For live mode | Target MR |
| `CI_API_V4_URL` | No (defaults to gitlab.com) | Custom GitLab instance |
| `ANTHROPIC_API_KEY` | No | Enables LLM semantic analysis |
| `PROACTIVE_MODEL_CLAIMS` | No | Override model for claim extraction |
| `PROACTIVE_MODEL_INVARIANTS` | No | Override model for invariant checking |
| `PROACTIVE_MODEL_DRIFT` | No | Override model for drift detection |

---

## 7. Dependency Map

```
proactive (core)
  ├── pyyaml >= 6.0
  └── (stdlib: re, json, uuid, dataclasses, datetime, pathlib)

proactive[gitlab]
  └── httpx >= 0.27

proactive[llm]
  └── anthropic >= 0.40

proactive[dev]
  ├── pytest >= 8.0
  └── pytest-cov >= 5.0
```

---

## V&T Statement

**Exists:** Complete architecture documentation covering all 10 source modules, 3 prompt templates, 10 test files, data structures, integration points, invariant specifications, configuration, and dependency map -- all derived from direct source code inspection

**Non-existent:** Full pipeline wiring between layers (COL -> Contract Window -> Validator chain exists as modules but is not integrated in CLI), live GitLab deployment

**Unverified:** Actual test execution results on current codebase, LLM semantic analysis quality in production scenarios

**Functional status:** Partial -- All architectural components are implemented and individually tested. The integration layer (CLI pipeline wiring) is the remaining work to make the architecture operational end-to-end.
