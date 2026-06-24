from server.parser import RESPParser


def test_ping():
    parser = RESPParser()

    data = b"*1\r\n$4\r\nPING\r\n"

    assert parser.parse(data) == ["PING"]


def test_get():
    parser = RESPParser()

    data = b"*2\r\n$3\r\nGET\r\n$4\r\nname\r\n"

    assert parser.parse(data) == ["GET", "name"]


def test_set():
    parser = RESPParser()

    data = (
        b"*3\r\n"
        b"$3\r\nSET\r\n"
        b"$4\r\nname\r\n"
        b"$6\r\nkeshav\r\n"
    )

    assert parser.parse(data) == [
        "SET",
        "name",
        "keshav"
    ]