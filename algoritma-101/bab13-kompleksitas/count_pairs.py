"""Bab 13: menghitung pasangan (i, j), i < j, dengan A[i] + A[j] = x.

Dua versi dari pseudocode yang sama di buku:
- count_pairs_naive: dua loop bersarang, T(n) = n(n-1)/2 perbandingan, O(n^2)
- count_pairs_sorted: urutkan lalu dua penunjuk, O(n log n)
Penghitung langkah dipakai untuk mencocokkan T(n) dengan hitungan tangan.
"""
import random
import time


def count_pairs_naive(a, x):
    """Kembalikan (banyak pasangan, banyak perbandingan)."""
    n = len(a)
    count = 0
    steps = 0
    for i in range(n - 1):          # pseudocode: i dari 1 sampai n-1
        for j in range(i + 1, n):   # pseudocode: j dari i+1 sampai n
            steps += 1
            if a[i] + a[j] == x:
                count += 1
    return count, steps


def count_pairs_sorted(a, x):
    """Versi O(n log n): sort lalu dua penunjuk lo dan hi."""
    b = sorted(a)
    lo, hi = 0, len(b) - 1
    count = 0
    while lo < hi:
        s = b[lo] + b[hi]
        if s < x:
            lo += 1
        elif s > x:
            hi -= 1
        elif b[lo] == b[hi]:
            # semua elemen di antara lo..hi sama: pilih 2 dari k
            k = hi - lo + 1
            count += k * (k - 1) // 2
            break
        else:
            # hitung kelompok nilai sama di kiri dan kanan
            left_val, right_val = b[lo], b[hi]
            cl = 0
            while b[lo] == left_val:
                lo += 1
                cl += 1
            cr = 0
            while b[hi] == right_val:
                hi -= 1
                cr += 1
            count += cl * cr
    return count


def linear_search_steps(a, x):
    """Banyak perbandingan linear search sampai x ditemukan (atau n)."""
    steps = 0
    for v in a:
        steps += 1
        if v == x:
            break
    return steps


def main():
    a = [3, 1, 4, 1, 5]
    count, steps = count_pairs_naive(a, 5)
    print("pasangan berjumlah 5:", count, "perbandingan:", steps)  # 2 10
    assert (count, steps) == (2, 10)
    assert count_pairs_sorted(a, 5) == 2

    # T(n) = n(n-1)/2 untuk setiap n
    for n in [1, 2, 5, 10, 100]:
        _, s = count_pairs_naive(list(range(n)), -1)
        assert s == n * (n - 1) // 2

    # kedua versi selalu sama pada data acak
    rng = random.Random(13)
    for _ in range(300):
        n = rng.randint(0, 40)
        arr = [rng.randint(-5, 5) for _ in range(n)]
        x = rng.randint(-6, 6)
        assert count_pairs_naive(arr, x)[0] == count_pairs_sorted(arr, x)

    # best, worst, average case linear search pada n = 10
    arr = list(range(1, 11))
    best = linear_search_steps(arr, 1)
    worst = linear_search_steps(arr, 99)
    avg = sum(linear_search_steps(arr, v) for v in arr) / len(arr)
    print("linear search n=10: best", best, "worst", worst, "rata-rata", avg)
    assert (best, worst, avg) == (1, 10, 5.5)

    # gambaran waktu nyata (angka bergantung mesin)
    for n in [1000, 2000, 4000]:
        arr = [rng.randint(1, 10**6) for _ in range(n)]
        t0 = time.perf_counter()
        count_pairs_naive(arr, 10**6)
        t1 = time.perf_counter()
        count_pairs_sorted(arr, 10**6)
        t2 = time.perf_counter()
        print(f"n={n:5d} naif {t1 - t0:8.4f} s  sorted {t2 - t1:8.5f} s")
    print("semua uji lolos")


if __name__ == "__main__":
    main()
