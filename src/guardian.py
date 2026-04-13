#!/usr/bin/env python3
"""
Guardian Kernel — MCP Safety Enforcement Server
Contract: CRSP-001
Version: 1.0.0
Status: Draft → Active (in progress)

An MCP server that acts as an inescapable constitutional cage — physically 
intercepting every agent tool call and enforcing safety invariants before 
any code is written.
"""
import argparse
import hashlib
import json
import sys
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator  # type: ignore[import-untyped]

TRINITY_FILES = [
    "THE_LIVING_CONSTITUTION.md",
    "CLAUDE.md",
    "MASTER_PROJECT_INVENTORY.md",
]
TRINITY_HASHES_LOG = "verification/crsp_CRSP-001_log.json"
DEFAULT_EVAL_EVIDENCE_SCHEMA = "projects/c-rsp/schemas/evidence_schema.json"
DEFAULT_EVAL_EVIDENCE_DIR = "projects/08-evaluation/verification"
REPO_ROOT = Path(__file__).resolve().parents[1]
WRITE_TOOLS = {"write_file", "edit_file", "str_replace"}
READ_ONLY_TOOLS = {"read_file"}
PROTECTED_FILES = {
    "THE_LIVING_CONSTITUTION.md",
    "CLAUDE.md",
    "MASTER_PROJECT_INVENTORY.md",
}
VERIFICATION_DIR = REPO_ROOT / "verification"
LOG_PATH = REPO_ROOT / TRINITY_HASHES_LOG


class GuardianState(str, Enum):
    INIT = "INIT"
    ACTIVE = "ACTIVE"
    SAFE_HALT = "SAFE_HALT"
    FAIL_HALT = "FAIL_HALT"


_state = GuardianState.INIT
_invariants = []
CONSTITUTIONAL_INVARIANTS = [
    {"id": "INVARIANT_TRINITY_01", "severity": "CRITICAL"},
    {"id": "INVARIANT_ARTICLE_I_01", "severity": "CRITICAL"},
    {"id": "INVARIANT_ARTICLE_I_02", "severity": "HIGH"},
    {"id": "INVARIANT_ARTICLE_II_01", "severity": "CRITICAL"},
    {"id": "INVARIANT_ARTICLE_II_02", "severity": "HIGH"},
    {"id": "INVARIANT_ARTICLE_III_01", "severity": "HIGH"},
    {"id": "INVARIANT_ARTICLE_IV_01", "severity": "CRITICAL"},
    {"id": "INVARIANT_ARTICLE_V_01", "severity": "CRITICAL"},
    {"id": "INVARIANT_READ_ONLY_01", "severity": "CRITICAL"},
    {"id": "INVARIANT_EVIDENCE_01", "severity": "HIGH"},
    {"id": "INVARIANT_GUARDIAN_LOG_01", "severity": "HIGH"},
]

def bootstrap_trinity() -> dict[str, Any]:
    hashes = {}
    for filename in TRINITY_FILES:
        filepath = REPO_ROOT / filename
        if not filepath.exists():
            return {"status": "FAIL", "hashes": {}, "error": f"Trinity file missing: {filename}"}
        if not filepath.is_file():
            return {"status": "FAIL", "hashes": {}, "error": f"Trinity path is not a file: {filename}"}
        try:
            content = filepath.read_bytes()
            file_hash = hashlib.sha256(content).hexdigest()[:16]
            hashes[filename] = file_hash
        except IOError as e:
            return {"status": "FAIL", "hashes": {}, "error": f"Cannot read {filename}: {e}"}
    return {"status": "PASS", "hashes": hashes, "error": None}

def log_trinity_bootstrap(result: dict[str, Any]) -> None:
    log_path = REPO_ROOT / TRINITY_HASHES_LOG
    log_path.parent.mkdir(parents=True, exist_ok=True)
    
    log_entry = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "operation": "OP-BOOTSTRAP",
        "trinity_bootstrap": result,
        "invariants_evaluated": ["INVARIANT_TRINITY_01"],
        "decision": result["status"]
    }
    
    if log_path.exists():
        with open(log_path, "r") as f:
            try:
                log_data = json.load(f)
                if not isinstance(log_data, list):
                    log_data = [log_data]
            except json.JSONDecodeError:
                log_data = []
    else:
        log_data = []
        
    log_data.append(log_entry)
    
    with open(log_path, "w") as f:
        json.dump(log_data, f, indent=2)

class GuardianMCP:
    def __init__(self):
        self.trinity_status = None
        self.invariants = []
        self.interceptors = {}

    def initialize(self) -> bool:
        self.trinity_status = bootstrap_trinity()
        if self.trinity_status["status"] != "PASS":
            return False
        log_trinity_bootstrap(self.trinity_status)
        return True

    def health_check(self) -> bool:
        if self.trinity_status is None:
            self.trinity_status = bootstrap_trinity()
        return self.trinity_status["status"] == "PASS"


