from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from pathlib import Path

from apps.tlc_semgraph.engine.multilang import build_multilang_graph
from apps.tlc_semgraph.engine.ripple import ripple_bfs


REPO_ROOT = Path(__file__).resolve().parents[3]


def _run_git(args: list[str]) -> str:
    proc = subprocess.run(
        ["git", *args],
        cwd=str(REPO_ROOT),
        check=True,
        capture_output=True,
        text=True,
    )
    return proc.stdout.strip()


def _sha12(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:12]


def _direct_units_with_symbols(
    paths: set[str], symbols_by_file: dict[str, list[str]]
) -> list[dict[str, str]]:
    units: list[dict[str, str]] = []
    for p in sorted(paths):
        units.append({"id": p, "kind": "file", "path": p})
        for sym in symbols_by_file.get(p, []):
            units.append(
                {
                    "id": f"{p}#{sym}",
                    "kind": "symbol",
                    "path": p,
                    "symbol": sym,
                }
            )
    return units


def build_cmd(source_root: str) -> Path:
    source_path = (REPO_ROOT / source_root).resolve()
    graph = build_multilang_graph(REPO_ROOT, source_path)

    payload = {
        "graph_version": "0.2.0",
        "repo_root": str(REPO_ROOT),
        "source_root": source_root,
        "nodes": sorted(graph.edges.keys()),
        "edges": {k: sorted(v) for k, v in graph.edges.items()},
        "symbols_by_file": {k: list(v) for k, v in graph.symbols_by_file.items()},
    }
    encoded = json.dumps(payload, sort_keys=True)
    graph_id = _sha12(encoded)

    out_dir = REPO_ROOT / "verification/semgraph/snapshots"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / f"graph-{graph_id}.json"
    out_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return out_path


def diff_cmd(base: str, head: str, source_root: str, max_depth: int) -> Path:
    snapshot_path = build_cmd(source_root)
    snapshot = json.loads(snapshot_path.read_text(encoding="utf-8"))
    edges: dict[str, set[str]] = {k: set(v) for k, v in snapshot["edges"].items()}
    symbols_by_file: dict[str, list[str]] = snapshot.get("symbols_by_file", {})

    changed_files = set(
        f for f in _run_git(["diff", "--name-only", base, head]).splitlines() if f.strip()
    )
    direct = changed_files.intersection(edges.keys())
    ripple = ripple_bfs(edges, direct, max_depth=max_depth)

    data = {
        "report_version": "0.2.0",
        "diff": {"base": base, "head": head},
        "direct_units": _direct_units_with_symbols(direct, symbols_by_file),
        "ripple_units": [{"id": p, "kind": "file", "path": p} for p in sorted(ripple)],
        "clusters_touched": [],
        "domains_touched": [],
        "risk": "low" if len(ripple) < 50 else "medium",
        "gaps": [
            "v0.2 uses multi-language import graph (Python AST + JS/TS regex); package imports still partial.",
        ],
        "evidence_uri": "",
        "meta": {
            "source_root": source_root,
            "snapshot": snapshot_path.as_posix(),
            "max_depth": max_depth,
            "changed_files_total": len(changed_files),
            "direct_files_in_graph": len(direct),
            "ripple_files_in_graph": len(ripple),
            "symbols_touched_files": sum(1 for p in direct if p in symbols_by_file),
        },
    }

    run_dir = REPO_ROOT / "verification/semgraph/runs"
    run_dir.mkdir(parents=True, exist_ok=True)
    run_id = _sha12(json.dumps({"base": base, "head": head, "data": data}, sort_keys=True))
    run_path = run_dir / f"ImpactReport-diff-{run_id}.json"
    data["evidence_uri"] = run_path.as_posix().replace(str(REPO_ROOT) + "/", "")

    envelope = {"schema": "ImpactReport", "data": data}
    run_path.write_text(json.dumps(envelope, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    (run_dir / f"ImpactReport-diff-{run_id}.data.json").write_text(
        json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    return run_path


def single_file_cmd(target_path: str, source_root: str, max_depth: int) -> Path:
    """Produce a schema-valid ImpactReport for a single target file.

    Used for Guardian auto-generation when a write tool arrives without evidence.
    """
    source_path = (REPO_ROOT / source_root).resolve()
    graph = build_multilang_graph(REPO_ROOT, source_path)
    edges = graph.edges
    symbols_by_file = graph.symbols_by_file

    normalized = target_path.lstrip("./")
    direct = {normalized} if normalized in edges else set()
    ripple = ripple_bfs(edges, direct, max_depth=max_depth) if direct else set()

    data = {
        "report_version": "0.2.0",
        "diff": {"base": "HEAD", "head": "WORKING"},
        "direct_units": _direct_units_with_symbols(direct or {normalized}, symbols_by_file),
        "ripple_units": [{"id": p, "kind": "file", "path": p} for p in sorted(ripple)],
        "clusters_touched": [],
        "domains_touched": [],
        "risk": "low" if len(ripple) < 50 else "medium",
        "gaps": [
            "auto-generated single-file ImpactReport (triggered by Guardian evidence auto-gen).",
        ],
        "evidence_uri": "",
        "meta": {
            "source_root": source_root,
            "single_file_target": normalized,
            "target_in_graph": normalized in edges,
            "direct_files_in_graph": len(direct),
            "ripple_files_in_graph": len(ripple),
            "auto_generated": True,
        },
    }

    run_dir = REPO_ROOT / "verification/semgraph/runs"
    run_dir.mkdir(parents=True, exist_ok=True)
    run_id = _sha12(json.dumps(data, sort_keys=True))
    run_path = run_dir / f"ImpactReport-auto-{run_id}.json"
    data["evidence_uri"] = run_path.as_posix().replace(str(REPO_ROOT) + "/", "")

    envelope = {"schema": "ImpactReport", "data": data}
    run_path.write_text(json.dumps(envelope, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    (run_dir / f"ImpactReport-auto-{run_id}.data.json").write_text(
        json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    return run_path


def main() -> int:
    parser = argparse.ArgumentParser(prog="tlc-semgraph")
    sub = parser.add_subparsers(dest="cmd", required=True)

    b = sub.add_parser("build")
    b.add_argument("--source-root", default="apps/tlc-control-plane")

    d = sub.add_parser("diff")
    d.add_argument("--base", required=True)
    d.add_argument("--head", required=True)
    d.add_argument("--source-root", default="apps/tlc-control-plane")
    d.add_argument("--max-depth", type=int, default=2)

    s = sub.add_parser("single-file")
    s.add_argument("--target", required=True, help="Repo-relative file path.")
    s.add_argument("--source-root", default="apps/tlc-control-plane")
    s.add_argument("--max-depth", type=int, default=2)

    args = parser.parse_args()

    if args.cmd == "build":
        out = build_cmd(args.source_root)
        print(out.as_posix())
        return 0

    if args.cmd == "diff":
        out = diff_cmd(args.base, args.head, args.source_root, args.max_depth)
        print(out.as_posix())
        return 0

    if args.cmd == "single-file":
        out = single_file_cmd(args.target, args.source_root, args.max_depth)
        print(out.as_posix())
        return 0

    raise RuntimeError("unreachable")


if __name__ == "__main__":
    raise SystemExit(main())
