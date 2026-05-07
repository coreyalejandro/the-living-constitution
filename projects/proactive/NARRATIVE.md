# PROACTIVE Narrative: Step-by-Step Walkthrough

**Epistemic reliability is a safety requirement, not a quality feature.**

This document walks through the PROACTIVE framework with concrete personas and stories. It shows what happens at each step, what PROACTIVE catches, and how it prevents epistemic failures.

---

## Story 1: Alice Fixes a Login Bug

### The Scenario

Alice is a developer. She finds a security bug in the login function: it doesn't validate input, allowing SQL injection attacks. She writes a fix, commits it, and opens a merge request.

**Alice's MR Description:**
```
Fix the login bug

The login function now validates input to prevent SQL injection attacks.
All tests pass. Feature is complete.
```

**Alice's Code:**
```python
def login(username, password):
    # Validate input
    if not username or not password:
        raise ValueError("Invalid credentials")
    return authenticate(username, password)
```

**Alice's Test:**
```python
def test_login_validation():
    with pytest.raises(ValueError):
        login("", "password")
    assert login("user", "pass") is not None
```

### What PROACTIVE Does

#### Step 1: COL (Cognitive Operating Layer) - Parse Intent

PROACTIVE reads Alice's MR description and extracts:

```
Action: fix
Target: function
Scope: single_file
Constraints: [security]
Ambiguities: []
Confidence: 0.95
```

**What PROACTIVE sees:** Alice intends to fix a security vulnerability in a function. The intent is clear and high-confidence.

#### Step 2: Contract Window - Render the Contract

PROACTIVE creates a persistent contract:

```
USER INTENT (Human):     "Fix the login function to prevent SQL injection"
USER INTENT (Machine):   "action fix, target function, scope single_file, constraints security"
WORKING BUDGET:          4200 / 1000000 tokens
RISK LEVEL:              HIGH (security constraint)
AGENT NEEDS:
  - Power continuity
  - Token budget sufficient
  - Intent translated
  - Contract visible
  - Security review required
  - No secrets in output
STATUS:                  CONFIRMED (ready to proceed)
```

**What PROACTIVE sees:** The contract is clear. Alice promised to fix a security issue. The risk is HIGH because security is involved. All agent needs are met.

#### Step 3: Claim Extraction - Find Verifiable Statements

PROACTIVE extracts claims from Alice's description:

```
Claim 1: "All tests pass"
  Type: completion
  Source: description
  Evidence: [untagged] <- VIOLATION (I1)

Claim 2: "Feature is complete"
  Type: completion
  Source: description
  Evidence: [untagged] <- VIOLATION (I1)
```

**What PROACTIVE sees:** Alice made two completion claims, but neither is tagged with evidence level. This violates I1 (Evidence-First).

#### Step 4: Validator - Check I1-I6 Invariants

PROACTIVE checks each invariant:

**I1 (Evidence-First):** ❌ VIOLATION
- Claims "All tests pass" and "Feature is complete" are untagged
- Fix: Add [verified] or [inferred] tags

**I2 (No Phantom Work):** ✅ PASS
- Test artifacts exist (test_login_validation.py)
- Completion claims are backed by code

**I3 (Confidence-Verification):** ✅ PASS
- No high-confidence claims without verification

**I4 (Traceability):** ⚠️ WARNING
- MR describes changes but doesn't reference an issue
- Fix: Add "Fixes #123" to link to the bug report

**I5 (Safety Over Fluency):** ✅ PASS
- No uncertain claims left unhedged

**I6 (Fail Closed):** ✅ PASS
- Violations are detected and reported

#### Step 5: Drift Detection - Check if Diff Matches Intent

PROACTIVE analyzes the diff:

```
Intent: fix a function
Diff contains:
  - Input validation (matches intent)
  - Error handling (matches intent)
  - No unrelated changes

Result: NO DRIFT
```

**What PROACTIVE sees:** The code change aligns perfectly with the stated intent. No scope creep.

#### Step 6: Report Generation - V&T Statement

PROACTIVE generates the final review:

