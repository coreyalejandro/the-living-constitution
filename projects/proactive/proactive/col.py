"""
PROACTIVE COL — Cognitive Operating Layer

First layer of the PROACTIVE pipeline. Uses Claude to parse human intent
from MR descriptions and issue text, extracting structured intent that
feeds into the Contract Window.

Falls back to regex when LLM is unavailable (API key missing). If the API key
is present but the LLM call fails, an exception is raised – no silent fallback.
This ensures deterministic behavior: with key present, output always comes
from the LLM or the system stops.

Output: IntentReceipt with action, target, scope, goal, constraints,
ambiguities, and confidence score.
"""

from __future__ import annotations

import json
import logging
import os
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, List, Optional

logger = logging.getLogger(__name__)

__all__ = [
    "ParsedIntent",
    "IntentReceipt",
    "compile_intent",
]

_PROMPTS_DIR = Path(__file__).parent / "prompts"


# ---------------------------------------------------------------------------
# Fallback regex vocabulary (used only when API key missing)
# ---------------------------------------------------------------------------

_ACTION_PATTERNS: list[tuple[str, str]] = [
    (r"\b(fix(?:es|ed)?|repair|resolve[sd]?|patch(?:ed)?)\b", "fix"),
    # Prefer "add tests" as test work before generic "add" (create)
    (r"\badd(?:s|ed)?\s+tests?\b", "test"),
    (r"\b(add(?:s|ed)?|implement(?:s|ed)?|creat(?:e[sd]?|ing)|introduc(?:e[sd]?|ing))\b", "create"),
    (r"\b(refactor(?:s|ed)?|restructur(?:e[sd]?|ing)|reorgani[sz](?:e[sd]?|ing))\b", "refactor"),
    (r"\b(updat(?:e[sd]?|ing)|modif(?:y|ies|ied)|chang(?:e[sd]?|ing))\b", "update"),
    (r"\b(remov(?:e[sd]?|ing)|delet(?:e[sd]?|ing)|drop(?:s|ped)?)\b", "remove"),
    (r"\b(test(?:s|ed|ing)?|verif(?:y|ies|ied)|validat(?:e[sd]?|ing))\b", "test"),
    (r"\b(optimiz(?:e[sd]?|ing)|improv(?:e[sd]?|ing)|enhanc(?:e[sd]?|ing))\b", "optimize"),
    (r"\b(document(?:s|ed|ing)?|explain(?:s|ed|ing)?)\b", "document"),
]

_TARGET_PATTERNS: list[tuple[str, str]] = [
    (r"\b(function|method|def\s+\w+)\b", "function"),
    (r"\b(class(?:es)?)\b", "class"),
    (r"\b(test(?:s)?|spec(?:s)?)\b", "test"),
    (r"\b(module(?:s)?|package(?:s)?)\b", "module"),
    (r"\b(api|endpoint(?:s)?|route(?:s)?)\b", "api"),
    (r"\b(database|db|migration(?:s)?|schema)\b", "database"),
    (r"\b(pipeline(?:s)?|ci(?:/cd)?|workflow(?:s)?)\b", "pipeline"),
    (r"\b(config(?:uration)?|setting(?:s)?|env(?:ironment)?)\b", "config"),
    (r"\b(doc(?:s|umentation)?|readme|changelog)\b", "documentation"),
    (r"\b(bug|error|issue|defect|regression)\b", "bug"),
]

_SCOPE_PATTERNS: list[tuple[str, str]] = [
    (r"\b(single[_\s]file|one[_\s]file)\b", "single_file"),
    (r"\b(module[_\s]wide|entire[_\s]module|whole[_\s]module)\b", "module"),
    (r"\b(project[-_\s]wide|entire[_\s]project|whole[_\s]project|global)\b", "project"),
    (r"\b(local|isolated|contained|scoped)\b", "local"),
]

_CONSTRAINT_PATTERNS: list[tuple[str, str]] = [
    (r"\b(security|secure|auth(?:entication|orization)?|sql[_\s]injection|xss|csrf)\b", "security"),
    (r"\b(performance|perf|speed|latency|throughput|O\([^)]+\))\b", "performance"),
    (r"\b(backward[_\s]compat(?:ible|ibility)?|no[_\s]breaking[_\s]changes?)\b", "backward_compat"),
    (r"\b(no[_\s]new[_\s]dep(?:endenc(?:y|ies))?|zero[_\s]dep(?:endenc(?:y|ies))?)\b", "no_new_deps"),
    (r"\b(test[_\s]coverage|coverage|covered)\b", "test_coverage"),
    (r"\b(type[_\s]safe(?:ty)?|typed|mypy|pyright)\b", "type_safety"),
]

