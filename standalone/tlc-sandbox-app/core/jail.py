#!/usr/bin/env python3
"""
INVARIANT_04 — Lower Sandbox namespace jail.

Simulated directory boundary (no reliance on OS chroot; portable macOS/Linux).
Path traversal is rejected; user code runs with a whitelisted import surface.
"""

from __future__ import annotations

import builtins
import importlib
import math
import os
import time
from pathlib import Path
from types import ModuleType
from typing import Any, Dict, FrozenSet, Optional, Tuple

# Allowed repo-relative roots under the TLC repository root (INVARIANT_04).
_ALLOWED_ROOT_SEGMENTS: Tuple[Tuple[str, ...], ...] = (
    ("projects", "sandbox-runtime"),
    ("standalone", "tlc-sandbox-app"),
)

# Execution cell may only import these top-level modules (plus whitelisted stdlib used by jail).
_IMPORT_WHITELIST: FrozenSet[str] = frozenset({"math", "json", "time"})


class SandboxJailError(ValueError):
    """Raised when a path or import violates the Lower Sandbox boundary."""


def _reject_traversal(rel: str) -> None:
    p = Path(rel)
    if p.is_absolute():
        raise SandboxJailError("absolute paths are not allowed in the Lower Sandbox")
    for part in p.parts:
        if part == "..":
            raise SandboxJailError("path traversal is forbidden in the Lower Sandbox")


def _allowed_root_paths(tlc_root: Path) -> Tuple[Path, ...]:
    return tuple((tlc_root.joinpath(*segments)).resolve() for segments in _ALLOWED_ROOT_SEGMENTS)


def _is_under(root: Path, candidate: Path) -> bool:
    try:
        candidate.relative_to(root)
        return True
    except ValueError:
        return False


def resolve_safe_script_path(relative: str, tlc_root: Path) -> Path:
    """
    Resolve a script path that must live under projects/sandbox-runtime/ or
    standalone/tlc-sandbox-app/ relative to tlc_root.
    """
    _reject_traversal(relative)
    rel = Path(relative)
    roots = _allowed_root_paths(tlc_root)
    for base in roots:
        candidate = (base / rel).resolve()
        if not _is_under(base, candidate):
            continue
        if candidate.is_file():
            return candidate
    raise SandboxJailError(
        f"script not found in Lower Sandbox allowed roots: {relative!r}"
    )


def assert_path_readable_in_jail(path: Path, tlc_root: Path) -> Path:
    """Verify a concrete path is inside an allowed root (after resolve)."""
    resolved = path.resolve()
    roots = _allowed_root_paths(tlc_root)
    for base in roots:
        if _is_under(base, resolved):
            return resolved
    raise SandboxJailError(f"path escapes Lower Sandbox: {path}")


def _restricted_import(
    name: str,
    globals: Optional[Dict[str, Any]] = None,
    locals: Optional[Dict[str, Any]] = None,
    fromlist: Tuple[str, ...] = (),
    level: int = 0,
) -> ModuleType:
    if level != 0:
        raise ImportError("relative imports are not allowed in the Lower Sandbox")
    base = name.split(".", 1)[0]
    if base not in _IMPORT_WHITELIST:
        raise ImportError(
            f"import of {name!r} is not permitted (whitelist: {sorted(_IMPORT_WHITELIST)})"
        )
    return importlib.import_module(name)


def _safe_builtins() -> Dict[str, Any]:
    """Minimal builtins for sandboxed user code (no open, exec, __import__)."""
    names = (
        "None",
        "False",
        "True",
        "abs",
        "bool",
        "bytes",
        "chr",
        "dict",
        "enumerate",
        "filter",
        "float",
        "format",
        "frozenset",
        "hash",
        "hex",
        "int",
        "isinstance",
        "issubclass",
        "iter",
        "len",
        "list",
        "map",
        "max",
        "min",
        "next",
        "object",
        "ord",
        "pow",
        "range",
        "repr",
        "reversed",
        "round",
        "set",
        "slice",
        "sorted",
        "str",
        "sum",
        "tuple",
        "zip",
        "print",
        "Exception",
        "ValueError",
        "TypeError",
        "RuntimeError",
        "StopIteration",
    )
    out: Dict[str, Any] = {}
    for n in names:
        out[n] = getattr(builtins, n)
    out["__import__"] = _restricted_import
    return out


def safe_exec_script(
    source: str,
    filename: str,
    extra_globals: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """
    Execute Python source with restricted builtins and whitelisted imports only.
    Returns the execution globals after running (for tests / callers).
    """
    g: Dict[str, Any] = {"__name__": "__sandbox__", "__doc__": None}
    g["__builtins__"] = _safe_builtins()
    # Inject whitelisted modules explicitly so typical `import math` works via __import__
    # and direct references remain ergonomic.
    g["math"] = math
    g["json"] = importlib.import_module("json")
    g["time"] = time
    if extra_globals:
        g.update(extra_globals)
    code = compile(source, filename, "exec", dont_inherit=True)
    exec(code, g, g)
    return g


def try_chroot_lower_sandbox(_path: Path) -> None:
    """
    Optional OS chroot (Linux-only, requires privileges). Not used by default;
    INVARIANT_04 is enforced via path resolution checks above.
    """
    if not hasattr(os, "chroot"):
        return
    # Intentionally no-op: real chroot needs root and breaks dev workflows.
