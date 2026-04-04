#!/usr/bin/env bash
# C-RSP next-build launcher: reads projects/c-rsp/NEXT_CRSP_BUILD.json and prints follow-on instructions.
set -euo pipefail

ROOT="$(git rev-parse --show-toplevel 2>/dev/null || true)"
if [[ -z "${ROOT}" ]]; then
  echo "crsp_next_build: run from inside the-living-constitution git repo" >&2
  exit 2
fi

JSON="${ROOT}/projects/c-rsp/NEXT_CRSP_BUILD.json"
if [[ ! -f "${JSON}" ]]; then
  echo "crsp_next_build: missing ${JSON}" >&2
  exit 3
fi

python3 - "${JSON}" <<'PY'
import json, sys
path = sys.argv[1]
with open(path, encoding="utf-8") as f:
    p = json.load(f)
status = p.get("status", "unknown")
inst = p.get("next_instance_path", "")
cid = p.get("contract_id", "")
print(f"NEXT_CRSP_BUILD status={status}")
if inst:
    print(f"instance_path={inst}")
if cid:
    print(f"contract_id={cid}")
print()
print("AUTO_LAUNCH: start next C-RSP session against instance_path; run that instance's Preflight; execute to PASS or recorded HALT.")
print("Template: projects/c-rsp/CRSP_OUTCOME_TEMPLATE.md | V&T: projects/c-rsp/BUILD_CONTRACT.md Section 16")
PY
