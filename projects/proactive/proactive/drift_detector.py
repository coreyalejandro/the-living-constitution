"""
PROACTIVE Drift Detector — Scope Drift and F5 Cross-Episode Detection

Fourth layer of the PROACTIVE pipeline. Checks whether the code diff
aligns with the stated intent from the Contract Window.

Detects:
- Unrelated additions (code that doesn't match the intent)
- Scope creep (changes beyond what was promised)
- F5 Cross-Episode Drift: recurring drift patterns across MRs

Uses Claude for semantic analysis, falls back to keyword matching.

Output: DriftResult with has_drift flag, unrelated additions, and severity.
"""

from __future__ import annotations

import json
import logging
import os
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Optional

from proactive.col import IntentReceipt, ParsedIntent

logger = logging.getLogger(__name__)

__all__ = [
    "DriftResult",
    "detect_drift",
]

_PROMPTS_DIR = Path(__file__).parent / "prompts"


# ---------------------------------------------------------------------------
# Dataclass
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class DriftResult:
    """Result of drift detection analysis."""

    has_drift: bool
    unrelated_additions: tuple[str, ...] = field(default_factory=tuple)
    suggestion: str = ""
    drift_severity: str = "none"   # none, minor, major


# ---------------------------------------------------------------------------
# Regex fallback (goal-aware)
# ---------------------------------------------------------------------------

_DIFF_FILE_PATTERN = re.compile(r"^\+\+\+ b/(.+)$", re.MULTILINE)
_DIFF_ADDED_PATTERN = re.compile(r"^\+(?!\+\+)(.+)$", re.MULTILINE)
_DIFF_REMOVED_PATTERN = re.compile(r"^-(?!-)(.+)$", re.MULTILINE)

_ACTION_KEYWORDS: dict[str, list[str]] = {
    "fix":       ["fix", "bug", "error", "patch", "repair", "resolve"],
    "create":    ["add", "create", "implement", "new", "introduce"],
    "refactor":  ["refactor", "restructure", "reorganize", "rename", "move"],
    "update":    ["update", "modify", "change", "edit"],
    "remove":    ["remove", "delete", "drop", "clean"],
    "test":      ["test", "spec", "assert", "mock", "fixture"],
    "optimize":  ["optimize", "improve", "cache", "performance", "speed"],
    "document":  ["doc", "comment", "readme", "docstring", "explain"],
}

# When the diff clearly matches the stated target artifact, verb keywords
# in the patch are often omitted (e.g. "fix" not spelled out in code).
_ACTION_RELAX_WHEN_TARGET_MATCHES = frozenset({
    "fix",
    "update",
    "refactor",
    "remove",
    "optimize",
    "test",
    "document",
    "create",
})

# COL often maps diverse MR titles onto generic goals (e.g. "resolve issue");
# do not treat those boilerplate tokens as required diff keywords.
_GOAL_BOILERPLATE_WORDS = frozenset({
    "resolve",
    "issue",
    "behavior",
    "existing",
    "functionality",
    "modify",
    "enhance",
    "improve",
    "structure",
    "adding",
    "create",
    "update",
    "remove",
    "performance",
    "code",
    "unnecessary",
    "delete",
    "clarify",
    "documentation",
    "verify",
    "correctness",
})

_TARGET_KEYWORDS: dict[str, list[str]] = {
    "function":      ["def ", "function", "method"],
    "class":         ["class ", "Class"],
    "test":          ["test_", "spec_", "pytest", "unittest"],
    "module":        [
        "import ",
        "from ",
        "module",
        "connection",
        "pool",
        "refactor",
    ],
    "api":           [
        "route",
        "endpoint",
        "api",
        "request",
        "response",
        "readme",
        "usage",
        "documentation",
    ],
    "database":      ["db.", "query", "migration", "schema", "model"],
    "pipeline":      ["pipeline", "ci", "workflow", "stage", "job"],
    "config":        ["config", "settings", "env", ".yml", ".yaml", ".toml"],
    "documentation": ["#", "\"\"\"", "'''", "README", "CHANGELOG"],
    "bug":           ["fix", "bug", "error", "exception", "raise"],
}


def _extract_changed_files(diff: str) -> List[str]:
    return _DIFF_FILE_PATTERN.findall(diff)


def _extract_added_lines(diff: str) -> List[str]:
    return [m.group(1) for m in _DIFF_ADDED_PATTERN.finditer(diff)]


def _extract_removed_lines(diff: str) -> List[str]:
    return [m.group(1) for m in _DIFF_REMOVED_PATTERN.finditer(diff)]


def _create_api_handler_gaps(intent: ParsedIntent, all_text: str) -> List[str]:
    """Docs-only diffs should not satisfy 'create API' implementation claims."""
    if intent.action != "create" or intent.target != "api":
        return []
    signals = (
        "route",
        "@app",
        "@router",
        "def ",
        "jsonify",
        "flask.",
        "fastapi",
        "endpoint(",
    )
    if not any(s in all_text for s in signals):
        return [
            "API creation claimed but diff lacks route/handler implementation signals"
        ]
    return []


