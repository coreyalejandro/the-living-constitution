# ARTICLE VI — AUDIENCE LAW

**Status:** Ratified  
**Authority:** THE_LIVING_CONSTITUTION.md — Article VI  
**Load when:** Building UI surfaces or any user-facing feature  
**Tracked here:** docs/governance/audience-contract.md  

---

## The Law

Every user-facing surface built under The Living Constitution must be designed for the Default User first.

See: docs/governance/doctrines/DEFAULT_USER_DOCTRINE.md

The Default User is not the minimum viable user. They are the design target. A system that passes Article VI for the Default User is a system that passes for all users. A system that passes for the neurotypical median and fails for the Default User has failed Article VI.

---

## Audience Contract Requirements

Every UI surface, every instruction set, every user-facing message must meet all of the following before it is considered production-safe:

### 1. Modality Coverage

The surface must provide information in at least two modalities:
- Text (plain language, not jargon-first)
- Structure (numbered steps, tables, or labeled sections — not prose blocks)
- Visual markers where spatial orientation is required (icons, color-coded states, diagrams)

A text-only interface without structure is a single-modality surface. That is not compliant.

### 2. No Skipped Steps

Every instruction sequence must be complete. No implied steps. No "you probably know this." No "etc." No "and so on."

If a step is obvious to a neurotypical user, document it anyway. The cost is one line. The benefit is that the Default User is not excluded.

### 3. Correct Path + Incorrect Path

Every decision point in a user-facing instruction must state:
- What the correct action is
- What the incorrect action is (the most likely mistake)
- What to do if you took the incorrect path

Instructions that only describe the happy path are not compliant.

### 4. Completion Signals

Every action sequence must end with a clear, unambiguous signal that the step is complete:
- "This step is done."
- "You should see X."
- "If you see Y instead, that means Z — do this."

"Did that work?" is not a completion signal. It is an ambiguous state. Do not produce it.

### 5. Recovery Path

Every user-facing action that can fail must include a documented recovery path that is as prominent as the success path. Recovery is not a footnote. It is a first-class instruction.

### 6. No Urgency Framing

No user-facing message may:
- Create artificial urgency
- Frame incomplete work as failure
- Use shame, warning language, or incomplete-task alerts during a legitimate pause
- Imply that the user has broken something when the system is in a recoverable state

### 7. Cognitive Load Awareness

No single screen or instruction block should require the user to hold more than 3-4 distinct pieces of information in working memory simultaneously. If a task requires more than that, it must be broken into sequential steps with confirmation gates between them.

---

## Accessibility Baseline

Every interface must meet WCAG 2.1 AA at minimum. This is the floor, not the ceiling.

Additional requirements for the Default User population:
- Font size: 16px minimum body, 14px minimum secondary
- Line height: 1.5 minimum
- Color contrast: 4.5:1 minimum for all text
- No motion that cannot be disabled
- Focus management: keyboard navigation must work for all primary actions
- No time-limited interactions without a documented extension or pause mechanism

---

## What Violates This Article

| Violation | Description |
|---|---|
| Single-modality surface | Text only, no structure |
| Implied steps | "Configure your environment" with no specification of what that means |
| Happy-path only | Instructions with no error or recovery paths |
| Ambiguous completion | "You're done!" with no verification signal |
| Urgency shaming | "You haven't finished step 3" displayed as a warning during a pause |
| Cognitive overload | 7-item decision trees presented as a single screen |
| Demo states | Placeholder content labeled as real data |

---

## Amendment Process

Any modification to the modality requirements or accessibility baseline requires evidence that the proposed change does not reduce coverage for the Default User. Baseline requirements may only increase.

---

**V&T**  
EXISTS: This article document.  
VERIFIED AGAINST: DEFAULT_USER_DOCTRINE.md. WCAG 2.1 AA (external standard, publicly available).  
NOT CLAIMED: All existing UI surfaces in TLC have been audited against this article.  
FUNCTIONAL STATUS: Ratified governance document. Loaded on demand when building UI surfaces.
