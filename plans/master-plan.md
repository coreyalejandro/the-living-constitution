# TLC Enterprise Restructuring: Master Plan

## Session Status (as of 2026-04-05)

- **Plan status:** COMPLETE — reviewed; **A-0** and **A-0.1** executed in-repo for the C-RSP template system.
- **A-0:** Documentation system overhaul — see `projects/c-rsp/outcomes/CRSP-A0-DOCSYS-OVERHAUL-001.md`.
- **A-0.1 (CRSP-A0-1-SEMANTIC-CANONICALIZATION-001):** Semantic canonicalization — explicit **authority order** (master > guided instance > schema > outcome > `workflows/*` > executed contracts), vocabulary, and **INVARIANT_SEM_01–04** in `projects/c-rsp/BUILD_CONTRACT.md`; subordinate **Artifact Role** in `BUILD_CONTRACT.instance.md`; `projects/c-rsp/CANONICAL_ROLE_MAP.md`; `projects/c-rsp/workflows/README.md`; aligned `CLAUDE.md`, `MASTER_PROJECT_INVENTORY.*`, `contract-schema.json` (`authority_order_crsp_a0_1`), `CRSP_OUTCOME_TEMPLATE.md` outcome-artifact label. Outcome: `projects/c-rsp/outcomes/CRSP-A0-1-SEMANTIC-CANONICALIZATION-001.md`.
- **Branch:** `claude/restructure-tlc-enterprise-LxIXt` (develop and push here)
- **Next action:** (1) Review A-0 / A-0.1 outcomes, (2) proceed to **A-1** only when satisfied with semantic clarity, (3) run `./scripts/run_fde_control_plane_verification.sh` after pulls if FDE paths change

### Key Decisions Made
- **C-RSP** = Constitutionally-Regulated Single Pass (canonical expansion, no variants)
- **"Canonical tool"** replaces "signature tool"
- **Front door** = README → STATUS.json / STATUS.md (NOT the Golden Sandbox)
- **Golden Sandbox** = execution substrate / guarded ingress
- **Blind Man Test** enforced structurally at every tier, with required ordered operations, halt conditions, success conditions, and major-component code snippets when code-bearing components materially change
- **3 Adoption Tiers** surface as user-facing workflow choice (Quick/Standard/Full)
- **5 Work Types** (Build/Fix/Refactor/Governance/Discovery) with type-specific starter prompts
- **CONTROL_RULE_KBC_01**: Single active BUILD_CONTRACT at a time until clear; no constitutional execution against a known-bad template system

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

## Immediate Next Move: Documentation Overhaul Before Execution

TLC does **not** need another partial contract first. It needs a **document overhaul across the constitutional truth surfaces, the C-RSP template system, and the template folder semantics** before any further execution claims are made.

### Why this is first

The current state has three compounding problems:

1. **Truth-surface drift** — `THE_LIVING_CONSTITUTION.md`, root `CLAUDE.md`, `MASTER_PROJECT_INVENTORY.*`, and the plan are not yet aligned
2. **Template drift** — `projects/c-rsp/BUILD_CONTRACT.md` and `projects/c-rsp/BUILD_CONTRACT.instance.md` are semantically inverted or unclear in role
3. **Documentation-system drift** — project contracts, template artifacts, workflow guidance, and constitutional instructions are mixed together in a way that fails the Blind Man Test

### A-0: Documentation System Overhaul (new blocking contract)

**Purpose:** Repair the document system before constitutional refactor execution.

| Contract | Scope | Key Deliverables |
|---|---|---|
| **A-0: Documentation System Overhaul** (NEW FIRST MOVE) | Normalize the C-RSP folder, clarify master-template vs. instance-template vs. executed-contract roles, repair naming, and align all governing documentation surfaces | Canonical role map for all C-RSP artifacts; corrected template hierarchy; Blind-Man-Test-compliant template requirements; document census; constitutional truth-surface alignment plan |

### A-0 Target Surfaces

The overhaul must explicitly inventory and reconcile at minimum:

- `README.md`
- `STATUS.json`
- `STATUS.md`
- `THE_LIVING_CONSTITUTION.md`
- root `CLAUDE.md`
- `MASTER_PROJECT_INVENTORY.json`
- `MASTER_PROJECT_INVENTORY.md`
- `projects/c-rsp/BUILD_CONTRACT.md`
- `projects/c-rsp/BUILD_CONTRACT.instance.md`
- `projects/c-rsp/contract-schema.json`
- `projects/c-rsp/CRSP_OUTCOME_TEMPLATE.md`
- `projects/*/BUILD_CONTRACT*`
- `projects/*/CLAUDE.md`
- `plans/master-plan.md`

