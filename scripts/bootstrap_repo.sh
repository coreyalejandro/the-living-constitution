#!/usr/bin/env bash
set -euo pipefail

echo "[BOOTSTRAP] Ensuring full clone integrity"

# Detect shallow clone
if git rev-parse --is-shallow-repository | grep -q true; then
  echo "[BOOTSTRAP] Deepening shallow clone"
  git fetch --unshallow
fi

# Fetch full tags
git fetch --tags --force --prune

# Initialize submodules
git submodule update --init --recursive

# Verify tags exist
if [ -z "$(git tag --list)" ]; then
  echo "BREACH: NO_TAGS_AVAILABLE"
  exit 1
fi

echo "[BOOTSTRAP] Complete"
