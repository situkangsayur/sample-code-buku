"""Exhaustive search: TSP, knapsack 0/1, dan assignment (Algoritma 24.3-21.4,
Kode 24.3).

Instance kecil di sini sama dengan yang dipakai lagi di Bab 25, 25, 26, dan 27.
"""
from itertools import combinations, permutations

# ---------- TSP: empat kota A, B, C, D (Gambar 24.4) ----------
KOTA = ["A", "B", "C", "D"]
JARAK = {("A", "B"): 2, ("A", "C"): 9, ("A", "D"): 10,
         ("B", "C"): 6, ("B", "D"): 4, ("C", "D"): 3}


def d(u, v):
    return JARAK[(u, v)] if (u, v) in JARAK else JARAK[(v, u)]


def tsp_brute(kota):
    awal, sisa = kota[0], kota[1:]
    terbaik, rute_terbaik = None, None
    for p in permutations(sisa):            # (n-1)! urutan
        rute = (awal,) + p + (awal,)
        panjang = sum(d(rute[i], rute[i + 1]) for i in range(len(rute) - 1))
        if terbaik is None or panjang < terbaik:
            terbaik, rute_terbaik = panjang, rute
    return rute_terbaik, terbaik


# ---------- Knapsack 0/1: empat barang, kapasitas W = 10 ----------
BERAT = [5, 4, 6, 3]
NILAI = [10, 40, 30, 50]
W = 10


def knapsack_brute(berat, nilai, W):
    """Mencoba semua 2^n himpunan bagian lewat bit mask.
    Bit ke-i bernilai 1 berarti barang ke-(i+1) diambil."""
    n = len(berat)
    terbaik, pilih = 0, ()
    for mask in range(1 << n):
        b = sum(berat[i] for i in range(n) if mask >> i & 1)
        v = sum(nilai[i] for i in range(n) if mask >> i & 1)
        if b <= W and v > terbaik:
            terbaik = v
            pilih = tuple(i + 1 for i in range(n) if mask >> i & 1)
    return pilih, terbaik


def semua_subset(n):
    for r in range(n + 1):
        for c in combinations(range(1, n + 1), r):
            yield c


# ---------- Assignment: empat orang, empat pekerjaan ----------
BIAYA = [[8, 3, 6, 9],
         [5, 7, 2, 6],
         [4, 9, 8, 3],
         [7, 5, 9, 4]]


def assignment_brute(C):
    n = len(C)
    terbaik, p_terbaik = None, None
    for p in permutations(range(n)):        # orang i mendapat pekerjaan p[i]
        total = sum(C[i][p[i]] for i in range(n))
        if terbaik is None or total < terbaik:
            terbaik, p_terbaik = total, p
    return p_terbaik, terbaik


if __name__ == "__main__":
    rute, panjang = tsp_brute(KOTA)
    assert panjang == 18 and rute == ("A", "B", "D", "C", "A")

    pilih, v = knapsack_brute(BERAT, NILAI, W)
    assert pilih == (2, 4) and v == 90
    layak = [s for s in semua_subset(4) if sum(BERAT[i - 1] for i in s) <= W]
    assert len(layak) == 10                   # Tabel 24.5: 10 dari 16 layak
    # varian Bab 25 dan 27: barang 3 = (7, 63), optimum {3, 4} = 113
    assert knapsack_brute([5, 4, 7, 3], [10, 40, 63, 50], 10) == ((3, 4), 113)

    p, total = assignment_brute(BIAYA)
    assert p == (1, 2, 0, 3) and total == 13  # orang 1->J2, 2->J3, 3->J1, 4->J4
    print("exhaustive.py: semua uji lolos")
