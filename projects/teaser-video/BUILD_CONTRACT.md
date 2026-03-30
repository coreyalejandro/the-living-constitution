# Build Contract: C-RSP "I'm Just a Build" Animation

## Status: EXECUTION-READY | Domain: D4 — Empirical Safety

## 🎯 Target State

A 60-second, 1080x1080 (12fps) MP4 explainer animation following the "I'm Just a Bill" parody script.

## 🧱 Implementation Spec (The Golden Source)

### 1. The Jitter Engine (Requirement)

Implement a `useJitter` hook. Every 2 frames, apply a random `translate(±1px, ±1px)` to all SVG elements to simulate vintage cel animation.

### 2. Digital Assets (SVG)

- **The Build:** `<path d="M40 50 H160 V250 H40 Z" fill="#FEF9E7" stroke="#E1AD01" stroke-width="8"/><circle cx="100" cy="200" r="30" fill="#CC5500" />`
- **Silicon Hill:** `<path d="M150 100 L650 100 L670 580 L130 580 Z" fill="#4B5320" />` (See full SVG definitions in memory).

### 3. The 10 Pillars (Sequence Data)

Animate the character passing through these gates during the Bridge (28s-48s):

1. Forensic Ingest | 2. Normalization | 3. Event Extraction | 4. Admissibility Gate | 5. TLC Adjudication | 6. Case Files | 7. Benchmarks | 8. Evals | 9. Prevention | 10. Research Workbench.

### 4. Deterministic Audio/Timing

- **Audio:** Use a 120BPM click-track if `audio.mp3` is missing.
- **Lyrics:** Use 'Bungee' font.
  - [0-15s]: Intro / Silicon Hill.
  - [15-28s]: Chorus (Constitutionally-Regulated).
  - [28-48s]: 10-Pillar Bridge.
  - [48-60s]: Outro / Success.

## 🏁 Acceptance Criteria

- [ ] Rendered at `/out/video.mp4`.
- [ ] SHA-256 hash of this contract visible in a 10pt Courier ticker (bottom-right).
- [ ] No gradients or modern blurs used (except sky).
- [ ] 10 Pillars are named and sequenced correctly.

## 📂 Repo Path

`/Users/coreyalejandro/Projects/the-living-constitution/projects/teaser-video/`
