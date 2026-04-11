from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT / "projects" / "sandbox-runtime") not in sys.path:
    sys.path.insert(0, str(REPO_ROOT / "projects" / "sandbox-runtime"))

from src import engine as sandbox_engine  # type: ignore # noqa: E402
from src import evidence_ledger  # type: ignore # noqa: E402


def _create_tlc_root(tmp_path: Path) -> Path:
    tlc_root = tmp_path / "tlc"
    (tlc_root / "verification").mkdir(parents=True, exist_ok=True)
    (tlc_root / "THE_LIVING_CONSTITUTION.md").write_text("# Constitution\n", encoding="utf-8")
    (tlc_root / "projects" / "sandbox-runtime" / "src").mkdir(parents=True, exist_ok=True)
    return tlc_root


def test_evidence_ledger_initialization_creates_sandbox_log(tmp_path: Path) -> None:
    tlc_root = _create_tlc_root(tmp_path)
    evidence_ledger.ensure_initialized(tlc_root)
    log_path = tlc_root / "verification" / "SANDBOX_LOG.md"
    assert log_path.is_file()
    content = log_path.read_text(encoding="utf-8")
    assert "Sandbox Evidence Ledger (Gold Star)" in content
    assert "Initialized ledger" in content


def test_evidence_ledger_append_includes_related_invariant(tmp_path: Path) -> None:
    tlc_root = _create_tlc_root(tmp_path)
    evidence_ledger.append_entry(
        tlc_root,
        action="Executed src/failing.py",
        result="Fail",
        related_invariant="INVARIANT_04",
    )
    content = (tlc_root / "verification" / "SANDBOX_LOG.md").read_text(encoding="utf-8")
    assert "Executed src/failing.py (INVARIANT_04)" in content
    assert "| Fail |" in content


def test_execute_script_success_writes_success_evidence(tmp_path: Path) -> None:
    tlc_root = _create_tlc_root(tmp_path)
    script = tlc_root / "projects" / "sandbox-runtime" / "src" / "ok.py"
    script.write_text("x = 1 + 1\n", encoding="utf-8")
    evidence_path = tlc_root / "tmp-evidence.jsonl"
    eng = sandbox_engine.SandboxEngine(evidence_path=evidence_path, tlc_root=tlc_root)
    assert eng.execute_script("src/ok.py") == "success"

    log_content = (tlc_root / "verification" / "SANDBOX_LOG.md").read_text(encoding="utf-8")
    assert "Executed src/ok.py" in log_content
    assert "| Success |" in log_content

    lines = evidence_path.read_text(encoding="utf-8").strip().splitlines()
    payloads = [json.loads(line)["payload"] for line in lines]
    assert any(p.get("event") == "script_executed" and p.get("result") == "success" for p in payloads)


def test_execute_script_failure_writes_fail_evidence(tmp_path: Path) -> None:
    tlc_root = _create_tlc_root(tmp_path)
    evidence_path = tlc_root / "tmp-evidence.jsonl"
    eng = sandbox_engine.SandboxEngine(evidence_path=evidence_path, tlc_root=tlc_root)

    with pytest.raises(Exception):
        eng.execute_script("../blocked.py")

    log_content = (tlc_root / "verification" / "SANDBOX_LOG.md").read_text(encoding="utf-8")
    assert "Executed ../blocked.py (INVARIANT_04)" in log_content
    assert "| Fail |" in log_content

    lines = evidence_path.read_text(encoding="utf-8").strip().splitlines()
    payloads = [json.loads(line)["payload"] for line in lines]
    assert any(p.get("event") == "script_executed" and p.get("result") == "fail" for p in payloads)


def test_run_execution_loop_returns_halted_on_in_process_halt(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    tlc_root = _create_tlc_root(tmp_path)
    evidence_path = tlc_root / "tmp-evidence.jsonl"
    eng = sandbox_engine.SandboxEngine(evidence_path=evidence_path, tlc_root=tlc_root)
    monkeypatch.setattr(eng, "enforce_resource_ceilings", lambda: None)

    def step(i: int) -> None:
        if i == 1:
            eng.halt()

    assert eng.run_execution_loop(step, max_iterations=5) == "halted"


def test_run_execution_loop_returns_completed_when_no_halt(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    tlc_root = _create_tlc_root(tmp_path)
    evidence_path = tlc_root / "tmp-evidence.jsonl"
    eng = sandbox_engine.SandboxEngine(evidence_path=evidence_path, tlc_root=tlc_root)
    monkeypatch.setattr(eng, "enforce_resource_ceilings", lambda: None)

    assert eng.run_execution_loop(lambda _i: None, max_iterations=3) == "completed"

    lines = evidence_path.read_text(encoding="utf-8").strip().splitlines()
    payloads = [json.loads(line)["payload"] for line in lines]
    assert any(p.get("event") == "max_iterations_reached" for p in payloads)


def test_run_execution_loop_halts_on_external_env_signal(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    tlc_root = _create_tlc_root(tmp_path)
    eng = sandbox_engine.SandboxEngine(evidence_path=tlc_root / "tmp-evidence.jsonl", tlc_root=tlc_root)
    monkeypatch.setattr(eng, "enforce_resource_ceilings", lambda: None)
    monkeypatch.setenv("TLC_HALT_AUTHORITY", "true")

    with pytest.raises(SystemExit) as err:
        eng.run_execution_loop(lambda _i: None, max_iterations=2)
    assert err.value.code == 0
