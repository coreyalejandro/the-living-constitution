# Runtime Model
## How the Commonwealth Operates at Runtime

---

## Overview

The Living Constitution is not a static document. At runtime, it operates through a layered execution model where governance rules are enforced by agents, hooks, CI pipelines, and configuration validators. This document describes how the system operates when a human gives an instruction and work flows through the Commonwealth.

---

## The Six-Layer Runtime Stack

The Commonwealth operates through six layers, from human intent at the top to evidence at the bottom. Each layer has a runtime role.

### Layer 6: Human Orchestrator

**Runtime role:** Provides intent, approves critical actions, receives plain-language summaries.

The human does not execute. The human states what they want, reviews what agents propose, and approves actions that cross authorization boundaries (Article IV). The human receives output formatted for the Default User profile: no skipped steps, clear completion signals, one thing at a time.

**Runtime artifacts:** Verbal or typed instructions, approval signals, corrections.

### Layer 5: Orchestration Cortex

**Runtime role:** Routes tasks to agents, enforces constitutional rules, manages context.

The orchestration cortex is Claude Code operating under CLAUDE.md instructions. When an instruction arrives from the human, the cortex:
1. Determines task complexity. If non-trivial (3+ steps or architectural decisions), enters plan mode.
2. Selects the appropriate agent(s) based on task type.
3. Dispatches work to agents with constitutional constraints attached.
4. Receives agent outputs and validates them against Article I (rights) and Article II (code governance).
5. Presents results to the human with a V&T Statement.

**Runtime artifacts:** `tasks/todo.md`, agent dispatch commands, V&T Statements.

### Layer 4: Agent Republic

**Runtime role:** Executes tasks within constitutional bounds.

Six agent types operate under Article IV's separation of powers:

| Agent | Runtime Behavior |
|-------|-----------------|
| Planner | Receives task description, produces implementation plan in `tasks/todo.md`. Cannot change architecture without human approval. |
| Builder | Receives plan items, writes code and tests. Cannot deploy to production or modify database schema without approval. |
| Sentinel | Runs continuously during agent execution. Monitors outputs for invariant violations (I1-I6). Can raise STOP signals to halt any agent. Cannot override agents or modify its own rules. |
| TDD Guide | Enforces test-first workflow: write test (RED), implement (GREEN), refactor (IMPROVE). Cannot skip the RED phase or ship below 80% coverage. |
| Code Reviewer | Reviews code after Builder writes it. Flags CRITICAL, HIGH, MEDIUM, LOW issues. Cannot auto-fix CRITICAL issues or approve its own work. |
| Data Scientist | Updates metrics, generates impact reports, syncs knowledge base. Cannot redefine theory of change nodes without human review. |

**Orchestration patterns:**
- Agents run in parallel when tasks are independent (security review + type checking + performance review).
- Agents run sequentially when tasks depend on each other (plan first, then build, then review).
- Subagents are spawned liberally to keep the main context window clean.
- Each subagent handles one focused track.

**Runtime artifacts:** Code files, test files, review reports, audit logs.

### Layer 3: Tool and MCP Republic

**Runtime role:** Provides external capabilities under Article II validation.

Tools include GitHub, Notion, Vercel, Cloudflare, evaluation harnesses, and MCP (Model Context Protocol) servers. Every tool call is validated before execution:
- Does the tool call comply with Article II (code governance)?
- Does the tool call require human approval under Article IV?
- Does the tool call access sensitive data (PII, secrets)?

Pre-tool-use hooks validate parameters. Post-tool-use hooks verify results and trigger formatting, type checking, or security scanning.

**Runtime artifacts:** API responses, deployment results, formatted files.

### Layer 2: Neurodivergent Access Infrastructure

**Runtime role:** Filters all outputs through Article I accessibility requirements.

Before any output reaches the human:
- Cognitive load is assessed. If the output would exceed the user's current capacity, it is broken into smaller pieces.
- Multiple modalities are used: text, tables, diagrams, numbered sequences, visual markers.
- Completion signals are explicit: "This step is done. Here is what changed. Here is what comes next."
- Error states include recovery paths as clear as the happy path.

This layer is conceptual at Tier 1. UICare implements portions of this layer for web interfaces. For CLI interactions (Claude Code), the CLAUDE.md instructions encode these requirements as agent behavior rules.

**Runtime artifacts:** Formatted output, pacing signals, completion confirmations.

