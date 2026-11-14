"""Penukaran koin minimum dengan DP (tabulation).

Bab 29 buku Algoritma 101, Algoritma 29.3.
"""

INF = float("inf")


def koin_minimum(koin, x):
    """Kembalikan (banyak koin minimum, daftar koin) untuk nilai x.

    C[v] = min over c in koin, c <= v, dari C[v - c] + 1; C[0] = 0.
    """
    c = [0] + [INF] * x
    pilih = [0] * (x + 1)  # koin terakhir yang dipakai untuk mencapai v
    for v in range(1, x + 1):
        for k in koin:
            if k <= v and c[v - k] + 1 < c[v]:
                c[v] = c[v - k] + 1
                pilih[v] = k
    if c[x] == INF:
        return None, []
    hasil = []
    v = x
    while v > 0:
        hasil.append(pilih[v])
        v -= pilih[v]
    return c[x], hasil


def koin_greedy(koin, x):
    """Greedy Bab 25: ambil koin terbesar yang masih muat."""
    hasil = []
    for k in sorted(koin, reverse=True):
        while x >= k:
            hasil.append(k)
            x -= k
    return hasil if x == 0 else None


if __name__ == "__main__":
    n, daftar = koin_minimum([1, 3, 4], 6)
    assert n == 2 and sorted(daftar) == [3, 3]
    assert koin_greedy([1, 3, 4], 6) == [4, 1, 1]
    assert koin_minimum([2], 3) == (None, [])
    assert koin_minimum([1, 5, 10, 25], 63)[0] == 6
    # tabel C[0..6] untuk Tabel 29.2
    tabel = [koin_minimum([1, 3, 4], v)[0] for v in range(7)]
    assert tabel == [0, 1, 2, 1, 1, 2, 2]
    print("C[0..6] =", tabel)
    print("6 dengan koin {1,3,4}:", daftar)
    print("semua uji lolos")
