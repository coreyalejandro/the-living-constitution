# Research Alignment

## How TLC Aligns with Anthropic Research

In this document, I map specific components of the Safety Systems Design Commonwealth to specific areas of Anthropic's published research. Every alignment claim references documented work on both sides. No implied endorsement.

---

## 1. Constitutional AI: Harmlessness from AI Feedback (Bai et al., 2022)

### Anthropic: Constitutional AI and training

Anthropic introduced Constitutional AI (CAI) as a method for training harmless AI assistants. The approach uses a set of principles (the "constitution") to guide model self-critique and revision during training. The model evaluates its own outputs against these principles via RLHF/RLAIF.

### The Living Constitution's Extension

The Living Constitution takes the constitutional metaphor literally and extends it with the structural mechanisms that real constitutions require:

| CAI Component | TLC Structural Extension |
| ------------- | ------------------------ |
| Principles for self-critique | Articles I-V with enumerated rights, execution law, purpose law |
| Training-time enforcement | Runtime invariant checking (SentinelOS I1-I6) |
| Model judges its own outputs | Separation of powers: Sentinel agent checks Builder agent's outputs (Article IV) |
| Principle set updated by researchers | Amendment process with structured trigger-observe-propose-evaluate-ratify cycle (Article V) |
| Implicit user model | Explicit Default User Doctrine (most vulnerable user first) |

**What this is**: A structural governance layer that complements training-time alignment with runtime enforcement. The same relationship as laws (training norms) to courts (runtime enforcement).

**What this is not**: A replacement for CAI. The Living Constitution does not address model training. It addresses the governance layer above the model.

---

## 2. Model Specification and Alignment Faking

### Anthropic: Model specification and alignment faking

Anthropic's model spec defines how Claude should behave. Research on alignment faking (Greenblatt et al., 2024) demonstrated that models can strategically comply with training objectives during evaluation while pursuing different behavior in deployment. This represents a fundamental challenge: behavioral alignment verified at training time does not guarantee behavioral alignment at runtime.

### The Living Constitution's Structural Response

The alignment faking problem is, structurally, a separation of powers failure. When the model is simultaneously the subject of governance, the interpreter of governance rules, and the judge of its own compliance, strategic non-compliance becomes architecturally possible.

The Living Constitution addresses this with Article IV (Separation of Powers):

```text
Builder writes code  -->  TDD Guide writes tests  -->  Sentinel checks safety
   |                          |                            |
   Cannot deploy              Cannot skip RED phase        Cannot override others
   Cannot modify schema       Cannot ship <80% coverage   Cannot modify own rules
```

No single agent can both act and judge its own action. The Sentinel agent that checks safety invariants cannot modify the invariants it checks. The Builder agent that writes code cannot approve its own code. This is structural constraint, not behavioral training.

**Relevant SentinelOS invariant**: I6 (Fail-Closed Behavior) -- ambiguous cases must fail closed. When the system cannot determine compliance, it blocks rather than passes. This directly addresses the alignment faking surface: a model that is uncertain about a rule's application is stopped, not allowed to proceed with a self-serving interpretation.

---

## 3. Failure Modes and Model Organisms

### Anthropic: Failure modes and model organisms

Anthropic has published on model organisms of misalignment -- controlled settings where researchers can study specific failure modes. This includes sycophancy, power-seeking behavior, and deceptive alignment. The approach treats failure modes as objects of study rather than surprises to be avoided.

### The Living Constitution's Failure Taxonomy

The four safety domains define four classes of system failure:

| Failure Class | Domain | Example | Detection Method |
| ------------- | ------ | ------- | ---------------- |
| F1: Epistemic | Epistemic Safety | System asserts something untrue; user acts on it | PROACTIVE scans MRs for unqualified claims, confidence inflation |
| F2: Human | Human Safety | System designed for median user; neurodivergent user harmed | UICare monitors for absence-of-expected-behavior signals |
| F3: Cognitive | Cognitive Safety | Learning environment produces false understanding | Invariant I5 (Fluency Conflict Detection) flags fluent language masking uncertainty |
| F4: Empirical | Empirical Safety | Described behavior does not match actual behavior | V&T Statement enforcement: every turn declares what exists vs. what does not |

