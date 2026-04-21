"""
EvalSuite — collection of EvalCases with metadata.

A suite is the unit of organization for eval runs. Suites can be:
  - Constructed programmatically from eval classes
  - Loaded from YAML spec files
  - Filtered by failure type, invariant, severity, or tags
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import yaml

from tlc_evals.core.types import EvalCase, FailureType, Invariant, Severity


class EvalSuite:
    """
    An ordered collection of EvalCases with a name and metadata.

    EvalSuites can be composed from multiple BaseEval instances or
    loaded directly from YAML spec files.
    """

    def __init__(
        self,
        name: str,
        cases: list[EvalCase],
        description: str = "",
        tags: list[str] | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> None:
        self.name = name
        self.cases = cases
        self.description = description
        self.tags = tags or []
        self.metadata = metadata or {}

    def __len__(self) -> int:
        return len(self.cases)

    def __iter__(self):
        return iter(self.cases)

    def __repr__(self) -> str:
        return f"EvalSuite(name={self.name!r}, cases={len(self.cases)})"

    # ------------------------------------------------------------------
    # Factory methods
    # ------------------------------------------------------------------

    @classmethod
    def from_evals(cls, *evals: Any, name: str = "composite") -> "EvalSuite":
        """Build a suite by collecting cases from multiple BaseEval instances."""
        all_cases: list[EvalCase] = []
        for ev in evals:
            all_cases.extend(ev.cases())
        return cls(name=name, cases=all_cases)

    @classmethod
    def from_yaml(cls, path: str | Path) -> "EvalSuite":
        """Load a suite from a YAML spec file."""
        p = Path(path)
        with p.open() as f:
            spec: dict[str, Any] = yaml.safe_load(f)

        cases: list[EvalCase] = []
        for c in spec.get("cases", []):
            # Parse invariants
            invariant_strs: list[str] = c.get("invariants", [])
            invariants: list[Invariant] = []
            for s in invariant_strs:
                try:
                    invariants.append(Invariant(s))
                except ValueError:
                    pass

            # Parse failure type
            ft_str: str | None = c.get("failure_type")
            ft: FailureType | None = None
            if ft_str:
                try:
                    ft = FailureType(ft_str)
                except ValueError:
                    pass

            # Parse severity
            sev_str: str = c.get("severity", "ERROR").upper()
            sev: Severity = Severity(sev_str) if sev_str in Severity.__members__ else Severity.ERROR

            cases.append(
                EvalCase(
                    id=c.get("id", ""),
                    failure_type=ft,
                    invariants=invariants,
                    severity=sev,
                    input=c.get("input", {}),
                    ideal=c.get("ideal", ""),
                    source_ref=c.get("source_ref"),
                    tags=c.get("tags", []),
                )
            )

        return cls(
            name=spec.get("name", p.stem),
            cases=cases,
            description=spec.get("description", ""),
            tags=spec.get("tags", []),
            metadata=spec.get("metadata", {}),
        )

    @classmethod
    def from_json(cls, path: str | Path) -> "EvalSuite":
        """Load a suite from a JSON file (compatible with failure_cases.json format)."""
        p = Path(path)
        with p.open() as f:
            records: list[dict[str, Any]] = json.load(f)

        cases: list[EvalCase] = []
        for r in records:
            ft_str: str | None = r.get("failureType") or r.get("failure_type")
            ft: FailureType | None = None
            if ft_str:
                try:
                    ft = FailureType(ft_str)
                except ValueError:
                    pass

            inv_strs: list[str] = []
            cv_str = r.get("constitutionalViolation", "")
            if cv_str:
                inv_strs = [s.strip() for s in cv_str.split(",")]

            invariants: list[Invariant] = []
            for s in inv_strs:
                try:
                    invariants.append(Invariant(s))
                except ValueError:
                    pass

            cases.append(
                EvalCase(
                    id=r.get("id", ""),
                    failure_type=ft,
                    invariants=invariants,
                    severity=Severity(r.get("severity", "ERROR")),
                    input={
                        "description": r.get("description", ""),
                        "evidence_ref": r.get("evidenceRef", ""),
                    },
                    ideal=f"Detect and flag: {r.get('description', '')}",
                    source_ref=r.get("source", r.get("sourceRef")),
                    tags=[ft_str] if ft_str else [],
                )
            )

        return cls(name=p.stem, cases=cases)

    # ------------------------------------------------------------------
    # Filtering
    # ------------------------------------------------------------------

    def filter_by_failure_type(self, *fts: FailureType) -> "EvalSuite":
        filtered = [c for c in self.cases if c.failure_type in fts]
        return EvalSuite(
            name=f"{self.name}[filtered]",
            cases=filtered,
            description=self.description,
        )

    def filter_by_invariant(self, *invs: Invariant) -> "EvalSuite":
        inv_set = set(invs)
        filtered = [c for c in self.cases if inv_set.intersection(c.invariants)]
        return EvalSuite(name=f"{self.name}[filtered]", cases=filtered)

    def filter_by_severity(self, *severities: Severity) -> "EvalSuite":
        filtered = [c for c in self.cases if c.severity in severities]
        return EvalSuite(name=f"{self.name}[filtered]", cases=filtered)

    def filter_by_tag(self, *tags: str) -> "EvalSuite":
        tag_set = set(tags)
        filtered = [c for c in self.cases if tag_set.intersection(c.tags)]
        return EvalSuite(name=f"{self.name}[filtered]", cases=filtered)
