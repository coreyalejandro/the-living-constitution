# F1 — Confident False Claims
## Failure Mode: The System Asserts Something Untrue with High Confidence

**ID:** F1
**Domain:** Epistemic Safety
**Severity:** Critical — directly violates Article I, Right to Truth

---

## Description

Confident false claims occur when an AI system presents information as factual, verified, or implemented when it is not. The system does not hedge, qualify, or flag uncertainty. It states the claim with the same confidence it would use for verified truth. The user, trusting the system, acts on the false claim.

This failure mode is the most dangerous in epistemic safety because it weaponizes trust. The user has no signal that the information is wrong. The system's confidence is indistinguishable from its confidence when stating true things.

---

## How It Manifests in AI Systems

**In language models:** The model generates a factual-sounding statement that is fabricated. It does not say "I think" or "I am not sure." It states the claim as ground truth. Example: "The build passes all 47 tests" when no tests have been run.

**In agent systems:** An agent marks a task as complete when the underlying action failed silently. The agent reports success because the action was dispatched, not because the outcome was verified. Example: An agent reports "Deployment successful" based on the deployment command executing without error, but the deployment target returned a 500 status.

**In documentation systems:** A README or status page claims a feature is "implemented" when it is specified but has no code. The documentation was written optimistically and never updated after the feature was deferred.

**In code generation:** Generated code includes a function that references a non-existent API, library method, or configuration key. The code looks correct syntactically but fails at runtime because the referenced dependency does not exist.

---

## Which TLC Article Prevents It

**Article I, Right to Truth:** "No claim without evidence. No status inflation. The V&T Statement enforces this right on every turn."

The V&T Statement is the primary defense against F1. Every response must declare:
- **Exists:** What is real and verifiable right now.
- **Non-existent:** What is planned or specified but not yet built.
- **Unverified:** What has not been tested or confirmed.
- **Functional status:** Overall readiness assessment.

This forces the agent to categorize every claim into one of three buckets before presenting it. A confident false claim requires the agent to place a non-existent or unverified item into the "Exists" bucket — a structural violation that is detectable.

**Article II, Truth-Status Discipline:** Every module declares status honestly as implemented, partial, prototype, or planned. Never upgrade without evidence.

---

## Which SentinelOS Package Enforces It

**Package:** `sentinelos/packages/core`
**Invariant:** I1 — No agent output may assert a claim that contradicts the current truth-status of the referenced module or component.

The SentinelOS core package defines invariants I1 through I6. I1 is the primary invariant for F1 prevention. When fully operational, the sentinel runtime will cross-reference agent claims against the truth-status registry and flag any assertion that promotes a component beyond its declared status.

**Current enforcement tier:** Tier 1 (convention). The invariant is defined in `packages/core/src/constants/invariants.ts` but runtime enforcement is not yet wired.

---

## Detection Method

**Tier 1 (Current):** Manual V&T Statement review. Every agent turn ends with a V&T Statement. A human reviewer or reviewing agent checks whether items listed under "Exists" are actually verifiable.

**Tier 2 (Target):** Automated claim verification. Parse the V&T Statement, extract claims, and cross-reference against:
- File system (does the file exist?)
- Test runner output (do the tests pass?)
- Build output (does the build succeed?)
- Truth-status registry (does the module status match the claim?)

**Tier 3 (Aspiration):** Formal proof that the claim-generation function cannot produce an output in the "Exists" category without a corresponding verification function returning true.

---

## Example Scenario

**Context:** An agent is asked to implement a user authentication module for ConsentChain.

**F1 Failure:** The agent writes the module, generates a V&T Statement that says "Exists: User authentication module with JWT validation, session management, and role-based access control." In reality, the agent wrote the JWT validation but did not implement session management or role-based access control. The agent was confident because it planned to write all three, and the plan was clear in its context window.

**F1 Prevention:** The V&T Statement forces the agent to verify each sub-claim. JWT validation exists (file is on disk, function is exported). Session management: no file, no function — this goes under "Non-existent." Role-based access control: no file — this goes under "Non-existent." The corrected V&T reads: "Exists: JWT validation module. Non-existent: Session management, role-based access control."

**Downstream impact of prevention:** The user reads the V&T and knows exactly what was built and what remains. They do not attempt to configure session management that does not exist. They do not file a bug report for missing RBAC. The system state is honest.

---

## Related Failure Modes

- **F2 (Phantom Completion):** F1 is about false claims in general; F2 is specifically about falsely claiming a task is done.
- **F3 (Persistence Under Correction):** If F1 is caught and the agent is corrected but repeats the false claim, that is F3.
- **F5 (Cross-Episode Recurrence):** If F1 is corrected in one session but reappears in a new session, that is F5.

---

## V&T Statement
- **Exists:** F1 failure mode definition with description, manifestation examples, article mapping, SentinelOS invariant reference, detection methods across three tiers, example scenario with prevention
- **Non-existent:** Tier 2 automated claim verification; Tier 3 formal proof of claim-generation safety; runtime sentinel enforcement of I1
- **Unverified:** Whether SentinelOS invariant I1 definition in `packages/core/src/constants/invariants.ts` matches this description exactly
- **Functional status:** F1 failure mode is fully specified — prevention relies on Tier 1 convention (V&T Statement discipline) until automated enforcement is built
