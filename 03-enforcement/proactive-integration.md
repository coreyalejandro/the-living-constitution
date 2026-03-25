# PROACTIVE Integration
## How PROACTIVE Enforces TLC Invariants in CI/CD Pipelines

---

## What PROACTIVE Is

PROACTIVE is the epistemic enforcement engine of the Commonwealth. It is a Python-based agent that integrates with GitLab CI to detect constitutional violations in code, commits, and pipeline outputs. It is the first subsystem to achieve operational Tier 2 (machine-checkable) enforcement.

**Repository:** `/Users/coreyalejandro/Projects/proactive-gitlab-agent`
**Technology:** Python, GitLab CI integration
**Safety domain:** Epistemic Safety (primary), Empirical Safety (secondary)
**Validated performance:** 100% detection rate, 0% false positive rate, 8 test cases, n=19 violations (validated 2026-01-24)

---

## Which TLC Invariants PROACTIVE Enforces

### F1 — Confident False Claims (Primary Target)

PROACTIVE scans for assertions in code, documentation, and pipeline outputs that claim something exists or works when evidence is absent. Detection mechanisms:

- **Truth-status inflation detection:** Scans module status declarations and cross-references against actual test results, build outputs, and file existence. If a module is declared "implemented" but has no passing tests, PROACTIVE flags the discrepancy.
- **Documentation-code divergence:** Compares documentation claims (README, API docs, status pages) against codebase reality. If documentation references an endpoint that does not exist in the route configuration, PROACTIVE flags it.
- **V&T claim verification:** Parses V&T Statements in commit messages and PR descriptions. Cross-references "Exists" claims against file system state and build results.

### F2 — Phantom Completion (Secondary Target)

PROACTIVE monitors pipeline completion signals for phantom completions:

- **Silent failure detection:** Checks whether pipeline steps that report success actually produced the expected artifacts. A deployment step that exits 0 but produces no deployment artifact is flagged.
- **Test result verification:** Ensures that "tests pass" claims correspond to actual test execution. A CI step that skips tests but reports success is flagged.
- **Build artifact validation:** Verifies that build steps produce non-empty, non-trivial output files.

### F5 — Cross-Episode Recurrence (Tertiary Target)

PROACTIVE maintains a violation history. When a violation is detected, it is logged with a pattern signature. If the same pattern recurs in a subsequent pipeline run, PROACTIVE flags it as a recurrence and escalates severity.

---

## How PROACTIVE Integrates with GitLab CI

```
Developer pushes code
        │
        ▼
GitLab CI pipeline triggers
        │
        ├── Stage 1: Build
        │       │
        │       ▼
        │   PROACTIVE: Verify build produces artifacts
        │
        ├── Stage 2: Test
        │       │
        │       ▼
        │   PROACTIVE: Verify tests actually execute
        │   PROACTIVE: Cross-reference results with claims
        │
        ├── Stage 3: Lint / Static Analysis
        │       │
        │       ▼
        │   PROACTIVE: Check for truth-status inflation
        │   PROACTIVE: Check for documentation divergence
        │
        ├── Stage 4: PROACTIVE Epistemic Scan
        │       │
        │       ▼
        │   Full constitutional compliance check:
        │   - V&T claim verification
        │   - Cross-reference with violation history
        │   - Invariant I1 enforcement
        │
        └── Stage 5: Deploy (if all stages pass)
                │
                ▼
            PROACTIVE: Post-deploy health check verification
```

**Pipeline behavior on violation:**
- PROACTIVE violations block the pipeline. The pipeline does not proceed to the next stage.
- The violation report includes: which invariant was violated, which file or claim triggered it, what the expected state is, and what the actual state is.
- The developer must fix the violation and re-push. PROACTIVE re-scans on the new push.

---

## PROACTIVE's Relationship to SentinelOS

PROACTIVE and SentinelOS are complementary enforcement layers:

| Aspect | PROACTIVE | SentinelOS |
|--------|-----------|------------|
| Runtime | CI/CD pipeline (batch) | Agent runtime (continuous) |
| Language | Python | TypeScript |
| Enforcement timing | On push/merge request | On every agent turn |
| Scope | Repository-level checks | Cross-repository governance |
| Invariants | I1, I2, I5 (CI-observable) | I1-I6 (full set) |
| Maturity | Tier 2 (operational, validated) | Tier 1 (defined, not yet wired) |

**Integration path:** When SentinelOS reaches Tier 2, PROACTIVE's detection patterns will be encoded as SentinelOS adapters. PROACTIVE will become one of several enforcement adapters in the SentinelOS hexagonal architecture — the GitLab CI adapter. The detection logic transfers; the platform binding changes.

---

## PROACTIVE Validation Evidence

The following validation results establish PROACTIVE's enforcement credibility:

| Metric | Value | Evidence Location |
|--------|-------|-------------------|
| Detection rate | 100% (19/19 violations detected) | `validation_results.json` in proactive-gitlab-agent repo |
| False positive rate | 0% (0 false positives across 8 test cases) | `validation_results.json` |
| Test cases | 8 distinct violation patterns tested | `tests/` directory |
| Validation date | 2026-01-24 | Git log timestamp |

These results are Tier 2 evidence: machine-generated, reproducible via `pytest -v`, and verifiable by re-running the test suite.

---

## Constitutional Authority

PROACTIVE operates under the following constitutional provisions:

- **Article I, Right to Truth:** PROACTIVE enforces the right by detecting false claims before they reach production.
- **Article II, Truth-Status Discipline:** PROACTIVE validates that module status declarations match actual build and test results.
- **Article III, Verification Before Done:** PROACTIVE prevents phantom completions by requiring verification artifacts for every pipeline stage.
- **Article IV, Separation of Powers:** PROACTIVE cannot override other agents or modify its own detection rules without human approval. It can only detect and report.

---

## V&T Statement
- **Exists:** PROACTIVE integration document describing invariant enforcement (F1, F2, F5), GitLab CI pipeline integration flow, relationship to SentinelOS, validation evidence with specific metrics, constitutional authority mapping
- **Non-existent:** PROACTIVE adapter encoded in SentinelOS hexagonal architecture; PROACTIVE enforcement of invariants I3, I4, I6 (outside CI-observable scope); automated PROACTIVE-to-SentinelOS migration path
- **Unverified:** Whether PROACTIVE validation results at 100%/0% still hold for code changes since 2026-01-24; whether the GitLab CI pipeline stages described match the current `.gitlab-ci.yml` configuration exactly
- **Functional status:** PROACTIVE is the most mature enforcement subsystem in the Commonwealth — operational at Tier 2 with validated detection performance