### A-0 Success Standard

A-0 is complete only when all of the following are true:

1. the role of each governing document is explicit
2. the template system has a clear hierarchy
3. the Blind Man Test is encoded structurally in the template system
4. the documentation system clearly separates:
   - constitutional truth surfaces
   - template artifacts
   - workflow artifacts
   - executed project contracts
5. A-1 can be instantiated without guessing which file is authoritative

### A-0.1: Semantic canonicalization (substep of A-0 program)

**Purpose:** Codify **artifact roles**, **terminology**, and **strict authority order** so executors do not rely on filename intuition.

**Deliverables:** `projects/c-rsp/CANONICAL_ROLE_MAP.md`; **Canonical Artifact Role** section in `projects/c-rsp/BUILD_CONTRACT.md`; **Artifact Role** in `projects/c-rsp/BUILD_CONTRACT.instance.md`; aligned root `CLAUDE.md`, inventory, plan, schema metadata, outcome template header.

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

**Purpose:** After A-0 repairs the documentation system, rewrite the canonical truth surfaces to codify the taxonomy.

| Contract | Scope | Key Deliverables |
|---|---|---|
| **A-0: Documentation System Overhaul** (NEW FIRST MOVE) | Repair the document system and C-RSP template hierarchy before constitutional execution | Canonical document role map; repaired C-RSP template system; normalized artifact naming/placement; Blind-Man-Test-compliant template requirements |
| **A-1: Taxonomy Canonicalization** (FIRST MOVE) | Codify Domains/Jurisdictions/Institutions/Projects/Verification layers into THE_LIVING_CONSTITUTION.md, root CLAUDE.md, and MASTER_PROJECT_INVENTORY.* | Updated Article VI (Institutionalization) with taxonomy layers; domain→institution registry in MASTER_PROJECT_INVENTORY.json; CLAUDE.md project registry updated with institutional roles; all three surfaces in agreement |
| **A-2: C-RSP Template Unification** | Upgrade the default BUILD_CONTRACT template in CLAUDE.md to C-RSP with tiered detail. Kill the prose-only path. | Single unified template; Tier-1 minimum enforces Blind Man's test (ordered operations, halt conditions, success conditions); fill-in-the-blank workflow; detail level chosen at contract start; common contract templates for product side |
| **A-3: SentinelOS Disposition** | Evaluate SentinelOS: absorb, deprecate, or redefine | Decision document + constitutional amendment if needed; update all references |
| **A-4: ClarityAI Discovery** | Discover and classify ClarityAI from GitHub; determine domain assignment and institutional role | Classification document; MASTER_PROJECT_INVENTORY.* entry if applicable |

**Critical path:** A-0 must complete first. A-1 depends on A-0. A-2 through A-4 may proceed only after the repaired template/document system is in place.

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

