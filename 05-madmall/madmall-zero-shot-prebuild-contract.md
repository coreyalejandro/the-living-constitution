# MADMall Zero-Shot Pre-Build Contract

## Contract Metadata

| Field | Value |
|-------|-------|
| System | MADMall |
| Domain | All four: Epistemic, Human, Cognitive, Empirical Safety |
| Current Status | Pending |
| Target Status | Partial (hackathon prototype) |
| Contract Type | Pre-build — no code exists, this contract defines what will be created |
| Target Event | Healthcare hackathon (~1.5 months from 2026-03-23) |
| Dependencies | ConsentChain at Validated status, UICare pattern library available |
| Stack (Planned) | Next.js 15 (App Router), Turborepo, pnpm, Prisma (PostgreSQL), TypeScript, Tailwind, ConsentChain SDK |

## Pre-Conditions

Before MADMall prototype build begins, the following must be true:

| Pre-Condition | Verification Method | Status |
|---------------|-------------------|--------|
| ConsentChain test suite passes with >= 80% coverage | `pnpm test` in ConsentChain repo exits 0 | Pending |
| ConsentChain Agent SDK is complete and typed | `@consentchain/agent-sdk` exports ConsentChainClient | Pending |
| ConsentChain CI pipeline runs on every push | GitHub Actions workflow exists and passes | Pending |
| UICare component patterns documented | Pattern library with at least: Button, Form, StepFlow, CompletionSignal, ErrorDignity | Pending |
| Healthcare hackathon rules and constraints reviewed | Hackathon requirements document read and analyzed | Pending |
| Regulatory advisory input received | At minimum: one conversation with someone who has HIPAA compliance experience | Pending |

## Prototype Scope Definition

The hackathon prototype demonstrates the full Commonwealth stack applied to a single healthcare use case. It is not a complete healthcare platform. It is a vertical slice that proves the architecture works.

### The Vertical Slice: Guided Care Navigation

One complete user flow from start to finish:

```
User opens MADMall
    |
    v
Creates wellness profile
    - Cultural background (optional)
    - Neurodivergence indicators (optional)
    - Communication preferences
    - Accessibility needs
    |
    v
Selects "Find a therapist"
    |
    v
Guided step-by-step flow:
    Step 1: What kind of support? (dropdown: anxiety, depression, PTSD, ADHD, general)
    Step 2: Insurance or self-pay? (binary choice)
    Step 3: Location preference (zip code or "telehealth only")
    Step 4: Cultural preferences (language, identity-affirming care, optional)
    Step 5: Review selections (all on one screen, editable)
    |
    v
Results displayed
    - Provider cards with match score
    - Each card explains WHY it matched
    - "Schedule" button per provider
    |
    v
Scheduling flow (simulated)
    - ConsentChain gate: "MADMall will share your preferences with [Provider]. Approve?"
    - ConsentChain ledger entry created
    - Confirmation screen with next steps
    |
    v
Consent history visible
    - User sees: "You shared [data] with [provider] on [date]"
    - "Revoke" button available
```

### What the Prototype Includes

| Component | Scope |
|-----------|-------|
| Wellness profile | CRUD for one user. 4 fields. Stored in Prisma. |
| Care navigation flow | 5-step guided flow for therapist search. Simulated provider database. |
| ConsentChain integration | Agent SDK calls for data sharing consent. Ledger entry visible to user. Revocation functional. |
| Provider matching | Simple algorithm: match on insurance, location, specialty, cultural preferences. No ML. |
| Consent dashboard | User sees their consent history. Can revoke. Can see ledger entries. |
| UICare patterns | Cognitive load budgeting, progressive disclosure, completion signals, error dignity applied to all screens. |

### What the Prototype Excludes

| Excluded | Reason |
|----------|--------|
| Real provider database | Requires healthcare data partnerships. Simulated data is sufficient for demonstration. |
| Real scheduling | Requires calendar API integration with provider systems. Simulated is sufficient. |
| Community spaces | Scope exceeds hackathon timeline. Phase 3 feature. |
| External health service connections | Requires OAuth integrations with health platforms. Phase 3 feature. |
| Measurement instruments | Requires clinical validation. Phase 3 feature. |
| Multi-user support | Prototype is single-user. Multi-tenancy is Phase 3. |
| Mobile app | Web-only for prototype. Responsive design covers mobile browsers. |

