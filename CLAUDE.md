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
  04-consentchain/              <- ConsentChain constitutional pack (docs/spec; not app source)
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
| ConsentChain | Empirical Safety | `/Users/coreyalejandro/Projects/the-living-constitution/projects/consentchain` (path semantics: `04-consentchain/REGISTRY_PATH_MIGRATION.md`) | Partial |
| UICare-System | Human Safety | `/Users/coreyalejandro/Projects/uicare-system` | Partial |
| Docen | Cognitive Safety | `/Users/coreyalejandro/Projects/docen` | Deployed on GCR |
| Portfolio | All 4 Domains | `/Users/coreyalejandro/Projects/coreys-agentic-portfolio` | Live on Vercel |
| TLC Evidence Observatory | Epistemic/Empirical Safety | `/Users/coreyalejandro/Projects/tlc-evidence-observatory` | Building — zero-shot contract executing |

## C-RSP template system (canonical hierarchy)

TLC uses **Constitutionally-Regulated Single Pass** (C-RSP) contracts for governed execution. Do not confuse these roles:

| Role | Path | Purpose |
|------|------|---------|
| **Canonical master template** | `projects/c-rsp/BUILD_CONTRACT.md` | Reusable section order, invariants, Blind Man execution requirements (§6), and output rules. |
| **Guided instance template** | `projects/c-rsp/BUILD_CONTRACT.instance.md` | Prompt skeleton with `{placeholders}` — **workflow artifact only**; not an executed contract. |
| **Outcome report shape** | `projects/c-rsp/CRSP_OUTCOME_TEMPLATE.md` | Mandatory V&T surface for C-RSP run summaries. |
| **Schema** | `projects/c-rsp/contract-schema.json` | Machine-readable section and validation rules (includes `blind_man_execution` constraints). |
| **Executed contracts** | `projects/<slug>/BUILD_CONTRACT.md`, `projects/<slug>/BUILD_CONTRACT`, `projects/c-rsp/instances/*.md`, etc. | Filled, scope-specific contracts; these may cite **CONTROL_RULE_KBC_01** and claim execution state. |

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
