# Build Contract: HumanGuard
## Contract Version: ZSB-HMG-v1.0
## Domain: D2 — Human Safety
## Parent Platform: SentinelOS
## Parent Ecosystem: The Living Constitution (TLC)

> The canonical full contract text lives at:
> `docs/prompts/ZERO_SHOT_BUILD_CONTRACT__HUMAN_GUARD.md`
> in this repository (once created) or at the TLC repo until then.

---

## System Identity

**HumanGuard** is TLC's D2 Human Safety integrated domain engine.

It manages session persistence, emergency grounding resets, harm language scanning, crisis signal intake, and confirmation gates around all destructive actions.

**External descriptor:** Session Safety and Human Dignity Platform
**Primary Component:** `SessionSafeguard`

---

## Role in TLC

Within TLC, HumanGuard translates:
- P3 Human Dignity → HarmScanner blocks traumatizing language before render
- P6 Idempotency → session reset/resume is lossless
- SOP-013 Session Recovery Protocol → implemented as `GroundingReset` + `SaveState`

It does not own: content evaluation (D3), claim verification (D1), behavioral telemetry (D4).

---

## Current Status

| Dimension | Status |
|-----------|--------|
| ZSB contract (v1.0) | Written — 2026-03-27 |
| Implementation | Planned |
| Build | Not started |
| Tests | Not started |
| Predecessor | UICare-System (partial) |

---

## First-Class Object

```json
{
  "session_id": "string (UUID)",
  "state_snapshot": { "step": "number", "page": "string", "data": "object", "saved_at": "string" },
  "crisis_state": "calm | stressed | crisis | unknown",
  "harm_detections": [{ "excerpt": "string", "harm_class": "string", "action_taken": "string" }],
  "grounding_events": [{ "event_id": "string", "trigger": "string", "timestamp_utc": "string" }],
  "confirm_gate_events": [{ "action_label": "string", "confirmed": "boolean" }],
  "recovery_available": "boolean"
}
```

---

## Required MVP Features (17)

1. Create and persist SafeSession on first interaction
2. Auto-save state on every user action (no loss window > 5s)
3. Resume session without data loss on page reload
4. GroundingReset — one-tap return to baseline, no navigation required
5. GroundingReset preserves snapshot before clearing
6. HarmScanner — detect punitive/urgency/shame language in UI copy
7. Block harmful language from rendering
8. Log all harm detections
9. CrisisGate — wrap all destructive actions in confirm gate
10. Confirm gate states human-readable consequence before action
11. Consume MoodSignal from EmpiricalGuard (D4)
12. Graceful degradation — works without D4 signal
13. Session history listing
14. Safe session export (user-facing)
15. Audit log of crisis events and harm detections
16. All error states handled with recovery guidance
17. Documentation does not overclaim

---

## Required Stack

| Concern | Technology |
|---------|-----------|
| Framework | Next.js App Router |
| Language | TypeScript |
| Crisis signal intake | WebSocket or SSE |
| Harm detection | Curated lexicon (no LLM required) |
| Validation | Zod |
| Database | PostgreSQL via Prisma |
| Tests | Vitest + Playwright |

---

## Acceptance Criteria

- [ ] Product name is HumanGuard on all surfaces
- [ ] Build contract at `docs/prompts/ZERO_SHOT_BUILD_CONTRACT__HUMAN_GUARD.md`
- [ ] Session auto-save confirmed by tests
- [ ] GroundingReset confirmed by tests
- [ ] HarmScanner blocks known harm-class words before render
- [ ] CrisisGate requires explicit confirm before destructive action
- [ ] MoodSignal intake triggers GroundingReset on crisis
- [ ] Graceful degradation confirmed (D4 absent)
- [ ] `docs/truth-status.md` exists and is honest
- [ ] All tests pass

---

## Forbidden Claims

- Clinical crisis detection or diagnosis
- HIPAA compliance
- Biometric state inference
- Exhaustive harm language coverage

---

## Default User Mandate

Every feature is designed for a neurodivergent adult with Bipolar I, ADHD, OCD, and trauma history. If a feature creates urgency, ambiguity, or risk of session loss for this user, it fails. Redesign before shipping.

---

## TLC Mapping

| TLC Principle | Responsibility |
|--------------|---------------|
| P3 Human Dignity | Primary domain |
| P6 Idempotency | Session reset/resume is lossless |
| SOP-013 | GroundingReset = machine implementation of Session Recovery Protocol |
| H2 Human Harm class | Primary harm class prevented |
