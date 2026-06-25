import threading
import time
from storage.models import Entry

class Store:

    def __init__(self, wal=None):

        self.data = {}
        self.lock = threading.RLock()
        self.wal = wal

    def set(self, key: str, value: str, log=True):

        if log and self.wal:
            self.wal.append(
                "SET",
                [key, value]
            )

        with self.lock:

            self.data[key] = Entry(value=value)

            return True

    def get(self, key):

        with self.lock:

            entry = self.data.get(key)

            if entry is None:
                return None

            expiry = entry.expiry

            if expiry is not None and expiry <= int(time.time()):

                del self.data[key]

                return None

            return entry.value

    def delete(self, key: str, log=True):

        if log and self.wal:
            self.wal.append(
                "DEL",
                [key]
            )

        with self.lock:

            if key in self.data:
                del self.data[key]
                return 1

            return 0

    def exists(self, key: str):

        with self.lock:
            return key in self.data

    def dbsize(self):

        with self.lock:
            return len(self.data)

    def flushall(self, log=True):

        if log and self.wal:
            self.wal.append(
                "FLUSHALL",
                []
            )

        with self.lock:

            self.data.clear()

            return True

    def set_expiry(self, key, seconds):

        with self.lock:

            if key not in self.data:
                return False

            self.data[key].expiry = (
                int(time.time()) + int(seconds)
            )

            return True

    def ttl(self, key):

        with self.lock:

            if key not in self.data:
                return -2

            expiry = self.data[key]["expiry"]

            if expiry is None:
                return -1

            remaining = expiry - int(time.time())

            if remaining <= 0:

                del self.data[key]

                return -2

            return remaining

    def cleanup_expired(self):

        with self.lock:

            now = int(time.time())

            expired_keys = []

            for key, entry in self.data.items():

                expiry = entry.expiry

                if expiry is not None and expiry <= now:
                    expired_keys.append(key)

            for key in expired_keys:

                print(f"Deleting expired key: {key}")

                del self.data[key]