#!/usr/bin/env python3
"""
Documentation constitution verifier for TLC core and governed-repo patterns.

Validates MVDS presence, root Markdown allowlist, governance placement,
YAML frontmatter path integrity, and staleness signals (warning by default).
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

try:
    import yaml
except ImportError as exc:  # pragma: no cover
    print("ERROR: PyYAML is required: pip install pyyaml", file=sys.stderr)
    raise SystemExit(2) from exc

FRONT_MATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*", re.DOTALL | re.MULTILINE)
OK_TOKEN = "DOCUMENT_CONSTITUTION_OK"


def _load_config(root: Path) -> dict[str, Any]:
    path = root / "config" / "docs_governance.json"
    if not path.is_file():
        raise FileNotFoundError(path)
    return json.loads(path.read_text(encoding="utf-8"))


def _git_head_short(root: Path) -> str | None:
    try:
        out = subprocess.check_output(
            ["git", "-C", str(root), "rev-parse", "--short", "HEAD"],
            text=True,
            stderr=subprocess.DEVNULL,
        )
        return out.strip()
    except (subprocess.CalledProcessError, FileNotFoundError):
        return None


def _parse_allowlist(root: Path) -> tuple[list[str], list[str]]:
    path = root / "docs" / "constitution" / "ROOT_DOC_ALLOWLIST.md"
    text = path.read_text(encoding="utf-8")
    literals: list[str] = []
    regexes: list[str] = []
    mode: str | None = None
    for line in text.splitlines():
        if line.strip().startswith("## "):
            if line.strip().startswith("## Literal allowlist"):
                mode = "lit"
            elif line.strip().startswith("## Regex"):
                mode = "rx"
            else:
                mode = None
            continue
        if mode and line.strip().startswith("- "):
            item = line.strip()[2:].strip()
            if item.startswith("`") and item.endswith("`"):
                item = item[1:-1]
            if mode == "lit":
                literals.append(item)
            elif mode == "rx":
                regexes.append(item)
    # Defaults if sections empty (fail-safe)
    if not literals:
        literals = ["README.md"]
    return literals, regexes


def _root_markdown_allowed(name: str, literals: list[str], regexes: list[str]) -> bool:
    if name in literals:
        return True
    for pat in regexes:
        try:
            if re.fullmatch(pat, name):
                return True
        except re.error:
            continue
    return False


def _parse_frontmatter(path: Path) -> dict[str, Any] | None:
    raw = path.read_text(encoding="utf-8")
    m = FRONT_MATTER_RE.match(raw)
    if not m:
        return None
    try:
        return yaml.safe_load(m.group(1)) or {}
    except yaml.YAMLError:
        return {"__parse_error__": True}


def _fail(errors: list[dict[str, Any]], out_path: Path | None) -> None:
    payload = {"ok": False, "errors": errors}
    txt = json.dumps(payload, indent=2)
    print(txt, file=sys.stderr)
    if out_path:
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(txt + "\n", encoding="utf-8")


def verify(root: Path, fail_on_stale: bool) -> int:
    errors: list[dict[str, Any]] = []
    warnings: list[dict[str, Any]] = []

    config = _load_config(root)
    mvds = config["mvds_paths"]
    forbidden = config.get("forbidden_live_governance_paths", [])
    staleness = config.get("staleness", {})
    max_age = int(staleness.get("max_age_days", 90))
    fail_stale = bool(staleness.get("fail_ci_on_stale", False))

    head = _git_head_short(root)

    # MVDS paths
    for rel in mvds:
        p = root / rel
        if not p.is_file():
            errors.append({"code": "MVDS_MISSING", "path": rel})

    # Forbidden governance paths under docs/governance/
    dgov = root / "docs" / "governance"
    if dgov.is_dir():
        for child in dgov.rglob("*"):
            if child.is_file():
                rel = str(child.relative_to(root))
                if rel in forbidden or child.name in (
                    "BUILD_CONTRACT.instance.md",
                    "governance-template.lock.json",
                    "GOVERNANCE_BINDING.md",
                ):
                    errors.append(
                        {
                            "code": "LIVE_GOVERNANCE_IN_DOCS_GOV",
                            "path": rel,
                            "detail": "Live governance must not live under docs/governance/",
                        }
                    )

    for fp in forbidden:
        if (root / fp).is_file():
            errors.append(
                {
                    "code": "FORBIDDEN_PATH_PRESENT",
                    "path": fp,
                }
            )

    # Root markdown allowlist
    literals, regexes = _parse_allowlist(root)
    for entry in root.iterdir():
        if not entry.is_file():
            continue
        if entry.suffix.lower() != ".md":
            continue
        if not _root_markdown_allowed(entry.name, literals, regexes):
            errors.append(
                {
                    "code": "ROOT_MARKDOWN_DENIED",
                    "path": entry.name,
                    "detail": "Not in literal/regex allowlist",
                }
            )

    # Frontmatter path integrity (governed roots)
    scan_roots = [root / "docs", root / "governance"]
    md_files: list[Path] = []
    for base in scan_roots:
        if base.is_dir():
            md_files.extend(base.rglob("*.md"))
    readme = root / "README.md"
    if readme.is_file():
        md_files.append(readme)

    for path in sorted(set(md_files)):
        rel = path.relative_to(root).as_posix()
        fm = _parse_frontmatter(path)
        if fm is None:
            # Navigational lightweight files may exist without YAML in non-MVDS legacy areas;
            # require YAML for MVDS paths only.
            if rel in mvds or rel in config.get("full_compliance_extra_paths", []):
                errors.append({"code": "MISSING_FRONTMATTER", "path": rel})
            continue
        if fm.get("__parse_error__"):
            errors.append({"code": "YAML_PARSE_ERROR", "path": rel})
            continue

        cpath = fm.get("canonical_path")
        if isinstance(cpath, str) and cpath != rel:
            errors.append(
                {
                    "code": "CANONICAL_PATH_MISMATCH",
                    "path": rel,
                    "canonical_path": cpath,
                }
            )

        nf = fm.get("next_file")
        if isinstance(nf, str) and nf.strip():
            if not (root / nf).is_file():
                errors.append(
                    {"code": "NEXT_FILE_MISSING", "path": rel, "next_file": nf}
                )

        nav = fm.get("navigation") or {}
        pi = nav.get("parent_index")
        if isinstance(pi, str) and pi.strip():
            if not (root / pi).is_file():
                errors.append(
                    {"code": "PARENT_INDEX_MISSING", "path": rel, "parent_index": pi}
                )

        lv = fm.get("last_verified") or {}
        commit = lv.get("commit") if isinstance(lv, dict) else None
        ts = lv.get("timestamp") if isinstance(lv, dict) else None
        if head and isinstance(commit, str) and commit.strip():
            ca = commit.strip()
            hb = head.strip()
            match = ca[:7] == hb[:7] if len(ca) >= 7 and len(hb) >= 7 else ca == hb
            if not match:
                msg = {
                    "code": "STALE_COMMIT",
                    "path": rel,
                    "last_verified_commit": commit,
                    "head": head,
                }
                warnings.append(msg)
                if fail_stale or fail_on_stale:
                    errors.append(msg)
        if isinstance(ts, str):
            try:
                tsd = datetime.fromisoformat(ts.replace("Z", "+00:00"))
                age = (datetime.now(timezone.utc) - tsd.astimezone(timezone.utc)).days
                if age > max_age:
                    w = {"code": "STALE_TIMESTAMP", "path": rel, "age_days": age}
                    warnings.append(w)
                    if fail_stale or fail_on_stale:
                        errors.append(w)
            except ValueError:
                warnings.append({"code": "BAD_TIMESTAMP", "path": rel, "timestamp": ts})

    # Blind Man's Test spot-check: operational + instructional surfaces
    for path in sorted((root / "docs" / "operations").glob("*.md")):
        rel = path.relative_to(root).as_posix()
        fm = _parse_frontmatter(path)
        if not fm:
            continue
        dt = fm.get("document_type")
        if dt in ("Operational", "Instructional"):
            raw = path.read_text(encoding="utf-8")
            if "What You Will Need" not in raw:
                errors.append(
                    {
                        "code": "MISSING_WHAT_YOU_WILL_NEED",
                        "path": rel,
                    }
                )
            if "**Checkpoint" not in raw:
                errors.append(
                    {
                        "code": "MISSING_CHECKPOINT",
                        "path": rel,
                    }
                )
            if "Confidence signal" not in raw and "Confidence signals" not in raw:
                errors.append(
                    {
                        "code": "MISSING_CONFIDENCE_SIGNAL",
                        "path": rel,
                    }
                )

    instruction_paths = list((root / "docs" / "instructions").glob("*.md"))
    help_md = root / "docs" / "HELP.md"
    if help_md.is_file():
        instruction_paths.append(help_md)
    for path in sorted(set(instruction_paths)):
        rel = path.relative_to(root).as_posix()
        fm = _parse_frontmatter(path)
        if not fm:
            continue
        if fm.get("document_type") == "Instructional":
            raw = path.read_text(encoding="utf-8")
            if "What You Will Need" not in raw:
                errors.append(
                    {
                        "code": "MISSING_WHAT_YOU_WILL_NEED",
                        "path": rel,
                    }
                )
            if "**Checkpoint" not in raw:
                errors.append(
                    {
                        "code": "MISSING_CHECKPOINT",
                        "path": rel,
                    }
                )
            if "Confidence signal" not in raw and "Confidence signals" not in raw:
                errors.append(
                    {
                        "code": "MISSING_CONFIDENCE_SIGNAL",
                        "path": rel,
                    }
                )

    # Evidence link spot-check: EVIDENCE_MAP must reference smoke file
    evmap = root / "docs" / "evidence" / "EVIDENCE_MAP.md"
    if evmap.is_file():
        evtxt = evmap.read_text(encoding="utf-8")
        if "2026-04-04-docs-governance-smoke.md" not in evtxt:
            errors.append(
                {
                    "code": "EVIDENCE_MAP_BROKEN",
                    "detail": "Smoke artifact not linked from EVIDENCE_MAP",
                }
            )

    out_fail = root / "verification" / "docs_constitution_failure.json"

    if warnings:
        for w in warnings:
            ann = f"::warning file={w.get('path', '')}:: {w}"
            print(ann, file=sys.stderr)

    if errors:
        _fail(errors, out_fail)
        return 1

    print(OK_TOKEN)
    if (root / "verification" / "docs_constitution_failure.json").is_file():
        (root / "verification" / "docs_constitution_failure.json").unlink(missing_ok=True)
    return 0


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--root", type=Path, default=Path("."))
    ap.add_argument(
        "--fail-on-stale",
        action="store_true",
        help="Treat stale last_verified as error (overrides config fail_ci_on_stale).",
    )
    args = ap.parse_args()
    root = args.root.resolve()
    raise SystemExit(verify(root, args.fail_on_stale))


if __name__ == "__main__":
    main()
