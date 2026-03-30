#!/usr/bin/env python3
"""
PASS 10A / PASS 11: Single-entry truth surface.

Aggregates MASTER_PROJECT_INVENTORY ci_provenance, immutable verification anchor
(tag + commit), informational git HEAD, workflow SHA, regression ledger tail,
remote evidence record, and cross-repo check into STATUS.json; renders
deterministic STATUS.md from STATUS.json.

Manual edits to STATUS.md are prohibited; regenerate with this script.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from json import JSONDecodeError
from pathlib import Path
from typing import Any, Dict, List, Tuple


def _load_json(path: Path) -> Dict[str, Any]:
    with path.open("r", encoding="utf-8") as f:
        data = json.load(f)
    if not isinstance(data, dict):
        raise ValueError(f"expected object: {path}")
    return data


def _git_head(root: Path) -> str:
    r = subprocess.run(
        ["git", "-C", str(root), "rev-parse", "HEAD"],
        capture_output=True,
        text=True,
        check=False,
    )
    h = (r.stdout or "").strip()
    if r.returncode != 0 or len(h) < 7:
        raise RuntimeError("git rev-parse HEAD failed; repository required for STATUS.json")
    return h


def _workflow_sha256(root: Path) -> str:
    p = root / ".github" / "workflows" / "verify.yml"
    if not p.is_file():
        return ""
    return hashlib.sha256(p.read_bytes()).hexdigest()


def _cross_repo_state(root: Path) -> Dict[str, Any]:
    inv_path = root / "MASTER_PROJECT_INVENTORY.json"
    try:
        inv = _load_json(inv_path) if inv_path.is_file() else {}
    except (OSError, ValueError, JSONDecodeError):
        inv = {}
    meta = inv.get("meta") if isinstance(inv.get("meta"), dict) else {}
    if str(meta.get("inventory_kind") or "") == "consentchain_governance_inventory":
        return {
            "state": "aligned",
            "exit_code": 0,
            "detail": "Satellite repo; canonical↔satellite cross-repo verification runs in The Living Constitution CI.",
        }
    target = root / "projects" / "consentchain" / "00-constitution" / "invariant-registry.json"
    if not target.is_file():
        return {
            "state": "target_incomplete",
            "detail": "projects/consentchain governance tree not present (init submodule for full check)",
        }
    r = subprocess.run(
        [
            sys.executable,
            str(root / "scripts" / "verify_cross_repo_consistency.py"),
            "--canonical-root",
            str(root),
            "--target-root",
            str(root / "projects" / "consentchain"),
        ],
        cwd=str(root),
        capture_output=True,
        text=True,
    )
    if r.returncode == 0:
        return {"state": "aligned", "exit_code": 0}
    if r.returncode == 1:
        return {"state": "drift", "exit_code": 1, "detail": (r.stderr or r.stdout or "").strip()[:500]}
    return {"state": "error", "exit_code": r.returncode, "detail": (r.stderr or r.stdout or "").strip()[:500]}


def aggregate_status(root: Path) -> Dict[str, Any]:
    inv = _load_json(root / "MASTER_PROJECT_INVENTORY.json")
    cp = inv.get("ci_provenance") or {}
    if not isinstance(cp, dict):
        raise ValueError("MASTER_PROJECT_INVENTORY.json: ci_provenance missing")
    rec = _load_json(root / "verification" / "ci-remote-evidence" / "record.json")
    ledger = _load_json(root / "verification" / "regression-ledger" / "ledger.json")
    records: List[Dict[str, Any]] = [x for x in (ledger.get("records") or []) if isinstance(x, dict)]
    last_ledger = records[-1] if records else {}
    policy_path = root / "verification" / "closed-epistemics-open-interfaces-policy.json"
    policy = _load_json(policy_path) if policy_path.is_file() else {}
    tb = policy.get("truth_boundary") if isinstance(policy, dict) else {}
    truth_reason = ""
    if isinstance(tb, dict):
        truth_reason = str(tb.get("reason") or "").strip()

    head = _git_head(root)
    wf_sha = _workflow_sha256(root)
    meta = inv.get("meta") if isinstance(inv.get("meta"), dict) else {}
    project = str(meta.get("repo") or "").strip()
    if not project:
        ik = str(meta.get("inventory_kind") or "")
        if ik == "consentchain_governance_inventory":
            project = "coreyalejandro/consentchain"
        else:
            project = "coreyalejandro/the-living-constitution"

    vac = str(cp.get("verification_anchor_commit") or "").strip()
    vat = str(cp.get("verification_anchor_tag") or "").strip()
    truth_anchor: Dict[str, Any] = {}
    if vac and vat:
        truth_anchor = {"type": "git_tag", "value": vat, "commit": vac}

    out: Dict[str, Any] = {
        "schema_version": "1.1.0",
        "project": project,
        "head_sha": head,
        "last_verified_commit": str(cp.get("last_verified_commit") or ""),
        "last_verified_run_id": str(cp.get("last_verified_run_id") or ""),
        "tip_state_truth": str(cp.get("tip_state_truth") or ""),
        "historical_state": {
            "regression_ledger_last_run_id": str(last_ledger.get("run_id") or ""),
            "regression_ledger_last_commit_sha": str(last_ledger.get("commit_sha") or ""),
            "regression_ledger_last_timestamp_utc": str(last_ledger.get("timestamp_utc") or ""),
            "ci_remote_record_captured_at_utc": str(rec.get("captured_at_utc") or ""),
        },
        "workflow_sha": wf_sha,
        "cross_repo_consistency": _cross_repo_state(root),
        "escalation_state": str(cp.get("escalation_state") or ""),
        "reviewer_status": str(cp.get("reviewer_status") or ""),
        "truth_boundary": {
            "reason": truth_reason,
            "policy_reference": "verification/closed-epistemics-open-interfaces-policy.json",
        },
        "inventory_meta_generated_at_utc": str((inv.get("meta") or {}).get("generated_at_utc") or ""),
        "governance_contract_version": str((inv.get("governance_artifacts") or {}).get("contract_version") or ""),
    }
    if truth_anchor:
        out["truth_anchor"] = truth_anchor
        out["verification_target"] = vac
    return out


def _status_doc_title(project: str) -> str:
    pl = (project or "").lower()
    if "consentchain" in pl:
        return "ConsentChain repository status"
    return "TLC repository status"


def render_markdown_from_status(data: Dict[str, Any]) -> str:
    """Deterministic Markdown mirror of STATUS.json (INVARIANT_39)."""
    proj = str(data.get("project") or "")
    title = _status_doc_title(proj)
    lines: List[str] = [
        f"# {title}",
        "",
        "> **Canonical JSON:** [`STATUS.json`](STATUS.json) — sole authoritative current-status artifact (PASS 10A).",
        "> **PASS 11:** Governance truth is anchored to `truth_anchor` / `verification_target` (immutable tag + commit). `head_sha` is informational only.",
        "",
        "| Field | Value |",
        "|-------|-------|",
    ]
    rows = [
        ("project", data.get("project")),
        ("verification_target", data.get("verification_target")),
        ("head_sha", data.get("head_sha")),
        ("last_verified_commit", data.get("last_verified_commit")),
        ("last_verified_run_id", data.get("last_verified_run_id")),
        ("tip_state_truth", data.get("tip_state_truth")),
        ("workflow_sha", data.get("workflow_sha")),
        ("escalation_state", data.get("escalation_state")),
        ("reviewer_status", data.get("reviewer_status")),
        ("governance_contract_version", data.get("governance_contract_version")),
        ("inventory_meta_generated_at_utc", data.get("inventory_meta_generated_at_utc")),
    ]
    for k, v in rows:
        lines.append(f"| `{k}` | `{v}` |")

    ta = data.get("truth_anchor")
    if isinstance(ta, dict) and ta:
        lines.extend(["", "## Immutable truth anchor (PASS 11)", ""])
        lines.append(f"- **type:** `{ta.get('type')}`")
        lines.append(f"- **tag:** `{ta.get('value')}`")
        lines.append(f"- **commit:** `{ta.get('commit')}`")

    lines.extend(
        [
            "",
            "## Historical / evidence anchors",
            "",
        ]
    )
    hist = data.get("historical_state")
    if isinstance(hist, dict):
        for key in sorted(hist.keys()):
            lines.append(f"- **{key}:** `{hist.get(key)}`")
    else:
        lines.append("- *(none)*")

    cr_heading = (
        "## Cross-repo consistency (canonical TLC CI)"
        if "consentchain" in proj.lower()
        else "## Cross-repo consistency (ConsentChain submodule)"
    )
    lines.extend(["", cr_heading, ""])
    cr = data.get("cross_repo_consistency")
    if isinstance(cr, dict):
        lines.append(f"- **state:** `{cr.get('state')}`")
        if cr.get("detail"):
            lines.append(f"- **detail:** {cr.get('detail')}")
    else:
        lines.append("- *(missing)*")

    lines.extend(["", "## Truth boundary", ""])
    tb = data.get("truth_boundary")
    if isinstance(tb, dict):
        reason = str(tb.get("reason") or "").strip()
        pref = str(tb.get("policy_reference") or "").strip()
        lines.append(reason)
        lines.append("")
        lines.append(f"Policy: `{pref}`")
    else:
        lines.append("*(see STATUS.json)*")

    lines.append("")
    return "\n".join(lines)


def _parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--root", type=Path, default=None, help="Repository root")
    p.add_argument(
        "--check",
        action="store_true",
        help="Exit 1 if STATUS.json or STATUS.md differs from aggregate/render (no writes)",
    )
    return p.parse_args()


def main() -> int:
    args = _parse_args()
    script_dir = Path(__file__).resolve().parent
    root = (args.root or script_dir.parent).resolve()

    aggregated = aggregate_status(root)
    status_path = root / "STATUS.json"
    md_path = root / "STATUS.md"
    rendered_md = render_markdown_from_status(aggregated)

    if args.check:
        errs: List[str] = []
        if not status_path.is_file():
            print("CHECK FAIL: STATUS.json missing", file=sys.stderr)
            return 1
        on_disk = _load_json(status_path)
        agg_n = dict(aggregated)
        disk_n = dict(on_disk)
        agg_x = {k: v for k, v in agg_n.items() if k != "head_sha"}
        disk_x = {k: v for k, v in disk_n.items() if k != "head_sha"}
        if json.dumps(disk_x, sort_keys=True) != json.dumps(agg_x, sort_keys=True):
            errs.append(
                "STATUS.json does not match aggregate_status (PASS 11: equality excludes informational head_sha)"
            )
        if not md_path.is_file():
            errs.append("STATUS.md missing")
        else:
            existing = md_path.read_text(encoding="utf-8")
            expected_check_md = render_markdown_from_status(disk_n)
            if existing.replace("\r\n", "\n") != expected_check_md.replace("\r\n", "\n"):
                errs.append("STATUS.md does not match render_markdown_from_status(STATUS.json)")
        for e in errs:
            print(f"CHECK FAIL: {e}", file=sys.stderr)
        return 1 if errs else 0

    status_path.write_text(json.dumps(aggregated, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    md_path.write_text(rendered_md, encoding="utf-8")
    print(f"OK: wrote {status_path.relative_to(root)} and {md_path.relative_to(root)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
