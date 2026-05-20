from __future__ import annotations
import json
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Optional

@dataclass
class Report:
    command: str
    target: Optional[str] = None
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    sections: dict[str, Any] = field(default_factory=dict)

    def add_section(self, title: str, data: Any) -> None:
        self.sections[title] = data

    def to_text(self) -> str:
        lines: list[str] = [
            "=" * 60,
            "  PYAUDIT — Rapport d'audit",
            f"  Commande  : {self.command}",
            f"  Cible     : {self.target or 'N/A'}",
            f"  Date (UTC): {self.created_at.strftime('%Y-%m-%d %H:%M:%S')}",
            "=" * 60, "",
        ]
        for title, data in self.sections.items():
            lines.append(f"[{title.upper()}]")
            if isinstance(data, list):
                for item in data:
                    lines.append(f"  • {item}")
            elif isinstance(data, dict):
                for k, v in data.items():
                    lines.append(f"  {k}: {v}")
            else:
                lines.append(f"  {data}")
            lines.append("")
        return "\n".join(lines)

    def to_json(self) -> str:
        payload = {
            "command": self.command,
            "target": self.target,
            "created_at": self.created_at.isoformat(),
            "sections": self.sections,
        }
        return json.dumps(payload, indent=2, default=str)

    def save(self, output_dir: Path, fmt: str = "txt") -> Path:
        output_dir.mkdir(parents=True, exist_ok=True)
        timestamp = self.created_at.strftime("%Y%m%d_%H%M%S")
        cmd_slug = self.command.replace(" ", "_")
        filename = f"{timestamp}_{cmd_slug}.{fmt}"
        filepath = output_dir / filename
        content = self.to_json() if fmt == "json" else self.to_text()
        filepath.write_text(content, encoding="utf-8")
        return filepath
