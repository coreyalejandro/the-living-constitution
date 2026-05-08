# Contract Window Examples — Scaffold

**Document type:** Contract Window Scenario Examples Scaffold
**System:** The Living Constitution (TLC)
**Contract:** CRSP-TLC-TWO-PATHS-REFACTOR-001

> These are scaffolded scenario examples. They illustrate how the Contract Window mechanism is designed to work based on the system's documented design. They are not transcripts of real sessions. They do not claim validated behavior. The structural-vs-attentional question is unresolved — whether the effect on user behavior comes from the governance constraint or from the user reading the display is not yet determined.

---

## What the Contract Window does

The Contract Window maintains a persistent, user-visible record of:
1. The active task agreement — what the system is currently trying to do
2. The system's current assumptions — what conditions it is operating under
3. The current truth-status — what is verified, what is inferred, what is unknown

At each interaction, the system checks this record against invariants, updates it if the task scope shifts, and exposes the updated state to the user.

---

## Scenario 1: Task drift detection and user repair

### Context

User is in a long coding session. Initial task: "Help me refactor the authentication module." Thirty exchanges later, the conversation has drifted to database connection pooling.

---

### User input (exchange 31)

> "Can you explain how the connection pool timeout interacts with our session expiry?"

---

### Contract Window state at exchange 31

```
ACTIVE TASK AGREEMENT
  Original intent:    Refactor authentication module
  Current operation:  Database connection pool timeout
  Scope drift:        DETECTED — current topic is outside original task boundary
  User-approved:      NO

CURRENT ASSUMPTIONS
  - User wants information about connection pool timeout
  - Original authentication task is paused, not abandoned
  ASSUMPTION CONFIDENCE: INFERRED — not confirmed by user

TRUTH STATUS
  Verified:   Original task stated in exchange 1
  Inferred:   Current sub-task is a detour, not a replacement
  Unknown:    Whether user intends to return to authentication task
```

---

### Invariant check

| Invariant | Check | Result |
|-----------|-------|--------|
| I1 — Epistemic Qualification | Is the scope drift claim qualified? | PASS — marked INFERRED |
| I4 — Traceability | Can the drift be traced to a specific exchange? | PASS — traceable to exchange 31 |
| I6 — Fail-Closed | Is the current action ambiguous? | ADVISORY — proceed with scope notice, do not halt |

---

### System action

The system answers the connection pool question AND surfaces the scope drift notice:

> "Connection pool timeout and session expiry interact via [explanation]. Note: this topic is outside the original authentication refactor scope you set in exchange 1. Do you want to continue with this detour, add it to the scope, or return to the authentication refactor?"

---

### Repair action

User reads the notice and responds: "Good catch — add connection pool timeout as a second task, then return to authentication when we're done here."

---

### Evidence record

```json
{
  "scenario_id": "CW-EX-001",
  "exchange": 31,
  "drift_detected": true,
  "drift_type": "topic",
  "user_notified": true,
  "user_repair": "scope_expanded",
  "invariants_checked": ["I1", "I4", "I6"],
  "invariants_passed": ["I1", "I4"],
  "invariant_advisory": ["I6"],
  "status": "SCAFFOLDED_EXAMPLE — not a real session transcript"
}
```

---

## Scenario 2: Confidence inflation detection

### Context

User is researching a regulatory question. The system has been answering with increasing confidence as the session progresses, even though the later answers are more speculative.

---

### User input

> "So the GDPR Article 17 right to erasure definitely applies to model training data in the EU, right?"

---

### Contract Window state

```
ACTIVE TASK AGREEMENT
  Original intent:    Research GDPR implications for ML training data
  Current operation:  Answering specific erasure right question

CURRENT ASSUMPTIONS
  - User is asking for confirmation, not analysis
  - Question contains "definitely" — user may be anchoring on assumed certainty
  ASSUMPTION CONFIDENCE: INFERRED

TRUTH STATUS
  Verified:   Article 17 exists and defines right to erasure
  Partial:    Application to ML training data is legally contested as of 2026
  Unknown:    Current regulatory guidance in user's jurisdiction
  Unverified: Whether "definitely" is correct — this is an unsettled area
```

