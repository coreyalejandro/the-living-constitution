# 2026-03-29 — The Blind Man's Test (BMT)
## Doctrine 4 of The Living Constitution
### A Documentation Standard for Absolute Determinism

**Version:** BMT-v1.0
**Author:** Corey Alejandro, Constitutional Operator
**Scope:** All specifications, build contracts, PRDs, CLAUDE.md files, SOPs, and technical documentation across the Safety Systems Design Commonwealth
**Authority:** THE_LIVING_CONSTITUTION.md — ratified under Article V

---

## 1. The Premise

All technical specifications must be written so that a blind person could successfully build the project independently if the specification were read out loud to them.

This is not a metaphor. This is not aspirational. This is a pass/fail standard.

The specification — whether it is a build contract, a PRD, a CLAUDE.md, or an SOP — must be so deterministic, so unambiguous, and so exceptionally descriptive that a person who cannot see the screen, cannot see the codebase, cannot see the file tree, and cannot see prior outputs can execute the task to completion by listening to the document read aloud, one section at a time, and following its instructions sequentially.

---

## 2. Why This Standard Exists

Three reasons. All of them are load-bearing.

**Reason 1: Neurodivergent-first governance.** The Living Constitution's default user has ADHD, OCD, autism, and bipolar I. This user cannot rely on "you'll figure it out" or "see the existing code for reference." If the spec requires the reader to hold unstated context in working memory, it fails the default user. BMT eliminates implicit context.

**Reason 2: Agentic execution.** Claude Code agents, subagents, and automated builders execute C-RSP build contracts (Contractually-Restrained Single-Pass builds) as deterministic instructions. An agent has no prior context beyond what the contract provides. If the contract is ambiguous, the agent will guess. Guessing is a constitutional violation (P2 — Epistemic Integrity). BMT makes guessing unnecessary.

**Reason 3: The Census Doctrine demands it.** You cannot govern what you have not described. A specification that relies on "obvious" context or "standard practice" has ungoverned gaps. Those gaps are where phantom completion (F2), instruction drift (F3), and confident false claims (F1) originate. BMT closes the gaps.

---

## 3. The Five BMT Requirements

A document passes the Blind Man's Test when ALL FIVE of the following are true.

### BMT-1: Sequential Completeness

The document can be executed from top to bottom without skipping ahead, referring back, or consulting external documents not explicitly referenced by name and path.

**Passes:** "Create a file at `/src/lib/validator.ts`. This file exports a single function named `validateClaim` that accepts one argument: `claim` of type `string`. The function returns an object with two fields: `valid` (boolean) and `reason` (string). When the claim string contains any of the words 'definitely', 'certainly', or 'absolutely' without a preceding hedge word ('might', 'possibly', 'appears'), return `{ valid: false, reason: 'Unhedged certainty language detected' }`. Otherwise return `{ valid: true, reason: 'No certainty violations found' }`."

**Fails:** "Create the validator. It should work like the one in PROACTIVE."

### BMT-2: Named Concreteness

Every reference to a file, function, variable, endpoint, schema field, directory, dependency, configuration value, or external system uses its exact name. No pronouns for technical artifacts. No "the usual structure." No "as discussed."

**Passes:** "Install the `jsonschema` Python package version 4.21.0 or later using `pip install jsonschema>=4.21.0`."

**Fails:** "Install the validation library."

### BMT-3: Decision Elimination

The document makes every design decision for the reader. The reader never needs to choose between approaches, pick a name, select a library, decide on a pattern, or determine the order of operations. If a decision point exists, the document states the decision and its rationale.

**Passes:** "Use SHA-256 for all file hashing. Not MD5 (collision-vulnerable). Not SHA-512 (unnecessary overhead for integrity checking). SHA-256 provides 256-bit collision resistance, which is sufficient for forensic deduplication."

**Fails:** "Hash the files using a secure algorithm."

### BMT-4: State Explicitness

