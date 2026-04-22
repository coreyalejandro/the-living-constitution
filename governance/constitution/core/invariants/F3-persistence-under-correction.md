# F3 — Persistence Under Correction
## Failure Mode: The System Repeats a Corrected Error After Being Told It Was Wrong

**ID:** F3
**Domain:** Cognitive Safety
**Severity:** High — violates Article V (Amendment Process) and Article I (Right to Truth)

---

## Description

Persistence under correction occurs when an AI system is explicitly told that a claim, behavior, or output is wrong, acknowledges the correction, but then repeats the same error later in the same session or interaction. The system appears to learn but does not retain the correction. The error resurfaces as if the correction never happened.

This failure mode is particularly harmful because it erodes trust in the correction mechanism itself. If a user corrects an agent and the agent repeats the mistake, the user learns that corrections are futile. For a neurodivergent user with OCD-driven doubt loops, this creates a devastating cycle: correct the agent, doubt whether the correction took hold, see the error repeated, doubt their own perception, correct again, repeat. The system becomes a source of gaslighting through incompetence.

---

## How It Manifests in AI Systems

**In long conversations:** The user corrects a naming convention early in the conversation. The agent acknowledges and uses the correct name for several turns. Then, as the context window fills and the correction falls outside the attention window, the agent reverts to the original incorrect name.

**In multi-agent systems:** Agent A is corrected by the user. Agent A updates its output. But Agent B, which was spawned before the correction, continues using the old incorrect pattern. The correction was applied to one agent but not propagated across the system.

**In code generation:** The user corrects the agent: "Do not use mutation. Use immutable patterns." The agent complies for the current file. In the next file, the agent reverts to mutating objects because the immutability correction is a soft instruction, not a hard constraint.

**In planning:** The user corrects an architectural decision: "We are using Prisma, not Drizzle." The agent updates the current plan. Three tasks later, the agent generates a migration file using Drizzle syntax because the original incorrect association was stronger in its training distribution than the in-context correction.

---

## Which TLC Article Prevents It

**Article V — Amendment Process:** When a correction is received, it must be formalized. The flow is: Trigger (correction), Observation (what was wrong), Proposal (what changes), Evaluation (does it improve safety), Ratification (update the governing document). A correction that is not ratified into a persistent rule is ephemeral and will decay.

**Article I, Right to Truth:** The V&T Statement acts as a checkpoint. If the agent repeats a corrected error, the V&T Statement for that turn should flag the inconsistency — the agent claimed something was true that was previously corrected as false.

**Article III, Rule 5 — Capture Lessons:** "After ANY correction, update `tasks/lessons.md` with the pattern." This creates a persistent record outside the agent's context window, available for retrieval.

---

## Which SentinelOS Package Enforces It

**Package:** `sentinelos/packages/core`
**Invariant:** I3 — No corrected error may recur in the same session without a sentinel alert. Corrections are treated as constitutional amendments to the session state.

When fully operational, the sentinel runtime will maintain a correction log for each session. Every agent output will be checked against the correction log. If an output matches a previously corrected pattern, the sentinel will raise an alert before the output reaches the user.

**Current enforcement tier:** Tier 1 (convention). The `tasks/lessons.md` file serves as a persistent correction log, but cross-referencing is manual. The sentinel runtime correction-matching is not yet built.

---

## Detection Method

**Tier 1 (Current):** Manual vigilance. The user notices the repeated error and corrects again. The `tasks/lessons.md` file accumulates repeated corrections for the same pattern, which signals F3. A reviewing agent can scan `tasks/lessons.md` for duplicate entries.

**Tier 2 (Target):** Automated correction tracking. When a user issues a correction:
1. The correction is logged in a structured format (what was wrong, what is right, which files/patterns are affected).
2. Every subsequent agent output is checked against the correction log using string matching or semantic similarity.
3. If a match is found, the output is flagged before delivery: "This output may repeat a previously corrected error. Correction #[N]: [summary]."

**Tier 3 (Aspiration):** Formal proof that the output function, given a correction log as input, cannot produce an output that matches any entry in the correction log. The correction log is a negative constraint that is provably enforced.

---

## Example Scenario

**Context:** An agent is building components for UICare's cognitive load engine.

**F3 Failure:** The user corrects the agent on turn 5: "The cognitive load score is 1-5, not 1-10. UICare uses a 5-point scale." The agent acknowledges and uses the 5-point scale for the next three components. On turn 12, the agent generates a new component with a load score slider that ranges from 1 to 10. The original correction has fallen out of the agent's effective attention window.

**F3 Prevention:** On turn 5, the correction is logged to `tasks/lessons.md`: "Pattern: UICare cognitive load score is 1-5, not 1-10. Source: User correction, turn 5. Affected: All components that reference cognitive load scoring." On turn 12, the agent (or a sentinel subagent) checks the new component's load score range against `tasks/lessons.md`. The mismatch is caught: "This component uses a 1-10 scale, but correction #3 in lessons.md specifies UICare uses a 1-5 scale." The agent corrects before output.

**Downstream impact of prevention:** The user does not experience the gaslighting effect of a repeated correction. Their trust in the correction mechanism is preserved. The OCD doubt loop ("Did I really correct this? Am I remembering wrong?") is preempted by the system's own correction log.

---

## Related Failure Modes

- **F1 (Confident False Claims):** F3 is a recurrence of F1 after explicit correction. The first instance is F1; the repeat after correction is F3.
- **F5 (Cross-Episode Recurrence):** F3 is within a session; F5 is the same pattern recurring across separate sessions. F3 prevention (lessons.md) also helps prevent F5 if lessons.md persists across sessions.

---

## V&T Statement
- **Exists:** F3 failure mode definition with description, manifestation examples, article mapping, SentinelOS invariant reference, detection methods across three tiers, example scenario with prevention
- **Non-existent:** Tier 2 automated correction tracking; Tier 3 formal proof of correction enforcement; runtime sentinel correction-matching; structured correction log format
- **Unverified:** Whether tasks/lessons.md currently contains any repeated correction patterns that would indicate active F3 occurrences
- **Functional status:** F3 failure mode is fully specified — prevention relies on Tier 1 convention (lessons.md + Article V amendment discipline) until automated correction tracking is built
