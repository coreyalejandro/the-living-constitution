# ZERO-SHOT BUILD CONTRACT

## Project: The Living Constitution (TLC)

## Contract Version: ZSB-TLC-v1.0

## Type: Meta-Governance Infrastructure

## Parent Ecosystem: Safety Systems Design Commonwealth

## Amendment Authority: Constitutional Operator (Corey Alejandro)

---

You are building and maintaining **The Living Constitution** — the governance operating system for the Safety Systems Design Commonwealth.

TLC is not a product. It is not a feature set. It is not an app.

It is the **source of authority** for every build contract, every agent, every CLAUDE.md, every enforcement hook, and every truth claim across all Commonwealth projects.

Without TLC, projects have no constitutional grounding. Without TLC, governance is performance, not enforcement.

This contract specifies what TLC must be, must contain, and must deliver for it to function as the ultimate single source of truth.

---

## 0. Core Thesis

TLC exists because agentic systems that lack structured governance cause harm — not through malice but through:

- epistemic drift (false claims treated as true)
- cognitive harm (correct outputs producing false understanding)
- human exclusion (systems designed for the median user that harm everyone else)
- empirical failure (described behavior that does not match actual behavior)

TLC operationalizes the doctrine that **safety is architectural, not incidental**.

Its job is to make governance real — not aspirational, not a styleguide, not a vibe — by encoding constitutional principles directly into the agents, hooks, CLAUDE.md files, build contracts, and CI/CD pipelines that govern every system in the Commonwealth.

---

## 1. What TLC Is

TLC is a **governance infrastructure system** composed of:

| Component | What It Is |
|-----------|-----------|
| Constitutional principles | Enumerated rules that all Commonwealth projects must satisfy |
| Safety domain definitions | Four domains that classify every project's safety responsibility |
| Invariants | Machine-checkable properties that must always be true |
| Harm classes | Taxonomy of harms the system must prevent |
| Governance roles | Defined authorities with explicit can/cannot boundaries |
| Standards of evidence | Tiered verification requirements for claims |
| Admissibility framework | Rules governing what evidence is valid and when |
| Doctrine formation process | How recurring patterns become constitutional rules |
| Amendment process | How TLC itself evolves through Article V |
| Commonwealth registry | Census of all governed projects |
| Subsystem inheritance model | How all ZSB contracts derive authority from TLC |
| CLAUDE.md propagation | How Articles I–V reach every project repo |
| SOP library | Operational procedures for common governance scenarios |
| Eval harness integration | How capability evals are run across all subsystems |
| Governance audit trail | Chain of custody for governance decisions |

---

## 2. The Four Safety Domains

Every Commonwealth project maps to at least one domain. Unmapped projects are ungoverned (Census Doctrine, P7).

### D1 — Epistemic Safety

| Field | Value |
|-------|-------|
| **Focus** | Truth, claims, verification |
| **Failure class** | System asserts something untrue; user acts on it |
| **Governing article** | Article II (Execution Law) + Article III (Purpose Law) |
| **Primary harm** | H1 — Epistemic Harm |
| **Projects** | PROACTIVE, TLC Evidence Observatory, Portfolio |

### D2 — Human Safety

| Field | Value |
|-------|-------|
| **Focus** | Behavior, decisions, intervention |
| **Failure class** | System designed for median user; everyone else harmed |
| **Governing article** | Article I (Bill of Rights) |
| **Primary harm** | H2 — Human Harm |
| **Projects** | UICare-System, Portfolio, BuildLattice Guard |

### D3 — Cognitive Safety

| Field | Value |
|-------|-------|
| **Focus** | Understanding, learning, mental models |
| **Failure class** | Learning environment produces false understanding |
| **Governing article** | Article I + Article III |
| **Primary harm** | H3 — Cognitive Harm |
| **Projects** | Instructional Integrity Studio, Docen, Portfolio |

### D4 — Empirical Safety

