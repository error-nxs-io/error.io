import json
from pathlib import Path
from typing import Any, Dict


def ensure_file(path: Path, default: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not path.exists():
        path.write_text(json.dumps(default, indent=2))


def load_json(path: Path, default: Dict[str, Any]) -> Dict[str, Any]:
    ensure_file(path, default)
    try:
        return json.loads(path.read_text())
    except json.JSONDecodeError:
        path.write_text(json.dumps(default, indent=2))
        return dict(default)


def save_json(path: Path, payload: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2))
