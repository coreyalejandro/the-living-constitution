#!/usr/bin/env python3
"""
verify_project_topology.py

Validates TLC workspace layout against MASTER_PROJECT_INVENTORY.json.
Does not assume repo relationships beyond what the inventory records.
Exit codes:
  0 — checks passed
  1 — validation failure (inventory missing, drift, or probe mismatch)
  2 — usage / file read error
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple


def _parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument(
        "--root",
        type=Path,
        default=None,
        help="TLC repository root (default: parent of scripts/)",
    )
    p.add_argument(
        "--inventory",
        type=Path,
        default=None,
        help="Path to MASTER_PROJECT_INVENTORY.json (default: <root>/MASTER_PROJECT_INVENTORY.json)",
    )
    p.add_argument(
        "--no-probes",
        action="store_true",
        help="Skip filesystem existence probes (only compare projects/ slugs to JSON).",
    )
    p.add_argument(
        "--with-governance",
        action="store_true",
        help="After topology checks pass, run scripts/verify_governance_chain.py on the same root.",
    )
    return p.parse_args()


def _load_json(path: Path) -> Dict[str, Any]:
    try:
        with path.open("r", encoding="utf-8") as f:
            return json.load(f)
    except (OSError, json.JSONDecodeError) as e:
        print(f"ERROR: cannot read JSON: {path}: {e}", file=sys.stderr)
        sys.exit(2)


def _norm_abs(p: str, projects_parent: Path) -> Path:
    """Resolve a path string that may be absolute or relative."""
    x = Path(p).expanduser()
    if x.is_absolute():
        return x
    return (projects_parent / x).resolve()


def _exists_dir(p: Optional[str]) -> Optional[bool]:
    if p is None:
        return None
    path = Path(p).expanduser()
    if not path.is_absolute():
        return None
    return path.is_dir()


def _satellite_governance_topology(root: Path, data: Dict[str, Any], with_governance: bool) -> int:
    """
    ConsentChain (and other satellite) repos use inventory_kind consentchain_governance_inventory:
    no projects/ overlay — verify governance_artifacts.canonical_paths exist, then optional governance chain.
    """
    ga = data.get("governance_artifacts") or {}
    canonical = ga.get("canonical_paths") or {}
    if not isinstance(canonical, dict) or not canonical:
        print(
            "ERROR: satellite inventory requires governance_artifacts.canonical_paths",
            file=sys.stderr,
        )
        return 1
    errs: List[str] = []
    for key, rel in sorted(canonical.items()):
        if not isinstance(rel, str) or not rel.strip():
            errs.append(f"canonical_paths[{key!r}]: invalid path")
            continue
        p = root / rel
        if not p.is_file():
            errs.append(f"satellite governance: missing file {key} -> {rel}")
    if errs:
        print("ERROR: satellite governance topology failed:", file=sys.stderr)
        for e in errs:
            print(f"  - {e}", file=sys.stderr)
        return 1
    print("OK: satellite governance topology (canonical_paths) verified")
    if with_governance:
        gov_script = root / "scripts" / "verify_governance_chain.py"
        if not gov_script.is_file():
            print(f"ERROR: governance verifier missing: {gov_script}", file=sys.stderr)
            return 2
        r = subprocess.run(
            [sys.executable, str(gov_script), "--root", str(root)],
            check=False,
        )
        return int(r.returncode)
    return 0


def main() -> None:
    args = _parse_args()
    # Inventory embeds absolute sibling paths from the machine that generated it; GitHub
    # runners cannot see those paths. Skip probes in CI without changing CLI flags.
    if os.environ.get("GITHUB_ACTIONS", "").lower() == "true":
        args.no_probes = True
        print(
            "NOTE: GITHUB_ACTIONS=true — skipping workstation path probes (same as --no-probes).",
            file=sys.stderr,
        )
    script_dir = Path(__file__).resolve().parent
    root = (args.root or (script_dir.parent)).resolve()
    inv_path = args.inventory or (root / "MASTER_PROJECT_INVENTORY.json")

    data = _load_json(inv_path)
    inv_kind = (data.get("meta") or {}).get("inventory_kind")
    if inv_kind == "consentchain_governance_inventory":
        rc = _satellite_governance_topology(root, data, getattr(args, "with_governance", False))
        sys.exit(rc)
    meta = data.get("meta") or {}
    recorded_root = meta.get("tlc_root")
    if recorded_root and Path(recorded_root).resolve() != root:
        print(
            f"WARNING: --root {root} != meta.tlc_root {recorded_root} "
            f"(inventory may be stale).",
            file=sys.stderr,
        )

    overlay = data.get("tlc_projects_overlay") or {}
    expected: List[str] = list(overlay.get("expected_slugs") or [])
    if not expected:
        print("ERROR: tlc_projects_overlay.expected_slugs is empty or missing.", file=sys.stderr)
        sys.exit(1)

    projects_dir = root / "projects"
    if not projects_dir.is_dir():
        print(f"ERROR: missing directory {projects_dir}", file=sys.stderr)
        sys.exit(1)

    on_disk: Set[str] = {p.name for p in projects_dir.iterdir() if p.is_dir()}
    expected_set = set(expected)
    if on_disk != expected_set:
        only_disk = sorted(on_disk - expected_set)
        only_json = sorted(expected_set - on_disk)
        print("ERROR: projects/ slugs do not match inventory.", file=sys.stderr)
        if only_disk:
            print(f"  On disk only: {only_disk}", file=sys.stderr)
        if only_json:
            print(f"  In JSON only: {only_json}", file=sys.stderr)
        sys.exit(1)

    errors: List[str] = []
    if not args.no_probes:
        entries: List[Dict[str, Any]] = list(overlay.get("entries") or [])
        by_slug = {e["slug"]: e for e in entries if "slug" in e}
        for slug in sorted(expected_set):
            ent = by_slug.get(slug)
            if not ent:
                errors.append(f"Missing overlay entry for slug {slug!r} in entries[]")
                continue

            recorded = ent.get("path_exists_probe")
            if recorded is None:
                continue

            bc = ent.get("implementation_repo_path_build_contract")
            cfg = ent.get("implementation_repo_path_config_ts")
            chosen: Optional[str] = None
            if bc is not None:
                chosen = bc
            elif cfg is not None:
                chosen = cfg

            if chosen is None:
                errors.append(
                    f"{slug}: path_exists_probe is set but no implementation path recorded"
                )
                continue

            actual = _exists_dir(chosen)
            if actual is None:
                errors.append(f"{slug}: non-absolute or unresolvable path {chosen!r}")
                continue
            if actual != bool(recorded):
                errors.append(
                    f"{slug}: probe mismatch — inventory says path_exists_probe={recorded} "
                    f"but directory exists={actual} for {chosen}"
                )

        cf = data.get("consentchain_family_script") or {}
        if "projects_consent_gateway_auth0_overlay_exists" in cf:
            gw = root / "projects" / "consent-gateway-auth0"
            exists = gw.is_dir()
            if bool(cf["projects_consent_gateway_auth0_overlay_exists"]) != exists:
                errors.append(
                    "consent-gateway-auth0: inventory flag "
                    f"projects_consent_gateway_auth0_overlay_exists="
                    f"{cf['projects_consent_gateway_auth0_overlay_exists']} "
                    f"but on_disk={exists} at {gw}"
                )

        bl = data.get("buildlattice_overlay_script") or {}
        if "projects_buildlattice_overlay_exists" in bl:
            bl_dir = root / "projects" / "buildlattice"
            exists_bl = bl_dir.is_dir()
            if bool(bl["projects_buildlattice_overlay_exists"]) != exists_bl:
                errors.append(
                    "buildlattice: inventory flag "
                    f"projects_buildlattice_overlay_exists="
                    f"{bl['projects_buildlattice_overlay_exists']} "
                    f"but on_disk={exists_bl} at {bl_dir}"
                )
        for rel in bl.get("expects_tlc_relative_paths") or []:
            p = root / rel
            if not p.is_file():
                errors.append(
                    f"buildlattice overlay: expected file missing at {rel!r} (resolved {p})"
                )

        eg = data.get("empirical_guard_overlay_script") or {}
        if "projects_empirical_guard_overlay_exists" in eg:
            eg_dir = root / "projects" / "empirical-guard"
            exists_eg = eg_dir.is_dir()
            if bool(eg["projects_empirical_guard_overlay_exists"]) != exists_eg:
                errors.append(
                    "empirical-guard: inventory flag "
                    f"projects_empirical_guard_overlay_exists="
                    f"{eg['projects_empirical_guard_overlay_exists']} "
                    f"but on_disk={exists_eg} at {eg_dir}"
                )
        for rel in eg.get("expects_tlc_relative_paths") or []:
            p = root / rel
            if not p.is_file():
                errors.append(
                    f"empirical-guard overlay: expected file missing at {rel!r} (resolved {p})"
                )

        epg = data.get("epistemic_guard_overlay_script") or {}
        if "projects_epistemic_guard_overlay_exists" in epg:
            epg_dir = root / "projects" / "epistemic-guard"
            exists_epg = epg_dir.is_dir()
            if bool(epg["projects_epistemic_guard_overlay_exists"]) != exists_epg:
                errors.append(
                    "epistemic-guard: inventory flag "
                    f"projects_epistemic_guard_overlay_exists="
                    f"{epg['projects_epistemic_guard_overlay_exists']} "
                    f"but on_disk={exists_epg} at {epg_dir}"
                )
        for rel in epg.get("expects_tlc_relative_paths") or []:
            p = root / rel
            if not p.is_file():
                errors.append(
                    f"epistemic-guard overlay: expected file missing at {rel!r} (resolved {p})"
                )

    if errors:
        print("ERROR: topology probes failed:", file=sys.stderr)
        for e in errors:
            print(f"  - {e}", file=sys.stderr)
        print(
            "\nRefresh MASTER_PROJECT_INVENTORY.json / .md after verifying facts, "
            "or pass --no-probes to only check projects/ slug list.",
            file=sys.stderr,
        )
        sys.exit(1)

    print("OK: project topology matches MASTER_PROJECT_INVENTORY.json")

    if getattr(args, "with_governance", False):
        gov_script = root / "scripts" / "verify_governance_chain.py"
        if not gov_script.is_file():
            print(f"ERROR: governance verifier missing: {gov_script}", file=sys.stderr)
            sys.exit(2)
        r = subprocess.run(
            [sys.executable, str(gov_script), "--root", str(root)],
            check=False,
        )
        sys.exit(r.returncode)

    sys.exit(0)


if __name__ == "__main__":
    main()
