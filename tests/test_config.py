from __future__ import annotations
from pathlib import Path
import pytest
from pyaudit.utils.config import load_config

class TestConfig:
    def test_default_loads(self) -> None:
        c = load_config()
        assert "general" in c and "recon" in c
    def test_user_override(self, tmp_path: Path) -> None:
        f = tmp_path / "cfg.yaml"
        f.write_text("general:\n  log_level: DEBUG\n")
        c = load_config(f)
        assert c["general"]["log_level"] == "DEBUG"
    def test_missing_file_raises(self, tmp_path: Path) -> None:
        with pytest.raises(FileNotFoundError):
            load_config(tmp_path / "nope.yaml")