def _intent_specificity_gaps(raw_lower: str, all_text: str) -> List[str]:
    """Flag diffs that miss high-signal terms from the stated intent."""
    out: List[str] = []
    if "sql injection" in raw_lower:
        if not (
            "sql" in all_text
            or "sanitize" in all_text
            or "parameter" in all_text
            or "injection" in all_text
        ):
            out.append(
                "SQL injection cited in intent; diff lacks obvious SQL-safety changes"
            )
    if re.search(r"\blogin\b", raw_lower) and any(
        x in raw_lower for x in ("fix", "bug", "vulnerability", "injection", "security")
    ):
        if "login" not in all_text:
            out.append(
                "Intent references login; diff does not reflect login-related changes"
            )
    return out


def _diff_matches_intent(
    receipt: IntentReceipt,
    added_lines: List[str],
    changed_files: List[str],
    diff: str,
) -> tuple[bool, List[str]]:
    """Check if diff content aligns with stated intent using keyword matching."""
    intent = receipt.parsed_intent
    raw_lower = receipt.raw_text.lower()
    removed_lines = _extract_removed_lines(diff)
    all_text = " ".join(added_lines + removed_lines + changed_files).lower()

    action_keywords = _ACTION_KEYWORDS.get(intent.action, [])
    target_keywords = _TARGET_KEYWORDS.get(intent.target, [])

    action_match = any(kw in all_text for kw in action_keywords)
    target_match = any(kw in all_text for kw in target_keywords)

    if (
        not action_match
        and intent.action != "unknown"
        and target_match
        and intent.action in _ACTION_RELAX_WHEN_TARGET_MATCHES
    ):
        action_match = True

    goal_keywords: List[str] = []
    if intent.goal:
        goal_keywords = [
            w
            for w in intent.goal.lower().split()
            if len(w) > 3 and w not in _GOAL_BOILERPLATE_WORDS
        ]

    goal_match = (not goal_keywords) or any(kw in all_text for kw in goal_keywords)

    unrelated: List[str] = []

    if not action_match and intent.action != "unknown":
        unrelated.append(f"No {intent.action}-related keywords found in diff")
    if not target_match and intent.target != "unknown":
        unrelated.append(f"No {intent.target}-related patterns found in diff")
    if goal_keywords and not goal_match:
        unrelated.append(
            f"Goal keywords ({', '.join(goal_keywords[:3])}) not reflected in diff"
        )

    unrelated.extend(_intent_specificity_gaps(raw_lower, all_text))
    unrelated.extend(_create_api_handler_gaps(intent, all_text))

    has_drift = len(unrelated) > 0
    return has_drift, unrelated


def _detect_drift_regex(
    receipt: IntentReceipt,
    diff: str,
) -> DriftResult:
    """Regex-based drift detection fallback."""
    if not diff.strip():
        return DriftResult(has_drift=False, drift_severity="none")

    changed_files = _extract_changed_files(diff)
    added_lines = _extract_added_lines(diff)

    has_drift, unrelated = _diff_matches_intent(receipt, added_lines, changed_files, diff)

    if not has_drift:
        return DriftResult(has_drift=False, drift_severity="none")

    severity = "major" if len(unrelated) >= 2 else "minor"
    suggestion = (
        "Diff may not align with stated intent. "
        + " ".join(unrelated)
    )

    return DriftResult(
        has_drift=True,
        unrelated_additions=tuple(unrelated),
        suggestion=suggestion,
        drift_severity=severity,
    )


# ---------------------------------------------------------------------------
# LLM-based detection (structured intent)
# ---------------------------------------------------------------------------

def _detect_drift_llm(
    intent_dict: dict,
    diff: str,
) -> Optional[DriftResult]:
    """Call Claude to assess drift semantically. Returns None on failure."""
    try:
        import anthropic

        api_key = os.environ.get("ANTHROPIC_API_KEY", "")
        if not api_key:
            return None

        prompt_path = _PROMPTS_DIR / "assess_drift.txt"
        system = prompt_path.read_text(encoding="utf-8")

        user_payload = {
            "intent": intent_dict,
            "diff": diff,
        }
        user_json = json.dumps(user_payload, indent=2)

        client = anthropic.Anthropic(api_key=api_key)
        response = client.messages.create(
            model=os.environ.get("PROACTIVE_MODEL_DRIFT", "claude-3-haiku-20240307"),
            max_tokens=512,
            temperature=0.0,
            system=system,
            messages=[{"role": "user", "content": user_json}],
        )
        raw = response.content[0].text.strip()

        if raw.startswith("```"):
            lines = raw.split("\n")
            raw = "\n".join(lines[1:-1]).strip()

        result = json.loads(raw)
        if not isinstance(result, dict):
            return None

        has_drift = bool(result.get("has_drift", False))
        unrelated = [str(u) for u in result.get("unrelated", [])]
        reason = str(result.get("reason", ""))

        if not has_drift:
            return DriftResult(has_drift=False, drift_severity="none")

        severity = "major" if len(unrelated) >= 2 else "minor"
        return DriftResult(
            has_drift=True,
            unrelated_additions=tuple(unrelated),
            suggestion=reason,
            drift_severity=severity,
        )

    except Exception:
        logger.warning("Drift LLM detection failed, falling back to regex", exc_info=True)
        return None


