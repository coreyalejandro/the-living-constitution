"""
Dataset loader — loads existing TLC evidence corpus into EvalCase format.

Bridges the existing datasets in 08-evaluation/datasets/ and
tests/failure_modes/ into the tlc_evals type system.
"""

from __future__ import annotations

import json
from pathlib import Path

from tlc_evals.evals.suite import EvalSuite

_DATASETS_ROOT = Path(__file__).parent.parent.parent / "datasets"
_FAILURE_MODES_ROOT = Path(__file__).parent.parent.parent.parent / "tests" / "failure_modes"


class DatasetLoader:
    """Loads TLC evidence datasets into EvalSuite objects."""

    @classmethod
    def load_failure_cases(cls) -> EvalSuite:
        """Load the canonical failure_cases.json dataset."""
        path = _DATASETS_ROOT / "failure_cases.json"
        if path.exists():
            return EvalSuite.from_json(path)
        return EvalSuite(name="failure_cases_empty", cases=[])

    @classmethod
    def load_failure_mode(cls, failure_type: str) -> EvalSuite:
        """
        Load test cases for a specific failure mode from tests/failure_modes/<FN>/.

        failure_type: "F1", "F2", "F3", "F4", or "F5"
        """
        path = _FAILURE_MODES_ROOT / failure_type
        if not path.exists():
            return EvalSuite(name=f"{failure_type}_empty", cases=[])

        all_cases = []
        suite = EvalSuite(name=f"{failure_type}_cases", cases=[])
        for json_file in sorted(path.glob("*.json")):
            try:
                data = json.loads(json_file.read_text(encoding="utf-8"))
                sub = EvalSuite.from_json.__func__(EvalSuite, json_file)  # type: ignore
                all_cases.extend(sub.cases)
            except Exception:
                continue

        suite.cases = all_cases
        return suite

    @classmethod
    def load_all(cls) -> EvalSuite:
        """Load all available datasets into one composite suite."""
        cases = []
        cases.extend(cls.load_failure_cases().cases)
        for ft in ("F1", "F2", "F3", "F4", "F5"):
            cases.extend(cls.load_failure_mode(ft).cases)
        return EvalSuite(name="tlc_all_datasets", cases=cases)
