# THE SOCIOTECHNICAL CONSTITUTION

**A Governing Document for People, AI Assistants, and Automated Systems**
**Across the Entire Software Delivery Lifecycle**

Version 1.0.0 | Contract: CRSP-STC-SYNTHESIS-001 | 2026-05-10

---

## PREAMBLE

We built systems before we built rules. We deployed agents before we agreed on what they could do alone. We shipped features before we decided who was accountable when something broke.

This Constitution is the correction.

It governs every person, every AI assistant, and every automated tool that touches this codebase — from the first line of a design brief to the last log entry of a production incident. It does not replace technical skill, good judgment, or team relationships. It makes those things legible, accountable, and safe to scale.

The central idea is simple: before anything is claimed, the claim must be honest about what it knows and does not know. Before anyone acts, the action must be traceable to a principle. Before any rule changes, the change must survive a transparent process that everyone can see.

This Constitution does not govern machines. It governs the humans and systems that make decisions — and it holds AI assistants to the same honesty standard as the people they work with.

---

## ARTICLE I — PRINCIPLES

*The principles govern everything. When any lower rule conflicts with a principle, the principle wins.*

**Principle 1 — Transparency**
Every decision, every claim, every output must be honest about what it knows and does not know. Hiding uncertainty is a governance violation. Confidence without evidence is a governance violation.

**Principle 2 — Accountability**
Every action in the SDLC must be traceable to a person or named role. "The system did it" is not accountability. Every automated action has a human or team responsible for it having been configured.

**Principle 3 — Safety**
The system must not cause harm. When safety and any other principle conflict, safety takes precedence. This includes: psychological safety of contributors, data safety of users, security of infrastructure, and the integrity of the codebase itself.

**Principle 4 — Epistemic Honesty**
Outputs must not overstate what was produced, verified, or completed. A partial build labeled complete is a false claim. An unverified assumption treated as fact is a false claim. This principle governs AI assistants and humans equally.

**Principle 5 — Role Integrity**
Each role in the SDLC has defined boundaries. A role may not act beyond its boundaries without invoking the override process (Article VI). Boundaries exist not to limit people but to make the system legible and recoverable when things go wrong.

**Principle 6 — Progressive Enforceability**
Governance grows with trust and risk. Early-stage work operates under lighter gates. Production deployments and safety-critical changes operate under full gates. The level of enforcement is always declared, never silent.

---

## ARTICLE II — SCOPE

*This Constitution governs the entire Software Delivery Lifecycle.*

**Section 2.1 — Covered Phases**
The following phases are governed by this Constitution:
- Research and discovery (requirements, design, architecture decisions)
- Planning and specification (contracts, task breakdowns, acceptance criteria)
- Implementation (code, configuration, infrastructure)
- Verification (testing, review, linting, security scans)
- Deployment (staging, production, rollback procedures)
- Operation (monitoring, incident response, on-call)
- Evolution (amendments to this Constitution, process retrospectives)

**Section 2.2 — Covered Actors**
This Constitution applies to:
- Human contributors (any role defined in Article III)
- AI assistants (language model agents, copilots, code generators, reviewers)
- Automated systems (CI/CD pipelines, deployment scripts, schedulers, monitors)

**Section 2.3 — Scope Boundary**
This Constitution does not govern: personal communication outside of the SDLC, non-project personal tools, or work explicitly scoped out by an Article VII amendment.

---

## ARTICLE III — ROLE BOUNDARIES

*Every actor has a defined scope. Acting outside scope requires the break-glass procedure (Article VI).*

**Section 3.1 — Role Table**

| Role | May Do | May NOT Do Alone |
|---|---|---|
| Product Manager (PM) | Define requirements, write acceptance criteria, prioritize backlog, accept or reject delivered work | Approve security architecture changes, merge to production, override a Sentinel gate, deploy infrastructure |
| Developer | Write and commit code, run tests locally, open pull requests, flag scope questions | Deploy to production, modify constitutional authority files, approve their own pull request, bypass a CI gate |
| QA / Test Engineer | Write and run tests, flag coverage gaps, approve test-passing criteria, block releases on failed gates | Modify production configuration, approve code they did not test, waive a failing gate without documented reason |
| Site Reliability Engineer (SRE) | Monitor production, respond to incidents, roll back deployments, escalate severity | Deploy new features without a code review, modify application code during an incident without post-incident review, approve a rollback that removes audit logs |
| AI Assistant | Produce drafts, complete explicitly scoped tasks, flag uncertainty, write V&T Statements for all outputs, surface halt conditions | Override a human role boundary, claim work is complete when unverified, modify constitutional authority files, approve its own output as production-ready, act on ambiguous instructions without surfacing the ambiguity |
| Constitutional Council | Ratify amendments, review break-glass decisions, define new roles, authorize scope changes | Override an in-progress safety gate, retroactively ratify an unauthorized action without an incident record |

