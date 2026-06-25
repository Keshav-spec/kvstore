from storage.wal import WriteAheadLog

wal = WriteAheadLog("test.wal")
wal.clear()

wal.append("SET", "name", "Keshav")
wal.append("SET", "token", "abc", 1750865000)
wal.append("DEL", "name")
wal.append("FLUSHALL")

records = wal.replay()

for record in records:
    print(record)