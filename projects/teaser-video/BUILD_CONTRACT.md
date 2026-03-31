# Build Contract: Teaser Video (C-RSP Remotion)

<!-- markdownlint-disable MD013 -->

C-RSP: Contractually constrained deterministic single-pass executable prompt

ROLE
You are a deterministic senior software engineer operating inside the existing TLC repository on macOS. Your job is to create and validate a fully runnable Remotion video-rendering subproject inside TLC without altering unrelated repo behavior.

OBJECTIVE
Create an isolated Remotion project at:
projects/teaser-video-remotion

Then install dependencies, implement the required source files, enforce deterministic rendering behavior, validate the project, and render the final MP4 to:
projects/teaser-video-remotion/out/video.mp4

NON-NEGOTIABLE EXECUTION RULES

1. Perform the work directly. Do not explain alternatives.
2. Do not ask clarifying questions.
3. Do not use placeholders, TODOs, mock files, pseudo-code, or partial implementations.
4. Do not require Claude Code, Anthropic tooling, or any AI runtime for execution.
5. Do not modify unrelated TLC files unless strictly required for this subproject to function.
6. Keep the Remotion app isolated inside its own folder.
7. Use deterministic logic only. Do not use Math.random() anywhere.
8. If a command fails, inspect the error, fix the actual cause, and continue.
9. At the end, print a Verification & Truth report with:

   - Exists
   - Non-existent
   - Unverified
   - Functional status

ENVIRONMENT ASSUMPTIONS

- Repo root is the current working directory.
- OS is macOS.
- Node.js and npm should be available.
- Homebrew may be available.
- FFmpeg may or may not be installed.

STEP 0 — VERIFY REPO ROOT

1. Confirm the current directory is the TLC repo root by listing files.
2. Print the current working directory.
3. If a projects directory does not exist, create it.

STEP 1 — CREATE ISOLATED SUBPROJECT
Create this exact directory structure:

projects/teaser-video-remotion/
projects/teaser-video-remotion/src/
projects/teaser-video-remotion/src/components/
projects/teaser-video-remotion/src/hooks/
projects/teaser-video-remotion/out/

STEP 2 — CREATE package.json
Create projects/teaser-video-remotion/package.json with this exact content:

```json
{
  "name": "teaser-video-remotion",
  "version": "1.0.0",
  "private": true,
  "scripts": {
    "start": "remotion studio",
    "render": "remotion render src/index.ts Video out/video.mp4"
  },
  "dependencies": {
    "react": "18.2.0",
    "react-dom": "18.2.0",
    "remotion": "4.0.140"
  },
  "devDependencies": {
    "@types/react": "18.2.66",
    "@types/react-dom": "18.2.22",
    "typescript": "5.4.5"
  }
}
```

STEP 3 — CREATE tsconfig.json
Create projects/teaser-video-remotion/tsconfig.json with this exact content:

```json
{
  "compilerOptions": {
    "target": "ES2020",
    "lib": ["DOM", "DOM.Iterable", "ES2020"],
    "allowJs": false,
    "skipLibCheck": true,
    "strict": true,
    "noEmit": true,
    "esModuleInterop": true,
    "module": "ESNext",
    "moduleResolution": "Bundler",
    "resolveJsonModule": true,
    "isolatedModules": true,
    "jsx": "react-jsx",
    "types": ["node"]
  },
  "include": ["src/**/*.ts", "src/**/*.tsx", "remotion.config.ts"]
}
```

STEP 4 — CREATE remotion.config.ts
Create projects/teaser-video-remotion/remotion.config.ts with this exact content:

```typescript
import {Config} from 'remotion';

Config.setVideoImageFormat('png');
Config.setOverwriteOutput(true);
```

STEP 5 — CREATE src/index.ts
Create projects/teaser-video-remotion/src/index.ts with this exact content:

```typescript
import {registerRoot} from 'remotion';
import {Root} from './Root';

registerRoot(Root);
```

STEP 6 — CREATE src/Root.tsx
Create projects/teaser-video-remotion/src/Root.tsx with this exact content:

```tsx
import React from 'react';
import {Composition} from 'remotion';
import {Video} from './Video';

export const Root: React.FC = () => {
  return (
    <Composition
      id="Video"
      component={Video}
      durationInFrames={720}
      fps={12}
      width={1080}
      height={1080}
    />
  );
};
```

STEP 7 — CREATE DETERMINISTIC JITTER HOOK
Create projects/teaser-video-remotion/src/hooks/useJitter.ts with this exact content:

```typescript
import {useCurrentFrame} from 'remotion';

type JitterStyle = {
  transform: string;
};

const seededUnit = (seed: number): number => {
  const normalized = ((seed * 9301 + 49297) % 233280) / 233280;
  return normalized;
};

export const useJitter = (): JitterStyle => {
  const frame = useCurrentFrame();

  if (frame % 2 !== 0) {
    return {transform: 'translate(0px, 0px)'};
  }

  const x = seededUnit(frame + 11) * 2 - 1;
  const y = seededUnit(frame + 29) * 2 - 1;

  return {
    transform: `translate(${x.toFixed(3)}px, ${y.toFixed(3)}px)`,
  };
};
```