## Data Models (Planned)

```prisma
model User {
  id                  String   @id @default(cuid())
  email               String   @unique
  createdAt           DateTime @default(now())
  updatedAt           DateTime @updatedAt
  wellnessProfile     WellnessProfile?
  consentRecords      ConsentRecord[]
  searchHistory       SearchSession[]
}

model WellnessProfile {
  id                    String   @id @default(cuid())
  userId                String   @unique
  culturalBackground    String?
  neurodivergenceFlags  String?
  communicationPrefs    String
  accessibilityNeeds    String?
  createdAt             DateTime @default(now())
  updatedAt             DateTime @updatedAt
  user                  User     @relation(fields: [userId], references: [id])
}

model Provider {
  id                String   @id @default(cuid())
  name              String
  specialty         String
  acceptsInsurance  Boolean
  insuranceNetworks String?
  location          String
  telehealth        Boolean
  languages         String
  identityAffirming Boolean  @default(false)
  matchCriteria     String
}

model SearchSession {
  id          String   @id @default(cuid())
  userId      String
  supportType String
  insurance   String
  location    String
  cultural    String?
  results     String
  createdAt   DateTime @default(now())
  user        User     @relation(fields: [userId], references: [id])
}

model ConsentRecord {
  id                  String   @id @default(cuid())
  userId              String
  consentChainActionId String
  dataShared          String
  sharedWith          String
  purpose             String
  revokedAt           DateTime?
  createdAt           DateTime @default(now())
  user                User     @relation(fields: [userId], references: [id])
}
```

## API Routes (Planned)

| Route | Method | Purpose | ConsentChain Gate |
|-------|--------|---------|-------------------|
| `/api/profile` | GET | Retrieve wellness profile | Agent validation |
| `/api/profile` | POST | Create/update wellness profile | Agent validation |
| `/api/search/therapist` | POST | Execute therapist search | Agent validation |
| `/api/providers` | GET | List matching providers | Agent validation |
| `/api/schedule` | POST | Simulate scheduling with consent | Full 7-stage pipeline (HIGH risk) |
| `/api/consent` | GET | View consent history | Agent validation |
| `/api/consent/revoke` | POST | Revoke consent | Agent validation + revocation |

## Page Structure (Planned)

```
apps/web/src/app/
  page.tsx                          — Landing / dashboard
  profile/
    page.tsx                        — Wellness profile form
  search/
    page.tsx                        — Care navigation entry
    therapist/
      page.tsx                      — 5-step guided flow
      results/
        page.tsx                    — Provider results
  schedule/
    [providerId]/
      page.tsx                      — Scheduling + consent gate
      confirmation/
        page.tsx                    — Confirmation + next steps
  consent/
    page.tsx                        — Consent history dashboard
```

## Build Phases

### Phase A: Scaffold (Day 1 of Hackathon)

**Objective:** Monorepo scaffold with data models and basic routing.

**File outputs:**
```
package.json
pnpm-workspace.yaml
turbo.json
prisma/schema.prisma
apps/web/src/app/layout.tsx
apps/web/src/app/page.tsx
apps/web/src/lib/prisma.ts
apps/web/src/lib/consent-client.ts  (ConsentChain SDK wrapper)
seed.ts                             (provider seed data — 20 simulated providers)
```

**Acceptance criteria:**
- `pnpm install` succeeds
- `pnpm build` succeeds
- Prisma migration applies cleanly
- Seed script populates 20 providers with varied attributes
- ConsentChain SDK client initializes without error

### Phase B: Profile + Search (Day 1 continued)

**Objective:** Wellness profile CRUD and therapist search flow.

