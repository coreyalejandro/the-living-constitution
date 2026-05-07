"""
PROACTIVE MR Analyzer

Full pipeline orchestrator: COL → Contract Window → Validator → Drift.

Extracts claims and intent from merge request context, renders a
persistent Contract Window, validates against constitutional invariants,
and detects scope drift from the contract.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import List, Optional

from proactive.col import IntentReceipt, compile_intent
from proactive.contract_window import (
    ContractWindowState,
    create_contract_state,
    render_contract,
)
from proactive.drift_detector import DriftResult, detect_drift
from proactive.llm_client import LLMClient
from proactive.validator import Violation, check_invariants


__all__ = [
    "Claim",
    "MRContext",
    "MRAnalysisResult",
    "extract_claims",
    "analyze_mr",
]


@dataclass(frozen=True)
class Claim:
    """A verifiable claim extracted from MR text."""

    text: str
    claim_type: str  # "completion", "performance", "correctness", "existence", "security"
    source: str      # "description", "comment", "diff_comment"
    line_number: Optional[int] = None


@dataclass(frozen=True)
class MRContext:
    """Context for a merge request under review."""

    title: str
    description: str
    diff: str
    test_artifacts_exist: bool
    pipeline_url: str = ""                     # URL to the CI pipeline
    pipeline_status: str = ""                   # e.g., "success", "failed"
    comments: List[str] = field(default_factory=list)
    linked_issues: List[str] = field(default_factory=list)


@dataclass
class MRAnalysisResult:
    """Result of analyzing a merge request.

    Contains the full pipeline output: intent receipt, contract state,
    violations, drift analysis, and claims.
    """

    violations: List[Violation] = field(default_factory=list)
    claims_found: List[Claim] = field(default_factory=list)
    trust_score: float = 1.0
    receipt: Optional[IntentReceipt] = None
    contract: Optional[ContractWindowState] = None
    drift: Optional[DriftResult] = None
    clarification_questions: List[str] = field(default_factory=list)
    pipeline_url: str = ""                      # For evidence summary
    test_artifacts_exist: bool = False          # For evidence summary
    pipeline_status: str = ""                    # For evidence summary

    @property
    def should_block(self) -> bool:
        return any(v.severity == "ERROR" for v in self.violations)

    @property
    def verdict(self) -> str:
        if self.should_block:
            return "BLOCKED"
        if self.drift and self.drift.has_drift:
            return "DRIFT_DETECTED"
        if self.contract and self.contract.status == "pending":
            return "PENDING_CLARIFICATION"
        if self.violations:
            return "FLAGGED"
        return "APPROVED"


# ---------------------------------------------------------------------------
# Claim extraction patterns (regex fallback)
# ---------------------------------------------------------------------------

COMPLETION_PATTERNS = [
    (r"\b(?:all\s+)?tests?\s+pass(?:ing|ed|es)?\b", "completion"),
    (r"\b(?:implementation|feature)\s+(?:is\s+)?complete[d]?\b", "completion"),
    (r"\bfully\s+implemented\b", "completion"),
    (r"\bfinished\s+(?:all|the|this)\b", "completion"),
    (r"\bdone\s+(?:with|implementing)\b", "completion"),
]

PERFORMANCE_PATTERNS = [
    (r"\bO\([^)]+\)", "performance"),
    (r"\b\d+x\s+(?:faster|slower|improvement)\b", "performance"),
    (r"\breduced\s+(?:latency|time|memory)\b", "performance"),
    (r"\breduces?\s+(?:latency|time|memory)\b", "performance"),
]

CORRECTNESS_PATTERNS = [
    (r"\bfixes?\s+(?:the\s+)?bug\b", "correctness"),
    (r"\bresolves?\s+(?:the\s+)?issue\b", "correctness"),
    (r"\bno\s+(?:more\s+)?(?:errors?|bugs?|issues?)\b", "correctness"),
]

EXISTENCE_PATTERNS = [
    (r"\b(new|added|created)\s+(?:file|function|class|module)\b", "existence"),
    (r"\bexists?\s+(?:now|currently)\b", "existence"),
]

SECURITY_PATTERNS = [
    (r"\b(?:prevents?|stops?|blocks?)\s+(?:sql\s+injection|xss|csrf)\b", "security"),
    (r"\b(?:adds?|implements?)\s+(?:authentication|authorization)\b", "security"),
]

_ALL_PATTERNS = (
    COMPLETION_PATTERNS
    + PERFORMANCE_PATTERNS
    + CORRECTNESS_PATTERNS
    + EXISTENCE_PATTERNS
    + SECURITY_PATTERNS
)


def extract_claims(text: str, source: str = "description") -> List[Claim]:
    """Extract verifiable claims from MR text using regex.

    Args:
        text: Raw text from MR description, comment, or diff.
        source: Origin label for the claim.

    Returns:
        List of extracted claims.
    """
    claims: List[Claim] = []
    for pattern, claim_type in _ALL_PATTERNS:
        for match in re.finditer(pattern, text, re.IGNORECASE):
            # Get the sentence containing the match
            start = text.rfind(".", 0, match.start())
            end = text.find(".", match.end())
            sentence = text[start + 1 : end + 1 if end != -1 else len(text)].strip()
            if not sentence:
                sentence = match.group()
            claims.append(
                Claim(
                    text=sentence,
                    claim_type=claim_type,
                    source=source,
                )
            )
    # Deduplicate by text (case-insensitive)
    unique = {}
    for c in claims:
        key = c.text.lower().strip()
        if key not in unique:
            unique[key] = c
    return list(unique.values())


def _update_contract_status(
    contract: ContractWindowState,
    new_status: str,
) -> ContractWindowState:
    """Create a new ContractWindowState with an updated status."""
    return ContractWindowState(
        user_intent_human=contract.user_intent_human,
        user_intent_machine=contract.user_intent_machine,
        working_budget=contract.working_budget,
        agent_needs=contract.agent_needs,
        risk_assessment=contract.risk_assessment,
        risk_factors=contract.risk_factors,
        constraints=contract.constraints,
        goal=contract.goal,
        status=new_status,
    )


def _merge_llm_claims(
    regex_claims: List[Claim],
    llm_claims: Optional[List[Claim]],
) -> List[Claim]:
    """Merge LLM-detected claims with regex claims, deduplicating by text."""
    if not llm_claims:
        return regex_claims
    existing_texts = {c.text.lower().strip() for c in regex_claims}
    merged = list(regex_claims)
    for claim in llm_claims:
        if claim.text.lower().strip() not in existing_texts:
            merged.append(claim)
            existing_texts.add(claim.text.lower().strip())
    return merged


def _merge_llm_violations(
    regex_violations: List[Violation],
    llm_violations: Optional[List[Violation]],
) -> List[Violation]:
    """Merge LLM-detected violations with regex violations."""
    if not llm_violations:
        return regex_violations
    # Use rule_id to deduplicate
    existing_ids = {v.rule_id for v in regex_violations}
    merged = list(regex_violations)
    for v in llm_violations:
        if v.rule_id not in existing_ids:
            merged.append(v)
            existing_ids.add(v.rule_id)
    return merged


def analyze_mr(
    context: MRContext,
    llm_client: Optional[LLMClient] = None,
) -> MRAnalysisResult:
    """Analyze a merge request through the full PROACTIVE pipeline.

    Pipeline: COL (intent) → Contract Window → Validator (I1-I6) → Drift.

    When an LLM client is provided and enabled, semantic analysis augments
    each pipeline stage. When unavailable, falls back to regex-only.

    Args:
        context: The MR context to analyze.
        llm_client: Optional LLM client for semantic augmentation.

    Returns:
        Analysis result with contract, violations, drift, and trust score.
    """
    if llm_client is None:
        llm_client = LLMClient.from_env()

    all_violations: List[Violation] = []
    all_claims: List[Claim] = []

    # --- Layer 1: COL — Capture Intent ---
    intent_text = f"{context.title}. {context.description}"
    receipt = compile_intent(intent_text)

    # Build intent dict for downstream layers (validator, drift)
    intent_dict = {
        "action": receipt.parsed_intent.action,
        "target": receipt.parsed_intent.target,
        "scope": receipt.parsed_intent.scope,
        "goal": receipt.parsed_intent.goal,
        "constraints": receipt.parsed_intent.constraints,
        "ambiguities": receipt.parsed_intent.ambiguities,
        "confidence": receipt.confidence,
    }

    # --- Layer 2: Contract Window — Render Contract ---
    contract = create_contract_state(receipt)

    # Collect clarification questions for ambiguous intent
    questions: List[str] = []
    if contract.status == "pending":
        questions = [
            f"Ambiguity: {a}" for a in receipt.parsed_intent.ambiguities
        ]

    # --- Extract claims (regex + LLM augmentation) ---
    # Description
    regex_claims_desc = extract_claims(context.description, "description")
    llm_claims_desc = llm_client.extract_claims_semantic(context.description)
    # Convert LLM dicts to Claim objects
    if llm_claims_desc:
        llm_claims_desc_obj = [
            Claim(
                text=item["text"],
                claim_type=item["claim_type"],
                source="description_llm",
            )
            for item in llm_claims_desc
            if item.get("text") and item.get("claim_type")
        ]
    else:
        llm_claims_desc_obj = []
    all_claims = _merge_llm_claims(regex_claims_desc, llm_claims_desc_obj)

    # Comments
    for comment in context.comments:
        regex_claims_comment = extract_claims(comment, "comment")
        llm_claims_comment = llm_client.extract_claims_semantic(comment)
        if llm_claims_comment:
            llm_claims_comment_obj = [
                Claim(
                    text=item["text"],
                    claim_type=item["claim_type"],
                    source="comment_llm",
                )
                for item in llm_claims_comment
                if item.get("text") and item.get("claim_type")
            ]
        else:
            llm_claims_comment_obj = []
        # Merge with existing claims
        all_claims = _merge_llm_claims(all_claims, regex_claims_comment)
        all_claims = _merge_llm_claims(all_claims, llm_claims_comment_obj)

    # --- Layer 3: Validator — Check against constitution ---
    # Run regex validator (always runs, even if LLM succeeds)
    regex_violations = check_invariants(
        context.description,
        "MR_DESCRIPTION",
        intent=intent_dict,
    )
    # LLM validator (returns None if fails)
    llm_violations_raw = llm_client.check_invariants_semantic(
        context.description,
        "MR_DESCRIPTION",
        intent=intent_dict,          # structured intent
    )
    # Convert raw dicts to Violation objects (assuming validator returns list of dicts)
    if llm_violations_raw:
        llm_violations = [
            Violation(
                violation_id=f"LLM-{i}",
                invariant=item["invariant"],
                severity=item["severity"],
                location=item.get("location", {}),
                message=item["message"],
                suggested_fix=item.get("suggested_fix", ""),
                evidence=item.get("evidence", {}),
                rule_id=f"{item['invariant']}_llm_semantic",
            )
            for i, item in enumerate(llm_violations_raw)
            if item.get("invariant")
        ]
    else:
        llm_violations = []
    all_violations = _merge_llm_violations(regex_violations, llm_violations)

    # Additional I2 check: phantom completion when no test artifacts
    completion_claims = [c for c in all_claims if c.claim_type == "completion"]
    if completion_claims and not context.test_artifacts_exist:
        for claim in completion_claims:
            all_violations.append(
                Violation(
                    violation_id=f"V-MR-I2-{hash(claim.text) % 10000:04X}",
                    invariant="I2",
                    severity="ERROR",
                    location={
                        "file": "MR_DESCRIPTION",
                        "line": 1,
                        "context": claim.text[:200],
                    },
                    message=(
                        f"I2 VIOLATION: Phantom completion detected. "
                        f"MR claims '{claim.text[:80]}' but no test execution "
                        f"artifacts found."
                    ),
                    suggested_fix=(
                        "Run tests and ensure artifacts are committed, "
                        "or remove the completion claim."
                    ),
                    evidence={
                        "claim_text": claim.text,
                        "claim_type": claim.claim_type,
                        "test_artifacts_exist": False,
                    },
                    rule_id="I2_phantom_completion_mr",
                )
            )

    # --- Layer 4: Drift Detection — Check diff against contract ---
    drift = detect_drift(
        receipt,            # pass full receipt
        context.diff,
    )

    # LLM drift augmentation
    llm_drift = llm_client.assess_drift_semantic(
        intent_text,
        context.diff,
        intent=intent_dict,
    )
    if llm_drift and llm_drift.get("has_drift") and not drift.has_drift:
        drift = DriftResult(
            has_drift=True,
            unrelated_additions=tuple(llm_drift.get("unrelated", [])),
            suggestion=llm_drift.get("reason", ""),
            drift_severity="major" if len(llm_drift.get("unrelated", [])) >= 2 else "minor",
        )

    # --- Update contract status based on findings ---
    if any(v.severity == "ERROR" for v in all_violations):
        contract = _update_contract_status(contract, "violations_found")
    elif drift.has_drift:
        contract = _update_contract_status(contract, "drift_detected")

    # --- Calculate trust score ---
    if not all_claims:
        trust_score = 1.0
    else:
        error_count = len([v for v in all_violations if v.severity == "ERROR"])
        trust_score = max(0.0, 1.0 - (error_count / len(all_claims)))

    return MRAnalysisResult(
        violations=all_violations,
        claims_found=all_claims,
        trust_score=trust_score,
        receipt=receipt,
        contract=contract,
        drift=drift,
        clarification_questions=questions,
        pipeline_url=context.pipeline_url,
        test_artifacts_exist=context.test_artifacts_exist,
        pipeline_status=context.pipeline_status,
    )