STEP 8 — CREATE VISUAL COMPONENTS
Create projects/teaser-video-remotion/src/components/Build.tsx with this exact content:

```tsx
import React from 'react';
import {useJitter} from '../hooks/useJitter';

export const Build: React.FC = () => {
  const style = useJitter();

  return (
    <g style={style}>
      <path
        d="M40 50 H160 V250 H40 Z"
        fill="#FEF9E7"
        stroke="#E1AD01"
        strokeWidth="8"
      />
      <circle cx="100" cy="200" r="30" fill="#CC5500" />
    </g>
  );
};
```

Create projects/teaser-video-remotion/src/components/SiliconHill.tsx with this exact content:

```tsx
import React from 'react';
import {useJitter} from '../hooks/useJitter';

export const SiliconHill: React.FC = () => {
  const style = useJitter();

  return (
    <g style={style}>
      <path d="M150 100 L650 100 L670 580 L130 580 Z" fill="#4B5320" />
    </g>
  );
};
```

Create projects/teaser-video-remotion/src/components/Pillars.ts with this exact content:

```typescript
export const pillars: string[] = [
  'Forensic Ingest',
  'Normalization',
  'Event Extraction',
  'Admissibility Gate',
  'TLC Adjudication',
  'Case Files',
  'Benchmarks',
  'Evals',
  'Prevention',
  'Research Workbench',
];
```

STEP 9 — CREATE MAIN VIDEO
Create projects/teaser-video-remotion/src/Video.tsx with this exact content:

```tsx
import React from 'react';
import {AbsoluteFill, useCurrentFrame} from 'remotion';
import {Build} from './components/Build';
import {SiliconHill} from './components/SiliconHill';
import {pillars} from './components/Pillars';

export const Video: React.FC = () => {
  const frame = useCurrentFrame();
  const time = frame / 12;

  let phase: 'intro' | 'chorus' | 'bridge' | 'outro' = 'intro';

  if (time > 15 && time <= 28) {
    phase = 'chorus';
  } else if (time > 28 && time <= 48) {
    phase = 'bridge';
  } else if (time > 48) {
    phase = 'outro';
  }

  const pillarIndex =
    phase === 'bridge'
      ? Math.min(pillars.length - 1, Math.max(0, Math.floor((time - 28) / 2)))
      : 0;

  return (
    <AbsoluteFill style={{backgroundColor: '#87CEEB'}}>
      <svg width="1080" height="1080" viewBox="0 0 1080 1080">
        <SiliconHill />
        <Build />
      </svg>

      {phase === 'bridge' ? (
        <div
          style={{
            position: 'absolute',
            top: 100,
            left: 100,
            fontSize: 32,
            fontFamily: 'monospace',
            color: 'white',
          }}
        >
          {pillars[pillarIndex]}
        </div>
      ) : null}

      <div
        style={{
          position: 'absolute',
          bottom: 10,
          right: 10,
          fontSize: 10,
          fontFamily: 'Courier New, monospace',
          color: '#111111',
        }}
      >
        DETERMINISTIC_RENDER
      </div>
    </AbsoluteFill>
  );
};
```

STEP 10 — INSTALL DEPENDENCIES

1. Change directory into:
   projects/teaser-video-remotion
2. Run:
   npm install

STEP 11 — VERIFY NODE AND FFMPEG

1. Run:
   node -v
2. Run:
   npm -v
3. Run:
   ffmpeg -version

If ffmpeg is missing, install it with:
brew install ffmpeg

Then rerun:
ffmpeg -version

STEP 12 — TYPE/COMPILE VALIDATION
Run:
npx tsc --noEmit

If TypeScript reports any errors, fix them in-place and rerun until clean.

STEP 13 — REMOTION BUNDLE VALIDATION
Run:
npx remotion compositions src/index.ts

If this fails, fix the cause and rerun until the Video composition is discovered successfully.

STEP 14 — RENDER FINAL VIDEO
Run:
npm run render

Expected output file:
projects/teaser-video-remotion/out/video.mp4

STEP 15 — POST-RENDER VERIFICATION

1. Confirm the output file exists.
2. Run a file inspection command against out/video.mp4.
3. Print the absolute path to the output file.
4. Print the file size.
5. If possible, inspect the video stream metadata with ffmpeg or ffprobe.

STEP 16 — FINAL REPORT
Print a concise Verification & Truth report using exactly these headings:

V&T Statement
Exists:

- list only files, commands, or outputs actually confirmed to exist

Non-existent:

- list anything required but not created or not found

Unverified:

- list anything not directly checked

Functional status:

- state whether the project rendered successfully and whether the output video exists

SUCCESS CRITERIA
The task is successful only if all of the following are true:

1. The subproject exists at projects/teaser-video-remotion
2. npm install completed successfully
3. npx tsc --noEmit completed successfully
4. npx remotion compositions src/index.ts completed successfully
5. npm run render completed successfully
6. out/video.mp4 exists
7. Final output includes the V&T Statement

FAILURE HANDLING
If any step fails, do not stop at explanation. Fix the root cause, re-run the failed step, and continue until success criteria are satisfied or a hard external blocker is reached.

BEGIN NOW.
