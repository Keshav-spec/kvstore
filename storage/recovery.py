def recover(store, wal):
    """
    Rebuild the in-memory store from the write-ahead log.
    """

    commands = wal.replay()
    print("Recovering database...")
    for command in commands:
        print(command)
        if not command:
            continue

        cmd = command[0].upper()

        if cmd == "SET":

            if len(command) >= 3:

                key = command[1]
                value = command[2]

                store.set(
                    key,
                    value,
                    log=False
                )

        elif cmd == "DEL":

            if len(command) >= 2:

                store.delete(
                    command[1],
                    log=False
                )

        elif cmd == "FLUSHALL":

            store.flushall(
                log=False
            )