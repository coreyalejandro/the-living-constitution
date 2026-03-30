# Verification Matrix
## Every Resume Claim -> Evidence

Last updated: 2026-03-30

| # | Resume Claim | Project | Evidence Location | Verification Method | Status | Result |
|---|-------------|---------|-------------------|-------------------|--------|--------|
| 1 | PROACTIVE: 100% detection rate, 8 test cases, n=19 violations | PROACTIVE | `validation_results.json` | File inspection | VERIFIED | File exists with claimed metrics |
| 2 | PROACTIVE: 0% false positive rate | PROACTIVE | `validation_results.json` | File inspection | VERIFIED | Confirmed in validation results |
| 3 | PROACTIVE: GitLab Duo + Claude Code agents | PROACTIVE | `.gitlab-ci.yml`, source code | Code inspection | VERIFIED | GitLab CI config and source confirmed |
| 4 | PROACTIVE: 212/212 tests passing | PROACTIVE | `pytest` output | `pytest -v` | VERIFIED | 212 passed in 0.27s (2026-03-25) |
| 5 | PROACTIVE: Submitted to GitLab AI Hackathon | PROACTIVE | gitlab.com/gitlab-ai-hackathon/participants/28441830 | URL check | VERIFIED | Submission confirmed |
| 6 | SentinelOS: TypeScript framework | SentinelOS | `packages/*/src/**/*.ts` | `wc -l` | VERIFIED | 1,037 LOC source (not ~1,500 as resume claims — UPDATE NEEDED) |
| 7 | SentinelOS: 6 safety invariants (I1-I6) | SentinelOS | `packages/core/src/constants/invariants.ts` | Code inspection | VERIFIED | All 6 defined with descriptions |
| 8 | SentinelOS: Build passes, types verified | SentinelOS | `pnpm build && tsc --noEmit` | Build + typecheck | PENDING | Node PATH issue in worktree; needs verification |
| 9 | Living Constitution: 5-article structure | TLC | `THE_LIVING_CONSTITUTION.md` | Document review | VERIFIED | All 5 articles present with full specification |
| 10 | Living Constitution: Agent republic (6 agents) | TLC | Article IV definitions | Document review | VERIFIED | 6 agents with power boundaries defined |
| 11 | Living Constitution: SOP-013 Session Recovery | TLC | `THE_LIVING_CONSTITUTION.md` Page 5 | Document review | VERIFIED | Full protocol documented |
| 12 | ConsentChain: 7-stage action gateway | ConsentChain | `apps/web/src/app/api/agent/action/route.ts` | Code inspection | VERIFIED | 7 stages confirmed in route handler |
| 13 | ConsentChain: Turborepo packages | ConsentChain | `packages/` + `apps/` | `ls` | VERIFIED | 8 packages in packages/, 1 app in apps/ |
| 14 | ConsentChain: Prisma schema | ConsentChain | `prisma/schema.prisma` | File exists | VERIFIED | 5 models: Agent, LedgerEntry, RevocationState, IdempotencyRecord, StepUpChallenge |
| 15 | UICare: GPT-4o-mini integration | UICare | Source code | `grep gpt-4o-mini` | VERIFIED | Referenced in deployment.yaml, agent-definition.yaml, docker-compose.yml, uicare_config.yaml |
| 16 | UICare: Kubernetes deployment | UICare | `deployment.yaml` | File exists | VERIFIED | deployment.yaml, Dockerfile, docker-compose.yml all present |
| 17 | UICare: Memory-bank architecture | UICare | `memory-bank/`, `brain/` modules | Directory exists | VERIFIED | memory-bank/, web/src/app/memory/, web/src/app/api/brain/ all exist |
| 18 | Docen: Deployed at GCR URL | Docen | HTTP response | `curl` returns 200 | VERIFIED | HTTP 200 (verified 2026-03-25) |
| 19 | Portfolio: Live at coreyalejandro.com | Portfolio | HTTP response | `curl` returns 200/307 | VERIFIED | HTTP 200, redirects to www.coreyalejandro.com |
| 20 | GitHub: repo count | GitHub | GitHub API | `gh api` | PARTIAL | API returned 257 repos — resume claims ~340. Discrepancy under investigation. |
| 21 | Zero-shot build contracts methodology | This repo | `projects/*/BUILD_CONTRACT.md` | Files exist | VERIFIED | BUILD_CONTRACT.md exists for SentinelOS, PROACTIVE, ConsentChain, UICare |
| 22 | MADMall: Production infrastructure | MADMall | Repo inspection | File tree + package.json | VERIFIED | 6 apps, 22 packages, ~152K LOC, Clerk/Stripe/Prisma wired |
| 23 | MADMall: ML Python package | MADMall | `ml/` directory | Code inspection | VERIFIED | CRISP-DM methodology, Jupyter notebooks, feature extraction |
| 24 | MADMall: Healthcare focus (Graves' disease) | MADMall | Notebooks, PROJECT.md | Content review | VERIFIED | Black women with Graves' disease — core product mission |
| 25 | TLC: Institutionalization layer (scheduled verify, regression ledger, escalation, adversarial tests, system card) | TLC | `.github/workflows/verify.yml`; `verification/regression-ledger/`; `scripts/verify_institutionalization.py`; `verification/GOVERNANCE_SYSTEM_CARD.md` | CI + local scripts per inventory `ci_verification_commands` | VERIFIED | PASS 5 — local verify 2026-03-30 (governance + institutionalization + failure-injection harness) |

## Verification Progress

- Total claims: 25
- Verified: 22
- Partial: 1 (GitHub repo count discrepancy)
- Pending: 1 (SentinelOS build)
- Failed: 0
- **Claims requiring resume update**: SentinelOS LOC (1,037 actual, not ~1,500), GitHub repos (257 verified, not ~340)

*Updated 2026-03-30 — added claim 25 (TLC institutionalization PASS 5).*
