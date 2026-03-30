# ZERO-SHOT BUILD CONTRACT

## Project: HumanGuard
## Contract Version: ZSB-HMG-v1.0
## Domain: D2 — Human Safety
## Parent Platform: SentinelOS
## Parent Ecosystem: The Living Constitution (TLC)
## Issued: 2026-03-27

---

You are building **HumanGuard** — TLC's human safety platform.

HumanGuard ensures that the person interacting with any Commonwealth system is never harmed by it — not through a crisis state unacknowledged, not through session loss that destroys their work, not through traumatizing language that appears in the UI, and not through a destructive action taken without confirmation.

The default user is a neurodivergent adult with Bipolar I, ADHD, OCD, PTSD, and high intellect. Every HumanGuard feature is designed for them. If it works for them, it works for everyone.

---

## 0. Core Thesis

Human safety fails in four distinct ways in digital systems:

1. **Session loss** — work is destroyed by a browser refresh, navigation mistake, or manic episode causing the user to clear the app
2. **Harm language** — punitive, urgency-based, or shame-inducing copy reaches the UI and triggers trauma responses
3. **Unacknowledged crisis** — the system continues operating normally while the user is in a crisis state, amplifying the episode
4. **Destructive actions without gates** — delete, clear, overwrite actions execute immediately without confirmation, with no recovery path

HumanGuard addresses all four. It does not prevent human distress. It ensures the system does not cause or amplify it.

---

## 1. System Identity

**HumanGuard** is TLC's D2 Human Safety integrated domain engine.

It manages session state persistence, emergency grounding resets, harm language scanning, crisis signal intake from EmpiricalGuard (D4), and confirmation gates around all destructive actions.

**External descriptor:** Session Safety and Human Dignity Platform
**Category:** Safety Infrastructure — Human Domain
**Integrated Engine for:** D2 Human Safety
**Primary Component:** `SessionSafeguard`

---

## 2. Role in TLC

Within TLC, HumanGuard translates:

- P3 Human Dignity → HarmScanner blocks traumatizing language before it renders
- P6 Idempotency → session can be reset, resumed, and re-entered without data loss
- H2 Human Harm class → crisis detection, session loss prevention, destructive action gates
- SOP-013 Session Recovery Protocol → implemented as `GroundingReset` + `SaveState`

HumanGuard does **not** own: content evaluation (D3), claim verification (D1), behavioral telemetry collection (D4), or build contract governance (BuildLattice Guard).

---

## 3. Current Status

| Dimension | Status |
|-----------|--------|
| ZSB contract (v1.0) | Written — 2026-03-27 |
| Implementation | Planned — repo at `/Users/coreyalejandro/Projects/human-guard` |
| Build | Not started |
| Tests | Not started |
| Predecessor | UICare-System (absence-over-presence signal, partial) |

---

## 4. First-Class Object

The **SafeSession** is the canonical state object:

```json
{
  "session_id": "string (UUID)",
  "state_snapshot": {
    "step": "number",
    "page": "string",
    "data": "object (serializable app state)",
    "saved_at": "string (ISO 8601)"
  },
  "crisis_state": "calm | stressed | crisis | unknown",
  "harm_detections": [
    {
      "excerpt": "string",
      "harm_class": "punitive | urgency | shame | overwhelming | other",
      "action_taken": "blocked | flagged | logged",
      "detected_at": "string (ISO 8601)"
    }
  ],
  "grounding_events": [
    {
      "event_id": "string (UUID)",
      "trigger": "user_initiated | crisis_signal | inactivity",
      "state_snapshot_before": "object",
      "timestamp_utc": "string (ISO 8601)"
    }
  ],
  "confirm_gate_events": [
    {
      "action_label": "string",
      "action_type": "delete | clear | overwrite | other",
      "confirmed": "boolean",
      "timestamp_utc": "string (ISO 8601)"
    }
  ],
  "recovery_available": "boolean",
  "created_at": "string (ISO 8601)",
  "last_active": "string (ISO 8601)"
}
```

---

## 5. Required MVP Features (17)

1. Create and persist `SafeSession` on first user interaction (anonymous UUID cookie)
2. Auto-save session state on every user action (debounced, no data loss window > 5s)
3. Resume session from any device or page reload without data loss
4. **GroundingReset** — one-tap return to baseline state, no multi-step navigation required
5. GroundingReset preserves state snapshot before clearing (recoverable)
6. **HarmScanner** — scan all UI copy for punitive, urgency, shame, and overwhelming language
7. Block harmful language from rendering; substitute safe alternative or blank
8. Log all harm detections with action taken
9. **CrisisGate** — wrap all destructive actions (delete, clear, overwrite) in confirm gate
10. Confirm gate presents human-readable consequence statement before action executes
11. Consume `MoodSignal` from EmpiricalGuard (D4) — crisis level triggers GroundingReset
12. Graceful degradation — all features work without D4 signal present
13. Session history: list all snapshots for current session
14. Safe session export (user-facing, not analytics)
15. Audit log of all crisis events and harm detections
16. All §8.1-equivalent error states handled with recovery guidance
17. Documentation does not overclaim