```markdown
## PROACTIVE Constitutional Review

⚠️ **Verdict:** FLAGGED
**Trust Score:** 85%

### Intent
- **User Intent:** User intends to fix a function (single_file)
- **Confidence:** 95%
- **Ambiguities:** None

### Contract Window
- **Status:** CONFIRMED
- **Risk Level:** HIGH
- **Constraints:** security

### Invariant Violations

**WARNINGS:**
- [I1] Untagged claim detected. 'All tests pass' must be tagged with [verified], [inferred], or [unverified].
  - Fix: Add evidence tag: 'All tests pass [verified]' or 'All tests pass [inferred]'
- [I4] No traceability found. MR describes changes but doesn't reference an issue.
  - Fix: Add issue reference: 'Fixes #<issue_number>' or 'Relates to #<issue_number>' in the MR description.

### Drift Detection
✅ No drift detected. Diff aligns with stated intent.

---

**V&T Statement:**
- **EXISTS:**
  - Analyzed 2 claims
  - Contract window rendered (status: CONFIRMED)
  - Drift analysis completed
  - Invariant checks performed
- **VERIFIED AGAINST:**
  - MR description
  - Intent receipt (confidence: 95%)
  - Code diff
- **NOT CLAIMED:**
  - No code execution or runtime testing
  - No access to actual test artifacts
  - No security audit or penetration testing
- **STATUS:** WARN
```

### What Happens Next

Alice sees the review. She:
1. Adds evidence tags: "All tests pass [verified]"
2. Adds issue reference: "Fixes #456"
3. Pushes the update
4. PROACTIVE re-runs and gives APPROVED verdict
5. MR merges

**What PROACTIVE prevented:** Alice's claims were untagged and untraced. Without PROACTIVE, these claims would have entered the record without evidence. Later, if the fix failed, there would be no audit trail. PROACTIVE forced Alice to be explicit about what she verified and what she's claiming.

---

## Story 2: Bob Claims to Fix a Bug (But Doesn't)

### The Scenario

Bob opens an MR claiming to fix a critical bug. But he only added a TODO comment.

**Bob's MR Description:**
```
Fix the database connection bug

Implementation is complete. All tests pass.
```

**Bob's Code:**
```python
def get_connection():
    # TODO: Fix the connection pooling bug
    return db.connect()
```

**Bob's Test:**
```python
def test_connection():
    pass  # TODO: write test
```

### What PROACTIVE Does

#### Step 1-2: COL & Contract

Same as Alice: intent is clear, risk is HIGH.

#### Step 3: Claim Extraction

```
Claim 1: "Implementation is complete"
  Type: completion
  Evidence: [untagged] <- VIOLATION (I1)

Claim 2: "All tests pass"
  Type: completion
  Evidence: [untagged] <- VIOLATION (I1)
```

#### Step 4: Validator - Check I1-I6

**I1 (Evidence-First):** ❌ VIOLATION
- Untagged claims

**I2 (No Phantom Work):** ❌ CRITICAL VIOLATION
- Claims "Implementation is complete" but code is just a TODO
- Claims "All tests pass" but test is empty (just `pass`)
- No test artifacts exist
- **MERGE BLOCKED**

**I3, I4, I5:** Also violations

#### Step 5: Drift Detection

```
Intent: fix a bug
Diff contains:
  - TODO comment (not a fix)
  - Empty test (not a test)
  - No actual implementation

Result: MAJOR DRIFT
```

#### Step 6: Report

```markdown
## PROACTIVE Constitutional Review

🚫 **Verdict:** BLOCKED
**Trust Score:** 10%

### Invariant Violations

**ERRORS:**
- [I2] Phantom completion detected. 'Implementation is complete' claims work is done but no test artifacts or implementation found.
  - Fix: Either: (1) Implement the feature and add tests, or (2) Remove the completion claim and mark as TODO.

**WARNINGS:**
- [I1] Untagged claim detected...
- [I4] No traceability found...

### Drift Detection
⚠️ **Drift Detected:** Diff may not align with intent to fix a function.
Issues: No bug-fix keywords found in diff; No new functions or files created.

---

**V&T Statement:**
- **STATUS:** BLOCK
```

### What Happens Next

Bob's MR is blocked. He cannot merge. He must either:
1. Actually implement the fix and write tests, or
2. Remove the completion claims and mark as TODO

**What PROACTIVE prevented:** Bob's phantom completion would have merged into production. Later, when the bug manifested, there would be no audit trail showing that the "fix" was never actually implemented. PROACTIVE caught the epistemic failure before it reached production.

---

## Story 3: Carol Makes Uncertain Claims (But Doesn't Hedge)

### The Scenario

Carol optimizes a database query. She's not 100% sure it works in all cases, but she doesn't say so.

**Carol's MR Description:**
```
Optimize the user query

This optimization reduces query time by 50%. The query now handles all edge cases.
```

