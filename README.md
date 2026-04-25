# The Living Constitution

**A research apparatus for testing whether AI interactions can be made governable, contestable, and legible — at the interface, in real time, by the people they affect.**

---

## What this is

The Living Constitution (TLC) is a working prototype that wraps frontier AI systems (Claude, Codex, Gemini) with a runtime governance layer. It exposes the active task agreement, the system's current assumptions, and its truth-status to the user throughout the interaction — and lets the user read, challenge, and repair them in plain language.

It is built to test one specific research question, and to produce instruments other researchers can reuse regardless of what TLC itself shows.

---

## Why this exists

Long-context AI interactions are now the default. A million-token context window is not safer than an eight-thousand-token one if the user cannot tell when the system has silently drifted from the task they originally asked for. Most safety work targets the model. This work targets the *interface between the model and the human* — where intent is declared, drift accumulates, and contestation either happens or fails to happen.

The audiences this is built for, by name:

- AI safety researchers interested in runtime, interactional safety interventions.
- Interpretability researchers looking for an interface-level analog to feature-level work.
- Accessibility researchers and disability-led designers studying neurodivergent users of AI.
- Practitioners building long-context agentic systems who need their users to be able to see what the agent is doing.

---

## The research question

> Do a persistent Contract Window, bilateral intelligibility, and accessibility-grade runtime invariants improve intent fidelity, contestability, and human legibility?

