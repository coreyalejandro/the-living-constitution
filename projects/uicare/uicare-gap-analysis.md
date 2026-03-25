# UICare Gap Analysis

## Reality-Based Assessment of What Exists

**Date:** 2026-03-23
**Source repo:** `/Users/coreyalejandro/Projects/uicare-system/`
**Assessment method:** Direct source code inspection of all modules, configs, and deployment files

---

## 1. What Exists (Verified)

### Agent Service Layer (Operational)

| File | Purpose | Status |
|------|---------|--------|
| `aiService.js` | Core agent service with Azure OpenAI integration | Operational |
| `agent-definition.yaml` | MonitorAgent + RescueAgent formal configs | Operational |
| `uicare_config.yaml` | Azure subscription, resource group, model config | Operational |

**Details:**
- `aiService.js` exports two functions: `detectLoop(text)` and `getAdvice(details)`
- `detectLoop` calls MonitorAgent deployment via Azure OpenAI chat completions API
- `getAdvice` calls RescueAgent deployment for intervention steps
- Both agents use `gpt-4o-mini` model
- API key read from `AZURE_OPENAI_KEY` environment variable
- Error handling present: throws on non-OK response with status code and body
- **Known issue:** `console.log` statement on line 7 logs the full API URL including deployment name

### Agent Definitions (Validated)

```yaml
MonitorAgent:
  model: gpt-4o-mini
  instructions: "Detect if user text repeats or loops. Return {loopDetected, details}."
  tools: chatCompletion

RescueAgent:
  model: gpt-4o-mini
  instructions: "If loopDetected, offer three clear steps. Return {advice: [string, string, string]}."
  tools: chatCompletion
```

Current agent capabilities are narrow: MonitorAgent detects text repetition/loops, RescueAgent provides 3-step advice. This is the minimum viable agent pair for the loop detection use case.

### Containerization (Operational)

| File | Purpose | Status |
|------|---------|--------|
| `Dockerfile` | Container build for agent service | Operational |
| `docker-compose.yml` | Local multi-agent development | Operational |
| `deployment.yaml` | Kubernetes deployment config | Operational |

**Details:**
- `docker-compose.yml` runs MonitorAgent on port 3001, RescueAgent on port 3002
- Both containers mount the full app directory and use `gpt-4o-mini`
- `deployment.yaml` configures Kubernetes with 256Mi/250m request, 512Mi/500m limits per container
- **Known issue:** deployment.yaml uses `${REGISTRY}` placeholder that must be substituted at deploy time
- **Known issue:** deployment.yaml metadata still says `hackathon-proj-agents` (stale naming)

### Web Application (Operational)

**Framework:** Next.js 14 with App Router
**Location:** `web/`

| Component | File | Purpose | Status |
|-----------|------|---------|--------|
| Main page | `page.tsx` | Loop checker UI with crisis detection | Operational |
| AI Service | `lib/aiService.ts` | Client-side API proxy for agent calls | Operational |
| Risk Service | `lib/riskService.ts` | Risk assessment API client | Operational |
| Mania Service | `lib/maniaService.ts` | Wearable sensor mania risk scoring | Partial |
| Brain | `lib/brain.ts` | SQLite-based embedding store (sql.js) | Operational |
| Proactive Agent | `lib/proactiveAgent.ts` | Future state simulation | Partial |
| Draft Enhancer | `lib/draftEnhancer.ts` | Autosave and AI-improved drafts | Partial |
| Auth | `lib/auth.ts` | Authentication module | Partial |
| Encryption | `lib/encryption.ts` | Data encryption utilities | Partial |

