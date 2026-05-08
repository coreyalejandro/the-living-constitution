# Reviewer Guide — The Living Constitution

**Document type:** Reviewer Routing Guide
**System:** The Living Constitution (TLC)
**Contract:** CRSP-TLC-TWO-PATHS-REFACTOR-001

---

## How to use this guide

Find the row that matches your reviewer role. Follow the path listed. Start with the truth surface listed for your role before reading anything else.

---

## Reviewer routing table

| Reviewer role | Start here | Then go to | Truth surface to check first |
|--------------|-----------|-----------|------------------------------|
| Research Reviewer | docs/research/RESEARCH_PATH.md | PROPOSAL.md, research/evidence-ledger.md | STATUS.md — Unverified section |
| Software Engineer | docs/build/BUILD_PATH.md | apps/, projects/c-rsp/, scripts/ | STATUS.json — functional status |
| Product Evaluator | docs/front-door/TWO_REVIEWER_PATHS.md | docs/build/BUILD_PATH.md, docs/product/TLC_REVIEWER_PRD.md | STATUS.md — Exists section |
| Safety/Governance Reviewer | THE_LIVING_CONSTITUTION.md | docs/governance/RUNTIME_INVARIANTS_INDEX.md, projects/c-rsp/ | STATUS.md — all four sections |
| Skeptic | This guide, section: Pattern vs. Signal | verification/, evidence/, research/evidence-ledger.md | verification/CRSP-TLC-TWO-PATHS-REFACTOR-001/outcome.md |
| General / Unknown | docs/front-door/TWO_REVIEWER_PATHS.md | Choose Research or Build path from there | STATUS.md |

---

## Research Reviewer

**You are here to evaluate TLC as an AI safety research contribution.**

What to look for:
- Are the hypotheses (H1, H2, H3) falsifiable?
- Is the Contract Window mechanistically distinct from plain UI display?
- Is the validation plan adequate for the claims?
- Is the structural-vs-attentional confound addressed?
- Is the inter-rater reliability study adequate?

Start at [docs/research/RESEARCH_PATH.md](../research/RESEARCH_PATH.md).

Read PROPOSAL.md for the full argument.

Read research/evidence-ledger.md for the honest status of every claim.

Check the Unverified section of STATUS.md. Every item there is something the researcher has not yet proven. A short list of unverified items is a signal of honesty. A missing Unverified section is a red flag.

Do not confuse the governance infrastructure (TLC) with the research contribution (cognitive-governance-lab). They are separate. The research question is tested in CGL. TLC provides the enforcement infrastructure that makes the research auditable. See research/TLC-CGL-BOUNDARY.md.

---

## Software Engineer

**You are here to evaluate whether TLC actually runs.**

What to look for:
- Does the code exist at the claimed paths?
- Do the tests pass?
- Does the build succeed?
- Are the claimed invariants actually enforced in code?

Start at [docs/build/BUILD_PATH.md](../build/BUILD_PATH.md).

Run scripts/verify_crsp_template_bundle.sh. If it fails, that is evidence, not a surprise.

Inspect apps/contract-window/ and apps/evidence-observatory/ directly. Read the source. Do not trust documentation of code — read the code.

Check research/evidence-ledger.md entries S1-S6 for the honest implementation status of SentinelOS. Partial means partial. Not all invariants are fully enforced.

Check STATUS.json for the machine-readable operational status.

---

## Product Evaluator

**You are here to evaluate TLC as a product or prototype.**

What to look for:
- What does the system actually do for a user?
- Is the Contract Window usable?
- Does the governance make the system more trustworthy or more annoying?
- What user populations benefit?

Start at [docs/front-door/TWO_REVIEWER_PATHS.md](TWO_REVIEWER_PATHS.md).

Read docs/product/TLC_REVIEWER_PRD.md for the product-focused overview.

Read docs/build/BUILD_PATH.md for what runs and what does not.

The Default User Doctrine matters here: TLC is designed for the most vulnerable user first, not the median user. If your evaluation assumes a median technical user, you are evaluating the wrong target population.

TLC is prototype-grade. It is not a shippable product. Evaluate it as a research prototype.

---

## Safety/Governance Reviewer