The document states what exists before each step begins. It never assumes the reader knows what the current state of the system is. Before giving an instruction, it describes what should be true at that point. After the instruction, it describes what should now be true.

**Passes:** "At this point, the directory `/raw/chatgpt/` should exist and contain at least one file named by its SHA-256 hash. The file `processed/ingestion_index.jsonl` should exist and contain at least one JSON line with the fields `artifact_id`, `sha256`, and `source`. If either of these conditions is not true, Layer 0 did not complete successfully — stop and debug before proceeding."

**Fails:** "Now run Layer 1."

### BMT-5: Failure Path Coverage

The document describes what happens when things go wrong — not just what happens when things go right. Every instruction that can fail includes: what failure looks like, what to do when it fails, and whether to stop or continue.

**Passes:** "Run `python -m pytest tests/ -v`. Expected output: all tests pass with exit code 0. If any test fails, the test name and failure reason will appear in the output. Do not proceed to the next layer. Fix the failing test first. Common failures: (a) `ModuleNotFoundError: jsonschema` means the dependency is not installed — run `pip install jsonschema>=4.21.0`. (b) `FileNotFoundError: schemas/ingestion_index.schema.json` means the schemas directory was not populated — go back to the schema creation step."

**Fails:** "Run the tests. They should pass."

---

## 4. The BMT Evaluation Rubric

Every document subject to BMT is evaluated against the five requirements. Scoring is binary per requirement — pass or fail.

| Requirement | Question the evaluator asks | Pass | Fail |
|-------------|---------------------------|------|------|
| BMT-1 Sequential Completeness | Can I execute this top-to-bottom without jumping around? | Yes — every step follows from the previous one | No — I had to skip ahead or refer back to understand a step |
| BMT-2 Named Concreteness | Does every technical reference use its exact name? | Yes — files, functions, variables, paths are all named | No — at least one reference uses "it", "the component", "as before" |
| BMT-3 Decision Elimination | Does the document make every choice for me? | Yes — I never had to decide anything | No — I encountered at least one open question |
| BMT-4 State Explicitness | Does the document tell me what should be true before and after each step? | Yes — preconditions and postconditions are stated | No — at least one step assumes I know the current state |
| BMT-5 Failure Path Coverage | Does the document tell me what to do when things fail? | Yes — failure modes are described with recovery steps | No — at least one instruction has no failure guidance |

**Passing score:** 5 of 5. There is no partial pass. A document that fails any single requirement does not pass BMT.

---

## 5. What BMT Applies To

| Document Type | BMT Required | Rationale |
|---------------|-------------|-----------|
| C-RSP Build Contracts (C-RSP-*) | Yes — mandatory | These are executed by agents with zero prior context |
| CLAUDE.md files (project-level) | Yes — mandatory | These govern agent behavior in every session |
| SOPs (SOP-001 through SOP-015) | Yes — mandatory | These are executed during high-stress or crisis moments (SOP-013) |
| Research methodology docs | Yes — mandatory | These govern reproducibility claims |
| API endpoint specifications | Yes — mandatory | These are consumed by frontend developers and integration partners |
| README files | No — exempt | READMEs are summaries, not execution specs |
| Amendment proposals | No — exempt | These are reviewed by the Constitutional Operator, not executed blind |
| Lessons.md entries | No — exempt | These are observational records, not instructions |
| V&T Statements | No — exempt | These are status declarations, not execution specs |

---

## 6. BMT Violation Detection

The following patterns in a document are automatic BMT failures:

| Pattern | Violates | Example |
|---------|----------|---------|
| "See [other doc] for details" without quoting the relevant content inline | BMT-1 | "See the PROACTIVE README for the validator config" |
| Pronoun referring to a technical artifact | BMT-2 | "Import it into the main file" |
| "Use an appropriate [X]" | BMT-3 | "Use an appropriate data structure" |
| "At this point you should have [X]" without verifiable check | BMT-4 | "At this point the database should be seeded" (how do I verify?) |
| "Run [command]" with no expected output or failure guidance | BMT-5 | "Run `npm install`" |
| "Standard [X]" or "typical [X]" | BMT-3 | "Use the standard project structure" |
| "As discussed" or "as mentioned" | BMT-1 | "As mentioned in our earlier session" |
| "Obviously" or "clearly" or "simply" | BMT-3 | "Simply wire up the API routes" |

