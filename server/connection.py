from server.parser import RESPParser
from commands.registry import dispatch


parser = RESPParser()


def handle_client(conn, store):
    try:
        while True:

            data = conn.recv(4096)

            print("RAW:", repr(data))

            command = parser.parse(data)

            print("PARSED:", command)

            response = dispatch(store, command)

            print("RESPONSE:", response)

            conn.sendall(response)

    except Exception as e:

        error = f"-ERR {str(e)}\r\n"

        conn.sendall(error.encode())

    finally:
        conn.close()