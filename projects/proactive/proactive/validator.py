"""
PROACTIVE Validator — Constitutional Invariant Enforcement

Third layer of the PROACTIVE pipeline. Checks MR content against the
six constitutional invariants (I1-I6) using Claude for semantic analysis,
with context from the COL layer (intent). Falls back to regex when LLM
is unavailable.

Output: List of Violation objects with severity, location, and suggested fixes.
"""

from __future__ import annotations

import json
import logging
import os
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)

__all__ = [
    "Violation",
    "check_invariants",
]

_PROMPTS_DIR = Path(__file__).parent / "prompts"


# ---------------------------------------------------------------------------
# Dataclasses
# ---------------------------------------------------------------------------

@dataclass
class Violation:
    """A single constitutional invariant violation."""

    violation_id: str
    invariant: str          # I1 through I6
    severity: str           # ERROR or WARNING
    location: Dict[str, Any]
    message: str
    rule_id: str
    suggested_fix: str = ""
    evidence: Dict[str, Any] = field(default_factory=dict)


# ---------------------------------------------------------------------------
# Regex fallback patterns
# ---------------------------------------------------------------------------

# I1 — Evidence-First: untagged absolute claims
_I1_PATTERNS = [
    r"\b(certainly|definitely|guaranteed|always|never|impossible|absolutely)\b",
    r"\ball\s+(?:tests?|cases?|edge\s+cases?)(?:\s+\w+){0,3}\s+(?:pass|work|handled)\b",
    r"\bfully\s+(?:implemented|tested|covered|secure)\b",
    r"\bno\s+(?:bugs?|errors?|issues?|vulnerabilities?)\b",
    r"\b100%\s+(?:coverage|correct|safe|secure)\b",
]

# I2 — No Phantom Work: completion claims
_I2_PATTERNS = [
    r"\b(?:all\s+)?tests?(?:\s+\w+){0,2}\s+pass(?:ing|ed|es)?\b",
    r"\b(?:implementation|feature)\s+(?:is\s+)?complete[d]?\b",
    r"\bfully\s+implemented\b",
    r"\bfinished\s+(?:all|the|this)\b",
    r"\bdone\s+(?:with|implementing)\b",
    r"\bready\s+(?:for\s+)?(?:review|merge|production)\b",
]

# I4 — Traceability: no issue reference
_I4_PATTERN = re.compile(
    r"(?:fixes?|closes?|resolves?|relates?\s+to|refs?)\s+#\d+",
    re.IGNORECASE,
)

# I5 — Safety Over Fluency: mixed hedging + certainty
_I5_HEDGE_WORDS = re.compile(
    r"\b(probably|likely|should|might|may|perhaps|possibly)\b",
    re.IGNORECASE,
)
_I5_CERTAIN_WORDS = re.compile(
    r"\b(definitely|certainly|guaranteed|always|will)\b",
    re.IGNORECASE,
)

# I6 — Fail Closed: error suppression
_I6_PATTERNS = [
    r"except\s*:\s*pass",
    r"except\s+Exception\s*:\s*pass",
    r"catch\s*\(\s*\)\s*\{\s*\}",
    r"\.ignore\s*\(",
    r"suppress\(",
    r"# noqa.*error",
    r"# type:\s*ignore",
]


# ---------------------------------------------------------------------------
# ID generation
# ---------------------------------------------------------------------------

def _vid(invariant: str, index: int, rule: str) -> str:
    return f"V-{invariant}-{index:04d}-{rule[:8].upper()}"


def _sentence_for_match(content: str, match: re.Match) -> str:
    start = content.rfind(".", 0, match.start())
    end = content.find(".", match.end())
    return content[start + 1 : end + 1 if end != -1 else len(content)].strip()


def _has_evidence_tag(sentence: str) -> bool:
    return bool(
        re.search(r"\[(?:verified|inferred|unverified)\]", sentence, re.IGNORECASE)
    )


# ---------------------------------------------------------------------------
# Regex-based checks (fallback)
# ---------------------------------------------------------------------------

def _check_i1_regex(content: str, file_path: str) -> List[Violation]:
    violations = []
    for i, pattern in enumerate(_I1_PATTERNS):
        for match in re.finditer(pattern, content, re.IGNORECASE):
            if _has_evidence_tag(_sentence_for_match(content, match)):
                continue
            violations.append(Violation(
                violation_id=_vid("I1", i, "absolute"),
                invariant="I1",
                severity="ERROR",
                location={"file": file_path, "line": 1, "context": match.group()},
                message=(
                    f"I1 VIOLATION: Untagged absolute claim '{match.group()}'. "
                    "Every claim must carry [verified], [inferred], or [unverified]."
                ),
                suggested_fix=(
                    f"Tag the claim: '{match.group()} [verified]' or downgrade: "
                    "'likely ...' [inferred]"
                ),
                rule_id="I1_untagged_absolute_claim",
            ))
    return violations