### Layer 1: Evidence and Change Foundation

**Runtime role:** Ensures every output traces to a theory of change node and is measurable.

Article III requires evidence-bound output. At runtime, this means:
- Every task links to a theory of change node (what change is this work intended to produce?).
- Every completion includes verification (did the change actually occur?).
- Lessons from corrections are captured in `tasks/lessons.md`.
- Impact metrics are updated when measurable outcomes are produced.

**Runtime artifacts:** `tasks/lessons.md`, verification matrix entries, build contract compliance records.

---

## Agent Orchestration Flow

When a human gives an instruction, here is the complete runtime flow:

```
Human instruction arrives
        │
        ▼
┌─────────────────────────┐
│ Orchestration Cortex    │
│ (Claude Code + CLAUDE.md)│
│                         │
│ 1. Parse intent         │
│ 2. Check complexity     │
│ 3. Enter plan mode if   │
│    non-trivial          │
└────────┬────────────────┘
         │
         ▼
┌─────────────────────────┐
│ Agent Selection         │
│                         │
│ Complex feature? → Planner first    │
│ Bug fix? → Builder directly         │
│ New feature? → TDD Guide first      │
│ Architectural? → Planner + review   │
└────────┬────────────────┘
         │
         ▼
┌─────────────────────────┐
│ Agent Execution         │
│                         │
│ Parallel where possible │
│ Sequential where needed │
│ Sentinel monitors all   │
└────────┬────────────────┘
         │
         ▼
┌─────────────────────────┐
│ Output Validation       │
│                         │
│ Article I: Rights check │
│ Article II: Code check  │
│ V&T Statement generated │
└────────┬────────────────┘
         │
         ▼
┌─────────────────────────┐
│ ND Access Filter        │
│                         │
│ Format for Default User │
│ Pace appropriately      │
│ Signal completion       │
└────────┬────────────────┘
         │
         ▼
   Output to Human
```

---

## Governance Flow at Runtime

Constitutional governance is not a separate process that runs occasionally. It runs continuously, on every turn.

**Every agent turn:**
1. The agent produces output.
2. The output is checked against Article I rights (safety, accessibility, dignity, clarity, truth).
3. The output is checked against Article II code rules (immutability, truth-status, simplicity).
4. A V&T Statement is generated declaring what exists, what does not, and what is unverified.

**Every session start:**
1. `tasks/lessons.md` is loaded to prevent F5 (cross-episode recurrence).
2. Project CLAUDE.md is loaded with any ratified amendments.
3. Build contracts are available for reference.

**Every session end:**
1. Corrections are checked for persistence (F5 prevention).
2. `tasks/todo.md` is updated with completed and remaining items.
3. If pausing (SOP-013), state is saved to `tasks/pause-state.md`.

**Every significant commit:**
1. V&T Statement covers the commit's changes.
2. Truth-status declarations are updated if module status changed.
3. Build contracts are checked for compliance.

---

## Error Handling and Recovery

**Agent error:** If an agent encounters an error, it does not swallow it. It reports the error with a user-friendly message, suggests a recovery path, and updates the V&T Statement to reflect the failure.

**Sentinel STOP signal:** If the Sentinel detects an invariant violation, all agents pause. The violation is reported to the human with: what happened, which invariant was violated, what the safe state is, and what action is recommended.

**Session recovery (SOP-013):** If the human signals overwhelm or the system detects high cognitive load, the Session Recovery Protocol activates: all agents pause, completed work is displayed, state is saved, and a gentle close message is provided.

**Build failure:** If a build fails, the build-error-resolver agent is invoked. It analyzes the error, attempts a fix, and verifies the fix. The human is not asked to debug — the agent resolves it autonomously.

---

## V&T Statement
- **Exists:** Runtime model describing all six layers of the Commonwealth stack; agent orchestration flow with selection criteria; governance flow at every turn, session start, session end, and commit; error handling and recovery procedures; tool validation description
- **Non-existent:** Automated cognitive load assessment in CLI mode (conceptual at Tier 1); runtime sentinel monitoring (SentinelOS packages exist but runtime wiring pending); theory of change node linking at runtime
- **Unverified:** Whether all six agent instruction files are currently functional; whether post-tool-use hooks are active in all repositories
- **Functional status:** Runtime model is fully specified — execution relies on Tier 1 convention (CLAUDE.md instructions + agent behavior rules) with partial Tier 2 automation via PROACTIVE CI integration
