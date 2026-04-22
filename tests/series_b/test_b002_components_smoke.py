from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT / "src") not in sys.path:
    sys.path.insert(0, str(REPO_ROOT / "src"))
if str(REPO_ROOT / "projects" / "sandbox-runtime") not in sys.path:
    sys.path.insert(0, str(REPO_ROOT / "projects" / "sandbox-runtime"))

import guardian  # noqa: E402
from src import engine as sandbox_engine  # type: ignore # noqa: E402
from src import evidence_ledger as sandbox_evidence  # type: ignore # noqa: E402
from src import jail as sandbox_jail  # type: ignore # noqa: E402


def test_guardian_invariant_registry_contains_article_iv_rule() -> None:
    ids = {item["id"] for item in guardian.CONSTITUTIONAL_INVARIANTS}
    assert "INVARIANT_ARTICLE_IV_01" in ids
    assert len(ids) >= 11


def test_sandbox_engine_detects_external_halt_env(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("TLC_HALT_AUTHORITY", "1")
    eng = sandbox_engine.SandboxEngine()
    assert eng._external_halt_signal() is True  # noqa: SLF001


def test_jail_blocks_parent_traversal_paths() -> None:
    with pytest.raises(sandbox_jail.SandboxJailError):
        sandbox_jail.resolve_safe_script_path("../secrets.txt", REPO_ROOT)


def test_evidence_ledger_constitution_hash_matches_file_digest() -> None:
    constitution_path = REPO_ROOT / "THE_LIVING_CONSTITUTION.md"
    expected = sandbox_evidence.sha256_file(constitution_path)
    actual = sandbox_evidence.constitutional_hash(REPO_ROOT)
    assert actual == expected


def test_taxonomy_registry_has_invariants_and_expected_shape() -> None:
    registry_path = (
        REPO_ROOT
        / "governance"
        / "constitution"
        / "core"
        / "invariant-registry.json"
    )
    payload = json.loads(registry_path.read_text(encoding="utf-8"))
    assert payload["schema_version"] == "1.0.0"
    invariants = payload.get("invariants")
    assert isinstance(invariants, list)
    assert len(invariants) >= 10
    first = invariants[0]
    assert {"id", "breach_taxonomy", "enforcement_hook"}.issubset(first.keys())
