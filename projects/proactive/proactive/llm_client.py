"""
PROACTIVE LLM Client

Provides semantic analysis via Anthropic Claude SDK with graceful degradation.
All methods return None when the API key is not configured or when an error
occurs, allowing callers to fall back to regex-based analysis.
"""

from __future__ import annotations

import json
import logging
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Optional

logger = logging.getLogger(__name__)

_PROMPTS_DIR = Path(__file__).parent / "prompts"

__all__ = [
    "LLMConfig",
    "LLMClient",
]


@dataclass(frozen=True)
class LLMConfig:
    """Configuration for the Anthropic Claude LLM client."""

    api_key: str = ""
    model: str = "claude-3-haiku-20240307"
    max_tokens: int = 1024
    temperature: float = 0.0

    @property
    def enabled(self) -> bool:
        """True when api_key is present and non-empty."""
        return bool(self.api_key.strip())


def _load_prompt(name: str) -> str:
    """Load a prompt template from the prompts directory."""
    path = _PROMPTS_DIR / name
    return path.read_text(encoding="utf-8")


def _parse_json_response(text: str) -> Any:
    """Extract JSON from an LLM response, handling markdown fences."""
    cleaned = text.strip()
    if cleaned.startswith("```"):
        lines = cleaned.split("\n")
        # Remove first and last fence lines
        start = 1
        end = len(lines)
        for i in range(len(lines) - 1, 0, -1):
            if lines[i].strip().startswith("```"):
                end = i
                break
        cleaned = "\n".join(lines[start:end]).strip()
    return json.loads(cleaned)


class LLMClient:
    """Anthropic Claude client with graceful degradation.

    When disabled (no API key), all methods return None.
    When errors occur, all methods catch exceptions and return None.
    """

    def __init__(self, config: LLMConfig) -> None:
        self._config = config
        self._client: Any = None
        if config.enabled:
            try:
                import anthropic
                self._client = anthropic.Anthropic(api_key=config.api_key)
            except Exception:
                logger.warning("Failed to initialize Anthropic client")

    @classmethod
    def from_env(cls) -> LLMClient:
        """Create an LLMClient from environment variables.

        Reads ANTHROPIC_API_KEY from the environment.
        """
        return cls(LLMConfig(api_key=os.environ.get("ANTHROPIC_API_KEY", "")))

    @property
    def enabled(self) -> bool:
        """True when the client is configured and ready."""
        return self._client is not None

    def _call(
        self, system: str, user: str, model_override: str = "",
    ) -> Optional[str]:
        """Make a single LLM call. Returns None on any failure."""
        if not self.enabled:
            return None
        try:
            model = model_override or self._config.model
            response = self._client.messages.create(
                model=model,
                max_tokens=self._config.max_tokens,
                temperature=self._config.temperature,
                system=system,
                messages=[{"role": "user", "content": user}],
            )
            return response.content[0].text
        except Exception:
            logger.warning("LLM call failed", exc_info=True)
            return None

    def extract_claims_semantic(
        self, text: str,
    ) -> Optional[list[dict[str, Any]]]:
        """Extract verifiable claims from MR text using semantic analysis.

        Returns a list of {text, claim_type, confidence} dicts,
        or None if LLM is unavailable.
        """
        if not self.enabled:
            return None
        try:
            prompt = _load_prompt("extract_claims.txt")
            model = os.environ.get("PROACTIVE_MODEL_CLAIMS", "")
            raw = self._call(prompt, text, model_override=model)
            if raw is None:
                return None
            result = _parse_json_response(raw)
            if not isinstance(result, list):
                return None
            return [
                {
                    "text": str(item.get("text", "")),
                    "claim_type": str(item.get("claim_type", "unknown")),
                    "confidence": float(item.get("confidence", 0.5)),
                }
                for item in result
                if isinstance(item, dict) and item.get("text")
            ]
        except Exception:
            logger.warning("extract_claims_semantic failed", exc_info=True)
            return None

    def check_invariants_semantic(
        self,
        content: str,
        file_path: str,
        intent: Optional[dict] = None,
    ) -> Optional[list[dict[str, Any]]]:
        """Check I1-I6 invariants at semantic level.

        Args:
            content: The text to check.
            file_path: Label for the source.
            intent: Structured intent dict from COL (action, target, scope, etc.)

        Returns a list of violation dicts, or None if LLM is unavailable.
        Each dict has: {invariant, severity, message, line, suggested_fix, evidence}.
        """
        if not self.enabled:
            return None
        try:
            prompt = _load_prompt("check_invariants.txt")
            user_payload = {
                "intent": intent if intent else {},
                "content": content,
                "file_path": file_path,
            }
            user_json = json.dumps(user_payload, indent=2)
            model = os.environ.get("PROACTIVE_MODEL_INVARIANTS", "")
            raw = self._call(prompt, user_json, model_override=model)
            if raw is None:
                return None
            result = _parse_json_response(raw)
            if not isinstance(result, list):
                return None
            return [
                {
                    "invariant": str(item.get("invariant", "")),
                    "severity": str(item.get("severity", "WARNING")),
                    "message": str(item.get("message", "")),
                    "line": int(item.get("line", 1)),
                    "suggested_fix": str(item.get("suggested_fix", "")),
                    "evidence": item.get("evidence", {}),
                }
                for item in result
                if isinstance(item, dict) and item.get("invariant")
            ]
        except Exception:
            logger.warning("check_invariants_semantic failed", exc_info=True)
            return None

    def assess_drift_semantic(
        self,
        intent_description: str,
        diff: str,
        intent: Optional[dict] = None,
    ) -> Optional[dict[str, Any]]:
        """Assess whether a diff drifts from the stated intent.

        Args:
            intent_description: Original text description of intent (for context).
            diff: Unified diff of changes.
            intent: Structured intent dict from COL (action, target, scope, etc.)

        Returns {has_drift, unrelated, reason}, or None if unavailable.
        """
        if not self.enabled:
            return None
        try:
            prompt = _load_prompt("assess_drift.txt")
            user_payload = {
                "intent": intent if intent else {},
                "diff": diff,
            }
            user_json = json.dumps(user_payload, indent=2)
            model = os.environ.get("PROACTIVE_MODEL_DRIFT", "")
            raw = self._call(prompt, user_json, model_override=model)
            if raw is None:
                return None
            result = _parse_json_response(raw)
            if not isinstance(result, dict):
                return None
            return {
                "has_drift": bool(result.get("has_drift", False)),
                "unrelated": list(result.get("unrelated", [])),
                "reason": str(result.get("reason", "")),
            }
        except Exception:
            logger.warning("assess_drift_semantic failed", exc_info=True)
            return None