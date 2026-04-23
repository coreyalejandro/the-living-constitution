from __future__ import annotations

import os
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


IMPORT_RE = re.compile(
    r"""(?mx)
    ^\s*import
    (?:[\s\w\{\}\*\$,]*\s+from\s+)?   # import ... from
    ["'](?P<spec>[^"']+)["']\s*;?\s*$
    """
)


@dataclass(frozen=True)
class ImportGraph:
    root: Path
    # adjacency: file (repo-relative) -> set(imported file repo-relative)
    edges: dict[str, set[str]]


def _iter_source_files(root: Path) -> Iterable[Path]:
    for dirpath, dirnames, filenames in os.walk(root):
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
            p = Path(dirpath) / name
            if p.suffix.lower() in {".ts", ".tsx", ".js", ".jsx"}:
                yield p


def _candidate_resolutions(from_file: Path, spec: str) -> list[Path]:
    if not spec.startswith("."):
        return []
    base = (from_file.parent / spec).resolve()
    candidates: list[Path] = []
    for suffix in (".ts", ".tsx", ".js", ".jsx"):
        candidates.append(Path(str(base) + suffix))
    for index_name in ("index.ts", "index.tsx", "index.js", "index.jsx"):
        candidates.append(base / index_name)
    candidates.append(base)
    return candidates


def build_import_graph(repo_root: Path, source_root: Path) -> ImportGraph:
    repo_root = repo_root.resolve()
    source_root = source_root.resolve()
    if not source_root.exists() or not source_root.is_dir():
        raise FileNotFoundError(str(source_root))

    edges: dict[str, set[str]] = {}
    for file_path in _iter_source_files(source_root):
        rel = file_path.resolve().relative_to(repo_root).as_posix()
        edges.setdefault(rel, set())
        try:
            text = file_path.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue

        for m in IMPORT_RE.finditer(text):
            spec = m.group("spec")
            for cand in _candidate_resolutions(file_path, spec):
                if cand.exists() and cand.is_file():
                    try:
                        imported_rel = cand.resolve().relative_to(repo_root).as_posix()
                    except ValueError:
                        continue
                    edges[rel].add(imported_rel)
                    break

    return ImportGraph(root=source_root, edges=edges)

