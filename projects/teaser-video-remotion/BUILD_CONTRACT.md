# C-RSP BUILD CONTRACT — “I’m Just a Build” Remotion Video
## Constitutionally-Regulated Single Pass Executable Prompt

### Summary

Build a deterministic Remotion video package inside TLC at `projects/teaser-video-remotion/` for a 60-second, 1080x1080, 12fps animated homage titled **“I’m Just a Build.”** The package must include source code, real authored documentation, shell scripts for local rendering and ZIP creation, and no placeholder content.

### Fixed Decisions

- **Repo host:** TLC
- **Subproject path:** `projects/teaser-video-remotion/`
- **Tooling:** Cursor + Node + npm + FFmpeg + Remotion
- **Runtime mode:** local
- **Format:** 1080x1080
- **FPS:** 12
- **Duration:** 60 seconds / 720 frames
- **Style:** 1970s Schoolhouse Rock-inspired cel-animation homage
- **Narrative:** uncertainty -> regulation -> proof -> legitimacy
- **Protagonist:** parchment build contract with wax seal
- **World:** Silicon Hill server-rack hillscape
- **Acts:** Concept / Mechanism / 10 Pillars / Validation
- **Determinism rule:** no `Math.random()` anywhere in project source

### Scope

Create the following:

- Real Remotion project files
- Deterministic animation utility layer
- Four act scene components
- Project docs:
  - `BUILD_CONTRACT.md`
  - `CLAUDE.md`
  - `README.md`
  - `DIRECTORS_TREATMENT.md`
  - `LYRICS_TIMECODE.md`
  - `VISUAL_INVARIANTS.md`
- Shell scripts:
  - local render
  - local ZIP packaging

### Required File Paths

- `projects/teaser-video-remotion/package.json`
- `projects/teaser-video-remotion/remotion.config.ts`
- `projects/teaser-video-remotion/tsconfig.json`
- `projects/teaser-video-remotion/README.md`
- `projects/teaser-video-remotion/CLAUDE.md`
- `projects/teaser-video-remotion/BUILD_CONTRACT.md`
- `projects/teaser-video-remotion/DIRECTORS_TREATMENT.md`
- `projects/teaser-video-remotion/LYRICS_TIMECODE.md`
- `projects/teaser-video-remotion/VISUAL_INVARIANTS.md`
- `projects/teaser-video-remotion/src/index.ts`
- `projects/teaser-video-remotion/src/Root.tsx`
- `projects/teaser-video-remotion/src/composition/VideoConfig.ts`
- `projects/teaser-video-remotion/src/scenes/Act1Concept.tsx`
- `projects/teaser-video-remotion/src/scenes/Act2Mechanism.tsx`
- `projects/teaser-video-remotion/src/scenes/Act3Pillars.tsx`
- `projects/teaser-video-remotion/src/scenes/Act4Validation.tsx`
- `projects/teaser-video-remotion/src/components/BuildCharacter.tsx`
- `projects/teaser-video-remotion/src/components/SiliconHill.tsx`
- `projects/teaser-video-remotion/src/components/CaptionCard.tsx`
- `projects/teaser-video-remotion/src/components/PillarGrid.tsx`
- `projects/teaser-video-remotion/src/lib/palette.ts`
- `projects/teaser-video-remotion/src/lib/timing.ts`
- `projects/teaser-video-remotion/src/lib/easing.ts`
- `projects/teaser-video-remotion/src/lib/deterministic.ts`
- `projects/teaser-video-remotion/src/lib/lyrics.ts`
- `projects/teaser-video-remotion/src/lib/pillars.ts`
- `projects/teaser-video-remotion/public/.gitkeep`
- `projects/teaser-video-remotion/scripts/render.sh`
- `projects/teaser-video-remotion/scripts/package-zip.sh`

### Story and Act Timing

- **Act I — Concept:** frames 0–179
- **Act II — Mechanism:** frames 180–359
- **Act III — 10 Pillars:** frames 360–539
- **Act IV — Validation / Resolution:** frames 540–719

### Ten Pillars

1. Constitutional Scope
2. Explicit Constraints
3. Deterministic Execution
4. Separated Powers
5. Verification Mapping
6. Truth Status Discipline
7. Evidence Before Claim
8. Failure Halt Rules
9. Reproducible Outputs
10. Legitimate Release

### Design Rules

- Flat shapes only
- Hard ink-like outlines
- No glossy or contemporary UI sheen
- Palette limited to mustard, olive, burnt orange, cream, ink, and muted red wax accent
- Deterministic analog wobble allowed only through seeded functions
- Character readability must remain strong at square-social resolution

### Determinism Rules

- No `Math.random()` in project source
- No timestamp-based behavior
- No non-deterministic ordering
- All visual jitter must come from stable seeded frame math
- Same input code must produce same motion behavior on repeated renders

### Documentation Rules

The authored markdown files must be generated with real project-specific content. They must not be generic templates and must clearly distinguish:

- created source/doc files
- locally renderable outputs
- outputs not yet rendered

### ZIP Deliverable Requirement

The build must include a packaging script that creates:

- `im-just-a-build-crsp-package.zip`

The archive must be created from the finished subproject directory. The build report must distinguish between:

- package structure existing
- ZIP script existing
- ZIP actually created in the execution environment

### Commands

Implement npm scripts:

- `npm run dev`
- `npm run render`
- `npm run lint`
- `npm run package:zip`

### Acceptance Criteria

The build passes only if:

- all required files exist
- the composition is 1080x1080 at 12fps and 720 frames
- the four acts are encoded in source
- the ten pillars appear in docs and source
- no `Math.random()` usage exists in source
- local render and ZIP scripts exist
- reporting uses constitutional truth discipline

### Final Reporting Rules

Use these labels only:

- **Exists**
- **Non-existent**
- **Unverified**
- **Functional status**

Do not claim the MP4 exists unless rendered locally. Do not claim the ZIP exists unless created in the current environment.
