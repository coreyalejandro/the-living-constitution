from __future__ import annotations

import ast
from dataclasses import dataclass, field
from pathlib import Path


@dataclass(frozen=True)
class PythonFileAnalysis:
    path: str
    imports: tuple[str, ...] = ()
    symbols: tuple[str, ...] = ()


@dataclass
class PythonImportSpec:
    module: str
    level: int = 0


def _collect_imports(tree: ast.AST) -> list[PythonImportSpec]:
    out: list[PythonImportSpec] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                out.append(PythonImportSpec(module=alias.name, level=0))
        elif isinstance(node, ast.ImportFrom):
            module = node.module or ""
            out.append(PythonImportSpec(module=module, level=node.level or 0))
    return out


def _collect_symbols(tree: ast.AST) -> list[str]:
    symbols: list[str] = []
    for node in ast.iter_child_nodes(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            symbols.append(f"function:{node.name}")
        elif isinstance(node, ast.ClassDef):
            symbols.append(f"class:{node.name}")
            for child in ast.iter_child_nodes(node):
                if isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    symbols.append(f"method:{node.name}.{child.name}")
    return symbols


def analyze_python_file(path: Path) -> PythonFileAnalysis:
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return PythonFileAnalysis(path=path.as_posix())

    try:
        tree = ast.parse(text, filename=path.as_posix())
    except SyntaxError:
        return PythonFileAnalysis(path=path.as_posix())

    imports = _collect_imports(tree)
    symbols = _collect_symbols(tree)

    return PythonFileAnalysis(
        path=path.as_posix(),
        imports=tuple(sorted({f"{i.level}:{i.module}" for i in imports})),
        symbols=tuple(symbols),
    )


def resolve_python_import(
    from_file: Path,
    spec: PythonImportSpec,
    source_root: Path,
) -> Path | None:
    """Attempt to resolve a Python import to a repo file path.

    Only handles:
      - relative imports (level >= 1) anchored at `from_file.parent`
      - absolute imports rooted at `source_root`

    Returns the resolved Path if a .py file or package __init__.py exists, else None.
    """
    if not spec.module and spec.level == 0:
        return None

    parts = spec.module.split(".") if spec.module else []

    if spec.level > 0:
        anchor = from_file.parent
        for _ in range(spec.level - 1):
            anchor = anchor.parent
        base = anchor.joinpath(*parts) if parts else anchor
    else:
        base = source_root.joinpath(*parts)

    candidates = [
        Path(str(base) + ".py"),
        base / "__init__.py",
    ]
    for cand in candidates:
        if cand.exists() and cand.is_file():
            return cand
    return None


@dataclass
class PythonGraphResult:
    edges: dict[str, set[str]] = field(default_factory=dict)
    symbols_by_file: dict[str, list[str]] = field(default_factory=dict)
