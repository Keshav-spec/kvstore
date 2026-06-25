import threading
import time
from config import TTL_CLEAN_INTERVAL

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

            

            self.store.cleanup_expired()

            time.sleep(TTL_CLEAN_INTERVAL)