def _check_i2_regex(content: str, file_path: str) -> List[Violation]:
    violations = []
    for i, pattern in enumerate(_I2_PATTERNS):
        for match in re.finditer(pattern, content, re.IGNORECASE):
            start = content.rfind(".", 0, match.start())
            end = content.find(".", match.end())
            sentence = content[start + 1: end + 1 if end != -1 else len(content)].strip()
            violations.append(Violation(
                violation_id=_vid("I2", i, "phantom"),
                invariant="I2",
                severity="ERROR",
                location={"file": file_path, "line": 1, "context": sentence[:200]},
                message=(
                    f"I2 VIOLATION: Phantom completion detected. "
                    f"'{sentence[:80]}' claims work is done without artifact evidence."
                ),
                suggested_fix=(
                    "Either: (1) reference the artifact that proves completion, "
                    "or (2) remove the completion claim."
                ),
                rule_id="I2_phantom_completion",
            ))
    return violations


def _check_i4_regex(content: str, file_path: str, intent: Optional[Dict] = None) -> List[Violation]:
    """Check traceability. If intent involves a bug/feature, make the check stricter."""
    has_reference = bool(_I4_PATTERN.search(content))
    if has_reference:
        return []

    # Determine severity based on intent
    severity = "WARNING"
    if intent:
        # If intent targets a bug or feature, traceability is more important
        if intent.get("target") in ("bug", "feature") or intent.get("action") in ("fix", "create"):
            severity = "ERROR"
            message_suffix = " (required because intent indicates a bug/feature change)"
        else:
            message_suffix = ""
    else:
        message_suffix = ""

    return [Violation(
        violation_id=_vid("I4", 0, "trace"),
        invariant="I4",
        severity=severity,
        location={"file": file_path, "line": 1},
        message=(
            f"I4 VIOLATION: No traceability found.{message_suffix} "
            "MR describes changes but doesn't reference an issue."
        ),
        suggested_fix=(
            "Add an issue reference: 'Fixes #<issue_number>' or "
            "'Relates to #<issue_number>' in the MR description."
        ),
        rule_id="I4_no_trace_reference",
    )]


def _check_i5_regex(content: str, file_path: str) -> List[Violation]:
    violations = []
    sentences = re.split(r"[.!?]", content)
    for i, sentence in enumerate(sentences):
        has_hedge = bool(_I5_HEDGE_WORDS.search(sentence))
        has_certain = bool(_I5_CERTAIN_WORDS.search(sentence))
        if has_hedge and has_certain:
            violations.append(Violation(
                violation_id=_vid("I5", i, "mixed"),
                invariant="I5",
                severity="WARNING",
                location={"file": file_path, "line": 1, "context": sentence.strip()[:200]},
                message=(
                    "I5 VIOLATION: Mixed hedging and certainty in the same statement. "
                    f"'{sentence.strip()[:80]}'"
                ),
                suggested_fix=(
                    "Choose one: either hedge consistently ('probably', 'likely') "
                    "or provide verification evidence to justify certainty."
                ),
                rule_id="I5_mixed_confidence",
            ))
    return violations


def _check_i6_regex(content: str, file_path: str) -> List[Violation]:
    violations = []
    for i, pattern in enumerate(_I6_PATTERNS):
        for match in re.finditer(pattern, content, re.IGNORECASE):
            violations.append(Violation(
                violation_id=_vid("I6", i, "suppress"),
                invariant="I6",
                severity="ERROR",
                location={"file": file_path, "line": 1, "context": match.group()},
                message=(
                    f"I6 VIOLATION: Error suppression detected: '{match.group()}'. "
                    "Errors must surface, not be silenced."
                ),
                suggested_fix=(
                    "Handle the error explicitly: log it, re-raise it, or return "
                    "a meaningful error value. Never suppress silently."
                ),
                rule_id="I6_error_suppression",
            ))
    return violations