**File outputs:**
```
apps/web/src/app/profile/page.tsx
apps/web/src/app/search/page.tsx
apps/web/src/app/search/therapist/page.tsx
apps/web/src/app/search/therapist/results/page.tsx
apps/web/src/app/api/profile/route.ts
apps/web/src/app/api/search/therapist/route.ts
apps/web/src/app/api/providers/route.ts
apps/web/src/components/StepFlow.tsx
apps/web/src/components/ProviderCard.tsx
apps/web/src/components/CompletionSignal.tsx
```

**Acceptance criteria:**
- User can create wellness profile (4 fields)
- 5-step therapist search flow works end-to-end
- Provider results display with match explanations
- All forms use UICare patterns: one field focus at a time, completion signals, error dignity
- All components under 200 lines

### Phase C: Consent Integration (Day 2 of Hackathon)

**Objective:** ConsentChain gates on data sharing + consent dashboard.

**File outputs:**
```
apps/web/src/app/schedule/[providerId]/page.tsx
apps/web/src/app/schedule/[providerId]/confirmation/page.tsx
apps/web/src/app/consent/page.tsx
apps/web/src/app/api/schedule/route.ts
apps/web/src/app/api/consent/route.ts
apps/web/src/app/api/consent/revoke/route.ts
apps/web/src/components/ConsentGate.tsx
apps/web/src/components/ConsentHistory.tsx
apps/web/src/components/RevokeButton.tsx
```

**Acceptance criteria:**
- Scheduling triggers ConsentChain 7-stage pipeline
- User sees explicit consent prompt: "MADMall will share [specific data] with [provider name]"
- User can approve or deny
- Approved sharing creates ConsentChain ledger entry AND local ConsentRecord
- Consent dashboard shows all records with timestamps
- Revoke button triggers ConsentChain revocation and updates local record
- Revoked consent blocks subsequent data sharing attempts

### Phase D: Polish + Demo Prep (Day 2 continued)

**Objective:** Responsive design, accessibility audit, demo script.

**File outputs:**
```
apps/web/src/app/globals.css         — Tailwind theme with sensory-safe palette
apps/web/src/components/NavSidebar.tsx
apps/web/src/components/AccessibilityToggle.tsx  (high contrast, large text)
DEMO.md                              — Demo script for presentation
```

**Acceptance criteria:**
- All pages responsive (mobile browser usable)
- Keyboard navigation works on all interactive elements
- Focus indicators visible on all focusable elements
- aria-labels on all buttons and form fields
- High contrast mode toggle functional
- Demo script covers full user flow in under 10 minutes
- `pnpm build` exits 0

## Success Definition

MADMall prototype is **Partial** when:
- Wellness profile CRUD works end-to-end
- 5-step therapist search flow produces results
- ConsentChain authorization gate fires on scheduling
- Consent history is visible and revocation works
- UICare patterns are applied to all user-facing screens
- The demo tells a coherent story: "This is what consent-first healthcare looks like"

MADMall prototype is NOT Validated until:
- Clinical advisory review of wellness recommendations
- HIPAA compliance review of data handling
- User research with target population
- Security audit of health data storage
- ConsentChain integration tested under realistic load

## What This Contract Does Not Promise

- This is not a production healthcare platform.
- This is not HIPAA-compliant (requires legal and security review).
- This does not replace professional medical advice.
- Provider data is simulated, not real.
- Scheduling is simulated, not connected to real systems.
- This is a hackathon prototype that demonstrates governance architecture applied to healthcare.

---

V&T Statement
Exists: Pre-build contract with 6 pre-conditions, vertical slice definition (guided care navigation), 5 Prisma models, 7 API routes, 10 pages, 4 build phases with file outputs and acceptance criteria, success definition, honest scope limitations
Non-existent: MADMall codebase, repository, any implementation whatsoever, provider database, ConsentChain SDK completion (dependency), UICare pattern library, clinical advisory input, HIPAA review
Unverified: Hackathon timeline feasibility (4 phases in 2 days), ConsentChain SDK compatibility with planned integration points, Prisma schema adequacy for care navigation flow, provider matching algorithm quality
Functional status: Contract is COMPLETE as a pre-build specification. MADMall itself is PENDING — no code exists. Execution depends on ConsentChain reaching Validated status and hackathon event confirmation.
