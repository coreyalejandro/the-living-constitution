#!/usr/bin/env python3
"""Compute documentation compliance score from MVDS + extended paths (real counts)."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--root", type=Path, default=Path("."))
    ap.add_argument("--json-out", type=Path, help="Write JSON report to this path")
    args = ap.parse_args()
    root = args.root.resolve()

    cfg = json.loads((root / "config" / "docs_governance.json").read_text(encoding="utf-8"))
    mvds = cfg["mvds_paths"]
    extra = cfg.get("full_compliance_extra_paths", [])

    def exists(rel: str) -> bool:
        return (root / rel).is_file()

    mvds_ok = sum(1 for p in mvds if exists(p))
    mvds_total = len(mvds)
    extra_ok = sum(1 for p in extra if exists(p))
    extra_total = len(extra)

    full_target = mvds_total + extra_total
    full_ok = mvds_ok + extra_ok

    mvds_pct = (100.0 * mvds_ok / mvds_total) if mvds_total else 100.0
    full_pct = (100.0 * full_ok / full_target) if full_target else 100.0

    report = {
        "contract_version": cfg.get("contract_version"),
        "mvds_label": cfg.get("mvds_label"),
        "mvds": {"present": mvds_ok, "required": mvds_total, "percent": round(mvds_pct, 2)},
        "full_compliance": {
            "present": full_ok,
            "required": full_target,
            "percent": round(full_pct, 2),
        },
        "missing_mvds": [p for p in mvds if not exists(p)],
        "missing_extended": [p for p in extra if not exists(p)],
    }

    print(json.dumps(report, indent=2))
    if args.json_out:
        args.json_out.parent.mkdir(parents=True, exist_ok=True)
        args.json_out.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
