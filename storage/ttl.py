import threading
import time


class ExpiryCleaner:

    def __init__(self, store):
        self.store = store
        self.running = False

    def start(self):

        print("Expiry cleaner started")

        self.running = True

        thread = threading.Thread(
            target=self.run,
            daemon=True
        )

        thread.start()

    def run(self):

        while self.running:

            print("Cleaner tick")

            self.store.cleanup_expired()

            time.sleep(1)