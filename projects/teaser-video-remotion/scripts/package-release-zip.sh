#!/usr/bin/env bash
# Local-only: release archive with rendered MP4 + verification evidence (no node_modules).
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
OUT="im-just-a-build-release.zip"
MP4="dist/im-just-a-build.mp4"

if [[ ! -f "$MP4" ]]; then
  echo "package-release-zip.sh: FAIL — missing ${MP4} (run npm run render first)"
  exit 1
fi
if [[ ! -f README.md ]] || [[ ! -f LICENSE ]]; then
  echo "package-release-zip.sh: FAIL — README.md and LICENSE are required for release packaging"
  exit 1
fi
if [[ ! -f verification/RENDER_REPORT.md ]]; then
  echo "package-release-zip.sh: FAIL — missing verification/RENDER_REPORT.md"
  exit 1
fi

shopt -s nullglob
SHA_FILES=(verification/*.sha256)
shopt -u nullglob
if [[ ${#SHA_FILES[@]} -eq 0 ]]; then
  echo "package-release-zip.sh: FAIL — no verification/*.sha256 files (create at least im-just-a-build.mp4.sha256)"
  exit 1
fi

rm -f "$OUT"
zip "$OUT" \
  "$MP4" \
  verification/RENDER_REPORT.md \
  README.md \
  LICENSE \
  "${SHA_FILES[@]}"

shasum -a 256 "$OUT" | tee verification/RELEASE_ZIP_SHA256.txt
echo "package-release-zip.sh: wrote ${ROOT}/${OUT}"
echo "package-release-zip.sh: recorded digest in verification/RELEASE_ZIP_SHA256.txt"
