# C-RSP Master Template v4.0 – Generic, Project-Agnostic Edition
C-RSP = Constitutionally-Regulated Single Pass.

## Purpose
A C-RSP contract is an executable governance contract for deterministic, single-pass AI-assisted build work. It binds an AI coding agent to constitutional constraints, machine-checkable halt conditions, evidence generation, lifecycle control, rollback semantics, and paired human-readable explanation.

## Authority
The constitutional authority set is defined by the JSON instance’s `authority_files` map. No hardcoded filenames are assumed. The contract itself (this file, stored as `BUILD_CONTRACT.md`) is the execution template, not the supreme authority. If any directive conflicts with the designated constitutional authority files, the authority files prevail.

## Required Files
A valid C-RSP environment must contain:
- All constitutional authority files listed in `authority_files` (exact filenames taken from that map)
- `BUILD_CONTRACT.md` (this template)
- `contract-schema.json`
- `CRSP_OUTCOME_TEMPLATE.md`
- `scripts/verify_crsp_template_bundle.sh`

If an inventory file is used, its name must appear in `authority_files.inventory` and the file must be present. The environment must include that file when it is declared.

## Five Non-Negotiable Directives
1. Constitutional Integrity: all authority files declared in `authority_files` must exist and not be placeholders.
2. Paired Artifact: every instance must produce `<basename>.json` and `<basename>.md`.
3. Machine-Halt Conditions: enforceable stops must be encoded as schema rules, predicates, verifier modules, or Guardian-kernel lifecycle rules.
4. Blind-Man Self-Sufficiency: setup and validation must be terminal-executable without hidden project knowledge.
5. Evidence Generation: validation, halt, transition, rollback, and execution outcomes must write evidence.

## Two-Layer Structure

### Machine Law Layer
The JSON instance is authoritative. It contains schema requirements, predicate DSL entries, verifier module references, halt matrix, lifecycle state, operation order, evidence paths, and rollback rules.

### Human Explanation Layer
The Markdown instance explains the JSON contract.

Mandatory disclaimer:
> Any obligation, restriction, halt condition, verifier, acceptance rule, or lifecycle rule stated in this Markdown but absent from the paired JSON is non-authoritative and shall not be enforced.

## Minimal JSON Instance Shape
```json
{
  "contract_id": "CRSP-XXX",
  "schema_version": "4.0",
  "status": "Draft",
  "basename": "CRSP-XXX",
  "authority_files": {
    "constitution": "CONSTITUTION.md",
    "agent_constraints": "AGENT_CONSTRAINTS.md",
    "inventory": "PROJECT_INVENTORY.json"
  },
  "scope": {
    "repo_path": ".",
    "allowed_roots": [],
    "forbidden_paths": [
      "${authority_files.constitution}",
      "${authority_files.agent_constraints}",
      "${authority_files.inventory}"
    ],
    "network_access": false
  },
  "topology": {
    "mode": "Core | Satellite | Dual-Topology",
    "verifier_class": "UNRESOLVED_REQUIRED_INPUT"
  },
  "baseline": {
    "commit": "UNRESOLVED_REQUIRED_INPUT",
    "dirty_worktree_allowed": false
  },
  "artifacts": {
    "json_path": "CRSP-XXX.json",
    "markdown_path": "CRSP-XXX.md",
    "generated_paths": [],
    "evidence_dir": "verification/CRSP-XXX"
  },
  "operations": [],
  "predicates": [],
  "verifier_modules": [
    {
      "module_id": "markdown_drift_detector",
      "path": "verifiers/markdown_drift_check.sh",
      "sha256": "..."
    }
  ],
  "halt_matrix": [],
  "lifecycle": {
    "allowed_states": ["Draft", "Active", "Frozen", "Superseded", "Quarantined"],
    "transition_evidence_path": "verification/CRSP-XXX/lifecycle.jsonl",
    "transition_predicates": {
      "Draft_to_Active": [],
      "Active_to_Frozen": [],
      "Frozen_to_Superseded": [],
      "Quarantine_override": []
    }
  },
  "rollback": {
    "safe_state": "UNRESOLVED_REQUIRED_INPUT",
    "procedure": [],
    "evidence_path": "verification/CRSP-XXX/rollback.jsonl"
  },
  "unresolved_field_ledger": [],
  "mandatory_enforcement_fields": [
    "status",
    "scope.repo_path",
    "scope.allowed_roots",
    "topology.mode",
    "topology.verifier_class",
    "baseline.commit",
    "artifacts.json_path",
    "artifacts.markdown_path",
    "artifacts.evidence_dir",
    "operations",
    "halt_matrix",
    "rollback.safe_state",
    "rollback.procedure",
    "unresolved_field_ledger"
  ]
}
