# PROACTIVE Demo Video Script — Final

**Target length:** 60–90 seconds
**Format:** Screen recording with voiceover narration
**Core demo:** MR !9 — phantom completion detection and BLOCK verdict

---

## OPENING HOOK (0:00–0:12)

**Screen:** Show MR !9 title and description in GitLab.

**Narration:**
> "This merge request claims to add a complete authentication system with 98% test coverage and production-ready code. Every function body is empty. Every test is a stub. No tool on the market catches this. PROACTIVE does."

---

## DEMO SECTION (0:12–0:50)

**Screen action:** Scroll through MR !9 description. Highlight the claims:
- "fully implemented and production-ready"
- "98% line coverage"
- "All edge cases verified"
- "Penetration testing completed"

**Narration:**
> "PROACTIVE is a constitutional safety agent for GitLab Duo. It extracts every claim from the MR description and validates each one against six invariants."

**Screen action:** Click to the "Changes" tab. Show `proactive/auth.py`. Scroll to the `login` function. The body is `pass`.

**Narration:**
> "Here is the actual code. The login function — the one described as 'fully implemented with rate limiting and brute-force protection' — is a single `pass` statement."

**Screen action:** Show `tests/test_auth.py`. Scroll through. Every test body is `pass` with `# TODO: implement`.

**Narration:**
> "The tests claimed to provide 98% coverage. Every test is a TODO stub."

**Screen action:** Show the PROACTIVE review output (either from Duo Chat or a screenshot of the formatted V&T report). Highlight:
- I2 VIOLATION: Phantom completion detected
- I1 VIOLATION: Untagged absolute claims
- Verdict: BLOCKED
- Trust Score: low percentage

**Narration:**
> "PROACTIVE detects the phantom completion — invariant I2 — and blocks the merge. The verdict is BLOCK. The V&T statement documents exactly what was checked and what failed."

---

## DIFFERENTIATION SECTION (0:50–1:10)

**Screen action:** Show a split view or text overlay:
- Left: "Code review tools ask: Is this code well-written?"
- Right: "PROACTIVE asks: Is what this MR claims actually true?"

**Narration:**
> "Existing tools review code quality. PROACTIVE validates whether claims about the code are true. That is the difference between catching a style issue and catching a safety violation. Linters see syntax. PROACTIVE sees lies."

---

## CLOSING (1:10–1:20)

**Screen action:** Show the repository URL and the PROACTIVE name.

**Narration:**
> "PROACTIVE — constitutional epistemic safety for GitLab. Enforceable AI governance, working today."

---

## PRODUCTION NOTES

- **MR to open:** [!9](https://gitlab.com/gitlab-ai-hackathon/participants/28441830/-/merge_requests/9)
- **Key files to show in Changes tab:**
  - `proactive/auth.py` — scroll to `def login(...)`, show `pass` body
  - `tests/test_auth.py` — scroll through, show `# TODO: implement` stubs
  - `docs/auth-design.md` — show "Status: Complete" header
- **V&T output:** Use a pre-generated screenshot if Duo Chat is unavailable live. See `docs/demo-runbook-final.md` for fallback instructions.
- **Pacing:** Speak slowly and clearly. Pause 1 second after each key claim. Let the screen do the work during the diff sections.
- **Do NOT say:** "The Living Constitution", "healthcare", "SentinelOS", or any component that is not implemented.
- **DO say:** "constitutional safety agent", "epistemic safety", "phantom completion", "claims validation"