| Field | Value |
|-------|-------|
| **Focus** | Measurement, evaluation, evidence |
| **Failure class** | Described behavior ≠ actual behavior; consent assumed |
| **Governing article** | Article III (Purpose Law) |
| **Primary harm** | H4 — Empirical Harm |
| **Projects** | ConsentChain, TLC Evidence Observatory, Frostbyte ETL, Portfolio |

---

## 3. The Ten Constitutional Principles

These are the substantive rules. Not schemas. Not field names. Rules.

Every subsystem ZSB contract is evaluated against these principles. Violation of any principle is a constitutional failure.

### P1 — Safety Priority

All system outputs, design decisions, and agentic behaviors prioritize the safety of the most vulnerable user over convenience, performance, or delivery speed.

The default user is a neurodivergent adult. Safety never loses a tradeoff.

**Violation:** Any design that prioritizes throughput, aesthetic polish, or delivery over user safety.

**Evidence requirement:** Tier 2 (tested) — automated accessibility and safety checks must pass.

---

### P2 — Epistemic Integrity

No claim may be asserted beyond the level of evidence that supports it.

The assurance level of any claim must match the verification method:

| Tier | Name | Method | Label Required |
|------|------|--------|---------------|
| T1 | Convention | Assertion only | "believed to be true" |
| T2 | Test | Automated test passes | "test-verified" |
| T3 | Validated | External or empirical study | "validated — [evidence reference]" |

Upgrading a claim from T1 to T3 without evidence is a P2 violation. Status inflation is epistemic harm.

**Violation:** Claiming `implemented` when only `partial`. Claiming `validated` without an evidence reference. Claiming `production-ready` without SOP-014 gate completion.

---

### P3 — Human Dignity

Every system output preserves the dignity of all users.

No output may shame, rush, exclude, or burden a user through design. Patience is infinite. Recovery is always possible. No urgency shaming. No incomplete-task warnings during pause.

**Violation:** Error messages that blame users. UI that creates panic or urgency. Outputs that assume or require able-bodied, neurotypical, or high-bandwidth operation.

---

### P4 — Cognitive Honesty

Correct content that produces false understanding is cognitively unsafe.

Systems must evaluate whether outputs produce accurate mental models, not merely accurate facts. Scaffolding quality is evaluated independently of content accuracy.

**Violation:** Instructional output that is factually correct but produces a false mental model. Explanations that skip prerequisite concepts without flagging the gap. Terminology used before it is defined.

---

### P5 — Empirical Accountability

Described behavior must match actual behavior.

No system may claim capabilities that are unverified. Truth-status files are the binding contract between the builder and the world. Every claim has an owner, a verification date, and a revalidation trigger.

**Violation:** README claims that don't match truth-status.md. Features labeled `implemented` with no passing tests. Status files not updated within their freshness window (7 days during active development; 30 days in maintenance).

---

### P6 — Idempotency

`f(f(x)) = f(x)`.

Every operation that claims to be deterministic must produce identical results on repeated execution with identical inputs. The user cannot break things by trying again. Recovery paths are as clear as happy paths.

**Violation:** Non-deterministic evaluation output from the same artifact and rubric. State mutations that produce different results on retry. Build processes that succeed once but not on repeat.

**Testable:** Run the same input 3 times; assert output equality.

---

### P7 — Census Completeness

Every component, project, capability, and claim must be inventoried.

Ungoverned = uncounted = unsafe. The Commonwealth registry (`config/projects.ts`) is the census instrument. Projects not in the registry are not under governance. Dead inventory is removed, not hidden.

**Violation:** Active projects not in `config/projects.ts`. Features not listed in truth-status.md. Claimed capabilities with no corresponding test or evidence.

---

### P8 — Change Leadership

Governance precedes code.

The build contract must exist and be reviewed before implementation begins. Incompleteness is honest, not weak. Show the act, not just the result. Plans are written before building. Amendments are formal, not informal.

