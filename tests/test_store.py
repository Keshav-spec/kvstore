from storage.store import Store


def test_set_and_get():
    store = Store()

    store.set("name", "keshav")

    assert store.get("name") == "keshav"


def test_delete_existing_key():
    store = Store()

    store.set("name", "keshav")

    assert store.delete("name") == 1
    assert store.get("name") is None


def test_delete_missing_key():
    store = Store()

    assert store.delete("unknown") == 0


def test_exists():
    store = Store()

    store.set("name", "keshav")

    assert store.exists("name") is True
    assert store.exists("city") is False


def test_dbsize():
    store = Store()

    store.set("a", "1")
    store.set("b", "2")

    assert store.dbsize() == 2


def test_flushall():
    store = Store()

    store.set("a", "1")
    store.set("b", "2")

    store.flushall()

    assert store.dbsize() == 0