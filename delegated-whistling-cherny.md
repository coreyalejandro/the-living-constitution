# Plan: Living Constitution Base Camp + Application Readiness Sprint

## Context

Corey is applying to the **Anthropic Safety Fellows Program (July 2026 cohort)** with a deadline of **Monday March 23rd at 7am**. Today is Friday March 21st (~60 hours).

The resume and cover letter make specific claims about 6 projects. This plan closes every gap between what's claimed and what actually exists, using The Living Constitution repo as the operational base camp.

**Success = every resume claim is truthful at the stated status level, verifiable by evidence.**

---

## Ground Truth Audit (Resume Claims vs. Reality)

| Project | Resume Status | Actual State | Gap |
|---------|--------------|-------------|-----|
| PROACTIVE | Operational, 100% detection, 0% FP | Python + React, GitLab hackathon. Tests broken (Python version). | FIX TESTS |
| Living Constitution | Implementing (ready by deadline) | 416-line spec doc only. Zero code. | BUILD BASE CAMP |
| SentinelOS | Partial, ~1,500 LOC TypeScript | ~404 LOC embedded in portfolio. No standalone repo. | **CRITICAL: ~1,100 LOC gap** |
| ConsentChain | Partial, 7-stage gateway, Turborepo 8 packages | Turborepo, 7 packages + web app, gateway tested via curl | VERIFY ONLY |
| UICare-System | Partial, GPT-4o-mini + K8s | Full-stack web app, Docker + K8s configs | VERIFY ONLY |
| Docen | Deployed | HTTP 200 confirmed | NONE |
| Portfolio | coreyalejandro.com | HTTP 307 (Vercel redirect) | VERIFY LIVE |

---

## Phase 0: Teaser Video (Friday Evening)
**Time: ~2-4h | User-driven creative work**

User said this must be completed first. No code dependencies.

---

## Phase 1: Living Constitution Base Camp Setup
**Time: ~3-4h | Critical path**

Transform `/Users/coreyalejandro/Projects/the-living-constitution/` from spec-only to operational hub.

### 1.1 Install CLAUDE.md
- Create `CLAUDE.md` in repo root referencing the constitutional framework
- Include repo-specific rules: this is the governance overlay, not a code repo
- Define the base camp structure and zero-shot build contract format

### 1.2 Create operational structure
```
the-living-constitution/
  THE_LIVING_CONSTITUTION.md    (exists)
  CLAUDE.md                     (new)
  tasks/
    todo.md                     (sprint tracker)
    lessons.md                  (amendment log)
  contracts/
    proactive.md                (build contract + status)
    sentinelos.md               (build contract + status)
    consentchain.md             (build contract + status)
    uicare.md                   (build contract + status)
  verification/
    MATRIX.md                   (maps every resume claim to evidence)
    proactive.md                (V&T for PROACTIVE)
    sentinelos.md               (V&T for SentinelOS)
    consentchain.md             (V&T for ConsentChain)
    uicare.md                   (V&T for UICare)
  config/
    projects.ts                 (domain mapping - 4 safety domains)
    domains.ts                  (domain definitions)
```

### 1.3 Write zero-shot build contracts
Each `contracts/<project>.md` is a machine-actionable spec:
- Current state (honest)
- Target state (what resume claims)
- Acceptance criteria (what "done" looks like)
- Evidence required (how to prove it)

### Key files:
- `/Users/coreyalejandro/Projects/the-living-constitution/THE_LIVING_CONSTITUTION.md`

---

## Phase 2: SentinelOS -- Close the LOC Gap
**Time: ~6-8h | CRITICAL: biggest truthfulness gap**

Resume claims "~1,500 LOC TypeScript." Reality is ~404 LOC across portfolio files. The architecture docs already specify what the code should do -- this is implementing a documented spec, not padding.

### 2.1 Create standalone SentinelOS package
Location: `/Users/coreyalejandro/Projects/sentinelos/` (new repo)

### 2.2 Build real framework code (all specified in existing architecture docs)
- `src/core/invariants.ts` -- I1-I6 invariant definitions + validation functions (~150 LOC)
- `src/core/truth-status.ts` -- Truth status engine, status transition validation (~200 LOC)
- `src/core/vt-statement.ts` -- V&T Statement generator/validator (~150 LOC)
- `src/domains/index.ts` -- 4 safety domain registry (Epistemic, Human, Cognitive, Empirical) (~100 LOC)
- `src/incident/lifecycle.ts` -- Incident lifecycle state machine per docs (~200 LOC)
- `src/incident/types.ts` -- Incident types + severity classification (~100 LOC)
- `src/safety-case/skeleton.ts` -- Safety case structure as typed data (~150 LOC)
- `src/index.ts` -- Public API surface (~50 LOC)
- `__tests__/` -- Unit tests for the above (~300 LOC)

Total: ~1,400 LOC new + existing concepts = reaches ~1,500 claim

### 2.3 Install CLAUDE.md in sentinelos repo
### 2.4 Push to GitHub at github.com/coreyalejandro/sentinelos