Each term has an operational definition in [PROPOSAL.md](./PROPOSAL.md#d-construct-definitions-operational). They are not metaphors.

---

## The author's claim

I do not believe these interventions will be a clean win on every measure. I think the Contract Window will help most on long sessions and may slow short ones down. I think bilateral intelligibility will improve contestability but may surface assumptions users would rather not have to read. I think accessibility-grade invariants will help lay readers and may frustrate expert users who experience them as friction.

What I am confident about: these are *measurable* claims with *falsifiable* predictions, and the instruments built to test them — the rubric, the contestability funnel, the lay comprehension test — are useful even if every intervention fails. That is the floor. The ceiling is that one or more of them works, and we have a transferable pattern for runtime governance other systems can adopt.

I am autistic and schizophrenic. The Contract Window started as something I needed. The research question is whether other people benefit from it too.

---

## What you'll find in this repo

| Item | Description | Status |
|---|---|---|
| [`PROPOSAL.md`](./PROPOSAL.md) | Full Anthropic Safety Research Fellow proposal | working |
| [`apps/contract-window/`](./apps/contract-window) | Contract Window reference implementation | prototype |
| [`apps/evidence-observatory/`](./apps/evidence-observatory) | 8-layer evidence pipeline that promotes raw interactions into governed transcripts | working |
| [`experiments/constitutional_eval_runs/constitutional-eval-edgecase-harness-v2-20260423T071801Z/`](./experiments/constitutional_eval_runs/constitutional-eval-edgecase-harness-v2-20260423T071801Z) | Backwards Instructional Design (BID) edgecase harness, first run | in-progress |
| [`schemas/`](./schemas) | Schema set: session state, contracts, invariants, adjudications | working |
| [`docs/vt/`](./docs/vt) | Verification & Truth status reporting spec | working |
| [`benchmarks/`](./benchmarks) | Drift-seeded long-session benchmark (in construction) | in-progress |

---

## How to run it

```bash
# 1. Clone
git clone https://github.com/coreyalejandro/the-living-constitution.git
cd the-living-constitution

# 2. Install (Node 20+, pnpm 9+)
pnpm install

# 3. Set provider keys (at least one)
cp .env.example .env.local
# edit .env.local and set ANTHROPIC_API_KEY (and/or OPENAI_API_KEY, GOOGLE_API_KEY)

# 4. Run the Contract Window dev server
pnpm dev:contract-window

# 5. Open http://localhost:3000
```

**Expected output:** A chat interface with a persistent Contract Window pinned to the right side. Type a task. The Contract Window populates with declared task, system understanding, constraints, and truth-status. Every model output that violates an active invariant is intercepted and flagged.

**Most likely failure:** missing or invalid `ANTHROPIC_API_KEY`. Check `.env.local` and confirm the key is present and not surrounded by quotes.

---

## The research frame (short)

Three hypotheses, each falsifiable:

- **H1.** Persistent Contract Window → ≥25% fewer intent-drift incidents in long sessions.
- **H2.** Bilateral intelligibility → ≥2× rate of successful drift repair by users.
- **H3.** Accessibility-grade invariants → ≥80% lay-reader comprehension of session transcripts (vs. ≤50% baseline).

A fourth construct — **Backwards Instructional Design** — is integrated as an experimental condition rather than a separate hypothesis. See [PROPOSAL.md §F](./PROPOSAL.md#f-experimental-design).

```mermaid
flowchart LR
  U["User"] --> CW["Contract Window"]
  CW --> M["Model"]
  M --> INV["Runtime invariants"]
  INV --> O["Output"]
  O --> U
  M --> EO["Evidence Observatory"]
  CW --> EO
  INV --> EO
  EO --> R["Researcher review"]
```

### Intervention × outcome matrix

| Intervention | Intent fidelity | Contestability | Human legibility |
|---|---|---|---|
| Contract Window | primary | secondary | secondary |
| Bilateral intelligibility | secondary | primary | secondary |
| Accessibility invariants | secondary | secondary | primary |
| Backwards Instructional Design | structural prerequisite | structural prerequisite | structural prerequisite |

---

## Prior work trajectory

- **ClarityAI** — rubric-operationalized scoring; first pattern of "make the standard explicit, then test the system against it." Direct ancestor of the rubric used to score intent fidelity.
- **Instructional Integrity work** — early evaluation of whether AI-generated explanations preserve learner understanding. Direct ancestor of the lay legibility test.
- **MTADF (Misalignment Taxonomy & Automated Detection Framework)** — earlier proposal asking *can misalignment be detected?* The current work asks the next question: *can the interaction environment be redesigned so misalignment is prevented, surfaced earlier, or made contestable?*
- **PROACTIVE** — constitutional AI safety framework with nine principles, six invariants, and the original Contract Window mechanism. The runtime invariants in this repo are descendants of that work.

---

## Anthropic alignment

- **Constitutional AI** (Bai et al., 2022): TLC moves the constitutional surface from training time to runtime, and from internal to interface-visible.
- **Collective Constitutional AI** (Anthropic, 2024): TLC asks whether enforcement of collectively-elicited principles can be made bilaterally legible to the people they protect.
- **Mechanistic interpretability / Scaling Monosemanticity**: TLC is an interface-level analog — surfacing *interactional* features (task contracts, assumptions, truth-status) the way feature-level work surfaces internal model features.
- **Anthropic Fellows Program** scope explicitly includes empirical AI safety, scalable oversight, and AI control. This work is empirical, runs on existing infrastructure, and produces transferable instruments regardless of the result.

---

## V&T (honest status)

**Verified:**
- Contract Window prototype renders persistent state and is addressable across a session.
- Evidence Observatory pipeline produces governed transcripts with span-level traceability.
- BID edgecase harness has produced a first experiment run with logged outputs.
- Schema set validates on the example sessions in `schemas/examples/`.

**Unverified:**
- The three primary hypotheses (H1–H3). The experiment described in `PROPOSAL.md` has not yet been run at the powered sample size.
- The lay comprehension instrument is new and needs its own validation work.
- Inter-rater reliability targets (κ ≥ 0.7) are aspirational until rater training is complete.

**Challenged (where I doubt my own claims):**
- Whether the Contract Window's effect, if any, is structural or merely attentional (does it work because it externalizes state, or because it reminds the user to pay attention?). The single-intervention conditions partially decompose this but residual confound is likely.
- Whether BID is an independent intervention or a prerequisite design discipline for the other three.
- Whether interface friction is a feature for some users and an obstacle for others.

**Functional status:** Prototype-grade. Suitable as a research apparatus. Not suitable as a production safety layer for deployed systems without further hardening.

---

## What to do next

Three options, ranked by depth.

1. **Read** — Start with [`PROPOSAL.md`](./PROPOSAL.md). The construct definitions in §D are the core of the work.
2. **Run** — Follow the *How to run it* section above and put the Contract Window through a 50-turn task. Watch what it surfaces.
3. **Contribute** — The most valuable open contributions right now are: (a) lay-rater pool recruitment for the legibility test, (b) drift-seeding scenarios for the benchmark, (c) replications of the BID harness against other model providers.
