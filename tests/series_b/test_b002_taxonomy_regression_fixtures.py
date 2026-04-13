from __future__ import annotations

import json
import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]


def _load_json(rel: str) -> dict:
    return json.loads((REPO_ROOT / rel).read_text(encoding="utf-8"))


def test_invariant_registry_ids_are_unique_and_well_formed() -> None:
    registry = _load_json("00-constitution/invariant-registry.json")
    invariants = registry["invariants"]
    ids = [item["id"] for item in invariants]
    assert len(ids) == len(set(ids))
    assert all(re.fullmatch(r"INVARIANT_\d{2}", i) for i in ids)


def test_registry_breach_taxonomy_and_failure_modes_are_populated() -> None:
    registry = _load_json("00-constitution/invariant-registry.json")
    for invariant in registry["invariants"]:
        assert re.fullmatch(r"BREACH-[A-Z]", invariant["breach_taxonomy"])
        assert isinstance(invariant["failure_mode"], str)
        assert invariant["failure_mode"].strip() != ""


def test_doctrine_and_article_invariants_exist_in_registry() -> None:
    doctrine_map = _load_json("00-constitution/doctrine-to-invariant.map.json")
    registry = _load_json("00-constitution/invariant-registry.json")
    registry_ids = {item["id"] for item in registry["invariants"]}

    doctrine_ids = {
        iid
        for doctrine in doctrine_map["doctrines"]
        for iid in doctrine.get("invariant_ids", [])
    }
    article_ids = {
        iid
        for article in doctrine_map["articles"]
        for iid in article.get("invariant_ids", [])
    }

    assert doctrine_ids.issubset(registry_ids)
    assert article_ids.issubset(registry_ids)


def test_doctrine_failure_classes_are_defined_in_failure_taxonomy() -> None:
    doctrine_map = _load_json("00-constitution/doctrine-to-invariant.map.json")
    taxonomy_md = (REPO_ROOT / "projects/08-evaluation/failure_taxonomy.md").read_text(
        encoding="utf-8"
    )
    known_failure_classes = set(re.findall(r"^## (F\d+):", taxonomy_md, flags=re.MULTILINE))
    assert known_failure_classes, "expected F-class headings in failure taxonomy"

    mapped_failure_classes = {
        fid
        for group in ("doctrines", "articles")
        for item in doctrine_map[group]
        for fid in item.get("failure_class_ids", [])
    }
    assert mapped_failure_classes.issubset(known_failure_classes)


def test_enforcement_module_hooks_point_to_existing_paths() -> None:
    enforcement_map = _load_json("03-enforcement/enforcement-map.json")
    for module in enforcement_map["modules"]:
        hook = module.get("enforcement_hook")
        assert isinstance(hook, str) and hook.strip()
        assert (REPO_ROOT / hook).exists(), f"missing enforcement hook path: {hook}"


def test_risk_bindings_cover_all_registry_invariants() -> None:
    registry = _load_json("00-constitution/invariant-registry.json")
    enforcement_map = _load_json("03-enforcement/enforcement-map.json")
    registry_ids = {item["id"] for item in registry["invariants"]}
    risk_binding_ids = set(enforcement_map["invariant_risk_bindings"].keys())
    assert registry_ids.issubset(risk_binding_ids)


def test_invariant_39_binding_targets_governance_chain_verifier() -> None:
    enforcement_map = _load_json("03-enforcement/enforcement-map.json")
    hook = enforcement_map["invariant_risk_bindings"]["INVARIANT_39"]["verification_hook"]
    assert "verify_governance_chain.py" in hook
