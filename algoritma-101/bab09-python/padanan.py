"""Bab 9: padanan pseudocode dan Python.

Setiap fungsi di sini diterjemahkan dari pseudocode di Bab 9 (dan Bab 4, 6, 7).
Ingat: pseudocode memakai indeks mulai 1, Python mulai 0.
Jalankan: python3 padanan.py
"""


def maksimum(a):
    """Algoritma Maksimum: nilai terbesar di list a (tidak kosong)."""
    maks = a[0]                      # pseudocode: maks <- A[1]
    for i in range(1, len(a)):       # pseudocode: for i <- 2 to n
        if a[i] > maks:
            maks = a[i]
    return maks


def jumlah_deret(n):
    """Jumlah 1 + 2 + ... + n dengan for."""
    s = 0
    for i in range(1, n + 1):        # batas atas range tidak ikut, jadi n + 1
        s = s + i
    return s


def fpb(a, b):
    """FPB Euclid dengan while (Bab 7)."""
    while b != 0:
        a, b = b, a % b              # tukar serentak, tanpa variabel bantu
    return a


def faktorial(n):
    """Faktorial rekursif (Bab 8)."""
    if n == 0:
        return 1
    return n * faktorial(n - 1)


def baca_sampai_positif(data):
    """Padanan repeat ... until x > 0.

    Python tidak punya repeat-until, jadi dipakai while True + break.
    `data` menggantikan input dari keyboard agar fungsi dapat diuji.
    """
    it = iter(data)
    while True:
        x = next(it)                 # badan loop: minimal dijalankan sekali
        if x > 0:                    # kondisi until diuji di akhir
            break
    return x


def nama_hari(k):
    """Padanan case/depend on dengan match (Python 3.10 ke atas)."""
    match k:
        case 1:
            return "Senin"
        case 2:
            return "Selasa"
        case 6 | 7:
            return "akhir pekan"
        case _:
            return "hari kerja lain"


def hitung_genap(a):
    """Contoh continue: hitung bilangan genap, lewati yang negatif."""
    c = 0
    for x in a:
        if x < 0:
            continue
        if x % 2 == 0:
            c += 1
    return c


if __name__ == "__main__":
    assert maksimum([7, 3, 9, 2]) == 9
    assert maksimum([-5]) == -5
    assert jumlah_deret(100) == 5050
    assert jumlah_deret(0) == 0
    assert fpb(48, 18) == 6
    assert fpb(17, 5) == 1
    assert faktorial(5) == 120
    assert baca_sampai_positif([-3, 0, 4, 8]) == 4
    assert baca_sampai_positif([2]) == 2
    assert nama_hari(1) == "Senin" and nama_hari(7) == "akhir pekan"
    assert nama_hari(4) == "hari kerja lain"
    assert hitung_genap([2, -4, 3, 8, 0]) == 3
    print("maksimum([7, 3, 9, 2]) =", maksimum([7, 3, 9, 2]))
    print("jumlah_deret(100) =", jumlah_deret(100))
    print("fpb(48, 18) =", fpb(48, 18))
    print("Semua uji padanan.py lolos.")
