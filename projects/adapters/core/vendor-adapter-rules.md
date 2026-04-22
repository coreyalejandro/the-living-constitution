# Vendor Adapter Rules
## Adapters Never Override the Constitution

---

## The Governing Principle

The Living Constitution governs. Vendors execute. This hierarchy is absolute and non-negotiable.

When a vendor's model, API, or execution environment conflicts with a constitutional rule, the constitutional rule wins. The adapter must enforce the Constitution against the vendor's behavior, not accommodate the vendor's behavior at the expense of the Constitution.

---

## The Rules

### Rule 1: Adapters Implement Ports, Not Governance

An adapter translates between the SentinelOS core and a specific vendor. It maps port types to vendor types and vendor types back to port types. It does not add governance rules, remove governance rules, or interpret governance rules. The core defines what must happen. The adapter defines how it happens on a specific platform.

**Violation example:** An adapter adds a "fast mode" that skips the V&T Statement requirement because the vendor's API has a low-latency endpoint that does not support structured output. This is a violation. The V&T requirement is constitutional. The adapter must find a way to satisfy it within the vendor's constraints, not waive it for performance.

### Rule 2: Vendor Training Does Not Override Constitutional Training

AI models from different vendors have different training distributions, safety policies, and behavioral tendencies. Some models may resist certain instructions, prefer certain output formats, or default to behaviors that conflict with TLC rules. The adapter must compensate.

**Compensation strategies:**
- Encode constitutional constraints in the system prompt at the highest priority level.
- Post-process vendor outputs to enforce compliance (strip non-compliant formatting, inject V&T Statements, validate truth-status claims).
- Reject non-compliant outputs and retry with more explicit instructions.
- If a vendor model consistently cannot comply with a constitutional requirement, flag the incompatibility rather than silently degrading governance.

### Rule 3: No Vendor-Specific Governance Paths

There must not be a "Claude governance path" and an "OpenAI governance path." Governance is defined once in TLC and SentinelOS. All adapters implement the same ports with the same contracts. The governance outcome must be equivalent regardless of which adapter is used.

**Test:** If you swap the Claude adapter for the ChatGPT adapter, does the system still enforce the same invariants, require the same consent pipeline, produce the same V&T Statement structure? If the answer is no, the divergent adapter is non-compliant.

### Rule 4: Adapters Handle Vendor Failures, Not Governance Failures

When a vendor API returns an error, the adapter reports it. When a vendor model produces a non-compliant output, the adapter rejects it. In both cases, the adapter does not make a governance decision about what to do next. It returns the failure to the core, and the core decides: retry, fallback, fail safely, or escalate to human.

**Specifically:**
- Adapter retries for transient vendor errors (rate limits, timeouts): allowed.
- Adapter retries for non-compliant outputs with stronger instructions: allowed.
- Adapter silently accepting a non-compliant output because retries are expensive: violation.
- Adapter choosing a fallback vendor without core authorization: violation.

### Rule 5: Vendor Data Does Not Leave the Governance Boundary Without Consent

When an adapter sends data to a vendor API, that data crosses a trust boundary. The adapter must ensure:

- No PII is sent to vendor APIs without explicit consent (ConsentChain Stage 4).
- No production secrets are included in API payloads.
- Data retention policies of the vendor are compatible with the Commonwealth's data governance.
- If the vendor's terms of service allow training on input data, the user must be informed and must consent.

### Rule 6: Adapters Are Audited Like Code

Adapters are code. They are subject to the same Article II requirements as all other code in the Commonwealth:

- Immutability: adapters use immutable patterns.
- Testing: adapters have unit tests and contract tests.
- Security: adapters do not hardcode secrets, validate all inputs, and handle errors comprehensively.
- File organization: adapter code follows the same size and structure rules.
- Code review: adapters are reviewed by the Code Reviewer agent before merge.

### Rule 7: New Vendors Require Constitutional Review

Adding a new vendor adapter is not a routine code change. It introduces a new trust boundary, a new data flow path, and a new potential failure mode. Before writing a new adapter:

1. **Domain impact assessment:** Which safety domains does this vendor integration touch?
2. **Data flow review:** What data will cross the vendor boundary? Is consent required?
3. **Failure mode analysis:** What happens when this vendor is unavailable? What is the fallback?
4. **Contract compatibility:** Does the existing port contract support this vendor, or does the port need extension?
5. **Cost analysis:** What is the cost profile of this vendor? Are cost guardrails in place?

This review is documented and stored in the `projects/adapters/core/` directory as a vendor assessment file.

---

## ChatGPT Subagents: Specific Application of These Rules

ChatGPT subagents (GPT-4o, GPT-4o-mini, and other OpenAI models) are the most common secondary adapter in the Commonwealth. The following specific rules apply:

1. **ChatGPT subagents are never the master architecture.** Claude Code with CLAUDE.md is the primary governance enforcement mechanism at Tier 1. ChatGPT subagents execute governed actions dispatched by the orchestration cortex.

2. **ChatGPT system prompts include constitutional constraints.** The adapter injects Article I rights, Article II code rules, and V&T Statement requirements into every system prompt. The ChatGPT model may not natively understand or enforce these — the adapter compensates through prompt engineering and output validation.

3. **ChatGPT outputs are validated before returning to the core.** The adapter checks every ChatGPT response for V&T Statement presence, truth-status honesty, and rights compliance before passing it upstream. Non-compliant responses are rejected and retried.

4. **OpenAI-specific features (DALL-E, vision, code interpreter) are treated as adapter capabilities, not core capabilities.** If the core needs image generation, it calls the ImageGenerationPort. The ChatGPT adapter implements that port using DALL-E. If DALL-E is replaced by a different service, only the adapter changes.

5. **Cost tracking is mandatory.** Every ChatGPT API call is logged with token count and estimated cost. The adapter enforces per-session and per-day cost limits. Exceeding limits triggers a rate-limit response to the core, not silent continuation.

---

## V&T Statement
- **Exists:** Seven vendor adapter rules with violation examples and compensation strategies; ChatGPT-specific rule application; new vendor review process; data governance requirements for vendor boundaries
- **Non-existent:** Automated adapter compliance testing; vendor assessment file template; cost tracking dashboard; automated system prompt injection validation
- **Unverified:** Whether current UICare GPT-4o-mini usage follows all seven rules; whether any existing adapter code in the Commonwealth has been formally reviewed against these rules
- **Functional status:** Vendor adapter rules are fully specified as Tier 1 convention — enforcement relies on human review and code reviewer agent until automated adapter compliance testing is built
