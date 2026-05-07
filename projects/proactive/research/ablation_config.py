"""
PROACTIVE Ablation Config — Variant Definitions

Defines 4 agent variants for ablation study:
  1. PROACTIVE (full)    — COL + Contract + Validator (I1-I6) + Drift
  2. PROACTIVE-lite      — COL + Contract + Validator (I1-I5 only)
  3. PROACTIVE-strict    — Full + all violations block (no warnings)
  4. Baseline            — No safety checks
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional, Set

__all__ = [
    "VariantName",
    "VariantConfig",
    "VARIANTS",
    "get_variant",
    "list_variants",
]


class VariantName(str, Enum):
    FULL = "proactive-full"
    LITE = "proactive-lite"
    STRICT = "proactive-strict"
    BASELINE = "baseline"


@dataclass(frozen=True)
class VariantConfig:
    """Configuration for a single ablation variant."""

    name: str
    description: str
    use_col: bool = True
    use_contract_window: bool = True
    use_validator: bool = True
    use_drift_detector: bool = True
    invariants_enabled: Set[str] = field(default_factory=lambda: {"I1", "I2", "I3", "I4", "I5", "I6"})
    block_on_warnings: bool = False
    block_on_errors: bool = True

    def to_dict(self) -> Dict:
        return {
            "name": self.name,
            "description": self.description,
            "use_col": self.use_col,
            "use_contract_window": self.use_contract_window,
            "use_validator": self.use_validator,
            "use_drift_detector": self.use_drift_detector,
            "invariants_enabled": sorted(self.invariants_enabled),
            "block_on_warnings": self.block_on_warnings,
            "block_on_errors": self.block_on_errors,
        }

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), indent=2)

    @classmethod
    def from_dict(cls, data: Dict) -> "VariantConfig":
        return cls(
            name=data["name"],
            description=data["description"],
            use_col=data.get("use_col", True),
            use_contract_window=data.get("use_contract_window", True),
            use_validator=data.get("use_validator", True),
            use_drift_detector=data.get("use_drift_detector", True),
            invariants_enabled=set(data.get("invariants_enabled", ["I1", "I2", "I3", "I4", "I5", "I6"])),
            block_on_warnings=data.get("block_on_warnings", False),
            block_on_errors=data.get("block_on_errors", True),
        )


# ---------------------------------------------------------------------------
# Variant definitions
# ---------------------------------------------------------------------------

VARIANTS: Dict[str, VariantConfig] = {
    VariantName.FULL: VariantConfig(
        name=VariantName.FULL,
        description="Full PROACTIVE framework with all layers and invariants.",
        use_col=True,
        use_contract_window=True,
        use_validator=True,
        use_drift_detector=True,
        invariants_enabled={"I1", "I2", "I3", "I4", "I5", "I6"},
        block_on_warnings=False,
        block_on_errors=True,
    ),
    VariantName.LITE: VariantConfig(
        name=VariantName.LITE,
        description="PROACTIVE without drift detector. I1-I5 only.",
        use_col=True,
        use_contract_window=True,
        use_validator=True,
        use_drift_detector=False,
        invariants_enabled={"I1", "I2", "I3", "I4", "I5"},
        block_on_warnings=False,
        block_on_errors=True,
    ),
    VariantName.STRICT: VariantConfig(
        name=VariantName.STRICT,
        description="Full PROACTIVE but all violations block (no warnings).",
        use_col=True,
        use_contract_window=True,
        use_validator=True,
        use_drift_detector=True,
        invariants_enabled={"I1", "I2", "I3", "I4", "I5", "I6"},
        block_on_warnings=True,
        block_on_errors=True,
    ),
    VariantName.BASELINE: VariantConfig(
        name=VariantName.BASELINE,
        description="No safety checks. Baseline for comparison.",
        use_col=False,
        use_contract_window=False,
        use_validator=False,
        use_drift_detector=False,
        invariants_enabled=set(),
        block_on_warnings=False,
        block_on_errors=False,
    ),
}


def get_variant(name: str) -> VariantConfig:
    """Get a variant config by name."""
    if name in VARIANTS:
        return VARIANTS[name]
    raise ValueError(f"Unknown variant: {name}. Available: {list(VARIANTS.keys())}")


def list_variants() -> List[str]:
    """List all available variant names."""
    return list(VARIANTS.keys())
