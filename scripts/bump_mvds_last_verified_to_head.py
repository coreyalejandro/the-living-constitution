#!/usr/bin/env python3
"""Set MVDS frontmatter last_verified.commit + timestamp to current HEAD (short) and UTC now.

Replaces the first YAML `last_verified` block matching commit + timestamp (any short hash).
Optional: sync DOCUMENTATION_CHANGELOG.md table row `| YYYY-MM-DD | <hash> |` for the latest MVDS row."""

from __future__ import annotations

import datetime as _dt
import re
import subprocess
import sys
from pathlib import Path

BLOCK_RE = re.compile(
    r"last_verified:\n  commit: \"[0-9a-f]{7}\"\n  timestamp: \"[^\"]+\"",
    re.MULTILINE,
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
    already = re.compile(
        r"last_verified:\n  commit: \"" + re.escape(short) + r"\"\n  timestamp:",
    )
    for rel in paths:
        p = root / rel
        text = p.read_text(encoding="utf-8")
        if already.search(text):
            # Avoid churn: already aligned to current HEAD (timestamp-only edits loop forever).
            print(f"skip (already {short}): {rel}")
            continue
        text2, n = BLOCK_RE.subn(repl, text, count=1)
        if n != 1:
            print(f"error: expected 1 last_verified block in {rel}, got {n}", file=sys.stderr)
            return 1
        # Changelog: sync MVDS refresh row commit column if present (C-RSP README row).
        if rel.endswith("DOCUMENTATION_CHANGELOG.md"):
            text2 = re.sub(
                r"(\| 2026-04-06 \| )[0-9a-f]{7}( \| `projects/c-rsp/README\.md`)",
                rf"\g<1>{short}\2",
                text2,
                count=1,
            )
        p.write_text(text2, encoding="utf-8")
        print(f"updated: {rel} -> {short}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
