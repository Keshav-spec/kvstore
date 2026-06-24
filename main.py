from storage.store import Store
from server.server import RedisLiteServer


def main():

    store = Store()

    server = RedisLiteServer()

    server.start(store)


if __name__ == "__main__":
    main()