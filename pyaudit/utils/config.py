from __future__ import annotations
import copy
from pathlib import Path
from typing import Any
import yaml

_DEFAULT_CONFIG = Path(__file__).parent.parent.parent / "config" / "default.yaml"

def _deep_merge(base: dict[str, Any], override: dict[str, Any]) -> dict[str, Any]:
    result = copy.deepcopy(base)
    for key, value in override.items():
        if key in result and isinstance(result[key], dict) and isinstance(value, dict):
            result[key] = _deep_merge(result[key], value)
        else:
            result[key] = value
    return result

def load_config(user_config_path: Path | None = None) -> dict[str, Any]:
    with _DEFAULT_CONFIG.open("r", encoding="utf-8") as f:
        config: dict[str, Any] = yaml.safe_load(f) or {}
    if user_config_path is not None:
        if not user_config_path.exists():
            raise FileNotFoundError(f"Fichier de configuration introuvable : {user_config_path}")
        with user_config_path.open("r", encoding="utf-8") as f:
            user_cfg: dict[str, Any] = yaml.safe_load(f) or {}
        config = _deep_merge(config, user_cfg)
    return config