**Violation:** Building before the build contract is written. Skipping plan mode for non-trivial changes. Making architectural changes without an ADR. Amending CLAUDE.md without an Article V process.

---

### P9 — Separation of Powers

No agent, system, or person has unchecked authority over governed domains.

Builders cannot approve their own work. Sentinels cannot override their own rules. Critical actions require human review. Agents operate within their Article IV boundaries.

**Violation:** Self-approval of code changes. Agent performing a Needs Human OK action without human review. Constitutional rule change without the Article V process.

---

### P10 — Evidence-Bound Action

Every output traces to a purpose. No output without a theory of change. No build without a contract. No claim without evidence. Dead artifacts are removed, not hidden.

**Violation:** Work items not in todo.md. Outputs that cannot be traced to a ToC&A node. Artifacts that exist but serve no active purpose. Sessions that produce outputs without V&T statements.

---

## 4. The Six Constitutional Invariants

These are machine-checkable properties that must hold at all times. Violation of any invariant is a constitutional failure that triggers the STOP protocol.

### I1 — Domain Coverage

Every project in `config/projects.ts` maps to at least one safety domain in `config/domains.ts`.

**Check:** `config/projects.ts` has no entry with an empty `domainIds` array.

---

### I2 — Status Honesty

No project holds `implemented` or `deployed` status without a truth-status file containing:

- at least one passing automated test (T2 evidence minimum)
- a last-verified date within the freshness window

**Check:** For every project with `status: "implemented"`, a truth-status file exists and contains test evidence.

---

### I3 — Contract Precedence

No subsystem build session may begin without:

- a build contract file at the project's required path
- the contract reviewed by the Constitutional Operator at least once

**Check:** Every `projects/[id]/BUILD_CONTRACT.md` or equivalent `docs/prompts/ZERO_SHOT_BUILD_CONTRACT__[PROJECT].md` exists before implementation begins.

---

### I4 — Release Gate Compliance

No project may claim release-readiness without passing all four SOP-014 Governance Release Gates:

- Gate 1: Audience compliance (Article VI)
- Gate 2: Failure handling (Article VII)
- Gate 3: Truth maintenance (Article VIII)
- Gate 4: Constitutional compliance (Articles I–V)

**Check:** truth-status.md includes SOP-014 gate checklist with all four gates marked pass.

---

### I5 — Amendment Integrity

No constitutional rule may be changed without following the Article V amendment process:

TRIGGER → OBSERVATION → PROPOSAL → EVAL → RATIFICATION

**Check:** Every change to CLAUDE.md, any governance file, or any SOP is committed with the message pattern `chore: amend constitution — [rule]`.

---

### I6 — V&T Currency

Every significant response, every document update, every PR description includes a V&T Statement.

Truth-status files not updated within their freshness window generate a staleness drift alarm.

**Check:** `docs/truth-status.md` `last_updated` date is within 7 days of today during active development.

---

## 5. The Three Core Doctrines

Doctrines are named operating principles that govern behavior across all domains. They are summaries of clusters of principles and invariants.

### Doctrine 1 — Idempotency

`f(f(x)) = f(x)`. Do it once. Do it again. Same result. The user cannot break things by trying again.

**Operationalized by:** P6, I6. Tested by determinism test suites. Applies to every evaluator, every compiler, every pipeline stage.

### Doctrine 2 — Calibrated Truth

The assurance level of a claim must match the method used to verify it. Never claim Tier 3 assurance at Tier 1. Never upgrade status without evidence.

**Operationalized by:** P2, P5, I2. Enforced by truth-status.md maintenance and V&T statements.

### Doctrine 3 — Census

You cannot govern what you have not counted. Every component is inventoried. Dead inventory is removed. Ungoverned = uncounted = unsafe.

**Operationalized by:** P7, I1. Enforced by `config/projects.ts` maintenance.

