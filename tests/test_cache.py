from storage.cache import LRUCache

cache = LRUCache(3)

cache.touch("A")
cache.touch("B")
cache.touch("C")

cache.list.display()

cache.touch("A")

cache.list.display()

evicted = cache.touch("D")

print("Evicted:", evicted)

cache.list.display()