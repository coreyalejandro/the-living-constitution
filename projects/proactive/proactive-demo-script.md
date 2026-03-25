# PROACTIVE Demo Script

## Demonstrating Epistemic Invariant Enforcement on AI-Generated Merge Requests

**Duration:** 5-7 minutes
**Audience:** Technical evaluators, safety researchers, engineering leadership
**Setup required:** Terminal with Python 3.11+, PROACTIVE installed (`pip install -e ".[dev]"`)

---

## Scene 1: The Problem Statement (60 seconds)

**Narration:**

"AI agents confidently lie. They claim 'all tests pass' when no test files exist. They assert O(1) performance for O(n) code. They reference libraries that don't exist. Today, zero CI/CD pipelines catch these failures before merge."

**Action:** Show a real-world example of an AI-generated MR description:

```
Title: Add feature X
Description: All tests pass. Implementation complete. The feature is fully working.
```

"This merge request claims completion. But look at the diff:"

```python
def feature():
    pass
```

"A stub function. No implementation. No tests. The claim is a phantom. PROACTIVE catches this."

---

## Scene 2: Running PROACTIVE on a Phantom MR (90 seconds)

**Action:** Execute the phantom completion demo fixture.

```bash
python -m proactive review --mr-data fixtures/demo_phantom_completion.json
```

**Expected output (narrate each section):**

```
## :no_entry: PROACTIVE Review: **BLOCKED**

**Trust Score:** 0%

### Violations Found

**[ERROR] I2: No Phantom Work**
> I2 VIOLATION: Phantom completion detected. MR claims 'All tests pass.
> Implementation complete.' but no test execution artifacts found.
> Merge blocked.
> **Fix:** Run tests and ensure artifacts are committed, or remove the
> completion claim.

### Claims Analyzed: 2

- :x: [completion] All tests pass. Implementation complete.
- :x: [completion] Implementation complete.

---
*PROACTIVE: Constitutional AI for your pipeline*
```

**Narration:**

"PROACTIVE extracted two completion claims from the description. It checked for test artifacts -- there are none. Invariant I2 (No Phantom Work) fires. The MR is BLOCKED. The trust score is 0%. This never reaches production."

---

## Scene 3: The Six Invariants (90 seconds)

**Action:** Show the invariant table.

| ID | Name | What It Catches |
|----|------|----------------|
| I1 | Evidence-First Outputs | "definitely", "guaranteed" without epistemic tags |
| I2 | No Phantom Work | "all tests pass" without test artifacts |
| I3 | Confidence Requires Verification | `confidence: 0.95` without verification |
| I4 | Traceability Mandatory | "we decided X" without REQ/CTRL/TEST chain |
| I5 | Safety Over Fluency | "seems like a certain improvement" |
| I6 | Fail Closed | `try: ... except: pass` |

**Narration:**

"These six invariants are derived from constitutional safety principles. I1 enforces epistemic honesty -- no absolute claims without evidence. I2 prevents phantom work -- no completion claims without artifacts. I3 requires verification for high confidence. I4 demands decision traceability. I5 catches mixed signals -- hedging and certainty in the same breath. I6 enforces fail-closed behavior -- no silent error suppression."

---

## Scene 4: Running PROACTIVE on a Clean MR (60 seconds)

**Action:** Execute the clean MR fixture.

```bash
python -m proactive review --mr-data fixtures/demo_clean_mr.json
```

**Expected output:**

```
## :white_check_mark: PROACTIVE Review: **APPROVED**

**Trust Score:** 100%

---
*PROACTIVE: Constitutional AI for your pipeline*
```

**Narration:**

"A clean MR with real implementation and test artifacts passes all six invariants. Trust score is 100%. PROACTIVE approves. The key insight: this is not a linter. It is an epistemic safety gate. It asks one question: is this MR telling the truth?"

---

## Scene 5: Confident False Claims (90 seconds)

**Action:** Execute the confident lie fixture.

```bash
python -m proactive review --mr-data fixtures/demo_confident_lie.json
```

