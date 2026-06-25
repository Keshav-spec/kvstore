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

            # Debug logs (remove later if desired)
            print(f"RECEIVED: {repr(data)}")
            print(f"BUFFER: {repr(buffer)}")

            while True:

                command, consumed = parser.parse(buffer)

                if command is None:
                    break

                print(f"COMMAND: {command}")

                buffer = buffer[consumed:]

                response = dispatch(
                    store,
                    command
                )

                print(f"RESPONSE: {response}")

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