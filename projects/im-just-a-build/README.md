# I'm Just a Build — C-RSP Remotion Package

This package contains a constitution-aligned starter repository and a fully instantiated C-RSP build contract for producing the **"I'm Just a Build"** video as a deterministic Remotion project inside TLC.

## Included
- `BUILD_CONTRACT.md` — executable C-RSP prompt for a coding operator
- `CLAUDE.md` — local project constitution and operator rules
- `DIRECTORS_TREATMENT.md` — act-by-act visual direction
- `LYRICS_TIMECODE.md` — line-to-scene timing map
- `VISUAL_INVARIANTS.md` — non-negotiable style and motion rules
- `SOURCE_SYNTHESIS.md` — distilled source material from the conversation and uploaded markdown
- `package.json`, `tsconfig.json`, `remotion.config.ts` — Remotion scaffold
- `src/` — deterministic starter implementation

## Intended location in TLC
```text
projects/im-just-a-build/
```

## Local commands
```bash
npm install
npx tsc --noEmit
npx remotion compositions src/index.ts
npm run render
```

## Output
```text
out/video.mp4
```
