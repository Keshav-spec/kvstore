import os
import unittest

from storage.wal import WriteAheadLog


class TestWriteAheadLog(unittest.TestCase):

    TEST_WAL = "test_kvstore.wal"

    def setUp(self):

        if os.path.exists(self.TEST_WAL):
            os.remove(self.TEST_WAL)

        self.wal = WriteAheadLog(self.TEST_WAL)

    def tearDown(self):

        if os.path.exists(self.TEST_WAL):
            os.remove(self.TEST_WAL)

    def test_append_set(self):

        self.wal.append(
            command="SET",
            key="name",
            value="Keshav"
        )

        records = self.wal.replay()

        self.assertEqual(len(records), 1)

        self.assertEqual(records[0]["cmd"], "SET")
        self.assertEqual(records[0]["key"], "name")
        self.assertEqual(records[0]["value"], "Keshav")
        self.assertIsNone(records[0]["expiry"])

    def test_append_set_with_expiry(self):

        self.wal.append(
            command="SET",
            key="token",
            value="abc",
            expiry=1234567890
        )

        records = self.wal.replay()

        self.assertEqual(records[0]["expiry"], 1234567890)

    def test_append_delete(self):

        self.wal.append(
            command="DEL",
            key="name"
        )

        records = self.wal.replay()

        self.assertEqual(records[0]["cmd"], "DEL")
        self.assertEqual(records[0]["key"], "name")

    def test_append_flushall(self):

        self.wal.append(
            command="FLUSHALL"
        )

        records = self.wal.replay()

        self.assertEqual(records[0]["cmd"], "FLUSHALL")

    def test_clear(self):

        self.wal.append(
            command="SET",
            key="A",
            value="1"
        )

        self.wal.clear()

        records = self.wal.replay()

        self.assertEqual(len(records), 0)

    def test_compaction(self):

        self.wal.append(
            command="SET",
            key="A",
            value="1"
        )

        self.wal.append(
            command="SET",
            key="B",
            value="2"
        )

        snapshot = [
            {
                "key": "B",
                "value": "2",
                "expiry": None
            }
        ]

        self.wal.compact(snapshot)

        records = self.wal.replay()

        self.assertEqual(len(records), 1)

        self.assertEqual(records[0]["key"], "B")

    def test_multiple_records(self):

        self.wal.append(
            command="SET",
            key="A",
            value="1"
        )

        self.wal.append(
            command="SET",
            key="B",
            value="2"
        )

        self.wal.append(
            command="DEL",
            key="A"
        )

        records = self.wal.replay()

        self.assertEqual(len(records), 3)

        self.assertEqual(records[2]["cmd"], "DEL")


if __name__ == "__main__":
    unittest.main()