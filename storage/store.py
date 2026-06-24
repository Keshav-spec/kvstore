import threading


class Store:
    def __init__(self):
        self.data = {}
        self.lock = threading.RLock()

    def set(self, key: str, value: str):
        with self.lock:
            self.data[key] = value
            return True

    def get(self, key: str):
        with self.lock:
            return self.data.get(key)

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