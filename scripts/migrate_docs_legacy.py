#!/usr/bin/env python3
"""
Legacy documentation migration helper: classify root vs docs/, suggest canonical targets,
and emit a migration report (dry-run by default).
"""

from __future__ import annotations

import argparse
import json
import re
from datetime import datetime, timezone
from pathlib import Path

FRONT_MATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*", re.DOTALL | re.MULTILINE)


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--root", type=Path, default=Path("."))
    ap.add_argument(
        "--apply",
        action="store_true",
        help="Danger: perform moves (not implemented; report only).",
    )
    args = ap.parse_args()
    root = args.root.resolve()

    report: dict = {
        "generated": datetime.now(timezone.utc).isoformat(),
        "root_markdown": [],
        "docs_without_frontmatter": [],
        "suggested_moves": [],
    }

    for p in sorted(root.glob("*.md")):
        report["root_markdown"].append(
            {
                "name": p.name,
                "class": "root_candidate",
                "note": "If substantive, move under docs/<taxonomy>/; keep README.md at root.",
            }
        )

    docs = root / "docs"
    if docs.is_dir():
        for path in sorted(docs.rglob("*.md")):
            raw = path.read_text(encoding="utf-8")
            if not FRONT_MATTER_RE.match(raw):
                rel = path.relative_to(root).as_posix()
                report["docs_without_frontmatter"].append(rel)

    out = root / "verification" / "docs_migration_report.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))

    if args.apply:
        print(
            "NOTE: --apply is not enabled for automatic moves; use git mv manually using suggested_moves in a future revision.",
            file=__import__("sys").stderr,
        )


if __name__ == "__main__":
    main()
