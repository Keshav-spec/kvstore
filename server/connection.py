from server.parser import RESPParser
from commands.registry import dispatch
from config import BUFFER_SIZE

parser = RESPParser()


def handle_client(conn, store):
    buffer = b""

    try:
        while True:

            data = conn.recv(BUFFER_SIZE)

            if not data:
                break

            buffer += data


            while True:

                command, consumed = parser.parse(buffer)

                if command is None:
                    break


                buffer = buffer[consumed:]

                response = dispatch(
                    store,
                    command
                )

                conn.sendall(response)

    except Exception as e:
        import traceback

        traceback.print_exc()

        error = f"-ERR {str(e)}\r\n"

        try:
            conn.sendall(error.encode())
        except Exception:
            pass

    finally:
        conn.close()