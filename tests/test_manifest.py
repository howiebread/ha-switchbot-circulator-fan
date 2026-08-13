"""Basic project structure checks."""

import json
from pathlib import Path


def test_manifest_declares_expected_metadata() -> None:
    """The manifest contains the metadata required by Home Assistant and HACS."""
    manifest_path = (
        Path(__file__).parents[1]
        / "custom_components"
        / "switchbot_circulator_fan"
        / "manifest.json"
    )
    manifest = json.loads(manifest_path.read_text())

    assert manifest["domain"] == "switchbot_circulator_fan"
    assert manifest["config_flow"] is True
    assert manifest["requirements"] == ["PySwitchbot==2.2.0"]
