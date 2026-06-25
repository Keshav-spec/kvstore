from storage.store import Store
from storage.wal import WriteAheadLog

wal = WriteAheadLog("compact_test.wal")
wal.clear()

store = Store(wal)

store.set("name", "Keshav")
store.set("city", "Chennai")

store.delete("name")

snapshot = store.snapshot()

wal.compact(snapshot)

# print(wal.replay())