First line: `# C-RSP Master Template v3.0 – Executable Governance Contract with Full Body Schema`

Last line: `- Absence of empty objects (except explicit `"UNRESOLVED"` strings).`

Everything from that first line to that last line (inclusive) goes into `BUILD_CONTRACT.md`. Below is the exact content in a single code block:

```markdown
# C-RSP Master Template v3.0 – Executable Governance Contract with Full Body Schema

**Role:** Principal AI Safety Engineer – AI Control, Scalable Oversight  
**Target:** Autonomous AI coding agents acting on The Living Constitution (TLC) repository  
**Purpose:** Generate a Constitutionally‑Regulated Single Pass (C‑RSP) instance containing a fully populated operational body (Identity, Lifecycle, Halt Matrix, Topology) in a machine‑enforceable JSON envelope.

---

## 📜 BOOTSTRAP COMMAND (Mandatory First Step)

```python
load_constitution("THE_LIVING_CONSTITUTION.md")
load_constitution("CLAUDE.md")
load_constitution("MASTER_PROJECT_INVENTORY")
load_contract("BUILD_CONTRACT.md")
load_schema("contract-schema.json")
```

> **Invariant 0 – Context Bootstrap:** You are **not allowed** to propose any code, architecture, or executable enforcement mechanism until you have successfully executed the BOOTSTRAP COMMAND and explicitly verified ingestion of the TLC Constitutional Trinity.

---

## 🧱 Semantic File References

| Semantic Name | Actual File | Role |
| :--- | :--- | :--- |
| `constitution_doc` | THE_LIVING_CONSTITUTION.md | Root Law |
| `claude_instructions` | CLAUDE.md | Agent Constraints |
| `project_inventory` | MASTER_PROJECT_INVENTORY | System Map |
| `build_contract` | BUILD_CONTRACT.md | This document (v3.0) |
| `contract_schema` | contract-schema.json | Expanded schema enforcing full body |
| `outcome_template` | CRSP_OUTCOME_TEMPLATE.md | Response Format |

---

## ⚙️ Three‑Stage Execution Pipeline (Strictly Enforced)

### Stage 1 – Read the Law
- Acknowledge **this v3.0 template** as the absolute Master Authority.
- **Read‑only constraint:** You may never modify constitutional files.

### Stage 2 – Draft the Paired Instance

You **must** generate two files with an identical basename (e.g., `CRSP-001`).

#### 2.1 – The Law (`<basename>.json`)
- Pure JSON. Zero Markdown. Validated against the expanded schema below.
- This JSON **must contain** the full operational body defined in `contract_body`.

#### 2.2 – The Commentary (`<basename>.md`)
- Human‑readable rationale.
- **Mandatory Disclaimer:** *Any rule mentioned in this Markdown file but absent from the companion JSON file is legally void and shall not be enforced by the Guardian kernel.*

### Stage 3 – Standard Outcome Response
Your entire response must be the `CRSP_OUTCOME_TEMPLATE.md` structure. No conversation.

---

## 📦 Required JSON Body Schema

The `contract-schema.json` file **must** validate the following top‑level structure. Populate all fields; unresolved fields must be marked `"UNRESOLVED"` and logged.

```json
{
  "contract_id": "CRSP-XXX-XXX",
  "version": "v1.0.0-draft",
  "schema_version": "3.0",
  "status": "Draft",
  "adoption_tier": "Tier-2-Operational",
  "contract_body": {
    "contract_identity": {
      "title": "...",
      "system_role": "...",
      "primary_objective": "...",
      "scope_boundary": "...",
      "not_claimed": "..."
    },
    "topology_profile": {
      "mode": "Dual-Topology | Single",
      "profile_overlay_source": "...",
      "verifier_class": "...",
      "instance_artifact_path": "...",
      "governance_lock_path": "..."
    },
    "baseline_state": {
      "existing_repo": "...",
      "baseline_commit": "...",
      "verified_assets": [],
      "known_constraints": [],
      "known_gaps": []
    },
    "dependencies": {
      "required_inputs": [],
      "external_dependencies": [],
      "governance_dependencies": [],
      "forbidden_assumptions": []
    },
    "risk_classification": {
      "risk_class": "High | Medium | Low",
      "side_effect_class": "Internal | External",
      "stop_override_required": true,
      "recovery_mode": "Manual | Automatic"
    },
    "execution_model": {
      "execution_mode": "Single-pass deterministic build contract",
      "decision_closure_rule": "...",
      "fallback_rule": "...",
      "generated_artifacts": [],
      "ordered_operations": [
        {
          "step_id": "OP-01",
          "actor": "human/agent",
          "action": "...",
          "inputs": [],
          "outputs": [],
          "verify": "...",
          "if_failure": "..."
        }
      ],
      "halt_conditions": [
        {
          "condition": "...",
          "stop_reason": "...",
          "next_action": "..."
        }
      ]
    },
    "lifecycle_state_machine": {
      "allowed_states": ["Draft", "Active", "Frozen", "Superseded"],
      "transition_rules": "BUILD → STABILIZE → OPERATE",
      "transition_evidence_path": "evidence/.../"
    },
    "invariants": {
      "global": ["INVARIANT_TERM_01", "INVARIANT_LIFE_FDE_01"],
      "profile": []
    },
    "acceptance_criteria": [
      {
        "id": "AC-01",
        "requirement": "...",
        "verification_method": "...",
        "pass_condition": "..."
      }
    ],
    "rollback_recovery": {
      "safe_state_definition": "...",
      "rollback_procedure": "...",
      "recovery_authority": "...",
      "rollback_evidence_path": "..."
    },
    "evidence_truth_surface": {
      "primary_evidence_paths": [],
      "generated_reports": [],
      "audit_artifacts": []
    },
    "halt_matrix": {
      "global_halt_triggers": [],
      "cross_repo_drift": "..."
    },
    "preflight": {
      "commands": [],
      "validation_scripts": []
    }
  }
}
```

---

## 🔒 Seven Non‑Negotiable Directives

| # | Directive | Enforcement Action |
| :--- | :--- | :--- |
| 1 | **Constitutional Integrity** | Pre‑flight check before Stage 2. |
| 2 | **Execution over Theory** | JSON must reference executable modules. |
| 3 | **Read‑Only Constraints** | Explicit statement in commentary Markdown. |
| 4 | **Evidence Generation** | Create `verification/` logs and rationales. |
| 5 | **Paired Artifact Execution** | Mandatory JSON + Markdown output. |
| 6 | **Blind Man’s Protocol** | Provide Day Zero instructions (below). |
| 7 | **Lifecycle Pipeline** | Ignore helper files (`PASS8_TEMPLATE.md`, etc.). |
| 8 | **Full Body Population** | JSON must contain all `contract_body` sections. |

---

## 👁️ Blind Man’s Protocol – Day Zero Initialization

1. Create a new directory (e.g., `mkdir crsp-instance`).
2. Download required files into that directory:
   - `THE_LIVING_CONSTITUTION.md`
   - `CLAUDE.md`
   - `MASTER_PROJECT_INVENTORY`
   - `BUILD_CONTRACT.md` (this file)
   - `contract-schema.json` (expanded version)
   - `CRSP_OUTCOME_TEMPLATE.md`
   - `scripts/verify_crsp_template_bundle.sh`
3. Open your AI agent and paste the **BOOTSTRAP COMMAND**.
4. Paste this entire **v3.0 Template** as the system prompt.
5. Instruct: *“Generate a C-RSP instance following the v3.0 template. Use basename CRSP-001.”*
6. After AI response, run the preflight script.

---

## ✅ AI Self‑Check Before Final Outcome

- [ ] BOOTSTRAP COMMAND executed.
- [ ] JSON file exists and validates against expanded schema.
- [ ] All `contract_body` sections present (even if `"UNRESOLVED"`).
- [ ] Markdown file contains legal disclaimer.
- [ ] Verification files created with unresolved token log.
- [ ] No helper files used.

---

## 🧪 Structural Preflight Integration

The script `./scripts/verify_crsp_template_bundle.sh` checks:
- JSON validity against expanded schema.
- Presence of all mandatory `contract_body` keys.
- Absence of empty objects (except explicit `"UNRESOLVED"` strings).
```
