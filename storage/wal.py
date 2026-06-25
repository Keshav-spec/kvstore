import os
from config import WAL_FILE

class WriteAheadLog:

    def __init__(self, filename=WAL_FILE):

        self.filename = filename

        if not os.path.exists(self.filename):
            open(self.filename, "w").close()

    def append(self, command, args):

        line = command

        if args:
            line += " " + " ".join(map(str, args))

        line += "\n"

        with open(
            self.filename,
            "a",
            encoding="utf-8"
        ) as file:

            file.write(line)

            file.flush()

    def replay(self):

        commands = []

        with open(
            self.filename,
            "r",
            encoding="utf-8"
        ) as file:

            for line in file:

                line = line.strip()

                if not line:
                    continue

                commands.append(
                    line.split()
                )

        return commands

    def clear(self):

        open(
            self.filename,
            "w"
        ).close()