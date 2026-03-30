# Sprint: Anthropic Safety Fellows Application
## Deadline: Monday March 23, 2026 — 7:00 AM

### Phase 0: Teaser Video
- [ ] Complete teaser video for LinkedIn release / application

### Phase 1: Base Camp Setup
- [x] Create CLAUDE.md with Living Constitution controls
- [x] Create directory structure
- [x] Write zero-shot build contracts for each project
- [x] Create teaser-video project folder with CLAUDE.md + BUILD_CONTRACT.md
- [x] Create evidence-observatory project folder with CLAUDE.md + BUILD_CONTRACT.md

### Phase 1.5: TLC Evidence Observatory (NEW)
- [ ] Build Evidence Observatory from zero-shot contract
- [ ] Python pipeline: ingest → normalize → extract → admissibility → adjudicate
- [ ] Case file + benchmark + eval generation
- [ ] Next.js research UI shell
- [ ] Seed data end-to-end demonstration
- [ ] Documentation (README, research-methodology, architecture)

### Phase 2: SentinelOS Turborepo Monorepo (hex8)
- [ ] Write build contract (spec before build)
- [ ] Initialize Turborepo with hexagonal architecture
- [ ] Implement core package (types, invariants, domains)
- [ ] Implement article-i through article-v packages
- [ ] Implement incident + safety-case packages
- [ ] Write tests (~300 LOC)
- [ ] Verify ~1,500 LOC total

### Phase 3: PROACTIVE — Fix Tests
- [ ] Fix Python version (>=3.11)
- [ ] Install dev dependencies
- [ ] Run pytest — fix failures
- [ ] Verify validation_results.json matches claims

### Phase 4: ConsentChain + UICare — Verify
- [ ] ConsentChain: pnpm install + dev server starts
- [ ] ConsentChain: curl tests from HANDOFF.md pass
- [ ] UICare: npm install + dev server starts
- [ ] UICare: Docker build succeeds

### Phase 5: Docen + Portfolio — Quick Verify
- [ ] Docen: deployment returns HTTP 200
- [ ] Portfolio: coreyalejandro.com loads

### Phase 6: Verification Matrix
- [ ] Create MATRIX.md mapping every resume claim to evidence
- [ ] Per-project V&T statements
- [ ] Final Commonwealth V&T
- [ ] Git commit + push all repos