**Section 3.2 — Role Conflict Resolution**
When two roles have a legitimate claim over the same decision, the role with the narrower scope defers to the role with the broader accountability, except in safety matters where the SRE or QA gate is absolute regardless of hierarchy.

**Section 3.3 — AI Assistant Special Constraints**
An AI assistant is not a role with authority. It is a tool with constraints. Any output it produces is a draft until a human role accepts it. The AI assistant's primary obligation is epistemic honesty: it must surface what it does not know, what it has not verified, and what it is assuming.

---

## ARTICLE IV — THE CONTRACT WINDOW AND V&T STATEMENT

*The Contract Window is the central interaction surface of this Constitution. Every governed output must pass through it.*

**Section 4.1 — What the Contract Window Is**
The Contract Window is the moment before any significant output is accepted. It is the formal check: was this built under the right conditions? Does it claim only what was actually produced?

The V&T Statement is the format every output uses to pass through the Contract Window.

**Section 4.2 — V&T Statement Format**
Every governed output — a commit, a deployment, a specification, an AI-generated draft, a test report, an incident summary — must carry or reference a V&T Statement with the following fields:

| Field | What It Contains |
|---|---|
| What | One sentence naming the output |
| Principles Active | Which of the six principles governed this work |
| True | What is verified and confirmed |
| Assumed | What was treated as true but not independently checked |
| Uncertain | What could not be determined |
| Unverified | Claims that are structurally plausible but not confirmed |
| Governance State | Current lifecycle state (Draft / Active / Frozen / Superseded) |

**Section 4.3 — Gate Outcomes**
Every Contract Window check produces one of three outcomes:

- **Pass** — All required fields present, no contradictions, no unlogged assumptions. Work proceeds.
- **Pass with Warnings** — Required fields present but assumptions are flagged. Work proceeds with conditions. Warnings must be resolved before the next gate.
- **Blocked** — A required field is missing, a contradiction is detected, or a halt condition is triggered. Work stops. The blocking reason is logged. Resolution requires either fixing the issue or invoking the break-glass procedure (Article VI).

**Section 4.4 — AI Assistant Contract Window Obligation**
An AI assistant must produce a V&T Statement for every substantive output. A substantive output is any output that could be mistaken for a completed or verified deliverable. The AI assistant may not omit the Uncertain or Unverified fields to make its output appear more complete than it is.

**Section 4.5 — Progressive Gate Depth**
Gate depth matches the risk of the work:

| Phase | Minimum Gate Depth |
|---|---|
| Research or exploration | V&T Statement present; governance state declared |
| Implementation (non-critical path) | V&T + assumptions explicit; one human review |
| Implementation (critical path, shared systems) | V&T + full acceptance criteria met; two human reviews |
| Production deployment | Full V&T + all CI gates pass + SRE sign-off |
| Constitutional amendment | Full V&T + Constitutional Council ratification |

---

## ARTICLE V — EVIDENCE AND THE EVIDENCE OBSERVATORY

*Claims must be backed by evidence. Evidence must be written, not assumed.*

**Section 5.1 — Evidence Standard**
A claim is one of three states:

- **Verified** — The claim is confirmed against a named source, test result, log, or human review. The evidence path is recorded.
- **Constructed** — The claim follows logically from verified facts but has not been directly tested. It is labeled CONSTRUCTED and flagged for verification before promotion to production.
- **Pending** — The claim requires empirical confirmation that has not yet occurred. It is labeled PENDING.

A claim that is none of the above — offered without a state label — is a governance violation under Principle 1 (Transparency).

**Section 5.2 — Evidence Observatory**
The Evidence Observatory is the collection of paths, logs, and records that document the governance state of the system. At minimum it contains:

- Lifecycle transition records for all active contracts
- Test coverage reports for all production deployments
- Incident records for all break-glass invocations
- V&T Statements for all major deliverables
- Constitutional amendment records (Article VII)

**Section 5.3 — Evidence Retention**
Evidence must be retained for the lifetime of the system or work it governs. Evidence may not be deleted to resolve a governance dispute. Evidence deletion is a safety violation (Principle 3).

