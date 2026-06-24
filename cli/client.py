import socket

HOST = "127.0.0.1"
PORT = 6399


def build_resp(parts):
    cmd = f"*{len(parts)}\r\n"

    for part in parts:
        cmd += f"${len(part)}\r\n{part}\r\n"

    return cmd


while True:

    raw = input("kv> ")

    if raw.lower() == "exit":
        break

    parts = raw.split()

    payload = build_resp(parts)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:

        s.connect((HOST, PORT))

        s.sendall(payload.encode())

        response = s.recv(4096)

        print(response.decode())