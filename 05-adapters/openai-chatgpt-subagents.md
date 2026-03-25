# OpenAI / ChatGPT Subagents
## Vendor Adapter Specification for ChatGPT Subagent Integration

---

## Purpose

This document specifies how ChatGPT-based subagents integrate with the Commonwealth as vendor adapters. ChatGPT subagents are one execution option among many. They implement ports defined by SentinelOS core. They never define governance, override the Constitution, or operate outside the consent pipeline.

---

## Architectural Position

ChatGPT subagents are **adapters**, not **core components**. Their position in the Commonwealth:

```
TLC (The Living Constitution)
    │
    ▼
SentinelOS Core (invariants, ports, governance)
    │
    ├── Port: AgentExecutionPort
    │       │
    │       ├── Adapter: Claude Code (primary)
    │       ├── Adapter: ChatGPT Subagent (secondary)
    │       ├── Adapter: Gemini (planned)
    │       └── Adapter: Local LLM (planned)
    │
    └── [Other ports...]
```

The ChatGPT subagent adapter is secondary to the Claude Code adapter. Claude Code is the primary orchestration environment because CLAUDE.md instructions are the current Tier 1 governance enforcement mechanism. ChatGPT subagents operate in contexts where Claude Code is not available or where OpenAI-specific capabilities are needed (vision, DALL-E integration, specific fine-tuned models).

---

## ChatGPT Subagent Adapter Specification

### Input Contract

The ChatGPT subagent adapter accepts a governed action request from the SentinelOS core. The request has already passed through ConsentChain's 7-stage pipeline (validate, authenticate, authorize, consent, rate-limit). The adapter receives a fully authorized, consented action.

### Execution

The adapter translates the governed action into ChatGPT API format:
- Maps the action description to a ChatGPT system prompt and user message.
- Includes constitutional constraints as system-level instructions.
- Sets appropriate model parameters (temperature, max tokens, stop sequences).
- Executes the API call to OpenAI.

### Output Contract

The adapter returns a structured result to the SentinelOS core:
- Success or failure status.
- The ChatGPT response content.
- Token usage for cost tracking.
- Any error messages from the OpenAI API.
- The result is validated against the V&T Statement requirement before returning.

### Constitutional Constraints in System Prompt

When the adapter constructs the ChatGPT system prompt, it includes:

```
You are operating as a subagent within the Safety Systems Design Commonwealth.
You are governed by The Living Constitution. Your output must comply with:

1. Article I: No output may create epistemic, cognitive, human, or empirical harm.
2. Article II: Use immutable patterns. Declare truth-status honestly.
3. Article III: Every output traces to a purpose. Do not produce filler.
4. V&T Statement: End every response with Exists / Non-existent / Unverified / Functional status.

You are an adapter. You execute governed actions. You do not define governance.
```

These constraints are injected by the adapter, not authored by the ChatGPT model. The model may not understand the Constitution natively — the adapter compensates by encoding constraints as system-level instructions and post-processing the output for compliance.

---

## What ChatGPT Subagents Can and Cannot Do

### Can Do

- Execute governed actions that have passed through the ConsentChain pipeline.
- Generate text, code, and analysis within constitutional constraints.
- Leverage OpenAI-specific capabilities (vision, image generation) when the action requires them.
- Process inputs in formats that Claude Code does not natively support, if such cases arise.
- Provide a secondary execution path for redundancy or comparison.

### Cannot Do

- Override TLC governance rules, even if the OpenAI model's training suggests a different approach.
- Bypass ConsentChain's 7-stage pipeline. Every action must be authorized and consented before reaching the adapter.
- Modify SentinelOS invariants or port definitions.
- Access production secrets, PII, or sensitive data without explicit authorization through the consent pipeline.
- Self-select for execution. The orchestration cortex (Claude Code) decides when to dispatch to the ChatGPT adapter. The adapter does not self-invoke.
- Communicate directly with the human user. All outputs flow back through the orchestration cortex for V&T validation and ND access filtering.

---

## UICare's Use of GPT-4o-mini

UICare currently uses GPT-4o-mini for cognitive load assessment. This is a specific instance of the ChatGPT subagent adapter pattern:

| Aspect | UICare GPT-4o-mini Usage |
|--------|-------------------------|
| Port | CognitiveLoadPort |
| Adapter | GPT-4o-mini adapter in UICare brain/ module |
| Input | Interface state + user interaction pattern |
| Output | Cognitive load score (1-5 scale) + recommended pacing |
| Fallback | Rule-based heuristic scoring if API unavailable |
| Governance | Score is advisory — UICare makes the final UI decision, not the model |

The key governance rule: GPT-4o-mini provides a score. UICare's cognitive engine makes the interface decision. The model is an input, not an authority. This prevents the vendor model from having ungoverned influence over user-facing behavior.

---

## Cost and Performance Considerations

| Model | Cost Profile | Use Case |
|-------|-------------|----------|
| GPT-4o-mini | Low cost, fast inference | Cognitive load scoring, lightweight classification |
| GPT-4o | Medium cost, high capability | Complex analysis where Claude Code is unavailable |
| GPT-4-turbo | Higher cost, large context | Large document processing (if needed) |

The adapter tracks token usage and cost per invocation. If costs exceed configured thresholds, the adapter raises a rate-limit signal to the orchestration cortex rather than silently accumulating charges.

---

## Vendor Lock-In Prevention

The adapter pattern explicitly prevents vendor lock-in:

1. **No OpenAI-specific types in the core.** All types are defined by ports. The adapter maps to and from port types.
2. **No OpenAI-specific configuration in governance rules.** Temperature, model selection, and API parameters are adapter configuration, not constitutional parameters.
3. **Contract test equivalence.** If the ChatGPT adapter passes the AgentExecutionPort contract tests, any other adapter that also passes those tests is a drop-in replacement.
4. **Fallback paths exist.** If OpenAI is unavailable, the system degrades to other adapters (Claude Code, local models) rather than failing entirely.

---

## V&T Statement
- **Exists:** ChatGPT subagent adapter specification describing architectural position, input/output contracts, constitutional constraint injection, capability and constraint lists, UICare GPT-4o-mini usage mapping, cost considerations, vendor lock-in prevention rules
- **Non-existent:** Formalized ChatGPT adapter code in SentinelOS; contract test suite for AgentExecutionPort; cost tracking dashboard; automated system prompt injection for constitutional constraints
- **Unverified:** Whether UICare's current GPT-4o-mini integration follows the adapter pattern described here; whether the system prompt constraint injection produces compliant outputs from ChatGPT models
- **Functional status:** Adapter specification is complete — UICare's GPT-4o-mini usage is the only operational instance; formal adapter code and contract tests are pending
