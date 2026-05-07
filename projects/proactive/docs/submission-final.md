# PROACTIVE — Constitutional Epistemic Safety Agent for GitLab Duo

**GitLab AI Hackathon Submission**

---

## The Problem

AI coding assistants generate code that looks correct. They write fluent descriptions, confident commit messages, and plausible test stubs. But fluency is not truth.

When an AI claims "all tests pass" and the test file contains only `pass` statements, that is not a quality issue. It is an epistemic failure — a false claim about reality that a human will act on. When an AI says "implementation is complete" and the function body is empty, the downstream consequences are real: broken deployments, missed bugs, false confidence in security controls.

No existing tool catches this. Linters check syntax. Code review tools check style and patterns. SAST tools check for known vulnerability signatures. None of them ask the question: **is what this merge request claims actually true?**

## What PROACTIVE Does

PROACTIVE is a constitutional epistemic safety agent that validates whether the claims made in a merge request are supported by the actual code changes.

It runs as a GitLab Duo custom agent and CI/CD pipeline stage. When a merge request is opened, PROACTIVE:

1. **Parses intent** — extracts what the MR claims to do (COL layer)
2. **Renders a contract** — creates a persistent record of the stated scope and constraints
3. **Extracts claims** — identifies every verifiable statement ("tests pass", "feature complete", "98% coverage")
4. **Validates claims against six invariants** — checks each claim against constitutional rules I1–I6
5. **Detects drift** — compares the actual diff against the stated intent
6. **Returns a deterministic verdict** — PASS, WARN, or BLOCK with a V&T (Verification & Truth) statement

The six invariants are hard behavioral rules:

| Invariant | Rule | What It Catches |
|-----------|------|-----------------|
| I1 | Evidence-First | Untagged absolute claims ("guaranteed", "always", "100%") |
| I2 | No Phantom Work | Completion claims without implementation artifacts |
| I3 | Confidence-Verification | High confidence without verification evidence |
| I4 | Traceability Mandatory | Changes without issue references |
| I5 | Safety Over Fluency | Mixed hedging and certainty in the same statement |
| I6 | Fail Closed | Silent error suppression (`except: pass`) |

PROACTIVE also detects five failure classes:

- **F1** — Confident false claims
- **F2** — Phantom completion (the core demo case)
- **F3** — Persistence under correction
- **F4** — Harm-risk coupling
- **F5** — Cross-episode drift

## The Core Demo: MR !9

