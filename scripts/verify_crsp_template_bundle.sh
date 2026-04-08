#!/usr/bin/env bash
# AC-007: Paired Artifact Bundle Verification for CRSP-001
# Verifies that the canonical paired artifacts and evidence files exist and
# are structurally valid before the Guardian Kernel contract can advance to
# Active status.
#
# Exit codes: 0 = all checks pass | 1 = one or more checks failed

set -uo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

FAIL=0

pass() { printf '[PASS] %s\n' "$1"; }
fail() { printf '[FAIL] %s\n' "$1"; FAIL=1; }

# PF-001: CRSP-001.json exists at TLC root
if [ -f "CRSP-001.json" ]; then
    pass "PF-001  CRSP-001.json exists"
else
    fail "PF-001  CRSP-001.json not found at TLC root"
fi

# PF-002: CRSP-001.md exists at TLC root
if [ -f "CRSP-001.md" ]; then
    pass "PF-002  CRSP-001.md exists"
else
    fail "PF-002  CRSP-001.md not found at TLC root"
fi

# PF-003: CRSP-001.json is valid JSON
if [ -f "CRSP-001.json" ]; then
    if python3 -c "import json, sys; json.load(open('CRSP-001.json'))" 2>/dev/null; then
        pass "PF-003  CRSP-001.json is valid JSON"
    else
        fail "PF-003  CRSP-001.json failed JSON parse"
    fi
else
    fail "PF-003  CRSP-001.json missing — cannot validate JSON"
fi

# PF-004: CRSP-001.md contains legal disclaimer phrase "legally void"
if [ -f "CRSP-001.md" ]; then
    if grep -q "legally void" "CRSP-001.md"; then
        pass "PF-004  CRSP-001.md contains legal disclaimer (\"legally void\")"
    else
        fail "PF-004  CRSP-001.md missing legal disclaimer phrase \"legally void\""
    fi
else
    fail "PF-004  CRSP-001.md missing — cannot check legal disclaimer"
fi

# PF-005a: verification/crsp_CRSP-001_log.json exists
if [ -f "verification/crsp_CRSP-001_log.json" ]; then
    pass "PF-005a verification/crsp_CRSP-001_log.json exists"
else
    fail "PF-005a verification/crsp_CRSP-001_log.json not found"
fi

# PF-005b: verification/crsp_CRSP-001_rationale.md exists
if [ -f "verification/crsp_CRSP-001_rationale.md" ]; then
    pass "PF-005b verification/crsp_CRSP-001_rationale.md exists"
else
    fail "PF-005b verification/crsp_CRSP-001_rationale.md not found"
fi

echo "---"
if [ "$FAIL" -eq 0 ]; then
    echo "AC-007 PASS — all paired-artifact bundle checks passed"
    exit 0
else
    echo "AC-007 FAIL — one or more checks failed (see [FAIL] lines above)"
    exit 1
fi
