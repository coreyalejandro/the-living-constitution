# TLC Enterprise Restructuring: Master Plan

## Session Status (as of 2026-04-05)

- **Plan status:** COMPLETE — reviewed, awaiting user's external agent review feedback
- **Execution status:** NOT STARTED — no files modified, no contracts instantiated
- **Branch:** `claude/restructure-tlc-enterprise-LxIXt` (develop and push here)
- **User requested:** Copy this plan into the repo and push so they can access it locally
- **Blocked by:** Plan mode was active; user needs to exit plan mode or start a new session to execute
- **Pending feedback:** User said "I'm getting another agent to review it" — review feedback not yet received
- **Next action:** (1) Exit plan mode, (2) copy this file to `plans/master-plan.md` in repo, (3) commit and push to branch, (4) await review feedback before executing Contract A-1

### Key Decisions Made
- **C-RSP** = Constitutionally-Regulated Single Pass (canonical expansion, no variants)
- **"Canonical tool"** replaces "signature tool"
- **Front door** = README → STATUS.json (NOT the Golden Sandbox)
- **Golden Sandbox** = execution substrate / guarded ingress
- **Blind Man's Test** enforced structurally at every tier (not just aspirational)
- **3 Adoption Tiers** surface as user-facing workflow choice (Quick/Standard/Full)
- **5 Work Types** (Build/Fix/Refactor/Governance/Discovery) with type-specific starter prompts
- **CONTROL_RULE_KBC_01**: Single active BUILD_CONTRACT at a time until clear

### Unresolved Items
- ChatGPT had a preferred framing the user mentioned but never shared
- ClarityAI discovery (needs GitHub access to coreyalejandro/clarity-ai) — deferred to Contract A-4
- SentinelOS disposition — deferred to Contract A-3

---

## Context

TLC (The Living Constitution) is being restructured from a governance meta-repository into a **first-class enterprise governance operating system and development overlay** for frontier coding agents (Claude Code, Codex, Gemini). The restructuring formalizes:

1. A **constitutional mental model** with 4 Safety Domains as jurisdictions, governing bodies as institutions, and projects as governed entities
2. A **product definition** stronger than "wrapper": "The Living Constitution is a governance operating system and development overlay for frontier coding agents and AI product teams. It wraps Claude Code, Codex, and Gemini with constitutional constraints, evidence capture, invariant enforcement, and dual-topology product governance."
3. A **C-RSP Program** (series of build contracts) as the primary mechanism for executing all work
4. **IDE-agnostic execution** — Claude Code primary, Cursor fallback, C-RSP contracts portable across all agents

The immediate trigger: the current constitutional documents (THE_LIVING_CONSTITUTION.md, root CLAUDE.md, MASTER_PROJECT_INVENTORY.*) do not reflect the taxonomy, and until those three surfaces agree, every subsequent contract will drift.

---

## Taxonomy: The Five Layers

| Layer | Analogy | TLC Implementation |
|---|---|---|
| **Article Layer** | Constitutional law | THE_LIVING_CONSTITUTION.md, Articles I-V, 59 invariants |
| **Domain Layer** | Jurisdictions | 4 Safety Domains (Epistemic, Human, Cognitive, Empirical) |
| **Institution Layer** | Governing bodies | One or more per domain; must obey dual-topology rule |
| **Project Layer** | Governed entities | Consumer/dev products governed by institutions |
| **Verification Layer** | Case law / evidence | STATUS.json, MATRIX.md, evidence ledger, attestations |

### Domain-to-Institution-to-Project Mapping (First Pass)

| Domain | Primary Institution (Canonical Tool) | Secondary Institutions | Governed Projects |
|---|---|---|---|
| **Epistemic Safety** | PROACTIVE (constitutional violation detector) | EpistemicGuard (ClaimAuditor) | TLC Evidence Observatory |
| **Human Safety** | UICare-System (session safeguard) | HumanGuard (SessionSafeguard) | — |
| **Cognitive Safety** | Docen (document processor) | Instructional Integrity Studio | — |
| **Empirical Safety** | ConsentChain (7-stage consent gateway) | EmpiricalGuard (BehaviorObserver) | Frostbyte ETL |
| **Cross-Domain Infrastructure** | C-RSP (tiered build contracts) | SentinelOS (invariant platform), BackboardAI-FDE (FDE lifecycle governor), Golden Sandbox (execution substrate) | TLC Control Plane, Portfolio, im-just-a-build, teaser-video-remotion |

