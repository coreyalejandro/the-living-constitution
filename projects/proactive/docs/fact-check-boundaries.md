# PROACTIVE — Fact-Check Boundaries

**Purpose:** Explicitly state what exists, what does not exist, and what is unverified. This document protects the credibility of the submission by drawing clear lines.

---

## What EXISTS and is VERIFIED

These artifacts are in the repository and can be independently confirmed:

| Artifact | Location | Status |
|----------|----------|--------|
| Constitutional validator (I1–I6) | `proactive/validator.py` | Implemented, tested |
| Cognitive Operating Layer (COL) | `proactive/col.py` | Implemented, tested |
| Contract Window | `proactive/contract_window.py` | Implemented, tested |
| Drift Detector | `proactive/drift_detector.py` | Implemented, tested |
| Semantic Drift Detector | `proactive/semantic_drift_detector.py` | Implemented, tested |
| MR Analyzer (full pipeline) | `proactive/mr_analyzer.py` | Implemented, tested |
| Severity Scorer | `proactive/severity_scorer.py` | Implemented, tested |
| Label Assigner | `proactive/label_assigner.py` | Implemented, tested |
| Report Formatter (V&T output) | `proactive/report_formatter.py` | Implemented, tested |
| V&T Generator (CLI + Web) | `proactive/vt_generator.py`, `proactive/web_ui.py` | Implemented, tested |
| LLM Client | `proactive/llm_client.py` | Implemented, tested |
| GitLab Client | `proactive/gitlab_client.py` | Implemented, tested |
| CLI entry point | `proactive/cli.py` | Implemented |
| Constitution (machine-readable) | `proactive/constitution.json` | Implemented |
| GitLab Duo agent definition | `.gitlab/duo/agents/proactive-agent.yml` | Registered |
| GitLab Duo triage flow | `.gitlab/duo/flows/proactive-triage.yml` | Defined |
| Claude Code flow | `.gitlab/duo/flows/claude.yaml` | Defined |
| CI/CD pipeline | `.gitlab-ci.yml` | Configured |
| Test suite | `tests/` (12 files) | 58+ tests, 83% coverage |
| Ablation study framework | `research/` (6 files) | Implemented |
| Demo MR (phantom completion) | MR !9 | Open, diff verifiable |
| Narrative documentation | `NARRATIVE.md` | Written |
| Agent constitution | `AGENTS.md`, `CLAUDE.md` | Written |
| Prompt templates | `proactive/prompts/` (4 files) | Written |

## What EXISTS but is NOT INDEPENDENTLY VERIFIED

These claims appear in the repository but have not been confirmed by an external party:

| Claim | Source | Verification Status |
|-------|--------|--------------------|
| "100% detection rate on n=200 TruthfulQA" | README.md | Self-reported. The validation script and results file exist, but no external party has reproduced the benchmark. |
| "0% false positive rate" | README.md | Self-reported. Based on internal test runs. No adversarial testing by a third party. |
| "83% test coverage" | README.md | Based on local `pytest --cov` runs. Judges can reproduce with `pytest tests/ -v --cov=proactive`. |
| LLM-augmented analysis quality | Multiple files | Depends on Claude API availability and model behavior. Regex fallback is deterministic and tested. |

## What DOES NOT EXIST

These are explicitly not implemented and not claimed:

| Component | Status | Notes |
|-----------|--------|-------|
| The Living Constitution (TLC) runtime | Not implemented | TLC is the broader architectural vision. PROACTIVE is the first working enforcement primitive. TLC as a runtime system does not exist. |
| UICare | Not implemented | Planned accessibility/consent component. Not built. |
| ConsentChain | Not implemented | Planned consent management component. Not built. |
| SentinelOS runtime | Not implemented | Referenced in some docs as the parent platform. No runtime exists. PROACTIVE is the working artifact. |
| Empirical Safety Engine (ESE) | Not implemented | Planned evaluation engine. Not built. |
| Production deployment | Not deployed | PROACTIVE runs locally and in CI. It is not deployed to a public-facing production instance. |
| External security audit | Not performed | No third-party security review has been conducted. |
| Live user feedback | Not collected | No real users have reviewed MRs with PROACTIVE in a production workflow. |
| Healthcare-specific functionality | Not implemented | The motivation references real-world stakes including healthcare, but PROACTIVE is a general-purpose epistemic safety tool. No healthcare-specific features exist. |
| Demo video | Not yet recorded | Script and runbook are prepared. Recording is pending. |

## Terminology Clarification

| Term | Meaning in This Project |
|------|------------------------|
| CMP (Cognitive Modeling Protocol) | The theoretical foundation for how AI systems should model their own epistemic state. PROACTIVE implements CMP principles through its invariant enforcement and V&T statements. |
| TLC (The Living Constitution) | The broader architectural vision for constitutional AI governance. PROACTIVE is the first proof artifact. TLC as a system does not exist. |
| Constitutional invariants (I1–I6) | Hard behavioral rules enforced by `proactive/validator.py`. These are implemented and tested. |
| Failure classes (F1–F5) | Categories of epistemic failure that PROACTIVE detects. Detection logic is implemented in the validator, drift detector, and MR analyzer. |
| V&T (Verification & Truth) | The mandatory output format for every PROACTIVE review. Documents what exists, what was verified, what was not claimed, and the verdict. |
| PASS / WARN / BLOCK | Deterministic verdicts. PASS = no violations. WARN = warnings only. BLOCK = at least one ERROR-severity violation. |

---

## V&T Statement for This Document

**V&T Statement:**
- **EXISTS:** All artifacts listed in the "EXISTS and is VERIFIED" table are present in the repository at the paths specified
- **VERIFIED AGAINST:** Repository file listing, test suite output, MR !9 diff, agent YAML definitions, CI configuration
- **NOT CLAIMED:** External reproduction of benchmarks, third-party audit, production deployment, TLC/UICare/ConsentChain implementation
- **STATUS:** PASS — boundaries are explicitly drawn; no overclaims detected in this document
