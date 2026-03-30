#!/usr/bin/env python3
"""
verify_governance_chain.py

Machine-checkable governance chain validation for TLC:
- invariant registry completeness
- doctrine map references
- enforcement map executable hooks exist
- agent capabilities JSON parseable
- evidence ledger seed uses only verified | unverified | missing
- MASTER_PROJECT_INVENTORY.json governance_artifacts + timestamp sync with .md

Exit codes: 0 OK, 1 validation failure, 2 usage/read error
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List


def _parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument(
        "--root",
        type=Path,
        default=None,
        help="TLC repository root (default: parent of scripts/)",
    )
    return p.parse_args()


def _load_json(path: Path) -> Dict[str, Any]:
    try:
        with path.open("r", encoding="utf-8") as f:
            return json.load(f)
    except (OSError, json.JSONDecodeError) as e:
        print(f"ERROR: cannot read JSON: {path}: {e}", file=sys.stderr)
        sys.exit(2)


def _fail(msg: str) -> None:
    print(f"ERROR: {msg}", file=sys.stderr)


def main() -> None:
    args = _parse_args()
    script_dir = Path(__file__).resolve().parent
    root = (args.root or script_dir.parent).resolve()

    errors: List[str] = []

    required_paths = [
        root / "00-constitution" / "invariant-registry.json",
        root / "00-constitution" / "doctrine-to-invariant.map.json",
        root / "03-enforcement" / "enforcement-map.json",
        root / "02-agents" / "agent-capabilities.json",
        root / "verification" / "evidence-ledger.schema.json",
        root / "verification" / "evidence-ledger" / "seed.json",
        root / "verification" / "governance-verification.template.json",
    ]
    for p in required_paths:
        if not p.is_file():
            errors.append(f"missing required file: {p.relative_to(root)}")

    inv_path = root / "00-constitution" / "invariant-registry.json"
    doctrine_path = root / "00-constitution" / "doctrine-to-invariant.map.json"
    enf_path = root / "03-enforcement" / "enforcement-map.json"
    agents_path = root / "02-agents" / "agent-capabilities.json"
    seed_path = root / "verification" / "evidence-ledger" / "seed.json"
    inventory_path = root / "MASTER_PROJECT_INVENTORY.json"
    inventory_md_path = root / "MASTER_PROJECT_INVENTORY.md"

    if errors:
        for e in errors:
            _fail(e)
        sys.exit(1)

    reg = _load_json(inv_path)
    inv_ids = {x["id"] for x in reg.get("invariants", []) if "id" in x}
    expected = {f"INVARIANT_{i:02d}" for i in range(1, 11)}
    if inv_ids != expected:
        errors.append(
            f"invariant-registry.json must define exactly INVARIANT_01..INVARIANT_10; got {sorted(inv_ids)}"
        )

    for row in reg.get("invariants", []):
        for key in ("enforcement_mechanism", "evidence_path_or_rule"):
            if not str(row.get(key, "")).strip():
                errors.append(f"invariant {row.get('id')}: missing {key}")

    for fc in reg.get("failure_class_artifacts", []):
        md_rel = fc.get("markdown")
        if md_rel:
            mp = root / md_rel
            if not mp.is_file():
                errors.append(f"failure class {fc.get('id')}: markdown missing at {md_rel}")

    doctrine = _load_json(doctrine_path)
    for key in ("doctrines", "articles"):
        for item in doctrine.get(key, []):
            ids = list(item.get("invariant_ids") or [])
            if not ids:
                errors.append(f"{key} entry {item.get('id')}: invariant_ids empty")
            for i in ids:
                if i not in inv_ids:
                    errors.append(f"{key} {item.get('id')}: unknown invariant {i}")

    enf = _load_json(enf_path)
    for mod in enf.get("modules", []):
        hook = mod.get("enforcement_hook")
        if not hook:
            errors.append(f"enforcement module {mod.get('id')}: missing enforcement_hook")
            continue
        if hook.endswith(".py"):
            hp = root / hook
            if not hp.is_file():
                errors.append(f"enforcement hook not found: {hook}")
        elif hook.endswith(".yml") or hook.endswith(".yaml"):
            hp = root / hook
            if not hp.is_file():
                errors.append(f"workflow hook not found: {hook}")

    agents = _load_json(agents_path)
    for ag in agents.get("agents", []):
        aid = ag.get("id")
        for fld in ("allowed_actions", "forbidden_actions", "required_output_constraints"):
            if not isinstance(ag.get(fld), list) or len(ag.get(fld) or []) == 0:
                errors.append(f"agent {aid}: {fld} must be non-empty list")

    seed = _load_json(seed_path)
    valid_states = {"verified", "unverified", "missing"}
    for rec in seed.get("records", []):
        st = rec.get("evidence_state")
        if st not in valid_states:
            errors.append(
                f"evidence record {rec.get('record_id')}: evidence_state must be one of {valid_states}"
            )

    data = _load_json(inventory_path)
    gov = data.get("governance_artifacts") or {}
    canonical = gov.get("canonical_paths") or {}
    if not canonical:
        errors.append("MASTER_PROJECT_INVENTORY.json: governance_artifacts.canonical_paths missing or empty")
    else:
        paths_seen: Set[str] = set()
        for k, rel in canonical.items():
            if rel in paths_seen:
                errors.append(f"duplicate canonical path for keys in governance_artifacts: {rel}")
            paths_seen.add(rel)
            p = root / rel
            if not p.is_file():
                errors.append(f"governance canonical path missing on disk: {rel}")

    meta = data.get("meta") or {}
    ts = meta.get("generated_at_utc")
    if not ts:
        errors.append("MASTER_PROJECT_INVENTORY.json: meta.generated_at_utc missing")
    else:
        try:
            md_text = inventory_md_path.read_text(encoding="utf-8")
        except OSError as e:
            print(f"ERROR: cannot read {inventory_md_path}: {e}", file=sys.stderr)
            sys.exit(2)
        if ts not in md_text:
            errors.append(
                "INVARIANT_04: MASTER_PROJECT_INVENTORY.md must contain the same "
                f"meta.generated_at_utc token as JSON: {ts!r}"
            )

    if errors:
        print("ERROR: governance chain validation failed:", file=sys.stderr)
        for e in errors:
            print(f"  - {e}", file=sys.stderr)
        sys.exit(1)

    print("OK: governance chain validation passed")
    sys.exit(0)


if __name__ == "__main__":
    main()
