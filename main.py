from storage.store import Store
from storage.ttl import ExpiryCleaner
from storage.wal import WriteAheadLog
from storage.recovery import recover
from server.server import RedisLiteServer


def replay_wal(store, wal):

    commands = wal.replay()

    for command in commands:

        if not command:
            continue

        cmd = command[0].upper()

        if cmd == "SET":

            if len(command) >= 3:
                store.set(
                    command[1],
                    command[2],
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


def main():

    wal = WriteAheadLog()

    store = Store(wal)

    recover(store, wal)

    cleaner = ExpiryCleaner(store)
    cleaner.start(verbose=True)

    server = RedisLiteServer()

    server.start(store)


if __name__ == "__main__":
    main()