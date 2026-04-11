# CLAUDE.md — I'm Just a Build

## Parent Authority
This project inherits from TLC and follows constitutional governance, evidence-first execution, deterministic rendering, and honest V&T reporting.

## Project Identity
A Remotion-based 60-second educational animation that remakes the Schoolhouse Rock-style "I'm Just a Bill" structure into an AI Constitution / C-RSP explainer.

## Hard Rules
1. Use **Remotion + React + TypeScript** only for the video build path.
2. Keep the project isolated in its own folder. Do not modify unrelated TLC files.
3. Use **12fps** and deterministic frame logic. No `Math.random()` anywhere.
4. Preserve the 1970s cel-animation homage aesthetic.
5. Do not introduce modern UI styling such as glassmorphism, soft blur fields, neon cyberpunk palettes, or 3D camera tricks.
6. Treat `BUILD_CONTRACT.md` as the execution authority for file generation and render steps.
7. Treat `DIRECTORS_TREATMENT.md`, `LYRICS_TIMECODE.md`, and `VISUAL_INVARIANTS.md` as the canonical creative constraints.
8. If audio is missing, keep the timeline and ship a silent or placeholder-safe render rather than inventing unsupported audio behavior.
9. Every final report must end with a V&T statement.

## Command Surface
- Install: `npm install`
- Type check: `npx tsc --noEmit`
- Inspect compositions: `npx remotion compositions src/index.ts`
- Preview: `npm run start`
- Render: `npm run render`

## Project Outputs
- Primary artifact: `out/video.mp4`
- Optional evidence: `out/render-report.md`, `out/video.sha256.txt`
