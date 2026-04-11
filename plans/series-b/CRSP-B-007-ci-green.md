# CRSP-B-007: CI Green + Final Verification

## Contract Identity

| Field | Value |
|-------|-------|
| Contract ID | CRSP-B-007 |
| Series | Series B — Fellowship-Ready Refactor |
| Title | CI Green + Final Verification |
| Depends On | All previous contracts (B-001 through B-006) |
| Completion Marker | `plans/series-b/.done-B-007` |
| Branch | `claude/refactor-repo-voice-UEFMp` |

## Pre-Flight Check

```bash
for i in 001 002 003 004 005 006; do
  test -f "plans/series-b/.done-B-$i" || { echo "BLOCKED: CRSP-B-$i not complete"; exit 1; }
done
echo "All prerequisites met"
```

## Why This Contract Exists

All the previous contracts changed files. This contract verifies that everything still works together. It runs every verifier, fixes any breakage from the refactor, ensures CI will pass, and produces a final state report.

## Pre-Flight Reads (MANDATORY)

1. `.github/workflows/verify.yml` — the entire CI workflow
2. `scripts/verify_governance_chain.py` — understand what it checks
3. `scripts/verify_document_constitution.py` — understand MVDS checks
4. `scripts/verify_project_topology.py` — understand topology checks
5. `scripts/render_status_surface.py` — understand status rendering
6. `config/docs_governance.json` — the MVDS configuration
7. `requirements-verify.txt` — verification dependencies
8. `STATUS.json` — current state after all previous contracts

## Ordered Operations

### OP-1: Install verification dependencies

```bash
pip install -r requirements-verify.txt
pip install -r requirements-dev.txt
```

### OP-2: Run bootstrap

```bash
./scripts/bootstrap_repo.sh
```

If this fails, diagnose and fix. Common issues:
- Submodule init failures (network or access)
- Shallow clone issues

### OP-3: Run document constitution verifier

```bash
python3 scripts/verify_document_constitution.py --root .
```

If this fails, it's likely because:
- Files moved by B-005 or B-006 are referenced in `config/docs_governance.json`
- YAML frontmatter was removed from README by B-004
- Files renamed from `01-anthropic/` to `research/` by B-006

**Fix approach:** Update `config/docs_governance.json` MVDS paths to match new file locations. If the config references `01-anthropic/`, change to `research/`. If it references files that moved to `projects/specifications/`, update paths.

### OP-4: Run project topology verifier

```bash
python3 scripts/verify_project_topology.py --root .
```

If this fails, it's because B-005 moved project folders. Fix `MASTER_PROJECT_INVENTORY.json` to match new paths, or update the verifier as specified in B-005.

### OP-5: Run governance chain verifier

```bash
python3 scripts/verify_governance_chain.py --root .
```

This is the most comprehensive verifier. If it fails, read the error output carefully. Common issues after refactor:
- Role registry paths don't match moved files
- Enforcement map references old paths
- Governance artifacts reference `01-anthropic/`

Fix each issue at the source. Do not modify the verifier to skip checks.

### OP-6: Render status surface

```bash
python3 scripts/render_status_surface.py --root .
```

This regenerates `STATUS.json` and `STATUS.md`. After all fixes, the status should show fewer failures than before Series B.

### OP-7: Run the test suite

```bash
pytest tests/ -v --tb=short 2>&1 | tee plans/series-b/B-007-final-test-output.txt
```

All tests from B-002 must still pass.

### OP-8: Run compliance scorer

```bash
python3 scripts/compliance_score_docs.py --root . --json-out verification/docs_compliance.json
```

### OP-9: Simulate CI locally

Run the exact same steps CI runs, in order:

```bash
# 1. Bootstrap
./scripts/bootstrap_repo.sh

# 2. Document constitution
python3 scripts/verify_document_constitution.py --root .

# 3. Compliance
python3 scripts/compliance_score_docs.py --root . --json-out verification/docs_compliance.json

# 4. Render STATUS
python3 scripts/render_status_surface.py --root .

# 5. Base camp structure
test -f CLAUDE.md
test -f THE_LIVING_CONSTITUTION.md

# 6. Project topology
python3 scripts/verify_project_topology.py --root . --with-governance

# 7. Governance chain
python3 scripts/verify_governance_chain.py --root .

# 8. Institutionalization
python3 scripts/verify_institutionalization.py --root .

# 9. Tests
pytest tests/ -v
```

Fix any failures. Each fix gets its own commit with a clear message.

### OP-10: Write final state report

Create `plans/series-b/SERIES_B_FINAL_REPORT.md`:

```markdown
# Series B Final Report

## Contracts Executed

| Contract | Title | Status |
|----------|-------|--------|
| CRSP-B-001 | Fix Broken Invariants | COMPLETE |
| CRSP-B-002 | Real Test Suite | COMPLETE |
| CRSP-B-003 | Clean Constitution | COMPLETE |
| CRSP-B-004 | README Rewrite | COMPLETE |
| CRSP-B-005 | Consolidate Projects | COMPLETE |
| CRSP-B-006 | Fellowship Surface | COMPLETE |
| CRSP-B-007 | CI Green | COMPLETE |

## Verification Results

(paste stdout from each verifier run)

## Test Results

(paste pytest output summary)

## Files Changed

(paste git diff --stat from main)

## Remaining Issues

(list anything that could not be fixed and why)
```

### OP-11: Push

```bash
git push -u origin claude/refactor-repo-voice-UEFMp
```

If push fails, retry up to 4 times with exponential backoff (2s, 4s, 8s, 16s).

## Acceptance Criteria

| AC | Requirement | Verification |
|----|-------------|--------------|
| AC-001 | Document constitution verifier passes | exit 0 |
| AC-002 | Project topology verifier passes | exit 0 |
| AC-003 | Governance chain verifier passes | exit 0 |
| AC-004 | Status surface renders without error | exit 0 |
| AC-005 | Pytest suite passes (25+ tests) | pytest output |
| AC-006 | Final report written | `test -f plans/series-b/SERIES_B_FINAL_REPORT.md` |
| AC-007 | Branch pushed to origin | `git log origin/claude/refactor-repo-voice-UEFMp --oneline -1` shows latest commit |
| AC-008 | CLAUDE.md, THE_LIVING_CONSTITUTION.md, README.md all exist and are non-empty | file checks |

## Completion

```bash
echo "CRSP-B-007 COMPLETE" > plans/series-b/.done-B-007
git add plans/series-b/ verification/ STATUS.json STATUS.md
git commit -m "verify: Series B complete — all verifiers pass, tests green, branch pushed

Series B contract CRSP-B-007. Full verification sweep after refactor.
Document constitution, project topology, governance chain, compliance
score, and pytest suite all passing."
git push -u origin claude/refactor-repo-voice-UEFMp
```
