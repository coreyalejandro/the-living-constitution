#!/usr/bin/env python3
"""
Governed Markdown generator: YAML frontmatter + canonical path enforcement.
Refuses root-level substantive docs (only README.md class may be requested via policy).
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

try:
    import yaml
except ImportError:
    print("ERROR: pip install pyyaml", file=sys.stderr)
    raise SystemExit(2)


def _short_head(root: Path) -> str:
    try:
        return (
            subprocess.check_output(
                ["git", "-C", str(root), "rev-parse", "--short", "HEAD"],
                text=True,
            ).strip()
        )
    except Exception:
        return "unknown"


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--root", type=Path, default=Path("."))
    ap.add_argument(
        "--doc-type",
        required=True,
        help='e.g. "Operational", "Instructional", "Navigational"',
    )
    ap.add_argument(
        "--header-tier",
        required=True,
        choices=("full", "minimal"),
    )
    ap.add_argument(
        "--category",
        required=True,
        help="Subfolder under docs/, e.g. operations, instructions, constitution",
    )
    ap.add_argument("--id", dest="doc_id", required=True, help="Document id e.g. DOC-OP-NEW-001")
    ap.add_argument("--slug", required=True, help="Filename without .md")
    ap.add_argument("--title", required=True)
    args = ap.parse_args()
    root = args.root.resolve()

    rel = f"docs/{args.category}/{args.slug}.md"
    out = root / rel

    if out.exists():
        print(f"ERROR: Refusing to overwrite existing {rel}", file=sys.stderr)
        raise SystemExit(1)

    if not rel.startswith("docs/") and rel != "README.md":
        print("ERROR: Only docs/ paths are generated (or README via separate flow).", file=sys.stderr)
        raise SystemExit(1)

    if rel.count("/") < 2 or ".." in rel:
        print("ERROR: Invalid path", file=sys.stderr)
        raise SystemExit(1)

    ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    head = _short_head(root)

    if args.header_tier == "full":
        fm = {
            "document_type": args.doc_type,
            "id": args.doc_id,
            "repo_scope": "TLC-Core",
            "authority_level": "L3",
            "truth_rank": 2,
            "status": "Draft",
            "canonical_path": rel,
            "next_file": "docs/INDEX.md",
            "last_verified": {"commit": head, "timestamp": ts},
            "metadata": {
                "est_time_minutes": 15,
                "cognitive_load": "Medium",
                "requires_interruption_buffer": False,
            },
            "navigation": {
                "parent_index": "docs/INDEX.md",
                "hierarchy_level": f"TLC > {args.category.title()} > {args.slug}",
            },
        }
    else:
        fm = {
            "document_type": args.doc_type,
            "id": args.doc_id,
            "status": "Draft",
            "canonical_path": rel,
            "next_file": "docs/INDEX.md",
            "last_verified": {"commit": head, "timestamp": ts},
        }

    body = f"""# {args.title}

## Starting state

<!-- Describe starting state -->

## Ending state

<!-- Describe ending state -->

## What You Will Need

- <!-- list prerequisites -->

### Step 1: <!-- title -->

**Action:** <!-- action -->
**Location:** <!-- path -->
**Command:**

```bash
# command
```

**Checkpoint [Critical]:**

> <!-- success criteria -->

**Confidence signal:** <!-- You should now see ... -->

"""
    if args.doc_type in ("Operational", "Instructional"):
        pass  # body already checkpoint-oriented
    else:
        body = f"# {args.title}\n\n<!-- Content -->\n"

    out.parent.mkdir(parents=True, exist_ok=True)
    text = "---\n" + yaml.safe_dump(fm, sort_keys=False) + "---\n\n" + body
    out.write_text(text, encoding="utf-8")
    print(f"Wrote {rel}")


if __name__ == "__main__":
    main()
