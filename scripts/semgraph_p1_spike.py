from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
from typing import Iterable


REPO_ROOT = Path(__file__).resolve().parents[1]


def iter_files(root: Path) -> Iterable[Path]:
    for dirpath, dirnames, filenames in os.walk(root):
        # ignore common heavy dirs
        dirnames[:] = [
            d
            for d in dirnames
            if d
            not in {
                ".git",
                "node_modules",
                "__pycache__",
                ".next",
                "dist",
                "build",
                ".turbo",
            }
        ]
        for name in filenames:
            yield Path(dirpath) / name


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 128), b""):
            h.update(chunk)
    return h.hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--target",
        required=True,
        help="Directory to scan (relative to repo root or absolute).",
    )
    args = parser.parse_args()

    target = Path(args.target)
    if not target.is_absolute():
        target = (REPO_ROOT / target).resolve()

    if not target.exists() or not target.is_dir():
        raise FileNotFoundError(str(target))

    counts: dict[str, int] = {
        "files_total": 0,
        "files_ts": 0,
        "files_tsx": 0,
        "files_js": 0,
        "files_jsx": 0,
        "files_py": 0,
        "files_go": 0,
    }

    content_hashes: list[str] = []
    for p in iter_files(target):
        counts["files_total"] += 1
        suf = p.suffix.lower()
        if suf == ".ts":
            counts["files_ts"] += 1
        elif suf == ".tsx":
            counts["files_tsx"] += 1
        elif suf == ".js":
            counts["files_js"] += 1
        elif suf == ".jsx":
            counts["files_jsx"] += 1
        elif suf == ".py":
            counts["files_py"] += 1
        elif suf == ".go":
            counts["files_go"] += 1

        # Hash only source-like files (keeps run deterministic but bounded).
        if suf in {".ts", ".tsx", ".js", ".jsx", ".py", ".go", ".json", ".md"}:
            try:
                content_hashes.append(sha256_file(p))
            except OSError:
                # best-effort; failures counted only by omission
                pass

    aggregate = hashlib.sha256(("".join(sorted(content_hashes))).encode("utf-8")).hexdigest()
    short = aggregate[:12]

    out_dir = REPO_ROOT / "verification/semgraph/runs"
    out_dir.mkdir(parents=True, exist_ok=True)

    data = {
        "report_version": "0.1.0",
        "diff": {"base": "P1-spike", "head": "P1-spike"},
        "direct_units": [],
        "ripple_units": [],
        "clusters_touched": [],
        "domains_touched": [],
        "risk": "low",
        "gaps": [
            "P1 spike only: counts + content hash; no tree-sitter parsing yet.",
            "No units/edges extracted in this spike.",
        ],
        "evidence_uri": f"verification/semgraph/runs/P1-build-{short}.json",
        "meta": {
            "target_dir": str(target),
            "aggregate_sha256": aggregate,
            "counts": counts,
        },
    }

    run_envelope = {
        "schema": "ImpactReport",
        "data": data,
    }

    run_path = out_dir / f"P1-build-{short}.json"
    run_path.write_text(json.dumps(run_envelope, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    data_path = out_dir / f"P1-build-{short}.data.json"
    data_path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    print(str(run_path))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

