"""Bab 1: mencari satu nama di antara 10.000 nama.

Membandingkan banyak perbandingan pada linear search (daftar acak)
dan binary search (daftar terurut). Indeks Python mulai dari 0,
sedangkan pseudocode di buku mulai dari 1.
"""
import math
import random


def linear_search(daftar, x):
    """Kembalikan (indeks, banyak_perbandingan); indeks -1 bila tidak ada."""
    langkah = 0
    for i, nama in enumerate(daftar):
        langkah += 1
        if nama == x:
            return i, langkah
    return -1, langkah


def binary_search(daftar, x):
    """daftar harus terurut. Kembalikan (indeks, banyak_perbandingan)."""
    lo, hi = 0, len(daftar) - 1
    langkah = 0
    while lo <= hi:
        mid = (lo + hi) // 2
        langkah += 1
        if daftar[mid] == x:
            return mid, langkah
        elif daftar[mid] < x:
            lo = mid + 1
        else:
            hi = mid - 1
    return -1, langkah


def buat_nama(n, seed=2026):
    """Nama buatan 'MHS00001' ... agar mudah diuji tanpa data pribadi."""
    nama = [f"MHS{i:05d}" for i in range(1, n + 1)]
    random.Random(seed).shuffle(nama)
    return nama


if __name__ == "__main__":
    n = 10_000
    acak = buat_nama(n)
    urut = sorted(acak)

    # Kasus terburuk linear search: nama tidak ada di daftar.
    _, lin_terburuk = linear_search(acak, "MHS99999")
    assert lin_terburuk == n

    # Kasus terburuk binary search tidak lebih dari floor(log2 n) + 1 = 14.
    batas = math.floor(math.log2(n)) + 1
    terburuk_biner = max(binary_search(urut, x)[1] for x in urut)
    _, biner_tidak_ada = binary_search(urut, "MHS99999")
    assert terburuk_biner <= batas and biner_tidak_ada <= batas
    assert batas == 14

    # Rata-rata linear search bila nama pasti ada: (n + 1) / 2.
    sampel = random.Random(7).sample(acak, 500)
    total = sum(linear_search(acak, x)[1] for x in sampel)
    rata_teori = (n + 1) / 2
    print(f"linear, terburuk      : {lin_terburuk} perbandingan")
    print(f"binary, terburuk      : {terburuk_biner} perbandingan (batas {batas})")
    print(f"linear, rata-rata teori: {rata_teori}")
    print(f"linear, 500 sampel acak: {total / 500:.1f} (posisi bergantung acakan)")

    # Pemeriksaan kebenaran: setiap nama ditemukan di posisi yang benar.
    for x in random.Random(1).sample(urut, 200):
        i, _ = binary_search(urut, x)
        assert urut[i] == x
        j, _ = linear_search(acak, x)
        assert acak[j] == x
    print("semua uji lolos")
