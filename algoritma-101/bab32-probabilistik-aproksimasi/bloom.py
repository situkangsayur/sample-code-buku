"""Bloom filter dengan double hashing (Kode 32.3)."""
import hashlib
import math


class BloomFilter:
    def __init__(self, m, k):
        self.m, self.k = m, k
        self.bit = bytearray(m)        # satu byte per bit agar mudah dibaca

    def _posisi(self, item):
        h = hashlib.sha256(item.encode()).digest()
        h1 = int.from_bytes(h[:8], "big")
        h2 = int.from_bytes(h[8:16], "big") | 1
        return [(h1 + i * h2) % self.m for i in range(self.k)]

    def tambah(self, item):
        for p in self._posisi(item):
            self.bit[p] = 1

    def mungkin_ada(self, item):
        return all(self.bit[p] for p in self._posisi(item))


def peluang_fp(m, n, k):
    return (1 - math.exp(-k * n / m)) ** k


def k_optimal(m, n):
    return max(1, round(m / n * math.log(2)))


if __name__ == "__main__":
    n, m = 1000, 10000                 # 10 bit per item
    k = k_optimal(m, n)
    print(k)                           # 7
    bf = BloomFilter(m, k)
    for i in range(n):
        bf.tambah(f"user{i}")
    assert all(bf.mungkin_ada(f"user{i}") for i in range(n))   # tanpa false negative
    uji = 100000
    fp = sum(bf.mungkin_ada(f"tamu{i}") for i in range(uji))
    print(f"false positive teramati: {fp / uji:.4f}")
    print(f"perkiraan rumus        : {peluang_fp(m, n, k):.4f}")   # 0.0082
    assert abs(fp / uji - peluang_fp(m, n, k)) < 0.004
    print("semua uji lolos")
