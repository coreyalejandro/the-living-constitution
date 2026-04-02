#!/usr/bin/env python3
"""
R&D reinforcement loop: propose a draft invariant for the Constitutional Architect.

Writes a markdown file under ``03-enforcement/drafts/`` at the TLC repository root.
"""

from __future__ import annotations

import argparse
import os
import re
from datetime import datetime, timezone
from pathlib import Path


def discover_tlc_root() -> Path:
    env = os.environ.get("TLC_REPO_ROOT")
    if env:
        return Path(env).resolve()
    here = Path(__file__).resolve().parent
    for base in (here, Path.cwd()):
        for p in [base] + list(base.parents):
            if (p / "THE_LIVING_CONSTITUTION.md").is_file():
                return p
    return Path.cwd().resolve()


def _slug(s: str) -> str:
    s = s.strip().lower()
    s = re.sub(r"[^a-z0-9]+", "-", s)
    return s.strip("-") or "draft"


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("title", help="Short title for the proposed invariant")
    p.add_argument(
        "--rationale",
        default="",
        help="Why this invariant should exist (observed failure mode or pattern)",
    )
    p.add_argument(
        "--failure-mode",
        default="",
        help="Optional failure mode keyword(s)",
    )
    args = p.parse_args()

    root = discover_tlc_root()
    drafts = root / "03-enforcement" / "drafts"
    drafts.mkdir(parents=True, exist_ok=True)

    ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    slug = _slug(args.title)
    out = drafts / f"INV-PROPOSED-{ts}-{slug}.md"

    body = f"""# Proposed Invariant (Draft)

**Status:** DRAFT — for Constitutional Architect review only.  
**Generated (UTC):** {ts}  
**Actor:** `project_id: sandbox-runtime-001` (propose_invariant.py)

## Title

{args.title.strip()}

## Failure mode

{args.failure_mode.strip() or "(not specified)"}

## Rationale

{args.rationale.strip() or "(not specified)"}

## Suggested enforcement hook

_(Architect fills: code path, verifier, or human gate.)_

## Suggested evidence hook

_(Architect fills: ledger, CI artifact, or manual attestation.)_

---
*End of draft.*
"""
    out.write_text(body, encoding="utf-8")
    print(f"Wrote {out.relative_to(root)}")


if __name__ == "__main__":
    main()
