import socket
import threading
from config import HOST, PORT
from server.connection import handle_client
from logger import logger

logger.info("Client connected")

class RedisLiteServer:

    def __init__(
        self,
        host=HOST,
        port=PORT
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

            thread = threading.Thread(
                target=handle_client,
                args=(conn, store),
                daemon=True
            )

            thread.start()