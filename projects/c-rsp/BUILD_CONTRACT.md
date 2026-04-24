# C-RSP Master Template v4.0

C-RSP = Constitutionally-Regulated Single Pass.

## Purpose
A C-RSP contract is an executable governance contract for deterministic, single-pass AI-assisted build work. It binds an AI coding agent to constitutional constraints, machine-checkable halt conditions, evidence generation, lifecycle control, rollback semantics, and paired human-readable explanation.

## Authority
The constitutional authority set is:
1. THE_LIVING_CONSTITUTION.md
2. CLAUDE.md
3. MASTER_PROJECT_INVENTORY.json

This document is the canonical C-RSP v4.0 Master Template and must be stored as `BUILD_CONTRACT.md` in a TLC-governed repository. If this template conflicts with the constitutional authority set, the constitutional authority set controls.

## Required Files
A valid C-RSP environment must contain:
- THE_LIVING_CONSTITUTION.md
- CLAUDE.md
- MASTER_PROJECT_INVENTORY.json
- BUILD_CONTRACT.md
- contract-schema.json
- CRSP_OUTCOME_TEMPLATE.md
- scripts/verify_crsp_template_bundle.sh

## Five Non-Negotiable Directives
1. Constitutional Integrity: authority files must exist before execution.
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
    "constitution": "THE_LIVING_CONSTITUTION.md",
    "claude": "CLAUDE.md",
    "inventory": "MASTER_PROJECT_INVENTORY.json"
  },
  "scope": {
    "repo_path": ".",
    "allowed_roots": [],
    "forbidden_paths": [
      "THE_LIVING_CONSTITUTION.md",
      "CLAUDE.md",
      "MASTER_PROJECT_INVENTORY.json"
    ],
    "network_access": false
  },
  "topology": {
    "mode": "TLC-Core | Satellite | Dual-Topology",
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
      "module_id": "...",
      "path": "...",
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
```

## Predicate DSL
Predicates must be implementable using POSIX shell, git, Python 3 standard library, and jq. Network access is forbidden unless `scope.network_access` is `true`.

Allowed predicate families:
- `exists(path)`
- `not_exists(path)`
- `file_sha256(path) == value`
- `json_path(path, selector) == value`
- `json_path_exists(path, selector)`
- `json_schema_valid(instance_path, schema_path)`
- `git_head(repo_path) == commit`
- `git_clean(repo_path) == true`
- `path_within_scope(path, allowed_roots) == true`
- `paired_artifact_exists(json_path, md_path) == true`
- `markdown_has_disclaimer(md_path) == true`
- `no_unresolved_in_required_fields(json_path) == true`
- `verifier_available(module_id) == true`
- `verifier_pass(module_id, contract_path, repo_path) == true`
- `evidence_written(path) == true`
- `no_forbidden_network_access(log_path) == true`
- `executable(path) == true`
- `directory_writable(path) == true`
- `inventory_contains(path, key) == true`  
  *new – checks that MASTER_PROJECT_INVENTORY.json contains a required key, e.g. `contract_schema_sha256`*

## Required Halt Matrix
Execution must halt if any condition is true:
- required authority file missing
- authority file is placeholder-only
- schema validation fails
- paired JSON or Markdown artifact missing
- Markdown disclaimer missing
- Markdown introduces enforceable obligations absent from JSON
- required verifier module unavailable (module_id not declared or path/sha256 mismatch)
- baseline commit mismatch
- dirty working tree when not declared
- generated artifact outside allowed roots
- network access detected while forbidden
- unresolved mandatory enforcement field exists *and* is not present in `unresolved_field_ledger`
- `unresolved_field_ledger` is missing or not an array
- `contract-schema.json` hash does not match `MASTER_PROJECT_INVENTORY.json`’s `contract_schema_sha256` (halt if key missing)
- `scripts/verify_crsp_template_bundle.sh` hash does not match inventory’s `bootstrap_sha256` if that key exists
- evidence directory missing or not writable
- verification script missing or not executable
- rollback evidence path missing
- lifecycle state is Superseded or Quarantined
- Frozen contract attempts mutation outside supersession metadata
- transition predicates for the attempted lifecycle change are not satisfied (as defined in `lifecycle.transition_predicates`)

## Lifecycle Rules
- Draft may contain unresolved advisory fields if logged.
- Draft may not execute if any mandatory enforcement field is unresolved.
- Active must contain zero unresolved mandatory enforcement fields; all mandatory fields must be resolved.
- Frozen may not mutate except through supersession metadata.
- Superseded may not execute.
- Quarantined may not execute until revalidated through evidence-backed Guardian-kernel action.
- Every lifecycle state transition must satisfy the predicate list in `lifecycle.transition_predicates` for that transition, and evidence must be written to `lifecycle.transition_evidence_path`.

## Guardian Kernel Minimum Interface
A v4.0 Guardian kernel must expose:
- `validateContract(contractPath)`
- `ingestContract(contractPath)`
- `evaluatePredicates(contractId)`
- `executeOperation(contractId, stepId)`
- `checkHaltConditions(contractId)`
- `writeEvidence(contractId, event)`
- `transitionLifecycle(contractId, targetState)`
- `quarantineContract(contractId, reason)`

Kernel storage must include:
- contract registry
- evidence ledger
- lifecycle state log
- predicate result log
- verifier module registry
- quarantine registry

The kernel must not infer obligations from Markdown, silently repair invalid contracts, mutate constitutional authority files, or perform network access unless declared and permitted.

## Blind-Man Bootstrap Script — Minimal Local C-RSP Environment
Copy into a file named `bootstrap-crsp.sh`, then run: `sh bootstrap-crsp.sh`

```sh
#!/bin/sh
set -eu

ROOT="${1:-crsp-instance}"
mkdir -p "$ROOT/scripts" "$ROOT/verification"

for f in THE_LIVING_CONSTITUTION.md CLAUDE.md MASTER_PROJECT_INVENTORY.json; do
  if [ ! -f "$ROOT/$f" ]; then
    printf '%s\n' "REPLACE ME: placeholder only. Not valid TLC authority." > "$ROOT/$f"
  fi
done

# Minimal structural schema – not the full enforcement schema.
# A real TLC-governed environment must supply the canonical contract-schema.json
cat > "$ROOT/contract-schema.json" <<'JSON'
{
  "type": "object",
  "required": [
    "contract_id",
    "schema_version",
    "status",
    "basename",
    "authority_files",
    "scope",
    "baseline",
    "artifacts",
    "operations",
    "predicates",
    "halt_matrix",
    "lifecycle",
    "rollback",
    "unresolved_field_ledger",
    "mandatory_enforcement_fields"
  ],
  "properties": {
    "schema_version": { "const": "4.0" },
    "status": { "enum": ["Draft", "Active", "Frozen", "Superseded", "Quarantined"] }
  }
}
JSON

cat > "$ROOT/CRSP_OUTCOME_TEMPLATE.md" <<'MD'
# C-RSP Outcome
## Produced Artifacts
## Verification Results
## Halt Status
## Evidence Paths
## V&T Statement
MD

cat > "$ROOT/BUILD_CONTRACT.md" <<'MD'
# C-RSP Master Template v4.0 Candidate
This is the canonical BUILD_CONTRACT.md for TLC. Replace with the latest version if obtained from the repository.
MD

cat > "$ROOT/scripts/verify_crsp_template_bundle.sh" <<'SH'
#!/bin/sh
set -eu

missing=0

for f in THE_LIVING_CONSTITUTION.md CLAUDE.md MASTER_PROJECT_INVENTORY.json BUILD_CONTRACT.md contract-schema.json CRSP_OUTCOME_TEMPLATE.md; do
  [ -f "$f" ] || { echo "MISSING: $f"; missing=1; }
done

[ -x scripts/verify_crsp_template_bundle.sh ] || {
  echo "NOT_EXECUTABLE: scripts/verify_crsp_template_bundle.sh"
  missing=1
}

python3 -m json.tool contract-schema.json >/dev/null || {
  echo "INVALID_JSON: contract-schema.json"
  missing=1
}

command -v jq >/dev/null 2>&1 || {
  echo "MISSING_DEPENDENCY: jq"
  missing=1
}

if grep -q "REPLACE ME: placeholder only" THE_LIVING_CONSTITUTION.md CLAUDE.md MASTER_PROJECT_INVENTORY.json; then
  echo "PLACEHOLDER_AUTHORITY_FILES_PRESENT"
  echo "Status: local bootstrap only; not valid TLC-governed execution."
fi

[ "$missing" -eq 0 ] && echo "BOOTSTRAP_OK_PLACEHOLDER_ONLY" || exit 1
SH

chmod +x "$ROOT/scripts/verify_crsp_template_bundle.sh"
( cd "$ROOT" && ./scripts/verify_crsp_template_bundle.sh )

echo "Created minimal local C-RSP environment at $ROOT."
echo "Status: placeholder-only; not a valid TLC-governed instance until real authority files are supplied."
```

## Verification Algorithm
1. Validate JSON against contract-schema.json.
2. Confirm paired Markdown exists and contains the mandatory disclaimer.
3. Confirm authority files exist and use exact required filenames.
4. Halt if authority files are placeholders.
5. Verify `contract-schema.json` integrity: if `MASTER_PROJECT_INVENTORY.json` contains `contract_schema_sha256`, compute sha256 of `contract-schema.json` and compare; halt on mismatch or missing key.
6. Reject execution if lifecycle state forbids execution.
7. Reject execution if unresolved mandatory enforcement fields exist and are not recorded in `unresolved_field_ledger`.
8. Evaluate all declared predicates.
9. Run all declared verifier modules (each must have a valid entry in `verifier_modules` with `module_id`, `path`, `sha256`; kernel verifies integrity before calling).
10. Check halt matrix.
11. Execute operations in declared order only if no halt condition is active.
12. Write evidence for every pass, failure, halt, rollback, and lifecycle transition.

## Acceptance Criteria
- Candidate uses exact required filenames.
- Candidate has exactly five directives.
- Candidate separates Machine Law Layer from Human Explanation Layer.
- Candidate defines Draft, Active, Frozen, Superseded, and Quarantined states with lifecycle transition predicates.
- Candidate does not treat Markdown-only obligations as enforceable.
- Candidate does not claim placeholder authority files create a valid TLC-governed instance.
- Candidate does not claim live repository validation.

## Migration Note – v3.0 to v4.0
v4.0 hardens v3.0 by:
- Reducing eight directives to exactly five, each directly enforceable.
- Introducing a strict two-layer architecture: authoritative JSON and advisory Markdown (v3.0 blurred this line).
- Adding a formal Predicate DSL and minimal verifier module interface, making halt conditions completely machine‑checkable.
- Adding Quarantined as a lifecycle state.
- Replacing the pseudo-code “Bootstrap Command” with an executable shell script.
- Embedding a required `contract-schema.json` hash check enforced by `MASTER_PROJECT_INVENTORY.json`.
- Requiring that all unresolved mandatory fields be logged explicitly in `unresolved_field_ledger`.
- Introducing lifecycle transition predicates, making state changes auditable.
- Removing ambiguous language like “absolute Master Authority”; the template now explicitly defers to the constitutional authority set.
---
