"""
SARIF Reporter — Static Analysis Results Interchange Format output.

Generates SARIF 2.1.0 compliant reports for CI/CD integration.
SARIF is the standard format for GitHub Code Scanning, GitLab SAST,
and most security/quality gates.

Using SARIF allows TLC eval results to surface directly in pull request
checks and CI pipelines without custom tooling.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from tlc_evals.core.types import EvalSummary, EvalResult, Severity

_TOOL_NAME = "tlc-evals"
_TOOL_VERSION = "0.1.0"
_TOOL_URI = "https://github.com/coreyalejandro/the-living-constitution"

_SEVERITY_TO_SARIF = {
    Severity.ERROR: "error",
    Severity.WARNING: "warning",
    Severity.INFO: "note",
    Severity.PASS: "note",
}

# Invariant rule definitions for SARIF
_INVARIANT_RULES = {
    "I1": {
        "id": "TLC-I1",
        "name": "EvidenceFirst",
        "shortDescription": "I1: Evidence-First — claims require epistemic tags.",
        "helpUri": f"{_TOOL_URI}/blob/main/THE_LIVING_CONSTITUTION.md#i1-evidence-first",
        "properties": {"tags": ["epistemic-safety", "constitutional"]},
    },
    "I2": {
        "id": "TLC-I2",
        "name": "NoPhantomWork",
        "shortDescription": "I2: No Phantom Work — completion claims require evidence.",
        "helpUri": f"{_TOOL_URI}/blob/main/THE_LIVING_CONSTITUTION.md#i2-no-phantom-work",
        "properties": {"tags": ["phantom-completion", "constitutional"]},
    },
    "I3": {
        "id": "TLC-I3",
        "name": "ConfidenceVerification",
        "shortDescription": "I3: Confidence must match verification quality.",
        "helpUri": f"{_TOOL_URI}/blob/main/THE_LIVING_CONSTITUTION.md#i3-confidence",
        "properties": {"tags": ["calibration", "constitutional"]},
    },
    "I4": {
        "id": "TLC-I4",
        "name": "Traceability",
        "shortDescription": "I4: Consequential actions require traceable rationale.",
        "helpUri": f"{_TOOL_URI}/blob/main/THE_LIVING_CONSTITUTION.md#i4-traceability",
        "properties": {"tags": ["traceability", "constitutional"]},
    },
    "I5": {
        "id": "TLC-I5",
        "name": "SafetyOverFluency",
        "shortDescription": "I5: Safety over fluency — no epistemic understatement.",
        "helpUri": f"{_TOOL_URI}/blob/main/THE_LIVING_CONSTITUTION.md#i5-safety-fluency",
        "properties": {"tags": ["safety", "constitutional"]},
    },
    "I6": {
        "id": "TLC-I6",
        "name": "FailClosed",
        "shortDescription": "I6: Fail closed — halt and escalate under uncertainty.",
        "helpUri": f"{_TOOL_URI}/blob/main/THE_LIVING_CONSTITUTION.md#i6-fail-closed",
        "properties": {"tags": ["fail-closed", "constitutional"]},
    },
}


class SARIFReporter:
    """Generates SARIF 2.1.0 reports from EvalSummary."""

    def generate(self, summary: EvalSummary) -> dict[str, Any]:
        """Generate SARIF dict from EvalSummary."""
        rules = list(_INVARIANT_RULES.values())

        results: list[dict[str, Any]] = []
        for eval_result in summary.results:
            results.extend(self._result_to_sarif(eval_result))

        return {
            "$schema": "https://raw.githubusercontent.com/oasis-tcs/sarif-spec/master/Schemata/sarif-schema-2.1.0.json",
            "version": "2.1.0",
            "runs": [
                {
                    "tool": {
                        "driver": {
                            "name": _TOOL_NAME,
                            "version": _TOOL_VERSION,
                            "informationUri": _TOOL_URI,
                            "rules": rules,
                        }
                    },
                    "results": results,
                    "properties": {
                        "runId": summary.run_id,
                        "suiteName": summary.eval_suite_name,
                        "passRate": summary.pass_rate,
                        "meanScore": summary.mean_score,
                        "totalCases": summary.total,
                    },
                }
            ],
        }

    def write(self, summary: EvalSummary, path: str | Path) -> None:
        """Write SARIF JSON to file."""
        sarif = self.generate(summary)
        Path(path).write_text(json.dumps(sarif, indent=2), encoding="utf-8")

    def _result_to_sarif(self, result: EvalResult) -> list[dict[str, Any]]:
        """Convert a single EvalResult to SARIF result entries."""
        sarif_results: list[dict[str, Any]] = []

        for violation in result.violations:
            inv_key = violation.invariant.value
            rule = _INVARIANT_RULES.get(inv_key, _INVARIANT_RULES["I1"])

            sarif_results.append(
                {
                    "ruleId": rule["id"],
                    "level": _SEVERITY_TO_SARIF.get(violation.severity, "warning"),
                    "message": {
                        "text": (
                            f"[{result.case_id}] {violation.description} "
                            f"Evidence: {violation.evidence[:100]}"
                        )
                    },
                    "locations": [
                        {
                            "logicalLocations": [
                                {
                                    "name": result.case_id,
                                    "decoratedName": f"{result.eval_name}::{result.case_id}",
                                    "kind": "function",
                                }
                            ]
                        }
                    ],
                    "properties": {
                        "caseId": result.case_id,
                        "evalName": result.eval_name,
                        "verdict": result.verdict.value,
                        "score": result.score,
                        "failureType": result.failure_type.value
                        if result.failure_type
                        else None,
                    },
                }
            )

        return sarif_results