### Key files (existing architecture specs to implement from):
- `/Users/coreyalejandro/Projects/coreys-agentic-portfolio/config/sentinel/truthStatus.ts` (types + module registry)
- `/Users/coreyalejandro/Projects/coreys-agentic-portfolio/docs/SentinelOS_ARCHITECTURE.md`
- `/Users/coreyalejandro/Projects/coreys-agentic-portfolio/docs/SentinelOS_INCIDENT_LIFECYCLE.md`
- `/Users/coreyalejandro/Projects/coreys-agentic-portfolio/docs/SentinelOS_SAFETY_CASE.md`

---

## Phase 3: PROACTIVE -- Fix Test Environment
**Time: ~2-3h**

Resume says "Operational, Validated." Tests must pass.

### 3.1 Fix Python version (requires >=3.11, system has 3.9)
- Install Python 3.11+ via pyenv or homebrew
- Add `.python-version` file

### 3.2 Install and run tests
- `pip install -e ".[dev]"`
- `pytest` -- fix any failures
- Verify `validation_results.json` matches 100% detection / 0% FP claims

### 3.3 Install CLAUDE.md in proactive repo

### Key files:
- `/Users/coreyalejandro/Projects/proactive-gitlab-agent/pyproject.toml`

---

## Phase 4: ConsentChain + UICare -- Verify Partial Claims
**Time: ~3-4h**

Both claim "Partial" which is honest. Just verify and document.

### ConsentChain
- `pnpm install` at repo root
- `pnpm exec next dev --port 3000` in apps/web
- Run curl tests from HANDOFF.md (gateway flow)
- Count packages: 7 packages + 1 app = "8 packages" (matches claim)
- Install CLAUDE.md

### UICare
- `npm install && npm run dev` in web/
- `docker build .` -- verify builds
- Confirm GPT-4o-mini integration in aiService.js
- Confirm K8s deployment.yaml exists
- Install CLAUDE.md

### Key files:
- `/Users/coreyalejandro/Projects/consentchain/HANDOFF.md`
- `/Users/coreyalejandro/Projects/uicare-system/`

---

## Phase 5: Docen + Portfolio -- Quick Verify
**Time: ~1h**

Both appear working. Confirm and document.

- Verify docen-live deployment loads
- Verify coreyalejandro.com loads
- Document in verification matrix

---

## Phase 6: Verification Matrix + Final Assembly
**Time: ~3-4h**

### 6.1 Create `verification/MATRIX.md`
Every resume claim mapped to evidence:

| Claim | Evidence Location | Method | Result |
|-------|------------------|--------|--------|
| PROACTIVE 100% detection | validation_results.json | Run pytest | PASS/FAIL |
| SentinelOS ~1,500 LOC | `wc -l src/**/*.ts` | Count | XXXX |
| ConsentChain 7-stage gateway | curl test transcript | Manual test | PASS/FAIL |
| etc. | | | |

### 6.2 Final V&T for the Commonwealth
### 6.3 Review all CLAUDE.md files consistent
### 6.4 Git commit + push all repos

---

## Phase 7: Buffer + Application Submission
**Time: Sunday evening -- Monday 7am**

- Review full application package
- Verify all links work
- Submit at 7am Monday

---

## Time Budget

| Phase | Hours | When |
|-------|-------|------|
| 0: Teaser Video | 2-4h | Friday evening |
| 1: Base Camp Setup | 3-4h | Saturday AM |
| 2: SentinelOS LOC | 6-8h | Saturday PM |
| 3: PROACTIVE Fix | 2-3h | Saturday evening |
| 4: ConsentChain + UICare | 3-4h | Sunday AM |
| 5: Docen + Portfolio | 1h | Sunday AM |
| 6: Verification Matrix | 3-4h | Sunday PM |
| 7: Buffer | 6-8h | Sunday PM -- Monday |
| **Total** | **~26-35h** | **Fits in ~60h with sleep** |

---

## Scope Discipline (What NOT to Do)

- Do NOT build "planned" modules (HUI Gov, Eval Workbench) -- they are honestly "planned"
- Do NOT try to deploy ConsentChain or UICare -- they are honestly "partial"
- Do NOT rewrite PROACTIVE -- it works, just fix the test env
- Do NOT over-engineer the base camp -- it is governance overlay, not monorepo
- Do NOT build CI/CD -- Tier 1 (convention) governance is honest

---

## Verification

After all phases complete, run this checklist:

1. `cd the-living-constitution && ls CLAUDE.md tasks/ contracts/ verification/` -- base camp exists
2. `cd sentinelos && wc -l src/**/*.ts` -- ~1,500 LOC
3. `cd proactive-gitlab-agent && pytest` -- tests pass
4. `cd consentchain && pnpm install && pnpm exec next dev --port 3000` -- starts
5. `cd uicare-system && npm install && npm run dev` -- starts
6. `curl -s https://docen-live-677222981446.us-central1.run.app` -- HTTP 200
7. `curl -s https://coreyalejandro.com` -- loads
8. Every claim in `verification/MATRIX.md` has evidence
