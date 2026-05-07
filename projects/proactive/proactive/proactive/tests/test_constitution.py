
from proactive.constitution import load_constitution


def test_load_constitution_returns_expected_shape() -> None:
    data = load_constitution()

    assert isinstance(data, dict)
    assert data["name"] == "PROACTIVE Constitution"
    assert isinstance(data["principles"], list)
    assert len(data["principles"]) > 0
    assert "[verified]" in data["required_tags"]
    assert "[inferred]" in data["required_tags"]
    assert "[unverified]" in data["required_tags"]
