from commands.string_cmds import (
    ping_command,
    set_command,
    get_command,
    del_command,
    exists_command,
    dbsize_command,
    flushall_command
)


COMMANDS = {
    "PING": ping_command,
    "SET": set_command,
    "GET": get_command,
    "DEL": del_command,
    "EXISTS": exists_command,
    "DBSIZE": dbsize_command,
    "FLUSHALL": flushall_command,
}


def dispatch(store, command_list):
    if not command_list:
        return b"-ERR empty command\r\n"

    cmd = command_list[0].upper()

    args = command_list[1:]

    handler = COMMANDS.get(cmd)

    if handler is None:
        return b"-ERR unknown command\r\n"

    return handler(store, args)