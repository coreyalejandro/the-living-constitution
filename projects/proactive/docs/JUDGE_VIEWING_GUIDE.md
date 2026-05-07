# JUDGE VIEWING GUIDE — PROACTIVE

**Project:** PROACTIVE — Constitutional Epistemic Safety Agent for GitLab Duo  
**Repo:** https://gitlab.com/gitlab-ai-hackathon/participants/28441830  
**Demo MR:** https://gitlab.com/gitlab-ai-hackathon/participants/28441830/-/merge_requests/9  
**Video length:** ~80 seconds

---

## What to Watch For

### 0:00–0:12 — The Problem
A merge request claims complete implementation with 98% test coverage. Watch for the contrast: confident claims vs. empty reality. This is the core problem PROACTIVE solves.

### 0:12–0:28 — The Claims
Five specific, verifiable claims scroll past. Each one is false. Note how convincing they sound — this is what makes AI-generated phantom completions dangerous.

### 0:28–0:42 — The Evidence
The actual code is shown. The `login()` function body is `pass`. Every test is `# TODO: implement`. This is the gap between claim and reality that no existing tool catches.

### 0:42–0:55 — The Detection
PROACTIVE's output appears. Look for:
- **I2 VIOLATION:** Phantom completion detected (the core invariant)
- **I1 VIOLATION:** Untagged absolute claims
- **Verdict: BLOCKED** — the merge is prevented
- **V&T Statement** — documents exactly what was checked

### 0:55–1:10 — The Differentiation
Two-column comparison. The key insight: code review tools check code quality. PROACTIVE checks whether claims about the code are true. This is a different layer of safety.

### 1:10–1:20 — Close
Project framing. PROACTIVE is a constitutional enforcement engine, not a code review tool.

---

## What Makes This Submission Different

1. **Novel problem space.** No existing tool validates whether MR claims match the actual diff. PROACTIVE is the first.

2. **Working demo with real artifact.** MR !9 is a real merge request in the repo. The claims are specific. The diff is empty. PROACTIVE catches it.

3. **Deterministic enforcement.** Six invariants (I1–I6) produce repeatable verdicts. Not probabilistic suggestions — hard BLOCK/WARN/PASS decisions.

4. **GitLab-native integration.** Runs as a Duo custom agent (`@proactive`), a Duo Flow (automated triage), and a CI/CD pipeline stage.

5. **Constitutional framework.** Nine principles, six invariants, five failure classes. The system has a formal governance structure, not ad-hoc rules.

---

## How to Verify Independently

### Option 1: Look at MR !9 directly
Open https://gitlab.com/gitlab-ai-hackathon/participants/28441830/-/merge_requests/9
- Read the description (confident claims)
- Click "Changes" tab (empty implementations)
- The gap is self-evident

### Option 2: Run the test suite
```bash
git clone https://gitlab.com/gitlab-ai-hackathon/participants/28441830.git
cd 28441830
pip install -e ".[dev]"
pytest tests/ -v --cov=proactive
```
58+ tests, 83% coverage. The phantom completion detection test exercises the exact MR !9 scenario.

### Option 3: Run PROACTIVE locally
```bash
python -m proactive.web_ui
# Open http://localhost:5000
# Paste MR content and run analysis
```

### Option 4: Invoke the Duo Agent
In GitLab Duo Chat on the project:
```
@proactive review MR !9 for epistemic safety
```

---

## Key Files to Inspect

| File | What It Shows |
|------|---------------|
| `proactive/validator.py` | I1–I6 invariant checks |
| `proactive/mr_analyzer.py` | Full MR analysis orchestrator |
| `proactive/col.py` | Intent parsing (COL layer) |
| `proactive/drift_detector.py` | Intent vs. diff comparison |
| `proactive/report_formatter.py` | V&T statement generation |
| `proactive/constitution.json` | Constitutional rules definition |
| `tests/test_mr_analyzer.py` | Phantom completion test case |
| `.gitlab/duo/agents/proactive-agent.yml` | Duo agent registration |
| `.gitlab/duo/flows/proactive-triage.yml` | Automated triage flow |

---

## One-Line Summary

PROACTIVE blocks merge requests that claim work is complete when the code proves otherwise — catching the epistemic failures that no linter, SAST tool, or code reviewer detects.
