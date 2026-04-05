#!/usr/bin/env python3
"""
Compare canonical C-RSP template section order and titles to an instance artifact.
Section 0 allows Template Governance (template) or Instance Governance (instance).
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

HEADER_RE = re.compile(r"^## (\d+)\.\s+(.+?)\s*$", re.MULTILINE)


def extract_sections(text: str) -> list[tuple[int, str]]:
    return [(int(m.group(1)), m.group(2).strip()) for m in HEADER_RE.finditer(text)]


def normalize_title(title: str) -> str:
    return re.sub(r"\s*\([^)]*\)\s*$", "", title).strip()


def section_titles_align(template_title: str, instance_title: str, section_num: int) -> bool:
    it = normalize_title(instance_title)
    tt = normalize_title(template_title)
    if section_num == 0:
        return it in (
            "Template Governance",
            "Instance Governance",
        ) and tt in ("Template Governance", "Instance Governance")
    return it == tt


def main() -> int:
    p = argparse.ArgumentParser(description="Verify C-RSP instance structure vs template")
    p.add_argument("--template", required=True, type=Path)
    p.add_argument("--instance", required=True, type=Path)
    p.add_argument("--report", required=True, type=Path)
    args = p.parse_args()

    template_text = args.template.read_text(encoding="utf-8")
    instance_text = args.instance.read_text(encoding="utf-8")

    t_secs = extract_sections(template_text)
    i_secs = extract_sections(instance_text)

    errors: list[str] = []
    if len(t_secs) != 18:
        errors.append(f"template: expected 18 sections (0-17), found {len(t_secs)}")
    if len(i_secs) != 18:
        errors.append(f"instance: expected 18 sections (0-17), found {len(i_secs)}")

    for idx in range(min(len(t_secs), len(i_secs))):
        tn, tt = t_secs[idx]
        inum, it = i_secs[idx]
        if tn != inum:
            errors.append(f"section index mismatch at position {idx}: template {tn} vs instance {inum}")
            continue
        if not section_titles_align(tt, it, tn):
            errors.append(
                f"section {tn} title mismatch: template={tt!r} instance={it!r}"
            )

    overall = "PASS" if not errors else "FAIL"
    report = {
        "tool": "verify_crsp_structure.py",
        "schema_version": "1.0.0",
        "overall": overall,
        "template_path": str(args.template),
        "instance_path": str(args.instance),
        "template_section_count": len(t_secs),
        "instance_section_count": len(i_secs),
        "errors": errors,
    }
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"overall": overall, "report": str(args.report)}, indent=2))
    return 0 if overall == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