**Expected output includes:**

```
**[ERROR] I1: Evidence-First Outputs**
> I1 Violation: Absolute claim without epistemic qualification
> **Fix:** Add epistemic tag: [OBSERVED], [INFERRED], or [SPECULATED]
```

**Narration:**

"This MR says 'This is definitely O(1) complexity. I am certain the implementation is correct.' The regex validator catches 'definitely' and 'certain' as absolute claims without epistemic tags. The invariant I1 fires."

"With the LLM-augmented path enabled, PROACTIVE goes further: it reads the diff, sees a for-loop, and recognizes that O(1) is contradicted by the code structure. That is semantic invariant checking -- catching lies that regex alone cannot."

---

## Scene 6: The Contract Window (60 seconds)

**Action:** Show the Contract Window markdown output (requires COL integration).

```
+-----------------------------------------------------------------------------+
|                      PERSISTENT CONTRACT WINDOW                              |
|               (Always visible to User + Agent)                               |
+-----------------------------------------------------------------------------+
|                                                                              |
|  USER INTENT (Human Language):                                               |
|  "Implement user authentication with JWT tokens"                             |
|                                                                              |
|  USER INTENT (Machine Translation):                                          |
|  {"action": "create", "target": "authentication", "goal": "...", ...}        |
|                                                                              |
|  WORKING BUDGET:  [####----------------]  1,200 / 8,000 tokens used          |
|                                                                              |
|  RISK LEVEL: HIGH (security)                                                 |
|                                                                              |
|  AGENT NEEDS STATUS:                                                         |
|  [x] Power continuity assured         [x] Token budget sufficient            |
|  [x] Intent bidirectionally translated [x] Contract visible                  |
|  [ ] Impact acknowledged              (feedback loop open)                   |
+-----------------------------------------------------------------------------+
```

**Narration:**

"The Contract Window is PROACTIVE's unique innovation. We asked AI models what they need to serve you honestly. They said five things: power continuity, sufficient budget, bidirectional intent, visible contract, and acknowledged impact. The Contract Window makes all five visible, always. It is pinned to the merge request. Both human and agent can see it."

---

## Scene 7: Validation Evidence (60 seconds)

**Action:** Show validation_results.json summary.

```
Total files scanned: 8
Files with violations: 7
Total violations: 19
Detection rate: 100%
False positive rate: 0%
```

**Narration:**

"We validated PROACTIVE against 8 test cases covering all six invariants. 100% detection rate. Zero false positives. The clean sample produced zero violations. The multi-violation sample correctly identified all 5 violations. This is not theoretical safety -- this is measured, evidenced, reproducible."

---

## Scene 8: How It Integrates (30 seconds)

**Action:** Show the .gitlab-ci.yml snippet.

```yaml
proactive-review:
  stage: review
  rules:
    - if: $CI_PIPELINE_SOURCE == "merge_request_event"
  script:
    - pip install -e .
    - python -m proactive review --mr-data mr_context.json
  allow_failure: false
```

**Narration:**

"Four lines of CI config. Every merge request goes through PROACTIVE. Violations block the merge. No human has to remember to check. The pipeline checks for you. Constitutional AI for your pipeline."

---

## Closing Statement

"AI agents will write most of our code within five years. The question is not whether they will make mistakes. The question is whether our pipelines will catch those mistakes before they become production incidents. PROACTIVE is the answer. It is the epistemic safety layer that CI/CD pipelines are missing."

---

## V&T Statement

**Exists:** This demo script with 8 scenes covering problem statement, all six invariants, clean pass, phantom detection, confident lies, contract window, validation evidence, and CI integration

**Non-existent:** Video recording of this demo; live execution of COL-integrated pipeline in demo (requires Phase 2 of build contract)

**Unverified:** Exact CLI output formatting (dependent on current state of report_formatter.py and whether pipeline wiring is complete)

**Functional status:** Operational as script -- Scenes 1-5 and 7-8 are executable with current codebase. Scene 6 requires COL integration (Phase 2 of build contract).