### Unresolved / Discovery Required

- **ClarityAI** — Exists on user's GitHub (coreyalejandro). Needs discovery to determine domain assignment and role. C-RSP Series B should include a discovery step.
- **ITAYN, HUNS** — Candidate repos being considered for TLC. Not yet committed. Note as future candidates; do not block on them.
- **SentinelOS disposition** — Spawned TLC but may be redundant now. Series A should evaluate: absorb into TLC core, deprecate, or redefine as a specific institution.

---

## Front Door Correction

The TLC front door is **NOT** the Golden Sandbox. It is the **governance overlay/base camp** anchored by:
- `README.md` → `STATUS.json` / `STATUS.md`

The Golden Sandbox (`sandbox-runtime-001`) is the **execution substrate / guarded ingress** for governed apps like the Constitutional UI.

---

## C-RSP Program: Five Series

All work is executed via C-RSP Build Contracts instantiated from `projects/c-rsp/BUILD_CONTRACT.md`. The term "signature tool" is replaced with **"canonical tool"** throughout.

### Series A: Constitutional Refactor

**Purpose:** Rewrite the three canonical truth surfaces to codify the taxonomy.

| Contract | Scope | Key Deliverables |
|---|---|---|
| **A-1: Taxonomy Canonicalization** (FIRST MOVE) | Codify Domains/Jurisdictions/Institutions/Projects/Verification layers into THE_LIVING_CONSTITUTION.md, root CLAUDE.md, and MASTER_PROJECT_INVENTORY.* | Updated Article VI (Institutionalization) with taxonomy layers; domain→institution registry in MASTER_PROJECT_INVENTORY.json; CLAUDE.md project registry updated with institutional roles; all three surfaces in agreement |
| **A-2: C-RSP Template Unification** | Upgrade the default BUILD_CONTRACT template in CLAUDE.md to C-RSP with tiered detail. Kill the prose-only path. | Single unified template; Tier-1 minimum enforces Blind Man's test (ordered operations, halt conditions, success conditions); fill-in-the-blank workflow; detail level chosen at contract start; common contract templates for product side |
| **A-3: SentinelOS Disposition** | Evaluate SentinelOS: absorb, deprecate, or redefine | Decision document + constitutional amendment if needed; update all references |
| **A-4: ClarityAI Discovery** | Discover and classify ClarityAI from GitHub; determine domain assignment and institutional role | Classification document; MASTER_PROJECT_INVENTORY.* entry if applicable |

**Critical path:** A-1 must complete first. A-2 through A-4 can run in parallel after A-1.

### Series B: Taxonomy Topography

**Purpose:** Build the machine-readable registry schema and formalize every project's constitutional role.

| Contract | Scope | Key Deliverables |
|---|---|---|
| **B-1: Domain Registry Schema** | Define JSON schema for domains, institutions, governed projects, canonical tools, evidence paths, integrated/standalone paths | `schemas/domain-registry.schema.json`; populated `config/domain-registry.json` |
| **B-2: Dual-Topology Census** | Audit all 20+ projects for dual-topology compliance; identify which need integrated+standalone paths; create migration plan for non-compliant projects | Census report; per-project topology status; migration queue |
| **B-3: Canonical Tool Registry** | Formalize the canonical tool for each institution — the named component that does the bulk of governance work in that domain | Registry entries in domain-registry.json; tool→invariant mapping |
| **B-4: ITAYN/HUNS Evaluation** | Evaluate candidate repos for TLC inclusion; classify or defer | Evaluation document per candidate |

### Series C: Overlay Productization

**Purpose:** Build TLC as a product overlay for frontier coding agents.

| Contract | Scope | Key Deliverables |
|---|---|---|
| **C-1: Guardian Mode (Claude Code)** | Terminal wrapper that intercepts Claude Code commands, validates against invariant registry, provides Litigation HUD | `packages/tlc-guardian/` — terminal wrapper; invariant interceptor; evidence collector; governed by Golden Sandbox |
| **C-2: Policy Sidecar (Codex/Copilot)** | MCP-based context injection for IDE-integrated agents | MCP server definition; dynamic `.github/copilot-instructions.md` generation from STATUS.json |
| **C-3: Context Bridge (Gemini)** | Context filter using Gemini's large context window; defines No-Go Zones and High-Trust Zones | Context filter specification; MCP integration |
| **C-4: IDE Portability** | Institutionalize Cursor's structured response format (Kanban + V&T) across all models; ensure C-RSP contracts execute identically in Claude Code, Cursor, Codex | `.cursor/rules/` propagation; CLAUDE.md response format enforcement; model-agnostic contract execution guide |

