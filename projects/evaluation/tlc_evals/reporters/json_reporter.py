"""JSON reporter — full structured output for programmatic consumption."""

from __future__ import annotations

import json
from pathlib import Path

from tlc_evals.core.types import EvalSummary


class JSONReporter:
    """Serialises EvalSummary to JSON."""

    def generate(self, summary: EvalSummary) -> str:
        return summary.model_dump_json(indent=2)

    def write(self, summary: EvalSummary, path: str | Path) -> None:
        Path(path).write_text(self.generate(summary), encoding="utf-8")

    def load(self, path: str | Path) -> EvalSummary:
        data = json.loads(Path(path).read_text(encoding="utf-8"))
        return EvalSummary.model_validate(data)
