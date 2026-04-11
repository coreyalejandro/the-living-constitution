from __future__ import annotations

import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT / "src") not in sys.path:
    sys.path.insert(0, str(REPO_ROOT / "src"))
if str(REPO_ROOT / "projects" / "sandbox-runtime") not in sys.path:
    sys.path.insert(0, str(REPO_ROOT / "projects" / "sandbox-runtime"))

import guardian  # noqa: E402
from src import jail as sandbox_jail  # type: ignore # noqa: E402


@pytest.fixture
def guardian_active(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    verification_dir = tmp_path / "verification"
    verification_dir.mkdir(parents=True, exist_ok=True)
    monkeypatch.setattr(guardian, "VERIFICATION_DIR", verification_dir)
    monkeypatch.setattr(guardian, "LOG_PATH", verification_dir / "guardian-log.json")
    guardian.bootstrap_trinity()
    guardian.load_invariants()
    guardian._state = guardian.GuardianState.ACTIVE  # noqa: SLF001


def test_guardian_blocks_planner_production_deploy(guardian_active: None) -> None:
    verdict = guardian.evaluate_invariants("planner", "deploy_production", {})
    assert verdict["decision"] == "FAIL"
    assert "INVARIANT_ARTICLE_IV_01" in verdict["violated_invariants"]


def test_guardian_blocks_constitution_write_without_signature(guardian_active: None) -> None:
    verdict = guardian.evaluate_invariants(
        "builder",
        "write_file",
        {"path": "THE_LIVING_CONSTITUTION.md", "toca_anchor": "T1.test.anchor"},
    )
    assert verdict["decision"] == "FAIL"
    assert "INVARIANT_READ_ONLY_01" in verdict["violated_invariants"]


def test_guardian_blocks_missing_toca_anchor_for_non_read_tool(guardian_active: None) -> None:
    verdict = guardian.evaluate_invariants("builder", "write_file", {"path": "src/feature.py"})
    assert verdict["decision"] == "FAIL"
    assert "INVARIANT_ARTICLE_III_01" in verdict["violated_invariants"]


def test_guardian_passes_valid_builder_write(guardian_active: None) -> None:
    verdict = guardian.evaluate_invariants(
        "builder",
        "write_file",
        {
            "path": "src/feature.py",
            "toca_anchor": "T1.builder.feature",
            "test_coverage": 90.0,
        },
    )
    assert verdict["decision"] == "PASS"


def test_jail_resolves_allowed_script_path() -> None:
    path = sandbox_jail.resolve_safe_script_path("src/__main__.py", REPO_ROOT)
    assert path.name == "__main__.py"
    assert path.is_file()


def test_jail_rejects_path_outside_allowed_roots() -> None:
    with pytest.raises(sandbox_jail.SandboxJailError):
        sandbox_jail.assert_path_readable_in_jail(REPO_ROOT / "README.md", REPO_ROOT)


def test_safe_exec_script_rejects_non_whitelisted_import() -> None:
    with pytest.raises(ImportError):
        sandbox_jail.safe_exec_script("import os\n", "blocked.py")


def test_safe_exec_script_allows_whitelisted_imports() -> None:
    globals_after = sandbox_jail.safe_exec_script("import math\nresult = math.sqrt(9)\n", "ok.py")
    assert globals_after["result"] == 3
