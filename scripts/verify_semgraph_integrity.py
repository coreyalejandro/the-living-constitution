from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import jsonschema


REPO_ROOT = Path(__file__).resolve().parents[1]


def load_json(path: Path) -> object:
    return json.loads(path.read_text(encoding="utf-8"))


def validate(instance_path: Path, schema_path: Path) -> None:
    instance = load_json(instance_path)
    schema = load_json(schema_path)
    jsonschema.validate(instance=instance, schema=schema)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--self-check",
        action="store_true",
        help="Verify required schemas exist and are parseable JSON.",
    )
    parser.add_argument(
        "--run",
        type=str,
        default=None,
        help="Path to a semgraph run JSON file (validates against its declared schema).",
    )
    args = parser.parse_args()

    impact_schema = REPO_ROOT / "verification/semgraph/ImpactReport.schema.json"
    drift_schema = REPO_ROOT / "verification/semgraph/ShadowDrift.schema.json"

    if args.self_check:
        _ = load_json(impact_schema)
        _ = load_json(drift_schema)
        return 0

    if args.run is None:
        parser.error("Provide --self-check or --run <path>.")

    run_path = Path(args.run).resolve()
    if not run_path.exists():
        raise FileNotFoundError(str(run_path))

    run_obj = load_json(run_path)
    if not isinstance(run_obj, dict) or "schema" not in run_obj or "data" not in run_obj:
        raise ValueError("Run JSON must be an object with keys: {schema, data}.")

    schema_name = run_obj["schema"]
    data_path = run_path.parent / f"{run_path.stem}.data.json"

    if schema_name == "ImpactReport":
        schema_path = impact_schema
    elif schema_name == "ShadowDrift":
        schema_path = drift_schema
    else:
        raise ValueError(f"Unknown schema: {schema_name!r}")

    # Validate either embedded `data` or the optional adjacent `.data.json` mirror.
    data = run_obj["data"]
    jsonschema.validate(instance=data, schema=load_json(schema_path))

    if data_path.exists():
        validate(data_path, schema_path)

    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"verify_semgraph_integrity.py: FAIL: {exc}", file=sys.stderr)
        raise

