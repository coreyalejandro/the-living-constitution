# PROACTIVE

## Constitutional Epistemic Safety Agent for GitLab Duo Chat

**Version:** 4.0.0  
**Language:** Python  
**License:** MIT  
**Status:** Production-ready within defined hackathon scope

---

## Description

PROACTIVE is a constitutional AI safety agent that enforces **epistemic reliability** in software workflows.

It evaluates whether claims made about code are grounded in verifiable evidence.

> **Are the claims being made about this code actually true?**

This includes claims about:

- Completion
- Correctness
- Coverage
- Security
- Implementation status
- Alignment between intent and output

---

## What PROACTIVE Does

PROACTIVE analyzes merge requests, descriptions, diffs, and metadata against a constitutional framework.

It detects:

- Unsupported claims
- Phantom work
- Unverified confidence
- Missing traceability
- Intent–implementation drift
- Safety violations hidden behind fluent language

It produces deterministic outcomes:

- **APPROVED**
- **FLAGGED**
- **BLOCKED**
- **DRIFT_DETECTED**
- **PENDING_CLARIFICATION**

---

## Why This Exists

AI-assisted development introduces a critical failure mode:

> Confident claims are made without verifiable evidence.

Examples:

- "fully implemented" with no artifacts
- "98% test coverage" without proof
- "production-ready" without validation
- Security claims without verification

PROACTIVE treats these as **epistemic safety failures**.

---

## Core Architecture

```text
MR Event
→ cli.py
→ mr_analyzer.py
→ COL
→ Contract Window
→ Validator
→ Drift Detector
→ report_formatter.py
→ gitlab_client.py
```

### Layer 1 — COL (Cognitive Operating Layer)

**File:** `proactive/col.py`

Parses MR title and description into structured intent.

**Outputs:**

- `action`
- `target`
- `scope`
- `goal`
- `constraints`
- `ambiguities`
- `confidence`

**Primary method:** `compile_intent()`  
**Fallback:** regex pattern matching

### Layer 2 — Contract Window

**File:** `proactive/contract_window.py`

Transforms intent into a machine-readable execution contract.

**Outputs:**

- Confirmed vs pending status
- Risk level
- Risk factors
- Working constraints
- Goal framing

**Primary methods:** `create_contract_state()`, `render_contract()`

### Layer 3 — Validator

**File:** `proactive/validator.py`

Checks content against constitutional invariants I1–I6.

**Primary method:** `check_invariants()`  
**Outputs:** `Violation[]`  
**Fallback:** regex checks

> **Note:** I3 requires LLM support.

### Layer 4 — Drift Detector

**File:** `proactive/drift_detector.py`

Compares declared intent against actual diff behavior.

**Primary method:** `detect_drift()`  
**Outputs:** `DriftResult`  
**Extended by:** `semantic_drift_detector.py`

### Layer 5 — Report Formatter

**File:** `proactive/report_formatter.py`

Generates structured markdown review comments.

**Primary method:** `format_review_comment()`

**Sections:**

- Header + Verdict
- Intent
- Contract Window
- Claims
- Violations
- Drift
- Evidence Summary
- V&T Statement

---

## Constitutional Framework

### 9 Principles

1. Privacy-First
2. Reality-Bound
3. Observability
4. Accessibility
5. Constitutional Constraints
6. Truth or Bounded Unknown
7. Intent Integrity
8. Verification Before Action
9. Error Ownership

### 6 Invariants

| Invariant | Meaning |
|-----------|----------------------------------------------|
| I1        | Evidence-First: claims tagged `[verified]`, `[inferred]`, or `[unverified]` |
| I2        | No Phantom Work |
| I3        | Confidence Requires Verification |
| I4        | Traceability Mandatory |
| I5        | Safety Over Fluency |
| I6        | Fail Closed |

### 5 Failure Classes

| Class | Meaning |
|-------|-------------------------------|
| F1    | Confident False Claims |
| F2    | Phantom Completion |
| F3    | Persistence Under Correction |
| F4    | Harm-Risk Coupling |
| F5    | Cross-Episode Drift |

**Base file:** `proactive/constitution.json`

---

## GitLab Integrations

### GitLab Duo Agent

**File:** `.gitlab/duo/agents/proactive-agent.yml`

**Invocation:**

```text
@proactive review this MR for epistemic safety
```

