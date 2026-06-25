import time


def recover(store, wal):
    """
    Rebuild the in-memory store from the write-ahead log.
    """

    print("Recovering database...")

    records = wal.replay()

    for record in records:

        print(record)

        cmd = record["cmd"]

        if cmd == "SET":

            expiry = record.get("expiry")

            # Skip expired keys
            if (
                expiry is not None
                and expiry <= int(time.time())
            ):
                continue

            store.set(
                record["key"],
                record["value"],
                log=False
            )

            if expiry is not None:
                store.data[record["key"]].expiry = expiry

        elif cmd == "DEL":

            store.delete(
                record["key"],
                log=False
            )

        elif cmd == "FLUSHALL":

            store.flushall(
                log=False
            )