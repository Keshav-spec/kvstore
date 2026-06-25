from storage.cache import Node, DoublyLinkedList

dll = DoublyLinkedList()

a = Node("A")
b = Node("B")
c = Node("C")

dll.add_to_front(a)
dll.add_to_front(b)
dll.add_to_front(c)

print("Initial:")
dll.display()

dll.move_to_front(a)

print("\nAfter moving A to front:")
dll.display()

removed = dll.remove_tail()

print(f"\nRemoved: {removed.key}")

print("\nRemaining:")
dll.display()