---

## 6. The Six Harm Classes

Every harm class has:
- a definition
- inclusion criteria (what qualifies)
- exclusion criteria (what does not qualify)
- a severity range (S1–S5)
- a governance response

### H1 — Epistemic Harm

**Definition:** A false belief is caused in a user's mind by system output. The user acts on this false belief.

**Includes:** Confident false claims, status inflation, hallucinated capabilities, unverified research citations, misleading progress indicators.

**Excludes:** Honest uncertainty statements; claims explicitly labeled as Tier 1 (Convention); future-state descriptions labeled as planned.

**Severity range:** S1 (caused confusion, no consequential action) → S5 (caused irreversible harm through confident false claim)

**Governance response:** Stop, correct, and re-verify. Article VIII truth-maintenance rules apply. V&T statement required on next output.

---

### H2 — Human Harm

**Definition:** A discriminatory, exclusionary, or dignity-violating outcome occurs for a user, particularly one whose needs differ from the "median" user profile.

**Includes:** Inaccessible UI, urgency shaming, cognitive overload by design, outputs that assume neurotypicality, systems that exclude based on disability, age, or language.

**Excludes:** Accidental UX friction not targeting any group; well-intentioned but imperfect accessibility that is being actively fixed.

**Severity range:** S1 (individual inconvenience) → S5 (systematic exclusion of protected class)

**Governance response:** Article I Bill of Rights applies. Immediate accessibility audit. SOP-007 (ND Cognitive Load Assessment) triggered.

---

### H3 — Cognitive Harm

**Definition:** A learning environment or instructional output produces a false mental model, regardless of factual accuracy.

**Includes:** Premature conclusions, terminology jumps, prerequisite gaps, compression overload, polished but unsafe explanations, misleading hierarchy.

**Excludes:** Simplified explanations explicitly labeled as simplifications; beginner-level introductions that defer advanced nuance.

**Severity range:** S1 (minor misconception, self-corrects) → S4 (deeply embedded false model that resists correction)

**Governance response:** IIS evaluation triggered. Cognitive Safety rubric applied. Remediation guidance required before re-publication.

---

### H4 — Empirical Harm

**Definition:** A measurement, evaluation, or evidence artifact describes behavior that does not match actual behavior. Consent is assumed where it was not given.

**Includes:** Test results claiming validation without a real validation study, metrics that describe the wrong thing, consent assumed from inaction, coverage numbers applied to untested code paths.

**Excludes:** Honest approximations labeled as approximations; estimates clearly marked as unvalidated.

**Severity range:** S1 (imprecise measurement, acknowledged) → S5 (fabricated evidence used for consequential decisions)

**Governance response:** ConsentChain + Evidence Observatory protocols. Chain of custody review. Evidence invalidation if breach found.

---

### H5 — Governance Harm

**Definition:** A constitutional process is bypassed, a rule is overridden without amendment, or an agent acts outside its Separation of Powers boundary.

**Includes:** Informal CLAUDE.md changes, self-approvals, agents performing Needs Human OK actions autonomously, skipping build contracts, skipping SOP-014 gates.

**Excludes:** Working in areas not yet covered by the Constitution; legitimate emergencies documented with SOP-013 (Session Recovery) protocol active.

**Severity range:** S2 (informal workaround, acknowledged and corrected) → S5 (deliberate override of safety invariant)

**Governance response:** Immediate STOP. Article V amendment process triggered. BuildLattice Guard enforcement decision logged.

---

### H6 — Integrity Harm

**Definition:** Chain of custody is broken, evidence is modified after recording, or an audit trail contains gaps.

**Includes:** Deleted chain-of-custody records, modified SHA-256 hashes, audit log gaps, evidence records without provenance spans, governance decisions not logged.

**Excludes:** Intentional compaction of working context (Claude Code context management); archival of observations beyond freshness window.