**You are here to evaluate whether TLC's governance structure actually governs.**

What to look for:
- Do the constitutional articles encode real constraints?
- Are the C-RSP contracts machine-enforceable?
- Do the halt conditions actually halt?
- Is the separation of powers real or nominal?

Start at THE_LIVING_CONSTITUTION.md. Read the actual constitutional text.

Read docs/governance/RUNTIME_INVARIANTS_INDEX.md for the invariant scaffold.

Read projects/c-rsp/BUILD_CONTRACT.md for the master contract structure.

Inspect a live C-RSP contract in projects/c-rsp/instances/ and check whether the halt_matrix conditions are programmatically enforced or just documented.

Read verification/ for evidence that contracts have been executed. Empty evidence directories are a signal.

Check the STATUS.md Functional Status section. Prototype-grade means constraints are defined and partially enforced — not that all halt conditions will fire in all cases.

---

## Skeptic

**You are here because you do not believe the claims hold up.**

This is the right posture. Here is how to test it.

**Check the Pattern vs. Signal problem first.** See that section below.

Evidence you can verify directly:
1. git clone the repo and run scripts/verify_crsp_template_bundle.sh. Does it pass?
2. Read research/evidence-ledger.md. Count the Proven, Partial, Pending, Broken entries. Is the Broken count zero? If so, why?
3. Read the Unverified section of STATUS.md. Are the unverified items plausible given the system's age?
4. Read verification/CRSP-TLC-TWO-PATHS-REFACTOR-001/outcome.md. Does the predicate evidence match the claims in the docs?
5. Read one complete C-RSP contract (projects/c-rsp/instances/CRSP-TLC-TWO-PATHS-REFACTOR-001.md). Does the halt matrix describe halt conditions that are actually enforced in code, or only documented?

Evidence you cannot verify from docs alone:
- Whether H1-H3 hold in powered studies (no studies run)
- Whether the Contract Window effect is structural or attentional (confound unresolved)
- Whether the Evidence Observatory pipeline produces reliable evidence (full audit not done)

The system acknowledges these gaps. If you find gaps it does not acknowledge, that is significant.

---

## Pattern vs. Signal

This section addresses the most common failure mode in evaluating AI governance research: confusing a coherent pattern with an empirical signal.

**The pattern failure:** A system with consistent terminology, comprehensive documentation, and well-structured artifacts looks more valid than a system with incomplete documentation and less organized artifacts. But documentation quality is not evidence quality. A well-structured validation plan is not evidence that validation was done.

**How TLC tries to prevent this failure:**
- STATUS.md maintains four explicit categories: Exists, Not claimed, Unverified, Functional status
- research/evidence-ledger.md distinguishes Proven, Partial, Pending, Broken
- Validation plan scaffolds include explicit UNRESOLVED REQUIRED INPUT markers
- This reviewer guide exists to route reviewers to evidence, not documentation

**How to apply this to your review:**
- Every claim should route to evidence, not to more documentation
- "The validation plan exists" is not evidence that validation was done
- "62/62 tests passing" is evidence — if you can run the tests yourself
- "Kappa 0.762 on synthetic data" is evidence with a scope qualifier — synthetic, not real
- "H1 predicts [X]" is a hypothesis, not a result

The Living Constitution is a prototype and a research program. It is not a proven intervention. The value of the pattern is that it is honest enough to tell you exactly which parts are proven and which are not. Evaluate the honesty of the status reporting, not just the status itself.

---

## Truth surface locations

| Surface | What it tells you | Authority level |
|---------|-----------------|----------------|
| STATUS.md | Human-readable current state | Secondary |
| STATUS.json | Machine-readable authoritative state | Primary |
| research/evidence-ledger.md | Every claim with honest status | Research record |
| verification/CRSP-TLC-TWO-PATHS-REFACTOR-001/outcome.md | This contract's execution evidence | Contract record |
| verification/CRSP-TLC-TWO-PATHS-REFACTOR-001/predicate-results.jsonl | Machine-readable predicate outcomes | Contract evidence |

---

> Contract: CRSP-TLC-TWO-PATHS-REFACTOR-001
> Truth surface: STATUS.md, verification/CRSP-TLC-TWO-PATHS-REFACTOR-001/outcome.md
