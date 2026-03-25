# UICare Integration into The Living Constitution

## How UICare Fits as TLC's Human Safety Subsystem

---

## 1. Domain Mapping

The Living Constitution governs four safety domains. UICare is the primary product in the Human Safety domain.

| Domain | Primary Product | Secondary Products |
|--------|----------------|-------------------|
| Epistemic Safety | PROACTIVE | SentinelOS truth-status |
| Human Safety | **UICare** | SentinelOS accessibility layer |
| Cognitive Safety | (shared) | PROACTIVE drift detection, UICare tutorials |
| Empirical Safety | SentinelOS | PROACTIVE validation evidence |

### UICare's Domain Definition

**Human Safety:** A system designed around the median user harms anyone outside that median. UICare exists because behavior-monitoring systems capture what users do (clicks, keystrokes, time-on-task) but miss what they stop doing. For neurodivergent users, the absence of expected behavior is the signal, not the presence of abnormal behavior.

### Constitutional Invariants UICare Enforces

| Invariant | How UICare Enforces It |
|-----------|----------------------|
| I1 (Evidence-First) | Behavioral baselines require evidence -- the Quintessential Sign-Off is the user-authenticated evidence that "this is normal for me" |
| I4 (Traceability) | Every intervention is logged with trigger reason, agent ID, timestamp, and outcome |
| I5 (Safety Over Fluency) | UICare intervenes even when the user says they are fine, because denial is a predictable response for people on the spectrum or in high-intensity states |

---

## 2. Architectural Position in the Commonwealth

```
THE LIVING CONSTITUTION
  |
  +-- SentinelOS (AI Safety Operating Layer)
  |     |
  |     +-- Truth-Status Registry
  |     +-- Build Lattice (CI/CD governance)
  |     +-- Agent Orchestration
  |     |
  |     +-- PROACTIVE (Epistemic Safety)
  |     |     Enforces: I1, I2, I3, I4, I5, I6
  |     |     Scope: AI output validation
  |     |
  |     +-- UICare (Human Safety)    <-- THIS
  |     |     Enforces: I1, I4, I5
  |     |     Scope: User behavioral safety
  |     |
  |     +-- ConsentChain (Empirical Safety)
  |           Enforces: I1, I4
  |           Scope: Consent and data governance
  |
  +-- Creative Chaos (Design System)
        Visual identity across all products
```

### UICare's Unique Position

UICare is the only product in the Commonwealth that faces the end user directly in a non-development context. PROACTIVE reviews code. SentinelOS governs infrastructure. ConsentChain manages data. UICare sits with the person. It is the confidante -- the Shakespearean character who sees the protagonist more clearly than they see themselves.

This means UICare carries the highest human-safety burden. A false negative (failing to detect distress) can mean a person in crisis receives no intervention. A false positive (incorrectly flagging distress) can erode trust and trigger the user to disable the system. The Quintessential Sign-Off protocol exists to calibrate this balance: the user defines what "normal" looks like, and only deviations from that authenticated baseline trigger intervention.

---

## 3. Data Flow Between UICare and Other Commonwealth Products

### UICare -> PROACTIVE

UICare's behavioral deviation scores can feed into PROACTIVE's validation pipeline as contextual signals:

```
UICare MonitorAgent detects:
  Developer in edit-revert loop for 45 minutes
  Commit frequency dropped from 8/day to 1/day
  Code review comments changed from constructive to terse

PROACTIVE receives:
  Context: "Developer behavioral deviation score: 0.82"
  Action: Adjust review strictness (more lenient during crisis)
  Log: "I4 trace: behavioral context from UICare MonitorAgent"
```

This is a planned integration, not a current implementation.

### PROACTIVE -> UICare

PROACTIVE's epistemic checks can validate UICare's own claims:

```
UICare claims: "Mania risk score: 0.3 (low)"
PROACTIVE checks: "Is this claim evidence-backed?"
  - Wearable data source: mock (random) -> I2 violation (phantom evidence)
  - Baseline samples: 2 (insufficient) -> I3 violation (low confidence)
Result: UICare's risk assessment is flagged as under-evidenced
```

This cross-product validation is the Commonwealth's check-and-balance system applied to safety products themselves.

### UICare -> SentinelOS

UICare reports its truth-status to SentinelOS's registry:

```yaml
uicare:
  status: partial
  evidence:
    - agent-definition.yaml (MonitorAgent, RescueAgent)
    - web application (MoodRING, reality filters)
    - docker-compose.yml (containerization)
  missing:
    - quintessential-sign-off (planned)
    - reading-the-room-engine (planned)
    - real-wearable-integration (placeholder)
```

