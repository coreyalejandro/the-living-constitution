# C-RSP Build Contract: Guardian Kernel — MCP Safety Enforcement Server

## Constitutionally-Regulated Single Pass Executable Prompt — Executed Instance

**Contract ID:** CRSP-001  
**Version:** 1.0.0  
**Status:** ACTIVE  
**Adoption Tier:** Tier-3-Constitutional  
**Basename:** CRSP-001  
**Series:** Series A  
**Generated:** 2026-04-08T03:57:44Z  
**Operator:** coreyalejandro  
**Git commit:** b1c46dfc4e1a46f2dfd017e971b26a479cdd5a5c (main)

---

> **LEGAL DISCLAIMER — READ BEFORE PROCEEDING**
>
> This Markdown file is the **Commentary** companion to `CRSP-001.json` (The Law).
> Any rule, constraint, or requirement mentioned in this Markdown file but
> **absent from the companion JSON file `CRSP-001.json` is legally void** and
> shall not be enforced by the Guardian kernel. The JSON file is the sole
> authoritative source for all machine-executable constraints. This file
> exists for human understanding only.

---

## Section 0 — Instance Governance

This file is an **executed instance** of the C-RSP Master Template
(`projects/c-rsp/BUILD_CONTRACT.md`). It is not a reusable template.

Authority order (strict — lower rows do not override higher rows):

| Band | Artifact |
| ------ | ---------- |
| 1 | `projects/c-rsp/BUILD_CONTRACT.md` — Canonical master template |
| 2 | `projects/c-rsp/BUILD_CONTRACT.instance.md` — Guided instance template |
| 3 | `projects/c-rsp/contract-schema.json` — Structural law |
| 4 | `projects/c-rsp/CRSP_OUTCOME_TEMPLATE.md` — Outcome artifact |
| 6 | `CRSP-001.json` + `CRSP-001.md` — This executed instance |

**Helper files ignored (as required by Directive 7):** `PASS8_TEMPLATE.md`,
`INSTANCE_PROCESS.md`, `workflows/` subdirectory.

**Read-only constraint (Directive 3):** This instance cannot modify
`THE_LIVING_CONSTITUTION.md`, `CLAUDE.md`, or `MASTER_PROJECT_INVENTORY.md`.
All modifications to those files require a human cryptographic signature in
the commit chain. Audits performed by this contract are strictly read-only.

---

## Section 1 — Contract Identity

| Field | Value |
| ------- | ------- |
| Contract Title | Guardian Kernel — MCP Safety Enforcement Server |
| Contract ID | CRSP-001 |
| Version | 1.0.0 |
| Schema Version | 1.0.0 |
| Status | Draft |
| Adoption Tier | Tier-3-Constitutional |
| Series | Series A |
| Parent ADR | `.agents/rules/guardian-kernel.md` |
| Owner | coreyalejandro |

**Strategic Intent:** Build `src/guardian.py` as an MCP server that acts as an
inescapable constitutional cage — physically intercepting every agent tool
call and enforcing safety invariants before any code is written. This is the
first executable enforcement mechanism in the TLC Constitutional Stack.

---

## Section 2 — Contract Topology + Profile

| Field | Value |
| ------- | ------- |
| Topology Mode | TLC-Core |
| Profile Type | Core |
| Verifier Class | core-verifier |
| Implementation Target | `src/guardian.py` |
| Domain Alignment | All 4 Safety Domains (Epistemic, Human, Cognitive, Empirical) |

### Dual Co-Pilot Mental Model

The Guardian Kernel enforces the Dual Co-Pilot separation defined in the ADR:

**Constitutional Lawyer** — Reads the law, verifies invariants, drafted this
JSON build contract (`CRSP-001.json`). This role is read-only during planning.

**Implementation Developer** — Executes the JSON contract, writes the Markdown
commentary (this file), runs the preflight bash scripts.

In an Antigravity multi-agent setup, these roles must be assigned to separate
agents to strictly enforce read-only constraints during the planning phase.

---

## Section 3 — Baseline State (Honest)

At the time this contract was generated:

| Item | Status |
| ------ | -------- |
| `src/guardian.py` | Does not exist |
| Guardian ADR (`.agents/rules/guardian-kernel.md`) | Exists — ingested |
| MCP server running | No |
| Tool call interception active | No |
| Invariant enforcement active | No |
| `verification/` directory | Exists |
| Trinity ingested | Yes — all three files loaded and verified |