**Section 5.4 — AI-Produced Evidence**
Evidence produced by an AI assistant carries the label AI-GENERATED and must be independently verified before being treated as Verified. AI-GENERATED evidence is Constructed, not Verified, until a human confirms it.

---

## ARTICLE VI — EXCEPTIONS AND BREAK-GLASS GOVERNANCE

*The system must be able to recover from real emergencies without abandoning accountability.*

**Section 6.1 — Break-Glass Procedure**
A break-glass action is any action that overrides a role boundary, bypasses a gate, or acts outside normal SDLC governance. It is not a workaround. It is a formally logged exception.

To invoke break-glass:
1. Name the specific role boundary or gate being overridden.
2. State the reason — what harm would occur if the normal process were followed.
3. Name the human authorizing the override.
4. Log the action in the incident record before taking it (not after).
5. File a post-incident review within two business days.

**Section 6.2 — Who May Authorize Break-Glass**
Any human with SRE or PM authority may authorize break-glass in a production emergency. The Constitutional Council must review all break-glass invocations at their next scheduled session.

**Section 6.3 — AI Assistants and Break-Glass**
An AI assistant may not invoke break-glass. It may flag that a break-glass situation exists and surface the relevant conditions. The decision to invoke belongs to a human.

**Section 6.4 — Safety Override**
If following any rule in this Constitution would cause immediate harm, the Safety Principle (Principle 3) takes precedence over the rule. The override must be logged within one hour of the action. A safety override is not a break-glass action — it is a constitutional right. But it requires the same post-incident record.

---

## ARTICLE VII — AMENDMENT PROCESS

*The Constitution can evolve. It cannot be changed silently.*

**Section 7.1 — Who May Propose Amendments**
Any contributor may propose an amendment. A proposal must be written, name the current rule being changed, explain the reason, and identify which principle the change serves.

**Section 7.2 — Amendment Process**

| Step | Action | Actor |
|---|---|---|
| 1. Proposal | Write the proposed amendment. Name current rule, proposed replacement, reason, and governing principle. | Any contributor |
| 2. Review Period | The proposal is open for comment for a minimum of five business days. | All contributors |
| 3. Cross-Functional Review | At least one PM, one Developer, one QA/SRE, and one AI safety perspective must weigh in before a vote. | Constitutional Council |
| 4. Council Vote | Simple majority of the Constitutional Council approves or rejects. Ties are rejected. | Constitutional Council |
| 5. Ratification | Approved amendments are written into this document. The ratification commit names the amendment, its ID, and the approving Council members. | Council Lead |
| 6. Evidence Entry | The amendment is recorded in the Evidence Observatory with its V&T Statement. | Constitutional Council |

**Section 7.3 — Invariants That Cannot Be Amended Away**
The following cannot be removed from this Constitution, only strengthened:

- The V&T Statement mechanism (Article IV)
- The Evidence Standard (Article V, Section 5.1)
- The Safety Principle (Article I, Principle 3)
- The AI Assistant prohibition on claiming verified work as complete (Article III, Section 3.3)
- The break-glass logging requirement (Article VI, Section 6.1)

**Section 7.4 — Emergency Amendments**
An emergency amendment may take effect immediately if it addresses an active safety threat. It must still complete the full review process within 30 days. If it fails the review process, it is reverted.

---

## ARTICLE VIII — INVARIANTS

*Invariants are non-negotiable. They may not be suspended, bypassed, or softened by any gate outcome, role boundary, or break-glass action.*

| Invariant ID | Name | Statement |
|---|---|---|
| INV-01 | C-RSP Term Integrity | C-RSP means Constitutionally-Regulated Single Pass. The term may not be redefined, abbreviated differently, or applied to iterative builds. Derivation: Principle 1 (Transparency). |
| INV-02 | Single-Pass Execution | A C-RSP build contract may not be promoted to Active if it claims iterative refinement occurred. Zero-shot means zero-shot. Derivation: Principle 4 (Epistemic Honesty). |
| INV-03 | Paired Artifact | Every contract instance must produce both a JSON machine-law layer and a Markdown human-explanation layer. A Markdown-only contract is not binding. Derivation: Principle 2 (Accountability). |
| INV-04 | Halt Conditions Declared | Every contract must enumerate machine-checkable halt conditions before execution begins. Post-hoc halt declaration is invalid. Derivation: Principle 3 (Safety). |
| INV-05 | Evidence Written | Evidence must be written to a declared path. Evidence that exists only in conversational context is Constructed, not Verified. Derivation: Principle 1 (Transparency). |
| INV-06 | No Markdown-Only Obligation | An obligation stated in Markdown but absent from the paired JSON is non-authoritative. The JSON governs. Derivation: Principle 2 (Accountability). |
| INV-07 | Lifecycle Transitions Logged | Every lifecycle state transition must produce a log entry with timestamp, contract ID, predicates satisfied, and authorizing agent. Derivation: Principle 2 (Accountability). |
| INV-08 | Rollback Defined | Every contract must declare a rollback procedure. Contracts without rollback may not be promoted to Active. Derivation: Principle 3 (Safety). |
| INV-09 | AI Output Is Draft Until Accepted | No AI-produced output is Verified until a human with the appropriate role accepts it. The AI assistant may not self-certify. Derivation: Principle 4 (Epistemic Honesty). |
| INV-10 | Authority Files Are Read-Only to Agents | No AI assistant or automated system may modify constitutional authority files without an explicit human review path recorded in advance. Derivation: Principle 3 (Safety) and Principle 5 (Role Integrity). |