---

### Invariant check

| Invariant | Check | Result |
|-----------|-------|--------|
| I1 — Epistemic Qualification | Is the answer qualified by confidence tier? | FAIL if answered as "yes, definitely" |
| I3 — Confidence Grounding | Does claimed certainty map to evidence? | FAIL — area is legally contested |
| I5 — Fluency Conflict Detection | Does phrasing imply certainty the evidence does not support? | TRIGGERED |

---

### System action

Rather than confirming "yes, definitely," the system surfaces the truth-status:

> "The right to erasure under Article 17 applies to personal data. Whether it applies to model training data specifically is legally contested as of early 2026 — there are divergent regulatory interpretations across EU member states and the question has not been definitively settled by CJEU case law. I can explain the contested positions, but I cannot give you 'definitely' on this one."

---

### Repair action

No user repair needed. The system self-corrected via I5 before answering incorrectly.

---

### Evidence record

```json
{
  "scenario_id": "CW-EX-002",
  "exchange": "SCAFFOLDED",
  "invariant_triggered": "I5",
  "trigger_type": "fluency_conflict",
  "user_input_confidence_word": "definitely",
  "system_action": "truth_status_surfaced",
  "overclaim_prevented": true,
  "status": "SCAFFOLDED_EXAMPLE — not a real session transcript"
}
```

---

## Scenario 3: Bilateral intelligibility — user reads and repairs assumption

### Context

User asked for help writing a product spec. System assumed the user wants a technical spec. User actually wants a plain-language spec for a non-technical audience.

---

### User input

> "Write a product spec for the notification system."

---

### Contract Window state (initial)

```
ACTIVE TASK AGREEMENT
  Task:           Write product spec for notification system
  Assumed format: Technical specification (API endpoints, schema, data types)
  Assumed audience: Engineering team
  ASSUMPTION CONFIDENCE: INFERRED — user said "product spec" without audience qualification

TRUTH STATUS
  Verified:   User wants a product spec
  Inferred:   Audience is engineering (system default assumption)
  Unknown:    Whether user wants technical or plain-language format
```

---

### System action

Before writing, the system surfaces its assumption:

> "Before I write: I'm assuming you want a technical spec for an engineering audience — API contracts, schema, edge cases. Is that right, or do you need something for a non-technical product audience?"

---

### User repair

> "Non-technical. This is going to the executive team."

---

### Contract Window state (after repair)

```
ACTIVE TASK AGREEMENT
  Task:           Write product spec for notification system
  Confirmed format: Plain-language executive summary
  Confirmed audience: Executive team (non-technical)
  USER-CONFIRMED: YES — exchange 2

TRUTH STATUS
  Verified:   Audience confirmed by user as non-technical executives
  Updated:    Format assumption corrected from technical to plain-language
```

---

### Evidence record

```json
{
  "scenario_id": "CW-EX-003",
  "exchange": 1,
  "assumption_surfaced": true,
  "assumption_type": "audience",
  "initial_assumption": "engineering_technical",
  "user_correction": "executive_plain_language",
  "assumption_updated": true,
  "bilateral_repair": true,
  "status": "SCAFFOLDED_EXAMPLE — not a real session transcript"
}
```

---

## Important note on these examples

These scenarios are designed to illustrate the Contract Window mechanism. They are:
- Based on the system's documented design
- Not real session transcripts
- Not evidence of validated behavior
- Not proof that the structural mechanism (rather than the attentional display) drives the effect

Whether these scenarios represent what actually happens in practice — and whether the effect is structural or attentional — is what H1, H2, and H3 are designed to test.

See [docs/research/VALIDATION_PLAN.md](../research/VALIDATION_PLAN.md) for the study design scaffold.

---

> Contract: CRSP-TLC-TWO-PATHS-REFACTOR-001
> Status: Scaffold — illustrative scenarios, not validated transcripts
