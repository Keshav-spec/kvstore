import threading
import time

from storage.models import Entry
from storage.cache import LRUCache


class Store:

    def __init__(self, wal=None, capacity=3):

        self.data = {}
        self.lock = threading.RLock()

        self.wal = wal
        self.cache = LRUCache(capacity)

    def set(self, key: str, value: str, log=True):

        if log and self.wal:

            expiry = None

            if key in self.data:
                expiry = self.data[key].expiry

            self.wal.append(
                command="SET",
                key=key,
                value=value,
                expiry=expiry
            )

        with self.lock:

            self.data[key] = Entry(value=value)

            # Update LRU
            evicted = self.cache.touch(key)

            if evicted is not None:
                self.data.pop(evicted, None)

            return True

    def get(self, key):

        with self.lock:

            entry = self.data.get(key)

            if entry is None:
                return None

            if (
                entry.expiry is not None
                and entry.expiry <= int(time.time())
            ):

                del self.data[key]
                self.cache.remove(key)

                return None

            # Mark as recently used
            self.cache.touch(key)

            return entry.value

    def delete(self, key: str, log=True):

        if log and self.wal:
            self.wal.append(
                command="DEL",
                key=key
            )

        with self.lock:

            if key in self.data:

                del self.data[key]
                self.cache.remove(key)

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
                command="FLUSHALL"
            )

        with self.lock:

            self.data.clear()

            # Reset cache
            self.cache = LRUCache(self.cache.capacity)

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

            expiry = self.data[key].expiry

            if expiry is None:
                return -1

            remaining = expiry - int(time.time())

            if remaining <= 0:

                del self.data[key]
                self.cache.remove(key)

                return -2

            return remaining

    def cleanup_expired(self):

        with self.lock:

            now = int(time.time())

            expired = []

            for key, entry in self.data.items():

                if (
                    entry.expiry is not None
                    and entry.expiry <= now
                ):
                    expired.append(key)

            for key in expired:

                print(f"Deleting expired key: {key}")

                del self.data[key]
                self.cache.remove(key)