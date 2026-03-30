#!/usr/bin/env python3
"""
CI-only: download-artifact self-check for governance verification runs.

Reads JSON from GITHUB_ARTIFACT_DIR (recursive), validates against
verification/governance-verification-run.schema.json, asserts commit_hash == GITHUB_SHA,
and ensures the artifact is non-empty (required fields present).

Exit: 0 OK, 1 validation failure, 2 usage/IO error
"""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path

try:
    from jsonschema import Draft202012Validator
except ImportError:
    print(
        "ERROR: jsonschema is required. Install: pip install -r requirements-verify.txt",
        file=sys.stderr,
    )
    sys.exit(2)


def _load_json(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as f:
        data = json.load(f)
    if not isinstance(data, dict):
        raise ValueError("root must be object")
    return data


def main() -> None:
    root = Path(os.environ.get("GITHUB_WORKSPACE", ".")).resolve()
    ad = os.environ.get("GITHUB_ARTIFACT_DIR", "").strip()
    if not ad:
        print("ERROR: GITHUB_ARTIFACT_DIR is required", file=sys.stderr)
        sys.exit(2)
    artifact_dir = (root / ad).resolve() if not Path(ad).is_absolute() else Path(ad).resolve()
    gsha = (os.environ.get("GITHUB_SHA") or "").strip()
    if not gsha:
        print("ERROR: GITHUB_SHA empty", file=sys.stderr)
        sys.exit(1)

    if not artifact_dir.is_dir():
        print(f"ERROR: artifact dir missing: {artifact_dir}", file=sys.stderr)
        sys.exit(1)

    json_files = sorted(artifact_dir.rglob("*.json"))
    if not json_files:
        print(f"ERROR: no JSON under {artifact_dir}", file=sys.stderr)
        sys.exit(1)

    prefer = [p for p in json_files if p.name.endswith("-governance.json")]
    pick_from = prefer if prefer else json_files
    artifact_path = max(pick_from, key=lambda p: p.stat().st_mtime)

    schema_path = root / "verification" / "governance-verification-run.schema.json"
    if not schema_path.is_file():
        print(f"ERROR: schema missing: {schema_path}", file=sys.stderr)
        sys.exit(2)

    schema = _load_json(schema_path)
    Draft202012Validator.check_schema(schema)
    validator = Draft202012Validator(schema)

    try:
        payload = _load_json(artifact_path)
    except (OSError, json.JSONDecodeError, ValueError) as e:
        print(f"ERROR: cannot parse artifact {artifact_path}: {e}", file=sys.stderr)
        sys.exit(1)

    try:
        validator.validate(payload)
    except Exception as e:
        print(f"ERROR: schema validation failed: {e}", file=sys.stderr)
        sys.exit(1)

    ch = str(payload.get("commit_hash") or "").strip()
    if len(ch) < 7:
        print("ERROR: commit_hash empty or too short in artifact", file=sys.stderr)
        sys.exit(1)
    if ch != gsha:
        print(
            f"ERROR: commit_hash mismatch: artifact={ch!r} GITHUB_SHA={gsha!r}",
            file=sys.stderr,
        )
        sys.exit(1)

    if not payload.get("timestamp"):
        print("ERROR: artifact timestamp empty", file=sys.stderr)
        sys.exit(1)

    print(f"OK: CI self-verify passed for {artifact_path.relative_to(root)}")
    sys.exit(0)


if __name__ == "__main__":
    main()
