"""Knapsack 0/1 dengan DP tabel V[i][w] dan penelusuran balik.

Bab 30 buku Algoritma 101, Algoritma 30.4 dan 26.5.
Instance bersama Bab 25, 25, 26, 27: W = 10,
barang (berat, nilai): (5, 10), (4, 40), (6, 30), (3, 50).
"""


def knapsack_tabel(berat, nilai, kapasitas):
    """V[i][w] = nilai terbaik memakai barang 1..i dengan kapasitas w.

    Indeks barang di buku mulai 1; di sini list Python mulai 0,
    sehingga barang ke-i ada di berat[i - 1].
    """
    n = len(berat)
    v = [[0] * (kapasitas + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        wi, vi = berat[i - 1], nilai[i - 1]
        for w in range(kapasitas + 1):
            v[i][w] = v[i - 1][w]  # barang i tidak diambil
            if wi <= w and v[i - 1][w - wi] + vi > v[i][w]:
                v[i][w] = v[i - 1][w - wi] + vi  # barang i diambil
    return v


def telusur_balik(v, berat, kapasitas):
    """Kembalikan nomor barang (mulai 1) yang diambil."""
    ambil = []
    w = kapasitas
    for i in range(len(berat), 0, -1):
        if v[i][w] != v[i - 1][w]:
            ambil.append(i)
            w -= berat[i - 1]
    return sorted(ambil)


def knapsack_1d(berat, nilai, kapasitas):
    """Versi hemat memori: satu baris, w diturunkan dari besar ke kecil."""
    best = [0] * (kapasitas + 1)
    for wi, vi in zip(berat, nilai):
        for w in range(kapasitas, wi - 1, -1):
            best[w] = max(best[w], best[w - wi] + vi)
    return best[kapasitas]


if __name__ == "__main__":
    berat = [5, 4, 6, 3]
    nilai = [10, 40, 30, 50]
    v = knapsack_tabel(berat, nilai, 10)
    for i, baris in enumerate(v):
        print(i, baris)
    assert v[4][10] == 90
    assert telusur_balik(v, berat, 10) == [2, 4]
    assert knapsack_1d(berat, nilai, 10) == 90
    assert v[2] == [0, 0, 0, 0, 40, 40, 40, 40, 40, 50, 50]
    assert v[3] == [0, 0, 0, 0, 40, 40, 40, 40, 40, 50, 70]
    assert v[4] == [0, 0, 0, 50, 50, 50, 50, 90, 90, 90, 90]
    # uji silang dengan brute force 2^n
    from itertools import combinations
    terbaik = 0
    for r in range(5):
        for s in combinations(range(4), r):
            if sum(berat[j] for j in s) <= 10:
                terbaik = max(terbaik, sum(nilai[j] for j in s))
    assert terbaik == 90
    print("nilai optimal 90, barang", telusur_balik(v, berat, 10))
    print("semua uji lolos")