def load_invariants() -> list[dict[str, str]]:
    global _invariants
    _invariants = list(CONSTITUTIONAL_INVARIANTS)
    return _invariants


def _append_log(record: dict[str, Any]) -> None:
    log_path = LOG_PATH
    log_path.parent.mkdir(parents=True, exist_ok=True)
    if log_path.exists():
        try:
            existing: Any = _load_json(log_path)
            if not isinstance(existing, list):
                existing = [existing]
        except json.JSONDecodeError:
            existing = []
    else:
        existing = []
    existing.append(record)
    with log_path.open("w", encoding="utf-8") as f:
        json.dump(existing, f, indent=2)


def evaluate_invariants(agent_id: str, tool_name: str, params: dict[str, Any]) -> dict[str, Any]:
    violated = []
    invariant_results = []
    agent_id = agent_id.lower()
    tool_name = tool_name.lower()

    forbidden_by_agent = {
        "planner": {"deploy_production"},
        "builder": {"deploy"},
        "sentinel": {"override_agent"},
        "tdd": {"skip_red_phase"},
        "reviewer": {"approve_own_work"},
        "datasci": {"redefine_toca_nodes"},
    }
    if tool_name in forbidden_by_agent.get(agent_id, set()):
        violated.append("INVARIANT_ARTICLE_IV_01")
        invariant_results.append(
            {
                "invariant_id": "INVARIANT_ARTICLE_IV_01",
                "result": "FAIL",
                "severity": "CRITICAL",
            }
        )
    else:
        invariant_results.append(
            {
                "invariant_id": "INVARIANT_ARTICLE_IV_01",
                "result": "PASS",
                "severity": "CRITICAL",
            }
        )

    if tool_name not in READ_ONLY_TOOLS and not params.get("toca_anchor"):
        violated.append("INVARIANT_ARTICLE_III_01")
        invariant_results.append(
            {
                "invariant_id": "INVARIANT_ARTICLE_III_01",
                "result": "FAIL",
                "severity": "HIGH",
            }
        )
    else:
        invariant_results.append(
            {
                "invariant_id": "INVARIANT_ARTICLE_III_01",
                "result": "PASS",
                "severity": "HIGH",
            }
        )

    target_raw = str(params.get("path", "")).strip()
    target_name = Path(target_raw).name if target_raw else ""
    if (
        tool_name in WRITE_TOOLS
        and target_name in PROTECTED_FILES
        and not params.get("human_crypto_signature")
    ):
        violated.append("INVARIANT_READ_ONLY_01")
        invariant_results.append(
            {
                "invariant_id": "INVARIANT_READ_ONLY_01",
                "result": "FAIL",
                "severity": "CRITICAL",
            }
        )
    else:
        invariant_results.append(
            {
                "invariant_id": "INVARIANT_READ_ONLY_01",
                "result": "PASS",
                "severity": "CRITICAL",
            }
        )

    decision = "FAIL" if violated else "PASS"
    verdict = {
        "decision": decision,
        "agent_id": agent_id,
        "tool_name": tool_name,
        "violated_invariants": violated,
        "invariant_results": invariant_results,
        "rationale": "blocked by constitutional invariant" if violated else "all invariants passed",
    }
    _append_log(
        {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "operation": "OP-INTERCEPT-LOOP",
            "decision": decision,
            "agent_id": agent_id,
            "tool_name": tool_name,
            "invariants_evaluated": [item["invariant_id"] for item in invariant_results],
            "violated_invariants": violated,
            "rationale": verdict["rationale"],
        }
    )
    return verdict


def emit_stop(agent_id: str, invariant_id: str, reason: str) -> dict[str, Any]:
    halt_state = "FAIL_HALT" if invariant_id in {"INVARIANT_READ_ONLY_01", "INVARIANT_ARTICLE_IV_01"} else "SAFE_HALT"
    record = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "operation": "OP-FAIL-HALT",
        "signal": "STOP",
        "agent_id": agent_id,
        "invariant_violated": invariant_id,
        "reason": reason,
        "halt_state": halt_state,
    }
    _append_log(record)
    return record


