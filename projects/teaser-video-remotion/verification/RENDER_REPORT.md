# Render verification report — I'm Just a Build

**Contract:** C-RSP v1.0.0 render stabilization + verification pass  
**Date:** 2026-03-31  
**Host:** Darwin arm64, Node v22.17.0  

## Canonical release posture

Authoritative distributables (project root, after packaging commands):

| Artifact | Use |
|----------|-----|
| `im-just-a-build-release.zip` | Sharing the **rendered deliverable** (MP4 + designated evidence). |
| `im-just-a-build-source.zip` | **Governance**, source review, and reproducibility work (no `dist/`). |

## Canonical verified artifact identities (originating host)

**MP4 (stable identity):**

| Artifact | SHA-256 |
|----------|---------|
| `dist/im-just-a-build.mp4` | `35c28f8f0fb82a51ceba7c89415afc91c8dd739dec034eb54982809dfd8cb6ff` |

**Release ZIP:** `README.md` and this report are **inside** `im-just-a-build-release.zip`, so any edit to those packaged files changes the outer ZIP digest. The **authoritative** digest is always the value in `verification/RELEASE_ZIP_SHA256.txt` immediately after `npm run package:release-zip` (verify with `shasum -a 256 im-just-a-build-release.zip`).

**Host-verified release ZIP SHA-256** recorded at release-hardened freeze (before further documentation-only churn to packaged files): `78cc64e96219fffa43058bb79bbf0007efe624ad18cb42edd327b1aaf2d8f05c`.

(Re-check `verification/OUTPUT_SHA256.txt`, `verification/RELEASE_ZIP_SHA256.txt`, and `verification/im-just-a-build.mp4.sha256` after any re-render or re-package.)

## Release decision record

Packaging and verification policy for this subproject is settled as:

- **Source ZIP** excludes `dist/`.
- **Release ZIP** includes the MP4 and designated evidence files (`RENDER_REPORT.md`, `*.sha256`, `README.md`, `LICENSE`).
- **Frame verification** remains **spot-check** default (not full-frame as the default release gate).
- **Cross-machine reproducibility** remains **explicitly unverified** until separately proven.

No additional discovery is required for this release position.

## Summary

- **Lint:** `npm run lint` — pass (exit 0).
- **Preflight:** `scripts/preflight-render-check.sh` — pass (exit 0).
- **Composition:** `ImJustABuild` listed as 1080x1080, 12 fps, 720 frames (60.00 sec).
- **Determinism:** No `Math.random` string under `src/` (see `src/lib/deterministic.ts`; jitter is seeded).
- **Render:** `npm run render` — **success** after minimal `scripts/render.sh` correction for local proxy behavior.

## First failure (diagnosed)

**Symptom:** `Error: Visited "http://localhost:3001/index.html" but got no response.`  
**Cause:** A system HTTP(S) proxy caused Chromium’s navigation to the Remotion bundle server on localhost to fail.  
**Fix (minimal):** `scripts/render.sh` now appends `127.0.0.1` and `localhost` to `NO_PROXY` and `no_proxy`, and passes `--ipv4`, `--timeout=120000`, `--concurrency=1`, and `--browser-executable` when a known Chrome/Chromium path exists.

## Output proof

| Check | Result |
|--------|--------|
| File | `dist/im-just-a-build.mp4` |
| Size | 5,694,049 bytes (host measurement) |
| SHA-256 | `35c28f8f0fb82a51ceba7c89415afc91c8dd739dec034eb54982809dfd8cb6ff` |
| ffprobe (video) | width=1080 height=1080 r_frame_rate=12/1 nb_frames=720 duration≈60s |

Spot-check frame hashes (raw RGB24): see `verification/FRAME_HASHES.txt`.

## ZIP

Two distributables at project root:

| Archive | Command | Contents policy |
|---------|---------|-------------------|
| `im-just-a-build-source.zip` | `npm run package:zip` | Full source + governance + verification; excludes `node_modules` and `dist` (MP4 not in archive). Legacy name: `im-just-a-build-crsp-package.zip` (same exclusion policy). |
| `im-just-a-build-release.zip` | `npm run package:release-zip` | `dist/im-just-a-build.mp4`, `verification/RENDER_REPORT.md`, `verification/*.sha256`, `README.md`, `LICENSE`. Digest recorded in `verification/RELEASE_ZIP_SHA256.txt`. |

## Artifacts

| Artifact | Role |
|----------|------|
| `verification/ENVIRONMENT.txt` | Tool versions and host note |
| `verification/COMMAND_LOG.txt` | Commands and failure/retry narrative |
| `verification/OUTPUT_SHA256.txt` | MP4 digest |
| `verification/FRAME_HASHES.txt` | Spot-check frame content hashes |
| `verification/RENDER_EVIDENCE.json` | Machine-readable pass record |
| `verification/RELEASE_ZIP_SHA256.txt` | SHA-256 of `im-just-a-build-release.zip` after `npm run package:release-zip` |
| `verification/im-just-a-build.mp4.sha256` | GNU-style digest line for `dist/im-just-a-build.mp4` (release package input) |
