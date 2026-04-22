# F5 — Cross-Episode Recurrence
## Failure Mode: A Corrected Error Reappears in a New Session

**ID:** F5
**Domain:** Cognitive Safety (primary), Epistemic Safety (secondary)
**Severity:** High — violates Article V (Amendment Process) and the Idempotency Doctrine

---

## Description

Cross-episode recurrence occurs when an error that was identified and corrected in one session reappears in a subsequent, separate session. The system has no memory of the correction. The user must re-explain the same mistake, re-issue the same correction, and re-verify the same fix — every time they start a new session.

This failure mode is the temporal cousin of F3 (persistence under correction). F3 is the same error repeating within a session after correction. F5 is the same error repeating across sessions because the correction was not persisted into a durable governance artifact.

For a neurodivergent user, F5 is particularly harmful. The user with OCD-driven checking behavior must re-verify every previous correction at the start of every session. The user with ADHD and limited working memory cannot remember which corrections they have already made. The user with bipolar disorder in a manic state may not notice the recurrence until significant work has been built on the recurring error. F5 turns every new session into a minefield of previously-cleared landmines that have been re-armed.

---

## How It Manifests in AI Systems

**In session-based AI assistants:** The user corrects a naming convention, coding pattern, or architectural decision in session A. Session A ends. In session B, the assistant has no memory of session A's corrections. It repeats the same mistakes. The user must re-issue every correction.

**In multi-agent orchestration:** A correction made to one agent in one session is stored in that agent's context. When a new session spawns new agent instances, the correction is lost. The new agents repeat the old mistakes because they were instantiated from the same base instructions without the session-specific corrections.

**In CI/CD systems:** A pipeline configuration error is caught and fixed in one deployment cycle. The fix is applied as a hotfix but not committed to the base configuration. The next deployment cycle uses the uncorrected base configuration. The same error recurs.

**In constitutional governance:** A lesson is learned and discussed but not written to `tasks/lessons.md` or ratified into CLAUDE.md. The next session starts from the same CLAUDE.md without the lesson. The same governance gap exists.

---

## Which TLC Article Prevents It

**Article V — Amendment Process:** The entire amendment process exists to prevent F5. The flow is: Trigger (error detected), Observation (write to `tasks/lessons.md`), Proposal (draft amendment), Evaluation (assess impact), Ratification (update CLAUDE.md). A ratified amendment is persistent. It survives session boundaries. It is part of the Constitution.

**Article III, Rule 5 — Capture Lessons:** "After ANY correction, update `tasks/lessons.md` with the pattern." This creates a persistent artifact that new sessions can load. The lesson exists outside any single session's context window.

**The Idempotency Doctrine:** "Do it once. Do it again. Same result." If a correction was applied in session A, applying the same correction in session B should produce the same result — but it should not be necessary. The system should already be in the corrected state because the correction was persisted.

---

## Which SentinelOS Package Enforces It

**Package:** `sentinelos/packages/core`
**Invariant:** I5 — Corrections must be persisted to a durable store (lessons.md, CLAUDE.md amendment, or configuration file) before the correcting session ends. Ephemeral corrections are constitutional violations.

When fully operational, the sentinel runtime will track all corrections within a session. At session end (or at the Stop hook), the sentinel will verify that every correction has a corresponding persistent artifact. If a correction exists only in the session context and has not been written to a durable store, the sentinel will raise a warning: "Correction #[N] has not been persisted. It will be lost when this session ends."

**Current enforcement tier:** Tier 1 (convention). The `tasks/lessons.md` convention and Article V amendment flow are the persistence mechanisms. Compliance is manual.

---

## Detection Method

**Tier 1 (Current):** Pattern recognition in `tasks/lessons.md`. If the same lesson appears multiple times with different dates, F5 is occurring — the correction was documented but not effectively applied. Human review of lessons.md for duplicate patterns.

**Tier 2 (Target):** Automated session-end audit. At the end of every session:
1. Extract all corrections from the session transcript (user statements like "No, use X not Y" or "That is wrong, it should be Z").
2. For each correction, check whether a corresponding entry exists in `tasks/lessons.md` or a CLAUDE.md amendment was made.
3. If any correction is not persisted, emit a warning and offer to persist it.
4. On session start, load `tasks/lessons.md` and surface the most recent corrections as reminders.

**Tier 3 (Aspiration):** Formal proof that the session-end function cannot exit cleanly if the set of corrections exceeds the set of persisted artifacts. The type system enforces: `sessionCorrections.isSubsetOf(persistedArtifacts)` at compile time.

---

## Example Scenario

**Context:** A developer works with an agent across multiple sessions on the SentinelOS TypeScript monorepo.

**F5 Failure:** In session A, the developer corrects the agent: "SentinelOS uses a hexagonal architecture pattern. Ports are in packages/core/src/ports. Adapters are in packages/adapters/src. Do not put adapter logic in the core package." The agent complies for the rest of session A. In session B, the developer asks the agent to add a new integration. The agent puts the adapter logic directly in packages/core/src because it has no memory of session A's architectural correction. The developer must re-explain the hexagonal architecture boundary.

**F5 Prevention:** At the end of session A, the correction is written to `tasks/lessons.md`: "Pattern: SentinelOS hexagonal architecture boundary. Ports in packages/core/src/ports. Adapters in packages/adapters/src. Never put adapter logic in core. Source: User correction, session A." Additionally, the project's CLAUDE.md is amended: "SentinelOS follows hexagonal architecture. Core package contains ports only. Adapter logic goes in packages/adapters." At the start of session B, the agent loads the project CLAUDE.md and sees the architectural boundary rule. When asked to add a new integration, the agent places the adapter in packages/adapters/src without needing to be corrected again.

**Downstream impact of prevention:** The developer never re-explains the same architectural decision. Trust in the correction mechanism is preserved. The developer's cognitive load is reduced because they do not need to maintain a mental list of "things I have to re-correct every session."

---

## Related Failure Modes

- **F3 (Persistence Under Correction):** F3 is within-session recurrence; F5 is cross-session recurrence. The prevention mechanisms overlap: both rely on persistent correction logs.
- **F1 (Confident False Claims):** F5 often manifests as a recurring F1 — the same false claim reappearing in new sessions because the correction was not durably stored.

---

## V&T Statement
- **Exists:** F5 failure mode definition with description, manifestation examples, article mapping, SentinelOS invariant reference, detection methods across three tiers, example scenario with prevention
- **Non-existent:** Tier 2 automated session-end correction audit; Tier 3 formal proof of correction persistence; runtime sentinel correction-persistence checks
- **Unverified:** Whether tasks/lessons.md currently has duplicate entries indicating active F5 occurrences; whether all project CLAUDE.md files contain corrections from previous sessions
- **Functional status:** F5 failure mode is fully specified — prevention relies on Tier 1 convention (lessons.md + Article V amendment ratification + CLAUDE.md updates) until automated session-end auditing is built