def _load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def verify_evidence(evidence_dir: Path, schema_path: Path) -> dict[str, Any]:
    if not evidence_dir.exists() or not evidence_dir.is_dir():
        return {
            "status": "FAIL",
            "error": f"Evidence directory missing: {evidence_dir}",
            "files_checked": 0,
            "invalid_files": [],
        }
    if not schema_path.exists() or not schema_path.is_file():
        return {
            "status": "FAIL",
            "error": f"Schema file missing: {schema_path}",
            "files_checked": 0,
            "invalid_files": [],
        }

    schema = _load_json(schema_path)
    validator = Draft202012Validator(schema)
    invalid_files: list[dict[str, Any]] = []
    files_checked = 0

    for json_file in sorted(evidence_dir.glob("*.json")):
        files_checked += 1
        try:
            payload = _load_json(json_file)
        except json.JSONDecodeError as err:
            invalid_files.append(
                {"file": str(json_file), "error": f"JSON decode error: {err}"}
            )
            continue

        errors = list(validator.iter_errors(payload))
        if errors:
            invalid_files.append(
                {
                    "file": str(json_file),
                    "error_count": len(errors),
                    "first_error": errors[0].message,
                }
            )

    status = "PASS" if not invalid_files and files_checked > 0 else "FAIL"
    if files_checked == 0:
        invalid_files.append({"file": str(evidence_dir), "error": "No evidence JSON files found"})
    return {
        "status": status,
        "schema": str(schema_path),
        "evidence_dir": str(evidence_dir),
        "files_checked": files_checked,
        "invalid_files": invalid_files,
    }


def check_eval001_compliance(evidence_dir: Path) -> dict[str, Any]:
    if not evidence_dir.exists() or not evidence_dir.is_dir():
        return {"status": "FAIL", "error": f"Evidence directory missing: {evidence_dir}"}

    required_patterns = [
        "crsp_EVAL-001_log.json",
        "topology_validation_*.json",
        "suite_config_*.json",
        "dataset_validation_*.json",
        "eval_results_*.json",
        "recurrence_analysis_*.json",
        "ci_signal_*.json",
    ]

    missing = []
    for pattern in required_patterns:
        if not list(evidence_dir.glob(pattern)):
            missing.append(pattern)

    if missing:
        return {
            "status": "FAIL",
            "error": "Missing required evidence artifacts",
            "missing_patterns": missing,
        }

    log_path = evidence_dir / "crsp_EVAL-001_log.json"
    try:
        log_data = _load_json(log_path)
    except json.JSONDecodeError as err:
        return {"status": "FAIL", "error": f"Invalid log JSON: {err}"}
    if isinstance(log_data, list):
        if not log_data:
            return {"status": "FAIL", "error": "Log file contains empty array"}
        log_data = log_data[-1]
    if not isinstance(log_data, dict):
        return {"status": "FAIL", "error": "Unsupported log structure"}

    ci_files = sorted(evidence_dir.glob("ci_signal_*.json"))
    latest_ci = ci_files[-1]
    ci_data = _load_json(latest_ci)
    ci_status = ci_data.get("status")

    compliance_ok = (
        log_data.get("contract_id") == "EVAL-001"
        and log_data.get("ci_compliance_bit") == 1
        and ci_status == 1
    )

    return {
        "status": "PASS" if compliance_ok else "FAIL",
        "contract_id": log_data.get("contract_id"),
        "log_status": log_data.get("status"),
        "ci_compliance_bit": log_data.get("ci_compliance_bit"),
        "ci_signal_file": latest_ci.name,
        "ci_signal_status": ci_status,
    }

def main():
    parser = argparse.ArgumentParser(description="Guardian Kernel")
    parser.add_argument("--health-check", action="store_true")
    parser.add_argument("--verify-evidence", type=str, default=None)
    parser.add_argument("--schema", type=str, default=DEFAULT_EVAL_EVIDENCE_SCHEMA)
    parser.add_argument("--check-compliance", type=str, default=None)
    parser.add_argument("--evidence-dir", type=str, default=DEFAULT_EVAL_EVIDENCE_DIR)
    parser.add_argument("--verbose", "-v", action="store_true")
    args = parser.parse_args()

    if args.health_check:
        guardian = GuardianMCP()
        ok = guardian.health_check()
        if args.verbose and not ok:
            status = guardian.trinity_status
            print(f"Trinity bootstrap failed: {status.get('error', 'Unknown')}", file=sys.stderr)
        print("PASS" if ok else "FAIL")
        sys.exit(0 if ok else 1)

    if args.verify_evidence:
        result = verify_evidence(Path(args.verify_evidence), Path(args.schema))
        if args.verbose:
            print(json.dumps(result, indent=2))
        print(result["status"])
        sys.exit(0 if result["status"] == "PASS" else 1)

    if args.check_compliance:
        if args.check_compliance != "EVAL-001":
            print("FAIL")
            if args.verbose:
                print(
                    json.dumps(
                        {
                            "status": "FAIL",
                            "error": f"Unsupported contract id: {args.check_compliance}",
                        },
                        indent=2,
                    )
                )
            sys.exit(1)
        result = check_eval001_compliance(Path(args.evidence_dir))
        if args.verbose:
            print(json.dumps(result, indent=2))
        print(result["status"])
        sys.exit(0 if result["status"] == "PASS" else 1)

    guardian = GuardianMCP()
    initialized = guardian.initialize()
    
    print("Guardian Kernel — CRSP-001")
    print(f"Trinity bootstrap: {guardian.trinity_status['status']}")
    sys.exit(0 if initialized else 1)

if __name__ == "__main__":
    main()