_AMBIGUITY_PATTERNS: list[tuple[str, str]] = [
    (r"\b(somehow|maybe|perhaps|possibly|might|could|should)\b", "uncertain_approach"),
    (r"\b(etc\.?|and[_\s]so[_\s]on|and[_\s]more|\.\.\.)\b", "incomplete_scope"),
    (r"\b(various|several|some|many|multiple)\b", "vague_quantity"),
    (r"\b(better|improve|good|nice|clean)\b", "subjective_quality"),
    (r"\b(asap|soon|quickly|fast)\b", "vague_timeline"),
]


# ---------------------------------------------------------------------------
# Dataclasses
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class ParsedIntent:
    """Structured representation of what the user intends to do."""

    action: str
    target: str
    scope: str
    goal: str
    constraints: List[str] = field(default_factory=list)
    ambiguities: List[str] = field(default_factory=list)
    reasoning: Optional[str] = None


@dataclass(frozen=True)
class IntentReceipt:
    """Output of the COL layer — structured intent with confidence."""

    raw_text: str
    parsed_intent: ParsedIntent
    confidence: float
    needs_clarification: bool
    clarification_questions: List[str] = field(default_factory=list)
    llm_used: bool = False          # True if LLM was used, False if regex fallback


# ---------------------------------------------------------------------------
# LLM parsing (strict: raises on failure)
# ---------------------------------------------------------------------------

def _parse_intent_llm(text: str) -> dict[str, Any]:
    """Call Claude to extract structured intent. Raises on failure."""
    import anthropic

    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        raise RuntimeError("ANTHROPIC_API_KEY not set")

    prompt_path = _PROMPTS_DIR / "compile_intent.txt"
    system = prompt_path.read_text(encoding="utf-8")

    client = anthropic.Anthropic(api_key=api_key)
    response = client.messages.create(
        model=os.environ.get("PROACTIVE_MODEL_INTENT", "claude-3-haiku-20240307"),
        max_tokens=1024,
        temperature=0.0,
        system=system,
        messages=[{"role": "user", "content": text}],
    )
    raw = response.content[0].text.strip()

    # Strip markdown fences if present
    if raw.startswith("```"):
        lines = raw.split("\n")
        raw = "\n".join(lines[1:-1]).strip()

    result = json.loads(raw)
    if not isinstance(result, dict):
        raise ValueError("LLM response is not a JSON object")
    return result


# ---------------------------------------------------------------------------
# Regex fallback (used only when API key missing)
# ---------------------------------------------------------------------------

def _match_first(text: str, patterns: list[tuple[str, str]], default: str) -> str:
    for pattern, label in patterns:
        if re.search(pattern, text, re.IGNORECASE):
            return label
    return default


def _match_all(text: str, patterns: list[tuple[str, str]]) -> List[str]:
    seen: set[str] = set()
    results: List[str] = []
    for pattern, label in patterns:
        if label not in seen and re.search(pattern, text, re.IGNORECASE):
            seen.add(label)
            results.append(label)
    return results


def _infer_goal_fallback(text: str, action: str) -> str:
    """Heuristic goal generation for fallback mode."""
    if action == "fix":
        return "resolve issue"
    if action == "create":
        return "add new functionality"
    if action == "refactor":
        return "improve code structure"
    if action == "update":
        return "modify existing behavior"
    if action == "remove":
        return "delete unnecessary code"
    if action == "test":
        return "verify correctness"
    if action == "optimize":
        return "enhance performance"
    if action == "document":
        return "clarify documentation"
    # Try to extract a short phrase after "to" or "so that"
    match = re.search(r"\b(?:to|so that)\s+(.+?)(?:\.|,|$)", text, re.I)
    if match:
        return match.group(1).strip()[:100]
    return "unknown"


def _parse_intent_regex(text: str) -> dict[str, Any]:
    action = _match_first(text, _ACTION_PATTERNS, "unknown")
    return {
        "action": action,
        "target": _match_first(text, _TARGET_PATTERNS, "unknown"),
        "scope": _match_first(text, _SCOPE_PATTERNS, "unknown"),
        "goal": _infer_goal_fallback(text, action),
        "constraints": _match_all(text, _CONSTRAINT_PATTERNS),
        "ambiguities": _match_all(text, _AMBIGUITY_PATTERNS),
    }


