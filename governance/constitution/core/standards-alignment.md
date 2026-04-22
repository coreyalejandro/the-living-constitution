# External Standards Alignment
## How TLC Maps to Recognized Governance Frameworks

The Living Constitution is not invented in isolation. Its articles map to widely recognized enterprise governance standards. This mapping makes TLC legible to organizations that already use these frameworks — and demonstrates that constitutional governance is not theoretical but grounded in established practice.

---

## Mapping Table

| TLC Article | External Standard | Standard Purpose | TLC Implementation |
|-------------|-------------------|-----------------|-------------------|
| **Article II** (Execution Law) | **NIST SSDF** (Secure Software Development Framework) | Defines secure SDLC practices as auditable artifacts | Immutability, truth-status discipline, security rules, file organization — all enforced via CLAUDE.md + CI hooks |
| **AI-Touching Surfaces** | **NIST AI RMF** (AI Risk Management Framework) | Manages risks and improves trustworthiness across AI system lifecycles | Every AI decision requires: documented purpose, bounded authority, audit trail, failure handling, expiry rules |
| **Article II** (Security) | **OpenSSF Scorecard** | Automated supply-chain risk controls | Branch protection, dependency hygiene, automated checks in CI |
| **Article I** (Bill of Rights) | **WCAG 2.1 AA** | Web accessibility standards | Neurodivergent-first design goes beyond WCAG — it is the floor, not the ceiling |
| **Article V** (Amendment Process) | **ISO 27001 Annex A** (Continual Improvement) | Systematic improvement of information security management | Trigger → observe → propose → evaluate → ratify cycle mirrors Plan-Do-Check-Act |

---

## Why This Matters

**For Anthropic reviewers**: TLC is not a bespoke framework with no external validation. Its articles implement patterns that real organizations use for real governance.

**For enterprise adoption**: Any organization already using NIST SSDF or AI RMF can adopt TLC as a compatible governance layer — not a replacement, but a constitutional structure that organizes existing practices.

**For the MADMall use case**: A healthcare product for a vulnerable population requires the highest governance standards. Mapping to NIST AI RMF ensures that moderation, recommendations, and content workflows meet externally recognized risk management criteria.

---

## Standard Details

### NIST SSDF (SP 800-218)
- **What**: Practices for secure software development lifecycle
- **Key requirement**: Practices produce *artifacts* as evidence — not just documentation, but proof that the practice happened
- **TLC alignment**: Article II's execution law produces artifacts (build contracts, V&T statements, test results) at every step

### NIST AI RMF (AI 100-1)
- **What**: Framework for managing AI system risks across the lifecycle
- **Key requirement**: Govern, Map, Measure, Manage — four functions for AI risk
- **TLC alignment**: Article I (Govern — rights that cannot be overridden), Article III (Map — every action traces to purpose), V&T Statements (Measure — honest status), Article V (Manage — amendment when failures occur)

### OpenSSF Scorecard
- **What**: Automated checks for supply-chain security
- **Key requirement**: Branch protection, dependency updates, CI/CD security, vulnerability disclosure
- **TLC alignment**: Article II security rules (no hardcoded secrets, validate input, OWASP Top 10), Census Doctrine (inventory every dependency)

---

## V&T Statement

Exists: Standards alignment mapping table connecting TLC Articles to NIST SSDF, NIST AI RMF, OpenSSF Scorecard, WCAG 2.1, and ISO 27001. Rationale for each mapping. Detailed descriptions of three primary standards.

Non-existent: Automated compliance checking against these standards. Formal certification or audit. CI gates that produce SSDF-style artifacts automatically.

Unverified: Whether current TLC implementation fully satisfies each standard's requirements. Specific control-level mapping (e.g., SSDF practice PW.1.1 to specific CLAUDE.md rules).

Functional status: Alignment mapping complete at the framework level. Detailed control-level mapping is a Phase 2 activity for enterprise adoption readiness.
