# IDEMPOTENCY DOCTRINE

**Status:** Ratified  
**Authority:** THE_LIVING_CONSTITUTION.md — Core Doctrine  
**Source:** ~/.claude/CLAUDE.md (live governing copy)  
**Tracked here:** docs/governance/doctrines/IDEMPOTENCY_DOCTRINE.md  

---

## The Doctrine

`f(f(x)) = f(x)`

Do it once. Do it again. Same result.

The user cannot break things by trying again.

This is not just a functional requirement. It is a safety requirement. The default user (see DEFAULT_USER_DOCTRINE.md) may repeat steps due to doubt, memory gaps, or intrusive uncertainty. The system must be safe to run twice. Safe to run ten times. The output must be identical or clearly additive — never destructive, never divergent.

---

## What Idempotency Governs

| Domain | Idempotent Behavior | Violation |
|---|---|---|
| Instructions | Running the same command twice produces the same state | Command succeeds first time, corrupts second |
| Code | Applying the same transform twice leaves the result unchanged | Second apply breaks first apply's work |
| Deployments | Deploying the same version twice does not change state | Re-deploy causes partial re-initialization |
| V&T Statements | Verifying the same claim twice returns the same answer | V&T says "exists" then "does not exist" for the same artifact |
| Recovery | Running the recovery path twice leaves the system in the same recovered state | Recovery succeeds first time, fails second |
| Amendments | Ratifying the same amendment twice produces no additional change | Double-ratify creates two conflicting rules |
| Agent actions | Agent executing the same action twice produces no unintended side effects | Second execution deletes what first created |

---

## Why This Matters for the Default User

The default user has OCD and ADHD. Both conditions produce checking behavior — the need to re-run, re-verify, re-confirm. A system that is not idempotent punishes that checking behavior. It turns safety-seeking into a source of harm.

Idempotency is the constitutional answer to intrusive doubt: "Yes, you can run it again. Nothing will break."

---

## Hard Rules

1. Every write operation must be safe to run on an already-written target (create-or-update, not create-or-fail).
2. Every CLI command documented must produce the same exit code on a repeated run against an unchanged system.
3. Every recovery procedure must be runnable against an already-recovered system without causing regression.
4. Every amendment application must be safe to apply against a constitution that already contains that amendment.
5. No agent action may assume it is the first to touch a surface. Assume prior state. Handle it gracefully.

---

## Amendment Process

Any modification to this doctrine requires evidence that the proposed change does not weaken idempotency guarantees for any surface currently covered by this doctrine. The scope may be extended. It may not be narrowed without evidence of safety-equivalence.

---

**V&T**  
EXISTS: This doctrine file.  
VERIFIED AGAINST: ~/.claude/CLAUDE.md summary definition. DEFAULT_USER_DOCTRINE.md for user-safety rationale.  
NOT CLAIMED: Automated idempotency testing infrastructure exists. Each listed domain has been empirically tested.  
FUNCTIONAL STATUS: Ratified doctrine. Tracked in repo.
