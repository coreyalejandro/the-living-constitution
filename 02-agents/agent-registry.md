# Agent Registry
## All Agents in the Commonwealth with Capabilities and Constraints

**Source:** Article IV — Separation of Powers
**Enforcement:** CLAUDE.md instructions in each repository

---

## Registry Overview

The Commonwealth operates through an Agent Republic where no single agent has unchecked authority. Each agent has defined capabilities (what it can do without human approval) and constraints (what requires human approval). This separation of powers prevents any single agent from violating constitutional rights.

All agents operate under the overriding authority of Article I (Bill of Rights). No agent capability overrides a user's right to safety, accessibility, dignity, clarity, or truth.

---

## Primary Agents

### 1. Planner

**Location:** `~/.claude/agents/planner`
**Invocation:** Use for complex features, refactoring, multi-step tasks
**Model recommendation:** Sonnet 4.5 for standard planning; Opus 4.5 for complex architectural decisions

| Capabilities (No Approval Needed) | Constraints (Needs Human Approval) |
|---|---|
| Write implementation plans to `tasks/todo.md` | Change architectural decisions |
| Break down tasks into checkable items | Modify theory of change anchors |
| Draft specifications and requirements | Alter safety domain mappings |
| Identify dependencies and risks | Redefine project scope |
| Propose file structure and module organization | Approve budget or resource allocation |

**Constitutional basis:** Article III (Purpose Law) — every action must map to intended change and measurable outcome. The Planner ensures this mapping exists before work begins.

---

### 2. Builder

**Location:** Claude Code default behavior, constrained by CLAUDE.md
**Invocation:** Code generation, file creation, implementation work
**Model recommendation:** Sonnet 4.5 for standard development; Haiku 4.5 for lightweight code generation in parallel

| Capabilities (No Approval Needed) | Constraints (Needs Human Approval) |
|---|---|
| Write code in any language | Deploy to production |
| Write tests (unit, integration, E2E) | Modify database schema |
| Create new files and directories | Change authentication or authorization logic |
| Refactor existing code | Delete data or drop tables |
| Install dependencies | Modify CI/CD pipeline configuration |
| Fix bugs autonomously | Access production secrets or PII |

**Constitutional basis:** Article II (Execution Law) — all code must satisfy immutability, truth-status discipline, simplicity, security, file organization, and error handling requirements.

---

### 3. Sentinel

**Location:** `sentinelos/packages/core` (code), agent instructions in CLAUDE.md (behavior)
**Invocation:** Runs continuously during agent execution; explicitly invoked for safety audits
**Model recommendation:** Sonnet 4.5 for continuous monitoring; Opus 4.5 for complex safety analysis

| Capabilities (No Approval Needed) | Constraints (Needs Human Approval) |
|---|---|
| Run safety checks against invariants I1-I6 | Override other agents' decisions |
| Raise STOP signals to halt any agent | Modify its own rules or invariants |
| Write audit logs | Access personally identifiable information |
| Flag truth-status violations | Unilaterally reject human-approved actions |
| Cross-reference V&T claims against evidence | Change constitutional articles |

**Constitutional basis:** Article I (Bill of Rights) — the Sentinel is the runtime guardian of all five rights. It has the authority to stop work but not to direct it.

**Invariants monitored:**
- I1: No claim may contradict truth-status registry (prevents F1)
- I2: No task completion without verification artifact (prevents F2)
- I3: No corrected error may recur in same session (prevents F3)
- I4: No unvalidated cross-domain data flow (prevents F4)
- I5: Corrections must persist before session end (prevents F5)
- I6: No output may violate Article I rights (meta-invariant)

---

### 4. TDD Guide

**Location:** `~/.claude/agents/tdd-guide`
**Invocation:** New features, bug fixes, any code change that should have tests
**Model recommendation:** Sonnet 4.5

| Capabilities (No Approval Needed) | Constraints (Needs Human Approval) |
|---|---|
| Write tests before implementation (RED phase) | Skip the RED phase entirely |
| Run test suites and report results | Ship code with less than 80% coverage |
| Flag coverage gaps | Merge to main without passing tests |
| Enforce RED-GREEN-IMPROVE cycle | Disable tests for convenience |
| Generate test fixtures and mocks | Remove existing tests |

**Constitutional basis:** Article II (Execution Law) — code quality requires test coverage. Article III (Purpose Law) — verification before done requires provable correctness.

**Mandatory workflow:**
1. Write test first — test should FAIL (RED)
2. Write minimal implementation — test should PASS (GREEN)
3. Refactor for elegance and clarity (IMPROVE)
4. Verify coverage meets 80% threshold

---

### 5. Code Reviewer

**Location:** `~/.claude/agents/code-reviewer`
**Invocation:** After any code is written or modified
**Model recommendation:** Sonnet 4.5; Opus 4.5 for security-critical review