---

## 7. How BMT Relates to Existing TLC Doctrines

BMT operationalizes all three existing doctrines at the documentation level:

| Doctrine | How BMT enforces it |
|----------|-------------------|
| Idempotency (Doctrine 1) | A BMT-compliant spec produces the same output regardless of who reads it or when. The document is the fixed point. |
| Calibrated Truth (Doctrine 2) | BMT-3 (Decision Elimination) prevents status inflation by requiring explicit statements of what exists vs. what is planned. BMT-4 (State Explicitness) forces pre/post conditions that are verifiable. |
| Census (Doctrine 3) | BMT-2 (Named Concreteness) requires every artifact to be named. Unnamed = uncounted = ungoverned. |

BMT is proposed as **Doctrine 4 — Deterministic Specification.** It joins the three existing doctrines as a cross-cutting principle that applies everywhere.

---

## 8. Constitutional Integration

### Amendment Proposal (Article V)

**Action:** ADD Doctrine 4 (Deterministic Specification / Blind Man's Test) to THE_LIVING_CONSTITUTION.md

**Because:** Documentation sprawl with 88 markdown files, multiple sources of truth, and implicit-context-dependent specs has caused phantom completion (F2) and instruction drift (F3) in agent execution. BMT eliminates the root cause: ambiguous specifications.

**Evidence:** The 88-file audit of the TLC base camp repo (2026-03-29). Build contracts that reference "see existing code" or "standard structure" without defining either. Agent sessions that produced divergent outputs from the same contract due to ambiguity.

**Preventing:** F1 (Confident False Claims from ambiguous specs), F2 (Phantom Completion from underspecified acceptance criteria), F3 (Instruction Drift from implicit assumptions).

### New Principle

**P11 — Deterministic Specification (Blind Man's Test)**

All technical specifications, build contracts, SOPs, and CLAUDE.md files must pass the Blind Man's Test: a blind person could successfully complete the specified task independently if the document were read out loud to them. Five requirements (BMT-1 through BMT-5) must all pass. There is no partial compliance.

**Violation:** Any specification that requires the reader to guess, assume, remember unstated context, consult unquoted external documents, or make design decisions not stated in the document.

**Evidence requirement:** Tier 1 (convention) — human review against BMT rubric. Tier 2 (target) — automated pattern matching for BMT violation patterns listed in Section 6.

### New Invariant

**I7 — Specification Determinism**

No build session may begin from a specification that has not been evaluated against BMT-1 through BMT-5.

**Check:** Every `BUILD_CONTRACT.md` and `CLAUDE.md` includes a BMT evaluation stamp: `BMT: PASS | [date] | [evaluator]` or `BMT: FAIL | [violations]`.

---

## 9. V&T Statement

**Exists:** Complete Blind Man's Test standard with premise, 5 requirements (BMT-1 through BMT-5), binary evaluation rubric, scope table, violation detection patterns, constitutional integration proposal (P11, I7), and relationship to existing Doctrines 1-3.

**Non-existent:** Automated BMT checker (Tier 2). BMT evaluation stamps on existing build contracts (all 11 contracts need evaluation). Formal Article V ratification by Constitutional Operator.

**Unverified:** Whether the 5 BMT requirements are sufficient to cover all ambiguity modes observed in Commonwealth documentation. Whether additional violation patterns exist beyond the 8 listed.

**Functional status:** BMT is fully specified and ready for ratification. It has not yet been applied to any existing document. First application should be the TLC master contract (C-RSP-TLC-v1.0) as a reference implementation.
