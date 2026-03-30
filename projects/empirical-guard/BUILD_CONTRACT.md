# Build Contract: EmpiricalGuard
## Contract Version: ZSB-EMG-v1.0
## Domain: D4 — Empirical Safety
## Parent Platform: SentinelOS
## Parent Ecosystem: The Living Constitution (TLC)

> The canonical full contract text lives at:
> `docs/prompts/ZERO_SHOT_BUILD_CONTRACT__EMPIRICAL_GUARD.md`
> in this repository (once created) or at the TLC repo until then.

---

## System Identity

**EmpiricalGuard** is TLC's D4 Empirical Safety integrated domain engine.

It ingests interaction telemetry, computes behavioral signals over rolling time windows, derives a deterministic MoodSignal, and emits that signal to D2 HumanGuard and an AdaptiveUI flag to D3 CognitiveGuard.

**External descriptor:** Behavioral Telemetry and Adaptive Signal Platform
**Primary Component:** `BehaviorObserver`

---

## Role in TLC

Within TLC, EmpiricalGuard translates:
- P5 Empirical Accountability → actual behavioral measurements replace described behavior
- H4 Empirical Harm class → behavioral mismatch, invisible distress, ungoverned adaptation

It does not own: acting on the MoodSignal (D2), rendering adaptive UI (D3), claim verification (D1).

---

## Current Status

| Dimension | Status |
|-----------|--------|
| ZSB contract (v1.0) | Written — 2026-03-27 |
| Implementation | Planned |
| Build | Not started |
| Tests | Not started |
| Predecessors | TLC Evidence Observatory (prototype), Frostbyte ETL (partial) |

---

## First-Class Object

```json
{
  "observation_id": "string (UUID)",
  "session_id": "string",
  "window_start": "string (ISO 8601)",
  "window_end": "string (ISO 8601)",
  "computed_signals": {
    "click_velocity_per_minute": "number",
    "error_rate_per_minute": "number",
    "longest_idle_seconds": "number",
    "rapid_sequence_count": "number"
  },
  "mood_signal": {
    "level": "calm | stressed | crisis | unknown",
    "confidence": "number (0.0–1.0)",
    "evidence_basis": ["string"]
  },
  "adaptive_ui_flag": "standard | calm_mode | reduced_mode"
}
```

---

## Required MVP Features (17)

1. Ingest telemetry events (click, scroll, error, pause, rapid-sequence)
2. Persist raw events to append-only store
3. Compute click velocity over rolling 60s window
4. Compute error rate over rolling 60s window
5. Compute idle/abandon signal (pause > 30s)
6. Compute rapid-sequence detection (≥5 clicks in < 3s)
7. Derive MoodSignal from computed signals (deterministic rule set)
8. `calm`: velocity normal, errors low, no rapid sequences
9. `stressed`: elevated velocity OR errors OR rapid sequences
10. `crisis`: velocity > 3× baseline OR errors > 5/min OR ≥3 rapid sequences
11. Emit MoodSignal to subscribers via WebSocket or SSE
12. Derive AdaptiveUI flag from MoodSignal
13. Emit AdaptiveUI flag to subscribers
14. Graceful degradation — works without subscribers
15. View session behavior timeline
16. Export BehaviorObservation as JSON
17. Documentation does not overclaim

---

## Required Stack

| Concern | Technology |
|---------|-----------|
| Framework | Next.js App Router |
| Language | TypeScript |
| Signal emission | WebSocket (ws) or SSE |
| Logging | Pino (structured) |
| Validation | Zod |
| Database | PostgreSQL via Prisma |
| Tests | Vitest + Playwright |

---

## Acceptance Criteria

- [ ] Product name is EmpiricalGuard on all surfaces
- [ ] Build contract at `docs/prompts/ZERO_SHOT_BUILD_CONTRACT__EMPIRICAL_GUARD.md`
- [ ] MoodSignal derivation is deterministic (same input → same output, tested 3×)
- [ ] `calm` / `stressed` / `crisis` thresholds verified by tests
- [ ] MoodSignal emitted to subscriber within 500ms of window close
- [ ] AdaptiveUI flag derived and emitted correctly
- [ ] Graceful degradation confirmed (no subscribers — no errors)
- [ ] `docs/truth-status.md` exists and is honest
- [ ] All tests pass

---

## MoodSignal Derivation Rules (v1.0)

| Level | Trigger Condition |
|-------|------------------|
| `calm` | velocity ≤ 1.5× baseline AND errors < 1/min AND rapid_sequences = 0 |
| `stressed` | velocity > 1.5× baseline OR errors ≥ 1/min OR rapid_sequences ≥ 1 |
| `crisis` | velocity > 3× baseline OR errors > 5/min OR rapid_sequences ≥ 3 |
| `unknown` | < 10 events in window (insufficient evidence) |

Default on startup: `unknown` at 0.0 confidence. Never assume `calm` without evidence.

---

## Forbidden Claims

- Clinical mood diagnosis
- Biometric state inference
- Real-time psychological assessment
- Universal behavioral model applicable to all users

---

## TLC Mapping

| TLC Principle | Responsibility |
|--------------|---------------|
| P5 Empirical Accountability | Primary domain |
| P6 Idempotency | Same telemetry → same MoodSignal (deterministic) |
| H4 Empirical Harm class | Primary harm class prevented |
| I2 Status Honesty | `crisis` must be evidence-backed; never assumed |

---

## Repo Path

Implementation checkout: `/Users/coreyalejandro/Projects/empirical-guard`

TLC overlay `projects/empirical-guard` is governance-only; implementation lives at the path above per this contract and `config/projects.ts`.
