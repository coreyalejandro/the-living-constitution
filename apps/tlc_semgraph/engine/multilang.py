from __future__ import annotations

import os
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable

from apps.tlc_semgraph.engine.python_ast import (
    PythonImportSpec,
    analyze_python_file,
    resolve_python_import,
)


JS_IMPORT_RE = re.compile(
    r"""(?mx)
    ^\s*import
    (?:[\s\w\{\}\*\$,]*\s+from\s+)?
    ["'](?P<spec>[^"']+)["']\s*;?\s*$
    """
)
JS_REQUIRE_RE = re.compile(
    r"""(?mx)
    require\(\s*["'](?P<spec>[^"']+)["']\s*\)
    """
)

JS_EXTS = (".ts", ".tsx", ".js", ".jsx", ".mjs", ".cjs")
PY_EXTS = (".py",)
ALL_EXTS = JS_EXTS + PY_EXTS

SKIP_DIRS = {
    ".git",
    "node_modules",
    "__pycache__",
    ".next",
    "dist",
    "build",
    ".turbo",
    ".venv",
    "venv",
    ".mypy_cache",
    ".pytest_cache",
}


@dataclass(frozen=True)
class MultiLangGraph:
    root: Path
    edges: dict[str, set[str]]
    symbols_by_file: dict[str, list[str]] = field(default_factory=dict)


def _iter_source_files(root: Path) -> Iterable[Path]:
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for name in filenames:
            p = Path(dirpath) / name
            if p.suffix.lower() in ALL_EXTS:
                yield p


def _js_candidate_resolutions(from_file: Path, spec: str) -> list[Path]:
    if not spec.startswith("."):
        return []
    base = (from_file.parent / spec).resolve()
    candidates: list[Path] = []
    for suffix in JS_EXTS:
        candidates.append(Path(str(base) + suffix))
    for index_name in (
        "index.ts",
        "index.tsx",
        "index.js",
        "index.jsx",
        "index.mjs",
        "index.cjs",
    ):
        candidates.append(base / index_name)
    candidates.append(base)
    return candidates


def _parse_js_ts(file_path: Path, repo_root: Path) -> set[str]:
    try:
        text = file_path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return set()
    out: set[str] = set()
    for regex in (JS_IMPORT_RE, JS_REQUIRE_RE):
        for m in regex.finditer(text):
            spec = m.group("spec")
            for cand in _js_candidate_resolutions(file_path, spec):
                if cand.exists() and cand.is_file():
                    try:
                        out.add(cand.resolve().relative_to(repo_root).as_posix())
                    except ValueError:
                        pass
                    break
    return out


def _parse_python(
    file_path: Path, repo_root: Path, source_root: Path
) -> tuple[set[str], list[str]]:
    analysis = analyze_python_file(file_path)
    edges: set[str] = set()
    for raw in analysis.imports:
        level_str, module = raw.split(":", 1)
        spec = PythonImportSpec(module=module, level=int(level_str))
        resolved = resolve_python_import(file_path, spec, source_root)
        if resolved is None:
            continue
        try:
            edges.add(resolved.resolve().relative_to(repo_root).as_posix())
        except ValueError:
            continue
    return edges, list(analysis.symbols)


def build_multilang_graph(repo_root: Path, source_root: Path) -> MultiLangGraph:
    repo_root = repo_root.resolve()
    source_root = source_root.resolve()
    if not source_root.exists() or not source_root.is_dir():
        raise FileNotFoundError(str(source_root))

    edges: dict[str, set[str]] = {}
    symbols_by_file: dict[str, list[str]] = {}

    for file_path in _iter_source_files(source_root):
        rel = file_path.resolve().relative_to(repo_root).as_posix()
        edges.setdefault(rel, set())
        ext = file_path.suffix.lower()
        if ext in PY_EXTS:
            py_edges, symbols = _parse_python(file_path, repo_root, source_root)
            edges[rel].update(py_edges)
            if symbols:
                symbols_by_file[rel] = symbols
        elif ext in JS_EXTS:
            edges[rel].update(_parse_js_ts(file_path, repo_root))

    return MultiLangGraph(
        root=source_root,
        edges=edges,
        symbols_by_file=symbols_by_file,
    )
