#!/usr/bin/env bash
# Series B Contract Runner
# Determines which contract to execute next based on completion markers.
# Usage: ./plans/series-b/run-next-contract.sh
#
# This script does NOT execute contracts. It tells you which one to run next
# and prints the contract file path so you can feed it to any model.

set -euo pipefail

SERIES_DIR="plans/series-b"

# Contract dependency graph:
# B-001: no deps
# B-002: depends on B-001
# B-003: depends on B-001
# B-004: depends on B-003
# B-005: depends on B-001
# B-006: depends on B-004 AND B-005
# B-007: depends on ALL

check_done() {
  test -f "$SERIES_DIR/.done-B-$1"
}

print_contract() {
  local id="$1"
  local file="$2"
  local title="$3"
  echo "========================================="
  echo "NEXT CONTRACT: CRSP-B-${id}"
  echo "TITLE: ${title}"
  echo "FILE: ${SERIES_DIR}/${file}"
  echo "========================================="
  echo ""
  echo "To execute, give any AI model this prompt:"
  echo ""
  echo "---"
  echo "Read the file '${SERIES_DIR}/${file}' in this repository."
  echo "Execute every Ordered Operation in sequence."
  echo "Verify every Acceptance Criterion."
  echo "Write the completion marker when done."
  echo "Commit with the exact message specified."
  echo "Do not skip steps. Do not improvise."
  echo "---"
}

# Check B-001
if ! check_done "001"; then
  print_contract "001" "CRSP-B-001-fix-broken-invariants.md" "Fix Broken Invariants"
  exit 0
fi

# B-002, B-003, B-005 can run in parallel after B-001
# Find which ones are not done
PARALLEL_READY=()
if ! check_done "002"; then
  PARALLEL_READY+=("002|CRSP-B-002-real-test-suite.md|Real Test Suite")
fi
if ! check_done "003"; then
  PARALLEL_READY+=("003|CRSP-B-003-clean-constitution.md|Clean THE_LIVING_CONSTITUTION.md")
fi
if ! check_done "005"; then
  PARALLEL_READY+=("005|CRSP-B-005-consolidate-projects.md|Consolidate Dead-Weight Project Folders")
fi

if [ ${#PARALLEL_READY[@]} -gt 0 ]; then
  echo "========================================="
  echo "PARALLEL-ELIGIBLE CONTRACTS (run any/all):"
  echo "========================================="
  for entry in "${PARALLEL_READY[@]}"; do
    IFS="|" read -r id file title <<< "$entry"
    echo ""
    echo "  CRSP-B-${id}: ${title}"
    echo "  FILE: ${SERIES_DIR}/${file}"
  done
  echo ""
  echo "These can run in parallel or sequentially."
  echo "Pick one and give it to any model with the standard prompt."
  exit 0
fi

# B-004 depends on B-003
if ! check_done "004"; then
  if check_done "003"; then
    print_contract "004" "CRSP-B-004-readme-rewrite.md" "README Rewrite (Research-First)"
  else
    echo "BLOCKED: CRSP-B-004 waiting on CRSP-B-003"
  fi
  exit 0
fi

# B-006 depends on B-004 AND B-005
if ! check_done "006"; then
  if check_done "004" && check_done "005"; then
    print_contract "006" "CRSP-B-006-fellowship-surface.md" "Fellowship-Ready Surface"
  else
    echo "BLOCKED: CRSP-B-006 waiting on:"
    check_done "004" || echo "  - CRSP-B-004"
    check_done "005" || echo "  - CRSP-B-005"
  fi
  exit 0
fi

# B-007 depends on ALL
if ! check_done "007"; then
  ALL_DONE=true
  for i in 001 002 003 004 005 006; do
    check_done "$i" || ALL_DONE=false
  done
  if $ALL_DONE; then
    print_contract "007" "CRSP-B-007-ci-green.md" "CI Green + Final Verification"
  else
    echo "BLOCKED: CRSP-B-007 waiting on:"
    for i in 001 002 003 004 005 006; do
      check_done "$i" || echo "  - CRSP-B-$(printf '%03d' $i)"
    done
  fi
  exit 0
fi

echo "========================================="
echo "SERIES B COMPLETE"
echo "========================================="
echo "All 7 contracts executed."
echo "Run: git log --oneline -10"
echo "Then: git push -u origin claude/refactor-repo-voice-UEFMp"
