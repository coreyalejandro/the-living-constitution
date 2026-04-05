#!/usr/bin/env python3
"""
Filesystem sensor: watches paths that affect verify_document_constitution.py and re-runs
the verifier after a debounce window. Run during editing sessions (separate terminal).

  pip install -r requirements-dev.txt
  python3 scripts/doc_root_sensor.py --root .

This is event-driven (create/modify/move), not polling and not tied to IDE turns.
"""

from __future__ import annotations

import argparse
import subprocess
import sys
import threading
from pathlib import Path

try:
    from watchdog.events import FileSystemEventHandler
    from watchdog.observers import Observer
except ImportError as exc:  # pragma: no cover
    print(
        "doc_root_sensor: install watchdog: pip install -r requirements-dev.txt",
        file=sys.stderr,
    )
    raise SystemExit(2) from exc

IGNORE_SUFFIXES = frozenset({".swp", ".tmp", "~"})
IGNORE_NAMES = frozenset({".DS_Store"})


def _should_consider(path: Path) -> bool:
    name = path.name
    if name in IGNORE_NAMES:
        return False
    if path.suffix.lower() in IGNORE_SUFFIXES:
        return False
    return True


def _is_doc_constitution_relevant(root: Path, path: Path) -> bool:
    """True if this file path can affect documentation constitution checks."""
    try:
        rel = path.resolve().relative_to(root.resolve())
    except ValueError:
        return False
    parts = rel.parts
    if not parts:
        return False
    first = parts[0]
    if first == "docs" or first == "governance":
        return path.suffix.lower() == ".md" and _should_consider(path)
    if first == "config" and rel.name == "docs_governance.json":
        return True
    if len(parts) == 1 and path.suffix.lower() == ".md":
        return _should_consider(path)
    if rel.as_posix() == "README.md":
        return _should_consider(path)
    return False


class _DebouncedVerify:
    def __init__(self, root: Path, debounce: float) -> None:
        self.root = root
        self.debounce = debounce
        self._timer: threading.Timer | None = None
        self._lock = threading.Lock()
        self.script = root / "scripts" / "verify_document_constitution.py"

    def schedule(self, trigger: str) -> None:
        with self._lock:
            if self._timer is not None:
                self._timer.cancel()
            self._timer = threading.Timer(self.debounce, self._run, args=(trigger,))
            self._timer.daemon = True
            self._timer.start()

    def _run(self, trigger: str) -> None:
        print(f"\n[doc_sensor] running verify (trigger: {trigger})\n", flush=True)
        proc = subprocess.run(
            [sys.executable, str(self.script), "--root", str(self.root)],
            cwd=str(self.root),
        )
        if proc.returncode == 0:
            print("[doc_sensor] DOCUMENT_CONSTITUTION_OK\n", flush=True)
        else:
            print(f"[doc_sensor] verify failed (exit {proc.returncode})\n", flush=True)


class _Handler(FileSystemEventHandler):
    def __init__(self, root: Path, debounced: _DebouncedVerify) -> None:
        super().__init__()
        self.root = root.resolve()
        self.debounced = debounced

    def _handle(self, path_str: str | None) -> None:
        if not path_str:
            return
        p = Path(path_str)
        if not _is_doc_constitution_relevant(self.root, p):
            return
        self.debounced.schedule(p.as_posix())

    def on_created(self, event):  # type: ignore[no-untyped-def]
        if event.is_directory:
            return
        self._handle(event.src_path)

    def on_modified(self, event):  # type: ignore[no-untyped-def]
        if event.is_directory:
            return
        self._handle(event.src_path)

    def on_moved(self, event):  # type: ignore[no-untyped-def]
        if event.is_directory:
            return
        dest = getattr(event, "dest_path", None)
        self._handle(dest if dest else event.src_path)


def main() -> None:
    ap = argparse.ArgumentParser(description="Watch docs-related paths and run doc constitution verifier.")
    ap.add_argument("--root", type=Path, default=Path("."), help="Repository root")
    ap.add_argument(
        "--debounce",
        type=float,
        default=1.5,
        help="Seconds to wait after last change before running verify (default: 1.5)",
    )
    args = ap.parse_args()
    root = args.root.resolve()
    script = root / "scripts" / "verify_document_constitution.py"
    if not script.is_file():
        print(f"Missing {script}", file=sys.stderr)
        raise SystemExit(1)

    debounced = _DebouncedVerify(root, args.debounce)
    handler = _Handler(root, debounced)
    observer = Observer()

    # Root: new/modified top-level *.md + README (root allowlist)
    observer.schedule(handler, str(root), recursive=False)
    for sub in ("docs", "governance"):
        p = root / sub
        if p.is_dir():
            observer.schedule(handler, str(p), recursive=True)
    cfg = root / "config"
    if cfg.is_dir():
        observer.schedule(handler, str(cfg), recursive=False)

    observer.start()
    print(
        "[doc_sensor] watching root .md, docs/, governance/, config/ "
        f"(debounce={args.debounce}s). Ctrl+C to stop.\n",
        flush=True,
    )
    try:
        while observer.is_alive():
            observer.join(1.0)
    except KeyboardInterrupt:
        print("\n[doc_sensor] stopped.", flush=True)
    finally:
        observer.stop()
        observer.join(timeout=5)


if __name__ == "__main__":
    main()
