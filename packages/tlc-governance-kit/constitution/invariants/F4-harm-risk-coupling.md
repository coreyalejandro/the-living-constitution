# F4 — Harm-Risk Coupling
## Failure Mode: A System Error in One Domain Creates Direct Harm in Another

**ID:** F4
**Domain:** Human Safety (primary), all domains (secondary)
**Severity:** Critical — violates Article I (Right to Safety) and crosses domain boundaries

---

## Description

Harm-risk coupling occurs when an error in one part of the system propagates into a different safety domain and causes direct harm to a user. The system was designed to handle each domain independently, but the failure path crosses domain boundaries in ways that were not anticipated or governed.

This is the most structurally dangerous failure mode because it means the system's safety architecture has gaps between its domains. A false claim (epistemic failure) that reaches a user making a healthcare decision (human safety failure) is an F4. A phantom completion (empirical failure) in an authorization system (human safety failure) is an F4. The coupling is the danger: errors that would be contained in one domain escape into another.

---

## How It Manifests in AI Systems

**Epistemic-to-Human coupling:** A language model generates a confident false claim (F1) about a medication interaction. The claim reaches a user who is managing their own prescriptions. The epistemic error (wrong information) creates human harm (dangerous drug interaction). The system had no mechanism to flag medical claims for elevated verification.

**Empirical-to-Human coupling:** A deployment agent reports a successful deployment (F2, phantom completion) of an authentication service. The auth service is actually down. Users who attempt to log in are either locked out (denial of service) or, worse, the fallback path allows unauthenticated access (security breach). The empirical error (false completion status) creates human harm (security vulnerability).

**Cognitive-to-Epistemic coupling:** A learning system teaches an incorrect mental model (cognitive safety failure). The user, operating with the false model, generates their own incorrect claims and shares them with others (epistemic failure propagation). The original cognitive error has amplified into a community-level epistemic failure.

**Within the Commonwealth specifically:** ConsentChain's 7-stage action gateway validates agent actions before execution. If the gateway has a phantom completion (F2) on the consent verification stage — reporting consent as obtained when it was not — the downstream action executes without authorization. An empirical failure in ConsentChain creates a human safety violation in whatever system the action targets.

---

## Which TLC Article Prevents It

**Article I, Right to Safety:** "No output may create epistemic, cognitive, human, or empirical harm." This is the constitutional floor. The right does not say "no harm within the same domain" — it says no harm, period. Cross-domain harm is still harm.

**The Four Safety Domains Framework:** By defining four distinct domains with explicit failure classes, the Constitution creates a map of potential coupling paths. Every project maps to one or more domains via `config/projects.ts` and `config/domains.ts`. When a project spans multiple domains, the coupling risk is explicitly visible.

**Article IV, Separation of Powers:** Agent boundaries prevent a single agent from having unchecked authority across multiple domains. The Sentinel agent can raise STOP signals but cannot override other agents. This separation reduces the blast radius of any single agent's failure.

---

## Which SentinelOS Package Enforces It

**Package:** `sentinelos/packages/core`
**Invariant:** I4 — No unvalidated output from one domain may be consumed as trusted input by another domain. Domain boundaries are enforcement boundaries.

When fully operational, the SentinelOS runtime will enforce domain boundary checks. When data flows from one domain's subsystem to another, the sentinel verifies that the data has been validated within its source domain before allowing it to cross. Unvalidated cross-domain data is quarantined and flagged.

**Supporting package:** `sentinelos/packages/sentinel-config`
The sentinel configuration defines which domain each module belongs to and which cross-domain data flows are permitted. Unauthorized cross-domain flows are blocked by default.

**Current enforcement tier:** Tier 1 (convention). Domain mappings exist in `config/projects.ts` and `config/domains.ts`. Cross-domain flow rules are conceptual, not enforced at runtime.

---

## Detection Method

**Tier 1 (Current):** Domain mapping review. When a change touches multiple projects or domains, the reviewer checks: Does this change create a new cross-domain data flow? Is the source data validated before crossing the domain boundary? Does the V&T Statement acknowledge the cross-domain impact?

**Tier 2 (Target):** Automated domain boundary enforcement. Define permitted cross-domain flows in a configuration file. On every build or deployment:
1. Static analysis identifies all data flows between modules.
2. Each flow is checked against the permitted-flows configuration.
3. Unauthorized flows fail the build.
4. Authorized flows are checked for validation at the boundary.

**Tier 3 (Aspiration):** Formal proof that every cross-domain data flow passes through a validation function, and that the validation function's postconditions satisfy the receiving domain's preconditions. No unvalidated data can cross a domain boundary.

---

## Example Scenario

**Context:** UICare's cognitive load engine generates a "safe to proceed" signal for a user interface interaction, which ConsentChain's authorization gateway consumes as an input.

**F4 Failure:** UICare's cognitive load assessment has a bug: it always returns "low cognitive load" for users in dark mode because the color contrast calculation is inverted. ConsentChain receives the "low cognitive load" signal and proceeds with a complex multi-step authorization flow. The user, who is actually experiencing high cognitive load, is overwhelmed by the authorization steps and clicks "Allow All" to escape the flow. A cognitive safety failure in UICare propagated through ConsentChain into a human safety failure (uninformed consent).

**F4 Prevention:** The domain boundary between UICare (human safety domain) and ConsentChain (empirical safety domain) requires validation. ConsentChain does not trust UICare's cognitive load signal directly. Instead, ConsentChain runs its own simplified cognitive load heuristic as a boundary check: if the user has been in the authorization flow for less than 3 seconds, flag as "rushed consent" regardless of UICare's signal. The boundary check catches the discrepancy. The authorization flow pauses and presents a simplified single-step consent option.

**Downstream impact of prevention:** The user is not overwhelmed. The consent is informed. The authorization is valid. The bug in UICare's dark mode calculation is logged for fix, but it did not cause downstream harm because the domain boundary enforced validation.

---

## Related Failure Modes

- **F1 (Confident False Claims):** F4 often starts with an F1 in the source domain. The false claim propagates across domains.
- **F2 (Phantom Completion):** F4 often starts with an F2 in a critical subsystem. The phantom completion creates a false foundation for downstream actions.
- **All failure modes can become F4** when they escape their domain of origin. F4 is the amplification failure mode.

---

## V&T Statement
- **Exists:** F4 failure mode definition with description, cross-domain manifestation examples, article mapping, SentinelOS invariant reference, detection methods across three tiers, example scenario with domain boundary prevention
- **Non-existent:** Tier 2 automated domain boundary enforcement; Tier 3 formal cross-domain validation proofs; runtime sentinel domain-crossing checks; permitted-flows configuration
- **Unverified:** Whether UICare and ConsentChain have any actual cross-domain data flows currently; whether config/projects.ts domain mappings are complete for all cross-domain risks
- **Functional status:** F4 failure mode is fully specified — prevention relies on Tier 1 convention (domain mapping review + V&T cross-domain acknowledgment) until automated boundary enforcement is built
