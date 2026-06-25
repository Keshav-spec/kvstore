import os

from config import WAL_FILE


class WriteAheadLog:

    def __init__(self, filename=WAL_FILE):

        self.filename = filename

        if not os.path.exists(self.filename):
            open(self.filename, "w").close()

    def append(self, command, key=None, value=None, expiry=None):
        """
        Append one operation to the WAL.

        Format:

        SET|key|value|expiry

        DEL|key

        FLUSHALL
        """

        if command == "SET":

            if expiry is None:
                expiry = ""

            line = f"SET|{key}|{value}|{expiry}\n"

        elif command == "DEL":

            line = f"DEL|{key}\n"

        elif command == "FLUSHALL":

            line = "FLUSHALL\n"

        else:

            raise ValueError(f"Unknown WAL command: {command}")

        with open(
            self.filename,
            "a",
            encoding="utf-8"
        ) as file:

            file.write(line)
            file.flush()

    def replay(self):
        """
        Read the WAL.

        Returns a list of parsed records.
        """

        records = []

        with open(
            self.filename,
            "r",
            encoding="utf-8"
        ) as file:

            for line in file:

                line = line.strip()

                if not line:
                    continue

                parts = line.split("|")

                command = parts[0]

                if command == "SET":

                    expiry = None

                    if len(parts) > 3 and parts[3] != "":
                        expiry = int(parts[3])

                    records.append({
                        "cmd": "SET",
                        "key": parts[1],
                        "value": parts[2],
                        "expiry": expiry
                    })

                elif command == "DEL":

                    records.append({
                        "cmd": "DEL",
                        "key": parts[1]
                    })

                elif command == "FLUSHALL":

                    records.append({
                        "cmd": "FLUSHALL"
                    })

        return records

    def clear(self):

        open(
            self.filename,
            "w"
        ).close()
    
    def compact(self, snapshot):
        """
        Rewrite the WAL using the current database snapshot.
        """

        temp_file = self.filename + ".tmp"

        with open(
            temp_file,
            "w",
            encoding="utf-8"
        ) as file:

            for record in snapshot:

                expiry = record["expiry"]

                if expiry is None:
                    expiry = ""

                line = (
                    f"SET|"
                    f"{record['key']}|"
                    f"{record['value']}|"
                    f"{expiry}\n"
                )

                file.write(line)

        os.replace(
            temp_file,
            self.filename
        )