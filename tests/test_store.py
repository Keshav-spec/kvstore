import unittest

from storage.store import Store


class TestStore(unittest.TestCase):

    def setUp(self):
        self.store = Store()

    def test_set_and_get(self):

        self.store.set("name", "Keshav")

        self.assertEqual(
            self.store.get("name"),
            "Keshav"
        )

    def test_get_missing_key(self):

        self.assertIsNone(
            self.store.get("missing")
        )

    def test_delete_existing_key(self):

        self.store.set("name", "Keshav")

        deleted = self.store.delete("name")

        self.assertEqual(
            deleted,
            1
        )

        self.assertIsNone(
            self.store.get("name")
        )

    def test_delete_missing_key(self):

        deleted = self.store.delete("unknown")

        self.assertEqual(
            deleted,
            0
        )

    def test_exists(self):

        self.store.set("city", "Chennai")

        self.assertTrue(
            self.store.exists("city")
        )

        self.assertFalse(
            self.store.exists("Delhi")
        )

    def test_dbsize(self):

        self.store.set("A", "1")
        self.store.set("B", "2")

        self.assertEqual(
            self.store.dbsize(),
            2
        )

    def test_flushall(self):

        self.store.set("A", "1")
        self.store.set("B", "2")

        self.store.flushall()

        self.assertEqual(
            self.store.dbsize(),
            0
        )

        self.assertIsNone(
            self.store.get("A")
        )


if __name__ == "__main__":
    unittest.main()