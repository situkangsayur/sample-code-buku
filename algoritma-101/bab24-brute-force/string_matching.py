"""String matching naif (Algoritma 24.1, Kode 24.1, Tabel 24.2).

Mengembalikan semua posisi kemunculan (indeks 0) dan banyak perbandingan
karakter, supaya jumlah langkah bisa dibandingkan dengan hitungan tangan.
"""


def cari_naif(teks, pola):
    n, m = len(teks), len(pola)
    posisi = []
    banding = 0
    for i in range(n - m + 1):          # setiap pergeseran
        j = 0
        while j < m:
            banding += 1
            if teks[i + j] != pola[j]:
                break
            j += 1
        if j == m:
            posisi.append(i)
    return posisi, banding


if __name__ == "__main__":
    pos, b = cari_naif("ABRAKADABRA", "ABRA")
    assert pos == [0, 7]
    assert b == 16, b                   # Tabel 24.2
    # kasus terburuk: teks AAAA...A, pola AA...AB
    teks = "A" * 20
    pola = "A" * 4 + "B"
    pos, b = cari_naif(teks, pola)
    assert pos == [] and b == (20 - 5 + 1) * 5
    assert cari_naif("abc", "abcd") == ([], 0)
    assert "ABRAKADABRA".find("ABRA") == 0
    print("string_matching.py: semua uji lolos")
