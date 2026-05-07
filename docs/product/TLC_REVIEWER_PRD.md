# TLC Reviewer PRD

**Document type:** Reviewer-facing Product Requirements Document
**Status:** Active
**Canonical path:** docs/product/TLC_REVIEWER_PRD.md

---

## Overview

This PRD summarizes The Living Constitution (TLC) as a reviewer-facing product/research system: a governance and research control plane for AI safety work, not a monolithic application. The repo's own README defines it as housing constitutional specifications, evidence rules, build contracts, verification automation, project overlays, and status truth surfaces for governed work across related repos.

---

## 1. Purpose

**Product purpose:** Create a reusable governance-as-code operating layer for AI projects where claims, build contracts, evidence, verification status, and reviewer handoff artifacts are machine-legible and auditable.

**Research purpose:** Test whether runtime governance artifacts — especially Contract Window-style state visibility, C-RSP build contracts, invariant enforcement, and evidence ledgers — can make long-context AI work more governable, contestable, and truth-bound.

**Reviewer value:** A reviewer should be able to answer four questions quickly:

| Reviewer Question | Repo Surface |
|---|---|
| What is the governing theory? | THE_LIVING_CONSTITUTION.md |
| What exists right now? | STATUS.json / STATUS.md |
| Which projects are governed? | MASTER_PROJECT_INVENTORY.json / .md |
| How are claims verified? | verification/MATRIX.md, verifier scripts, CI workflow |

The repo explicitly warns that STATUS.json is the authoritative current-status artifact and that STATUS.md is only a deterministic mirror.

---

## 2. Core Modules

| Module | Purpose | Current Role |
|---|---|---|
| Constitutional Specification | Defines governing principles, Articles I–V, amendment logic, agent powers, safety/accessibility/code/evidence constraints. | Human-readable governance source in THE_LIVING_CONSTITUTION.md. |
| Operational Base Camp | Defines how agents and project repos inherit TLC controls. | CLAUDE.md identifies this repo as the governance overlay, not the implementation repo. |
| C-RSP Build Contracts | Converts goals into Constitutionally-Regulated Single Pass build contracts. | Master template in projects/c-rsp/BUILD_CONTRACT.md; governs generated instance contracts. |
| Project Inventory | Maps governed projects, overlays, repo paths, anomalies, and verification commands. | MASTER_PROJECT_INVENTORY.json/.md; includes explicit unknowns and anomalies. |
| Verification Layer | Runs topology, governance-chain, institutionalization, cross-repo, and failure-injection checks. | Scripts under scripts/; outputs under verification/. Inventory lists executable checks. |
| Truth Surface | Provides canonical status, truth anchor, review state, and tip-state truth. | STATUS.json declares active status, tip_pending, reviewer pending, and review required. |
| Evidence / Claim Ledger | Maps claims to evidence and exported proofs. | verification/MATRIX.md, evidence ledger schema, governance templates. |
| Runtime / Product Apps | Contract Window, Evidence Observatory, control-plane UI, and downstream apps. | Mostly in sibling repos or submodules; this repo governs them rather than duplicating all implementation. |

---

## 3. Governance-as-Code Model

TLC uses a layered model:

1. **Constitutional Law Layer** — THE_LIVING_CONSTITUTION.md defines Articles, amendment flow, agent powers, and safety/accessibility/code/evidence duties.
2. **Operational Control Layer** — CLAUDE.md tells agents how to operate in the repo: every work item gets a project folder, build contract, verification evidence, and status discipline. It also states that build contracts must be reviewed before building.
3. **Contract Layer** — C-RSP build contracts convert intent into executable constraints. The template requires bootstrap ingestion of the constitutional trinity, paired JSON/Markdown artifacts, verification logs, rationale files, and structural preflight.
4. **Verification Layer** — Scripts check project topology, governance chain, institutionalization, cross-repo consistency, and failure injection. The inventory states these checks exit non-zero on drift between disk and inventory.
5. **Truth Surface Layer** — STATUS.json is the machine truth source. It records verification target, truth anchor, workflow identity, review status, governance contract version, and tip-state truth.
6. **Open Interface / Closed Epistemics Boundary** — The repo's truth boundary says internal status is synthesized from inventory, CI provenance, git HEAD, workflow identity, regression ledger, and remote evidence record; external parties receive exported proofs and schema-valid artifacts only.

---

## 4. APIs / Interfaces

