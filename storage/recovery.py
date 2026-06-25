import time


def recover(store, wal):
    """
    Rebuild the in-memory store from the write-ahead log.
    """

   

    records = wal.replay()

    for record in records:

        cmd = record["cmd"]

        if cmd == "SET":

            expiry = record.get("expiry")

            # Skip expired keys
            if (
                expiry is not None
                and expiry <= int(time.time())
            ):
                # A later SET with an expired TTL should remove
                # any previously restored version of this key.
                store.delete(
                    record["key"],
                    log=False
                )
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