**Trinity ingestion confirmed:**

- `THE_LIVING_CONSTITUTION.md` — Articles I-V, 6-layer enforcement stack,
  Agent Republic powers, Amendment Process, SOP library
- `CLAUDE.md` — Repo structure, operational controls, project registry,
  C-RSP authority order, 8 projects with disk probes
- `MASTER_PROJECT_INVENTORY.md` — 20 project slugs, governance chain,
  anomalies (5 missing implementation paths), artifact manifest

**Anomalies from inventory (recorded, not claimed resolved):**

- `MADMall-Production` directory missing on disk
- `buildlattice` implementation path missing on disk
- `empirical-guard`, `epistemic-guard`, `human-guard` implementation paths
  missing on disk
- `projects/c-rsp` lacks `CLAUDE.md` per base-camp convention

---

## Section 4 — Dependencies and Inputs

### Required Files (All Loaded)

| Semantic Name | Path | Role |
| --------------- | ------ | ------ |
| `constitution_doc` | `THE_LIVING_CONSTITUTION.md` | Governing law — Articles I-V |
| `claude_instructions` | `CLAUDE.md` | Operational controls |
| `project_inventory` | `MASTER_PROJECT_INVENTORY.md` | Commonwealth manifest |
| `build_contract` | `projects/c-rsp/BUILD_CONTRACT.md` | Master template |
| `contract_schema` | `projects/c-rsp/contract-schema.json` | Structural validation |
| `guardian_adr` | `.agents/rules/guardian-kernel.md` | Architecture decisions |

### Runtime Dependencies

- `python3 >= 3.11` — Guardian execution environment
- `mcp >= 1.0.0` — MCP server SDK for `src/guardian.py`

---

## Section 5 — Risk + Control Classification

| Field | Value |
| ------- | ------- |
| Risk Class | Critical |
| Side Effect Class | Internal |
| Stop Override Required | Yes |
| Recovery Mode | Manual |

**Why Critical:** The Guardian Kernel is the only enforcement gate between
agent intent and code execution. If it fails, uninspected tool calls execute
freely, violating Articles I-IV of the Living Constitution.

**Why Stop Override = Yes:** A Guardian STOP signal cannot be self-overridden
by any agent. Human operator review is required before resumption.

### Controls

| ID | Name | Description |
| ---- | ------ | ------------- |
| CTRL-001 | Trinity Preflight Gate | Guardian enters SAFE_HALT if Trinity bootstrap fails |
| CTRL-002 | Read-Only Constitution Lock | Write attempts without cryptographic signature trigger HALT |
| CTRL-003 | Invariant Evaluation Engine | Every tool call evaluated before forwarding; FAIL = structured log + halt |
| CTRL-004 | Evidence Generation Mandatory | Every decision written to `verification/` before action |
| CTRL-005 | No Recursive Self-Modification | Runtime rule changes forbidden; require new C-RSP instance |

---

## Section 6 — Execution Model

**Target:** `src/guardian.py` (Python MCP Server)

### Ordered Operations

| Step | ID | Name | Halt Condition | Success Condition |
| ------ | ---- | ------ | ---------------- | ------------------- |
| 1 | OP-BOOTSTRAP | Trinity Bootstrap | Any Trinity file missing | All 3 loaded; hashes logged |
| 2 | OP-INVARIANT-LOAD | Invariant Registry Load | Registry empty or unreadable | ≥7 invariants registered |
| 3 | OP-MCP-INIT | MCP Server Initialization | Server fails to bind | All 6 agent interceptors registered |
| 4 | OP-INTERCEPT-LOOP | Tool Call Interception Loop | Invariant engine throws exception | Deterministic PASS/FAIL per call |
| 5 | OP-PASS-FORWARD | PASS — Forward Call | N/A | Call forwarded unmodified; PASS logged |
| 6 | OP-FAIL-HALT | FAIL — Emit STOP + Log | Log write fails | STOP emitted; structured record persisted |
| 7 | OP-EVIDENCE-FLUSH | Evidence Flush | Flush fails after 3 retries | All entries persisted; session summary written |

### Key Functions (src/guardian.py)

- `bootstrap_trinity()` — Load and hash-verify all three Trinity files
- `load_invariants()` — Register all constitutional invariants from this contract
- `evaluate_invariants(agent_id, tool_name, params)` — Sequential evaluation engine
- `emit_stop(agent_id, invariant_id, reason)` — Structured STOP signal emitter
- `log_decision(decision_record)` — Write to `verification/crsp_CRSP-001_log.json`

