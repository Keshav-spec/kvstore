import os


class WriteAheadLog:

    def __init__(self, filename="wal.log"):
        self.filename = filename

        if not os.path.exists(filename):
            open(filename, "a").close()
    
    def append(self, command, args):

        line = command

        if args:
            line += " " + " ".join(args)

        line += "\n"

        with open(
            self.filename,
            "a",
            encoding="utf-8"
        ) as f:

            f.write(line)

            f.flush()
    def replay(self):

        commands = []

        with open(
            self.filename,
            "r",
            encoding="utf-8"
        ) as f:

            for line in f:

                line = line.strip()

                if not line:
                    continue

                commands.append(
                    line.split()
                )

        return commands