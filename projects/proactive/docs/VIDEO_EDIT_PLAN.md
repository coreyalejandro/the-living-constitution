# VIDEO EDIT PLAN — PROACTIVE Demo

**Decision: NEW RECORDING REQUIRED**

No existing video was provided for evaluation. This plan covers full recording from scratch.

---

## PRE-RECORDING CHECKLIST

- [ ] Browser open, logged into GitLab
- [ ] MR !9 open: https://gitlab.com/gitlab-ai-hackathon/participants/28441830/-/merge_requests/9
- [ ] MR !9 is still in `opened` state (confirmed: yes)
- [ ] Screen recording tool set to 1920x1080
- [ ] Recording area = browser window only (no desktop, no dock)
- [ ] Microphone tested (5-second silence playback check)
- [ ] Printed copy of FINAL_VIDEO_SCRIPT.md visible off-screen
- [ ] Two-column differentiation overlay prepared (PNG or slide)
- [ ] PROACTIVE verdict screenshot prepared (see Generation section below)

---

## RECORDING STEPS — EXACT SEQUENCE

### Step 1: Position browser
- Navigate to MR !9 overview page
- Ensure title "feat: implement secure login authentication system" is fully visible
- Ensure description is scrolled to top
- Start recording

### Step 2: Hold on MR overview (12 seconds)
- Do not scroll for 3 seconds
- Read SEGMENT 1 voiceover
- Begin slow scroll through description

### Step 3: Scroll through claims (16 seconds)
- Scroll slowly. Pause 1.5 seconds on each claim block:
  1. "fully implemented and production-ready"
  2. "98% test coverage achieved"
  3. "OWASP Top 10 authentication risks addressed"
  4. "Penetration testing completed"
  5. "Supports 10,000 concurrent sessions"
- Read SEGMENT 2 voiceover during scroll

### Step 4: Click Changes tab (14 seconds)
- Click "Changes" tab
- Wait for diff to load (1 second)
- Scroll to `proactive/auth.py`
- Find `def login(username: str, password: str) -> dict:`
- Pause on `pass` body — hold 2 seconds
- Read first half of SEGMENT 3 voiceover
- Scroll to `tests/test_auth.py`
- Show 3–4 test functions with `# TODO: implement` + `pass`
- Read second half of SEGMENT 3 voiceover

### Step 5: Show PROACTIVE verdict (13 seconds)
- Switch to pre-captured PROACTIVE output (new browser tab or overlay)
- Show: I2 VIOLATION, I1 VIOLATION, Verdict: BLOCKED, V&T Statement
- Scroll slowly through output
- Read SEGMENT 4 voiceover

### Step 6: Show differentiation (15 seconds)
- Display two-column overlay or switch to prepared slide
- Left: "Code review tools ask: Is this code well-written?"
- Right: "PROACTIVE asks: Is what this MR claims actually true?"
- Read SEGMENT 5 voiceover

### Step 7: Close (10 seconds)
- Navigate to project root
- Read SEGMENT 6 voiceover
- Hold 3 seconds
- Stop recording

---

## GENERATING THE PROACTIVE VERDICT SCREENSHOT

```bash
git clone https://gitlab.com/gitlab-ai-hackathon/participants/28441830.git
cd 28441830
pip install -e ".[dev]"

# Run the phantom completion test
pytest tests/test_mr_analyzer.py -v -k phantom

# Or run full suite
pytest tests/ -v --cov=proactive
```

Screenshot the terminal output showing:
- I2 violation detection
- BLOCK verdict
- V&T statement

Alternatively, use the web UI:
```bash
python -m proactive.web_ui
# Open http://localhost:5000
# Paste MR !9 content and run analysis
```

---

## POST-RECORDING EDIT INSTRUCTIONS

### Cuts
- Remove any dead time > 2 seconds (except the intentional 2-second hold on `pass`)
- Remove any browser loading spinners > 1 second (speed up 4x)
- Remove any false starts or narration stumbles

### Overlays to add in post
- **0:42–0:55:** If verdict is shown as terminal output, add a semi-transparent overlay box highlighting "BLOCKED" in red
- **0:55–1:10:** Two-column comparison text (if not using a prepared slide)
- **1:10–1:20:** Project URL text overlay at bottom: `gitlab.com/gitlab-ai-hackathon/participants/28441830`

### Audio
- Normalize voiceover to -14 LUFS
- No background music
- No sound effects

### Export
- Format: MP4, H.264
- Resolution: 1920x1080
- Frame rate: 30fps
- Target file size: < 50MB
- Filename: `proactive-demo-final.mp4`

---

## TIMING BUDGET

| Segment | Duration | Cumulative |
|---------|----------|------------|
| Hook | 12s | 0:12 |
| Claims walkthrough | 16s | 0:28 |
| Actual code | 14s | 0:42 |
| PROACTIVE verdict | 13s | 0:55 |
| Differentiation | 15s | 1:10 |
| Close | 10s | 1:20 |
| **Total** | **80s** | **1:20** |

If over 90 seconds after recording, cut from:
1. Claims walkthrough (reduce pauses to 1 second each)
2. Differentiation (trim to 10 seconds)
3. Close (trim hold to 2 seconds)
