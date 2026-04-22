# CLAUDE.md — The Living Constitution Base Camp

## What This Repo Is

This is the **governance overlay** for the Safety Systems Design Commonwealth. It is NOT a code repository. It is the operational hub that:
- Holds the constitutional specification (`THE_LIVING_CONSTITUTION.md`)
- Manages zero-shot build contracts for every project in the Commonwealth
- Tracks verification evidence for every resume/application claim
- Coordinates sprint execution across all project repos

## Repo Structure

```
the-living-constitution/
  THE_LIVING_CONSTITUTION.md    <- The specification (source of truth)
  CLAUDE.md                     <- This file (operational controls)
  projects/consentchain-pack/core/              <- ConsentChain constitutional pack (docs/spec; not app source)
  tasks/
    todo.md                     <- Sprint tracker
    lessons.md                  <- Amendment log (feeds Article V)
  projects/
    teaser-video/               <- Video deliverable
    sentinelos/                 <- SentinelOS build contract
    proactive/                  <- PROACTIVE build contract
    consentchain/               <- ConsentChain implementation (git submodule)
    consent-gateway-auth0/      <- Consent Gateway Auth0 (git submodule)
    buildlattice/               <- BuildLattice Guard governance overlay (implementation: see BUILD_CONTRACT Repo Path)
    uicare/                     <- UICare build contract
  verification/
    MATRIX.md                   <- Every claim -> evidence mapping
    *.md                        <- Per-project V&T statements
  config/
    projects.ts                 <- Domain mapping (4 safety domains)
    domains.ts                  <- Domain definitions
```

## Rules

1. **Every work item gets its own folder** under `projects/` with:
   - `CLAUDE.md` (inherits Living Constitution controls + project-specific rules)
   - `BUILD_CONTRACT.md` (zero-shot build contract: machine-actionable spec)

2. **No building until the build contract is reviewed.** The contract IS the spec. Write it right, build it once.

3. **Build contracts point to external repos.** This base camp does NOT duplicate code. Each `projects/<name>/BUILD_CONTRACT.md` references the actual repo path where implementation lives.

**C-RSP classification:** Root `projects/<name>/BUILD_CONTRACT*.md` files are **executed instances** or resume-aligned overlays for that scope. They are **not** the C-RSP **canonical master template** (`projects/c-rsp/BUILD_CONTRACT.md`) and must not be mistaken for reusable global templates. Optional executed instances stored under `projects/c-rsp/BUILD_CONTRACTS/` follow the same **executed instance** role (see `projects/c-rsp/CANONICAL_ROLE_MAP.md`).

4. **Verification is mandatory.** Every claim in the resume/cover letter must have a corresponding entry in `verification/MATRIX.md` with evidence.

5. **The Living Constitution governs all work.** Articles I-V apply to every project folder, every build contract, every commit.

## Cursor and assistant report format (TLC-wide)

- **Mandatory shape for AI replies in this repo:** `.cursor/rules/tlc-universal-response-format.mdc` (Kanban table, body, Verification & Truth block, then exactly three ranked next steps as the **last** section). Opt-out only if the user sends `FORMAT: FREE` for that turn.
- **Required GitHub status checks (configure in repo Settings):** `.github/BRANCH_PROTECTION.md`

## Project Registry

| Project | Domain | Repo Path | Status |
|---------|--------|-----------|--------|
| PROACTIVE | Epistemic Safety | `/Users/coreyalejandro/Projects/proactive-gitlab-agent` | Validated — 212/212 tests, submitted to GitLab hackathon |
| SentinelOS | All 4 Domains | `/Users/coreyalejandro/Projects/sentinelos` | Partial — 9 packages, 1,037 LOC, hex arch |
| MADMall-Production | Human/Cognitive/Empirical | `/Users/coreyalejandro/Projects/MADMall-Production` | Partial — infrastructure mature, features Phase 1/4 |
| ConsentChain | Empirical Safety | `/Users/coreyalejandro/Projects/the-living-constitution/projects/consentchain` (path semantics: `projects/consentchain-pack/core/REGISTRY_PATH_MIGRATION.md`) | Partial |
| UICare-System | Human Safety | `/Users/coreyalejandro/Projects/uicare-system` | Partial |
| Docen | Cognitive Safety | `/Users/coreyalejandro/Projects/docen` | Deployed on GCR |
| Portfolio | All 4 Domains | `/Users/coreyalejandro/Projects/coreys-agentic-portfolio` | Live on Vercel |
| TLC Evidence Observatory | Epistemic/Empirical Safety | `/Users/coreyalejandro/Projects/tlc-evidence-observatory` | Building — zero-shot contract executing |

## C-RSP template system (semantic authority order)

TLC uses **Constitutionally-Regulated Single Pass** (C-RSP) contracts for governed execution. **Authority order is strict** (lower rows do not override higher rows). **How to use the folder (read this first):** `projects/c-rsp/README.md`. Full map: `projects/c-rsp/CANONICAL_ROLE_MAP.md`.

| Order | Artifact | Path |
|------:|----------|------|
| 1 | **Canonical master template** | `projects/c-rsp/BUILD_CONTRACT.md` |
| 2 | **Guided instance template** (subordinate to 1) | `projects/c-rsp/BUILD_CONTRACT.instance.md` |
| 3 | **Schema artifact** | `projects/c-rsp/contract-schema.json` |
| 4 | **Outcome artifact** (V&T report shape) | `projects/c-rsp/CRSP_OUTCOME_TEMPLATE.md` |
| 5 | **Workflow / profile helpers** (helpers only; not truth surfaces) | `projects/c-rsp/workflows/*` **and** (same band) `projects/c-rsp/INSTANCE_PROCESS.md`, `projects/c-rsp/PASS8_TEMPLATE.md`, `projects/c-rsp/BUILD_CONTRACT.instance.example.md`, `projects/c-rsp/BUILD_CONTRACT.instance.template.md` |
| 6 | **Executed project contracts** (instances, not reusable templates) | `projects/*/BUILD_CONTRACT*`, `projects/c-rsp/instances/*.md`, `projects/c-rsp/BUILD_CONTRACTS/*.md`, etc. |

**FDE control plane (example executed instance):** `projects/c-rsp/instances/CRSP-FDE-CTRL-PLANE-GAPS-002.md`. **Verification bundle:** `./scripts/run_fde_control_plane_verification.sh`.

## Zero-Shot Build Contract Format (project overlays)

Many `projects/<name>/BUILD_CONTRACT.md` overlays also follow this **resume-aligned** zero-shot shape (distinct from the C-RSP master template):

```markdown
# Build Contract: [Project Name]

## Current State (Honest)
[What actually exists right now — verified, not assumed]

## Target State (What Resume Claims)
[Exact claims from resume/cover letter]

## Acceptance Criteria
[What "done" looks like — measurable, verifiable]

## Evidence Required
[How to prove each claim — commands to run, files to check]

## Implementation Spec
[Machine-actionable build instructions — zero ambiguity]

## Repo Path
[Where the actual code lives]
```

## Sprint Context

- **Application:** Anthropic Safety Fellows Program (July 2026 cohort)
- **Deadline:** Monday March 23, 2026 at 7:00 AM
- **Success criteria:** Every resume claim truthful at stated status level, backed by evidence
