# C-RSP — Conflict / operations log (teaser-video-remotion)

Append-only operational notes for this subproject. Does not override TLC root governance verifiers unless explicitly wired.

---

## 2026-03-31 — Render stabilization (host-verified MP4)

**Invariant context:** INVARIANT_07 — MP4 success only with file at `dist/im-just-a-build.mp4` after successful render.

| Phase | Observation | Action |
|--------|-------------|--------|
| Initial render | `Visited "http://localhost:3001/index.html" but got no response` | Diagnosed proxy breaking localhost bundle URL |
| Correction | — | `scripts/render.sh`: `NO_PROXY`/`no_proxy` for `127.0.0.1,localhost`; `--ipv4`; `--timeout=120000`; `--concurrency=1`; optional `--browser-executable` |
| Retry | Render completed 720/720; FFmpeg stitched; MP4 written | Pass |

**Breach check:** No BREACH-A/B/C/D/E/F — evidence files correspond to commands run; dependency install from `package-lock.json` unchanged.

---
