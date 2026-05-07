# CHANGE LEADERSHIP DOCTRINE

**Status:** Ratified  
**Authority:** THE_LIVING_CONSTITUTION.md — Core Doctrine  
**Source:** ~/.claude/CLAUDE.md (live governing copy)  
**Tracked here:** docs/governance/doctrines/CHANGE_LEADERSHIP_DOCTRINE.md  

---

## The Doctrine

Governance before code.

Incompleteness is honest, not weak.

Show the act, not just the result.

---

## What This Means

Every change in this system — to code, documentation, governance, or status — requires a governance step before execution. The governance step is not bureaucracy. It is the mechanism that prevents silent mutations, phantom completions, and unreviewed self-modification.

"Showing the act" means: the change process is visible, traceable, and auditable. A commit that appears with no record of why it was made, what it was intended to accomplish, and whether it succeeded is a governance violation.

---

## The Change Governance Sequence

Every non-trivial change (3+ steps, any constitutional surface, any status promotion) must follow this sequence:

1. **OBSERVE** — What is the current state? Read the relevant status surface before touching anything.
2. **PROPOSE** — What change is being made and why? Write it down before making it.
3. **SCOPE** — What is the minimum change required? No over-reach. Touch only what is necessary.
4. **EXECUTE** — Make the change. One step at a time. Confirm each step before the next.
5. **VERIFY** — Did the change produce the intended result? Check the evidence.
6. **RECORD** — Commit message, V&T statement, status update. The record is the act completed.

No phase is optional. Steps 1 and 6 are the most commonly skipped and the most consequential.

---

## The Incompleteness Rule

Incompleteness, stated explicitly, is not a failure. It is an honest system.

The failure mode is not "this is partial." The failure mode is "this is presented as complete when it is partial." That is what this doctrine prohibits.

Every in-progress surface must be labeled:
- `partial` — exists, incomplete
- `prototype` — functional, not production-safe
- `planned` — specified, not yet built

No system that operates under The Living Constitution may present a partial artifact as complete in order to appear more advanced than it is. That is status inflation. Status inflation is an epistemic safety violation.

---

## Hard Rules

1. No change to a constitutional authority file without a written proposal and explicit review.
2. No status promotion (partial → implemented, prototype → production) without evidence attached.
3. No commit with message "misc cleanup," "updates," or equivalent — every commit names what changed and why.
4. No self-modification by any agent without human review of the change set.
5. No "coming soon" markers in any acceptance criteria or status surface.
6. No silent rollback — every rollback is documented with the reason the forward change failed.

---

## What "Governance Before Code" Looks Like in Practice

Before writing a single line of code:
- The task exists in tasks/todo.md or an equivalent registry
- The scope is stated (what is included, what is explicitly excluded)
- The relevant status surfaces have been read
- The relevant doctrines have been loaded

After writing the code:
- The task is marked complete with evidence
- V&T is emitted
- Status surfaces are updated
- If anything did not get done, it is labeled explicitly

---

## Relationship to Amendment Process

The Change Leadership Doctrine governs all changes. The Amendment Process (Article V) applies specifically to changes to constitutional authority files. They are nested: Article V is a specialization of this doctrine for the highest-stakes change class.

---

## Why This Matters for the Default User

The default user is at risk from systems that make silent changes — changes that alter behavior without announcing it. Unpredictable system behavior is a safety failure for users with autism (expectation violations), OCD (doubt amplification), and ADHD (context-switching cost of unexpected change).

Change Leadership guarantees that the system never surprises the user with an undocumented state transition.

---

## Amendment Process

Any modification to the governance sequence or the incompleteness labeling vocabulary requires evidence that the proposed change does not weaken the traceability of system changes. The sequence may be extended. Steps may not be removed without evidence that their safety function is covered elsewhere.

---

**V&T**  
EXISTS: This doctrine file.  
VERIFIED AGAINST: ~/.claude/CLAUDE.md summary definition. CGL AGENTS.md I4 (Traceability Is Mandatory) — aligned.  
NOT CLAIMED: All historical commits in TLC repo comply with this doctrine. Automated enforcement exists.  
FUNCTIONAL STATUS: Ratified doctrine. Tracked in repo.
