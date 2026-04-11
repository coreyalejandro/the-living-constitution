# CRSP-B-006: Fellowship-Ready Surface

## Contract Identity

| Field | Value |
|-------|-------|
| Contract ID | CRSP-B-006 |
| Series | Series B — Fellowship-Ready Refactor |
| Title | Fellowship-Ready Surface |
| Depends On | CRSP-B-004, CRSP-B-005 |
| Completion Marker | `plans/series-b/.done-B-006` |
| Branch | `claude/refactor-repo-voice-UEFMp` |

## Pre-Flight Check

```bash
test -f plans/series-b/.done-B-004 || { echo "BLOCKED: CRSP-B-004 not complete"; exit 1; }
test -f plans/series-b/.done-B-005 || { echo "BLOCKED: CRSP-B-005 not complete"; exit 1; }
```

## Why This Contract Exists

The research positioning docs (`01-anthropic/`) are the strongest material in this repo. They make specific, bounded arguments connecting TLC to Anthropic's published research. But they're buried in a directory nobody would find unless they already knew to look there.

This contract creates a clear "fellowship surface" — a single directory that a reviewer can open and immediately understand: what the project is, why it matters for AI safety, what's built, and who built it.

## Pre-Flight Reads (MANDATORY)

1. `01-anthropic/fellowship-positioning.md` — the full file
2. `01-anthropic/research-alignment.md` — the full file
3. `01-anthropic/repo-relationship-map.md` — the full file
4. `README.md` — the rewritten version from B-004
5. `verification/MATRIX.md` — first 50 lines (understand the claim tracking)
6. `tests/failure_modes/` — all 5 JSON fixtures

## Ordered Operations

### OP-1: Restructure 01-anthropic/ into research/

Rename `01-anthropic/` to `research/`. The numbered prefix (`01-`) is internal governance taxonomy. A reviewer expects `research/`.

```bash
git mv 01-anthropic research
```

### OP-2: Create research/README.md

Write an index file for the research directory:

```markdown
# Research: Runtime Constitutional Governance for Agentic AI

This directory contains the research positioning, alignment analysis,
and system architecture documentation for The Living Constitution.

## Documents

| Document | What It Covers |
|----------|---------------|
| [fellowship-positioning.md](fellowship-positioning.md) | The core argument: TLC as a structural amendment to Constitutional AI |
| [research-alignment.md](research-alignment.md) | Point-by-point alignment with five areas of Anthropic's published research |
| [repo-relationship-map.md](repo-relationship-map.md) | How this repo relates to the broader Safety Systems Design Commonwealth |

## The Argument in Brief

Anthropic named its approach Constitutional AI — principles that guide model
behavior during training. The Living Constitution adds the structural
governance that constitutional systems require: enumerated rights, separation
of powers, runtime invariant enforcement, a formal amendment process, and
design for the most vulnerable user first.

This is not a critique. It is an Amendment.
```

### OP-3: Clean fellowship-positioning.md

Read `research/fellowship-positioning.md` (formerly `01-anthropic/fellowship-positioning.md`). This file is strong but needs minor cleanup:

1. **Update any stale claims.** Check that every specific number cited (e.g., "212/212 tests passing", "53 claims across 9 categories") is still accurate or clearly labeled with its verification source. If you cannot verify a number, add a parenthetical: "(as of last PROACTIVE verification run)".

2. **Remove the third-person framing.** The "What Corey Brings" section talks about Corey in third person. For a fellowship application, this should be first person. Change "Corey is neurodivergent" to "I am neurodivergent." Change "Corey would contribute" to "I would contribute." This is HIS document about HIS work.

3. **Keep the V&T statement.** It's honest and bounded. Don't touch it.

### OP-4: Clean research-alignment.md

Read `research/research-alignment.md`. This file is well-structured and honest. Minor cleanup only:

1. **Verify all citation years are correct.** Bai et al. 2022 for Constitutional AI. Greenblatt et al. 2024 for alignment faking. Check these are right.
2. **Keep the Boundaries section.** It explicitly states what the doc does NOT claim. This is rare and valuable.
3. **Keep the V&T statement.**

### OP-5: Update references to 01-anthropic/ across the repo

After the rename, grep for `01-anthropic` and update references:

```bash
grep -rl "01-anthropic" --include="*.md" --include="*.json" --include="*.py" . | grep -v ".git/"
```

Update each file to reference `research/` instead of `01-anthropic/`.

### OP-6: Add research link to README

Ensure the new README (from B-004) links to `research/` directory. If it doesn't already, add a line in the contributions section:

```markdown
**Full research positioning:** [`research/`](research/)
```

## Voice Constraint

The fellowship-positioning.md is Corey's best writing in this repo. The "Amendment, not critique" framing is original and compelling. The Default User Doctrine section is written from lived experience that cannot be faked. Do NOT rewrite these sections. Only change third-person to first-person where indicated, and verify specific numbers.

## Acceptance Criteria

| AC | Requirement | Verification |
|----|-------------|--------------|
| AC-001 | `research/` directory exists | `test -d research` |
| AC-002 | `01-anthropic/` no longer exists | `test ! -d 01-anthropic` |
| AC-003 | `research/README.md` exists | `test -f research/README.md` |
| AC-004 | fellowship-positioning.md uses first person | `grep -c "I am neurodivergent\|I would contribute" research/fellowship-positioning.md` >= 1 |
| AC-005 | No remaining references to `01-anthropic/` | `grep -rl "01-anthropic" --include="*.md" --include="*.json" . \| grep -v .git \| wc -l` returns 0 |
| AC-006 | README links to `research/` | `grep -c 'research/' README.md` >= 1 |

## Completion

```bash
echo "CRSP-B-006 COMPLETE" > plans/series-b/.done-B-006
git add research/ README.md plans/series-b/.done-B-006
# Also add any files that had 01-anthropic references updated
git add -u
git commit -m "feat: create research surface — rename 01-anthropic to research, first-person voice

Series B contract CRSP-B-006. Research positioning and alignment docs
moved to research/ for discoverability. Fellowship positioning converted
to first person. All cross-references updated."
```
