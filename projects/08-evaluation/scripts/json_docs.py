#!/usr/bin/env python3
"""
JSON-canonical document management for 08-evaluation.

This keeps JSON as the source of truth while still generating markdown
compatibility files required by humans and existing tooling.
"""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = ROOT / "docs_json" / "manifest.json"
SCHEMA_VERSION = "1.0"


@dataclass(frozen=True)
class DocEntry:
    document_id: str
    source_json: str
    output_markdown: str

    @staticmethod
    def from_dict(raw: dict[str, str]) -> "DocEntry":
        return DocEntry(
            document_id=raw["document_id"],
            source_json=raw["source_json"],
            output_markdown=raw["output_markdown"],
        )


def _load_manifest() -> list[DocEntry]:
    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    return [DocEntry.from_dict(entry) for entry in manifest["documents"]]


def _extract_title(markdown: str, fallback: str) -> str:
    for line in markdown.splitlines():
        stripped = line.strip()
        if stripped.startswith("# "):
            return stripped[2:].strip()
    return fallback


def _source_path(entry: DocEntry) -> Path:
    return ROOT / entry.source_json


def _output_path(entry: DocEntry) -> Path:
    return ROOT / entry.output_markdown


def _render_text(source_payload: dict[str, object], source_relative_path: str) -> str:
    body = str(source_payload["body_markdown"]).rstrip() + "\n"
    banner = (
        "<!-- GENERATED FILE: edit JSON source instead.\n"
        f"     source: {source_relative_path}\n"
        "-->\n\n"
    )
    return banner + body


def _validate_source_payload(payload: dict[str, object], source_path: Path) -> None:
    required_fields = (
        "schema_version",
        "document_id",
        "title",
        "output_markdown",
        "canonical_format",
        "last_generated_utc",
        "body_markdown",
    )
    missing = [field for field in required_fields if field not in payload]
    if missing:
        raise ValueError(f"{source_path}: missing required fields: {', '.join(missing)}")

    if payload["schema_version"] != SCHEMA_VERSION:
        raise ValueError(
            f"{source_path}: unsupported schema_version={payload['schema_version']!r}; "
            f"expected {SCHEMA_VERSION!r}"
        )
    if payload["canonical_format"] != "json":
        raise ValueError(
            f"{source_path}: canonical_format must be 'json', got {payload['canonical_format']!r}"
        )


def bootstrap(force: bool) -> None:
    entries = _load_manifest()
    created = 0

    for entry in entries:
        source_path = _source_path(entry)
        output_path = _output_path(entry)

        if source_path.exists() and not force:
            continue
        if not output_path.exists():
            raise FileNotFoundError(f"Missing markdown file for bootstrap: {output_path}")

        markdown_body = output_path.read_text(encoding="utf-8")
        title = _extract_title(markdown_body, entry.document_id)
        payload = {
            "schema_version": SCHEMA_VERSION,
            "document_id": entry.document_id,
            "title": title,
            "output_markdown": entry.output_markdown,
            "canonical_format": "json",
            "last_generated_utc": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
            "body_markdown": markdown_body,
        }

        source_path.parent.mkdir(parents=True, exist_ok=True)
        source_path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
        created += 1

    print(f"Bootstrapped {created} JSON source file(s).")


def render() -> None:
    entries = _load_manifest()
    written = 0

    for entry in entries:
        source_path = _source_path(entry)
        if not source_path.exists():
            raise FileNotFoundError(f"Missing JSON source file: {source_path}")

        payload = json.loads(source_path.read_text(encoding="utf-8"))
        _validate_source_payload(payload, source_path)
        output_path = _output_path(entry)
        expected = _render_text(payload, entry.source_json)
        current_output = output_path.read_text(encoding="utf-8") if output_path.exists() else ""

        if current_output != expected:
            payload["last_generated_utc"] = datetime.now(timezone.utc).isoformat().replace(
                "+00:00", "Z"
            )
            source_path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
            output_path.write_text(_render_text(payload, entry.source_json), encoding="utf-8")
            written += 1

    print(f"Rendered {written} markdown file(s).")


def check() -> None:
    entries = _load_manifest()
    mismatches: list[str] = []

    for entry in entries:
        source_path = _source_path(entry)
        output_path = _output_path(entry)

        if not source_path.exists():
            mismatches.append(f"{entry.document_id}: missing source JSON ({entry.source_json})")
            continue
        if not output_path.exists():
            mismatches.append(f"{entry.document_id}: missing markdown output ({entry.output_markdown})")
            continue

        payload = json.loads(source_path.read_text(encoding="utf-8"))
        _validate_source_payload(payload, source_path)
        expected = _render_text(payload, entry.source_json)
        actual = output_path.read_text(encoding="utf-8")
        if expected != actual:
            mismatches.append(
                f"{entry.document_id}: stale markdown ({entry.output_markdown}) does not match JSON source"
            )

    if mismatches:
        print("JSON-doc check failed:")
        for issue in mismatches:
            print(f" - {issue}")
        raise SystemExit(1)

    print(f"JSON-doc check passed for {len(entries)} file(s).")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    bootstrap_parser = subparsers.add_parser("bootstrap", help="Create JSON sources from existing markdown")
    bootstrap_parser.add_argument("--force", action="store_true", help="Overwrite existing JSON source files")

    subparsers.add_parser("render", help="Render markdown files from JSON source files")
    subparsers.add_parser("check", help="Verify rendered markdown matches JSON source files")
    args = parser.parse_args()

    if args.command == "bootstrap":
        bootstrap(force=args.force)
    elif args.command == "render":
        render()
    elif args.command == "check":
        check()


if __name__ == "__main__":
    main()
