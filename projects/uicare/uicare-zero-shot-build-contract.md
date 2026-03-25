# UICare Zero-Shot Build Contract

## Objective

Harden the UICare system from Partial to Validated status by fixing code defects, establishing CI, improving agent-UI integration, and replacing placeholder implementations with production-grade alternatives.

**Precondition:** The web application, agent service, and containerization already exist. This contract fixes, integrates, and hardens.

---

## Phase 1: Code Defect Fixes (Immediate)

### Task 1.1: Fix Duplicate Import in page.tsx

**Input:** `web/src/app/page.tsx` lines 3-4
**Output:** Single correct import

**Action:** Replace both lines with:
```typescript
import React, { useState, useEffect, useRef } from "react";
```

**Acceptance criteria:**
- `npm run build` in `web/` succeeds without warnings
- Page renders correctly in browser

### Task 1.2: Fix Mutable State in maniaService.ts

**Input:** `web/src/lib/maniaService.ts`
**Output:** Immutable version using function parameters instead of module state

**Actions:**
1. Remove module-level `let baseline` and `let samples`
2. Create a `ManiaState` interface: `{ baseline: WearableMetrics | null; samples: number }`
3. Make `ingestMetrics` a pure function: `(state: ManiaState, metrics: WearableMetrics) => ManiaState`
4. Make `computeRisk` a pure function: `(baseline: WearableMetrics, metrics: WearableMetrics) => number`
5. Export a `createManiaMonitor()` factory that returns an object with `getRisk(metrics?)` method using closure state
6. Alternatively, use React context or a store if state needs to persist across renders

**Acceptance criteria:**
- `getManiaRisk()` with identical metrics twice produces identical risk scores
- No module-level `let` statements remain
- Existing tests still pass

### Task 1.3: Remove console.log from aiService.js

**Input:** `aiService.js` line 7
**Output:** Remove or replace with proper logging

**Action:** Remove `console.log('Calling Azure OpenAI:', url);` or guard it behind a `DEBUG` environment variable check.

**Acceptance criteria:**
- No `console.log` statements in production code
- API URL is not leaked to client console

### Task 1.4: Fix Deployment Naming

**Input:** `deployment.yaml`
**Output:** Replace `hackathon-proj-agents` with `uicare-agents`

**Actions:**
1. Replace all instances of `hackathon-proj-agents` with `uicare-agents` in metadata.name, spec.selector, and template.metadata.labels
2. Replace `hackathon-proj` with `uicare` in `agent-definition.yaml`

**Acceptance criteria:**
- `deployment.yaml` contains no references to `hackathon`
- `agent-definition.yaml` project field is `uicare`

---

## Phase 2: Test Infrastructure

### Task 2.1: Add package.json Test Script

**Input:** `web/package.json`
**Output:** Test scripts configured for Jest/Vitest

**Actions:**
1. Verify test runner is installed (check web/package.json devDependencies)
2. Add or verify `"test"` script in web/package.json
3. Add `"test:coverage"` script with coverage flag
4. Run tests and verify all 6 existing test files pass

**Acceptance criteria:**
- `cd web && npm test` runs all tests
- `cd web && npm run test:coverage` produces coverage report
- All existing tests pass

### Task 2.2: Add Critical Missing Tests

**Input:** Existing test files
**Output:** New test files for untested critical paths

**Tests to add:**
1. `web/src/lib/__tests__/aiService.test.ts` -- Mock fetch, test detectLoop and getAdvice happy/error paths
2. `web/src/lib/__tests__/maniaService.test.ts` -- Test risk scoring with known metrics, baseline calculation, threshold behavior
3. `web/src/lib/__tests__/riskService.test.ts` -- Mock fetch, test assessRisk
4. `web/src/app/api/detect-loop/__tests__/route.test.ts` -- Test API route handler

**Acceptance criteria:**
- 10+ test files total
- All tests pass
- Coverage of critical paths (agent calls, risk scoring, API routes)

---

## Phase 3: Agent-UI Integration

### Task 3.1: Create Agent Response Types

**Input:** `agent-definition.yaml` response schemas
**Output:** `web/src/types/agents.ts`

