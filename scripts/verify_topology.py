#!/usr/bin/env python3
"""
verify_topology.py — TLC Golden Sandbox dual-topology (Gold Star) verifier.

Verifies that projects/sandbox-runtime and standalone/tlc-sandbox-app share the same
project_id in PROJECT_TOPOLOGY.json. Fail-closed: missing files or mismatch => exit 1.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Set


def _load_topology(path: Path) -> Dict[str, Any]:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def _sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def _py_names(dir_path: Path) -> Set[str]:
    if not dir_path.is_dir():
        return set()
    return {p.name for p in dir_path.glob("*.py")}


def verify_strict_core(root: Path) -> tuple[bool, List[str]]:
    """
    INVARIANT_16 parity: same Python modules under src/ and core/ (byte-identical).
    """
    integrated_src = root / "projects" / "sandbox-runtime" / "src"
    standalone_core = root / "standalone" / "tlc-sandbox-app" / "core"
    errors: List[str] = []
    a = _py_names(integrated_src)
    b = _py_names(standalone_core)
    if a != b:
        errors.append(f"Python module set mismatch: integrated={sorted(a)} standalone={sorted(b)}")
        return False, errors
    for name in sorted(a):
        pa = integrated_src / name
        pb = standalone_core / name
        if not pb.is_file():
            errors.append(f"missing mirrored file: {pb.relative_to(root)}")
            continue
        ha, hb = _sha256_file(pa), _sha256_file(pb)
        if ha != hb:
            errors.append(f"SHA-256 mismatch for {name}: integrated vs standalone mirror")
    return len(errors) == 0, errors


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument(
        "--root",
        type=Path,
        default=None,
        help="TLC repository root (default: parent of scripts/)",
    )
    p.add_argument(
        "--strict",
        action="store_true",
        help="Also require byte-identical Python under projects/sandbox-runtime/src and standalone/tlc-sandbox-app/core",
    )
    args = p.parse_args()
    script_dir = Path(__file__).resolve().parent
    root = (args.root or script_dir.parent).resolve()

    integrated = root / "projects" / "sandbox-runtime" / "PROJECT_TOPOLOGY.json"
    standalone = root / "standalone" / "tlc-sandbox-app" / ".tlc" / "PROJECT_TOPOLOGY.json"

    missing: list[str] = []
    if not integrated.is_file():
        missing.append(str(integrated.relative_to(root)))
    if not standalone.is_file():
        missing.append(str(standalone.relative_to(root)))

    if missing:
        print(
            "Constitutional Breach: PROJECT_TOPOLOGY.json missing from dual topology path(s):",
            file=sys.stderr,
        )
        for m in missing:
            print(f"  - {m}", file=sys.stderr)
        return 1

    try:
        a = _load_topology(integrated)
        b = _load_topology(standalone)
    except (OSError, json.JSONDecodeError) as e:
        print(f"ERROR: invalid topology JSON: {e}", file=sys.stderr)
        return 1

    id_a = a.get("project_id")
    id_b = b.get("project_id")
    if not isinstance(id_a, str) or not isinstance(id_b, str):
        print("ERROR: project_id must be a string in both topology files.", file=sys.stderr)
        return 1

    if id_a != id_b:
        print(
            f"ERROR: dual topology project_id mismatch: integrated={id_a!r} standalone={id_b!r}",
            file=sys.stderr,
        )
        return 1

    print(f"OK: dual topology linked for project_id={id_a!r}")
    print(f"  integrated:  {integrated.relative_to(root)}")
    print(f"  standalone:  {standalone.relative_to(root)}")

    if args.strict:
        ok, errs = verify_strict_core(root)
        if not ok:
            print("ERROR: --strict dual-topology core parity failed:", file=sys.stderr)
            for e in errs:
                print(f"  - {e}", file=sys.stderr)
            return 1
        print("OK: strict core parity (src/ <-> core/)")

    return 0


if __name__ == "__main__":
    sys.exit(main())
