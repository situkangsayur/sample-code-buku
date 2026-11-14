"""Bab 12: menguji ketiga sorting dengan kasus batas dan uji acak.

Jalankan: python3 uji_sorting.py
"""
import random

from sorting import SEMUA, bubble_sort, insertion_sort, selection_sort

KASUS_BATAS = [
    [],                         # kosong
    [7],                        # satu elemen
    [2, 1],                     # dua elemen terbalik
    [1, 2, 3, 4, 5],            # sudah terurut
    [5, 4, 3, 2, 1],            # terbalik
    [3, 3, 3, 3],               # semua sama
    [4, 1, 4, 1, 4],            # duplikat
    [0, -5, 12, -5, 7],         # negatif
    [10 ** 18, -10 ** 18, 0],   # nilai sangat besar
]


def terurut(a, akhir):
    """True bila a[0..akhir-1] terurut menaik."""
    return all(a[k] <= a[k + 1] for k in range(akhir - 1))


def insertion_sort_diperiksa(a):
    """Insertion sort dengan assert loop invariant: a[0..i-1] terurut."""
    for i in range(1, len(a)):
        assert terurut(a, i), "invariant rusak di i = %d" % i
        kunci = a[i]
        j = i - 1
        while j >= 0 and a[j] > kunci:
            a[j + 1] = a[j]
            j -= 1
        a[j + 1] = kunci
    assert terurut(a, len(a))            # terminasi


def cek_stabil(f):
    """True bila f mempertahankan urutan relatif data dengan kunci sama."""
    data = [(3, "a"), (1, "b"), (3, "c"), (2, "d"), (1, "e")]

    class Item:
        def __init__(self, k, t):
            self.k, self.t = k, t

        def __lt__(self, o):
            return self.k < o.k

        def __gt__(self, o):
            return self.k > o.k

    items = [Item(k, t) for k, t in data]
    f(items)
    return [it.t for it in items] == [t for _, t in sorted(data, key=lambda p: p[0])]


if __name__ == "__main__":
    for f in SEMUA:
        for kasus in KASUS_BATAS:
            b = kasus.copy()
            f(b)
            assert b == sorted(kasus), (f.__name__, kasus, b)

    rng = random.Random(12)
    for _ in range(3000):
        n = rng.randint(0, 30)
        a = [rng.randint(-50, 50) for _ in range(n)]
        for f in SEMUA:
            b = a.copy()
            f(b)
            assert b == sorted(a)
        insertion_sort_diperiksa(a.copy())

    assert cek_stabil(bubble_sort)
    assert cek_stabil(insertion_sort)
    assert not cek_stabil(selection_sort)    # selection sort tidak stabil
    print("stabil: bubble =", cek_stabil(bubble_sort),
          "insertion =", cek_stabil(insertion_sort),
          "selection =", cek_stabil(selection_sort))
    print("Semua uji uji_sorting.py lolos.")