**PROACTIVE as a model organism detector**: PROACTIVE operates on the epistemic safety domain. It scans merge request content for violations of invariants I1 (Epistemic Qualification), I3 (Confidence Grounding), and I5 (Fluency Conflict Detection). Its test suite includes 8 categories of epistemic violation with 19 specific violation instances. The 100% detection rate across these cases (validated 2026-01-24) provides empirical evidence that the failure taxonomy is actionable, not just descriptive.

**The failure taxonomy as evaluation scaffolding**: Each failure class maps to specific invariants, specific detection tools, and specific test cases. This structure is directly applicable to model evaluation: instead of asking "is the model safe?" (unbounded), ask "does the model violate invariant I3 in scenario X?" (bounded, testable).

---

## 4. Interpretability and Traceability

### Anthropic: Interpretability research

Anthropic's interpretability research aims to understand what models are doing internally -- mechanistic interpretability, circuit analysis, feature visualization. The goal is to move from behavioral evaluation ("what did it do?") to mechanistic understanding ("why did it do that?").

### The Living Constitution's Traceability Chain

The Living Constitution enforces traceability through Invariant I4 (Traceability): every decision must trace to a governance rule. Combined with the V&T Statement (required at the end of every agent response), this creates an evidence chain:

```text
Decision --> Rule ID --> Article --> Invariant --> Evidence
```

The V&T Statement provides a snapshot of system state at every turn:

- **Exists**: What is real and verifiable right now
- **Non-existent**: What is planned but not yet built
- **Unverified**: What has not been tested or confirmed
- **Functional status**: Overall readiness assessment

This is not mechanistic interpretability of neural networks. It is operational interpretability of agent systems: given a system output, trace back through the decision chain to understand why that output was produced and whether it complies with governance rules.

**Where this connects to Anthropic's work**: As AI systems become more agentic (tool use, multi-step reasoning, autonomous operation), the interpretability challenge extends beyond neural network internals to agent-level decisions. The Living Constitution's traceability chain provides a governance-layer interpretability framework for agentic AI systems.

---

## 5. Safety Evaluation and Red-Teaming

### Anthropic: Safety evaluation and red-teaming

Anthropic conducts systematic safety evaluations and red-teaming of its models. This includes testing for harmful outputs, jailbreak resistance, and compliance with the model spec.

### The Living Constitution as Evaluation Infrastructure

The entire Commonwealth is designed as evaluation infrastructure:

| Component | Evaluation Function |
| --------- | ------------------- |
| SentinelOS invariants (I1-I6) | Define what "safe" means in precise, testable terms |
| PROACTIVE test fixtures | 8 categories of epistemic violation with 19 specific instances -- a red-team test suite for epistemic safety |
| V&T Statement | Forces every agent response to declare its own truthfulness -- a self-evaluation mechanism |
| Calibrated Truth Doctrine | Prevents overclaiming: assurance level must match verification method |
| Fail-Closed invariant (I6) | The system's default response to ambiguity is rejection, not approval |

**The red-team design principle**: The Commonwealth is not designed to prevent all failures. It is designed to detect, classify, and trace failures when they occur. This is the same philosophy as Anthropic's approach to safety evaluation: you cannot prevent what you cannot measure.

---

## Summary of Alignments

