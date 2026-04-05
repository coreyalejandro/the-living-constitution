#!/usr/bin/env bash
# Deterministic standalone twin path resolution for FDE control-plane dual topology.
set -euo pipefail

REPORT=""
while [[ $# -gt 0 ]]; do
  case "$1" in
    --report)
      REPORT="${2:?}"
      shift 2
      ;;
    *)
      echo "Usage: $0 --report <path.json>" >&2
      exit 2
      ;;
  esac
done

ROOT="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
export RESOLVE_ROOT="$ROOT"
export RESOLVE_REPORT="$REPORT"

python3 <<'PY'
import json
import os
from pathlib import Path

root = Path(os.environ["RESOLVE_ROOT"]).resolve()
report_path = Path(os.environ["RESOLVE_REPORT"])

candidates: list[str] = []
bb = root / "projects" / "backboardai-fde"
if bb.is_dir():
    candidates.append("projects/backboardai-fde")

blocking = ""
resolved = ""
status = "UNRESOLVED_REQUIRED_INPUT"

if len(candidates) == 0:
    blocking = (
        "No candidate directories found (e.g. projects/backboardai-fde). "
        "MASTER_PROJECT_INVENTORY.json does not record an FDE standalone twin path."
    )
elif len(candidates) > 1:
    blocking = (
        "Multiple candidate paths detected; cannot select a unique twin without "
        "explicit maintainer designation."
    )
else:
    p = candidates[0]
    marker = root / p / "BUILD_CONTRACT"
    if marker.is_file() and marker.stat().st_size == 0:
        blocking = (
            f"Candidate {p} exists but contains only an empty BUILD_CONTRACT placeholder; "
            "not a governance-complete standalone twin artifact set."
        )
    else:
        resolved = p
        status = "RESOLVED"

out = {
    "tool": "resolve_fde_standalone_path.sh",
    "schema_version": "1.0.0",
    "resolution_status": status,
    "standalone_path": resolved if status == "RESOLVED" else None,
    "candidates": candidates,
    "blocking_rationale": blocking if status != "RESOLVED" else None,
    "repo_root": str(root),
}
report_path.parent.mkdir(parents=True, exist_ok=True)
report_path.write_text(json.dumps(out, indent=2) + "\n", encoding="utf-8")
print(json.dumps({"overall": status, "report": str(report_path)}, indent=2))
PY
