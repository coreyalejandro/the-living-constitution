# ARTICLE VII — FAILURE OPERATIONS LAW

**Status:** Ratified  
**Authority:** THE_LIVING_CONSTITUTION.md — Article VII  
**Load when:** Building error handling, failure states, or recovery flows  
**Tracked here:** docs/governance/failure-operations-contract.md  

---

## The Law

Every failure must be governable. Every failure must be recoverable. No failure state may leave the user stranded.

This article governs how the system handles errors, failures, unexpected states, and recovery paths. It applies to code, to user-facing messages, and to agent behavior.

---

## The Four Failure Classes

From the Four Safety Domains in THE_LIVING_CONSTITUTION.md:

| Class | What Failed | Governing Principle |
|---|---|---|
| **Epistemic failure** | System asserts something untrue | Calibrated Truth Doctrine |
| **Human safety failure** | System designed for median user; vulnerable user harmed | Default User Doctrine + Article VI |
| **Cognitive failure** | Output produces false understanding | V&T requirement + no fluent wrong answers |
| **Empirical failure** | Described behavior differs from actual behavior | Evidence requirement + regression gating |

Every error handling design must identify which class of failure it is governing.

---

## Hard Rules for Error Handling

### 1. Never Swallow Exceptions

Caught exceptions must be logged and surfaced with enough context for a human to diagnose them. Silencing an exception to make a system appear to work is a governance violation. It is also a safety hazard for the Default User, who may interpret silence as success.

### 2. User-Facing Errors Must Be Actionable

Every error message shown to a user must include:
- What happened (plain language, not error codes alone)
- Whether the user caused it or the system caused it
- What to do next (specific, not "try again")
- How to recover (exact steps, not general advice)

"Something went wrong" is not a compliant error message.

### 3. Recovery Path = First-Class Instruction

Recovery paths are not footnotes. They are not appended to success-path documentation as an afterthought. They are documented with the same completeness and priority as the success path.

For every user-facing action that can fail:
- Document the failure condition
- Document the recovery steps
- Document what a successful recovery looks like
- Confirm the system returns to a known-good state

### 4. Fail Closed by Default

When in doubt about a system state, the system must fail closed — halt, preserve current state, and surface the uncertainty — rather than proceeding into an unknown state.

Proceeding despite uncertainty is how silent failures become compounding failures.

### 5. No Partial Completion Without Rollback

Any multi-step operation that fails mid-sequence must either:
- Complete cleanly from the failure point (idempotent continuation), or
- Roll back completely to the pre-operation state

Leaving the system in a half-applied state with no documented recovery is a failure operations violation.

### 6. Agent Failure Requires Human Escalation

When an agent encounters a halt condition — any state it cannot resolve within its authorized scope — it must:
1. Stop immediately
2. Preserve current state (git stash, state file, pause-state.md)
3. Surface the failure with exact context to the human operator
4. Provide an explicit recovery instruction
5. Not attempt to work around the halt condition autonomously

### 7. BREAK_GLASS Protocol

When two invariants conflict, or when the correct action is genuinely ambiguous, the agent must:
1. Stop the current action
2. Document the conflict in /artifacts/case-law/ as BREAK_GLASS_[DATE]_[DESCRIPTION].md
3. State which invariants are in tension and why
4. Surface to the human operator — do not resolve silently

These BREAK_GLASS artifacts are primary research data. They are not embarrassments to be avoided. They are the empirical record of the system's judgment under pressure.

---

## Failure States and Labels

Every failure state visible to the user must carry one of these labels:

| Label | Meaning | User Action Required |
|---|---|---|
| `recoverable` | System can return to good state; recovery steps follow | Follow recovery steps |
| `partial` | Some work completed; remainder not attempted | Review what succeeded; decide whether to continue |
| `blocked` | Proceeding requires human decision | Read the blocker description; make the decision |
| `rollback_available` | Clean rollback to prior state is available | Execute rollback command (exact command provided) |
| `data_loss_risk` | Recovery may not preserve all state | Read carefully before proceeding |

No failure state may be unlabeled. An unlabeled failure is an invisible failure.

---

## Recovery Documentation Requirements

Every recovery procedure documented in this repo must include:
- Exact commands, not paraphrased steps
- Expected output for each step (what success looks like)
- Expected output for each failure mode within recovery (what to do if recovery itself fails)
- Estimated time (so the Default User can hold a realistic expectation)
- Confirmation gate at the end: "If you see X, recovery succeeded. If you see Y, escalate."

---

## Relationship to Session Recovery Protocol (SOP-013)

SOP-013 governs cognitive overwhelm and executive function crashes for the Default User. This article governs technical failure states. They are complementary.

If a technical failure occurs during a session recovery, SOP-013 takes precedence: pause first, preserve state, then address the technical failure after the human is stable.

---

## Amendment Process

Any modification to the failure class definitions or recovery documentation requirements must demonstrate that the proposed change does not reduce the system's ability to keep the Default User informed and in control during a failure state.

---

**V&T**  
EXISTS: This article document.  
VERIFIED AGAINST: ~/.claude/CLAUDE.md Article II (Error Handling clause), CLAUDE.md SOP-013, CGL AGENTS.md I6 (Fail Closed).  
NOT CLAIMED: All existing error handling in TLC codebases has been audited against this article.  
FUNCTIONAL STATUS: Ratified governance document. Loaded on demand when building error handling or failure states.
