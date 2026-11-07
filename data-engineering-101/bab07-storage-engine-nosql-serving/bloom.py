"""Bloom filter sederhana dan perbandingan false positive rate dengan rumus
p = (1 - e^(-k n / m))^k."""
import hashlib
import math
import random


class Bloom:
    def __init__(self, m: int, k: int):
        self.m, self.k = m, k
        self.bit = bytearray((m + 7) // 8)

    def _posisi(self, key: str):
        d = hashlib.sha256(key.encode()).digest()
        a = int.from_bytes(d[:8], "little")
        b = int.from_bytes(d[8:16], "little") | 1
        return ((a + i * b) % self.m for i in range(self.k))   # double hashing

    def tambah(self, key: str) -> None:
        for p in self._posisi(key):
            self.bit[p // 8] |= 1 << (p % 8)

    def mungkin_ada(self, key: str) -> bool:
        return all(self.bit[p // 8] >> (p % 8) & 1 for p in self._posisi(key))


if __name__ == "__main__":
    n = 100_000
    for bits_per_key in (5, 10, 15):
        m = n * bits_per_key
        k = max(1, round(bits_per_key * math.log(2)))          # k optimal = (m/n) ln 2
        bf = Bloom(m, k)
        for i in range(n):
            bf.tambah(f"rek:{i}")
        uji = [f"bukan:{random.random()}" for _ in range(50_000)]
        fp = sum(bf.mungkin_ada(x) for x in uji) / len(uji)
        teori = (1 - math.exp(-k * n / m)) ** k
        print(f"{bits_per_key:>2} bit/key, k={k}: FP terukur {fp:.4f}, teori {teori:.4f}")
    assert all(bf.mungkin_ada(f"rek:{i}") for i in range(n))   # tidak pernah salah negatif
    print("tidak ada false negative")
