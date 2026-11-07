"""Kode 1.3: merasakan laju pertumbuhan O(n^2) vs O(n log n) secara empiris."""
import time

import numpy as np


def pasangan_terdekat_naif(a):
    # O(n^2): bandingkan setiap pasangan
    best = np.inf
    for i in range(len(a)):
        for j in range(i + 1, len(a)):
            best = min(best, abs(a[i] - a[j]))
    return best


def pasangan_terdekat_urut(a):
    # O(n log n): urutkan dulu, lalu cukup cek tetangga
    b = np.sort(a)
    return np.min(np.diff(b))


def main():
    rng = np.random.default_rng(0)
    for n in [500, 1000, 2000]:
        a = rng.random(n)
        t0 = time.perf_counter()
        r1 = pasangan_terdekat_naif(a)
        t1 = time.perf_counter()
        r2 = pasangan_terdekat_urut(a)
        t2 = time.perf_counter()
        assert np.isclose(r1, r2)
        print(f"n={n:5d}  naif={t1 - t0:.3f}s  urut={t2 - t1:.5f}s")
    # Saat n digandakan, waktu versi naif naik sekitar 4 kali.


if __name__ == "__main__":
    main()
