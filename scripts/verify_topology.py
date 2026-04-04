#!/usr/bin/env python3
"""
verify_topology.py — TLC dual-topology (Gold Star) verifier.

Loads `dual_topology_registry` from MASTER_PROJECT_INVENTORY.json and verifies each
pair: integrated PROJECT_TOPOLOGY.json vs standalone .tlc/PROJECT_TOPOLOGY.json
(project_id parity). With --strict, requires byte-identical *.py under integrated src/
and standalone core/.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Set, Tuple


def _load_json(path: Path) -> Dict[str, Any]:
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


def verify_strict_core_pair(
    root: Path,
    integrated_path: str,
    standalone_repo_path: str,
) -> Tuple[bool, List[str]]:
    """INVARIANT_16 parity: same Python modules under integrated src/ and standalone core/."""
    integrated_src = root / integrated_path / "src"
    standalone_core = root / standalone_repo_path / "core"
    errors: List[str] = []
    label = f"{integrated_path} <-> {standalone_repo_path}"
    a = _py_names(integrated_src)
    b = _py_names(standalone_core)
    if a != b:
        errors.append(
            f"{label}: Python module set mismatch integrated={sorted(a)} standalone={sorted(b)}"
        )
        return False, errors
    for name in sorted(a):
        pa = integrated_src / name
        pb = standalone_core / name
        if not pb.is_file():
            errors.append(f"{label}: missing mirrored file {pb.relative_to(root)}")
            continue
        ha, hb = _sha256_file(pa), _sha256_file(pb)
        if ha != hb:
            errors.append(f"{label}: SHA-256 mismatch for {name}")
    return len(errors) == 0, errors


def _registry_pairs(root: Path) -> List[Dict[str, Any]]:
    inv_path = root / "MASTER_PROJECT_INVENTORY.json"
    if not inv_path.is_file():
        return []
    try:
        inv = _load_json(inv_path)
    except (OSError, json.JSONDecodeError):
        return []
    reg = inv.get("dual_topology_registry")
    if not isinstance(reg, list):
        return []
    return [x for x in reg if isinstance(x, dict)]


def _legacy_sandbox_pair() -> Tuple[str, str, str]:
    """Hardcoded first dual-topology (pre-registry)."""
    return (
        "sandbox-runtime-001",
        "projects/sandbox-runtime",
        "standalone/tlc-sandbox-app",
    )


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
        help="Require byte-identical Python under each pair's integrated src/ vs standalone core/",
    )
    args = p.parse_args()
    script_dir = Path(__file__).resolve().parent
    root = (args.root or script_dir.parent).resolve()

    pairs: List[Tuple[str, str, str]] = []
    for row in _registry_pairs(root):
        pid = row.get("project_id")
        dt = row.get("dual_topology")
        if not isinstance(pid, str) or not isinstance(dt, dict):
            continue
        ip = dt.get("integrated_path")
        sp = dt.get("standalone_repo_path")
        if isinstance(ip, str) and isinstance(sp, str):
            pairs.append((pid, ip, sp))

    if not pairs:
        pid, ip, sp = _legacy_sandbox_pair()
        pairs = [(pid, ip, sp)]

    all_errors: List[str] = []
    for project_id, integrated_path, standalone_repo_path in pairs:
        integrated = root / integrated_path / "PROJECT_TOPOLOGY.json"
        standalone = root / standalone_repo_path / ".tlc" / "PROJECT_TOPOLOGY.json"

        missing: list[str] = []
        if not integrated.is_file():
            missing.append(str(integrated.relative_to(root)))
        if not standalone.is_file():
            missing.append(str(standalone.relative_to(root)))

        if missing:
            print(
                f"Constitutional Breach ({project_id}): PROJECT_TOPOLOGY.json missing:",
                file=sys.stderr,
            )
            for m in missing:
                print(f"  - {m}", file=sys.stderr)
            return 1

        try:
            a = _load_json(integrated)
            b = _load_json(standalone)
        except (OSError, json.JSONDecodeError) as e:
            print(f"ERROR ({project_id}): invalid topology JSON: {e}", file=sys.stderr)
            return 1

        id_a = a.get("project_id")
        id_b = b.get("project_id")
        if not isinstance(id_a, str) or not isinstance(id_b, str):
            print(
                f"ERROR ({project_id}): project_id must be a string in both topology files.",
                file=sys.stderr,
            )
            return 1

        if id_a != id_b:
            print(
                f"ERROR ({project_id}): integrated/standalone topology project_id mismatch: "
                f"{id_a!r} vs {id_b!r}",
                file=sys.stderr,
            )
            return 1

        if id_a != project_id:
            print(
                f"ERROR: registry project_id {project_id!r} != topology file {id_a!r}",
                file=sys.stderr,
            )
            return 1

        print(f"OK: dual topology linked for project_id={id_a!r}")
        print(f"  integrated:  {integrated.relative_to(root)}")
        print(f"  standalone:  {standalone.relative_to(root)}")

        if args.strict:
            ok, errs = verify_strict_core_pair(root, integrated_path, standalone_repo_path)
            if not ok:
                all_errors.extend(errs)

    if args.strict and all_errors:
        print("ERROR: --strict dual-topology core parity failed:", file=sys.stderr)
        for e in all_errors:
            print(f"  - {e}", file=sys.stderr)
        return 1

    if args.strict:
        print("OK: strict core parity (src/ <-> core/) for all registry pairs")

    return 0


if __name__ == "__main__":
    sys.exit(main())
