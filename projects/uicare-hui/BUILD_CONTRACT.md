# Build Contract: UICare-HUI — Behavioral Safety System
# (TLC Governance Overlay — Implementation at /Users/coreyalejandro/Projects/uicare-hui)

## Contract ID
CRSP-UICARE-HUI-001

## Governing Instance
`projects/c-rsp/instances/CRSP-UICARE-HUI-001.md`

## Repo Path
`/Users/coreyalejandro/Projects/uicare-hui`

## GitHub Remote
https://github.com/coreyalejandro/uicare-hui (to be created and pushed)

## Current State (Honest)

Build contract executed. Monorepo scaffolded and committed locally.

- `packages/safety-core/` — Pure TypeScript, zero runtime deps. All 11 invariants
  implemented as assertion functions. Ports defined for SignalCollector, ConsentStore,
  InterventionDisplay, AuditLogger, DataLifecycle, Clock, AIAdvisor.
- `apps/pwa/` — Next.js 14 PWA with IndexedDB adapters, AES-256-GCM encryption,
  BehavioralGate and InterventionBanner UI components, useBehavioralSafety hook.
- `apps/experimental-tools/` — HUI Python research packages. Isolated. No production
  safety dependency.
- `tests/` — 72/72 passing (57 unit + 15 governance).
- `docs/` — 6 governance documents. governance-report.md STATUS: DRAFT.
- `.github/workflows/ci.yml` — 5 CI jobs including boundary-check (INVARIANT_011).
- Git: local commit exists. No remote.

## Target State (What This Contract Claims)

A production-grade Hexagonal Architecture monorepo implementing a local-first
Behavioral Safety System. The system gates high-risk user actions during unsafe
behavioral states, surfaces non-clinical interventions, enforces explicit consent,
and operates fully offline. The AI advisor (Azure OpenAI) is a replaceable adapter
with graceful degradation — AI failure never disables local safety gates.

## Acceptance Criteria

1. `packages/safety-core` builds with zero runtime dependencies (INVARIANT_011)
2. 72/72 automated tests pass
3. CI boundary lint enforces INVARIANT_011 on every PR
4. All Safety Specification gate documents approved in STATUS.json
5. governance-report.md reviewed and signed off (SPEC_006 → APPROVED)
6. GitHub remote created and pushed
7. MASTER_PROJECT_INVENTORY.json updated with uicare-hui slug

## Phased Implementation (Phases 0–8)

All phases executed. Evidence in implementation repo.

## Not Claimed

- Not a medical device
- Not an emergency-response system
- Not a clinical diagnostic tool
- Does not replace professional mental-health services
- `apps/pwa` Next.js build (next build) not CI-verified yet
- AuditLogger IndexedDB adapter not yet written
- DataLifecycle adapter not yet written
- Real SignalCollector wearable adapter not yet written
- Playwright accessibility tests not yet written
- GitHub remote not yet created

## Verification Commands

```bash
cd /Users/coreyalejandro/Projects/uicare-hui
npm run test:core      # 57 unit tests
npm run test           # 72 tests (unit + governance)
npm run build          # safety-core TypeScript build
npm run lint:boundaries  # INVARIANT_011 boundary check
```

## TLC Articles Governing This Contract

Articles I–V (The Living Constitution). Authority order:
  projects/c-rsp/BUILD_CONTRACT.md (1) >
  projects/c-rsp/instances/CRSP-UICARE-HUI-001.md (2) >
  projects/c-rsp/contract-schema.json (3) >
  this file (governance overlay, not canonical C-RSP source)