---

## 4. Shared Infrastructure

### Design System (Creative Chaos)

UICare's web application uses design tokens from the Creative Chaos design system:
- `colors.ts` -- danger/warning/success for crisis states
- `typography.ts` -- h1-h6 scale for accessibility
- `spacing.ts` -- consistent padding/margins
- `breakpoints.ts` -- responsive design targets

When Creative Chaos matures, UICare should consume tokens from the shared package rather than maintaining local copies.

### Agent Orchestration (SentinelOS)

UICare's MonitorAgent and RescueAgent are currently self-contained. Under SentinelOS orchestration:
- Agent registration in a central agent registry
- Health checks and heartbeat monitoring
- Cross-agent communication (MonitorAgent -> PROACTIVE Sentinel for epistemic validation)
- Shared logging format and audit trail

### Build Governance (SentinelOS Build Lattice)

UICare should publish a BUILD_CONTRACT.md that satisfies SentinelOS build lattice requirements:
- Declared dependencies with version pins
- Test coverage threshold (80%)
- Accessibility compliance level (WCAG 2.1 AA)
- Agent model declarations with cost tracking

---

## 5. Integration Tasks (Sequenced)

| Priority | Task | Depends On | Effort |
|----------|------|-----------|--------|
| 1 | Register UICare in SentinelOS truth-status config | SentinelOS config file exists | 15 min |
| 2 | Align UICare design tokens with Creative Chaos | Creative Chaos package published | 30 min |
| 3 | Implement I4 traceability in agent interventions | UICare hardening complete | 60 min |
| 4 | Cross-validate UICare risk scores via PROACTIVE | PROACTIVE pipeline wired | 90 min |
| 5 | Register agents in SentinelOS agent registry | Registry specification exists | 45 min |
| 6 | Build UICare status dashboard for SentinelOS | SentinelOS dashboard framework | 120 min |

---

## 6. The Default User Connection

UICare is the product most directly shaped by the Default User profile from the Constitution:

| Default User Trait | UICare Feature |
|-------------------|----------------|
| Autism (explicit instructions) | Quintessential Sign-Off: user explicitly defines baseline |
| Bipolar I (manic episodes) | Mania monitoring with wearable sensor integration |
| ADHD (limited working memory) | Loop detection catches edit-revert cycles |
| OCD (doubt loops) | RescueAgent provides clear 3-step interventions |
| Trauma survivor (dignity) | Confidante model: never punitive, always precise |
| High capacity, poor spatial reasoning | MoodRING reality filters reduce visual noise |

Every feature in UICare maps to a constitutional requirement. The system was not designed for a generic user and then adapted. It was designed for the hardest case first.

---

## 7. Long-Term Vision: Reading the Room

The core innovation -- absence-over-presence behavioral detection -- positions UICare uniquely in the Commonwealth:

**Current state:** Text loop detection via AI agent
**Next state:** Multi-signal behavioral analysis (code patterns, interaction frequency, communication tone)
**Target state:** Environmental sensing -- cameras and sensors that capture what a person is NOT doing

This progression from text to behavior to environment tracks the Constitutional principle of ascending the Calibrated Truth Doctrine's assurance ladder:
- Tier 1 (Current): Agent says "loop detected" based on text analysis
- Tier 2 (Next): Machine verifies behavioral deviation against quantified baseline
- Tier 3 (Aspiration): Formal proof that intervention criteria are met given sensor inputs

---

## V&T Statement

**Exists:** This integration document mapping UICare to the Human Safety domain, identifying constitutional invariant enforcement (I1, I4, I5), cross-product data flows with PROACTIVE and SentinelOS, shared infrastructure dependencies, 6 sequenced integration tasks, Default User trait-to-feature mapping, and long-term vision alignment with Calibrated Truth Doctrine

**Non-existent:** Cross-product data flows (planned, not implemented), SentinelOS agent registry, Creative Chaos shared design tokens, PROACTIVE-UICare cross-validation, SentinelOS UICare status dashboard

**Unverified:** Whether current UICare codebase satisfies I4 traceability (agent interventions are logged but trace chain format not verified), whether Creative Chaos design tokens are compatible with UICare's current token structure

**Functional status:** Partial -- UICare is architecturally positioned as TLC's Human Safety subsystem. The domain mapping, invariant alignment, and integration points are specified. The cross-product integrations are planned but not yet built. UICare operates independently until SentinelOS orchestration layer is ready.
