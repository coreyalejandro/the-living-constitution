#!/usr/bin/env python3
"""
SANDBOX-BREACH-SIM — master driver for breach A/B and halt circuit (project sandbox-runtime-001).

Exit 0 only if all interdictions succeed and SANDBOX_LOG.md records expected FAIL rows.
"""

from __future__ import annotations

import os
import re
import subprocess
import sys
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
        from src import evidence_ledger  # type: ignore
    else:
        from core.engine import SandboxEngine  # type: ignore
        from core import evidence_ledger  # type: ignore
    return SandboxEngine, evidence_ledger


def _count_fail_rows(text: str) -> int:
    return len(re.findall(r"\|\s*Fail\s*\|", text))


def _write_report(path: Path, body: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(body, encoding="utf-8")


def main() -> int:
    tlc_root = _discover_tlc_root()
    os.environ["TLC_REPO_ROOT"] = str(tlc_root)

    report_path = tlc_root / "verification" / "STRESS_TEST_REPORT.md"
    _write_report(
        report_path,
        "# Stress Test Report (SANDBOX-BREACH-SIM)\n\n**Status:** running…\n",
    )

    SandboxEngine, evidence_ledger = _import_engine(tlc_root)
    log_path = tlc_root / "verification" / "SANDBOX_LOG.md"
    ch = evidence_ledger.constitutional_hash(tlc_root)

    baseline = log_path.read_text(encoding="utf-8") if log_path.is_file() else ""
    fail_before = _count_fail_rows(baseline)

    results: list[tuple[str, bool, str]] = []
    eng = SandboxEngine(
        tlc_root=tlc_root,
        evidence_path=tlc_root / "verification" / ".stress_suite_evidence.jsonl",
    )

    # Breach A — import bypass
    try:
        eng.execute_script("samples/breach_import.py")
        results.append(("breach_import blocked (ImportError)", False, "execute_script returned success"))
    except ImportError as e:
        results.append(("breach_import blocked (ImportError)", True, str(e)))
    except Exception as e:
        results.append(("breach_import blocked (ImportError)", False, repr(e)))

    # Breach B — path escape to constitution (driver path)
    try:
        eng.execute_script("../../../THE_LIVING_CONSTITUTION.md")
        results.append(("breach_path constitution traversal blocked", False, "no exception"))
    except ValueError as e:
        results.append(("breach_path constitution traversal blocked", True, str(e)))
    except Exception as e:
        results.append(("breach_path constitution traversal blocked", isinstance(e, ValueError), repr(e)))

    # Third FAIL row — legacy evil_import sample (same class as breach A; ledger row / hash proof)
    try:
        eng.execute_script("samples/evil_import.py")
        results.append(("evil_import blocked (ImportError)", False, "execute_script returned success"))
    except ImportError as e:
        results.append(("evil_import blocked (ImportError)", True, str(e)))
    except Exception as e:
        results.append(("evil_import blocked (ImportError)", False, repr(e)))

    after_breaches = log_path.read_text(encoding="utf-8") if log_path.is_file() else ""
    fail_after_breaches = _count_fail_rows(after_breaches)
    new_fails = fail_after_breaches - fail_before

    # Halt circuit (subprocess — must print HALT_BY_CONSTITUTIONAL_AUTHORITY)
    halt_script = tlc_root / "scripts" / "test_halt_circuit.py"
    halt_proc = subprocess.run(
        [sys.executable, str(halt_script)],
        cwd=str(tlc_root),
        env={**os.environ, "TLC_REPO_ROOT": str(tlc_root)},
        capture_output=True,
        text=True,
        timeout=120,
    )
    halt_ok = halt_proc.returncode == 0 and "HALT_BY_CONSTITUTIONAL_AUTHORITY" in (halt_proc.stderr or "")

    # Ledger checks: three new FAIL rows, invariants, hash
    text = log_path.read_text(encoding="utf-8") if log_path.is_file() else ""
    inv04 = "| INVARIANT_04 |" in text or "INVARIANT_04" in text
    inv05 = "INVARIANT_05" in text
    hash_ok = ch in text
    ledger_three = new_fails >= 3

    all_ok = (
        all(ok for _, ok, _ in results)
        and halt_ok
        and ledger_three
        and inv04
        and inv05
        and hash_ok
    )

    lines = [
        "# Stress Test Report (SANDBOX-BREACH-SIM)",
        "",
        f"- **TLC root:** `{tlc_root}`",
        f"- **Constitutional SHA-256:** `{ch}`",
        f"- **New FAIL rows (since driver start):** {new_fails} (require >= 3)",
        f"- **HALT circuit:** {'PASS' if halt_ok else 'FAIL'} (exit {halt_proc.returncode})",
        "",
        "## Breach scripts",
        "",
    ]
    for name, ok, detail in results:
        lines.append(f"- **{name}:** {'PASS' if ok else 'FAIL'} — {detail}")
    lines.extend(
        [
            "",
            "## Halt subprocess",
            "",
            "```",
            (halt_proc.stderr or "").strip(),
            "```",
            "",
            "## Ledger checks",
            "",
            f"- Three new FAIL rows: {'yes' if ledger_three else 'no'}",
            f"- INVARIANT_04 present: {'yes' if inv04 else 'no'}",
            f"- INVARIANT_05 present: {'yes' if inv05 else 'no'}",
            f"- Constitutional hash in log: {'yes' if hash_ok else 'no'}",
            "",
            f"**Overall:** {'PASS' if all_ok else 'FAIL'}",
            "",
        ]
    )
    _write_report(report_path, "\n".join(lines) + "\n")

    if not all_ok:
        print("\n".join(lines), file=sys.stderr)
        return 1
    print("STRESS_TEST_REPORT.md written:", report_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
