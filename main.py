from storage.store import Store
from server.server import RedisLiteServer
from storage.ttl import ExpiryCleaner


def main():

    store = Store()

    cleaner = ExpiryCleaner(store)
    cleaner.start()

    server = RedisLiteServer()
    server.start(store)


if __name__ == "__main__":
    main()