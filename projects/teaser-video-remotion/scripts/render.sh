#!/usr/bin/env bash
# Local-only: requires Node, npm, FFmpeg, and npm install in this directory.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

if ! command -v node >/dev/null 2>&1; then
  echo "render.sh: node is required on PATH"
  exit 1
fi
if ! command -v npm >/dev/null 2>&1; then
  echo "render.sh: npm is required on PATH"
  exit 1
fi
if ! command -v ffmpeg >/dev/null 2>&1; then
  echo "render.sh: ffmpeg is required on PATH for Remotion encoding"
  exit 1
fi

mkdir -p dist

# Remotion serves the bundle on localhost; a system HTTP(S)_PROXY can break Puppeteer's
# navigation to 127.0.0.1 (observed: "got no response"). Always bypass proxy for local bundle.
export NO_PROXY="${NO_PROXY:+$NO_PROXY,}127.0.0.1,localhost"
export no_proxy="${no_proxy:+$no_proxy,}127.0.0.1,localhost"

REMOTION_EXTRA=()
REMOTION_EXTRA+=(--ipv4)
REMOTION_EXTRA+=(--timeout=120000)
REMOTION_EXTRA+=(--concurrency=1)

if [[ -x "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" ]]; then
  REMOTION_EXTRA+=(--browser-executable "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome")
elif command -v google-chrome-stable >/dev/null 2>&1; then
  REMOTION_EXTRA+=(--browser-executable "$(command -v google-chrome-stable)")
elif command -v chromium >/dev/null 2>&1; then
  REMOTION_EXTRA+=(--browser-executable "$(command -v chromium)")
fi

exec npx remotion render src/index.ts ImJustABuild dist/im-just-a-build.mp4 "${REMOTION_EXTRA[@]}"
