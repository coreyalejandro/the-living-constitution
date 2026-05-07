# ARTICLE VIII — TRUTH MAINTENANCE LAW

**Status:** Ratified  
**Authority:** THE_LIVING_CONSTITUTION.md — Article VIII  
**Load when:** Managing truth claims, status files, documentation, or preparing external publications  
**Tracked here:** docs/governance/truth-maintenance-contract.md  
**Governs:** CALIBRATED_TRUTH_DOCTRINE.md maintenance over time

---

## The Law

Truth is not a one-time act. Truth requires maintenance.

A status that was accurate last week may be inaccurate today. A claim that was CONSTRUCTED last month may be PROVEN today — or may have been falsified. Article VIII governs the ongoing responsibility to keep truth surfaces current, accurate, and appropriately calibrated.

Truth inflation — allowing a CONSTRUCTED claim to remain labeled as PROVEN after the evidence lapses — is as much a violation as original falsification. Systems rot. Evidence ages. This article governs the decay function.

---

## The Truth Surfaces

These are the authoritative truth surfaces in this system. Every one of them must be maintained under this article:

| Surface | What It Claims | Maintenance Frequency |
|---|---|---|
| STATUS.json | Current operational state of the repo | Every significant change |
| MASTER_PROJECT_INVENTORY.json | Current project census | Every project state change |
| research/evidence-ledger.md | What evidence exists and its tier | Every new evidence artifact |
| research/registry/*.json | Current experiment/eval/corpus/proposal state | Every registry event |
| verification/research/*.json | Latest run results and regression state | Every research run |
| V&T Statements | Per-output truth claims | Every substantive output |
| docs/governance/doctrines/ | Doctrine content | When doctrine changes |
| reports/*.md | Research and system reports | After every major run |

---

## Hard Rules

### 1. Status Cannot Drift Forward

A status label may not be promoted without evidence. Moving `partial` to `implemented` without a passing test, a green CI run, or explicit human verification is a truth maintenance violation.

### 2. Status May Drift Backward Without Evidence

If a previously `implemented` surface breaks, its status must be immediately downgraded. Maintaining a stale `implemented` label after a known regression is a truth inflation violation.

### 3. Evidence Timestamps Matter

Every evidence artifact must carry a timestamp. Evidence without a timestamp cannot be used to maintain a truth claim because its freshness cannot be assessed.

### 4. Stale Evidence Is Not Evidence

Evidence older than the last significant system change is stale. Stale evidence may not be used to justify a current truth claim. It must be re-verified or labeled `stale — re-verification required`.

### 5. No Orphaned Claims

Every claim in every published document must trace to a current evidence artifact. A claim without a current evidence trace is an orphaned claim. Orphaned claims must be labeled PENDING or CONSTRUCTED until re-verified.

### 6. V&T Statements Are Not Retroactive

A V&T Statement reflects truth at the time of writing. It does not guarantee that the claim remains true after the session ends. If significant time has passed or significant changes have been made, V&T must be re-issued.

### 7. Release Decisions Require Fresh Truth

Before any release decision (see SOP-014), every truth surface relevant to the release must be verified as current. A release built on stale truth is a release built on false premises.

---

## The Truth Decay Model

Truth claims decay at different rates:

| Claim Type | Decay Rate | Re-verification Trigger |
|---|---|---|
| File exists at path | Slow (until file moves or is deleted) | Any structural refactor |
| Test passes | Medium (until code changes) | Any code change in scope |
| Eval score | Fast (until model or prompt changes) | Any model/prompt change |
| Status label | Medium | Any state-changing operation |
| Research result | Slow (empirical) / Fast (infrastructure) | Infrastructure change or model update |
| Evidence ledger entry | Slow | Change to the artifact it references |

Agents must ask: "When was this last verified? Has anything changed since then that could invalidate it?" If yes or uncertain, re-verify before citing.

---

## What Violates This Article

| Violation | Description |
|---|---|
| Status inflation | `planned` presented as `implemented` |
| Stale status | `implemented` maintained after known regression |
| Orphaned claim | Document asserts X with no current evidence trace |
| Stale evidence citation | Using a 3-month-old eval result to justify current production readiness |
| Missing timestamp | Evidence artifact with no creation date |
| Release on stale truth | Deploying without verifying truth surfaces are current |

---

## Amendment Process

Any modification to the truth surface registry or decay model requires evidence that the proposed change does not reduce the system's ability to detect truth inflation. The list of governed surfaces may only expand.

---

**V&T**  
EXISTS: This article document.  
VERIFIED AGAINST: ~/.claude/CLAUDE.md Articles II and III (Truth-Status Discipline, Verification Before Done). Calibrated Truth Doctrine.  
NOT CLAIMED: All existing status surfaces are currently accurate. An automated truth-staleness detection system exists.  
FUNCTIONAL STATUS: Ratified governance document. Loaded on demand when managing truth claims or documentation.