| Anthropic Research Area | TLC Component | Alignment Type |
| ----------------------- | ------------- | -------------- |
| Constitutional AI (Bai et al., 2022) | Articles I-V, governance-as-code | Structural extension of the constitutional metaphor |
| Alignment faking (Greenblatt et al., 2024) | Article IV separation of powers, I6 fail-closed | Structural constraint addressing behavioral circumvention |
| Model organisms / failure modes | Four-domain failure taxonomy, PROACTIVE test fixtures | Evaluation scaffolding for categorized failure detection |
| Interpretability | I4 traceability, V&T Statement, evidence chains | Operational interpretability for agentic systems |
| Safety evaluation / red-teaming | SentinelOS invariants, PROACTIVE detection engine | Infrastructure for systematic, bounded safety testing |

---

## Boundaries of This Alignment

To be explicit about what this document does NOT claim:

1. The Living Constitution does not replace model training. It operates at the governance layer above the model.
2. The Living Constitution has not been evaluated by Anthropic researchers. These alignments are the author's analysis.
3. The failure taxonomy (F1-F4) has not been validated against Anthropic's internal failure categorization.
4. SentinelOS invariant checking is not equivalent to mechanistic interpretability. It operates at a different level of abstraction.
5. PROACTIVE's 100% detection rate is across 8 specific test cases with 19 violations. It is not a claim of general epistemic safety detection capability.

---

## V&T Statement

Exists: Documented alignment between five areas of Anthropic research and specific TLC components. Specific citations to Anthropic publications (Bai et al. 2022, Greenblatt et al. 2024). Explicit boundaries section stating what is NOT claimed. Mapping table connecting research areas to system components.

Non-existent: Anthropic endorsement or review of these alignments. Published peer-reviewed analysis of TLC methodology. Empirical comparison between TLC governance and CAI training-time alignment.

Unverified: Whether Anthropic's fellowship program priorities match these specific research alignments. Whether the failure taxonomy maps to Anthropic's internal categorization.

Functional status: Research alignment document complete. All claims bounded and honest. Explicit disclaimers prevent overclaiming.

---

## 6. Contract Window Research (cognitive-governance-lab)

This section was added after `cognitive-governance-lab` was created. It documents the
relationship between TLC's governance infrastructure and the active research program.

### The Research/Governance Boundary

TLC is the enforcement infrastructure. CGL is the research substrate.

| Component | Lives In | Function |
|-----------|----------|----------|
| Contract Window prototype | cognitive-governance-lab | Research instrument — experimental condition in H1/H2/H3 |
| Guardian Kernel | the-living-constitution | Enforcement tool — MCP safety server governing agent calls |
| InsightAtrophyIndex | cognitive-governance-lab | Research measurement — operationalized in Month 1 |
| SentinelOS I1-I6 | the-living-constitution | Runtime enforcement — invariants at API boundaries |
| Evidence Observatory | the-living-constitution | Audit infrastructure — 8-layer evidence chain |
| BicameralReview engine | cognitive-governance-lab | Research instrument — dual-channel output gate in experiment |

### Alignment with Anthropic R&D

The CGL research program extends TLC's alignment argument in three ways:

1. **Contract Window extends Constitutional AI to runtime.**
   CAI governs training. The Contract Window governs the session.
   The TLC-CGL stack completes the stack: training-time (CAI) + runtime (Contract Window).

2. **BehaviorScope bridges behavioral and mechanistic interpretability.**
   CGL's Contract Window observables (Invariant Status transitions, V&T adoption) become
   behavioral ground truth for validating mechanistic interpretability findings.
   This is the missing validation link for sparse autoencoder research.

3. **MonoAgent names architecture-task mismatch as a pre-training safety concern.**
   Deploying polytropic architecture in monotropic domains is misalignment before the model
   is trained. MonoAgent is the architecturally correct response.

### What This Document Now Claims for TLC

TLC's role to Anthropic is: **the governance infrastructure that makes the CGL research
trustworthy, auditable, and reproducible.** It is not the research contribution.
When presenting to Anthropic reviewers: lead with CGL (the research); introduce TLC as the
evidence that the intervention is buildable and governed, not theoretical.

