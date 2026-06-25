from dataclasses import dataclass
from typing import Optional


@dataclass
class Node:
    """
    Node used in the doubly linked list for the LRU cache.
    """

    key: str
    prev: Optional["Node"] = None
    next: Optional["Node"] = None