**Severity range:** S2 (accidental gap, no consequential use of compromised data) → S5 (deliberate tampering with evidence used for decisions)

**Governance response:** Evidence Observatory flagged. All downstream decisions from affected records held pending review. Integrity hash re-verification required.

---

## 7. Governance Roles and Authorities

### R1 — Constitutional Operator

**Who:** Corey Alejandro (primary); delegated reviewer for formal reviews

**Can do without approval:**
- Ratify amendments
- Define new principles
- Approve ZSB contracts
- Mark projects as released
- Override Sentinel signals with documented justification

**Cannot do:**
- Bypass SOP-014 gates retroactively without documentation
- Claim T3 (Validated) status for evidence they generated themselves without external review
- Modify TLC in ways that weaken neurodivergent accessibility (P1, P3 are absolute)

---

### R2 — Safety Evaluator

**Who:** Any reviewer operating in evaluation mode

**Can do without approval:**
- Run evaluations against published rubrics
- Flag potential safety violations
- Assign harm classes to artifacts
- Write adjudication records

**Cannot do:**
- Override another evaluator's adjudication without reconciliation
- Mark an artifact safe without running the applicable rubric
- Assign T3 (Validated) status to their own work

---

### R3 — Builder

**Who:** Any agent or person implementing features

**Can do without approval:**
- Write code, tests, files
- Create build contracts (for review)
- Run test suites
- Flag coverage gaps

**Cannot do:**
- Deploy to production
- Modify DB schema
- Change auth systems
- Approve their own work
- Skip the RED phase of TDD

---

### R4 — Sentinel Agent

**Who:** Automated safety checking agent

**Can do without approval:**
- Run safety checks
- Raise STOP signals
- Write audit logs
- Flag CRITICAL issues

**Cannot do:**
- Override other agents
- Modify its own rules
- Access user PII
- Auto-fix CRITICAL issues (flag only)

---

### R5 — Evidence Curator

**Who:** Reviewer operating on the Evidence Observatory pipeline

**Can do without approval:**
- Ingest and normalize artifacts
- Extract and classify events
- Write chain-of-custody records
- Flag events for adjudication

**Cannot do:**
- Modify records after chain-of-custody hash is written
- Adjudicate their own extractions (R2 or R1 must adjudicate)
- Delete chain-of-custody entries

---

## 8. Standards of Evidence

| Tier | Name | Definition | Minimum for Status Claim |
|------|------|-----------|--------------------------|
| T1 | Convention | Assertion; no external verification | `planned`, `prototype` |
| T2 | Test | Automated test passes; code-verified | `partial`, `implemented` |
| T3 | Validated | External or empirical study with documented methodology | `deployed` (for accuracy claims) |

**Tier upgrade rules:**
- T1 → T2: requires passing test suite with named test files as evidence
- T2 → T3: requires external reviewer or empirical study with documented protocol
- Downgrade is automatic when evidence expires or tests fail

---

## 9. Admissibility Framework

### What constitutes valid evidence in TLC governance decisions

An evidence item is admissible when it meets ALL of the following:

1. **Source traceability** — the artifact it derives from is identified with a stable reference (file path, SHA, URL)
2. **Provenance** — the method of extraction or generation is documented
3. **Integrity** — a SHA-256 hash or equivalent immutable identifier exists for the record
4. **Tier labeling** — the evidence tier (T1/T2/T3) is explicitly stated
5. **Freshness** — the evidence is within its revalidation window

### Grounds for inadmissibility

| Ground | Description |
|--------|-------------|
| No source reference | Evidence with no traceable artifact |
| Fabricated provenance | Evidence whose provenance cannot be independently verified |
| Hash mismatch | Evidence whose integrity hash does not match the current record |
| Expired | Evidence past its revalidation window and not re-verified |
| Circular | AI-generated evidence about AI behavior without external anchor |
| Self-adjudicated | Evidence adjudicated by the same person who generated it |

