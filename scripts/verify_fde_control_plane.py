#!/usr/bin/env python3
"""
Validate FDE control-plane evidence JSON against declared JSON Schemas and
optional promotion-readiness checks (dual-topology-verifier alignment).
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

try:
    import jsonschema
    from jsonschema import Draft202012Validator
except ImportError as e:
    print("jsonschema is required: pip install -r requirements-verify.txt", file=sys.stderr)
    raise SystemExit(2) from e

DEFAULT_INSTANCE = Path("projects/c-rsp/instances/CRSP-FDE-CTRL-PLANE-GAPS-002.md")


def load_json(path: Path) -> object:
    return json.loads(path.read_text(encoding="utf-8"))


def validate_schema_wellformed(schema_path: Path, report_details: list[dict]) -> bool:
    try:
        data = load_json(schema_path)
        Draft202012Validator.check_schema(data)
        report_details.append(
            {"target": str(schema_path), "kind": "meta_schema", "result": "PASS"}
        )
        return True
    except Exception as ex:
        report_details.append(
            {
                "target": str(schema_path),
                "kind": "meta_schema",
                "result": "FAIL",
                "error": str(ex),
            }
        )
        return False


def validate_instance(
    schema_path: Path,
    instance_path: Path,
    report_details: list[dict],
) -> bool:
    schema = load_json(schema_path)
    instance = load_json(instance_path)
    try:
        Draft202012Validator(schema).validate(instance)
        report_details.append(
            {
                "schema": str(schema_path),
                "instance": str(instance_path),
                "result": "PASS",
            }
        )
        return True
    except jsonschema.ValidationError as ex:
        report_details.append(
            {
                "schema": str(schema_path),
                "instance": str(instance_path),
                "result": "FAIL",
                "error": ex.message,
            }
        )
        return False


def validate_fde_lifecycle_file(
    schema_path: Path,
    evidence_path: Path,
    report_details: list[dict],
) -> bool:
    """Validate fde_operating_lifecycle subdocument when present."""
    schema = load_json(schema_path)
    doc = load_json(evidence_path)
    if "fde_operating_lifecycle" not in doc:
        report_details.append(
            {
                "schema": str(schema_path),
                "instance": str(evidence_path),
                "result": "SKIP",
                "detail": "no fde_operating_lifecycle key",
            }
        )
        return True
    wrapper = {"fde_operating_lifecycle": doc["fde_operating_lifecycle"]}
    try:
        Draft202012Validator(schema).validate(wrapper)
        report_details.append(
            {
                "schema": str(schema_path),
                "instance": str(evidence_path),
                "result": "PASS",
                "fragment": "fde_operating_lifecycle",
            }
        )
        return True
    except jsonschema.ValidationError as ex:
        report_details.append(
            {
                "schema": str(schema_path),
                "instance": str(evidence_path),
                "result": "FAIL",
                "error": ex.message,
            }
        )
        return False


def promotion_readiness(
    lock_path: Path,
    instance_path: Path,
    out: dict,
) -> bool:
    lock = load_json(lock_path)
    text = instance_path.read_text(encoding="utf-8")
    vclass = lock.get("verifier", {}).get("class")
    ok = True
    checks = []
    if vclass != "dual-topology-verifier":
        checks.append(
            {
                "check": "lock_verifier_class",
                "result": "FAIL",
                "expected": "dual-topology-verifier",
                "actual": vclass,
            }
        )
        ok = False
    else:
        checks.append({"check": "lock_verifier_class", "result": "PASS"})

    if "dual-topology-verifier" not in text:
        checks.append(
            {
                "check": "instance_mentions_dual_topology_verifier",
                "result": "FAIL",
            }
        )
        ok = False
    else:
        checks.append(
            {"check": "instance_mentions_dual_topology_verifier", "result": "PASS"}
        )

    if not re.search(r"Topology Mode:\s*\*?\*?Dual-Topology", text) and "Dual-Topology" not in text:
        checks.append({"check": "instance_dual_topology_mode", "result": "FAIL"})
        ok = False
    else:
        checks.append({"check": "instance_dual_topology_mode", "result": "PASS"})

    out["promotion_readiness_checks"] = checks
    return ok


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "--schemas",
        nargs="*",
        default=[],
        help="JSON Schema files to validate (well-formed) and apply to instances",
    )
    ap.add_argument("--report", type=Path, required=True)
    ap.add_argument(
        "--promotion-readiness",
        action="store_true",
        help="Check governance lock + instance verifier alignment",
    )
    ap.add_argument(
        "--lock",
        type=Path,
        default=Path("projects/c-rsp/governance-template.lock.json"),
    )
    ap.add_argument("--instance", type=Path, default=DEFAULT_INSTANCE)
    ap.add_argument(
        "--evidence-dir",
        type=Path,
        default=Path("evidence/fde-control-plane"),
    )
    args = ap.parse_args()

    details: list[dict] = []
    all_ok = True

    schema_paths = [Path(s) for s in args.schemas]

    for sp in schema_paths:
        if not validate_schema_wellformed(sp, details):
            all_ok = False

    evidence_dir = args.evidence_dir
    blind_man_sample = evidence_dir / "blind-man-step-sample.json"

    for sp in schema_paths:
        name = sp.name
        if name == "fde-lifecycle.schema.json":
            for ev in [
                evidence_dir / "lifecycle-transition-contract-record.json",
            ]:
                if ev.is_file():
                    if not validate_fde_lifecycle_file(sp, ev, details):
                        all_ok = False
        elif name == "blind-man-execution.schema.json":
            if blind_man_sample.is_file():
                if not validate_instance(sp, blind_man_sample, details):
                    all_ok = False
            else:
                details.append(
                    {
                        "schema": str(sp),
                        "instance": str(blind_man_sample),
                        "result": "FAIL",
                        "detail": "blind-man-step-sample.json required for schema validation",
                    }
                )
                all_ok = False

    if not schema_paths and not args.promotion_readiness:
        print("Provide --schemas and/or --promotion-readiness", file=sys.stderr)
        return 2

    report_body: dict = {
        "tool": "verify_fde_control_plane.py",
        "schema_version": "1.0.0",
        "overall_schema_validation": "PASS" if all_ok else "FAIL",
        "details": details,
    }

    if not schema_paths:
        report_body["overall_schema_validation"] = "SKIPPED"

    if args.promotion_readiness:
        pr_ok = promotion_readiness(args.lock, args.instance, report_body)
        report_body["promotion_readiness"] = "PASS" if pr_ok else "FAIL"
        if not pr_ok:
            all_ok = False

    report_body["overall"] = "PASS" if all_ok else "FAIL"

    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(json.dumps(report_body, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"overall": report_body["overall"], "report": str(args.report)}, indent=2))
    return 0 if all_ok else 1


if __name__ == "__main__":
    sys.exit(main())