---

## Section 7 — Lifecycle State Machine

### Contract Lifecycle

```text
Draft → Active → Frozen → Superseded
```

- **Draft → Active:** `src/guardian.py` exists and passes preflight; log initialized
- **Active → Frozen:** All acceptance criteria passed; human review with cryptographic signature
- **Frozen → Superseded:** Replacement C-RSP (CRSP-002+) is Active; human signature

### Guardian Runtime State Machine

```text
INIT → TRINITY_LOADING → INVARIANT_LOADING → MCP_STARTING → ACTIVE
                                                              ↓
                                                     (on any halt condition)
                                                     SAFE_HALT | FAIL_HALT
```

Terminal states (`SAFE_HALT`, `FAIL_HALT`) require manual operator intervention.

---

## Section 8 — Invariants

### Constitutional Invariants (sourced from THE_LIVING_CONSTITUTION.md and BUILD_CONTRACT.md)

**INVARIANT_TRINITY_01 — Trinity Bootstrap Required (CRITICAL)**
No code proposal or enforcement mechanism activates until all three Trinity
files are loaded and verified. Guardian enters SAFE_HALT if this fails.

**INVARIANT_ARTICLE_I_01 — ND Access Filter Mandatory (CRITICAL)**
Every agent output passes through the Neurodivergent Access Layer before
reaching the user. Outputs bypassing this filter are unconstitutional.

**INVARIANT_ARTICLE_I_02 — User Rights: Safety, Accessibility, Dignity, Clarity (HIGH)**
Any interaction violating these four rights is blocked with a STOP signal.

**INVARIANT_ARTICLE_II_01 — All Tool Calls Pre-Validated (CRITICAL)**
No tool call from any agent executes without Guardian evaluation. No bypass.

**INVARIANT_ARTICLE_II_02 — Code Quality Gates (HIGH)**
Builder tool calls must pass: immutability checks (no direct constitution
writes), test coverage (cannot ship <80% coverage), and security checks.

**INVARIANT_ARTICLE_III_01 — ToC&A Anchor Required (HIGH)**
Every agent action must map to at least one Theory of Change node. Actions
with no ToC&A anchor are blocked; DataSci agent notified.

**INVARIANT_ARTICLE_IV_01 — Agent Power Boundaries Enforced (CRITICAL)**
Each agent operates within constitutional bounds. Out-of-bounds actions
are blocked; human review required.

- Planner: Cannot change architectural decisions without human review
- Builder: Cannot deploy to production; cannot modify DB schema or auth systems
- Sentinel: Cannot override other agents; cannot modify its own rules
- TDD: Cannot skip RED phase; cannot ship with <80% coverage
- Reviewer: Cannot approve its own work; can only flag CRITICAL, suggest MEDIUM, approve LOW
- DataSci: Cannot redefine ToC&A nodes or change success metrics without review

**INVARIANT_ARTICLE_V_01 — Amendment Requires Eval Harness (CRITICAL)**
No agent may modify the constitution without completing:
Observation → Proposal → Eval Harness Review → Ratification (SOP-010).

**INVARIANT_READ_ONLY_01 — Constitution Files Read-Only (CRITICAL)**
`THE_LIVING_CONSTITUTION.md`, `CLAUDE.md`, and `MASTER_PROJECT_INVENTORY.md`
are read-only to all agents. Writes require human cryptographic signature.

**INVARIANT_EVIDENCE_01 — Evidence Generation Mandatory (HIGH)**
Every Guardian decision (PASS or FAIL) is logged. Silent decisions are
forbidden. Log write failure → FAIL_HALT.

**INVARIANT_PAIRED_ARTIFACT_01 — Paired Artifact Execution (HIGH)**
Every C-RSP instance produces exactly two files sharing an identical basename:
a JSON law file and a Markdown commentary file. Rules in Markdown absent from
JSON are legally void.

### Guardian-Specific Invariants

**INVARIANT_GUARDIAN_SELF_01 — No Runtime Self-Modification (CRITICAL)**
`src/guardian.py` enforcement rules cannot change at runtime. All updates
require a new C-RSP instance.

**INVARIANT_GUARDIAN_LOG_01 — Log-Before-Act (HIGH)**
Guardian writes the decision record to `verification/` before forwarding or
blocking any tool call. No action without prior evidence generation.