---

## 10. Subsystem Inheritance Model

Every ZSB contract in the Commonwealth inherits from ZSB-TLC-v1.0 as follows:

| What is inherited | How it appears in subsystem contracts |
|-------------------|--------------------------------------|
| P1–P10 principles | Must not be violated; binding without re-statement |
| I1–I6 invariants | Must be maintained; subsystem-specific invariants may be added |
| H1–H6 harm classes | Must be checked; subsystem may add domain-specific harm classes |
| R1–R5 roles | Must be respected; subsystem may narrow but not expand authority |
| T1–T3 evidence tiers | Must be used; no custom tier names |
| SOP library | Must reference applicable SOPs; subsystem may add SOPs |
| SOP-014 gates | All four gates are mandatory for every subsystem release |
| Article V amendment | Any subsystem rule change follows Article V |
| V&T statement | Required on every significant response in every subsystem |

**Conflict resolution:** If a subsystem contract conflicts with TLC, TLC governs. The conflict must be documented in an ADR and the subsystem contract amended.

---

## 11. Commonwealth Registry Requirements

A project is in the Commonwealth when:

1. It has an entry in `config/projects.ts` with:
   - `id` (unique slug)
   - `name` (display name)
   - `domainIds` (at least one from `config/domains.ts`)
   - `status` (one of: `planned`, `prototype`, `partial`, `implemented`, `deployed`)
   - `repoPath` (absolute path or remote URL)
   - `resumeClaim` (truthful single-sentence status, Calibrated Truth Doctrine applies)

2. It has a build contract at one of:
   - `the-living-constitution/projects/[id]/BUILD_CONTRACT.md` (internal)
   - `[project-repo]/docs/prompts/ZERO_SHOT_BUILD_CONTRACT__[NAME].md` (canonical)

3. It has a `docs/truth-status.md` at the project level or an equivalent V&T document.

**Census failure:** A project without all three is ungoverned by TLC regardless of what its code does.

---

## 12. CLAUDE.md Propagation Rules

TLC governance reaches every project via CLAUDE.md files in a cascade:

| Level | File | Content |
|-------|------|---------|
| Global | `~/.claude/CLAUDE.md` | Compact core: Articles I–V summaries, Default User, SOP-013, Communication Law, V&T requirement |
| Governance on demand | `~/.claude/docs/governance/*.md` | Articles VI–VIII full text, SOP-014, doctrine full texts |
| Project | `[project-repo]/CLAUDE.md` | Project-specific: commands, architecture, module map, test layout |
| Subsystem | `the-living-constitution/projects/[id]/CLAUDE.md` | Contract-specific: build contract reference, project invariants |

**Rule:** Every project repo must have a CLAUDE.md that references the TLC governing contract and includes or inherits the V&T statement requirement.

**Authority cascade:** `~/.claude/CLAUDE.md` > `[project]/CLAUDE.md`. Project-level rules may add; they may not subtract from constitutional rules.

---

## 13. SOP Library

Fifteen standard operating procedures govern common governance scenarios.

| SOP | Title | Status |
|-----|-------|--------|
| SOP-001 | New Project Intake | defined |
| SOP-002 | Plan Mode Activation Criteria | defined |
| SOP-003 | Agent Assignment Protocol | defined |
| SOP-004 | Zero-Shot Build Contract Creation | defined |
| SOP-005 | Git Worktree Parallel Execution | defined |
| SOP-006 | SST Triple Gate Execution | defined |
| SOP-007 | ND Cognitive Load Assessment | defined |
| SOP-008 | Multi-Modal Output Generation | defined |
| SOP-009 | Trauma-Aware Content Handling | defined |
| SOP-010 | Constitutional Amendment Process | defined |
| SOP-011 | Eval Harness Run Protocol | defined |
| SOP-012 | Deployment Safety Checklist | defined |
| SOP-013 | Session Recovery (Crisis Protocol) | defined — highest priority |
| SOP-014 | Governance Release Gates | defined — 4-gate checklist |
| SOP-015 | Quarterly ToC&A Impact Review | defined |