```text
A-0 (Documentation System Overhaul) ← NEW FIRST MOVE, blocks everything
      │
      v
A-1 (Taxonomy Canonicalization) ← depends on repaired template/document system
 ├── A-2 (C-RSP Unification) ← can continue after A-0; must not drift from A-1
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

## The First Move: Contract A-0

**A single C-RSP Build Contract whose only job is to overhaul the documentation system and normalize the constitutional document hierarchy before any taxonomy execution begins.**

### A-0 Objectives

1. Explicitly classify every governing document by role
2. Normalize the C-RSP template hierarchy:
   - canonical master template
   - guided instance template
   - workflow/router artifacts
   - executed project contracts
3. Identify naming/path inversions and document-system drift
4. Encode Blind-Man-Test structural requirements into the template system
5. Produce a clean handoff so A-1 can execute against an unambiguous template/document system

### Files to Modify (A-0)

| File | Change |
|---|---|
| `plans/master-plan.md` | Update execution order and blocking dependency to A-0 first |
| `projects/c-rsp/BUILD_CONTRACT.md` | Repair canonical master-template structure and role |
| `projects/c-rsp/BUILD_CONTRACT.instance.md` | Repair guided instance-template role and ergonomics |
| `projects/c-rsp/contract-schema.json` | Reconcile schema with required structural Blind-Man-Test fields if needed |
| `projects/c-rsp/CRSP_OUTCOME_TEMPLATE.md` | Ensure output shape matches repaired contract system |
| `root CLAUDE.md` | Update Zero-Shot Build Contract guidance to point at repaired template hierarchy |
| `MASTER_PROJECT_INVENTORY.md` | Add or sync any document-system artifact notes if required |

### Files to Read (reference, not modify unless required by contract)

| File | Purpose |
|---|---|
| `README.md` | Confirm front-door positioning and governing entrypoint |
| `STATUS.json` / `STATUS.md` | Confirm operational truth-surface role |
| `THE_LIVING_CONSTITUTION.md` | Confirm constitutional role and amendment pressure |
| `projects/*/BUILD_CONTRACT*` | Inventory executed contract patterns and drift |
| `projects/*/CLAUDE.md` | Inventory local project instruction surfaces |
| `plans/master-plan.md` | Keep plan aligned with repaired template system |

### A-0 Output

A-0 must produce a normalized document system in which an executor can answer, from text alone:

- which file is the canonical template
- which file is the guided instance template
- which files are workflow artifacts
- which files are executed project contracts
- what structural fields are required for Blind-Man-Test compliance

## The Second Move: Contract A-1

Only after A-0 is complete:

**A single C-RSP Build Contract whose only job is to canonicalize the taxonomy and topography across three truth surfaces:**

1. `THE_LIVING_CONSTITUTION.md` — Add Article VI section formalizing the 5-layer taxonomy (Article, Domain, Institution, Project, Verification)
2. Root `CLAUDE.md` — Update the Project Registry table to include domain assignment, institutional role (governing body vs. governed project vs. infrastructure), canonical tool name, and topology mode for every project
3. `MASTER_PROJECT_INVENTORY.json` / `MASTER_PROJECT_INVENTORY.md` — Add `domain_registry` object with institution-to-project mapping, canonical tools, and dual-topology paths

**A-1 must be instantiated only against the repaired template system created by A-0.**

### Files to Modify (A-1)

| File | Change |
|---|---|
| `THE_LIVING_CONSTITUTION.md` | Add taxonomy layer definitions; formalize domain jurisdiction model |
| `CLAUDE.md` (root) | Rewrite Project Registry with domain, institution role, canonical tool columns |
| `MASTER_PROJECT_INVENTORY.json` | Add `domain_registry` schema with institution→project→tool mapping |
| `MASTER_PROJECT_INVENTORY.md` | Sync with JSON (token parity) |
| `config/domains.ts` | Add `governingBodies` and `canonicalTool` fields to SafetyDomain interface |
| `config/projects.ts` | Add `institutionalRole` and `canonicalTool` fields to project entries |

### Files to Read (A-1 reference)

| File | Purpose |
|---|---|
| `projects/c-rsp/BUILD_CONTRACT.md` | Repaired canonical template |
| `projects/c-rsp/BUILD_CONTRACT.instance.md` | Repaired guided instance template |
| `projects/c-rsp/contract-schema.json` | Schema validation |
| `projects/c-rsp/CRSP_OUTCOME_TEMPLATE.md` | Output format |
| `00-constitution/invariant-registry.json` | 59 invariants to map to domains |
| `00-constitution/doctrine-to-invariant.map.json` | Doctrine→invariant relationships |
| `00-constitution/role-registry.json` | Separation of powers roles |
| Every `projects/*/BUILD_CONTRACT*` | Current project constitutional role pressure |

### A-1 Output

A-1 must produce three aligned, taxonomy-canonical surfaces and an updated project registry.

---

## Verification

1. `python3 scripts/verify_governance_chain.py --root .` exits 0 after A-1
2. `python3 scripts/verify_project_topology.py --root . --with-governance` exits 0 after A-1
3. `projects/c-rsp/BUILD_CONTRACT.md` and `projects/c-rsp/BUILD_CONTRACT.instance.md` have distinct, explicit roles after A-0
4. THE_LIVING_CONSTITUTION.md, root CLAUDE.md, and MASTER_PROJECT_INVENTORY.json all reference the same taxonomy layers and domain assignments after A-1
5. No project exists in one surface but not the others (census parity)
6. The Kanban board for A-0 is clear before A-1 is instantiated, and the Kanban board for A-1 is clear before any Series B contract is instantiated

---
---

## C-RSP Golden Workflow Templates (Contract A-2 Detail)

### Problem

The current `BUILD_CONTRACT.md` template is a 17-section constitutional master. It's correct but **not ergonomic**: every field says `[REQUIRED]`, there's no guided workflow, and a human or agent filling it out must already know the schema to avoid mistakes. The tier system (Tier-1/2/3) exists in the schema but isn't surfaced as a user-facing choice that controls what they see.

The Blind Man's Test — "Could someone who has never seen this codebase execute this contract by following the steps in order, knowing when to stop, and knowing what success looks like?" — is the quality bar, but it's not enforced structurally.

### Design: Three Layers

```
┌─────────────────────────────────────────────────┐
│  Layer 1: WORKFLOW ROUTER (detail chooser)       │
│  "What kind of work? What tier?"                 │
│  → Selects template + sets visible sections      │
├─────────────────────────────────────────────────┤
│  Layer 2: FILL-IN-THE-BLANK TEMPLATE             │
│  Per-tier, per-type guided prompts               │
│  Blind Man's Test enforced at every tier          │
├─────────────────────────────────────────────────┤
│  Layer 3: CANONICAL SCHEMA (unchanged)           │
│  contract-schema.json — immutable 17 sections    │
│  Workflow templates compile DOWN to this          │
└─────────────────────────────────────────────────┘
```

Layer 3 (the existing schema) does NOT change. Layers 1 and 2 are new.

### Layer 1: Workflow Router

At contract start, two questions determine the template:

**Question 1: What tier of governance?**

| Choice | Visible Sections | Use When |
|---|---|---|
| **Quick (Tier-1-MVG)** | §1 Identity, §2 Topology, §6 Execution (ops only), §9 Acceptance (pass/fail only), §14 Preflight, §16 Output | Single-file changes, documentation updates, config tweaks, discovery tasks |
| **Standard (Tier-2-Operational)** | All of Quick + §3 Baseline, §5 Risk, §7 Lifecycle, §10 Rollback, §11 Evidence | Feature builds, refactors, integrations, multi-file changes |
| **Full (Tier-3-Constitutional)** | All 17 sections | Cross-repo governance, constitutional amendments, new institution creation, dual-topology enforcement |

**Question 2: What type of work?**

| Type | Starter Prompts | Blind Man's Emphasis |
|---|---|---|
| **Build** | "What are you building? What exists now? What does done look like?" | Ordered build steps, file creation sequence, test commands |
| **Fix** | "What's broken? How do you reproduce it? What does fixed look like?" | Repro steps, root cause, verification command |
| **Refactor** | "What's changing shape? What must stay the same? How do you prove equivalence?" | Before/after invariants, regression test commands |
| **Governance** | "What rule is changing? What does it affect? How do you verify compliance?" | Affected surfaces, compliance check commands, amendment procedure |
| **Discovery** | "What are you investigating? What would you do with the answer? When do you stop?" | Search scope, halt conditions (found/not-found), output artifact |

The router produces a `CONTRACT_WORKFLOW_HEADER` block at the top of the instance:

```markdown
<!-- C-RSP Workflow Header -->
<!-- Tier: Quick | Standard | Full -->
<!-- Type: Build | Fix | Refactor | Governance | Discovery -->
<!-- Blind Man's Test: ENFORCED -->
<!-- Generated: YYYY-MM-DD -->
```

### Layer 2: Fill-in-the-Blank Templates

Each tier×type combination gets guided prompts instead of raw `[REQUIRED]`. The Blind Man's Test is enforced by requiring three specific subsections in every Execution Model (§6), regardless of tier:

#### Blind Man's Test Block (mandatory at every tier)

```markdown
## 6. Execution Model

### 6.BMT — Blind Man's Test

#### Ordered Operations
<!-- List every step in execution order. A person who has never seen this
     codebase must be able to follow these steps top-to-bottom without
     judgment calls. If a step requires a decision, it's not ready. -->

1. [Step]: [Exact command or action] → [Expected output]
2. [Step]: [Exact command or action] → [Expected output]
3. ...

#### Halt Conditions
<!-- When must execution STOP? List every condition that means
     "do not continue, something is wrong." -->

- HALT if: [condition] → [what to do instead]
- HALT if: [condition] → [what to do instead]

#### Success Conditions
<!-- How does the executor KNOW they're done? Not "it works" —
     specific observable outcomes. -->

- SUCCESS when: [observable condition]
- SUCCESS when: [observable condition]
- DONE when: ALL success conditions met AND zero halt conditions active
```

#### Quick (Tier-1) Fill-in-the-Blank

```markdown
# C-RSP Instance: [What are you doing, in ≤10 words?]

## 1. Identity
- **Title:** [name]
- **ID:** CRSP-[YYYY]-[NNN]
- **Tier:** Tier-1-MVG
- **Objective:** [One sentence: what does this accomplish?]
- **Scope:** [What files/systems are touched?]
- **Not in scope:** [What are you explicitly NOT doing?]

## 2. Topology
- **Mode:** [TLC-Core | Satellite | Dual-Topology]
- **Truth surface:** [Which file is the source of truth for this change?]

## 6. Execution (Blind Man's Test)

### Ordered Operations
1. ...

### Halt Conditions
- HALT if: ...

### Success Conditions
- SUCCESS when: ...

## 9. Acceptance Criteria
| What | How to check | Pass if |
|---|---|---|
| [criterion] | [command or inspection] | [expected result] |

## 14. Preflight
- [ ] No placeholders remain
- [ ] Topology declared
- [ ] Commands in Ordered Operations are copy-pasteable

## 16. Output → CRSP_OUTCOME_TEMPLATE.md
```

#### Standard (Tier-2) Fill-in-the-Blank

Includes everything from Quick, plus:

```markdown
## 3. Baseline
- **Current state:** [What exists RIGHT NOW? Be honest.]
- **Anchor commit:** [SHA or "HEAD of <branch>"]
- **Known gaps:** [What's missing or broken that this contract addresses?]

## 5. Risk
- **Risk class:** [Low | Moderate | High]
- **Side effects:** [What changes outside the target files?]
- **Reversible?** [Yes: how | No: why not]

## 7. Lifecycle
- **Starting state:** Draft
- **Promotion gate:** [What must be true to mark Active → Frozen?]

## 10. Rollback
- **Safe state:** [Describe the state to return to if this fails]
- **Rollback command:** [Exact command: git revert, restore, etc.]

## 11. Evidence
- **Evidence paths:** [Where does proof live after execution?]
- **Truth discipline:** [What claims does this contract make, and where is proof?]
```

#### Full (Tier-3) Fill-in-the-Blank

Includes everything from Standard, plus all remaining sections (§4 Dependencies, §8 Invariants, §12 Conflict Matrix, §13 Halt Matrix) with guided prompts. Same pattern: questions instead of `[REQUIRED]`.

### Workflow File Locations

```
projects/c-rsp/
  BUILD_CONTRACT.md              ← Master template (unchanged)
  contract-schema.json           ← Canonical schema (unchanged)
  CRSP_OUTCOME_TEMPLATE.md       ← Output format (unchanged)
  workflows/
    ROUTER.md                    ← Decision tree for tier + type selection
    tier-1-quick.template.md     ← Fill-in-the-blank for Tier-1
    tier-2-standard.template.md  ← Fill-in-the-blank for Tier-2
    tier-3-full.template.md      ← Fill-in-the-blank for Tier-3
    type-starters/
      build.md                   ← Starter prompts for Build type
      fix.md                     ← Starter prompts for Fix type
      refactor.md                ← Starter prompts for Refactor type
      governance.md              ← Starter prompts for Governance type
      discovery.md               ← Starter prompts for Discovery type
    blind-mans-test.partial.md   ← Reusable BMT block (included in all tiers)
```

### Validation Rule

A workflow template is valid if and only if:
1. It compiles to a valid `contract-schema.json` instance (sections not surfaced at the chosen tier are filled with canonical defaults or `N/A — below tier threshold`)
2. The Blind Man's Test block (§6.BMT) has ≥1 ordered operation, ≥1 halt condition, and ≥1 success condition
3. Every ordered operation has an exact command or action (no "figure out how to...")
4. Every halt condition has a recovery action (not just "stop")
5. Every success condition is observable (not "it works" — specific output, exit code, file state)

### How This Relates to the Plan

- **Contract A-2** builds these workflow templates
- **Contract A-1** (taxonomy canonicalization) will be the first contract **instantiated using** the Quick workflow (Tier-1, Governance type) — proving the template works
- All subsequent Series B-E contracts are instantiated through the router
- The root `CLAUDE.md` Zero-Shot Build Contract Format section gets replaced with a pointer to the router

---

## Key Terminology

- **C-RSP** = Constitutionally-Regulated Single Pass (canonical, no variants)
- **Canonical tool** = the named component that does the bulk of governance/enforcement work for an institution (replaces "signature tool")
- **Dual-topology** = every institution/product must exist as both integrated TLC component AND standalone product
- **Governing body / Institution** = the app/agent that governs a domain
- **Governed entity / Project** = consumer/dev product under institutional governance
- **Front door** = README → STATUS.json / STATUS.md (NOT the sandbox)
- **Execution substrate** = Golden Sandbox (guarded ingress for governed apps)
