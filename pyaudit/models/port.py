from __future__ import annotations
from dataclasses import dataclass
from enum import Enum
from typing import Optional

class PortStatus(Enum):
    OPEN = "open"
    CLOSED = "closed"
    FILTERED = "filtered"
    UNKNOWN = "unknown"

@dataclass
class Port:
    number: int
    protocol: str = "tcp"
    status: PortStatus = PortStatus.UNKNOWN
    banner: Optional[str] = None
    service_hint: Optional[str] = None

    def __str__(self) -> str:
        return f"{self.number}/{self.protocol} [{self.status.value}]"