**UI Components:**
- `RealityFilter.tsx` -- CSS filter overlays (Standard, Ninja Vision, Protocol modes)
- `RealityProvider.tsx` -- React context for reality filter state
- `SettingsPanel.tsx` -- User preferences persistence (localStorage)
- `SettingsContext.tsx` -- React context for settings state
- `UIcareToolbar.tsx` -- Toolbar for filter/settings access
- `NinjaPresence.tsx` -- Enhanced contrast mode component
- `PersonalizedContentPlayer.tsx` -- Media queue player for crisis intervention
- `FutureSimulations.tsx` -- Future state prediction display
- `GuidedTutorial.tsx` -- Step-by-step tutorial system
- `MemoryViewer.tsx` -- Memory bank viewer
- `MemoryNavigator.tsx` -- Memory bank navigation

**API Routes:**
- `/api/detect-loop` -- Proxy to MonitorAgent
- `/api/get-advice` -- Proxy to RescueAgent
- `/api/assess-risk` -- Risk assessment endpoint
- `/api/brain` -- Brain embedding API
- `/api/drafts` -- Draft save/retrieve
- `/api/settings` -- User settings
- `/api/memory/[fileName]` -- Memory bank file access
- `/api/simulate-future` -- Future state simulation

### Design System (Operational)

| File | Purpose |
|------|---------|
| `web/src/design-system/colors.ts` | Color tokens |
| `web/src/design-system/typography.ts` | Typography scale |
| `web/src/design-system/spacing.ts` | Spacing tokens |
| `web/src/design-system/breakpoints.ts` | Responsive breakpoints |
| `web/src/design-system/index.ts` | Barrel export |

### Mania Monitoring Module (Partial)

`lib/maniaService.ts` implements:
- `WearableMetrics` interface (heartRate, sleepHours, activity)
- Rolling baseline calculation via running average
- Composite risk score: 33% heart rate delta + 34% sleep deficit + 33% activity spike
- Risk threshold: 0.7 triggers crisis mode in the UI
- **Critical limitation:** `readWearableMetrics()` returns random data (placeholder for real device API)
- Baseline uses mutable module-level state (`let baseline`, `let samples`) -- violates immutability principle

### Brain / Embedding Store (Operational)

`lib/brain.ts` implements:
- SQLite-based vector store using `sql.js` (in-browser/Node SQLite)
- Simple 3-dimensional embedding via character code summation (not a real embedding model)
- Cosine similarity search for retrieval
- `storeEmbedding(text, metadata)` and `searchEmbedding(query, k)` API
- Persistence to `brain.db` file on disk
- **Limitation:** 3-dimensional embedding is toy-level; production would need sentence-transformers or similar

### Memory Bank (Operational)

6 context files in `memory-bank/`:
- `activeContext.md` -- Current work focus, recent changes, next steps
- `productContext.md` -- Product vision and user needs
- `progress.md` -- Implementation progress tracking
- `projectbrief.md` -- Project brief and scope
- `systemPatterns.md` -- Architecture patterns and decisions
- `techContext.md` -- Technology stack and constraints

### Test Coverage (Minimal)

| Test File | What It Tests |
|-----------|---------------|
| `web/src/app/__tests__/riskEscalation.test.tsx` | Risk escalation flow |
| `web/src/app/components/__tests__/GuidedTutorial.test.tsx` | Tutorial component |
| `web/src/app/components/__tests__/MemoryViewer.test.tsx` | Memory viewer |
| `web/src/app/api/auth.test.ts` | Auth API |
| `web/src/lib/__tests__/brain.test.ts` | Brain embedding store |
| `web/src/lib/encryption.test.ts` | Encryption utilities |

6 test files exist. No coverage measurement configured. No CI/CD pipeline present.

---

## 2. What's Missing

### Critical Gaps

| Gap | Impact | Severity |
|-----|--------|----------|
| No CI/CD pipeline | Code changes are unvalidated | Critical |
| No real wearable integration | Mania monitoring returns random data | High |
| Agent-Web integration incomplete | MonitorAgent/RescueAgent output not displayed in real-time UI | High |
| Mutable state in maniaService.ts | Module-level `let baseline` violates immutability | Medium |
| `console.log` in aiService.js | Logs API URL to console in production | Medium |
| No test coverage measurement | Cannot verify code quality | Medium |
| Duplicate React import in page.tsx | Line 3 and 4 both import React with different destructuring | Low (may cause build warning) |
| `hackathon-proj` naming in deployment.yaml | Stale naming from hackathon origin | Low |