**Critical path:** C-1 first (Claude Code is primary environment). C-4 should run in parallel with C-1. C-2 and C-3 follow.

### Series D: Domain Packs

**Purpose:** Build the Core + Plugin invariant architecture.

| Contract | Scope | Key Deliverables |
|---|---|---|
| **D-1: Universal Core Pack** | Extract universal invariants from the existing 59 into a reusable core pack applicable to any domain | `packages/tlc-governance-kit/packs/universal/` |
| **D-2: Domain-Specific Pack Architecture** | Define the plugin system for on-demand domain packs (FinTech, Healthcare, etc.) | Pack schema; hydration workflow; `tlc init --domain <name>` specification |
| **D-3: First Domain Pack (FinTech or Healthcare)** | Build one pre-packaged domain pack as proof of concept | Complete pack with domain-specific invariants, evidence requirements, and acceptance criteria |

### Series E: Constitutional UI

**Purpose:** Build the Control Plane as a governed product (not the front door).

| Contract | Scope | Key Deliverables |
|---|---|---|
| **E-1: Control Plane MVP** | Core API that serves Constitution state, STATUS.json, and domain health | `projects/tlc-control-plane/src/app.py` with full PASS 8 compliance |
| **E-2: Litigation HUD** | Interactive governance interface for real-time rule negotiation | Litigation tab; version comparison; adversarial scenario testing |
| **E-3: Desktop App Shell** | Standalone desktop wrapper (not IDE — like Claude Desktop) | `standalone/tlc-ui-desktop/` with dual-topology parity |

---

## Execution Order

```
A-1 (Taxonomy Canonicalization) ← FIRST MOVE, blocks everything
 ├── A-2 (C-RSP Unification) ← can start after A-1
 ├── A-3 (SentinelOS Disposition) ← can start after A-1
 └── A-4 (ClarityAI Discovery) ← can start after A-1
      │
      v
B-1 through B-4 (Taxonomy Topography) ← after Series A complete
      │
      v
C-1 + C-4 in parallel (Guardian Mode + IDE Portability) ← after Series B
C-2, C-3 follow C-1
      │
      v
D-1 through D-3 (Domain Packs) ← after Series C
      │
      v
E-1 through E-3 (Constitutional UI) ← after Series D
```

---

## The First Move: Contract A-1

**A single C-RSP Build Contract whose only job is to canonicalize the taxonomy and topography across three truth surfaces:**

1. `THE_LIVING_CONSTITUTION.md` — Add Article VI section formalizing the 5-layer taxonomy (Article, Domain, Institution, Project, Verification)
2. Root `CLAUDE.md` — Update the Project Registry table to include domain assignment, institutional role (governing body vs. governed project vs. infrastructure), canonical tool name, and topology mode for every project
3. `MASTER_PROJECT_INVENTORY.json` / `MASTER_PROJECT_INVENTORY.md` — Add `domain_registry` object with institution-to-project mapping, canonical tools, and dual-topology paths

**This contract must be fully instantiated against `projects/c-rsp/BUILD_CONTRACT.md` (all 17 sections) before execution.**

### Files to Modify (A-1)

| File | Change |
|---|---|
| `THE_LIVING_CONSTITUTION.md` | Add taxonomy layer definitions; formalize domain jurisdiction model |
| `CLAUDE.md` (root) | Rewrite Project Registry with domain, institution role, canonical tool columns |
| `MASTER_PROJECT_INVENTORY.json` | Add `domain_registry` schema with institution→project→tool mapping |
| `MASTER_PROJECT_INVENTORY.md` | Sync with JSON (token parity) |
| `config/domains.ts` | Add `governingBodies` and `canonicalTool` fields to SafetyDomain interface |
| `config/projects.ts` | Add `institutionalRole` and `canonicalTool` fields to project entries |

### Files to Read (reference, not modify)

