# PROACTIVE Demo Recording Runbook — Final

**Purpose:** Step-by-step operator guide for recording the hackathon demo video.

---

## Pre-Recording Setup

1. Open a browser. Log in to GitLab at https://gitlab.com.
2. Navigate to the project: https://gitlab.com/gitlab-ai-hackathon/participants/28441830
3. Open MR !9: https://gitlab.com/gitlab-ai-hackathon/participants/28441830/-/merge_requests/9
4. Verify MR !9 is still open and the diff is visible.
5. Open your screen recording tool. Set resolution to 1920x1080 or higher.
6. Set recording area to the browser window only (no desktop clutter).
7. Test your microphone. Record 5 seconds of silence and play back to check levels.
8. Open `docs/video-script-final.md` in a separate window or printed copy for narration reference.

---

## Recording Sequence

### Part 1: Opening Hook (0:00–0:12)

9. Start recording.
10. Browser should show MR !9 overview page (title + description visible).
11. Read the opening narration from the script.
12. Pause 1 second.

### Part 2: Claims Walkthrough (0:12–0:30)

13. Slowly scroll through the MR !9 description.
14. Pause on each bold claim:
    - "fully implemented and production-ready"
    - "98% line coverage across all authentication paths"
    - "All edge cases verified"
    - "Penetration testing completed on 2026-03-01"
15. Read the narration about claim extraction and invariants.

### Part 3: Show the Actual Code (0:30–0:45)

16. Click the **"Changes"** tab in MR !9.
17. Scroll to `proactive/auth.py`.
18. Find the `def login(username: str, password: str) -> dict:` function.
19. Pause on the function body: `pass`. Hold for 2 seconds.
20. Read the narration about the empty function body.
21. Scroll to `tests/test_auth.py`.
22. Show 3–4 test functions. Each has `# TODO: implement` and `pass`.
23. Read the narration about the test stubs.

### Part 4: Show PROACTIVE Verdict (0:45–0:55)

24. **Option A (Live Duo Chat):**
    - Open GitLab Duo Chat panel.
    - Type: `@proactive review MR !9 for epistemic safety`
    - Wait for response.
    - Scroll through the output. Highlight I2 violation and BLOCK verdict.

25. **Option B (Pre-generated output — use if Duo Chat is unavailable):**
    - Switch to a browser tab showing a pre-captured screenshot of the PROACTIVE review output.
    - The screenshot should show: I2 VIOLATION, I1 VIOLATION, Verdict: BLOCKED, Trust Score, V&T Statement.
    - Scroll through the screenshot slowly.

26. Read the narration about the BLOCK verdict.

### Part 5: Differentiation (0:55–1:10)

27. Show a prepared slide or text overlay with the two-column comparison:
    - Left: "Code review tools: Is this code well-written?"
    - Right: "PROACTIVE: Is what this MR claims actually true?"
28. Read the differentiation narration.

### Part 6: Closing (1:10–1:20)

29. Navigate back to the project root: https://gitlab.com/gitlab-ai-hackathon/participants/28441830
30. Read the closing narration.
31. Hold on the project page for 3 seconds.
32. Stop recording.

---

## Fallback: Screenshot-Based Demo

If live recording is not possible, capture these screenshots in order:

1. **Screenshot 1:** MR !9 overview — title and full description visible.
2. **Screenshot 2:** MR !9 description scrolled to show claims ("98% coverage", "production-ready").
3. **Screenshot 3:** Changes tab — `proactive/auth.py` with `def login(...)` and `pass` body visible.
4. **Screenshot 4:** Changes tab — `tests/test_auth.py` with 3–4 `# TODO: implement` stubs visible.
5. **Screenshot 5:** Changes tab — `docs/auth-design.md` with "Status: Complete" visible.
6. **Screenshot 6:** PROACTIVE review output showing I2 violation, BLOCK verdict, and V&T statement.
7. **Screenshot 7:** Two-column differentiation text.
8. **Screenshot 8:** Project root page.

Assemble screenshots into a video with narration voiceover using any video editor. Target 60–90 seconds.

---

## Generating the PROACTIVE Review Output (for Screenshot 6)

If you need to generate the review output locally:

```bash
git clone https://gitlab.com/gitlab-ai-hackathon/participants/28441830.git
cd 28441830
pip install -e ".[dev]"

# Run the test that exercises the MR analyzer on phantom completion
pytest tests/test_mr_analyzer.py -v -k phantom

# Or run the full test suite to confirm everything passes
pytest tests/ -v --cov=proactive
```

The test output will show the I2 violation detection and BLOCK verdict. Screenshot the terminal output.

---

## Post-Recording Checklist

- [ ] Video is 60–90 seconds long
- [ ] MR !9 is clearly visible
- [ ] Empty `pass` function bodies are shown
- [ ] PROACTIVE verdict (BLOCK) is shown
- [ ] V&T statement is visible
- [ ] Differentiation slide/overlay is included
- [ ] Audio is clear and narration matches script
- [ ] No personal information, API keys, or tokens visible on screen
- [ ] No claims about unimplemented features (TLC runtime, healthcare, UICare)
