"""LSM-tree mini untuk belajar: memtable, flush ke SSTable terurut (immutable),
bloom filter per SSTable, tombstone, dan compaction. Tanpa WAL dan tanpa disk."""
import bisect

from bloom import Bloom

TOMBSTONE = object()


class SSTable:
    def __init__(self, items: dict):
        self.keys = sorted(items)
        self.vals = [items[k] for k in self.keys]
        self.bloom = Bloom(max(64, 10 * len(self.keys)), 7)
        for k in self.keys:
            self.bloom.tambah(k)

    def get(self, key):
        if not self.bloom.mungkin_ada(key):      # lewati tanpa "membaca disk"
            return None, False
        i = bisect.bisect_left(self.keys, key)   # pencarian biner: berkas terurut
        if i < len(self.keys) and self.keys[i] == key:
            return self.vals[i], True
        return None, False


class LSM:
    def __init__(self, batas_memtable: int = 4):
        self.mem, self.batas = {}, batas_memtable
        self.sst: list[SSTable] = []             # indeks 0 = paling baru
        self.baca_sst = 0                        # statistik amplifikasi baca

    def put(self, key, val):
        self.mem[key] = val                      # tulis ke memori: cepat
        if len(self.mem) >= self.batas:
            self.sst.insert(0, SSTable(self.mem))  # flush
            self.mem = {}

    def delete(self, key):
        self.put(key, TOMBSTONE)                 # hapus = tulis penanda

    def get(self, key):
        if key in self.mem:
            v = self.mem[key]
            return None if v is TOMBSTONE else v
        for t in self.sst:                       # dari yang terbaru
            v, ada = t.get(key)
            self.baca_sst += ada
            if ada:
                return None if v is TOMBSTONE else v
        return None

    def compaction(self):
        gabung = {}
        for t in reversed(self.sst):             # lama dulu, yang baru menimpa
            gabung.update(zip(t.keys, t.vals))
        hidup = {k: v for k, v in gabung.items() if v is not TOMBSTONE}
        self.sst = [SSTable(hidup)] if hidup else []


if __name__ == "__main__":
    db = LSM()
    for i in range(10):
        db.put(f"rek:{i:03d}", 1000 + i)
    db.put("rek:001", 5000)                      # versi baru, versi lama tetap di SSTable
    db.delete("rek:002")
    for i in range(10, 13):
        db.put(f"rek:{i:03d}", 1000 + i)
    print("jumlah SSTable sebelum compaction:", len(db.sst))
    print("rek:001 =", db.get("rek:001"), "| rek:002 =", db.get("rek:002"))
    total = sum(len(t.keys) for t in db.sst)
    print("entri di SSTable:", total, "(termasuk versi lama dan tombstone);",
          "di memtable:", len(db.mem))
    db.compaction()
    print("setelah compaction: SSTable", len(db.sst), "| entri", len(db.sst[0].keys))
    print("rek:001 =", db.get("rek:001"), "| rek:002 =", db.get("rek:002"))