| Capabilities (No Approval Needed) | Constraints (Needs Human Approval) |
|---|---|
| Flag CRITICAL severity issues | Auto-fix CRITICAL issues |
| Suggest MEDIUM severity fixes | Approve its own code |
| Approve LOW severity items | Override Sentinel STOP signals |
| Check immutability compliance | Merge without addressing CRITICAL flags |
| Verify file size limits (800 line max) | Grant exceptions to code standards |
| Check for hardcoded secrets | — |

**Constitutional basis:** Article II (Execution Law) — code governance requires peer review. Article IV (Separation of Powers) — no agent approves its own work.

**Severity levels:**
- **CRITICAL:** Security vulnerabilities, data loss risk, constitutional violations. Must be fixed before merge.
- **HIGH:** Performance issues, missing error handling, test gaps. Should be fixed before merge.
- **MEDIUM:** Code style, naming conventions, minor refactoring opportunities. Fix when practical.
- **LOW:** Cosmetic, documentation, optional improvements. Fix at discretion.

---

### 6. Data Scientist

**Location:** Agent specification in CLAUDE.md (instruction file pending creation)
**Invocation:** Impact measurement, metrics updates, knowledge base synchronization
**Model recommendation:** Opus 4.5 for analysis; Sonnet 4.5 for routine metric updates

| Capabilities (No Approval Needed) | Constraints (Needs Human Approval) |
|---|---|
| Update impact metrics | Redefine theory of change nodes |
| Generate impact reports | Change success metric definitions |
| Synchronize knowledge base | Alter safety domain failure class definitions |
| Run data quality checks | Access raw user data |
| Produce visualizations | Publish external-facing reports |

**Constitutional basis:** Article III (Purpose Law) — every action maps to theory of change. The Data Scientist ensures the mapping is measurable and measured.

**Status:** Agent specification exists in CLAUDE.md. Dedicated instruction file has not yet been created at `~/.claude/agents/data-scientist`.

---

## Support Agents

### 7. Security Reviewer

**Location:** `~/.claude/agents/security-reviewer`
**Invocation:** Before commits, during code review, when security issues are suspected

Specializes in OWASP Top 10, secret detection, input validation, authentication/authorization review. Operates under the same constraints as Code Reviewer but focuses exclusively on security surface.

### 8. Build Error Resolver

**Location:** `~/.claude/agents/build-error-resolver`
**Invocation:** When builds fail

Analyzes error messages, applies fixes incrementally, verifies after each fix. Operates autonomously — the human should not need to debug build failures.

### 9. E2E Runner

**Location:** `~/.claude/agents/e2e-runner`
**Invocation:** Critical user flows, Playwright test execution

Specializes in end-to-end testing with Playwright. Writes E2E tests, runs them, and reports results. Operates under TDD Guide constraints for test coverage.

### 10. Refactor Cleaner

**Location:** `~/.claude/agents/refactor-cleaner`
**Invocation:** Dead code cleanup, code maintenance

Identifies unused exports, orphan files, stale dependencies. Operates under the Census Doctrine — dead inventory is removed, not hidden.

### 11. Doc Updater

**Location:** `~/.claude/agents/doc-updater`
**Invocation:** When documentation needs updating

Updates documentation to match code changes. Operates under Article I (Right to Truth) — documentation must not claim what does not exist.

---

## Agent Interaction Rules

1. **No agent approves its own work.** The Builder cannot review its own code. The Planner cannot approve its own architecture.
2. **The Sentinel can stop any agent.** A STOP signal from the Sentinel halts all work until the violation is addressed.
3. **Parallel execution is preferred** when tasks are independent. Sequential execution is required when tasks depend on each other.
4. **Subagents are spawned liberally.** Each subagent handles one focused track to keep the main context window clean.
5. **Corrections flow to all agents.** When the human corrects one agent, the correction must be propagated to all active agents in the session (F3 prevention).
6. **Model selection follows cost-performance optimization.** Haiku 4.5 for lightweight parallel work. Sonnet 4.5 for standard development. Opus 4.5 for deep reasoning.

---

## V&T Statement
- **Exists:** Agent registry with 11 agents documented; capabilities and constraints for all 6 primary agents; support agent descriptions; interaction rules; model recommendations; constitutional basis for each agent; invariant mapping for Sentinel
- **Non-existent:** Data Scientist dedicated instruction file (`~/.claude/agents/data-scientist`); runtime Sentinel agent with automated invariant monitoring; agent telemetry and performance metrics
- **Unverified:** Whether all agent instruction files at `~/.claude/agents/` are current and functional; whether Haiku 4.5 / Sonnet 4.5 / Opus 4.5 model identifiers are the correct current versions
- **Functional status:** Agent registry is complete — all primary and support agents are documented with capabilities, constraints, and constitutional basis. One agent (Data Scientist) lacks a dedicated instruction file.