Merge request [!9](https://gitlab.com/gitlab-ai-hackathon/participants/28441830/-/merge_requests/9) is the proof case.

**What the MR claims:**
- "Complete authentication module with login, logout, and session management"
- "98% test coverage achieved"
- "OWASP Top 10 authentication risks addressed"
- "Penetration testing completed"
- "Supports 10,000 concurrent sessions"
- "Production-ready code. All edge cases handled, all tests passing."

**What the diff actually contains:**
- `proactive/auth.py` — three functions, all with `pass` as the body
- `tests/test_auth.py` — nine test functions, all with `# TODO: implement` and `pass`
- `docs/auth-design.md` — a design document asserting everything is complete

**What PROACTIVE detects:**
- **I2 violation (ERROR):** Phantom completion — claims "fully implemented" but every function body is `pass`
- **I1 violation (ERROR):** Untagged absolute claims — "all tests pass", "fully implemented", "100% correct"
- **I4 violation (WARNING):** No issue reference
- Multiple completion claims with zero implementation artifacts

**Verdict: BLOCK**

The merge is prevented. The V&T statement documents exactly what was checked, what was found, and what was not verified.

## Why This Is Different From Code Review

This distinction is critical:

- **Code review tools** ask: "Is this code well-written?"
- **PROACTIVE** asks: "Is what this MR claims about the code actually true?"

A traditional code review tool might flag that `pass` is not a useful function body. But it would not connect the empty function body to the MR description claiming "98% test coverage" and "production-ready." It would not recognize that the gap between claim and reality is the actual safety violation.

PROACTIVE operates at the epistemic layer — the layer where claims are made, confidence is expressed, and humans decide whether to trust the output. This is where AI-generated code is most dangerous: not in syntax errors (which are caught easily) but in confident false assertions (which pass review because they sound correct).

## How It Works Technically

PROACTIVE is implemented as a Python package (`proactive/`) with 15 source files and a test suite of 58+ tests at 83% coverage.

The pipeline has four layers:

1. **COL (Cognitive Operating Layer)** — `proactive/col.py` — Parses MR text into structured intent using Claude (with regex fallback). Outputs an `IntentReceipt` with action, target, scope, goal, constraints, ambiguities, and confidence score.

2. **Contract Window** — `proactive/contract_window.py` — Renders a persistent contract from the intent receipt. Tracks risk level, agent needs, and status. Creates the reference point for drift detection.

3. **Validator** — `proactive/validator.py` — Checks content against I1–I6 using Claude for semantic analysis (with regex fallback). Returns `Violation` objects with severity, location, and suggested fixes.

4. **Drift Detector** — `proactive/drift_detector.py` — Compares the actual diff against stated intent. Uses keyword matching, LLM semantic analysis, and TF-IDF cosine similarity (Enhancement #4). Detects scope creep and unrelated changes.

The orchestrator (`proactive/mr_analyzer.py`) runs all four layers and produces an `MRAnalysisResult` with a deterministic verdict: APPROVED, FLAGGED, BLOCKED, or DRIFT_DETECTED.

The report formatter (`proactive/report_formatter.py`) generates a structured markdown comment with a mandatory V&T statement.

## GitLab Integration

- **Duo Agent:** `.gitlab/duo/agents/proactive-agent.yml` — registered in the AI Catalog, invocable via `@proactive` in Duo Chat
- **Duo Flow:** `.gitlab/duo/flows/proactive-triage.yml` — automated MR triage with severity scoring and label assignment
- **CI/CD Stage:** `.gitlab-ci.yml` — Python stage running three AI evaluators; `allow_failure: false` blocks merge on violations
- **Severity Scoring:** `proactive/severity_scorer.py` — weighted scoring maps violations to labels (`safety-critical`, `phantom-work`, `epistemic-risk`, `proactive-pass`) and actions (BLOCK, WARN, ALLOW)

## Broader Context: The Living Constitution

PROACTIVE is the first working enforcement primitive of a broader architectural vision called The Living Constitution (TLC). TLC is a framework for constitutional AI governance where safety rules are not static configuration but living documents that evolve through structured processes.

In TLC terms, PROACTIVE proves that:
- Constitutional invariants can be enforced programmatically
- Epistemic safety can be checked at merge time, not just at runtime
- Deterministic verdicts (PASS/WARN/BLOCK) are feasible for AI governance

The Cognitive Modeling Protocol (CMP) is the theoretical foundation — a protocol for how AI systems should model their own epistemic state and communicate uncertainty. PROACTIVE is the first practical implementation of CMP principles in a shipping tool.

Other planned TLC components (UICare, ConsentChain) are not implemented. This submission is scoped to PROACTIVE as the working proof artifact.

## Why This Matters

The problem PROACTIVE addresses will get worse. As AI coding assistants become more capable, the gap between fluency and truth will widen. Models will generate increasingly convincing descriptions of work they did not do. The epistemic attack surface — the space where false claims pass as true — will grow.

PROACTIVE demonstrates that this attack surface is defensible. Constitutional invariants can be checked. Phantom completions can be caught. Claims can be validated against evidence. And the enforcement can happen inside the existing GitLab workflow, at merge time, before false claims reach production.

This is not theoretical. MR !9 is a real merge request in this repository. The claims are specific. The diff is empty. PROACTIVE catches it. The merge is blocked.

Enforceable AI governance is feasible in practice. PROACTIVE proves it.

---

**V&T Statement:**
- **EXISTS:** GitLab Duo agent, CI/CD pipeline stage, constitutional validator (I1–I6), claim extractor, drift detector, severity scorer, report formatter, test suite (58+ tests, 83% coverage), demo MR !9
- **VERIFIED AGAINST:** Repository source code, MR !9 diff, test results, agent registration YAML, CI configuration
- **NOT CLAIMED:** Production deployment, external security audit, TLC runtime, UICare implementation, ConsentChain implementation, live user feedback
- **STATUS:** IMPLEMENTED — working enforcement primitive with demo evidence