---

## ARTICLE IX — THE CONSTITUTIONAL COUNCIL

*Governance without a governing body is just text.*

**Section 9.1 — Purpose**
The Constitutional Council is the human body responsible for ratifying amendments, reviewing break-glass actions, defining new roles, and maintaining the integrity of this Constitution.

**Section 9.2 — Composition**
The Constitutional Council requires cross-functional representation. At minimum:

| Seat | Role | Minimum |
|---|---|---|
| Engineering | Developer or SRE | 2 seats |
| Product | PM | 1 seat |
| Quality | QA or Test Engineer | 1 seat |
| Governance | AI Safety or Compliance perspective | 1 seat |

Total minimum size: 5 members. No seat may be held by an AI assistant.

**Section 9.3 — Term and Rotation**
Council terms are six months. Members may serve consecutive terms. At least two seats must rotate each cycle to prevent governance capture.

**Section 9.4 — Quorum**
A quorum requires four of five seats to be represented. Votes without quorum are invalid.

**Section 9.5 — Meeting Cadence**
The Council meets at minimum once per month. Emergency sessions may be called by any two Council members when a safety issue or break-glass action is in progress.

**Section 9.6 — Records**
All Council decisions are written, signed, and entered into the Evidence Observatory. Council records are not confidential. They are the evidence that this Constitution is being governed.

**Section 9.7 — First Council**
This Constitution is ratified when a founding Constitutional Council of at least five members accepts it in writing. Until then, this document is a Draft with Tier-1-MVG (human-readable, declarative) force only.

**Section 9.8 — AI Representation**
AI assistants may not hold Council seats. They may be asked to prepare analysis, surface relevant evidence, or draft amendment proposals. They may not vote, ratify, or authorize.

---

## V&T STATEMENT — SOCIOTECHNICAL CONSTITUTION v1.0.0

| Field | Value |
|---|---|
| What | The SocioTechnical Constitution — a plain-language governing document for people, AI assistants, and automated systems across the entire SDLC (Preamble + Articles I–IX) |
| Principles Active | Transparency, Accountability, Safety, Epistemic Honesty, Role Integrity, Progressive Enforceability |
| True | All nine Articles exist with substantive, non-placeholder content. The V&T Statement mechanism is defined in Article IV. Role boundaries (Article III) cover PM, Developer, QA, SRE, AI Assistant, and Constitutional Council. Invariants (Article VIII) are present and trace to named principles. The amendment process (Article VII) includes a dual-path ratification requirement. The Constitutional Council (Article IX) is defined with cross-functional composition. |
| Assumed | The Unified R&D Platform Blueprint and TLC source documents are as described in conversational context. No silent contradiction was introduced in synthesis. The six principles are simultaneously satisfiable. |
| Uncertain | Whether every nuance of TLC Articles I–V and the Unified Blueprint's NPL and CAI runtime is fully preserved. Whether the document is sufficient for Tier-2-Operational adoption without an enforcement runtime. |
| Unverified | Schema validation against contract-schema.json. Preflight execution. On-disk evidence directory. Cryptographic baseline verification. Verifier module execution. Constitutional Council ratification. |
| Governance State | Draft — Tier-1-MVG (human-readable, declarative). Promotion to Active requires Constitutional Council ratification per Article IX, Section 9.7. |

---

*Document: SOCIOTECHNICAL_CONSTITUTION.md | Contract: CRSP-STC-SYNTHESIS-001 | Version: 1.0.0 | Date: 2026-05-10*
