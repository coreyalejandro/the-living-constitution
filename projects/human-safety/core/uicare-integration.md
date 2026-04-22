# UICare Integration
## How UICare Implements Human Safety Under TLC

---

## What UICare Is

UICare is the human safety subsystem of the Commonwealth. It ensures that user interfaces do not create harm through design patterns that ignore neurodivergent needs. UICare detects cognitive overload, monitors absence-over-presence signals, and enforces pacing requirements defined by Article I (Bill of Rights).

**Repository:** `/Users/coreyalejandro/Projects/uicare-system`
**Technology:** Next.js, Kubernetes, Docker, GPT-4o-mini
**Safety domain:** Human Safety (primary), Cognitive Safety (secondary)
**Architecture:** Memory-bank architecture with `brain/` module for cognitive assessment

---

## UICare's Role in the Commonwealth

The Default User doctrine states that all work is designed for the most vulnerable user first. UICare is where this doctrine becomes operational software. While the CLAUDE.md instructions enforce Default User rules for agent behavior (CLI interactions), UICare enforces them for web interfaces.

### What UICare Protects Against

**Cognitive overload from interface complexity:** Interfaces that present too many options, too much information, or too many decision points at once. For a user with ADHD, this causes executive function shutdown. For a user with OCD, this triggers doubt loops across all options.

**Absence-over-presence signal blindness:** Traditional UX design focuses on what is present (buttons, text, alerts). UICare monitors what is absent — the user who stopped interacting, the form that was abandoned, the session that went silent. Absence signals often indicate overwhelm, not disinterest.

**Urgency-driven harm:** Interfaces that create artificial urgency (countdown timers, "limited time" banners, disappearing options) cause direct harm to users with bipolar disorder prone to manic episodes. The urgency can trigger manic decision-making. UICare flags and blocks urgency patterns.

**Inaccessible consent flows:** Consent dialogs that are dense, legalistic, or visually overwhelming. For the Default User, a 12-paragraph consent form is not informed consent — it is a cognitive barrier designed to extract agreement through exhaustion.

---

## Article I Implementation Through UICare

Each right in the Bill of Rights maps to a UICare enforcement mechanism:

### Right to Safety

**UICare implementation:** Cognitive load scoring. Every interface element is assessed for cognitive load contribution. When the cumulative load exceeds the threshold, UICare intervenes:
- Simplifies the interface by hiding non-essential elements.
- Breaks multi-step flows into smaller chunks.
- Adds breathing room (visual whitespace, pacing delays).

**Technology:** GPT-4o-mini processes the interface state and user interaction patterns to produce a cognitive load score. The score informs adaptive interface decisions.

### Right to Accessibility

**UICare implementation:** Multi-modal output. Every piece of information is presented in at least two modalities:
- Text plus visual (diagrams, icons, color coding).
- Sequential plus spatial (numbered steps plus a progress bar).
- Summary plus detail (headline with expandable sections).

**Technology:** The `brain/` module maintains a user model that tracks which modalities the user engages with most, adapting future presentations accordingly.

### Right to Dignity

**UICare implementation:** No-shame interaction patterns.
- Incomplete forms are saved, not lost. The user can return without starting over.
- Error messages explain what happened and how to fix it, never blame the user.
- No "are you sure?" confirmations that imply the user made a mistake. Instead: "Here is what will happen. Continue?"
- Session recovery mirrors SOP-013: when the user disengages, their state is preserved. When they return, they resume from where they left off.

### Right to Clarity

**UICare implementation:** Plain language enforcement. Every piece of user-facing text is evaluated for:
- Reading level (target: 8th grade or below for primary content).
- Jargon density (technical terms are defined inline or on hover).
- Sentence length (no sentences over 25 words for critical instructions).

### Right to Truth

**UICare implementation:** Status honesty in interfaces. If a feature is not ready, the interface says so. If a process is still running, the interface shows a real progress indicator (not a fake progress bar that moves regardless of actual progress). If an error occurred, the interface reports it clearly — it does not show a spinner forever.

---

## The Memory-Bank Architecture

UICare's `brain/` module uses a memory-bank pattern to maintain context across interactions:

```
brain/
├── short-term/       User's current session state
│                     What they have seen, what they have done,
│                     what their current cognitive load is
│
├── working-memory/   Active task context
│                     What the user is trying to accomplish,
│                     where they are in the flow,
│                     what decisions they have made
│
├── long-term/        Persistent user preferences
│                     Which modalities they prefer,
│                     what their typical session length is,
│                     what triggers overwhelm
│
└── episodic/         Interaction history
                      Past sessions, past completions,
                      past points of overwhelm
```

The memory-bank architecture allows UICare to detect patterns across sessions. If a user consistently abandons a particular flow at the same point, UICare can proactively simplify that flow or offer an alternative path.

---

## UICare's Relationship to Other Subsystems

### UICare and ConsentChain

UICare renders the consent interfaces that ConsentChain's Stage 4 (Consent) requires. When ConsentChain needs user consent for an agent action, UICare presents the consent flow in a format that respects the Default User doctrine:
- One decision at a time.
- Clear description of what will happen.
- No legalistic language.
- Easy to decline without penalty.

### UICare and SentinelOS

SentinelOS invariant I6 (no output may violate Article I rights) is implemented at the interface level by UICare. When SentinelOS detects a rights violation in an interface element, UICare is responsible for remediation — modifying or removing the offending element.

### UICare and PROACTIVE

PROACTIVE validates UICare's claims about accessibility and cognitive load compliance in CI. If UICare's documentation claims "all interfaces meet 8th-grade reading level" but a new page has not been tested, PROACTIVE flags the discrepancy.

---

## Deployment Architecture

| Component | Technology | Purpose |
|-----------|------------|---------|
| Frontend | Next.js | User-facing interface rendering |
| Cognitive engine | GPT-4o-mini API | Cognitive load assessment and adaptive decisions |
| Brain module | Custom Node.js | Memory-bank state management |
| Container | Docker | Application packaging |
| Orchestration | Kubernetes | Deployment, scaling, health checks |
| Persistence | Pending — database selection not finalized | Long-term memory storage |

The Kubernetes deployment provides health checks that detect when the cognitive engine is unresponsive. If GPT-4o-mini is unavailable, UICare falls back to rule-based cognitive load assessment (heuristic scoring) rather than degrading silently. The fallback is less accurate but maintains the safety guarantee.

---

## V&T Statement
- **Exists:** UICare integration document describing human safety implementation for all five Article I rights; memory-bank architecture diagram; relationship mapping to ConsentChain, SentinelOS, and PROACTIVE; deployment architecture table; absence-over-presence signal monitoring description
- **Non-existent:** Automated cognitive load scoring with validated thresholds; plain language enforcement tooling; real-time absence signal detection; database persistence for long-term memory bank
- **Unverified:** Whether the brain/ module currently implements the memory-bank architecture as described; whether GPT-4o-mini integration is currently functional; whether Kubernetes deployment files are current
- **Functional status:** UICare is partial — Next.js frontend, Docker containers, and GPT-4o-mini integration exist; cognitive load scoring, absence signal detection, and memory-bank persistence are not yet wired end-to-end
