"""Greedy dasar: koin, activity selection, fractional knapsack, dan contoh gagal
(Algoritma 26.2-22.3, Kode 26.1).
"""
from fractions import Fraction


def koin_greedy(pecahan, x):
    """Ambil pecahan terbesar yang masih muat. pecahan diurut menurun."""
    hasil = []
    for c in pecahan:
        while x >= c:
            x -= c
            hasil.append(c)
    return hasil if x == 0 else None


def activity_selection(kegiatan):
    """kegiatan: list (nama, mulai, selesai). Urut menurut waktu selesai."""
    urut = sorted(kegiatan, key=lambda k: k[2])
    terpilih = []
    akhir = float("-inf")
    for nama, s, f in urut:
        if s >= akhir:               # tidak bentrok dengan yang terakhir dipilih
            terpilih.append(nama)
            akhir = f
    return terpilih


def fractional_knapsack(berat, nilai, W):
    """Urut menurut rasio nilai/berat; barang terakhir boleh diambil sebagian.
    Fraction dipakai agar hasilnya eksak."""
    urut = sorted(range(len(berat)), key=lambda i: nilai[i] / berat[i], reverse=True)
    total = Fraction(0)
    ambil = [Fraction(0)] * len(berat)
    sisa = W
    for i in urut:
        if sisa == 0:
            break
        x = min(Fraction(1), Fraction(sisa, berat[i]))
        ambil[i] = x
        total += x * nilai[i]
        sisa -= x * berat[i]
    return ambil, total


def knapsack01_greedy(berat, nilai, W):
    """Greedy rasio untuk knapsack 0/1: hanya utuh atau tidak sama sekali."""
    urut = sorted(range(len(berat)), key=lambda i: nilai[i] / berat[i], reverse=True)
    pilih, sisa, total = [], W, 0
    for i in urut:
        if berat[i] <= sisa:
            pilih.append(i + 1)
            sisa -= berat[i]
            total += nilai[i]
    return sorted(pilih), total


if __name__ == "__main__":
    rupiah = [50000, 20000, 10000, 5000, 2000, 1000]
    assert koin_greedy(rupiah, 87000) == [50000, 20000, 10000, 5000, 2000]
    # sistem koin {4, 3, 1}: greedy memberi 3 koin, optimal 2 koin (3 + 3)
    assert koin_greedy([4, 3, 1], 6) == [4, 1, 1]
    assert koin_greedy([5, 2], 6) is None     # padahal 6 = 2 + 2 + 2

    K = [("K1", 8, 10), ("K2", 9, 11), ("K3", 10, 12), ("K4", 11, 13),
         ("K5", 8, 13), ("K6", 12, 14), ("K7", 13, 15), ("K8", 14, 16)]
    assert activity_selection(K) == ["K1", "K3", "K6", "K8"]

    # instance knapsack Bab 25: berat 5,4,6,3; nilai 10,40,30,50; W = 10
    B, V, W = [5, 4, 6, 3], [10, 40, 30, 50], 10
    ambil, total = fractional_knapsack(B, V, W)
    assert ambil == [0, 1, Fraction(1, 2), 1] and total == 105
    assert knapsack01_greedy(B, V, W) == ([2, 4], 90)   # kebetulan optimal
    # varian barang 3 = (7, 63): greedy rasio 90, optimum {3, 4} = 113
    B2, V2 = [5, 4, 7, 3], [10, 40, 63, 50]
    assert knapsack01_greedy(B2, V2, W) == ([2, 4], 90)
    assert fractional_knapsack(B2, V2, W)[1] == 117
    print("greedy_dasar.py: semua uji lolos")
