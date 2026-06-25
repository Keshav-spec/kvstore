import unittest

from server.parser import RESPParser


class TestRESPParser(unittest.TestCase):

    def setUp(self):
        self.parser = RESPParser()

    def test_ping(self):

        data = b"*1\r\n$4\r\nPING\r\n"

        command, consumed = self.parser.parse(data)

        self.assertEqual(command, ["PING"])
        self.assertEqual(consumed, len(data))

    def test_get(self):

        data = (
            b"*2\r\n"
            b"$3\r\nGET\r\n"
            b"$4\r\nname\r\n"
        )

        command, consumed = self.parser.parse(data)

        self.assertEqual(
            command,
            ["GET", "name"]
        )

        self.assertEqual(consumed, len(data))

    def test_set(self):

        data = (
            b"*3\r\n"
            b"$3\r\nSET\r\n"
            b"$4\r\nname\r\n"
            b"$6\r\nkeshav\r\n"
        )

        command, consumed = self.parser.parse(data)

        self.assertEqual(
            command,
            [
                "SET",
                "name",
                "keshav"
            ]
        )

        self.assertEqual(consumed, len(data))

    def test_exists(self):

        data = (
            b"*2\r\n"
            b"$6\r\nEXISTS\r\n"
            b"$4\r\nname\r\n"
        )

        command, consumed = self.parser.parse(data)

        self.assertEqual(
            command,
            [
                "EXISTS",
                "name"
            ]
        )

        self.assertEqual(consumed, len(data))

    def test_delete(self):

        data = (
            b"*2\r\n"
            b"$3\r\nDEL\r\n"
            b"$4\r\nname\r\n"
        )

        command, consumed = self.parser.parse(data)

        self.assertEqual(
            command,
            [
                "DEL",
                "name"
            ]
        )

        self.assertEqual(consumed, len(data))

    def test_expire(self):

        data = (
            b"*3\r\n"
            b"$6\r\nEXPIRE\r\n"
            b"$4\r\nname\r\n"
            b"$2\r\n60\r\n"
        )

        command, consumed = self.parser.parse(data)

        self.assertEqual(
            command,
            [
                "EXPIRE",
                "name",
                "60"
            ]
        )

        self.assertEqual(consumed, len(data))

    def test_ttl(self):

        data = (
            b"*2\r\n"
            b"$3\r\nTTL\r\n"
            b"$4\r\nname\r\n"
        )

        command, consumed = self.parser.parse(data)

        self.assertEqual(
            command,
            [
                "TTL",
                "name"
            ]
        )

        self.assertEqual(consumed, len(data))

    def test_dbsize(self):

        data = (
            b"*1\r\n"
            b"$6\r\nDBSIZE\r\n"
        )

        command, consumed = self.parser.parse(data)

        self.assertEqual(
            command,
            [
                "DBSIZE"
            ]
        )

        self.assertEqual(consumed, len(data))

    def test_flushall(self):

        data = (
            b"*1\r\n"
            b"$8\r\nFLUSHALL\r\n"
        )

        command, consumed = self.parser.parse(data)

        self.assertEqual(
            command,
            [
                "FLUSHALL"
            ]
        )

        self.assertEqual(consumed, len(data))

    def test_keys(self):

        data = (
            b"*2\r\n"
            b"$4\r\nKEYS\r\n"
            b"$1\r\n*\r\n"
        )

        command, consumed = self.parser.parse(data)

        self.assertEqual(
            command,
            [
                "KEYS",
                "*"
            ]
        )

        self.assertEqual(consumed, len(data))


if __name__ == "__main__":
    unittest.main()