# ---------------------------------------------------------------------------
# Confidence + clarification
# ---------------------------------------------------------------------------

def _compute_confidence_fallback(
    action: str,
    target: str,
    scope: str,
    ambiguities: List[str],
    text_length: int,
) -> float:
    """Heuristic confidence when LLM not used."""
    score = 1.0
    if action == "unknown":
        score -= 0.3
    if target == "unknown":
        score -= 0.2
    if scope == "unknown":
        score -= 0.1
    score -= len(ambiguities) * 0.05
    if text_length < 20:
        score -= 0.2
    return round(max(0.0, min(1.0, score)), 2)


def _build_clarification_questions(
    action: str,
    target: str,
    scope: str,
    ambiguities: List[str],
    confidence: float = 1.0,
) -> List[str]:
    questions: List[str] = []

    if action == "unknown":
        questions.append(
            "What action are you performing? (e.g. fix, add, refactor, update)"
        )
    if target == "unknown":
        questions.append(
            "What is the target of this change? (e.g. function, class, API endpoint)"
        )
    if scope == "unknown":
        # High-confidence receipts with concrete action+target do not need a
        # blocking scope question (e.g. clear security fixes).
        if not (
            confidence >= 0.85
            and action != "unknown"
            and target != "unknown"
        ):
            questions.append(
                "What is the scope of this change? (e.g. single file, module, project)"
            )
    if "uncertain_approach" in ambiguities:
        questions.append(
            "The approach seems uncertain. Can you describe the specific method you'll use?"
        )
    if "incomplete_scope" in ambiguities:
        questions.append(
            "The scope appears incomplete. What exactly is included in this change?"
        )
    if "subjective_quality" in ambiguities:
        questions.append(
            "Quality terms like 'better' or 'cleaner' are subjective. "
            "What specific measurable improvement are you targeting?"
        )

    return questions


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def compile_intent(text: str) -> IntentReceipt:
    """Parse human intent from MR or issue text using Claude.

    If ANTHROPIC_API_KEY is set, uses Claude and raises an exception on failure.
    If the key is not set, falls back to regex-based parsing.

    Args:
        text: Raw text from an MR title + description, or issue body.

    Returns:
        IntentReceipt ready to feed into the Contract Window.
    """
    text = text.strip()

    api_key = os.environ.get("ANTHROPIC_API_KEY")
    using_llm = bool(api_key)

    if using_llm:
        # Strict mode: LLM must succeed or raise
        parsed_data = _parse_intent_llm(text)
        # Extract fields with defaults
        action = str(parsed_data.get("action", "unknown"))
        target = str(parsed_data.get("target", "unknown"))
        scope = str(parsed_data.get("scope", "unknown"))
        goal = str(parsed_data.get("goal", "unknown"))
        constraints = [str(c) for c in parsed_data.get("constraints", [])]
        ambiguities = [str(a) for a in parsed_data.get("ambiguities", [])]
        reasoning = parsed_data.get("reasoning")
        # Use model's confidence if provided, else compute a fallback
        model_conf = parsed_data.get("confidence")
        if model_conf is not None:
            try:
                confidence = round(max(0.0, min(1.0, float(model_conf))), 2)
            except (TypeError, ValueError):
                confidence = _compute_confidence_fallback(action, target, scope, ambiguities, len(text))
        else:
            confidence = _compute_confidence_fallback(action, target, scope, ambiguities, len(text))
    else:
        # Fallback to regex
        parsed_data = _parse_intent_regex(text)
        action = parsed_data["action"]
        target = parsed_data["target"]
        scope = parsed_data["scope"]
        goal = parsed_data["goal"]
        constraints = parsed_data["constraints"]
        ambiguities = parsed_data["ambiguities"]
        reasoning = None
        confidence = _compute_confidence_fallback(action, target, scope, ambiguities, len(text))

    questions = _build_clarification_questions(
        action, target, scope, ambiguities, confidence
    )
    needs_clarification = bool(questions) or confidence < 0.5

    parsed = ParsedIntent(
        action=action,
        target=target,
        scope=scope,
        goal=goal,
        constraints=constraints,
        ambiguities=ambiguities,
        reasoning=reasoning,
    )

    return IntentReceipt(
        raw_text=text,
        parsed_intent=parsed,
        confidence=confidence,
        needs_clarification=needs_clarification,
        clarification_questions=questions,
        llm_used=using_llm,
    )