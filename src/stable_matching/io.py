from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def load_preferences(path: str | Path) -> tuple[dict[str, list[str]], dict[str, list[str]]]:
    """Load proposer/receiver preferences from a JSON file."""
    file_path = Path(path)
    with file_path.open("r", encoding="utf-8") as handle:
        data: Any = json.load(handle)

    if not isinstance(data, dict):
        raise ValueError("input file must contain a JSON object")

    proposers = _validate_side(data.get("proposers"), "proposers")
    receivers = _validate_side(data.get("receivers"), "receivers")
    return proposers, receivers


def _validate_side(value: Any, name: str) -> dict[str, list[str]]:
    if not isinstance(value, dict) or not value:
        raise ValueError(f"'{name}' must be a non-empty JSON object")

    parsed: dict[str, list[str]] = {}
    for participant, ranking in value.items():
        if not isinstance(participant, str) or not participant:
            raise ValueError(f"all {name} names must be non-empty strings")
        if not isinstance(ranking, list) or not all(isinstance(item, str) for item in ranking):
            raise ValueError(f"preference list for {participant} must be a JSON array of strings")
        parsed[participant] = ranking

    return parsed
