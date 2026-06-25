from dataclasses import dataclass


@dataclass
class Entry:
    value: str
    expiry: int | None = None