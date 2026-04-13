# Series C Low-Capability Agent Playbook

This playbook is optimized for simple agents that need deterministic steps.

## Allowed Workflow

1. Show contract queue:
   - `python3 scripts/series_contract_orchestrator.py status --series series-c --root .`
2. Start next contract only through orchestrator:
   - `python3 scripts/series_contract_orchestrator.py start-next --series series-c --root .`
3. Work only on the active contract.
4. Complete contract through orchestrator (runs hard gates first):
   - `python3 scripts/series_contract_orchestrator.py complete --series series-c --id <CONTRACT_ID> --root .`

## Non-Negotiable Rules

- Never mark a contract complete manually in `CONTRACT_STATE.json`.
- Never activate a new contract while another is active.
- Never skip gate commands in `completion_gates`.
- If a gate fails, stop and fix the failure before retrying completion.

## Output Discipline

Every execution summary must include:

- Exists
- Verified against
- Not claimed
- Non-existent
- Unverified
- Functional status
