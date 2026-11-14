"""Bab 11: linear search.

Pseudocode mengembalikan indeks 1..n atau 0 bila tidak ada.
Python mengembalikan indeks 0..n-1 atau -1 bila tidak ada.
Jalankan: python3 linear_search.py
"""


def linear_search(a, x):
    """Indeks pertama i dengan a[i] == x, atau -1."""
    for i in range(len(a)):
        if a[i] == x:
            return i
    return -1


def linear_search_hitung(a, x):
    """Seperti linear_search, ditambah jumlah perbandingan a[i] == x."""
    banding = 0
    for i in range(len(a)):
        banding += 1
        if a[i] == x:
            return i, banding
    return -1, banding


def linear_search_sentinel(a, x):
    """Versi sentinel: x ditaruh di ujung sehingga loop tidak perlu cek batas."""
    n = len(a)
    a.append(x)                      # sentinel
    i = 0
    while a[i] != x:
        i += 1
    a.pop()                          # kembalikan list seperti semula
    return i if i < n else -1


if __name__ == "__main__":
    nilai = [42, 17, 8, 99, 23, 8]
    assert linear_search(nilai, 99) == 3
    assert linear_search(nilai, 8) == 2          # kemunculan pertama
    assert linear_search(nilai, 5) == -1
    assert linear_search([], 5) == -1            # list kosong
    assert linear_search(nilai, 42) == 0         # elemen pertama
    assert linear_search(nilai, 8) == nilai.index(8)
    assert linear_search_hitung(nilai, 42) == (0, 1)   # best case: 1 perbandingan
    assert linear_search_hitung(nilai, 5) == (-1, 6)   # worst case: n perbandingan
    for x in [42, 17, 8, 99, 23, 5, -1]:
        assert linear_search_sentinel(nilai, x) == linear_search(nilai, x)
    assert nilai == [42, 17, 8, 99, 23, 8]
    print("linear_search(nilai, 99) =", linear_search(nilai, 99))
    print("Semua uji linear_search.py lolos.")
