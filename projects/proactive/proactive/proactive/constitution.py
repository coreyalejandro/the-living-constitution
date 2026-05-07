from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def get_constitution_path() -> Path:
    return Path(__file__).with_name("constitution.json")


def load_constitution() -> dict[str, Any]:
    path = get_constitution_path()

    if not path.exists():
        raise FileNotFoundError(f"Constitution file not found: {path}")

    with path.open("r", encoding="utf-8") as file:
        data = json.load(file)

    if not isinstance(data, dict):
        raise ValueError("Constitution must deserialize to a dictionary.")

    required_top_level_keys = {"name", "version", "principles", "required_tags"}
    missing = required_top_level_keys - set(data.keys())
    if missing:
        raise ValueError(
            f"Constitution missing required keys: {sorted(missing)}"
        )

    if not isinstance(data["principles"], list):
        raise ValueError("'principles' must be a list.")

    if not isinstance(data["required_tags"], list):
        raise ValueError("'required_tags' must be a list.")

    return data
