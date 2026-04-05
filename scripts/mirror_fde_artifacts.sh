#!/usr/bin/env bash
# Copy governed FDE integrated artifacts into the in-repo standalone twin tree
# (projects/backboardai-fde/). Default: dry-run. Use --apply to write files.
#
# Usage:
#   ./scripts/mirror_fde_artifacts.sh           # dry-run (lists planned copies)
#   ./scripts/mirror_fde_artifacts.sh --apply   # perform copies
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

TWIN="${ROOT}/projects/backboardai-fde"
APPLY=false

while [[ $# -gt 0 ]]; do
  case "$1" in
    --apply)
      APPLY=true
      shift
      ;;
    -h | --help)
      echo "Usage: $0 [--apply]"
      echo "  Dry-run by default; --apply writes into projects/backboardai-fde/"
      exit 0
      ;;
    *)
      echo "Unknown option: $1" >&2
      exit 2
      ;;
  esac
done

copy_tree() {
  local src="$1"
  local dst="$2"
  if [[ ! -e "$src" ]]; then
    echo "SKIP (missing source): $src"
    return 0
  fi
  mkdir -p "$dst"
  if $APPLY; then
    if command -v rsync >/dev/null 2>&1; then
      rsync -a --delete "${src}/" "${dst}/"
    else
      mkdir -p "$dst"
      find "$dst" -mindepth 1 -delete
      cp -R "${src}/." "${dst}/"
    fi
    echo "APPLIED: $src -> $dst"
  else
    echo "DRY-RUN would sync: $src -> $dst"
  fi
}

copy_file() {
  local src="$1"
  local dst="$2"
  if [[ ! -f "$src" ]]; then
    echo "SKIP (missing source): $src"
    return 0
  fi
  mkdir -p "$(dirname "$dst")"
  if $APPLY; then
    cp "$src" "$dst"
    echo "APPLIED: $src -> $dst"
  else
    echo "DRY-RUN would copy: $src -> $dst"
  fi
}

echo "==> FDE artifact mirror (twin root: ${TWIN})"
if ! $APPLY; then
  echo "    (dry-run; pass --apply to write)"
fi

# Directory mirrors
copy_tree "${ROOT}/docs/fde-control-plane" "${TWIN}/docs/fde-control-plane"
copy_tree "${ROOT}/evidence/fde-control-plane" "${TWIN}/evidence/fde-control-plane"

# Single files
copy_file "${ROOT}/governance-rules/fde-lifecycle-invariants.yaml" \
  "${TWIN}/governance-rules/fde-lifecycle-invariants.yaml"
copy_file "${ROOT}/schemas/fde-lifecycle.schema.json" \
  "${TWIN}/schemas/fde-lifecycle.schema.json"
copy_file "${ROOT}/schemas/blind-man-execution.schema.json" \
  "${TWIN}/schemas/blind-man-execution.schema.json"

echo "==> Mirror complete ($($APPLY && echo apply || echo dry-run))."
