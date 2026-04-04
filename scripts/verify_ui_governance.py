#!/usr/bin/env python3
"""
verify_ui_governance.py — TLC Control Plane UI (control-plane-001) governance binding.

Read-only checks: jail allows control-plane roots; app.py forbids os/subprocess;
enforcement-map lists every invariant in 00-constitution/invariant-registry.json and
references that registry path.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any, Dict, List, Set


def _load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def _expected_invariant_ids(registry_path: Path) -> Set[str]:
    data = _load_json(registry_path)
    inv = data.get("invariants")
    if not isinstance(inv, list):
        raise ValueError("invariant-registry.json missing invariants[]")
    out: Set[str] = set()
    for row in inv:
        if isinstance(row, dict) and isinstance(row.get("id"), str):
            out.add(row["id"])
    return out


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument(
        "--root",
        type=Path,
        default=None,
        help="TLC repository root (default: parent of scripts/)",
    )
    args = p.parse_args()
    script_dir = Path(__file__).resolve().parent
    root = (args.root or script_dir.parent).resolve()

    jail_path = root / "projects" / "sandbox-runtime" / "src" / "jail.py"
    if not jail_path.is_file():
        print(f"ERROR: missing {jail_path.relative_to(root)}", file=sys.stderr)
        return 1
    jail_text = jail_path.read_text(encoding="utf-8")
    for needle in (
        '("projects", "tlc-control-plane")',
        '("standalone", "tlc-ui-desktop")',
    ):
        if needle not in jail_text:
            print(f"ERROR: jail.py must include allowed root segment {needle!r}", file=sys.stderr)
            return 1
    if '"pathlib"' not in jail_text and "'pathlib'" not in jail_text:
        print("ERROR: jail.py import whitelist must include pathlib for UI entry", file=sys.stderr)
        return 1

    app_path = root / "projects" / "tlc-control-plane" / "src" / "app.py"
    if not app_path.is_file():
        print(f"ERROR: missing {app_path.relative_to(root)}", file=sys.stderr)
        return 1
    app_text = app_path.read_text(encoding="utf-8")
    if re.search(r"^\s*import\s+os\s*$", app_text, re.M) or re.search(
        r"^\s*import\s+subprocess\s*$", app_text, re.M
    ):
        print("ERROR: app.py must not import os or subprocess", file=sys.stderr)
        return 1

    reg_path = root / "00-constitution" / "invariant-registry.json"
    expected_ids = _expected_invariant_ids(reg_path)

    em_path = root / "projects" / "tlc-control-plane" / "governance" / "enforcement-map.json"
    if not em_path.is_file():
        print(f"ERROR: missing {em_path.relative_to(root)}", file=sys.stderr)
        return 1
    em: Dict[str, Any] = _load_json(em_path)
    ref = em.get("canonical_invariant_registry_ref")
    if ref != "00-constitution/invariant-registry.json":
        print(
            f"ERROR: enforcement-map canonical_invariant_registry_ref must be "
            f"00-constitution/invariant-registry.json (got {ref!r})",
            file=sys.stderr,
        )
        return 1
    modules = em.get("modules")
    if not isinstance(modules, list) or not modules:
        print("ERROR: enforcement-map modules[] required", file=sys.stderr)
        return 1
    listed: Set[str] = set()
    for mod in modules:
        if isinstance(mod, dict):
            ids = mod.get("invariant_ids")
            if isinstance(ids, list):
                for x in ids:
                    if isinstance(x, str):
                        listed.add(x)
    missing = sorted(expected_ids - listed)
    extra = sorted(listed - expected_ids)
    if missing:
        print(f"ERROR: enforcement-map missing invariant_ids ({len(missing)}): {missing}", file=sys.stderr)
        return 1
    if extra:
        print(f"ERROR: enforcement-map unknown invariant_ids: {extra}", file=sys.stderr)
        return 1

    print("OK: control-plane UI governance binding verified")
    print(f"  invariants mapped: {len(listed)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
