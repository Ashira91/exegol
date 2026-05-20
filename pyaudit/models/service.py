from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional

@dataclass
class Service:
    name: str
    port: int
    version: Optional[str] = None
    cves: list[str] = field(default_factory=list)
    notes: Optional[str] = None

    def __str__(self) -> str:
        v = f" v{self.version}" if self.version else ""
        return f"{self.name}{v} (port {self.port})"
