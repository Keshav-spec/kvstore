from dataclasses import dataclass
from typing import Optional
from storage.cache import Node


@dataclass
class Entry:
    value: str
    expiry: Optional[int] = None
    node: Optional["Node"] = None