---

## Section 9 — Acceptance Criteria

| ID | Name | Verification Command |
| ---- | ------ | --------------------- |
| AC-001 | Guardian module exists | `python3 -c "import ast; ast.parse(open('src/guardian.py').read()); print('PASS')"` |
| AC-002 | MCP server starts | `python3 src/guardian.py --health-check` |
| AC-003 | Trinity bootstrap verified | Check `verification/crsp_CRSP-001_log.json` for `trinity_bootstrap: PASS` |
| AC-004 | Invariant enforcement active | `python3 scripts/test_guardian_invariants.py --invariant INVARIANT_ARTICLE_IV_01` |
| AC-005 | Constitution files read-only | `python3 scripts/test_guardian_readonly.py` |
| AC-006 | Structured evidence logs | `python3 scripts/verify_governance_chain.py --root .` |
| AC-007 | Paired artifacts valid | `./scripts/verify_crsp_template_bundle.sh` |
| AC-008 | No helper file pollution | `grep -r 'PASS8_TEMPLATE\|INSTANCE_PROCESS\|workflows/' CRSP-001.json && echo FAIL \|\| echo PASS` |

---

## Section 10 — Rollback and Recovery

**Recovery Mode:** Manual (per SOP-013 Session Recovery Protocol)

### Rollback Steps

1. All agent operations pause immediately (SOP-013 triggered)
2. Read last log entry in `verification/crsp_CRSP-001_log.json` — identify halt cause
3. If Trinity file missing: `git checkout HEAD -- THE_LIVING_CONSTITUTION.md`
4. If invariant engine bug: inspect and fix `src/guardian.py`; re-run preflight
5. If unauthorized constitution modification: `git revert <commit>`; require human signature
6. After resolution: restart Guardian; verify health check passes
7. Document incident in `verification/crsp_CRSP-001_log.json` and `tasks/lessons.md`

**Key rollback commands:**

```bash
git stash
git checkout HEAD -- src/guardian.py
git checkout HEAD -- THE_LIVING_CONSTITUTION.md
./scripts/verify_crsp_template_bundle.sh
```

---

## Section 11 — Evidence and Truth Surface

**Authoritative truth surface:** `verification/crsp_CRSP-001_log.json`

| ID | Path | Role |
| ---- | ------ | ------ |
| EP-001 | `verification/crsp_CRSP-001_log.json` | Primary structured decision log (required) |
| EP-002 | `verification/crsp_CRSP-001_rationale.md` | Human-readable rationale (required) |
| EP-003 | `CRSP-001.json` | The Law — authoritative JSON (required) |
| EP-004 | `CRSP-001.md` | The Commentary — this file (required) |
| EP-005 | `verification/runs/` | CI verification run artifacts (optional) |

**Governance artifact chain:**

- Invariant registry: `governance/constitution/core/invariant-registry.json`
- Doctrine map: `governance/constitution/core/doctrine-to-invariant.map.json`
- Enforcement hooks map: `governance/enforcement/core/enforcement-map.json`
- Agent capabilities: `governance/agents/core/agent-capabilities.json`

---

## Section 12 — Conflict Matrix

| ID | Scenario | Resolution |
| ---- | ---------- | ------------ |
| CONFLICT-001 | False positive STOP (legitimate call blocked) | Human reviews log; fix via new C-RSP instance |
| CONFLICT-002 | Guardian crashes on init | All agents HALT; SOP-013; human fixes src/guardian.py |
| CONFLICT-003 | Two invariants give opposing verdicts | Most restrictive wins; block pending human review |
| CONFLICT-004 | Valid constitution amendment needed | Full SOP-010 amendment pipeline; human signature required |
| CONFLICT-005 | Markdown rule absent from JSON | JSON governs; Markdown rule is legally void; fix in next revision |

---

## Section 13 — Halt Matrix

| ID | Trigger | Halt State | Override Required |
| ---- | --------- | ------------ | ------------------- |
| HALT-001 | Trinity file missing on startup | SAFE_HALT | Yes |
| HALT-002 | Unauthorized write to constitution file | FAIL_HALT | Yes |
| HALT-003 | Invariant engine unhandled exception | FAIL_HALT | Yes |
| HALT-004 | Evidence log write fails | FAIL_HALT | Yes |
| HALT-005 | Guardian self-modification attempt | FAIL_HALT | Yes |
| HALT-006 | MCP server fails to bind | SAFE_HALT | No |
| HALT-007 | src/guardian.py syntax error on startup | SAFE_HALT | No |

