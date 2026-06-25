import os
import time
import unittest

from storage.store import Store
from storage.wal import WriteAheadLog
from storage.recovery import recover


class TestRecovery(unittest.TestCase):

    TEST_WAL = "test_recovery.wal"

    def setUp(self):

        if os.path.exists(self.TEST_WAL):
            os.remove(self.TEST_WAL)

        self.wal = WriteAheadLog(self.TEST_WAL)

    def tearDown(self):

        if os.path.exists(self.TEST_WAL):
            os.remove(self.TEST_WAL)

    def test_recover_set(self):

        store = Store(self.wal)

        store.set("name", "Keshav")

        recovered = Store()

        recover(recovered, self.wal)

        self.assertEqual(
            recovered.get("name"),
            "Keshav"
        )

    def test_recover_delete(self):

        store = Store(self.wal)

        store.set("name", "Keshav")

        store.delete("name")

        recovered = Store()

        recover(recovered, self.wal)

        self.assertIsNone(
            recovered.get("name")
        )

    def test_recover_flushall(self):

        store = Store(self.wal)

        store.set("A", "1")
        store.set("B", "2")

        store.flushall()

        recovered = Store()

        recover(recovered, self.wal)

        self.assertEqual(
            recovered.dbsize(),
            0
        )

    def test_recover_ttl(self):

        store = Store(self.wal)

        store.set("token", "abc")

        store.set_expiry(
            "token",
            10
        )

        recovered = Store()

        recover(recovered, self.wal)

        ttl = recovered.ttl("token")

        self.assertGreater(ttl, 0)

    def test_skip_expired_key(self):

        store = Store(self.wal)

        store.set("temp", "hello")

        store.set_expiry(
            "temp",
            1
        )

        time.sleep(2)

        recovered = Store()

        recover(recovered, self.wal)

        self.assertIsNone(
            recovered.get("temp")
        )

    def test_multiple_operations(self):

        store = Store(self.wal)

        store.set("A", "1")
        store.set("B", "2")
        store.delete("A")
        store.set("C", "3")

        recovered = Store()

        recover(recovered, self.wal)

        self.assertIsNone(
            recovered.get("A")
        )

        self.assertEqual(
            recovered.get("B"),
            "2"
        )

        self.assertEqual(
            recovered.get("C"),
            "3"
        )


if __name__ == "__main__":
    unittest.main()