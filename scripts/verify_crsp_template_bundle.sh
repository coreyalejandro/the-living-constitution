#!/usr/bin/env bash
# Verify canonical C-RSP master template section alignment against:
#   - guided instance template
#   - executed FDE gap-closure instance (when present)
#
# Note: verify_crsp_structure.py checks numbered section titles (0–17), not the prose inside
# Section 6 (e.g. §6A ordered-operations tables). Those remain human-review + contract discipline.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

OUT_DIR="${OUT_DIR:-verification/c-rsp-structure}"
mkdir -p "$OUT_DIR"

TEMPLATE="projects/c-rsp/BUILD_CONTRACT.md"
GUIDED="projects/c-rsp/BUILD_CONTRACT.instance.md"
FDE_INSTANCE="projects/c-rsp/instances/CRSP-FDE-CTRL-PLANE-GAPS-002.md"

echo "==> C-RSP structural verification (template vs instances)"

python3 scripts/verify_crsp_structure.py \
  --template "$TEMPLATE" \
  --instance "$GUIDED" \
  --report "$OUT_DIR/structural-guided.json"

python3 scripts/verify_crsp_structure.py \
  --template "$TEMPLATE" \
  --instance "$FDE_INSTANCE" \
  --report "$OUT_DIR/structural-fde-instance.json"

echo "==> C-RSP structural verification PASS"
