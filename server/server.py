import socket
import threading

from server.connection import handle_client


class RedisLiteServer:

    def __init__(
        self,
        host="127.0.0.1",
        port=6399
    ):
        self.host = host
        self.port = port

    def start(self, store):

        server = socket.socket(
            socket.AF_INET,
            socket.SOCK_STREAM
        )

        server.setsockopt(
            socket.SOL_SOCKET,
            socket.SO_REUSEADDR,
            1
        )

        server.bind(
            (self.host, self.port)
        )

        server.listen()

        print(
            f"Listening on {self.host}:{self.port}"
        )

        while True:

            conn, addr = server.accept()

            print(
                f"Client connected: {addr}"
            )

            thread = threading.Thread(
                target=handle_client,
                args=(conn, store),
                daemon=True
            )

            thread.start()