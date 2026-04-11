# CRSP-B-004: README Rewrite (Research-First)

## Contract Identity

| Field | Value |
|-------|-------|
| Contract ID | CRSP-B-004 |
| Series | Series B — Fellowship-Ready Refactor |
| Title | README Rewrite (Research-First) |
| Depends On | CRSP-B-003 |
| Completion Marker | `plans/series-b/.done-B-004` |
| Branch | `claude/refactor-repo-voice-UEFMp` |

## Pre-Flight Check

```bash
test -f plans/series-b/.done-B-003 || { echo "BLOCKED: CRSP-B-003 not complete"; exit 1; }
```

## Why This Contract Exists

The current README opens with a YAML frontmatter block and describes the repo as a "governance overlay." It routes the reader to `docs/instructions/FIRST_RUN.md`. An Anthropic fellowship reviewer will spend 30 seconds on this page. If they don't immediately understand what this project contributes to AI safety research, they leave.

The README needs to lead with the research contribution, not the folder structure. It needs to make one clear argument: this project extends Constitutional AI with runtime governance that structurally addresses alignment faking, and it's built as working code.

## Pre-Flight Reads (MANDATORY)

1. `README.md` — the current file (to understand what exists)
2. `01-anthropic/fellowship-positioning.md` — the author's argument (this is the source of truth for the pitch)
3. `01-anthropic/research-alignment.md` — the specific research connections
4. `01-anthropic/repo-relationship-map.md` — the full system map
5. `src/guardian.py` — lines 1-27 (the module docstring describes what it does)
6. `THE_LIVING_CONSTITUTION.md` — lines 1-50 (the core metaphor)
7. `tests/failure_modes/F1/case_001.json` — a concrete example of the failure taxonomy
8. `STATUS.json` — current operational status

## Ordered Operations

### OP-1: Rewrite README.md

Replace the entire README with a research-first document. Structure:

**Section 1: The Thesis (3-4 sentences)**
- What Constitutional AI is (Anthropic's approach — training-time principles)
- What this project adds (runtime governance — the structural layer constitutions require)
- One sentence on what's actually built (Guardian Kernel, Sandbox Engine, Failure Taxonomy)
- CI badge (keep the existing one)

**Section 2: The Contribution (bullet list, 5-7 items)**
Each item names a specific mechanism with a one-line description and the file path where it lives:
- Articles I-V: enumerated rights, execution law, purpose law, separation of powers, amendment process → `THE_LIVING_CONSTITUTION.md`
- Guardian Kernel: MCP server that intercepts every agent tool call and evaluates safety invariants → `src/guardian.py`
- Sandbox Engine: namespace-jailed execution cell with constitutional halt authority → `projects/sandbox-runtime/src/`
- Failure Taxonomy (F1-F5): five classes of AI failure with concrete test cases from production systems → `tests/failure_modes/`
- Separation of Powers: six agents with defined boundaries — no agent judges its own work → `THE_LIVING_CONSTITUTION.md` Article IV
- Default User Doctrine: design for the most vulnerable user first (neurodivergent-accessible by default) → `THE_LIVING_CONSTITUTION.md` Article I
- Amendment Process: structured trigger-observe-propose-evaluate-ratify cycle → `THE_LIVING_CONSTITUTION.md` Article V

**Section 3: How It Relates to Anthropic's Research (compact table)**
Pull from `01-anthropic/research-alignment.md` — the 5-row summary table. Do not copy the whole doc. Just the table.

**Section 4: What's Built vs What's Specified (honest status)**
Two columns: "Working Code" and "Specification Only". Be honest. Working code: Guardian Kernel, Sandbox Engine, Governance Verifiers, CI Pipeline, Failure Taxonomy. Specification only: SentinelOS runtime, Agent Republic multi-agent orchestration, ND Access Layer, MCP tool integration.

**Section 5: Run It**
```bash
# Bootstrap
./scripts/bootstrap_repo.sh

# Run tests
pytest tests/ -v

# Verify governance
python3 scripts/verify_governance_chain.py --root .
```

**Section 6: Author**
One paragraph. Who Corey is, the lived experience angle, the Default User Doctrine origin. Pull from `01-anthropic/fellowship-positioning.md` "What Corey Brings" section — but write it in first person, in Corey's voice, not third person academic.

### OP-2: Remove YAML frontmatter from README

The current README starts with:
```yaml
---
document_type: "Navigational"
id: "DOC-README-ROOT-001"
...
---
```

This is governance infrastructure. It's useful for internal verifiers but it's the first thing a human sees. Remove it from README.md. If the documentation verifier requires frontmatter on README.md, add it as an HTML comment instead:

```html
<!-- document_type: Navigational | id: DOC-README-ROOT-001 | status: Active -->
```

### OP-3: Verify README is under 120 lines

A good README is scannable. Count the lines. If over 120, cut. The details live in the linked files — the README is a landing page, not an encyclopedia.

```bash
wc -l README.md
```

## Voice Constraint

The README is the public face of Corey's work. It must sound like Corey — direct, confident, no hedging, no academic passive voice. "This project extends Constitutional AI" not "This project seeks to explore potential extensions to the Constitutional AI framework." The work speaks for itself when presented clearly.

Do NOT include phrases like "we believe," "we hope to," "this aims to." State what it does. State what it doesn't do yet. That's it.

## Acceptance Criteria

| AC | Requirement | Verification |
|----|-------------|--------------|
| AC-001 | README exists and is under 120 lines | `wc -l README.md` < 120 |
| AC-002 | First paragraph mentions Constitutional AI and runtime governance | `head -10 README.md` contains both phrases |
| AC-003 | CI badge preserved | `grep -c 'badge.svg' README.md` >= 1 |
| AC-004 | File paths for Guardian, Sandbox, Tests referenced | grep finds `src/guardian.py`, `sandbox-runtime`, `tests/` |
| AC-005 | Honest status section exists with "Working Code" and "Specification Only" | grep finds both phrases |
| AC-006 | No YAML frontmatter block visible | First line is not `---` |
| AC-007 | Run commands section exists | grep finds `pytest` and `verify_governance_chain` |

## Completion

```bash
echo "CRSP-B-004 COMPLETE" > plans/series-b/.done-B-004
git add README.md plans/series-b/.done-B-004
git commit -m "docs: rewrite README — research-first, honest status, author voice

Series B contract CRSP-B-004. README now leads with the Constitutional AI
extension thesis, lists concrete contributions with file paths, includes
honest built-vs-specified status, and presents the author's lived
experience in first person."
```