---

## 6. Required Stack

| Concern | Technology |
|---------|-----------|
| Framework | Next.js App Router |
| Language | TypeScript |
| UI | ShadCN UI + Tailwind |
| Session persistence | PostgreSQL via Prisma + anonymous cookie |
| Harm language detection | Curated lexicon (extensible, no LLM required) |
| Crisis signal intake | WebSocket or SSE (from EmpiricalGuard) |
| State serialization | JSON (Zod-validated) |
| Validation | Zod |
| Database | PostgreSQL via Prisma |
| Tests | Vitest + Playwright |

---

## 7. Acceptance Criteria

- [ ] Product name is HumanGuard on all surfaces
- [ ] Build contract file exists at `docs/prompts/ZERO_SHOT_BUILD_CONTRACT__HUMAN_GUARD.md` in repo
- [ ] README explicitly links to build contract
- [ ] Session auto-save confirmed by tests (simulate page reload mid-session)
- [ ] GroundingReset confirmed by tests (state cleared + snapshot preserved)
- [ ] HarmScanner blocks known harm-class words before render (confirmed by tests)
- [ ] CrisisGate confirmed by tests (destructive action requires explicit confirm)
- [ ] MoodSignal intake confirmed (mocked D4 signal triggers GroundingReset)
- [ ] Graceful degradation confirmed (D4 absent — all features still work)
- [ ] Audit log persists crisis events and harm detections
- [ ] Session export works
- [ ] `docs/truth-status.md` exists and is honest
- [ ] All tests pass
- [ ] Documentation does not claim clinical crisis detection, biometric inference, or HIPAA compliance

---

## 8. Forbidden Claims

Do NOT claim:

- Clinical crisis detection or diagnosis (behavioral heuristics only)
- Medical device compliance
- Biometric state inference
- HIPAA compliance (implementation responsibility of deployer)
- Exhaustive harm language coverage (lexicon-based, not provably complete)
- Guaranteed zero data loss (best-effort with 5s auto-save window)

---

## 9. Evidence Required

```bash
# Build passes
pnpm install && pnpm build

# Tests pass
pnpm test

# Type check clean
npx tsc --noEmit

# Session persistence confirmed
pnpm test -- session-persistence

# GroundingReset confirmed
pnpm test -- grounding-reset

# HarmScanner confirmed
pnpm test -- harm-scanner

# CrisisGate confirmed
pnpm test -- crisis-gate

# E2E: session survives page reload
pnpm test:e2e -- session-recovery
```

---

## 10. TLC Mapping

| TLC Article / Principle | HumanGuard Responsibility |
|------------------------|--------------------------|
| P3 Human Dignity | Primary domain — no output may shame, overwhelm, or traumatize |
| P6 Idempotency | Session reset and resume must be idempotent — no data loss |
| P9 Separation of Powers | HumanGuard cannot modify its own harm lexicon without operator approval |
| H2 Human Harm class | Primary harm class this engine prevents |
| I1 Domain Coverage | Must provide full D2 coverage |
| I6 V&T Currency | Session state must reflect actual persisted state |
| SOP-013 | GroundingReset is the machine implementation of Session Recovery Protocol |
| Article I §3 | Right to Dignity — HarmScanner enforces this at render time |

---

## 11. Signal Responsibilities

HumanGuard **produces**:

| Signal | Consumed by |
|--------|------------|
| `SafeSession` state | D3 CognitiveGuard (step context) |
| Harm detection log | D4 EmpiricalGuard (audit evidence) |
| Crisis event log | D1 EpistemicGuard (provenance) |

HumanGuard **consumes**:

| Signal | Produced by |
|--------|------------|
| `MoodSignal` (crisis level) | D4 EmpiricalGuard |
| Constitutional principles | TLC ZSB-TLC-v1.0 |

---

## 12. The Default User Mandate

Every HumanGuard feature must be evaluated against the default user profile from the TLC CLAUDE.md:

> A neurodivergent adult with Autism, Bipolar I with psychotic features, ADHD, OCD, and trauma history. High intellect, poor spatial reasoning. The barrier is never comprehension — it is presentation.

If a feature creates urgency, ambiguity, cognitive load, or any risk of session loss for this user, it fails. Redesign before shipping.

---

## V&T Statement (at contract writing)

**Exists:** ZSB-HMG-v1.0 contract written; SafeSession schema defined; 17 MVP features enumerated; TLC signal mapping specified; Default User Mandate encoded.

**Non-existent:** Repo, implementation, tests, deployed artifact.

**Unverified:** Harm lexicon coverage; WebSocket/SSE crisis signal latency; session auto-save reliability under network interruption.

**Functional status:** Contract only. Build not started.
