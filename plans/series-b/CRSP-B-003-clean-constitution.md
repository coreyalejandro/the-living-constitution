# CRSP-B-003: Clean THE_LIVING_CONSTITUTION.md

## Contract Identity

| Field | Value |
|-------|-------|
| Contract ID | CRSP-B-003 |
| Series | Series B — Fellowship-Ready Refactor |
| Title | Clean THE_LIVING_CONSTITUTION.md |
| Depends On | CRSP-B-001 |
| Completion Marker | `plans/series-b/.done-B-003` |
| Branch | `claude/refactor-repo-voice-UEFMp` |

## Pre-Flight Check

```bash
test -f plans/series-b/.done-B-001 || { echo "BLOCKED: CRSP-B-001 not complete"; exit 1; }
```

## Why This Contract Exists

THE_LIVING_CONSTITUTION.md is the supreme document of this entire project. It is referenced by every verifier, every contract, every invariant. Right now it has two problems:

1. Raw XML artifacts (`</text>` and `</response>`) from a ChatGPT export sitting on lines 399-400
2. A Sources section at the bottom that links to generic blog posts and tutorials — not primary research. This undermines credibility.

The content itself — the constitutional metaphor, the enforcement stack, the amendment process, the agent republic, the SOP library — is genuinely original work. It needs to be cleaned, not rewritten. The author's voice stays. The architecture stays. The artifacts and filler go.

## Pre-Flight Reads (MANDATORY)

1. `THE_LIVING_CONSTITUTION.md` — the full file, every line
2. `01-anthropic/research-alignment.md` — to understand which citations are legitimate
3. `01-anthropic/fellowship-positioning.md` — to understand the author's framing

## Ordered Operations

### OP-1: Remove XML artifacts

Find and remove these exact lines (near line 399):
```
</text>
</response>
```

These are ChatGPT export artifacts. They are not content. Delete them.

### OP-2: Clean up the Sources section

The current Sources section (starting around line 404) lists generic blog posts:
- dextralabs.com, dev.to, thoughtminds.ai, shipyard.build, claudefa.st

These are not primary sources. They are filler that a reviewer will notice immediately and it will hurt credibility.

**Replace the Sources section with this:**

```markdown
---

## Foundational References

- Bai et al., "Constitutional AI: Harmlessness from AI Feedback" (Anthropic, 2022) — the constitutional metaphor this framework extends
- Greenblatt et al., "Alignment Faking in Large Language Models" (Anthropic, 2024) — the alignment faking problem that Article IV structurally addresses
- World Economic Forum, "How neurodivergent minds can help humanize AI governance" (2025) — external validation of the Default User premise
```

Only cite what the author's work actually engages with. These three are cited in the research-alignment doc with specific connections to TLC components. Everything else was generic background reading that doesn't belong in the constitution.

### OP-3: Verify constitutional hash still computes

The evidence ledger computes SHA-256 of this file. After edits, verify it still works:

```bash
python3 -c "
import hashlib
from pathlib import Path
content = Path('THE_LIVING_CONSTITUTION.md').read_bytes()
h = hashlib.sha256(content).hexdigest()
print(f'Constitutional hash: {h}')
print(f'File size: {len(content)} bytes')
assert len(h) == 64, 'Hash computation failed'
print('HASH CHECK: PASS')
"
```

### OP-4: Verify no structural changes

The file's heading structure is referenced by other documents. Verify the main headings still exist:

```bash
grep -n "^## " THE_LIVING_CONSTITUTION.md
```

Expected headings (must all be present):
- PAGE 1 — THE GOVERNING METAPHOR
- PAGE 2 — FULL ECOSYSTEM ARCHITECTURE
- PAGE 3 — THE AMENDMENT PROCESS
- PAGE 4 — SEPARATION OF POWERS
- PAGE 5 — SOP LIBRARY AND PRACTICAL IMPLEMENTATION
- Foundational References (new, replacing Sources)

## Acceptance Criteria

| AC | Requirement | Verification |
|----|-------------|--------------|
| AC-001 | No `</text>` or `</response>` in file | `grep -c '</text>\|</response>' THE_LIVING_CONSTITUTION.md` returns 0 |
| AC-002 | No dextralabs/shipyard/claudefast URLs | `grep -c 'dextralabs\|shipyard\|claudefa.st\|thoughtminds' THE_LIVING_CONSTITUTION.md` returns 0 |
| AC-003 | Foundational References section exists | `grep -c 'Foundational References' THE_LIVING_CONSTITUTION.md` returns 1 |
| AC-004 | All 5 PAGE headings still present | grep finds all 5 |
| AC-005 | Hash computation passes | OP-3 script prints `HASH CHECK: PASS` |
| AC-006 | File is still over 350 lines | `wc -l THE_LIVING_CONSTITUTION.md` > 350 |

## Voice Constraint

Do NOT rewrite the constitution's prose. The ASCII art, the SOP descriptions, the session recovery protocol, the agent power table — that is all Corey's original work and voice. You are removing artifacts and filler citations only. If you are tempted to "improve" the writing, stop. That is not this contract.

## Completion

```bash
echo "CRSP-B-003 COMPLETE" > plans/series-b/.done-B-003
git add THE_LIVING_CONSTITUTION.md plans/series-b/.done-B-003
git commit -m "fix: clean constitution — remove ChatGPT artifacts, replace filler citations

Series B contract CRSP-B-003. Removed </text></response> XML export
artifacts. Replaced generic blog post Sources with three primary
references the work actually engages with (Bai 2022, Greenblatt 2024,
WEF 2025). All original prose and structure preserved."
```
