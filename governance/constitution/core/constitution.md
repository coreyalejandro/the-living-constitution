# The Living Constitution
## Foundational Governance Document for the Safety Systems Design Commonwealth

**Source of truth:** `THE_LIVING_CONSTITUTION.md` (root of this repository)
**Governing authority:** This document summarizes and references the full constitutional specification.

---

## What This Is

The Living Constitution is the supreme governing document for all software, agents, outputs, and processes produced under the Safety Systems Design identity. It is not a style guide or a set of recommendations. It is the operating system for how work is done.

The Constitution exists because the systems that should have protected the most vulnerable did not. It was built by a person who needed it and could not find it. Every marginalized person who has survived a system not designed for them knows this story. The system should have been designed for us in the first place.

---

## Constitutional Foundation

The Constitution rests on three doctrines and five articles.

### Doctrines (Cross-Cutting Principles)

**The Idempotency Doctrine** — Do it once. Do it again. Same result. No hidden state, no side effects. If a function, deployment, instruction, or agent action cannot survive being run twice and producing the same outcome, it is not safe. This is the mathematical guarantee that a neurodivergent user with OCD-driven doubt loops or ADHD-driven restarts cannot break the system by trying again.

**The Calibrated Truth Doctrine** — The assurance level of a claim matches the method used to verify it. Three tiers: Tier 1 (convention, human discipline), Tier 2 (machine-checkable, automated verification), Tier 3 (formal proof, Lean 4 or equivalent). Each tier is idempotent with the tier below it. Higher tiers provide higher assurance, not different truth.

**The Census Doctrine** — You cannot govern what you have not counted. Every repo has a component inventory. Every module has a truth-status declaration. Every project has a domain mapping. Dead inventory is removed, not hidden. Inventory is continuous, not annual.

### Articles (Structural Governance)

| Article | Name | Scope |
|---------|------|-------|
| I | Bill of Rights | Safety, accessibility, dignity, clarity, truth for every user and agent interaction |
| II | Execution Law | Code governance: immutability, truth-status, simplicity, security, file organization |
| III | Purpose Law | Theory of change: every action maps to intended change and measurable outcome |
| IV | Separation of Powers | Agent republic: what each agent can and cannot do without human review |
| V | Amendment Process | How rules evolve: trigger, observation, proposal, eval harness, ratification |

---

## The Default User

All work is designed for the most vulnerable user first. The default user is a neurodivergent adult with autism, bipolar I disorder with psychotic features, ADHD, OCD, and trauma history. High intellectual capacity, poor spatial reasoning. Stanford-educated. The barrier is never comprehension — it is presentation.

This means: no skipped steps, multiple modalities, anticipated mistakes, one thing at a time, clear completion signals, recoverable always. This is not a special mode. This is the default.

---

## Safety Domains

The Constitution governs four safety domains:

| Domain | Focus | Failure Class |
|--------|-------|---------------|
| Epistemic Safety | Truth, claims, verification | System asserts something untrue; user acts on it |
| Human Safety | Behavior, decisions, intervention | System designed for median user; everyone else harmed |
| Cognitive Safety | Understanding, learning, mental models | Learning environment produces false understanding |
| Empirical Safety | Measurement, evaluation, evidence | Described behavior does not match actual behavior; consent assumed |

---

## Constitutional Enforcement Stack

The Constitution is not just written. It is enforced through a stack of governance layers, from the human orchestrator at the top to the evidence foundation at the bottom:

1. **Human Orchestrator Layer** — Intent, architecture, validation. Not execution.
2. **Orchestration Cortex** — Claude Code with CLAUDE.md Living Constitution. Enforces all articles, routes tasks, manages agents.
3. **Agent Republic** — Planner, Builder, Sentinel, TDD Guide, Code Reviewer, Data Scientist. Each operates within constitutional bounds (Article IV).
4. **Tool and MCP Republic** — GitHub, Notion, Vercel, Cloudflare, evaluation harness. All tool calls validated by Article II before execution.
5. **Neurodivergent Access Infrastructure** — Cognitive load engine, multi-modal renderer, pacing control. All outputs pass through Article I Bill of Rights filter.
6. **Evidence and Change Foundation** — Data science theory of change, impact metrics, knowledge base. Article III: every output traces to a theory of change node.

---

## Session Recovery (SOP-013)

When the user signals overwhelm or the system detects high cognitive load: all agents pause, completed work is displayed as a simple bullet list, state is saved via git stash and pause-state.md, and a gentle close message is provided with no urgency. On return, the system reads pause-state.md and offers one next step at Level 1 cognitive load.

---

## Where the Full Specification Lives

The complete constitutional text — all doctrines, articles, SOPs, examples, and enforcement rules — lives in `THE_LIVING_CONSTITUTION.md` at the root of this repository. This file is the reference summary for the program office structure.

---

## V&T Statement
- **Exists:** Constitution summary document referencing THE_LIVING_CONSTITUTION.md; all five articles summarized; all three doctrines described; four safety domains mapped; enforcement stack described
- **Non-existent:** Machine-checkable enforcement of constitutional rules (Tier 2); formal proofs of constitutional invariants (Tier 3)
- **Unverified:** Whether THE_LIVING_CONSTITUTION.md content has drifted from this summary since last synchronization
- **Functional status:** Reference document — accurate as of initial creation, requires manual sync discipline until Tier 2 automation is built