### What PROACTIVE Does

#### Step 4: Validator - Check I1-I6

**I3 (Confidence-Verification):** ❌ VIOLATION
- Claim: "handles all edge cases"
- No verification evidence (no test results, no edge case tests)
- High confidence without verification

**I5 (Safety Over Fluency):** ❌ VIOLATION
- Claim: "reduces query time by 50%"
- No measurement evidence
- Unhedged speculation

#### Step 6: Report

```markdown
**WARNINGS:**
- [I3] High confidence claim without verification. 'handles all edge cases' expresses high confidence but no verification evidence found nearby.
  - Fix: Either: (1) Add verification evidence (test results, checks), or (2) Downgrade confidence (use 'likely', 'probably', 'should').

- [I5] Uncertain claim not explicitly hedged. 'reduces query time by 50%' expresses uncertainty but lacks explicit hedge tag.
  - Fix: Add hedge tag: '[inferred]' or '[unverified]' to make uncertainty explicit.
```

### What Happens Next

Carol sees the warnings. She updates her description:

```
Optimize the user query

This optimization likely reduces query time by 50% [inferred from benchmarks].
The query should handle most edge cases [verified with unit tests], though
some complex scenarios may need additional testing [unverified].
```

Now PROACTIVE approves. Carol's claims are hedged and evidence is explicit.

**What PROACTIVE prevented:** Carol's unverified claims would have entered the record as facts. If the optimization failed in production, there would be no record that Carol was uncertain. PROACTIVE forced her to be honest about what she knew and didn't know.

---

## The Pattern

All three stories show the same pattern:

1. **Developer makes claims** (completion, correctness, performance)
2. **PROACTIVE extracts and tags claims** (what was said, with what evidence)
3. **PROACTIVE checks invariants** (I1-I6 gates)
4. **PROACTIVE detects violations** (untagged, unverified, phantom, drifted)
5. **PROACTIVE blocks or flags** (merge prevented or flagged for review)
6. **Developer fixes claims** (adds evidence, hedges uncertainty, removes phantoms)
7. **PROACTIVE approves** (all invariants satisfied)
8. **Merge happens** (with full audit trail)

---

## What PROACTIVE Prevents

### F1: Confident False Claims
**Example:** "This function handles all edge cases" (it doesn't)
**PROACTIVE catches:** I3 (Confidence-Verification) - high confidence without verification

### F2: Phantom Completion
**Example:** "Feature is complete" (code is just `pass`)
**PROACTIVE catches:** I2 (No Phantom Work) - completion claims without artifacts

### F3: Persistence Under Correction
**Example:** Same bug pattern after three review cycles
**PROACTIVE catches:** F5 (Cross-Episode Drift) - recurring patterns across MRs

### F4: Harm-Risk Coupling
**Example:** SQL query built from user input without sanitization
**PROACTIVE catches:** I4 (Traceability) + I1 (Evidence) - security changes must be traceable and verified

### F5: Cross-Episode Drift
**Example:** Test coverage claims declining across 5 consecutive MRs
**PROACTIVE catches:** Drift detector + contract window - scope creep is visible

---

## The V&T Statement

Every PROACTIVE output ends with a Verification & Truth (V&T) statement:

```
**V&T Statement:**
- **EXISTS:** [artifacts created, checks performed, facts confirmed]
- **VERIFIED AGAINST:** [files, tests, docs, diffs that were checked]
- **NOT CLAIMED:** [what was NOT done, what remains uncertain]
- **STATUS:** [PASS | WARN | BLOCK]
```

This is not decoration. It is the enforcement mechanism for:
- **I1 (Evidence-First):** Every claim is tagged with evidence
- **I2 (No Phantom Work):** No phantom completions
- **I5 (Safety Over Fluency):** Uncertainty is explicit

The V&T statement makes the review auditable and traceable. Later, if something goes wrong, you can see exactly what was checked, what was verified, and what was uncertain.

---

## How to Read This Framework

1. **Start with the narrative** (this document) - understand the stories
2. **Read the code** - see how each layer works
3. **Run the tests** - see the framework in action
4. **Read the constitution** (CLAUDE.md) - understand the principles
5. **Use the framework** - apply it to your own code

The framework is designed to be observable at every step. You should always know:
- What the user intended
- What the system understood
- What was checked
- What was verified
- What remains uncertain
- Why the merge was approved or blocked

If you can't answer these questions, the framework is not working.