---

## Section 14 — Preflight

**Script:** `./scripts/verify_crsp_template_bundle.sh`

| ID | Check | Required |
| ---- | ------- | ---------- |
| PF-001 | `CRSP-001.json` exists at TLC root | Yes |
| PF-002 | `CRSP-001.md` exists at TLC root | Yes |
| PF-003 | `CRSP-001.json` is valid JSON with zero Markdown | Yes |
| PF-004 | `CRSP-001.md` contains legal disclaimer | Yes |
| PF-005 | `verification/` directory exists | Yes |
| PF-006 | No helper file references in `CRSP-001.json` | Yes |
| PF-007 | Trinity files exist at TLC root | Yes |
| PF-008 | All 18 required schema sections present in JSON | Yes |

---

## Section 15 — Adoption Tiers

Applied tier: **Tier-3-Constitutional** (all minimums satisfied)

| Tier | Minimum Sections | Satisfied |
| ------ | ----------------- | ----------- |
| Tier-1-MVG | contract_identity, topology_profile, preflight, output_format, instance_declaration | Yes |
| Tier-2-Operational | acceptance_criteria, risk_classification, rollback_recovery, lifecycle_state_machine, evidence_truth_surface | Yes |
| Tier-3-Constitutional | invariants, dependencies_inputs, halt_matrix, conflict_matrix, instance_declaration | Yes |

All 18 schema sections present.

---

## Section 16 — Output Format

All four output artifacts required before this contract advances to Active:

| ID | Filename | Type |
| ---- | ---------- | ------ |
| OUT-001 | `CRSP-001.json` | The Law — authoritative JSON, zero Markdown |
| OUT-002 | `CRSP-001.md` | The Commentary — this file |
| OUT-003 | `verification/crsp_CRSP-001_log.json` | Structured decision log |
| OUT-004 | `verification/crsp_CRSP-001_rationale.md` | Human-readable rationale |

Response format follows `CRSP_OUTCOME_TEMPLATE.md`. No conversational escape
hatch. Questions embedded in Next Steps only.

---

## Section 17 — Instance Declaration

This file is an **executed instance** of the C-RSP master template. It is
not a reusable template. It governs exactly one build scope:

> **Guardian Kernel — `src/guardian.py` — Series A**

| Field | Value |
| ------- | ------- |
| Basename | CRSP-001 |
| Parent template | `projects/c-rsp/BUILD_CONTRACT.md` |
| Instance role | executed-instance |
| Not a reusable template | True |
| Operator | coreyalejandro |
| Stage completed | Stage-2 — Draft the Instance |
| Trinity loaded | Yes |
| Schema validated | Yes |
| Helper files ignored | Yes |

### Seven Directives Applied

| # | Directive | Applied |
| --- | ----------- | --------- |
| 1 | Constitutional Integrity — Trinity verified before any code proposal | Yes |
| 2 | Execution over Theory — JSON references executable modules (`src/guardian.py`) | Yes |
| 3 | Read-Only Constraints — Explicit statement above; no constitution modification | Yes |
| 4 | Evidence Generation — verification/ log and rationale required | Yes |
| 5 | Paired Artifact Execution — CRSP-001.json (law) + CRSP-001.md (commentary) | Yes |
| 6 | Blind Man's Protocol — Day Zero instructions in master template followed | Yes |
| 7 | C-RSP Lifecycle Pipeline — 3-stage pipeline enforced; helpers ignored | Yes |

### Blind Man's Protocol — Day Zero Quick Reference

For a zero-knowledge user starting fresh:

1. Ensure `THE_LIVING_CONSTITUTION.md`, `CLAUDE.md`, `MASTER_PROJECT_INVENTORY.md`,
   `projects/c-rsp/BUILD_CONTRACT.md`, and `projects/c-rsp/contract-schema.json`
   exist in the TLC root.
2. Run the preflight: `./scripts/verify_crsp_template_bundle.sh`
3. If preflight passes, `CRSP-001.json` is ready for Guardian kernel ingestion.
4. Build `src/guardian.py` following the ordered operations in Section 6.
5. Run acceptance criteria checks in Section 9 in order.
6. Advance contract status from `Draft` to `Active` with human sign-off.

---

*End of CRSP-001 Commentary. No narrative follows.*
