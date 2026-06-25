import threading
import time

from storage.store import Store
from storage.wal import WriteAheadLog


NUM_THREADS = 20
OPS_PER_THREAD = 1000


def run_benchmark(title, worker):

    threads = []

    start = time.perf_counter()

    for thread_id in range(NUM_THREADS):

        thread = threading.Thread(
            target=worker,
            args=(thread_id,)
        )

        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    end = time.perf_counter()

    elapsed = end - start

    total_ops = NUM_THREADS * OPS_PER_THREAD

    print("=" * 55)
    print(title)
    print("-" * 55)
    print(f"Threads            : {NUM_THREADS}")
    print(f"Operations/thread  : {OPS_PER_THREAD}")
    print(f"Total operations   : {total_ops}")
    print(f"Elapsed time       : {elapsed:.4f} sec")
    print(f"Throughput         : {total_ops / elapsed:.2f} ops/sec")
    print()


def set_worker(thread_id):

    store = Store()

    for i in range(OPS_PER_THREAD):

        key = f"{thread_id}:{i}"

        store.set(
            key,
            str(i),
            log=False
        )


def get_worker(thread_id):

    store = Store()

    for i in range(OPS_PER_THREAD):

        key = f"{thread_id}:{i}"

        store.set(
            key,
            str(i),
            log=False
        )

    for i in range(OPS_PER_THREAD):

        key = f"{thread_id}:{i}"

        store.get(key)


def mixed_worker(thread_id):

    store = Store()

    for i in range(OPS_PER_THREAD):

        key = f"{thread_id}:{i}"

        store.set(
            key,
            str(i),
            log=False
        )

        store.get(key)


def wal_worker(thread_id):

    wal = WriteAheadLog("benchmark.wal")

    store = Store(wal=wal)

    for i in range(OPS_PER_THREAD):

        key = f"{thread_id}:{i}"

        store.set(
            key,
            str(i)
        )


def cleanup():

    import os

    if os.path.exists("benchmark.wal"):
        os.remove("benchmark.wal")


def main():

    cleanup()

    print()
    print("=" * 55)
    print("RedisLite Benchmark Suite")
    print("=" * 55)
    print()

    run_benchmark(
        "SET Benchmark",
        set_worker
    )

    run_benchmark(
        "GET Benchmark",
        get_worker
    )

    run_benchmark(
        "Mixed Benchmark",
        mixed_worker
    )

    run_benchmark(
        "WAL Benchmark",
        wal_worker
    )

    cleanup()


if __name__ == "__main__":
    main()