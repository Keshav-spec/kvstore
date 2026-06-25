import unittest

from storage.cache import LRUCache


class TestLRUCache(unittest.TestCase):

    def test_insert(self):

        cache = LRUCache(3)

        cache.touch("A")
        cache.touch("B")
        cache.touch("C")

        self.assertEqual(len(cache.nodes), 3)

        self.assertTrue(cache.contains("A"))
        self.assertTrue(cache.contains("B"))
        self.assertTrue(cache.contains("C"))

    def test_existing_key_moves_to_front(self):

        cache = LRUCache(3)

        cache.touch("A")
        cache.touch("B")
        cache.touch("C")

        cache.touch("A")

        first = cache.list.head.next

        self.assertIsNotNone(first)

        if first is not None:
            self.assertEqual(
                first.key,
                "A"
            )

    def test_lru_eviction(self):

        cache = LRUCache(3)

        cache.touch("A")
        cache.touch("B")
        cache.touch("C")

        evicted = cache.touch("D")

        self.assertEqual(evicted, "A")

        self.assertFalse(cache.contains("A"))
        self.assertTrue(cache.contains("B"))
        self.assertTrue(cache.contains("C"))
        self.assertTrue(cache.contains("D"))

    def test_recent_access_changes_eviction(self):

        cache = LRUCache(3)

        cache.touch("A")
        cache.touch("B")
        cache.touch("C")

        cache.touch("A")

        evicted = cache.touch("D")

        self.assertEqual(evicted, "B")

        self.assertFalse(cache.contains("B"))
        self.assertTrue(cache.contains("A"))
        self.assertTrue(cache.contains("C"))
        self.assertTrue(cache.contains("D"))

    def test_remove_existing_key(self):

        cache = LRUCache(3)

        cache.touch("A")
        cache.touch("B")

        cache.remove("A")

        self.assertFalse(cache.contains("A"))
        self.assertEqual(len(cache.nodes), 1)

    def test_remove_missing_key(self):

        cache = LRUCache(3)

        cache.touch("A")

        cache.remove("Z")

        self.assertTrue(cache.contains("A"))
        self.assertEqual(len(cache.nodes), 1)

    def test_capacity_never_exceeded(self):

        cache = LRUCache(3)

        for i in range(10):
            cache.touch(str(i))

        self.assertEqual(len(cache.nodes), 3)

    def test_evict_empty_cache(self):

        cache = LRUCache(3)

        self.assertIsNone(cache.evict())

    def test_remove_all(self):

        cache = LRUCache(3)

        cache.touch("A")
        cache.touch("B")
        cache.touch("C")

        cache.remove("A")
        cache.remove("B")
        cache.remove("C")

        self.assertEqual(len(cache.nodes), 0)


if __name__ == "__main__":
    unittest.main()