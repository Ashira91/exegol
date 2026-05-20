from __future__ import annotations
import socket
from dataclasses import dataclass, field
from typing import Optional

@dataclass
class Target:
    """Représente une cible réseau (domaine ou IP)."""
    host: str
    ip: Optional[str] = None
    ports: list = field(default_factory=list)
    services: list = field(default_factory=list)
    metadata: dict = field(default_factory=dict)

    def __post_init__(self) -> None:
        if self.ip is None:
            self.ip = self._resolve()

    def _resolve(self) -> Optional[str]:
        try:
            return socket.gethostbyname(self.host)
        except socket.gaierror:
            return None

    @property
    def is_reachable(self) -> bool:
        return self.ip is not None

    def __str__(self) -> str:
        ip_str = self.ip if self.ip else "non résolu"
        return f"Target({self.host} -> {ip_str})"
