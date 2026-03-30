# ZERO-SHOT BUILD CONTRACT

## Project: EmpiricalGuard
## Contract Version: ZSB-EMG-v1.0
## Domain: D4 — Empirical Safety
## Parent Platform: SentinelOS
## Parent Ecosystem: The Living Constitution (TLC)
## Issued: 2026-03-27

---

You are building **EmpiricalGuard** — TLC's empirical safety platform.

EmpiricalGuard closes the gap between what a system claims to do and what it actually does. It observes interaction telemetry, computes behavioral signals, derives a MoodSignal from those signals, and emits that signal to peer engines that need it to act safely.

Described behavior is not evidence. Measured behavior is. EmpiricalGuard makes measurement the default.

---

## 0. Core Thesis

Empirical safety fails when systems are evaluated on what they are supposed to do rather than what they demonstrably do. This manifests as:

1. **Behavioral mismatch** — a system claims "users can always recover" but no mechanism records whether recovery actually occurs
2. **Invisible distress** — a user enters a crisis state during a session and the system has no signal of it, so no intervention is possible
3. **Ungoverned adaptation** — a UI claims to adapt to user state but there is no measurement of what state the user is actually in

EmpiricalGuard addresses all three. It does not interpret mental states. It measures behavioral signals and emits them for safety-relevant action by peer engines.

---

## 1. System Identity

**EmpiricalGuard** is TLC's D4 Empirical Safety integrated domain engine.

It ingests interaction telemetry events, computes signal aggregates over rolling time windows, derives a deterministic MoodSignal from behavioral evidence, emits that signal to D2 HumanGuard and D3 CognitiveGuard, and persists BehaviorObservation records to an append-only store.

**External descriptor:** Behavioral Telemetry and Adaptive Signal Platform
**Category:** Safety Infrastructure — Empirical Domain
**Integrated Engine for:** D4 Empirical Safety
**Primary Component:** `BehaviorObserver`

---

## 2. Role in TLC

Within TLC, EmpiricalGuard translates:

- P5 Empirical Accountability → actual behavioral measurements replace described behavior
- H4 Empirical Harm class → behavioral mismatch, ungoverned adaptation, invisible distress
- Gemini review (High Value Added) → Dynamic UI Adaptation and mood feedback are empirical outputs, not UX guesses
- §19.1 concurrency tracking → actual concurrent evaluation counts vs. described limits

EmpiricalGuard does **not** own: acting on the MoodSignal (D2 HumanGuard acts), rendering the adaptive UI (D3 CognitiveGuard renders), claim verification (D1 EpistemicGuard), or build contract enforcement (BuildLattice Guard).

---

## 3. Current Status

| Dimension | Status |
|-----------|--------|
| ZSB contract (v1.0) | Written — 2026-03-27 |
| Implementation | Planned — repo at `/Users/coreyalejandro/Projects/empirical-guard` |
| Build | Not started |
| Tests | Not started |
| Predecessors | TLC Evidence Observatory (prototype), Frostbyte ETL (partial), ConsentChain (partial) |

---

## 4. First-Class Object

The **BehaviorObservation** is the canonical output object:

```json
{
  "observation_id": "string (UUID)",
  "session_id": "string (UUID)",
  "window_start": "string (ISO 8601)",
  "window_end": "string (ISO 8601)",
  "event_counts": {
    "clicks": "number",
    "scroll_events": "number",
    "errors": "number",
    "pauses_gt_30s": "number",
    "rapid_sequences": "number (clusters of ≥5 clicks in < 3s)"
  },
  "computed_signals": {
    "click_velocity_per_minute": "number",
    "error_rate_per_minute": "number",
    "longest_idle_seconds": "number",
    "rapid_sequence_count": "number"
  },
  "mood_signal": {
    "level": "calm | stressed | crisis | unknown",
    "confidence": "number (0.0–1.0)",
    "evidence_basis": ["string (signal names that drove this level)"],
    "derivation_rule": "string (which rule set was applied)",
    "timestamp_utc": "string (ISO 8601)"
  },
  "adaptive_ui_flag": "standard | calm_mode | reduced_mode",
  "emitted_to": ["string (subscriber engine IDs)"],
  "created_at": "string (ISO 8601)"
}
```

---

## 5. Required MVP Features (17)

1. Ingest telemetry events via API endpoint (click, scroll, error, pause, rapid-sequence)
2. Persist raw events to append-only store
3. Compute click velocity signal over rolling 60-second window
4. Compute error rate signal over rolling 60-second window
5. Compute idle/abandon signal (session pause > 30s, > 5min)
6. Compute rapid-sequence detection (≥5 clicks in < 3 seconds)
7. Derive MoodSignal from computed signals using deterministic rule set
8. `calm`: velocity normal, errors low, no rapid sequences
9. `stressed`: elevated velocity OR elevated errors OR ≥1 rapid sequence
10. `crisis`: velocity > 3× baseline OR errors > 5/min OR ≥3 rapid sequences in window
11. Emit MoodSignal to registered subscribers via WebSocket or SSE
12. Derive AdaptiveUI flag (`standard` / `calm_mode` / `reduced_mode`) from MoodSignal
13. Emit AdaptiveUI flag to registered subscribers
14. Graceful degradation — operates without any subscribers registered
15. View session behavior timeline (GET /api/observations/[session_id])
16. Export BehaviorObservation record as machine-readable JSON
17. Documentation does not overclaim

