#!/usr/bin/env bash
# Local-only: creates a distributable archive of this package (excludes heavy dirs).
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
# Source package: excludes dist/ and node_modules/ (reproducible source + governance + verification).
# Legacy filename was im-just-a-build-crsp-package.zip; content policy unchanged.
OUT="im-just-a-build-source.zip"
rm -f "$OUT"

zip -r "$OUT" . \
  -x "*.zip" \
  -x "node_modules/*" \
  -x "dist/*" \
  -x ".DS_Store"

echo "package-zip.sh: wrote ${ROOT}/${OUT}"
