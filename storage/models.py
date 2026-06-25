from dataclasses import dataclass
from typing import Optional


@dataclass
class Entry:
    value: str
    expiry: Optional[int] = None
    node: Optional["Node"] = None