def ping_command(store, args):
    return b"+PONG\r\n"


def set_command(store, args):
    if len(args) != 2:
        return b"-ERR wrong number of arguments\r\n"

    key, value = args

    store.set(key, value)

    return b"+OK\r\n"


def get_command(store, args):
    if len(args) != 1:
        return b"-ERR wrong number of arguments\r\n"

    key = args[0]

    value = store.get(key)

    if value is None:
        return b"$-1\r\n"

    response = f"${len(value)}\r\n{value}\r\n"

    return response.encode()


def del_command(store, args):
    if len(args) != 1:
        return b"-ERR wrong number of arguments\r\n"

    deleted = store.delete(args[0])

    return f":{deleted}\r\n".encode()


def exists_command(store, args):
    if len(args) != 1:
        return b"-ERR wrong number of arguments\r\n"

    exists = int(store.exists(args[0]))

    return f":{exists}\r\n".encode()


def dbsize_command(store, args):
    size = store.dbsize()

    return f":{size}\r\n".encode()


def flushall_command(store, args):
    store.flushall()

    return b"+OK\r\n"