**Catalog ID:** `gid://gitlab/Ai::Catalog::Item/1003424`

**Available tools:**

- `read_file`
- `read_files`
- `run_command`
- `grep`
- `list_dir`
- `find_files`
- `get_commit_diff`
- `run_tests`
- `get_pipeline_errors`
- `ci_linter`

### GitLab Duo Triage Flow

**File:** `.gitlab/duo/flows/proactive-triage.yml`

```text
fetch_mr_context
→ run_proactive_validator
→ score_and_label
→ post_review_comment
→ end
```

### Claude External Agent Flow

**File:** `.gitlab/duo/flows/claude.yaml`

**Supports:**

- Mention triggers
- Issue assignment
- MR reviewer assignment

**Installs:**

- `@anthropic-ai/claude-code@latest`
- Python dependencies
- Local package (editable mode)

---

## Entry Points

### CLI

**File:** `proactive/cli.py`

**Commands:**

- `review`
- `review-api`
- `vt-generate`

**Exit codes:**

| Code | Meaning |
|------|-----------------|
| 0    | APPROVED |
| 1    | BLOCKED |
| 2    | CONFIG_ERROR |
| 3    | API_FAILURE |
| 4    | UNEXPECTED_ERROR |

### Web UI

**File:** `proactive/web_ui.py`  
**Framework:** Flask

**Routes:**

- `GET /`
- `POST /generate`
- `POST /api/generate`

**Run:**

```bash
python -m proactive.web_ui
```

---

## Ablation Study

**Run:**

```bash
python -m research.run_ablation
```

**Variants:**

- `proactive-full`
- `proactive-lite`
- `proactive-strict`
- `baseline`

---

## Example Failure Case

A merge request claims:

- Full implementation
- Complete test coverage
- Production readiness

But the diff is empty.

PROACTIVE detects:

- I2 violation
- Trust collapse
- Intent–artifact drift

**Returns:** `BLOCKED`

---

## Verification & Truth (V&T)

Each output includes:

```text
V&T Statement:
- EXISTS: [verifiable artifacts]
- VERIFIED AGAINST: [checked sources]
- NOT CLAIMED: [unverified items]
- STATUS: [PASS | WARN | BLOCK]
```

---

## System Boundaries

PROACTIVE **does not:**

- Execute code
- Perform runtime validation
- Run tests itself
- Conduct full security audits
- Claim unverified evidence

It **analyzes:**

- Claims
- Diffs
- Metadata
- Context

---

## Installation

```bash
pip install -e ".[dev]"
```

---

## Running Tests

```bash
pytest tests/ -v --cov=proactive --cov-report=term-missing
```

**CI configuration:**

- Python 3.11 slim
- Coverage extraction
- Cobertura artifact output

---

## Project Structure

```text
.
├── .ai-catalog-mapping.json
├── .gitlab-ci.yml
├── .gitlab/
│   └── duo/
│       ├── agents/
│       └── flows/
├── AGENTS.md
├── CLAUDE.md
├── LICENSE
├── NARRATIVE.md
├── PROACTIVE_CODE_REVIEW.md
├── README.md
├── pyproject.toml
├── agents/
├── docs/
├── evidence/
├── flows/
├── proactive/
├── research/
└── tests/
```

---

## Documentation

| File | Description |
|------|-------------|
| `docs/agent-usage.md` | Agent usage guide |
| `docs/submission-final.md` | Final submission document |
| `docs/video-script-final.md` | Video script |
| `docs/demo-runbook-final.md` | Demo runbook |
| `docs/judge-test-guide-final.md` | Judge testing guide |
| `docs/fact-check-boundaries.md` | Fact-check boundaries |
| `docs/research-methodology.md` | Research methodology |
| `docs/semantic-drift.md` | Semantic drift documentation |
| `NARRATIVE.md` | Project narrative |
| `CLAUDE.md` | Claude integration notes |

---

## Design Position

PROACTIVE is:

- A constitutional enforcement engine
- An epistemic safety layer
- A claim-validation system
- A governance primitive

It operates within the broader Living Constitution (TLC) system.

---

## Maintenance Note

There is a nested directory `proactive/proactive/` that contains older or duplicate files. The canonical path is `proactive/`. Cleanup is recommended in a future refactor.

---

## License

MIT