| File | Purpose |
|---|---|
| `projects/c-rsp/BUILD_CONTRACT.md` | Canonical template — contract must conform |
| `projects/c-rsp/contract-schema.json` | Schema validation |
| `projects/c-rsp/CRSP_OUTCOME_TEMPLATE.md` | Output format |
| `00-constitution/invariant-registry.json` | 59 invariants to map to domains |
| `00-constitution/doctrine-to-invariant.map.json` | Doctrine→invariant relationships |
| `00-constitution/role-registry.json` | Separation of powers roles |
| Every `projects/*/BUILD_CONTRACT.md` | Current state of each project |

---

## Verification

After A-1 execution:
1. `python3 scripts/verify_governance_chain.py --root .` exits 0
2. `python3 scripts/verify_project_topology.py --root . --with-governance` exits 0
3. THE_LIVING_CONSTITUTION.md, root CLAUDE.md, and MASTER_PROJECT_INVENTORY.json all reference the same taxonomy layers and domain assignments
4. No project exists in one surface but not the others (census parity)
5. The Kanban board for A-1 is clear before any Series B contract is instantiated

---

---


## C-RSP Golden Workflow Templates (Contract A-2 Detail)

### Problem

The current `BUILD_CONTRACT.md` template is constitutionally ambitious but operationally weak. It does not reliably pass the Blind Man Test because it allows:

- master-template rules to blur into instance content
- prose requirements without executable payloads
- implementation-bearing contracts without component code shape
- topology claims without paired path discipline
- tier selection without structural consequences
- acceptance criteria that are sometimes stronger than the evidence plan

The template must be revised so an executor can determine, from text alone:

1. what kind of contract this is
2. what exact artifacts are in scope
3. what exact steps to perform in order
4. what code shape is expected for major components
5. when to halt
6. how to prove success
7. what is not being claimed

### Design Correction

The revised C-RSP system has three distinct artifacts and they must never be conflated:

| Artifact | Purpose | May Contain Concrete Project Content? |
|---|---|---|
| `BUILD_CONTRACT.md` | Canonical master template | No |
| `BUILD_CONTRACT.instance.md` | Workflow-friendly instance template | Only instance fields, not executed outcomes |
| Project `BUILD_CONTRACT` / `BUILD_CONTRACT.md` | Fully instantiated executable contract for one task | Yes |

### Non-Negotiable Structural Fixes

#### 1. Blind Man Test becomes a hard structural section, not a principle

Every executable contract, at every tier, must include a required execution payload with:

- **Ordered Operations**
- **Halt Conditions**
- **Success Conditions**
- **Failure Handling**

Every ordered step must contain:

- actor
- exact action
- exact input artifact
- exact output artifact
- verification method
- failure response

No vague execution language is permitted in executable sections.

#### 2. Major Component code shape becomes mandatory

If the work type is **Build**, **Fix**, or **Refactor**, and a component is materially changed, the contract must include a dedicated subsection for each major component with:

- component name
- exact path
- role
- interface contract
- invariant coverage
- implementation status
- **real code snippet or structural stub**
- exact verification command
- failure signature

This closes the gap where a contract says "build the engine" or "wire the verifier" without showing the expected code shape.

#### 3. Tiering must change what is required, not just what is visible

The tiers are:

| Tier | Name | Required Minimum |
|---|---|---|
| Tier-1 | Quick / MVG | Identity, topology, execution payload, acceptance, preflight, output |
| Tier-2 | Standard / Operational | Tier-1 plus baseline, risk, lifecycle, rollback, evidence |
| Tier-3 | Full / Constitutional | All canonical sections plus dependency graph, invariant completeness, conflict matrix, halt matrix, governance lock |

A lower-tier contract may not silently claim higher-tier completeness.

#### 4. Dual-topology contracts must be fail-closed

If `Topology Mode = Dual-Topology`, the contract must:

- name the integrated path
- name the standalone path
- define parity or controlled divergence rules
- define the verifier scope for both paths
- block completion claims if one path is unresolved
- register the blocked follow-on build in `projects/c-rsp/NEXT_CRSP_BUILD.json`

#### 5. Master template and instance template must not contain executed-state language

The master template and the instance template must not contain:

- outcome summaries
- done-state language
- project-specific execution claims
- repo-specific evidence claims unless those are clearly labeled as instance inputs

### Revised Master Template Requirements