def _check_invariants_regex(
    content: str,
    file_path: str,
    intent: Optional[Dict] = None,
    *,
    skip_i4: bool = False,
) -> List[Violation]:
    violations: List[Violation] = []
    violations.extend(_check_i1_regex(content, file_path))
    violations.extend(_check_i2_regex(content, file_path))
    # I3 is not easily checked with regex; rely on LLM
    if not skip_i4:
        violations.extend(_check_i4_regex(content, file_path, intent))
    violations.extend(_check_i5_regex(content, file_path))
    violations.extend(_check_i6_regex(content, file_path))
    return violations


# ---------------------------------------------------------------------------
# LLM-based checks (updated to accept structured intent)
# ---------------------------------------------------------------------------

def _check_invariants_llm(
    content: str,
    file_path: str,
    intent: Optional[Dict] = None,
) -> Optional[List[Violation]]:
    """Call Claude to check I1-I6 semantically. Returns None on failure."""
    try:
        import anthropic

        api_key = os.environ.get("ANTHROPIC_API_KEY", "")
        if not api_key:
            return None

        prompt_path = _PROMPTS_DIR / "check_invariants.txt"
        system = prompt_path.read_text(encoding="utf-8")

        # Build user message with intent as JSON
        user_msg = {
            "intent": intent if intent else {},
            "content": content,
            "file_path": file_path,
        }
        user_json = json.dumps(user_msg, indent=2)

        client = anthropic.Anthropic(api_key=api_key)
        response = client.messages.create(
            model=os.environ.get("PROACTIVE_MODEL_INVARIANTS", "claude-3-haiku-20240307"),
            max_tokens=1024,
            temperature=0.0,
            system=system,
            messages=[{"role": "user", "content": user_json}],
        )
        raw = response.content[0].text.strip()

        if raw.startswith("```"):
            lines = raw.split("\n")
            raw = "\n".join(lines[1:-1]).strip()

        result = json.loads(raw)
        if not isinstance(result, list):
            return None

        violations = []
        for i, item in enumerate(result):
            if not isinstance(item, dict) or not item.get("invariant"):
                continue
            invariant = str(item["invariant"])
            severity = str(item.get("severity", "WARNING"))
            message = str(item.get("message", ""))
            line = int(item.get("line", 1))
            suggested_fix = item.get("suggested_fix", "")
            evidence = item.get("evidence", {})

            violations.append(Violation(
                violation_id=_vid(invariant, i, "llm"),
                invariant=invariant,
                severity=severity,
                location={"file": file_path, "line": line},
                message=f"[LLM] {message}",
                rule_id=f"{invariant}_llm_semantic",
                suggested_fix=suggested_fix,
                evidence=evidence,
            ))

        return violations

    except Exception:
        logger.warning("Validator LLM check failed, falling back to regex", exc_info=True)
        return None


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def check_invariants(
    content: str,
    file_path: str,
    intent: Optional[Dict] = None,  # now expects a dict (e.g., from COL)
    *,
    skip_i4: bool = False,
) -> List[Violation]:
    """Check content against I1-I6 constitutional invariants.

    Uses Claude for semantic analysis when available, falls back to
    regex-based checks when LLM is unavailable. The optional intent
    provides context to make checks more accurate.

    Args:
        content: Text to check (MR description, code, comment).
        file_path: Label for the source (e.g. "MR_DESCRIPTION", "src/foo.py").
        intent: Structured intent from COL (as a dict). Contains action,
                target, scope, goal, constraints, ambiguities, etc.
        skip_i4: If True, skip I4 traceability checks (e.g. standalone V&T tool
                without issue context).

    Returns:
        List of Violation objects. Empty list means no violations found.
    """
    llm_violations = _check_invariants_llm(content, file_path, intent)

    if llm_violations is not None:
        # LLM succeeded — also run regex for I4 and I6 which benefit from
        # deterministic pattern matching regardless, and now also I5 (simple mix detection)
        regex_violations = []
        if not skip_i4:
            regex_violations.extend(_check_i4_regex(content, file_path, intent))
        regex_violations.extend(_check_i6_regex(content, file_path))
        regex_violations.extend(_check_i5_regex(content, file_path))  # I5 also easy to regex

        # Merge: avoid duplicates by rule_id
        existing_rules = {v.rule_id for v in llm_violations}
        for v in regex_violations:
            if v.rule_id not in existing_rules:
                llm_violations.append(v)
                existing_rules.add(v.rule_id)

        return llm_violations

    # LLM unavailable — full regex fallback
    logger.info("LLM unavailable, using regex-only invariant checking")
    return _check_invariants_regex(content, file_path, intent, skip_i4=skip_i4)