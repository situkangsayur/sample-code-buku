"""Learned index sederhana: regresi linear + binary search terbatas (Algoritma 34.2)."""
import bisect
import random


class LearnedIndex:
    def __init__(self, keys):
        self.keys = keys                      # harus terurut
        n = len(keys)
        mx = sum(keys) / n
        my = (n - 1) / 2
        sxx = sum((k - mx) ** 2 for k in keys)
        sxy = sum((k - mx) * (i - my) for i, k in enumerate(keys))
        self.a = sxy / sxx                    # kemiringan
        self.b = my - self.a * mx             # titik potong
        self.err = max(abs(self._tebak(k) - i) for i, k in enumerate(keys))

    def _tebak(self, k):
        return round(self.a * k + self.b)

    def cari(self, k):
        """Kembalikan (indeks atau -1, banyak perbandingan)."""
        p = self._tebak(k)
        lo = max(0, p - self.err)
        hi = min(len(self.keys) - 1, p + self.err)
        banding = 0
        while lo <= hi:
            mid = (lo + hi) // 2
            banding += 1
            if self.keys[mid] == k:
                return mid, banding
            if self.keys[mid] < k:
                lo = mid + 1
            else:
                hi = mid - 1
        return -1, banding


def binary_search(keys, k):
    lo, hi, banding = 0, len(keys) - 1, 0
    while lo <= hi:
        mid = (lo + hi) // 2
        banding += 1
        if keys[mid] == k:
            return mid, banding
        if keys[mid] < k:
            lo = mid + 1
        else:
            hi = mid - 1
    return -1, banding


if __name__ == "__main__":
    rng = random.Random(3)
    keys = sorted(rng.sample(range(10_000_000), 1_000_000))   # hampir seragam
    li = LearnedIndex(keys)
    print(f"model: posisi ~ {li.a:.6f} * key + {li.b:.1f}, err maks {li.err}")
    total_li = total_bs = 0
    for k in rng.sample(keys, 10000):
        i, c = li.cari(k)
        j, d = binary_search(keys, k)
        assert i == j == bisect.bisect_left(keys, k)
        total_li += c
        total_bs += d
    print(f"rata-rata perbandingan: learned {total_li / 10000:.1f}, binary {total_bs / 10000:.1f}")
    assert li.cari(-5)[0] == -1
    assert total_li < total_bs
    print("semua uji lolos")