| Interface Type | Surface | Consumer |
|---|---|---|
| Status API | STATUS.json | Reviewers, CI, dashboards, control-plane UI |
| Inventory API | MASTER_PROJECT_INVENTORY.json | Project registry, topology verifiers, portfolio/reviewer surfaces |
| Build Contract API | projects/*/BUILD_CONTRACT.md, C-RSP JSON instances | AI coding agents, Guardian kernel, reviewers |
| Evidence API | verification/*, evidence ledgers, claim matrix | Reviewers, auditors, CI |
| Verifier CLI | python3 scripts/verify_project_topology.py, verify_governance_chain.py, verify_institutionalization.py, verify_cross_repo_consistency.py | Maintainers and CI |
| CI Interface | .github/workflows/verify.yml | GitHub Actions |
| Human Review Interface | README, STATUS.md, inventory markdown, handoff docs | Anthropic/research/product reviewers |
| Runtime App Interfaces | Contract Window, Evidence Observatory, control-plane apps | Users, researchers, internal operators |

---

## 5. Key Milestones

| Milestone | Definition of Done |
|---|---|
| M1 — Reviewer Front Door Stabilized | README, STATUS, inventory, governance map, and reviewer checklist are aligned and link correctly. |
| M2 — Status Truth Surface Hardened | STATUS.json remains canonical; STATUS.md regenerates deterministically; tip-state policy is documented and enforced. |
| M3 — C-RSP Instance Pipeline Validated | C-RSP JSON/Markdown paired artifacts validate against schema; preflight script passes; logs and rationale files are generated. |
| M4 — Verification Matrix Completed | Every public claim maps to evidence, command, artifact path, and status. |
| M5 — Runtime Governance Demo Bound | Contract Window and/or Evidence Observatory demo shows active task contract, assumptions, invariant checks, and evidence capture. |
| M6 — Cross-Repo Governance Audit | Inventory paths, submodules, sibling repos, and project overlays are reconciled; anomalies are either resolved or explicitly retained as unknowns. |
| M7 — Reviewer Package Exported | Create a concise reviewer bundle: README, PRD, STATUS, inventory, verification matrix, run commands, screenshots/demo link, and known limitations. |

---

## 6. Handoff Checklist for Reviewers

### Required Reading Order

1. README.md
2. STATUS.json
3. STATUS.md
4. MASTER_PROJECT_INVENTORY.md
5. THE_LIVING_CONSTITUTION.md
6. CLAUDE.md
7. projects/c-rsp/BUILD_CONTRACT.md
8. verification/MATRIX.md
9. docs/operations/VERIFY.md
10. Relevant downstream project README or build contract

### Required Verification Commands

```bash
pip install -r requirements-verify.txt
python3 scripts/verify_project_topology.py --root .
python3 scripts/verify_project_topology.py --root . --with-governance
python3 scripts/verify_governance_chain.py --root .
python3 scripts/verify_institutionalization.py --root .
python3 scripts/verify_cross_repo_consistency.py --canonical-root . --target-root projects/consentchain
python3 scripts/governance_failure_injection_tests.py
python3 scripts/render_status_surface.py --root .
```

### Reviewer Acceptance Criteria

| Criterion | Pass Condition |
|---|---|
| Status clarity | STATUS.json identifies authoritative state, truth anchor, and review state. |
| Claim traceability | Public claims resolve to evidence paths or are marked unverified. |
| Governance coherence | Constitution, C-RSP contracts, inventory, and verification scripts agree. |
| Repo boundary honesty | TLC is not overstated as the implementation repo when implementations live elsewhere. |
| Reproducibility | A reviewer can run verifier commands from a fresh clone. |
| Failure visibility | Known unknowns and anomalies remain explicit rather than hidden. |
| Handoff quality | Reviewer can determine what exists, what is specified, what is unverified, and what requires review. |

---

## Outcome

This repo should be positioned as a governance control plane and reviewer evidence system for AI safety projects. Its strongest signal is not a single app; it is the combination of:

- constitutional specification,
- C-RSP executable build contracts,
- machine-readable status surfaces,
- project inventory,
- verification scripts,
- evidence ledger discipline,
- explicit unknown/anomaly reporting,
- downstream governance overlays.

The main reviewer risk is scope ambiguity: the repo contains many artifacts, project overlays, and implementation references, but not all downstream product code. The PRD should therefore preserve a strict boundary: TLC governs, verifies, and evidences the system; product implementation may live in sibling repos or submodules.

---

## V&T Statement

- **Exists:** README, STATUS.json, STATUS.md, MASTER_PROJECT_INVENTORY.md, THE_LIVING_CONSTITUTION.md, CLAUDE.md, and projects/c-rsp/BUILD_CONTRACT.md were read from the active public repository or raw GitHub sources.
- **Non-existent / not established here:** I did not verify every downstream sibling repo, every project implementation, or every verifier run result locally.
- **Unverified:** Actual command execution, CI pass/fail state at the current GitHub tip, runtime app behavior, and completeness of verification/MATRIX.md were not independently executed in this session.
- **Functional status:** This PRD is a concise reviewer-facing synthesis based on repo-visible documentation and status files; it is not a full technical audit or executed verification report.