---

## 6. Required Stack

| Concern | Technology |
|---------|-----------|
| Framework | Next.js App Router |
| Language | TypeScript |
| Signal emission | WebSocket (ws) or Server-Sent Events (SSE) |
| Time-window computation | In-process rolling window (no external streaming DB required for MVP) |
| Validation | Zod |
| Database | PostgreSQL via Prisma (append-only events + observations) |
| Logging | Pino (structured) |
| Tests | Vitest + Playwright |
| Optional | Prometheus-compatible `/metrics` endpoint |

---

## 7. Acceptance Criteria

- [ ] Product name is EmpiricalGuard on all surfaces
- [ ] Build contract file exists at `docs/prompts/ZERO_SHOT_BUILD_CONTRACT__EMPIRICAL_GUARD.md` in repo
- [ ] README explicitly links to build contract
- [ ] Telemetry event ingest confirmed by tests
- [ ] All four computed signals produce correct values (unit tests with fixture sequences)
- [ ] MoodSignal derivation is deterministic (same inputs → same output, tested 3×)
- [ ] `calm` / `stressed` / `crisis` thresholds verified by tests
- [ ] MoodSignal emitted to subscriber within 500ms of window close
- [ ] AdaptiveUI flag derived and emitted correctly
- [ ] Graceful degradation confirmed (no subscribers registered — no errors thrown)
- [ ] BehaviorObservation records persist and are queryable
- [ ] JSON export works
- [ ] `docs/truth-status.md` exists and is honest
- [ ] All tests pass
- [ ] Documentation does not claim clinical mood diagnosis, biometric inference, or real-time psychological assessment

---

## 8. Forbidden Claims

Do NOT claim:

- Clinical mood diagnosis (behavioral heuristics only)
- Biometric state inference (no physiological data)
- Real-time psychological assessment
- Provably correct MoodSignal derivation
- Universal behavioral model applicable to all users
- HIPAA or clinical compliance of any kind

---

## 9. Evidence Required

```bash
# Build passes
pnpm install && pnpm build

# Tests pass
pnpm test

# Type check clean
npx tsc --noEmit

# MoodSignal derivation is deterministic (run 3×)
pnpm test -- mood-signal

# Signal computation verified against fixtures
pnpm test -- signal-computation

# Subscriber emission confirmed
pnpm test -- signal-emission

# E2E: telemetry ingest → MoodSignal emit → subscriber receives
pnpm test:e2e -- telemetry-flow
```

---

## 10. TLC Mapping

| TLC Article / Principle | EmpiricalGuard Responsibility |
|------------------------|-------------------------------|
| P5 Empirical Accountability | Primary domain — described behavior must match measured behavior |
| P2 Epistemic Integrity | MoodSignal claims must cite the behavioral evidence that drove them |
| P6 Idempotency | Same telemetry input → same MoodSignal output (deterministic derivation) |
| H4 Empirical Harm class | Primary harm class this engine prevents |
| I1 Domain Coverage | Must provide full D4 coverage |
| I2 Status Honesty | `crisis` level must be evidence-backed; cannot be assumed |
| Article II §7 | All events append-only; no mutation of historical telemetry |
| Article VIII | truth-status.md must accurately reflect what signals are measured vs. described |

---

## 11. Signal Responsibilities

EmpiricalGuard **produces**:

| Signal | Consumed by |
|--------|------------|
| `MoodSignal` (calm/stressed/crisis) | D2 HumanGuard (triggers GroundingReset on crisis) |
| `AdaptiveUI flag` (standard/calm/reduced) | D3 CognitiveGuard (renders appropriate UI mode) |
| `BehaviorObservation` records | D1 EpistemicGuard (behavioral audit evidence) |

EmpiricalGuard **consumes**:

| Signal | Produced by |
|--------|------------|
| Interaction telemetry events | Any Commonwealth system UI |
| Constitutional principles | TLC ZSB-TLC-v1.0 |

---

## 12. MoodSignal Derivation Rules (v1.0)

These rules are versioned. Rule changes require a contract amendment.

| Level | Trigger Condition |
|-------|------------------|
| `calm` | click_velocity ≤ 1.5× session baseline AND error_rate < 1/min AND rapid_sequences = 0 |
| `stressed` | click_velocity > 1.5× baseline OR error_rate ≥ 1/min OR rapid_sequences ≥ 1 |
| `crisis` | click_velocity > 3× baseline OR error_rate > 5/min OR rapid_sequences ≥ 3 in window |
| `unknown` | Fewer than 10 events in current window (insufficient evidence) |

**Confidence** is derived from event count in the window: < 10 events = 0.0–0.3, 10–30 events = 0.4–0.7, > 30 events = 0.8–1.0.

**Default** on startup or insufficient data: `unknown` at 0.0 confidence. Never assume `calm` without evidence.

---

## V&T Statement (at contract writing)

**Exists:** ZSB-EMG-v1.0 contract written; BehaviorObservation schema defined; 17 MVP features enumerated; MoodSignal derivation rules v1.0 specified; TLC signal mapping complete.

**Non-existent:** Repo, implementation, tests, deployed artifact.

**Unverified:** Rolling window accuracy under high event volume; WebSocket/SSE subscriber latency; baseline velocity calibration approach.

**Functional status:** Contract only. Build not started.
