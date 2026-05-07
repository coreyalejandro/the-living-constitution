# GitLab AI Hackathon Submission Checklist

Project:

PROACTIVE — Constitutional AI Safety Agent

Repository:

https://gitlab.com/gitlab-ai-hackathon/participants/28441830

---

## 1. Required Repository Artifacts

Verify the repository contains:

- README.md
- NARRATIVE.md
- AGENTS.md
- CLAUDE.md

Evidence directory:

```
evidence/
```

Test suite:

```
tests/
```

CI configuration:

```
.gitlab-ci.yml
```

---

## 2. Merge Request Demonstration

Create a demonstration MR showing constitutional enforcement.

Example scenario:

Create a commit containing:

```python
def login():
    pass
```

And documentation claiming the function is implemented.

Expected behavior:

Pipeline detects **phantom completion (I2)**.

Merge request is blocked.

Judges can observe:

- MR discussion
- CI pipeline logs
- failure report

---

## 3. Demo Video Requirements

Video should demonstrate:

1. Opening a Merge Request
2. CI pipeline executing
3. AI agents analyzing MR
4. Constitutional violation detection
5. Merge blocked by invariant enforcement

Recommended length:

3-5 minutes.

---

## 4. Verification Steps for Judges

To verify system behavior:

Clone repository

```bash
git clone https://gitlab.com/gitlab-ai-hackathon/participants/28441830.git
```

Run tests

```bash
pytest tests/
```

Run invariant checks

```bash
pytest tests/test_constitution.py
```

Review CI pipeline history.

---

## 5. Evidence for Judging

Evidence should include:

- Pipeline execution logs
- MR review comments from agent
- V&T reports
- Test results

These artifacts appear in:

```
evidence/
```

---

## 6. Judging Criteria Alignment

| Criterion | Evidence |
|----------|----------|
| Technical Implementation | CI pipeline + agents |
| Innovation | Constitutional AI enforcement |
| Reliability | invariant I1-I6 enforcement |
| Integration | GitLab Duo + Claude Code |
| Demonstration | MR pipeline example |

---

## 7. Final Pre-Submission Checks

Confirm:

- [ ] CI pipeline passes on main branch
- [ ] Merge request demo works
- [ ] Demo video uploaded
- [ ] README clearly explains system
- [ ] Judges can reproduce verification locally

---

## Submission Status

**NOT READY**

_Update to READY once all checks above are confirmed._
