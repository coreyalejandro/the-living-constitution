# FINAL VIDEO SCRIPT — PROACTIVE Demo

**Total runtime:** 80 seconds  
**Format:** Screen recording + voiceover  
**Demo artifact:** MR !9 (phantom completion)

---

## SEGMENT 1 — HOOK (0:00–0:12)

**On-screen:** MR !9 overview page. Title and description visible.

**Voiceover (exact words):**
> "This merge request claims to add a complete authentication system with 98% test coverage and production-ready code. Every function body is empty. Every test is a stub. No tool on the market catches this. PROACTIVE does."

---

## SEGMENT 2 — CLAIMS WALKTHROUGH (0:12–0:28)

**On-screen:** Slowly scroll MR !9 description. Pause 1.5 seconds on each claim:
- "fully implemented and production-ready"
- "98% line coverage across all authentication paths"
- "All edge cases verified"
- "Penetration testing completed"
- "Supports 10,000 concurrent sessions"

**Voiceover (exact words):**
> "PROACTIVE is a constitutional safety agent for GitLab Duo. It extracts every claim from the MR description and validates each one against six invariants."

---

## SEGMENT 3 — THE ACTUAL CODE (0:28–0:42)

**On-screen:** Click "Changes" tab. Scroll to `proactive/auth.py`. Pause on `def login(username: str, password: str) -> dict:` — body is `pass`. Hold 2 seconds.

**Voiceover (exact words):**
> "Here is the actual code. The login function — described as fully implemented with rate limiting and brute-force protection — is a single pass statement."

**On-screen:** Scroll to `tests/test_auth.py`. Show 3–4 test functions. Each body is `# TODO: implement` followed by `pass`.

**Voiceover (exact words):**
> "The tests claimed to provide 98% coverage. Every test is a TODO stub."

---

## SEGMENT 4 — PROACTIVE VERDICT (0:42–0:55)

**On-screen:** Show PROACTIVE review output. Highlight:
- I2 VIOLATION (ERROR): Phantom completion — claims "fully implemented" but every function body is `pass`
- I1 VIOLATION (ERROR): Untagged absolute claims — "all tests pass", "fully implemented"
- I4 VIOLATION (WARNING): No issue reference
- Verdict: **BLOCKED**
- V&T Statement visible

**Voiceover (exact words):**
> "PROACTIVE detects the phantom completion — invariant I2 — and blocks the merge. The verdict is BLOCK. The V&T statement documents exactly what was checked and what failed."

---

## SEGMENT 5 — DIFFERENTIATION (0:55–1:10)

**On-screen:** Two-column overlay:
- Left column: "Code review tools ask: Is this code well-written?"
- Right column: "PROACTIVE asks: Is what this MR claims actually true?"

**Voiceover (exact words):**
> "Existing tools review code quality. PROACTIVE validates whether claims about the code are true. That is the difference between catching a style issue and catching a safety violation. Linters see syntax. PROACTIVE sees lies."

---

## SEGMENT 6 — CLOSE (1:10–1:20)

**On-screen:** Project root page: https://gitlab.com/gitlab-ai-hackathon/participants/28441830

**Voiceover (exact words):**
> "PROACTIVE — constitutional epistemic safety for GitLab. Enforceable AI governance, working today."

**Hold 3 seconds. Stop recording.**

---

## HARD RULES

- Do NOT say: "The Living Constitution", "healthcare", "SentinelOS", "UICare", "ConsentChain"
- DO say: "constitutional safety agent", "epistemic safety", "phantom completion", "claims validation"
- Speak slowly. Pause 1 second after each key claim.
- Let the screen do the work during diff sections.
- Total runtime must be 60–90 seconds.
