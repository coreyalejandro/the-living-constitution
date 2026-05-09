# TLC and CGL: Governance Infrastructure vs. Research Substrate

## The One-Sentence Boundary Rule

TLC governs the arc. CGL runs the experiment.

---

## Why This Boundary Exists

Two repos. One research program. They do different things.

Collapsing them causes a specific failure: TLC starts looking like the research contribution,
and Anthropic reviewers evaluate the governance framework when they should be evaluating the
empirical research program.

Keeping them distinct causes a different problem if the connection is not explicit: reviewers
see two repos that appear unrelated, and miss the argument that the governance infrastructure
is itself evidence that the research is buildable and auditable.

This document makes the connection explicit and the boundary exact.

---

## The Living Constitution (this repo): Runtime Governance Enforcement Layer

What TLC contains:
- THE_LIVING_CONSTITUTION.md — the constitutional specification (Articles I-V)
- Guardian Kernel — MCP safety enforcement server intercepting every agent tool call
- SentinelOS — TypeScript invariant enforcement platform (I1-I6 at API boundaries)
- Evidence Observatory — 8-layer evidence chain (raw interaction -> governed evidence)
- BID harness — Backwards Instructional Design experiment structure
- Constitutional evaluators — policy-gated evaluation scripts
- Agent Republic — six-role agent system with separation of powers
- STATUS.json / MASTER_PROJECT_INVENTORY.json — truth surfaces
- C-RSP build contracts — governance-as-code for each product domain

What TLC is NOT:
- The research contribution (that lives in CGL)
- The experimental instrument (Contract Window implementation lives in CGL)
- The publication target (papers come from CGL)
- The product roadmap (ConstitutionKit SDK / BehaviorScope / MonoAgent are CGL products)

What TLC proves to Anthropic:
The Contract Window intervention is BUILDABLE and GOVERNED, not theoretical.
TLC is the evidence that the research program has enforcement infrastructure behind it.

---

## cognitive-governance-lab (CGL): Research Substrate

What CGL contains:
- Contract Window (9/9 tests passing)
- BicameralReview engine (kappa 0.762 on synthetic pilot)
- InsightAtrophyIndex (operational, empirical calibration Month 1)
- SessionRecorder (29/29 tests passing)
- 62/62 tests passing total (as of 2026-04-29)
- Three research proposals (I: ConstitutionKit, II: BehaviorScope, III: MonoAgent)
- Pilot datasets (PILOT-S001 through PILOT-S010)
- Artifacts / case law

What CGL is NOT:
- The enforcement layer (that's TLC)
- The constitutional authority (articles, invariants, truth surfaces live in TLC)
- A standalone safety product (it's a research harness governed by TLC)

What CGL proves to Anthropic:
The research program is live, instrumented, and already running.
Not a proposal about what we intend to build — a running program with passing tests.

---

## The Dependency Arrow

cognitive-governance-lab --> the-living-constitution

CGL depends on TLC's constitutional framework.
TLC does not depend on CGL — it precedes it.

The research tests whether the governance intervention (defined in TLC) produces measurable
improvements in human-AI investigative integrity (measured in CGL).

---

## How to Present This to Anthropic

LEAD WITH: CGL — the research, the hypotheses, the infrastructure, the pilot
INTRODUCE TLC AS: the enforcement layer that makes the research auditable and governed

Do NOT say: "I built TLC and it's a research contribution"
DO say: "The Contract Window research is governed by TLC's enforcement infrastructure,
         which means the experiment produces evidence that is verifiable, auditable,
         and reproducible — not just a self-reported result"

That framing makes TLC a *research argument* (your governance infrastructure is unusual
and valuable) without confusing it with the research *contribution* (the CGL experiment).

---

## The Refactor Alignment Note

The TLC-RDI-MVP-001 refactor contract (filed 2026-04-30) must respect this boundary.

The refactor:
- MAY add research workbench UI for VIEWING CGL outputs and evidence
- MAY add eval runner for RUNNING constitutional compliance checks on TLC itself
- MAY add governance surfaces that VALIDATE CGL's methodology against constitutional rules
- MUST NOT move governance-kernel, experiment harness, or proposal content from CGL into TLC
- MUST NOT create a tlc-research-kernel that duplicates CGL's governance-kernel
- MUST NOT blur the enforcement/research boundary in any STATUS surface

The test: after the refactor, a reviewer should still be able to say
"TLC governs, CGL experiments" without confusion.

---

V&T: TLC-CGL-BOUNDARY.md
EXISTS: This document, written 2026-04-30
VERIFIED AGAINST: Both repos (TLC file structure, CGL 62/62 tests), THREE_PROPOSALS_MASTER.md,
  RESEARCH_STORY_MASTER.md, repo-relationship-map.md (updated with CGL entry)
NOT CLAIMED: This document does not resolve the tip_pending state in TLC STATUS.json —
  that requires separate verification pass before executing refactor
FUNCTIONAL STATUS: Boundary document complete. Authoritative for both repos.
