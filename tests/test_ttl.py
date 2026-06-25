import time
import unittest

from storage.store import Store
from storage.ttl import ExpiryCleaner


class TestTTL(unittest.TestCase):

    def setUp(self):
        self.store = Store()

    def test_set_expiry(self):

        self.store.set("token", "abc")

        success = self.store.set_expiry(
            "token",
            5
        )

        self.assertTrue(success)

        ttl = self.store.ttl("token")

        self.assertGreaterEqual(ttl, 4)
        self.assertLessEqual(ttl, 5)

    def test_expired_key_returns_none(self):

        self.store.set("token", "abc")

        self.store.set_expiry(
            "token",
            1
        )

        time.sleep(2)

        self.assertIsNone(
            self.store.get("token")
        )

    def test_ttl_missing_key(self):

        self.assertEqual(
            self.store.ttl("missing"),
            -2
        )

    def test_ttl_without_expiry(self):

        self.store.set("name", "Keshav")

        self.assertEqual(
            self.store.ttl("name"),
            -1
        )

    def test_expiry_cleaner(self):

        cleaner = ExpiryCleaner(self.store)
        cleaner.start()

        self.store.set("temp", "hello")

        self.store.set_expiry(
            "temp",
            1
        )

        time.sleep(2)

        self.assertIsNone(
            self.store.get("temp")
        )

        cleaner.running = False

    def test_cleanup_expired(self):

        self.store.set("A", "1")
        self.store.set("B", "2")

        self.store.set_expiry("A", 1)

        time.sleep(2)

        self.store.cleanup_expired()

        self.assertFalse(
            self.store.exists("A")
        )

        self.assertTrue(
            self.store.exists("B")
        )


if __name__ == "__main__":
    unittest.main()