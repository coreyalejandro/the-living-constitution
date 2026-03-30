#!/usr/bin/env python3
"""
verify_cross_repo_consistency.py

PASS 9: Compare canonical The Living Constitution governance artifacts to a target
repository (e.g. projects/consentchain) and fail on drift.

Compares JSON byte-for-byte after canonical JSON normalization (sorted keys),
and validates MATRIX.md / GOVERNANCE_SYSTEM_CARD.md structural anchors.

Exit: 0 OK, 1 drift, 2 usage/read error
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Tuple


JSON_RELPATHS: Tuple[str, ...] = (
    "00-constitution/invariant-registry.json",
    "00-constitution/doctrine-to-invariant.map.json",
    "00-constitution/role-registry.json",
    "03-enforcement/enforcement-map.json",
    "verification/evidence-ledger.schema.json",
    "verification/governance-verification-run.schema.json",
    "verification/regression-ledger.schema.json",
    "verification/governance-verification.template.json",
    "verification/tip-state-policy.json",
    "verification/review-escalation-policy.json",
    "verification/pass7-branch-verification-policy.json",
)

MATRIX_HEADER_EXPECTED = (
    "| # | Resume Claim | Project | Evidence Location | Verification Method | Status | Result |"
)

CARD_ANCHORS: Tuple[str, ...] = (
    "**Governance scope:**",
    "**Continuously evaluated:**",
    "**Known failure modes:**",
    "Escalation thresholds (machine-readable):",
    "Tip-state exactness (PASS 6 / PASS 7):",
    "## Separation of Powers",
    "Current evidence boundary:",
    "Not claimed:",
    "**Contract:**",
)


def _parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument(
        "--canonical-root",
        type=Path,
        required=True,
        help="TLC repository root (canonical), or 'the-living-constitution' next to target in CI",
    )
    p.add_argument(
        "--target-root",
        type=Path,
        required=True,
        help="Target repository root (e.g. ConsentChain checkout)",
    )
    return p.parse_args()


def _resolve_canonical_root(canonical_root: Path, target_root: Path) -> Path:
    """Prefer explicit path; if missing, allow ConsentChain-as-submodule under TLC (../.. from target)."""
    c = canonical_root.resolve()
    marker = c / "00-constitution" / "invariant-registry.json"
    if marker.is_file():
        return c
    alt = target_root.resolve().parent.parent
    alt_m = alt / "00-constitution" / "invariant-registry.json"
    if alt_m.is_file():
        print(
            f"verify_cross_repo_consistency: using TLC root fallback {alt} (canonical path {c!s} not found)",
            file=sys.stderr,
        )
        return alt
    return c


def _load_json(path: Path) -> Dict[str, Any]:
    with path.open("r", encoding="utf-8") as f:
        data = json.load(f)
    if not isinstance(data, dict):
        raise ValueError(f"expected object in {path}")
    return data


def _norm_json(data: Any) -> str:
    return json.dumps(data, sort_keys=True, ensure_ascii=False, indent=2) + "\n"


def _matrix_header_line(text: str) -> str:
    for line in text.splitlines():
        s = line.strip()
        if s.startswith("| # |") and "Resume Claim" in s:
            return s
    return ""


def _check_card(path: Path, errors: List[str]) -> None:
    if not path.is_file():
        errors.append(f"missing {path}")
        return
    body = path.read_text(encoding="utf-8", errors="replace")
    for anchor in CARD_ANCHORS:
        if anchor not in body:
            errors.append(f"GOVERNANCE_SYSTEM_CARD.md missing anchor: {anchor!r}")


def main() -> int:
    args = _parse_args()
    target = args.target_root.resolve()
    canon = _resolve_canonical_root(args.canonical_root, args.target_root)
    errors: List[str] = []

    for rel in JSON_RELPATHS:
        a = canon / rel
        b = target / rel
        if not a.is_file():
            errors.append(f"canonical missing: {rel}")
            continue
        if not b.is_file():
            errors.append(f"target missing: {rel}")
            continue
        try:
            ja = _load_json(a)
            jb = _load_json(b)
        except (OSError, json.JSONDecodeError, ValueError) as e:
            errors.append(f"{rel}: read/parse error: {e}")
            continue
        if _norm_json(ja) != _norm_json(jb):
            errors.append(f"JSON drift (normalized): {rel}")

    for name in ("verification/MATRIX.md", "verification/GOVERNANCE_SYSTEM_CARD.md"):
        a = canon / name
        b = target / name
        if not a.is_file() or not b.is_file():
            errors.append(f"missing markdown: {name}")
            continue
        if name.endswith("MATRIX.md"):
            ha = _matrix_header_line(a.read_text(encoding="utf-8", errors="replace"))
            hb = _matrix_header_line(b.read_text(encoding="utf-8", errors="replace"))
            if ha != MATRIX_HEADER_EXPECTED.strip():
                errors.append(f"canonical MATRIX.md header row unexpected: {ha!r}")
            if hb != MATRIX_HEADER_EXPECTED.strip():
                errors.append(f"target MATRIX.md header must match canonical categories: {hb!r}")
            if ha != hb:
                errors.append("MATRIX.md header row differs between canonical and target")
        else:
            _check_card(a, errors)
            _check_card(b, errors)

    if errors:
        print("verify_cross_repo_consistency: FAIL", file=sys.stderr)
        for e in errors:
            print(f"  - {e}", file=sys.stderr)
        return 1

    print("verify_cross_repo_consistency: OK (canonical vs target)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