**Content:**
```typescript
export interface MonitorResponse {
  readonly loopDetected: boolean;
  readonly details: string;
}

export interface RescueResponse {
  readonly advice: readonly [string, string, string];
}

export interface RiskAssessment {
  readonly score: number;
  readonly factors: readonly string[];
}
```

**Acceptance criteria:**
- All agent service functions use these types for return values
- Type checking passes with `tsc --noEmit`

### Task 3.2: Real-Time Agent Status in UI

**Input:** `page.tsx` current one-shot check flow
**Output:** Polling-based agent status display

**Actions:**
1. Add a `useAgentStatus` custom hook that polls `/api/detect-loop` every 30 seconds when text is present
2. Display agent status indicator in toolbar: "Monitoring" (green) / "Loop Detected" (amber) / "Crisis" (red) / "Offline" (gray)
3. When loop detected, auto-trigger RescueAgent advice without requiring button click
4. Debounce text changes before sending to agent (2-second debounce)

**Acceptance criteria:**
- Agent status updates automatically every 30 seconds
- Status indicator visible in toolbar
- No excessive API calls (debounced, paused when no text)

---

## Phase 4: Mania Monitoring Hardening

### Task 4.1: Create Wearable Integration Interface

**Input:** `web/src/lib/maniaService.ts`
**Output:** Abstracted wearable provider interface

**Actions:**
1. Define `WearableProvider` interface with `readMetrics(): Promise<WearableMetrics>`
2. Create `MockWearableProvider` (current random implementation)
3. Create `AppleHealthProvider` stub (returns error: "Apple Health integration pending")
4. Create `FitbitProvider` stub (returns error: "Fitbit integration pending")
5. Factory function `createWearableProvider(type: string)` selects provider
6. The `getManiaRisk()` function accepts a `WearableProvider` parameter

**Acceptance criteria:**
- `maniaService.ts` no longer uses hardcoded random data directly
- Provider selection is explicit and configurable
- Mock provider is clearly labeled as mock in UI
- Tests verify risk calculation with deterministic mock data

---

## Phase 5: CI/CD Pipeline

### Task 5.1: Create GitHub Actions Workflow

**Input:** None
**Output:** `.github/workflows/ci.yml`

**Actions:**
1. Trigger on push and pull_request to main
2. Steps: checkout, setup-node (20.x), install dependencies, run lint, run tests, run build
3. Separate job for Docker build verification

**Acceptance criteria:**
- CI runs on push
- Tests must pass for PR merge
- Build must succeed

---

## Phase 6: Documentation Cleanup

### Task 6.1: Update README Status Matrix

**Input:** `README.md`
**Output:** Updated status matrix reflecting fixes from Phases 1-4

**Acceptance criteria:**
- All status labels match actual code state after fixes
- No stale hackathon references
- V&T Statement updated

---

## Dependency Graph

```
Phase 1 (no dependencies, all tasks independent)
  |
  v
Phase 2 (depends on Phase 1 fixes for clean test runs)
  |
  v
Phase 3 (depends on Phase 2 for test infrastructure)
  Phase 4 (can run parallel with Phase 3)
  |
  v
Phase 5 (depends on Phase 2)
  |
  v
Phase 6 (depends on all prior phases)
```

---

## Estimated Effort

| Phase | Tasks | Estimate |
|-------|-------|----------|
| Phase 1: Code fixes | 4 | 30 minutes |
| Phase 2: Test infrastructure | 2 | 60 minutes |
| Phase 3: Agent-UI integration | 2 | 90 minutes |
| Phase 4: Mania hardening | 1 | 45 minutes |
| Phase 5: CI/CD | 1 | 30 minutes |
| Phase 6: Documentation | 1 | 15 minutes |
| **Total** | **11** | **~4.5 hours** |

---

## V&T Statement

**Exists:** This build contract with 6 phases and 11 tasks, derived from direct source inspection of all UICare modules, identifying specific line-level defects and missing infrastructure

**Non-existent:** The fixes, tests, integration work, and CI pipeline described in this contract

**Unverified:** Time estimates, whether existing 6 test files pass on current codebase, Docker build success

**Functional status:** Pending -- This contract defines the path from Partial (working demo with defects) to Validated (tested, CI-gated, production-naming, immutable patterns)