# ---------------------------------------------------------------------------
# Semantic drift integration (Enhancement #4)
# ---------------------------------------------------------------------------

def _run_semantic_drift(
    receipt: IntentReceipt,
    diff: str,
) -> Optional["_SemanticInfo"]:
    """Run semantic drift detection safely. Returns None on failure."""
    try:
        from proactive.semantic_drift_detector import detect_semantic_drift
        result = detect_semantic_drift(receipt, diff)
        return _SemanticInfo(
            similarity=result.similarity_score,
            drift_level=result.drift_level,
            drifted_files=list(result.drifted_files),
            should_split=result.should_split,
            split_suggestion=result.split_suggestion,
        )
    except Exception:
        logger.warning("Semantic drift detection failed", exc_info=True)
        return None


@dataclass
class _SemanticInfo:
    """Internal container for semantic drift results."""
    similarity: float
    drift_level: str
    drifted_files: List[str]
    should_split: bool
    split_suggestion: str


def _merge_with_semantic(
    base_result: DriftResult,
    semantic: Optional["_SemanticInfo"],
) -> DriftResult:
    """Merge keyword/LLM drift result with semantic analysis."""
    if semantic is None:
        return base_result

    # TF-IDF similarity is noisy on short diffs and intent snippets; never
    # override a clean keyword/LLM pass. Semantic layer only enriches results
    # when the base detector already found drift.
    if not base_result.has_drift:
        return base_result

    # Combine unrelated additions
    unrelated = list(base_result.unrelated_additions)
    if semantic.drift_level in ("warning", "critical"):
        unrelated.append(
            f"Semantic similarity: {semantic.similarity:.2f} ({semantic.drift_level})"
        )
    if semantic.drifted_files:
        unrelated.append(
            f"Semantically drifted files: {', '.join(semantic.drifted_files[:3])}"
        )
    if semantic.should_split:
        unrelated.append(semantic.split_suggestion)

    # Escalate severity if semantic analysis found critical drift
    severity = base_result.drift_severity
    if semantic.drift_level == "critical" and severity != "major":
        severity = "major"
    elif semantic.drift_level == "warning" and severity == "none":
        severity = "minor"

    has_drift = base_result.has_drift or semantic.drift_level != "none"

    suggestion = base_result.suggestion
    if semantic.split_suggestion and semantic.split_suggestion not in suggestion:
        suggestion = f"{suggestion} {semantic.split_suggestion}".strip()

    return DriftResult(
        has_drift=has_drift,
        unrelated_additions=tuple(unrelated),
        suggestion=suggestion,
        drift_severity=severity,
    )


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def detect_drift(
    receipt: IntentReceipt,
    diff: str,
) -> DriftResult:
    """Detect scope drift between stated intent and actual diff.

    Uses Claude for semantic analysis when available, falls back to
    keyword-based matching when LLM is unavailable. Also runs semantic
    similarity analysis (Enhancement #4) to complement keyword/LLM checks.

    Args:
        receipt: Full IntentReceipt from COL layer (includes parsed intent and metadata).
        diff: Raw git diff string.

    Returns:
        DriftResult with has_drift, unrelated_additions, and severity.
    """
    if not diff.strip():
        return DriftResult(has_drift=False, drift_severity="none")

    # Build a dict with all relevant intent fields
    intent_dict = {
        "action": receipt.parsed_intent.action,
        "target": receipt.parsed_intent.target,
        "scope": receipt.parsed_intent.scope,
        "goal": receipt.parsed_intent.goal,
        "constraints": receipt.parsed_intent.constraints,
        "ambiguities": receipt.parsed_intent.ambiguities,
        "confidence": receipt.confidence,
    }

    # Run semantic drift detection (Enhancement #4)
    semantic_result = _run_semantic_drift(receipt, diff)

    llm_result = _detect_drift_llm(intent_dict, diff)
    if llm_result is not None:
        return _merge_with_semantic(llm_result, semantic_result)

    logger.info("LLM unavailable, using regex-based drift detection")
    regex_result = _detect_drift_regex(receipt, diff)
    return _merge_with_semantic(regex_result, semantic_result)