**Status of SOP content:** Defined as named procedures. Full procedural text exists for SOP-013 and SOP-014. Remaining SOPs are titled and described; full text is deferred to SOP Library expansion.

---

## 14. Amendment Process (Article V — Formalized)

### Step 1 — Trigger

An amendment is triggered by:
- A user correction that reveals a constitutional gap
- A lessons.md entry documenting a failure
- A three-stakeholder review identifying an essential gap
- A subsystem build surfacing an unresolved conflict

### Step 2 — Observation

Write to `tasks/lessons.md`:

```
Date: [ISO date]
Article/Principle violated or missing: [P1–P10, I1–I6, or gap]
What happened: [plain language]
What the correct rule should be: [proposed language]
Evidence: [test failure, incident, review finding]
```

### Step 3 — Proposal

Format:
> "ADD/MODIFY/REMOVE rule [X] in [Article/SOP] because [evidence], preventing [failure class]"

### Step 4 — Evaluation

The proposed amendment must satisfy:

- [ ] Improves at least one safety domain (D1–D4) without degrading others
- [ ] Does not weaken P1 (Safety Priority) or P3 (Human Dignity)
- [ ] Satisfies Calibrated Truth Doctrine (evidence matches tier)
- [ ] Is neurodivergent-accessible (Article I passes)
- [ ] Does not create a new invariant violation

### Step 5 — Ratification

- Update the relevant governance file
- Commit: `chore: amend constitution — [rule name]`
- Update CHANGELOG.md
- Update truth-status.md if feature status changes

---

## 15. Doctrine Formation Process

A recurring pattern becomes doctrine when:

1. The pattern appears in at least 3 separate incidents or lessons.md entries
2. A principle (P1–P10) does not already cover it
3. The Constitutional Operator ratifies it following Article V

Doctrine names follow the pattern: one word, describes the rule, not the failure.

**Who decides:** Constitutional Operator (R1) with input from available reviews.

**Threshold:** 3 independent confirming instances + Article V ratification.

**Stare decisis:** Ratified doctrines are binding on subsequent decisions. They may be amended but not silently ignored.

---

## 16. Required Artifacts

TLC itself must maintain:

| Artifact | Path | Purpose |
|----------|------|---------|
| This contract | `docs/prompts/ZERO_SHOT_BUILD_CONTRACT__THE_LIVING_CONSTITUTION.md` | Machine-actionable spec |
| Vision document | `THE_LIVING_CONSTITUTION.md` | Plain-language overview |
| Commonwealth registry | `config/projects.ts` | Census — all governed projects |
| Domain definitions | `config/domains.ts` | Four safety domains |
| Amendment log | `tasks/lessons.md` | Article V trigger record |
| Sprint tracker | `tasks/todo.md` | Current work items |
| Verification matrix | `verification/MATRIX.md` | Claim → evidence mapping |
| SOP Library | `docs/sops/` | 15 SOPs (full text, deferred) |
| Governance articles | `00-constitution/` | Article-level specifications |
| Subsystem contracts | `projects/[id]/BUILD_CONTRACT.md` | Per-project governance |

---

## 17. Commonwealth Registry (Current State)

As of 2026-03-27:

| ID | Name | Domains | Status | Contract |
|----|------|---------|--------|----------|
| proactive | PROACTIVE | D1 | implemented | yes |
| sentinelos | SentinelOS | D1–D4 | partial | yes |
| consentchain | ConsentChain | D4 | partial | yes |
| uicare | UICare-System | D2 | partial | yes |
| docen | Docen | D3 | deployed | unknown |
| portfolio | Portfolio | D1–D4 | deployed | unknown |
| instructional-integrity-studio | Instructional Integrity Studio | D3 | partial | yes (ZSB-IIS-v2.0) |
| tlc-evidence-observatory | TLC Evidence Observatory | D1+D4 | prototype | yes (needs critical-review response) |
| buildlattice-guard | BuildLattice Guard | D1–D4 | planned | yes (ZSB-BLG-v2.0) |
| frostbyte-etl | Frostbyte ETL | D4 | partial | no — required |