### Feature Gaps

| Feature | Description | Priority |
|---------|-------------|----------|
| Quintessential Sign-Off | User-authenticated behavioral baseline protocol | High |
| Reading the Room engine | Absence-based behavioral deviation scoring | High |
| Real-time agent-to-UI pipeline | WebSocket or SSE from MonitorAgent to MoodRING UI | High |
| Environmental sensing | Camera/sensor integration for spatial behavior | Medium |
| Multi-agent orchestration | Coordination layer for specialist agents beyond Monitor/Rescue | Medium |
| Behavioral profile beyond loops | Manic state, anxiety patterns, dissociation signals | Medium |
| Production deployment pipeline | CI/CD, staging, production environments | Medium |
| WCAG 2.1 AA compliance audit | Accessibility target stated but not verified | Medium |

---

## 3. What's Broken

### Duplicate Import in page.tsx

Lines 3-4 of `web/src/app/page.tsx`:
```typescript
import React, { useEffect, useState } from "react";
import React, { useState, useEffect, useRef } from "react";
```

Two conflicting React imports. This will either cause a build error or a runtime warning depending on bundler behavior. The second import is the one that provides `useRef`, so it should replace the first.

### Mutable State in maniaService.ts

```typescript
let baseline: WearableMetrics | null = null;
let samples = 0;
```

Module-level mutable state. The `ingestMetrics()` function mutates `baseline` directly:
```typescript
baseline.heartRate += (metrics.heartRate - baseline.heartRate) / samples;
```

This violates the immutability principle and makes the service non-idempotent. Multiple calls with the same metrics will produce different results because the baseline shifts.

### Missing JSX Closing Structure in page.tsx

The JSX in `page.tsx` has a structural issue around line 222 where a loading skeleton `<ul>` is opened but the ternary structure appears malformed -- the `loading` ternary transitions directly into a `crisis` ternary without proper closing. This may cause rendering issues or build failures depending on the actual whitespace and bracket alignment.

---

## 4. Inventory Summary

| Category | Count | Status |
|----------|-------|--------|
| JavaScript/TypeScript source files | ~25 | 15 operational, 10 partial |
| API routes | 8 | Operational (proxy to agents or local logic) |
| UI components | 11 | Operational |
| Design system tokens | 5 files | Operational |
| Agent definitions | 2 (Monitor + Rescue) | Operational |
| Docker/K8s configs | 3 | Operational |
| Memory bank files | 6 | Operational |
| Test files | 6 | Minimal coverage |
| Documentation files | ~9 | Operational |
| MoodRing Beta | 1 directory | Early/experimental |

---

## V&T Statement

**Exists:** MonitorAgent + RescueAgent definitions and service layer, Docker + Kubernetes containerization, Next.js 14 web application with MoodRING overlay (reality filters, settings, toolbar), 11 UI components, 8 API routes, design system with 5 token files, mania monitoring service (placeholder data), brain embedding store (toy embeddings), memory bank with 6 context files, 6 test files, Azure OpenAI configuration

**Non-existent:** Quintessential Sign-Off protocol, Reading the Room engine, real wearable device integration, environmental sensing, multi-agent orchestration layer, production deployment pipeline, CI/CD configuration, WCAG 2.1 AA compliance verification

**Unverified:** Build success with duplicate import in page.tsx, test pass rate (no CI to confirm), actual crisis intervention effectiveness, accessibility compliance level, whether Docker containers build and run correctly on current code

**Functional status:** Partial -- Agent layer works for loop detection/rescue advice. Web UI renders with reality filters and crisis resources. Mania monitoring uses placeholder data. Brain store uses toy embeddings. The system demonstrates the concept but is not production-ready. Primary gaps are: real sensor integration, agent-to-UI real-time pipeline, behavioral profile depth beyond loop detection, and the Quintessential Sign-Off protocol that is the core innovation.
