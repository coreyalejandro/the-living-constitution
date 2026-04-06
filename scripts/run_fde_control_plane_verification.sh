#!/usr/bin/env bash
# Single entrypoint: standalone path resolution + structural + schema + promotion-readiness.
# Use locally or from CI. Exits non-zero on first failing verifier.
#
# Usage:
#   ./scripts/run_fde_control_plane_verification.sh
#   ./scripts/run_fde_control_plane_verification.sh --skip-resolve   # reuse existing standalone-path-resolution.json
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

SKIP_RESOLVE=0
while [[ $# -gt 0 ]]; do
  case "$1" in
    --skip-resolve)
      SKIP_RESOLVE=1
      shift
      ;;
    -h | --help)
      echo "Usage: $0 [--skip-resolve]"
      exit 0
      ;;
    *)
      echo "Unknown option: $1" >&2
      exit 2
      ;;
  esac
done

echo "==> FDE control plane C-RSP verification (root: ${ROOT})"

if [[ "${SKIP_RESOLVE}" -eq 0 ]]; then
  echo "==> [1/4] Standalone path resolution"
  bash scripts/resolve_fde_standalone_path.sh \
    --report evidence/fde-control-plane/standalone-path-resolution.json
else
  echo "==> [1/4] Standalone path resolution (skipped)"
fi

echo "==> [2/4] Structural diff (template vs instance)"
python3 scripts/verify_crsp_structure.py \
  --template projects/c-rsp/BUILD_CONTRACT.md \
  --instance projects/c-rsp/instances/CRSP-FDE-CTRL-PLANE-GAPS-002.md \
  --report evidence/fde-control-plane/structural-diff-report.json

echo "==> [3/4] Schema validation"
python3 scripts/verify_fde_control_plane.py \
  --schemas schemas/fde-lifecycle.schema.json schemas/blind-man-execution.schema.json \
  --report evidence/fde-control-plane/schema-validation-report.json

echo "==> [4/4] Promotion readiness (dual-topology-verifier)"
python3 scripts/verify_fde_control_plane.py \
  --promotion-readiness \
  --lock projects/c-rsp/governance-template.lock.json \
  --instance projects/c-rsp/instances/CRSP-FDE-CTRL-PLANE-GAPS-002.md \
  --report evidence/fde-control-plane/verifier-execution-report.json

echo "==> All FDE control plane verification steps passed."
