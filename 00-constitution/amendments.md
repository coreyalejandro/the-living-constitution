# Amendment Log
## Formal Record of Constitutional Changes

---

## How Amendments Work

The Living Constitution evolves through a structured amendment process defined in Article V. Amendments are not ad hoc edits. They are formal governance changes with evidence, rationale, and traceability.

### Amendment Flow

1. **Trigger** — A user correction, a lesson learned, or a pattern failure detected by an agent.
2. **Observation** — The failure or improvement is documented in `tasks/lessons.md` with the specific article violated or enhanced.
3. **Proposal** — A structured amendment proposal is drafted following the format below.
4. **Evaluation** — The proposal is evaluated against four criteria: does it improve safety, code quality, theory-of-change alignment, or neurodivergent accessibility?
5. **Ratification** — The amendment is applied to the governing CLAUDE.md file(s) and committed with the prefix `chore: amend constitution —`.

### Amendment Proposal Format

```
## Amendment [NUMBER]

**Date:** YYYY-MM-DD
**Trigger:** [What caused this amendment — user correction, lesson learned, failure detected]
**Article affected:** [I, II, III, IV, or V]
**Action:** [ADD | MODIFY | REMOVE]

### Current Rule
[The rule as it exists before the amendment, or "No existing rule" for additions]

### Proposed Change
[The exact text of the new or modified rule]

### Rationale
[Why this change is necessary — what evidence supports it, what failure it prevents]

### Evaluation
- Safety impact: [Positive | Neutral | Negative — with explanation]
- Code quality impact: [Positive | Neutral | Negative — with explanation]
- ToC&A alignment impact: [Positive | Neutral | Negative — with explanation]
- ND accessibility impact: [Positive | Neutral | Negative — with explanation]

### Ratification
- Commit hash: [git commit hash after ratification]
- Files modified: [list of CLAUDE.md files updated]
- Ratified by: [Human name or "Human + Agent collaborative review"]
```

---

## Amendment Registry

### Pre-Constitutional Amendments (Before Formal Tracking)

The Constitution underwent multiple revisions before the amendment log was established. The following are reconstructed from commit history and lesson patterns:

**Amendment P-1: V&T Statement Mandate**
- Date: Pre-formal tracking
- Article affected: I (Bill of Rights)
- Action: ADD
- Summary: Added the V&T Statement as a mandatory output on every turn. This was the first formal enforcement of the Right to Truth.
- Rationale: Without explicit truth-status declarations, agents would present planned features as implemented, violating epistemic safety.

**Amendment P-2: Immutability Doctrine**
- Date: Pre-formal tracking
- Article affected: II (Execution Law)
- Action: ADD
- Summary: Codified the immutability requirement for all code: create new objects, never mutate.
- Rationale: Mutation introduced hidden state that violated the Idempotency Doctrine. Immutable patterns make state transitions explicit and auditable.

**Amendment P-3: Session Recovery Protocol (SOP-013)**
- Date: Pre-formal tracking
- Article affected: I (Bill of Rights)
- Action: ADD
- Summary: Added the Session Recovery Protocol for moments of cognitive overwhelm, executive function crash, or manic episode onset.
- Rationale: Without a formal pause mechanism, agents would continue pushing work during crisis states, violating the Right to Dignity and the Right to Safety.

---

### Formal Amendments

No formal amendments have been ratified since the amendment log was established. The next amendment will be numbered Amendment 1.

---

## Amendment Metrics

| Metric | Value |
|--------|-------|
| Total formal amendments | 0 |
| Pre-formal amendments (reconstructed) | 3 |
| Most amended article | Pending — no formal amendments yet |
| Average time from trigger to ratification | Pending — evidence not yet collected |

---

## V&T Statement
- **Exists:** Amendment log template with proposal format; three pre-formal amendments reconstructed from known constitutional history; amendment registry structure; metrics table
- **Non-existent:** Formal amendments (none ratified yet); automated amendment tracking; CI integration for amendment validation
- **Unverified:** Whether the three pre-formal amendments capture all pre-tracking constitutional changes; exact dates of pre-formal amendments
- **Functional status:** Amendment log template is ready for use — first formal amendment will be numbered Amendment 1
