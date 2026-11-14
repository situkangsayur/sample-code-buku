"""Bab 38: HyperLogLog (Flajolet dkk. 2007) versi sederhana.

Redis memakai m = 16384 register 6 bit (sekitar 12 KB). Di sini p dapat diatur.
Jalankan: python3 hyperloglog.py
"""
import math

MASK64 = (1 << 64) - 1


def fnv1a64(data: bytes) -> int:
    h = 0xCBF29CE484222325
    for b in data:
        h ^= b
        h = (h * 0x100000001B3) & MASK64
    return h


def mix64(x: int) -> int:
    """Finalizer splitmix64: meratakan bit hasil FNV."""
    x ^= x >> 30
    x = (x * 0xBF58476D1CE4E5B9) & MASK64
    x ^= x >> 27
    x = (x * 0x94D049BB133111EB) & MASK64
    x ^= x >> 31
    return x


class HyperLogLog:
    def __init__(self, p=10):
        self.p = p
        self.m = 1 << p
        self.reg = [0] * self.m

    def add(self, item: str):
        h = mix64(fnv1a64(item.encode()))
        idx = h >> (64 - self.p)               # p bit teratas memilih register
        rest = (h << self.p) & MASK64          # sisa 64 - p bit
        rank = 1
        while rank <= 64 - self.p and not (rest & (1 << 63)):
            rank += 1                          # posisi bit 1 pertama dari kiri
            rest = (rest << 1) & MASK64
        if rank > self.reg[idx]:
            self.reg[idx] = rank

    def count(self) -> float:
        m = self.m
        alpha = 0.7213 / (1 + 1.079 / m)
        z = sum(2.0 ** -r for r in self.reg)
        e = alpha * m * m / z
        zeros = self.reg.count(0)
        if e <= 2.5 * m and zeros > 0:         # koreksi rentang kecil
            e = m * math.log(m / zeros)
        return e

    def merge(self, other):
        self.reg = [max(a, b) for a, b in zip(self.reg, other.reg)]


if __name__ == "__main__":
    h = HyperLogLog(p=10)
    print(f"m = {h.m} register, galat baku teoretis = {1.04 / math.sqrt(h.m) * 100:.2f}%")
    for n in (1_000, 10_000, 100_000):
        h = HyperLogLog(p=10)
        for i in range(n):
            h.add(f"user-{i}")
            h.add(f"user-{i}")  # duplikat tidak menambah taksiran
        est = h.count()
        err = abs(est - n) / n * 100
        print(f"n = {n:>7}: taksiran = {est:,.0f}, galat = {err:.2f}%")
        assert err < 4 * 3.25  # dalam empat kali galat baku

    # gabungan dua HLL = HLL gabungan himpunan
    a, b = HyperLogLog(12), HyperLogLog(12)
    for i in range(0, 60_000):
        a.add(f"k{i}")
    for i in range(40_000, 100_000):
        b.add(f"k{i}")
    a.merge(b)
    assert abs(a.count() - 100_000) / 100_000 < 0.05
    print(f"Redis: 16384 register, galat baku = {1.04 / math.sqrt(16384) * 100:.2f}%")
    print("semua uji hyperloglog lolos")
