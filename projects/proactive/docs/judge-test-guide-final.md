# PROACTIVE — Judge Testing Guide

**Goal:** Make it trivial for judges to verify that PROACTIVE works.

Four methods are provided, from easiest to most thorough.

---

## Method 1: Review MR !9 (2 minutes, no setup)

This is the fastest way to see what PROACTIVE catches.

1. Open [MR !9](https://gitlab.com/gitlab-ai-hackathon/participants/28441830/-/merge_requests/9).
2. Read the description. Note the claims:
   - "fully implemented and production-ready"
   - "98% test coverage achieved"
   - "OWASP Top 10 authentication risks addressed"
   - "Penetration testing completed"
3. Click the **Changes** tab.
4. Open `proactive/auth.py`. Every function body is `pass`.
5. Open `tests/test_auth.py`. Every test body is `# TODO: implement` followed by `pass`.
6. Open `docs/auth-design.md`. It says "Status: Complete."

**What this proves:** The MR makes strong claims. The code is empty. This is the exact failure class (F2: Phantom Completion) that PROACTIVE detects and blocks.

---

## Method 2: Duo Chat (3 minutes, requires Duo access)

1. Open the project: https://gitlab.com/gitlab-ai-hackathon/participants/28441830
2. Open GitLab Duo Chat.
3. Type: `@proactive review MR !9 for epistemic safety`
4. Read the response. It should identify:
   - I2 violations (phantom completion)
   - I1 violations (untagged absolute claims)
   - A BLOCK or WARN verdict
   - A V&T statement at the end

**What this proves:** The Duo agent is registered, responds to queries, and applies constitutional invariants to real MR content.

---

## Method 3: Run Tests Locally (5 minutes)

```bash
git clone https://gitlab.com/gitlab-ai-hackathon/participants/28441830.git
cd 28441830
pip install -e ".[dev]"
pytest tests/ -v --cov=proactive
```

Expected output:
- 58+ tests pass
- 83%+ coverage
- Key tests to look for:
  - `test_mr_analyzer.py` — exercises the full pipeline (COL → Contract → Validator → Drift)
  - `test_validator.py` — tests I1–I6 invariant detection
  - `test_drift_detector.py` — tests scope drift detection
  - `test_constitution.py` — tests constitutional rule enforcement
  - `test_severity_scorer.py` — tests BLOCK/WARN/ALLOW verdict logic

To run only the constitutional invariant tests:

```bash
pytest tests/test_validator.py tests/test_constitution.py -v
```

**What this proves:** The validation logic is implemented, tested, and deterministic. Invariant checks produce correct verdicts on known inputs.

---

## Method 4: Read the Documentation (5 minutes)

For judges who want to understand the architecture without running code:

1. **Start here:** [README.md](https://gitlab.com/gitlab-ai-hackathon/participants/28441830/-/blob/main/README.md) — system overview, invariants, status matrix
2. **Narrative walkthrough:** [NARRATIVE.md](https://gitlab.com/gitlab-ai-hackathon/participants/28441830/-/blob/main/NARRATIVE.md) — three concrete stories showing PROACTIVE in action
3. **Agent constitution:** [AGENTS.md](https://gitlab.com/gitlab-ai-hackathon/participants/28441830/-/blob/main/AGENTS.md) — repository structure, agent configuration, key concepts
4. **Boundaries:** [docs/fact-check-boundaries.md](https://gitlab.com/gitlab-ai-hackathon/participants/28441830/-/blob/main/docs/fact-check-boundaries.md) — what exists, what does not, what is unverified
5. **Core validator code:** [proactive/validator.py](https://gitlab.com/gitlab-ai-hackathon/participants/28441830/-/blob/main/proactive/validator.py) — I1–I6 enforcement logic
6. **MR analyzer:** [proactive/mr_analyzer.py](https://gitlab.com/gitlab-ai-hackathon/participants/28441830/-/blob/main/proactive/mr_analyzer.py) — full pipeline orchestrator

**What this proves:** The system is documented, the architecture is coherent, and the claims in the submission are traceable to source code.

---

## Quick Reference

| What to verify | Where to look |
|----------------|---------------|
| Phantom completion demo | [MR !9](https://gitlab.com/gitlab-ai-hackathon/participants/28441830/-/merge_requests/9) |
| Duo agent registration | `.gitlab/duo/agents/proactive-agent.yml` |
| I1–I6 invariant logic | `proactive/validator.py` |
| Full pipeline | `proactive/mr_analyzer.py` |
| Severity scoring | `proactive/severity_scorer.py` |
| Test suite | `tests/` (12 files, 58+ tests) |
| CI configuration | `.gitlab-ci.yml` |
| Claim boundaries | `docs/fact-check-boundaries.md` |
