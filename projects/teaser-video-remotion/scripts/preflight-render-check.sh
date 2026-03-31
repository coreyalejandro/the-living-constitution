#!/usr/bin/env bash
# C-RSP preflight: environment + assets + lint + compositions + determinism scan.
# Exit non-zero on any failure.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

REQUIRED=(
  package.json
  package-lock.json
  tsconfig.json
  remotion.config.ts
  src/index.ts
  src/Root.tsx
  src/composition/VideoConfig.ts
  scripts/render.sh
)

echo "preflight: working directory: $ROOT"

for f in "${REQUIRED[@]}"; do
  if [[ ! -f "$f" ]]; then
    echo "preflight: FAIL — missing required file: $f"
    exit 1
  fi
done

if ! node -e "const p=require('./package.json'); if(p.name!=='teaser-video-remotion') process.exit(1)"; then
  echo "preflight: FAIL — package.json name must be teaser-video-remotion"
  exit 1
fi

for cmd in node npm ffmpeg; do
  if ! command -v "$cmd" >/dev/null 2>&1; then
    echo "preflight: FAIL — $cmd not on PATH"
    exit 1
  fi
done

echo "preflight: running npm run lint ..."
if ! npm run lint; then
  echo "preflight: FAIL — npm run lint"
  exit 1
fi

echo "preflight: composition discovery ..."
COMP_OUT="$(mktemp)"
if ! npx remotion compositions src/index.ts 2>&1 | tee "$COMP_OUT"; then
  echo "preflight: FAIL — remotion compositions"
  rm -f "$COMP_OUT"
  exit 1
fi
if ! grep -q 'ImJustABuild' "$COMP_OUT"; then
  echo "preflight: FAIL — composition ImJustABuild not listed"
  rm -f "$COMP_OUT"
  exit 1
fi
if ! grep -q '1080x1080' "$COMP_OUT" || ! grep -q '720' "$COMP_OUT"; then
  echo "preflight: FAIL — expected 1080x1080 and 720 frames in composition listing"
  rm -f "$COMP_OUT"
  exit 1
fi
rm -f "$COMP_OUT"

echo "preflight: scanning src/ for Math.random ..."
if rg -q 'Math\.random' src/ 2>/dev/null; then
  echo "preflight: FAIL — Math.random reference found under src/"
  exit 1
fi

echo "preflight: PASS"
exit 0
