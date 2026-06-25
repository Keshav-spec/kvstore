import threading
import unittest

from storage.store import Store


class TestConcurrency(unittest.TestCase):

    def setUp(self):
        self.store = Store()

    def worker(self, thread_id):

        for i in range(100):

            key = f"thread{thread_id}_{i}"

            self.store.set(key, str(i))

            value = self.store.get(key)

            self.assertEqual(value, str(i))

            if i % 2 == 0:
                self.store.delete(key)

    def test_multiple_threads(self):

        threads = []

        for i in range(20):

            thread = threading.Thread(
                target=self.worker,
                args=(i,)
            )

            threads.append(thread)

            thread.start()

        for thread in threads:
            thread.join()

        # Verify all remaining keys are readable

        for key in list(self.store.data.keys()):

            self.assertIsNotNone(
                self.store.get(key)
            )


if __name__ == "__main__":
    unittest.main()