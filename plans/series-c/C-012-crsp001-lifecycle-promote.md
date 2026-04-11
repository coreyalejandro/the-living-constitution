# C-012: CRSP-001 Lifecycle Promotion

## Goal

Advance CRSP-001 lifecycle state only after re-verification evidence is complete.

## Scope

- Validate that CRSP re-verification contract is completed in state machine.
- Run lifecycle status checks and ensure no illegal transition is attempted.
- Record promotion evidence in governance truth surfaces.

## Verification Gates

- `python3 scripts/series_contract_orchestrator.py status --series series-c --root .`
- `python3 -c "import json; d=json.load(open('CRSP-001.json')); assert d.get('status') in {'Active','Frozen','Superseded'}"`
- `python3 -c "import json; d=json.load(open('CRSP-001.json')); assert d.get('sections',{}).get('lifecycle_state_machine',{}).get('current_state') in {'Draft','Active','Frozen','Superseded'}"`
- `python3 scripts/verify_governance_chain.py --root .`

## Definition of Done

- Lifecycle status remains internally consistent with evidence.
- Promotion summary is recorded in handoff/project notes before merge.
