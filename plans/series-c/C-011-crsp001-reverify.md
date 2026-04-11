# C-011: CRSP-001 Re-Verification

## Goal

Re-verify Guardian Kernel constitutional enforcement against current TLC state
using existing machine-checkable acceptance surfaces.

## Scope

- Re-run health and invariant checks for `src/guardian.py`.
- Re-run governance and institutionalization verifiers tied to CRSP evidence.
- Confirm paired artifact and helper-pollution controls still hold.

## Verification Gates

- `python3 src/guardian.py --health-check`
- `python3 scripts/test_guardian_invariants.py --invariant INVARIANT_ARTICLE_IV_01`
- `python3 scripts/test_guardian_readonly.py`
- `python3 scripts/verify_governance_chain.py --root .`
- `python3 scripts/verify_institutionalization.py --root .`
- `./scripts/verify_crsp_template_bundle.sh`

## Definition of Done

- All gate commands exit `0`.
- No contradictory status claim is introduced in CRSP artifacts.
