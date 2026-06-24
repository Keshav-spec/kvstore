class RESPParser:

    def parse(self, buffer: bytes):

        if not buffer:
            return None, 0

        try:
            pos = 0

            if buffer[pos:pos+1] != b"*":
                return None, 0

            end = buffer.find(b"\r\n", pos)

            if end == -1:
                return None, 0

            num_elements = int(
                buffer[pos+1:end]
            )

            pos = end + 2

            result = []

            for _ in range(num_elements):

                if pos >= len(buffer):
                    return None, 0

                if buffer[pos:pos+1] != b"$":
                    raise ValueError(
                        "Expected bulk string"
                    )

                end = buffer.find(
                    b"\r\n",
                    pos
                )

                if end == -1:
                    return None, 0

                length = int(
                    buffer[pos+1:end]
                )

                pos = end + 2

                if len(buffer) < pos + length + 2:
                    return None, 0

                value = buffer[
                    pos:pos+length
                ].decode()

                result.append(value)

                pos += length + 2

            return result, pos

        except Exception:
            return None, 0