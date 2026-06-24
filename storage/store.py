import threading
import time

class Store:
    def __init__(self):
        self.data = {}
        self.lock = threading.RLock()

    def set(self, key: str, value: str):
        with self.lock:
            self.data[key] = {
                "value": value,
                "expiry": None
            }
            return True

    def get(self, key):

        with self.lock:

            entry = self.data.get(key)

            if entry is None:
                return None

            expiry = entry["expiry"]

            if expiry is not None:

                if expiry <= int(time.time()):

                    del self.data[key]

                    return None

            return entry["value"]

    def delete(self, key: str):
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

    def flushall(self):
        with self.lock:
            self.data.clear()
            return True
    def set_expiry(self, key, seconds):
        with self.lock:

            if key not in self.data:
                return False

            self.data[key]["expiry"] = (
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

            keys_to_delete = []

            for key, entry in self.data.items():

                expiry = entry.get("expiry")

                if expiry is not None and expiry <= now:
                    keys_to_delete.append(key)

            for key in keys_to_delete:

                print(f"Deleting expired key: {key}")

                del self.data[key]