The canonical `projects/c-rsp/BUILD_CONTRACT.md` must require these sections in canonical order:

1. Contract Identity  
2. Contract Topology + Profile  
3. Baseline State  
4. Dependencies and Inputs  
5. Risk + Control Classification  
6. Execution Model  
7. Lifecycle State Machine  
8. Invariants  
9. Acceptance Criteria  
10. Rollback & Recovery  
11. Evidence + Truth Surface  
12. Conflict Matrix  
13. Halt Matrix  
14. Preflight  
15. Adoption Tiers  
16. Output Format  
17. Instance Declaration

### Required Execution Model Substructure

Section 6 must always contain:

#### 6A. Ordered Operations

For each step:

```markdown
- **Step ID:** OP-01
- **Actor:** human | agent | CI | verifier
- **Action:** exact command or exact file operation
- **Inputs:** exact file(s) or artifact(s)
- **Outputs:** exact file(s), artifact(s), or observable console output
- **Verify:** exact command, test, diff, or inspection
- **If Failure:** exact halt, rollback, or escalation action
```

#### 6B. Halt Conditions

Every halt entry must have:

- condition
- stop reason
- next action

#### 6C. Success Conditions

Every success entry must be objectively observable.

#### 6D. Major Component Implementation Snippets

Required when `Work Type = Build | Fix | Refactor` and a component is materially affected.

For each major component:

```markdown
#### Component: {COMPONENT_NAME}
- **Path:** {EXACT_PATH}
- **Role:** {ONE SENTENCE}
- **Interface Contract:** {INPUTS / OUTPUTS / CALL SURFACE}
- **Invariant Coverage:** {LIST}
- **Implementation Status:** Draft | Canonical Example | Production Target
- **Snippet:**
```ts
// real code or structural stub
```
- **Verification:** {EXACT_COMMAND}
- **Failure Signature:** {HOW BREAKAGE PRESENTS}
```

### Revised Instance Template Requirements

The workflow-friendly `BUILD_CONTRACT.instance.md` must:

- compile down to the canonical 17-section structure
- use guided prompts instead of `[REQUIRED]`
- preserve every required section even when the tier hides detail from the user
- fill below-tier sections with canonical `N/A — below tier threshold` values rather than omitting them
- require the Blind Man execution payload at every tier
- require code snippets for major components when applicable

### Validation Rule

A C-RSP template or instance is invalid if any of the following are true:

1. canonical section order is broken
2. an executable section contains vague continuation language
3. a material component is changed without a component snippet block
4. a dual-topology contract names only one path and still claims completion
5. a success condition is not observable
6. a halt condition lacks an exact next action
7. evidence claims exceed the truth surface
8. a lower-tier contract implies higher-tier guarantees

### A-2 Deliverables (Corrected)

| Deliverable | Purpose |
|---|---|
| `projects/c-rsp/BUILD_CONTRACT.md` | Revised canonical master template |
| `projects/c-rsp/BUILD_CONTRACT.instance.md` | Revised guided instance template |
| `projects/c-rsp/workflows/ROUTER.md` | Tier + work-type decision router |
| `projects/c-rsp/workflows/tier-1-quick.template.md` | Quick workflow template |
| `projects/c-rsp/workflows/tier-2-standard.template.md` | Standard workflow template |
| `projects/c-rsp/workflows/tier-3-full.template.md` | Full workflow template |
| `projects/c-rsp/workflows/partials/blind-mans-test.partial.md` | Required execution payload partial |
| `projects/c-rsp/workflows/partials/component-snippet.partial.md` | Required major-component snippet partial |
| `projects/c-rsp/workflows/type-starters/*.md` | Work-type starter prompts |

### Relationship to A-1

Contract **A-1** should not execute against the old template. The corrected sequence is:

1. repair the canonical C-RSP template system
2. validate that the repaired template passes the Blind Man Test
3. instantiate A-1 using the repaired instance template
4. execute A-1 only after template repair is verified

### Key Terminology

- **C-RSP** = Constitutionally-Regulated Single Pass
- **Canonical tool** = the named component that does the bulk of governance/enforcement work for an institution
- **Dual-topology** = integrated TLC component plus standalone governed product
- **Blind Man Test** = text-only executability with no visual inference or omitted steps
- **Major component snippet** = required code-shape block for any materially changed component
