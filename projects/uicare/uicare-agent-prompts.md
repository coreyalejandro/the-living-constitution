# UICare Agent Prompts

## Prompt Pack for Uninterrupted Claude Code Continuation

**Purpose:** Self-contained instruction blocks for Claude Code agent sessions. Each prompt targets a specific phase of the UICare build contract.

---

## Prompt 1: Fix Code Defects

```
CONTEXT:
You are working in /Users/coreyalejandro/Projects/uicare-system/
This is a Next.js 14 project with a web/ subdirectory containing the application.

KNOWN DEFECTS:
1. web/src/app/page.tsx has duplicate React imports on lines 3-4:
   Line 3: import React, { useEffect, useState } from "react";
   Line 4: import React, { useState, useEffect, useRef } from "react";

2. web/src/lib/maniaService.ts has mutable module-level state:
   let baseline: WearableMetrics | null = null;
   let samples = 0;
   And ingestMetrics() mutates baseline directly.

3. aiService.js (root) has console.log on line 7 that logs the API URL.

4. deployment.yaml uses "hackathon-proj-agents" naming throughout.
   agent-definition.yaml uses "hackathon-proj" as project name.

TASK:
1. Fix page.tsx: Replace both imports with:
   import React, { useState, useEffect, useRef } from "react";

2. Fix maniaService.ts: Refactor to immutable pattern:
   - Define ManiaState interface: { baseline: WearableMetrics | null; samples: number }
   - Make ingestMetrics pure: (state, metrics) => ManiaState (return new object)
   - Make computeRisk pure: (baseline, metrics) => number (no side effects)
   - Export createManiaMonitor() factory that manages state internally via closure
   - The factory returns { getRisk: (metrics?) => Promise<number> }
   - Keep the WearableMetrics interface and readWearableMetrics placeholder

3. Fix aiService.js: Remove or comment out console.log on line 7.

4. Fix deployment.yaml: Replace all "hackathon-proj-agents" with "uicare-agents"
   Fix agent-definition.yaml: Replace "hackathon-proj" with "uicare"

VERIFY:
- cd web && npm run build (should succeed without warnings)
- No "let" statements remain in maniaService.ts at module level
- No console.log in aiService.js
- grep -r "hackathon" should return nothing
```

---

## Prompt 2: Establish Test Infrastructure

```
CONTEXT:
You are working in /Users/coreyalejandro/Projects/uicare-system/web/
The project has 6 existing test files but no coverage measurement.
Test files exist at:
- src/app/__tests__/riskEscalation.test.tsx
- src/app/components/__tests__/GuidedTutorial.test.tsx
- src/app/components/__tests__/MemoryViewer.test.tsx
- src/app/api/auth.test.ts
- src/lib/__tests__/brain.test.ts
- src/lib/encryption.test.ts

TASK:
1. Check web/package.json for test runner config (likely Jest or Vitest via Next.js)
2. Ensure "test" and "test:coverage" scripts exist in web/package.json
3. Run all existing tests: npm test -- verify which pass and which fail
4. Fix any failing tests if the fix is straightforward

5. Add these new test files:

   a. src/lib/__tests__/aiService.test.ts:
      - Mock global fetch
      - Test detectLoop: returns loopDetected/details on success
      - Test detectLoop: throws on non-OK response
      - Test getAdvice: returns steps array on success
      - Test getAdvice: throws on non-OK response

   b. src/lib/__tests__/maniaService.test.ts:
      - Test computeRisk with known baseline and metrics
      - Test risk score = 0 when metrics match baseline
      - Test risk score > 0.7 with elevated heart rate + reduced sleep
      - Test getManiaRisk returns number between 0 and 1

   c. src/lib/__tests__/riskService.test.ts:
      - Mock global fetch
      - Test assessRisk returns score
      - Test assessRisk throws on error

6. Run full suite: npm test
7. Run coverage: npm run test:coverage

VERIFY:
- All tests pass
- Coverage report shows tested modules above 60%
- At least 9 test files total
```

---

## Prompt 3: Agent-UI Integration

