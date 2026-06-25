from storage.wal import WriteAheadLog

wal = WriteAheadLog()

wal.append("SET", ["name", "Keshav"])
wal.append("SET", ["city", "Chennai"])
wal.append("DEL", ["city"])

print(wal.replay())