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


class DoublyLinkedList:
    """
    Maintains access order for the LRU cache.

    Head = Most Recently Used (MRU)
    Tail = Least Recently Used (LRU)
    """

    def __init__(self):

        self.head = Node("__HEAD__")
        self.tail = Node("__TAIL__")

        self.head.next = self.tail
        self.tail.prev = self.head

    def add_to_front(self, node: Node):
        """
        Insert node immediately after head.
        """

        first = self.head.next

        if first is None:
            raise RuntimeError("Linked list is corrupted.")

        node.prev = self.head
        node.next = first

        self.head.next = node
        first.prev = node

    def remove(self, node: Node):
        """
        Remove a node from the list.
        """

        prev_node = node.prev
        next_node = node.next

        if prev_node:
            prev_node.next = next_node

        if next_node:
            next_node.prev = prev_node

        node.prev = None
        node.next = None

    def move_to_front(self, node: Node):
        """
        Mark a node as recently used.
        """

        self.remove(node)
        self.add_to_front(node)

    def remove_tail(self):
        """
        Remove the least recently used node.

        Returns:
            Node | None
        """

        if self.tail.prev == self.head:
            return None

        lru = self.tail.prev

        if lru is None:
            return None

        self.remove(lru)

        return lru
    def display(self):

        current = self.head.next

        while current is not None and current != self.tail:
            print(current.key, end=" ")

            current = current.next

        print()