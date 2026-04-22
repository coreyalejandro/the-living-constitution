"""
BaseInvariant — abstract base class for constitutional invariant checkers.

Each invariant (I1–I6) is an independent, composable checker. Invariants
run deterministically (no model calls) and return a list of violations.
They are designed to be composed by the InvariantChecker orchestrator.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import ClassVar

from tlc_evals.core.types import Invariant, InvariantViolation


class BaseInvariant(ABC):
    """Abstract base for invariant checkers."""

    invariant: ClassVar[Invariant]
    description: ClassVar[str] = ""

    @abstractmethod
    def check(self, text: str, context: dict | None = None) -> list[InvariantViolation]:
        """
        Check text for violations of this invariant.

        Args:
            text: The agent output to check.
            context: Optional additional context (e.g., code diff, filesystem state).

        Returns:
            List of InvariantViolation. Empty list = no violations.
        """
        ...

    def passes(self, text: str, context: dict | None = None) -> bool:
        """True if no violations are found."""
        return len(self.check(text, context)) == 0