---

## 18. Acceptance Criteria for TLC

TLC is considered operational when ALL of the following are true:

### Constitutional Content
- [ ] All 10 principles (P1–P10) are enumerated with definitions and violation criteria
- [ ] All 6 invariants (I1–I6) are stated with machine-checkable criteria
- [ ] All 6 harm classes (H1–H6) are enumerated with inclusion/exclusion criteria
- [ ] All 5 governance roles (R1–R5) are defined with can/cannot boundaries
- [ ] All 3 evidence tiers (T1–T3) are defined with upgrade/downgrade rules

### Registry Completeness
- [ ] All active Commonwealth projects are in `config/projects.ts`
- [ ] All active projects have build contracts
- [ ] All active projects have truth-status files
- [ ] No project claims `implemented` without T2 evidence

### Propagation
- [ ] `~/.claude/CLAUDE.md` contains compact Articles I–V
- [ ] Governance articles exist as on-demand files
- [ ] Every active project repo has a CLAUDE.md referencing TLC

### Governance Process
- [ ] Amendment process is documented and has been used at least once
- [ ] Doctrine formation process is defined
- [ ] SOP-013 and SOP-014 full procedural text exists

### Truth
- [ ] This contract's truth-status is honest
- [ ] No forbidden claims are present in any Commonwealth documentation

---

## 19. Forbidden Claims for TLC

TLC must never claim:

- Formal verification of any system
- Provable safety guarantees
- Universal governance of all AI agents
- Production-readiness of any subsystem unless SOP-014 gates pass
- Validated accuracy of any evaluator unless T3 evidence exists
- Complete constitutional coverage of all edge cases

---

## 20. V&T Statement — TLC Current Truth

**Exists (verified):**
- Vision document (`THE_LIVING_CONSTITUTION.md`) — 411 lines
- Commonwealth registry (`config/projects.ts`) — 10 projects as of 2026-03-27
- Four safety domain definitions (`config/domains.ts`)
- 6 subsystem build contracts in `projects/`
- Compact CLAUDE.md at `~/.claude/CLAUDE.md` (refactored 2026-03-26)
- Governance on-demand articles at `~/.claude/docs/governance/`
- This master contract (ZSB-TLC-v1.0) — written 2026-03-27

**Does not exist:**
- Full SOP library procedural text (SOP-001 through SOP-015 are titled; only SOP-013 and SOP-014 have full text)
- Frostbyte ETL build contract (required by I3)
- Docen and Portfolio build contracts (unknown — unverified)
- Full adjudication framework content for Evidence Observatory (three-stakeholder review identified essential gaps A–I)
- Governance audit trail (chain of custody for governance decisions)
- External audit hooks

**Unverified:**
- Whether all propagation rules are actually enforced in CI/CD
- Whether SentinelOS, ConsentChain, and UICare status claims survive T2 scrutiny
- Whether Docen and Portfolio have truth-status files

**Functional status:**
TLC is constitutionally grounded as of 2026-03-27. The master contract (this document) fills the gap identified by the three-stakeholder review: "TLC is architecturally mandated but substantively empty." Constitutional content now exists. Propagation infrastructure exists. Gaps remain in SOP full text, two unknown project contracts, and the governance audit trail. TLC is `partial` — not `implemented`. Article V amendment process has not yet been formally exercised.

---

*This is ZSB-TLC-v1.0. Amendment authority: Constitutional Operator. Next review trigger: any subsystem contract execution, any new project intake, any three-stakeholder review finding.*