```
CONTEXT:
You are working in /Users/coreyalejandro/Projects/uicare-system/web/
The web app has a one-shot "Check for Loop" button flow.
Agent services are called via /api/detect-loop and /api/get-advice API routes.
The page.tsx has existing state for loop detection and crisis mode.

TASK:
1. Create web/src/types/agents.ts with typed interfaces:
   - MonitorResponse: { readonly loopDetected: boolean; readonly details: string }
   - RescueResponse: { readonly advice: readonly string[] }
   - AgentStatus: "idle" | "monitoring" | "loop-detected" | "crisis" | "offline"

2. Create web/src/hooks/useAgentStatus.ts custom hook:
   - Takes: text (string), enabled (boolean)
   - Returns: { status: AgentStatus, advice: string[] | null, error: string | null }
   - Polls /api/detect-loop every 30 seconds when enabled and text is non-empty
   - Debounces text changes (2 seconds) before sending
   - If loopDetected, auto-fetches advice from /api/get-advice
   - Handles offline state via navigator.onLine
   - Cleans up intervals on unmount

3. Create web/src/app/components/AgentStatusIndicator.tsx:
   - Shows colored dot + label based on AgentStatus
   - idle: gray "Idle"
   - monitoring: green "Monitoring"
   - loop-detected: amber "Loop Detected"
   - crisis: red "Crisis"
   - offline: gray "Offline"
   - Accessible: uses aria-label and role="status"

4. Integrate into page.tsx:
   - Use useAgentStatus hook
   - Add AgentStatusIndicator to the toolbar area
   - When advice is auto-provided, display it without requiring button click

VERIFY:
- npm run build succeeds
- AgentStatusIndicator renders with correct colors for each status
- Hook cleans up on unmount (no memory leaks)
```

---

## Prompt 4: Mania Monitoring Hardening

```
CONTEXT:
You are working in /Users/coreyalejandro/Projects/uicare-system/web/
The maniaService.ts should now be refactored to immutable patterns (from Prompt 1).
The readWearableMetrics() function returns random data.

TASK:
1. Create web/src/lib/wearableProviders.ts:

   interface WearableProvider {
     readonly name: string;
     readMetrics(): Promise<WearableMetrics>;
   }

   class MockWearableProvider implements WearableProvider {
     readonly name = "mock";
     async readMetrics(): Promise<WearableMetrics> {
       return {
         heartRate: 60 + Math.random() * 40,
         sleepHours: 6 + Math.random() * 2,
         activity: 4000 + Math.random() * 2000,
       };
     }
   }

   class AppleHealthProvider implements WearableProvider {
     readonly name = "apple-health";
     async readMetrics(): Promise<WearableMetrics> {
       throw new Error("Apple Health integration pending. Using mock data.");
     }
   }

   function createWearableProvider(type: string = "mock"): WearableProvider {
     switch (type) {
       case "apple-health": return new AppleHealthProvider();
       default: return new MockWearableProvider();
     }
   }

2. Update maniaService.ts to accept a WearableProvider parameter in getManiaRisk()

3. In page.tsx, show a small label when mock provider is active:
   "(Using simulated sensor data)"

4. Add test: web/src/lib/__tests__/wearableProviders.test.ts
   - MockWearableProvider returns metrics within expected ranges
   - AppleHealthProvider throws with informative error

VERIFY:
- npm run build succeeds
- npm test passes
- UI shows mock data indicator
```

---

## Prompt 5: CI/CD and Final Validation

```
CONTEXT:
You are working in /Users/coreyalejandro/Projects/uicare-system/
All code fixes from prior prompts are complete.

TASK:
1. Create .github/workflows/ci.yml:
   name: UICare CI
   on:
     push:
       branches: [main]
     pull_request:
       branches: [main]
   jobs:
     test:
       runs-on: ubuntu-latest
       steps:
         - uses: actions/checkout@v4
         - uses: actions/setup-node@v4
           with:
             node-version: '20'
         - run: cd web && npm ci
         - run: cd web && npm test
         - run: cd web && npm run build
     docker:
       runs-on: ubuntu-latest
       steps:
         - uses: actions/checkout@v4
         - run: docker compose build

2. Update README.md:
   - Update Status Matrix to reflect all fixes
   - Remove any stale hackathon references
   - Update V&T Statement

3. Final validation:
   - cd web && npm test (all pass)
   - cd web && npm run build (succeeds)
   - docker compose build (succeeds)
   - grep -r "hackathon" . (returns nothing)
   - grep -rn "console.log" aiService.js (returns nothing)

VERIFY: All checks pass. README is accurate.
```

---

## V&T Statement

**Exists:** Five agent prompts covering the complete UICare hardening pipeline from code fixes through CI/CD establishment, based on verified source code defects and gaps

**Non-existent:** Execution of these prompts (they are instructions, not completed work)

**Unverified:** Whether prompts produce expected results when executed (dependent on current codebase state and dependency versions)

**Functional status:** Operational as instruction set -- prompts are deterministic, ordered, and independently executable after sequential dependency resolution
