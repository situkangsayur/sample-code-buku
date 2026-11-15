"""Bab 36: LSM-tree mini dengan Bloom filter per SSTable.

Tulis masuk ke memtable (dict). Bila penuh, memtable di-flush menjadi
SSTable: list pasangan (key, value) terurut + Bloom filter.
Baca: memtable dulu, lalu SSTable dari yang terbaru. SSTable dilewati
bila Bloom filter menjawab "pasti tidak ada".
Hapus memakai tombstone. Compaction menggabung semua SSTable.
"""
import bisect
import hashlib
import math
import random

TOMBSTONE = object()


class BloomFilter:
    def __init__(self, m, k):
        self.m, self.k = m, k
        self.bits = bytearray((m + 7) // 8)

    def _posisi(self, key):
        # double hashing: g_i(x) = h1(x) + i * h2(x) mod m
        d = hashlib.blake2b(repr(key).encode(), digest_size=16).digest()
        h1 = int.from_bytes(d[:8], "little")
        h2 = int.from_bytes(d[8:], "little") | 1
        return [(h1 + i * h2) % self.m for i in range(self.k)]

    def add(self, key):
        for p in self._posisi(key):
            self.bits[p >> 3] |= 1 << (p & 7)

    def mungkin_ada(self, key):
        return all(self.bits[p >> 3] >> (p & 7) & 1 for p in self._posisi(key))


def ukuran_bloom(n, p):
    """m dan k optimal untuk n elemen dan peluang false positive p."""
    m = math.ceil(-n * math.log(p) / (math.log(2) ** 2))
    k = max(1, round(m / n * math.log(2)))
    return m, k


class SSTable:
    def __init__(self, pasangan, p=0.01):
        self.keys = [k for k, _ in pasangan]
        self.values = [v for _, v in pasangan]
        m, k = ukuran_bloom(max(1, len(pasangan)), p)
        self.bloom = BloomFilter(m, k)
        for key in self.keys:
            self.bloom.add(key)

    def get(self, key):
        i = bisect.bisect_left(self.keys, key)       # binary search
        if i < len(self.keys) and self.keys[i] == key:
            return True, self.values[i]
        return False, None


class LSMTree:
    def __init__(self, batas_memtable=64):
        self.memtable = {}
        self.sstables = []                           # lama ke baru
        self.batas = batas_memtable
        self.dilewati = 0                            # dihemat oleh Bloom
        self.dibaca = 0                              # SSTable yang dibuka

    def put(self, key, value):
        self.memtable[key] = value
        if len(self.memtable) >= self.batas:
            self.flush()

    def delete(self, key):
        self.put(key, TOMBSTONE)

    def flush(self):
        if self.memtable:
            self.sstables.append(SSTable(sorted(self.memtable.items())))
            self.memtable = {}

    def get(self, key):
        if key in self.memtable:
            v = self.memtable[key]
            return None if v is TOMBSTONE else v
        for sst in reversed(self.sstables):
            if not sst.bloom.mungkin_ada(key):
                self.dilewati += 1
                continue
            self.dibaca += 1
            ada, v = sst.get(key)
            if ada:
                return None if v is TOMBSTONE else v
        return None

    def compact(self):
        gabung = {}
        for sst in self.sstables:                    # yang baru menimpa
            gabung.update(zip(sst.keys, sst.values))
        hidup = sorted((k, v) for k, v in gabung.items() if v is not TOMBSTONE)
        self.sstables = [SSTable(hidup)] if hidup else []


if __name__ == "__main__":
    m, k = ukuran_bloom(1000, 0.01)
    assert (m, k) == (9586, 7)                       # sekitar 9,6 bit per key

    bf = BloomFilter(m, k)
    for i in range(1000):
        bf.add(i)
    assert all(bf.mungkin_ada(i) for i in range(1000))   # tanpa false negative
    fp = sum(bf.mungkin_ada(i) for i in range(10_000, 110_000)) / 100_000
    print("false positive teramati: %.4f (target 0,01)" % fp)
    assert fp < 0.02

    rng = random.Random(34)
    lsm, model = LSMTree(batas_memtable=50), {}
    for _ in range(5000):
        key = rng.randrange(800)
        if rng.random() < 0.15:
            lsm.delete(key)
            model.pop(key, None)
        else:
            val = rng.randrange(10**6)
            lsm.put(key, val)
            model[key] = val
    for key in range(1000):
        assert lsm.get(key) == model.get(key)
    print("SSTable: %d, dibuka: %d, dilewati Bloom: %d"
          % (len(lsm.sstables), lsm.dibaca, lsm.dilewati))
    assert lsm.dilewati > lsm.dibaca
    lsm.flush()
    lsm.compact()
    assert len(lsm.sstables) == 1
    for key in range(1000):
        assert lsm.get(key) == model.get(key)
    print("lsm_bloom: semua uji lolos")
