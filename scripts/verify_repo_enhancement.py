#!/usr/bin/env python3
"""Verify CRSP-REPO-ENHANCEMENT-2026-06-22 acceptance surfaces."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent


def read_text(relative_path: str) -> str:
    return (REPO_ROOT / relative_path).read_text(encoding="utf-8")


def require(condition: bool, message: str, failures: list[str]) -> None:
    prefix = "PASS" if condition else "FAIL"
    print(f"{prefix}: {message}")
    if not condition:
        failures.append(message)


def check_metadata(relative_path: str, failures: list[str]) -> None:
    text = read_text(relative_path)
    for field in ("authority:", "truth_surface:", "machine_enforced:"):
        require(field in text, f"{relative_path} contains `{field[:-1]}` metadata", failures)


def main() -> int:
    failures: list[str] = []

    for relative_path in (
        "PROGRAM_ARCHITECTURE.md",
        "MODULE_STATUS.md",
        "SOCIOTECHNICAL_CONSTITUTION.md",
    ):
        require((REPO_ROOT / relative_path).exists(), f"{relative_path} exists", failures)
        check_metadata(relative_path, failures)

    program_architecture = read_text("PROGRAM_ARCHITECTURE.md")
    require(
        "not a binding or canonical authority" in program_architecture,
        "PROGRAM_ARCHITECTURE.md declares itself non-canonical",
        failures,
    )

    module_status = read_text("MODULE_STATUS.md")
    require(
        "derived status surface" in module_status.lower(),
        "MODULE_STATUS.md declares itself derived",
        failures,
    )
    require(
        "not standalone evidence" in module_status.lower(),
        "MODULE_STATUS.md says it is insufficient as standalone evidence",
        failures,
    )

    trust_guide = read_text("docs/governance/TRUST_SURFACE_GUIDE.md").lower()
    for phrase in (
        "canonical",
        "narrative",
        "derived",
        "machine-enforced",
        "what is not claimed",
    ):
        require(
            phrase in trust_guide,
            f"TRUST_SURFACE_GUIDE.md explains `{phrase}`",
            failures,
        )

    tui = subprocess.run(
        ["node", "src/tui/index.js", "--snapshot"],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    require(tui.returncode == 0, "TUI snapshot command exits successfully", failures)
    require(
        "Show repository status" in tui.stdout
        and "Explain trust surfaces" in tui.stdout
        and "List what is not claimed" in tui.stdout,
        "TUI snapshot uses plain-English menu labels",
        failures,
    )

    if failures:
        print(f"\nVerification failed with {len(failures)} issue(s).")
        return 1

    print("\nAll repository enhancement checks passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
