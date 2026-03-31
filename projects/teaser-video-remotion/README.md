# I’m Just a Build

## Deterministic Remotion teaser video inside TLC

“I’m Just a Build” is a Remotion subproject housed inside TLC. It is a constitutional remake-homage of the pedagogical structure behind “I’m Just a Bill,” reframed around C-RSP build discipline: uncertainty -> regulation -> proof -> legitimacy.

## Why this exists inside TLC

This package functions as a front-door teaser artifact for the broader constitutional operating model. It translates abstract governance concepts into a short narrative object that is easier to see, explain, demo, and eventually publish. The video is not a separate product platform. It is a bounded, isolated media subproject inside TLC.

## Fixed format

- **Canvas:** 1080x1080
- **Duration:** 60 seconds
- **FPS:** 12
- **Total frames:** 720

## Style

- 1970s Schoolhouse Rock-inspired cel-animation homage
- flat shapes
- hard outlines
- mustard / olive / burnt-orange palette
- deterministic analog-feeling wobble
- no glossy modern motion-graphics look

## Story structure

1. **Act I — Concept**
2. **Act II — Mechanism**
3. **Act III — 10 Pillars**
4. **Act IV — Validation / Resolution**

## Runtime requirements

Install locally:

- Node.js
- npm
- FFmpeg (required for `npm run render` / Remotion encoding)
- Remotion-compatible environment

Claude Code is **not** required to run this project.

## Install

From the TLC repo root:

```bash
cd projects/teaser-video-remotion
npm install
```

## Preview (Remotion Studio)

```bash
npm run dev
```

## Render

Authoritative composition settings verified on the originating machine:

- Composition: `ImJustABuild`
- Resolution: `1080x1080`
- FPS: `12`
- Frames: `720`

Primary commands:

```bash
npm install
npm run preflight
npm run render
```

Rendered output path:

`dist/im-just-a-build.mp4`

Known successful output SHA256:

`35c28f8f0fb82a51ceba7c89415afc91c8dd739dec034eb54982809dfd8cb6ff`

### Root cause of first failed render

The initial render failure was not caused by composition logic. It was caused by HTTP(S) proxy settings breaking access to localhost during the Remotion render workflow.

### Mitigation now in place

`scripts/render.sh` was hardened with:

- `NO_PROXY` / `no_proxy`
- Remotion runtime flags
- optional Chrome detection
- `--ipv4`
- `--timeout=120000`
- `--concurrency=1`

## Verification

Verification artifacts are stored under:

`verification/`

Governance artifacts are stored under:

`.c-rsp/`

The render is verified only on the originating machine at this time. Cross-machine reproducibility is not yet established.

### Verification scope policy

Default release verification uses:

- preflight success
- successful render
- output file existence
- authoritative MP4 SHA256
- spot-check frame hashing

Full-frame hashing is reserved for elevated audit runs and is not yet the default release gate.

## Packaging

Two packages are maintained:

1. **Source package** — `npm run package:zip` writes `im-just-a-build-source.zip`
   - Excludes `dist/` and `node_modules/`
   - Intended for source review, governance review, and reproducibility work
   - Legacy filename was `im-just-a-build-crsp-package.zip`; content policy (no `dist/` in archive) is unchanged

2. **Release package** — `npm run package:release-zip` writes `im-just-a-build-release.zip`
   - Includes `dist/im-just-a-build.mp4`
   - Includes verification evidence required to validate the shipped artifact (`verification/RENDER_REPORT.md`, `verification/*.sha256`)
   - Includes `README.md` and `LICENSE`
   - Records the release ZIP SHA256 in `verification/RELEASE_ZIP_SHA256.txt`

### Canonical release posture (originating host)

- **Share the rendered deliverable** → `im-just-a-build-release.zip`
- **Governance / source / reproducibility** → `im-just-a-build-source.zip`

**Publishable release candidate — packaging commands** (from TLC repo root):

```bash
cd projects/teaser-video-remotion
npm run package:zip
npm run package:release-zip
```

**MP4 SHA-256** (host-verified): `35c28f8f0fb82a51ceba7c89415afc91c8dd739dec034eb54982809dfd8cb6ff`

**Release ZIP SHA-256:** Use `verification/RELEASE_ZIP_SHA256.txt` after `npm run package:release-zip` (this README is inside the ZIP, so the outer digest changes if packaged text changes). Freeze-time host-verified release ZIP digest: `78cc64e96219fffa43058bb79bbf0007efe624ad18cb42edd327b1aaf2d8f05c`. Full detail: `verification/RENDER_REPORT.md`.

## Proxy / localhost troubleshooting

A prior render failure was caused by proxy settings interfering with localhost access during Remotion rendering.

The render wrapper hardens against this by setting:

- `NO_PROXY`
- `no_proxy`
- `--ipv4`
- `--timeout=120000`
- `--concurrency=1`

If render fails in an environment with corporate or shell-level proxies:

1. Inspect `HTTP_PROXY`, `HTTPS_PROXY`, `http_proxy`, `https_proxy`
2. Ensure `localhost` and `127.0.0.1` are excluded through `NO_PROXY` and `no_proxy`
3. Re-run through `scripts/render.sh` rather than invoking the raw Remotion command directly
4. Verify Chrome detection on that machine if a browser binary is not auto-resolved

## Lint

```bash
npm run lint
```

Runs `tsc --noEmit`.

## Deterministic guarantee

Project source must not use `Math.random()`. All jitter and analog-feeling motion are generated through seeded frame-based logic (`src/lib/deterministic.ts`) so repeated renders from the same source remain reproducible. (Tooling under `node_modules/` may use randomness; that is outside this package’s source contract.)

## Core authored documents

- `BUILD_CONTRACT.md` — executable build contract
- `CLAUDE.md` — repo-local operating overlay
- `DIRECTORS_TREATMENT.md` — concept, staging, and motion direction
- `LYRICS_TIMECODE.md` — lyric and caption timing map
- `VISUAL_INVARIANTS.md` — non-drifting style rules

## Truth discipline

This package can exist before the MP4 exists. The code and documents are source artifacts. The rendered video and ZIP archives only exist after local execution of the relevant commands.

## Release hardening checklist

- [x] Reprint live tree and final file contents from the rendering machine
- [x] Add README sections for render, verification, packaging, and proxy troubleshooting
- [x] Create second distributable ZIP that includes `dist/im-just-a-build.mp4`
- [x] Keep current source ZIP behavior (exclude `dist/`)
- [x] Record SHA256 for the release ZIP (`verification/RELEASE_ZIP_SHA256.txt`)
- [x] Keep frame hashing at spot-check default
- [x] Mark cross-machine reproducibility as unverified until separately proven
