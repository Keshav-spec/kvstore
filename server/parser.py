class RESPParser:
    def parse(self, data: bytes):
        text = data.decode()

        lines = text.split("\r\n")

        if not lines[0].startswith("*"):
            raise ValueError("Invalid RESP Array")

        num_elements = int(lines[0][1:])

        result = []

        idx = 1

        for _ in range(num_elements):
            if not lines[idx].startswith("$"):
                raise ValueError("Expected bulk string")

            idx += 1

            result.append(lines[idx])

            idx += 1

        return result