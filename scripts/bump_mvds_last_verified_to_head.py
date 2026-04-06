#!/usr/bin/env python3
"""Set MVDS frontmatter last_verified.commit + timestamp to current HEAD (short) and UTC now.

Used after doc edits so verify_document_constitution STALE_COMMIT aligns with HEAD.
Default file list matches CI STALE_COMMIT surfaces (see verify.yml doc step)."""

from __future__ import annotations

import datetime as _dt
import subprocess
import sys
from pathlib import Path

NEEDLE = (
    'last_verified:\n'
    '  commit: "71a0913"\n'
    '  timestamp: "2026-04-06T12:00:00Z"'
)

DEFAULT_PATHS = (
    "README.md",
    "docs/constitution/amendments/README.md",
    "docs/constitution/TERMINOLOGY.md",
    "docs/constitution/DOC_TRUTH_HIERARCHY.md",
    "docs/constitution/DOCUMENTATION_STANDARD.md",
    "docs/constitution/DOCUMENTATION_CHANGELOG.md",
    "docs/constitution/CANONICAL_PATHS.md",
    "docs/constitution/AMENDMENT_PROCESS.md",
    "docs/INDEX.md",
    "docs/HELP.md",
)


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    short = subprocess.check_output(
        ["git", "-C", str(root), "rev-parse", "--short", "HEAD"],
        text=True,
    ).strip()
    ts = _dt.datetime.now(_dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    repl = f'last_verified:\n  commit: "{short}"\n  timestamp: "{ts}"'
    paths = sys.argv[1:] if len(sys.argv) > 1 else list(DEFAULT_PATHS)
    for rel in paths:
        p = root / rel
        text = p.read_text(encoding="utf-8")
        if NEEDLE not in text:
            print(f"skip (needle missing): {rel}", file=sys.stderr)
            continue
        text = text.replace(NEEDLE, repl, 1)
        if rel.endswith("DOCUMENTATION_CHANGELOG.md"):
            text = text.replace("PLACEHOLDER_SHORT", short)
        p.write_text(text, encoding="utf-8")
        print(f"updated: {rel} -> {short}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
