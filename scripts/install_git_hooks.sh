#!/usr/bin/env bash
# Point this repo at tracked hooks under .githooks/ (documentation constitution on commit).
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
git config core.hooksPath .githooks
chmod +x .githooks/pre-commit 2>/dev/null || true
echo "core.hooksPath set to .githooks (pre-commit runs verify_document_constitution.py)"
echo "Ensure: pip install -r requirements-verify.txt"
