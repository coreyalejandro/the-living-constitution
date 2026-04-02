#!/usr/bin/env python3
"""
Breach sim C: external halt authority via TLC_HALT_SENTINEL_FILE (no /tmp sentinel).

Creates the sentinel under verification/ after 2s while the engine runs a long loop.
Expects HALT_BY_CONSTITUTIONAL_AUTHORITY on stderr and process exit 0.
"""

from __future__ import annotations

import os
import sys
import threading
import time
from pathlib import Path


def _discover_tlc_root() -> Path:
    env = os.environ.get("TLC_REPO_ROOT")
    if env:
        return Path(env).resolve()
    here = Path(__file__).resolve().parent
    for base in (here, *here.parents):
        if (base / "THE_LIVING_CONSTITUTION.md").is_file():
            return base
    return here.parent


def _sandbox_pkg(tlc_root: Path) -> Path:
    integrated = tlc_root / "projects" / "sandbox-runtime"
    if (integrated / "src" / "engine.py").is_file():
        return integrated
    standalone = tlc_root / "standalone" / "tlc-sandbox-app"
    if (standalone / "core" / "engine.py").is_file():
        return standalone
    raise RuntimeError("sandbox-runtime package not found under TLC root")


def _import_engine(tlc_root: Path):
    pkg = _sandbox_pkg(tlc_root)
    sys.path.insert(0, str(pkg))
    if (pkg / "src" / "engine.py").is_file():
        from src.engine import SandboxEngine  # type: ignore
    else:
        from core.engine import SandboxEngine  # type: ignore
    return SandboxEngine


def main() -> int:
    tlc_root = _discover_tlc_root()
    os.environ["TLC_REPO_ROOT"] = str(tlc_root)

    sentinel = tlc_root / "verification" / ".stress_halt_sentinel"
    try:
        sentinel.unlink()
    except OSError:
        pass

    os.environ["TLC_HALT_SENTINEL_FILE"] = str(sentinel)

    SandboxEngine = _import_engine(tlc_root)
    evidence = tlc_root / "verification" / ".stress_halt_evidence.jsonl"
    eng = SandboxEngine(tlc_root=tlc_root, evidence_path=evidence)

    def touch_sentinel() -> None:
        time.sleep(2.0)
        sentinel.parent.mkdir(parents=True, exist_ok=True)
        sentinel.write_text("halt\n", encoding="utf-8")

    threading.Thread(target=touch_sentinel, daemon=True).start()

    def step(_i: int) -> None:
        time.sleep(0.05)

    # External halt prints HALT_LOG_MESSAGE and exits 0 (never returns).
    eng.run_execution_loop(step, max_iterations=1_000_000)
    print("expected halt exit, loop returned", file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
