#!/usr/bin/env python3
"""
sync_master_project_inventory_from_projects.py

Full automation for TLC overlay discovery: scan projects/ directories and align
MASTER_PROJECT_INVENTORY.json (expected_slugs + entries) and MASTER_PROJECT_INVENTORY.md
(section 1 table + header timestamps) without touching governance blocks (ci_provenance, etc.).

- Existing entries for a slug are preserved verbatim (human-curated paths stay).
- New slugs get a default overlay entry (in-TLC paths + CLAUDE/BUILD_CONTRACT flags).
- Removed folders drop out of expected_slugs and entries.

See: .github/workflows/sync-master-project-inventory.yml (push on projects/**).
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Tuple

SECTION1_END = re.compile(
    r"^## 1\. TLC `projects/` overlay \(\d+ slugs\)\s*\r?\n"
    r"[\s\S]*?"
    r"(?=^- \*\*)",
    re.MULTILINE,
)


def discover_slugs(projects_dir: Path) -> List[str]:
    if not projects_dir.is_dir():
        print(f"ERROR: {projects_dir} is not a directory", file=sys.stderr)
        sys.exit(2)
    return sorted(
        p.name for p in projects_dir.iterdir() if p.is_dir() and not p.name.startswith(".")
    )


def default_entry(root: Path, slug: str) -> Dict[str, Any]:
    d = root / "projects" / slug
    tlc = str(root.resolve())
    in_tlc = f"{tlc}/projects/{slug}"
    has_claude = (d / "CLAUDE.md").is_file()
    has_bc = (d / "BUILD_CONTRACT.md").is_file() or (d / "BUILD_CONTRACT").is_file()
    return {
        "slug": slug,
        "implementation_repo_path_build_contract": in_tlc,
        "implementation_repo_path_config_ts": in_tlc,
        "path_exists_probe": True,
        "path_exists_status": "present",
        "has_claude_md": has_claude,
        "has_build_contract_md": has_bc,
        "repo_path_source": (
            "auto-sync: TLC overlay projects/"
            + slug
            + "/ (scripts/sync_master_project_inventory_from_projects.py)"
        ),
    }


def yn(val: Any) -> str:
    if val is True:
        return "yes"
    if val is False:
        return "no"
    return "n/a"


def probe_cell(entry: Dict[str, Any]) -> str:
    pe = entry.get("path_exists_probe")
    if pe is None:
        return "n/a"
    return "yes" if pe else "no"


def impl_cell(entry: Dict[str, Any]) -> str:
    bc = entry.get("implementation_repo_path_build_contract")
    cfg = entry.get("implementation_repo_path_config_ts")
    if bc:
        return f"`{bc}`"
    if cfg:
        return f"`{cfg}`"
    return "*none in contract*"


def render_section1(slugs: List[str], by_slug: Dict[str, Dict[str, Any]], n: int) -> str:
    lines = [
        f"## 1. TLC `projects/` overlay ({n} slugs)",
        "",
        "Canonical slug list (must match `MASTER_PROJECT_INVENTORY.json` → `tlc_projects_overlay.expected_slugs`):",
        "",
        "| Slug | `CLAUDE.md` | `BUILD_CONTRACT.md` | Implementation path (primary source) | Exists on disk (probe) |",
        "| ---- | ----------- | ------------------- | ------------------------------------ | ----------------------- |",
    ]
    for s in slugs:
        e = by_slug[s]
        row = (
            f"| {s} | {yn(e.get('has_claude_md'))} | {yn(e.get('has_build_contract_md'))} "
            f"| {impl_cell(e)} | {probe_cell(e)} |"
        )
        lines.append(row)
    lines.append("")
    lines.append("**File-level notes (non-exhaustive):**")
    return "\n".join(lines)


def build_inventory_payload(root: Path) -> Tuple[Dict[str, Any], List[str], List[Dict[str, Any]]]:
    projects_dir = root / "projects"
    slugs = discover_slugs(projects_dir)
    inv_path = root / "MASTER_PROJECT_INVENTORY.json"
    data = json.loads(inv_path.read_text(encoding="utf-8"))
    overlay = data.setdefault("tlc_projects_overlay", {})
    meta = data.setdefault("meta", {})

    prior = list(overlay.get("entries") or [])
    by_slug = {e["slug"]: e for e in prior if isinstance(e, dict) and e.get("slug")}

    new_entries: List[Dict[str, Any]] = []
    for slug in slugs:
        if slug in by_slug:
            new_entries.append(by_slug[slug])
        else:
            new_entries.append(default_entry(root, slug))

    prior_slugs = list(overlay.get("expected_slugs") or [])
    prior_entries = prior
    root_str = str(root.resolve())

    overlay["expected_slugs"] = slugs
    overlay["entries"] = new_entries
    meta["tlc_root"] = root_str

    if prior_slugs != slugs or prior_entries != new_entries or str(meta.get("tlc_root") or "") != root_str:
        meta["generated_at_utc"] = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    else:
        meta["generated_at_utc"] = str(meta.get("generated_at_utc") or "")

    return data, slugs, new_entries


def render_master_project_inventory_md(
    root: Path,
    slugs: List[str],
    entries: List[Dict[str, Any]],
    meta_ts: str,
) -> str:
    md_path = root / "MASTER_PROJECT_INVENTORY.md"
    text = md_path.read_text(encoding="utf-8")
    text = re.sub(
        r"\*\*Generated \(UTC\):\*\*[^\n]*",
        f"**Generated (UTC):** {meta_ts}  ",
        text,
        count=1,
    )
    tlc_root = str(root.resolve())
    text = re.sub(
        r"\*\*TLC root:\*\*[^\n]*",
        f"**TLC root:** `{tlc_root}`  ",
        text,
        count=1,
    )
    by_slug = {e["slug"]: e for e in entries if isinstance(e, dict) and e.get("slug")}
    section = render_section1(slugs, by_slug, len(slugs))
    if not SECTION1_END.search(text):
        print(
            "ERROR: could not find section 1 (## 1. TLC ... through **File-level notes**) "
            f"in {md_path}",
            file=sys.stderr,
        )
        sys.exit(2)
    return SECTION1_END.sub(section.rstrip() + "\n\n", text, count=1)


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--root", type=Path, default=None, help="TLC repo root (default: parent of scripts/)")
    ap.add_argument(
        "--dry-run",
        action="store_true",
        help="Print JSON preview only (first 4000 chars); do not write files",
    )
    ap.add_argument(
        "--check",
        action="store_true",
        help="Exit 1 if inventory files would change; exit 0 if already aligned",
    )
    args = ap.parse_args()

    script_dir = Path(__file__).resolve().parent
    root = (args.root or script_dir.parent).resolve()
    inv_path = root / "MASTER_PROJECT_INVENTORY.json"
    md_path = root / "MASTER_PROJECT_INVENTORY.md"

    if not inv_path.is_file():
        print(f"ERROR: missing {inv_path}", file=sys.stderr)
        sys.exit(2)
    if not md_path.is_file():
        print(f"ERROR: missing {md_path}", file=sys.stderr)
        sys.exit(2)

    data, slugs, entries = build_inventory_payload(root)
    meta_ts = (data.get("meta") or {}).get("generated_at_utc", "")
    new_json = json.dumps(data, indent=2, ensure_ascii=False) + "\n"
    new_md = render_master_project_inventory_md(root, slugs, entries, meta_ts)

    if args.dry_run:
        print(new_json[:4000])
        if len(new_json) > 4000:
            print("\n... [truncated]", file=sys.stderr)
        sys.exit(0)

    old_json = inv_path.read_text(encoding="utf-8")
    old_md = md_path.read_text(encoding="utf-8")
    changed = old_json != new_json or old_md != new_md

    if args.check:
        sys.exit(1 if changed else 0)

    if not changed:
        print("OK: MASTER_PROJECT_INVENTORY already matches projects/")
        sys.exit(0)

    inv_path.write_text(new_json, encoding="utf-8")
    md_path.write_text(new_md, encoding="utf-8")
    print(
        f"OK: updated MASTER_PROJECT_INVENTORY.* ({len(slugs)} slugs, generated_at_utc={meta_ts})",
        file=sys.stderr,
    )
    sys.exit(0)


if __name__ == "__main__":
    main()
