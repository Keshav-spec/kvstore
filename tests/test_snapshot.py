from storage.store import Store

store = Store()

store.set("name", "Keshav")
store.set("city", "Chennai")

store.set_expiry("city", 60)

snapshot = store.snapshot()

for record in snapshot:
    print(record)