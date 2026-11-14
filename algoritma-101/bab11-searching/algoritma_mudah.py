"""Bab 11: algoritma mudah.

Maksimum (dengan posisinya), jumlah, tukar nilai, cek prima, konversi biner.
Indeks Python mulai 0; pseudocode di buku mulai 1.
Jalankan: python3 algoritma_mudah.py
"""


def maks_dan_posisi(a):
    """Nilai terbesar dan indeks pertama tempat ia muncul (a tidak kosong)."""
    maks, pos = a[0], 0
    for i in range(1, len(a)):
        if a[i] > maks:              # > (bukan >=): posisi pertama yang dipertahankan
            maks, pos = a[i], i
    return maks, pos


def jumlah(a):
    s = 0
    for x in a:
        s += x
    return s


def tukar(a, i, j):
    """Tukar A[i] dan A[j] dengan variabel bantu, seperti di pseudocode."""
    temp = a[i]
    a[i] = a[j]
    a[j] = temp


def is_prima(n):
    """True bila n prima. Cukup uji pembagi d dengan d * d <= n."""
    if n < 2:
        return False
    d = 2
    while d * d <= n:
        if n % d == 0:
            return False
        d += 1
    return True


def ke_biner(n):
    """Konversi bilangan bulat n >= 0 ke string biner dengan pembagian berulang."""
    if n == 0:
        return "0"
    digit = []
    while n > 0:
        digit.append(str(n % 2))     # sisa bagi = bit paling kanan yang belum ditulis
        n //= 2
    digit.reverse()
    return "".join(digit)


if __name__ == "__main__":
    assert maks_dan_posisi([4, 9, 2, 9, 1]) == (9, 1)
    assert maks_dan_posisi([-3]) == (-3, 0)
    assert maks_dan_posisi([-8, -2, -5]) == (-2, 1)   # semua negatif
    assert jumlah([]) == 0 and jumlah([1, 2, 3]) == 6
    a = [10, 20, 30]
    tukar(a, 0, 2)
    assert a == [30, 20, 10]
    tukar(a, 1, 1)                                     # tukar dengan diri sendiri
    assert a == [30, 20, 10]
    prima = [n for n in range(30) if is_prima(n)]
    assert prima == [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
    assert not is_prima(1) and not is_prima(0) and not is_prima(-7)
    assert is_prima(97) and not is_prima(91)           # 91 = 7 * 13
    for n in range(0, 300):
        assert ke_biner(n) == bin(n)[2:]               # bandingkan dengan fungsi bawaan
    assert ke_biner(13) == "1101"
    print("maks_dan_posisi([4, 9, 2, 9, 1]) =", maks_dan_posisi([4, 9, 2, 9, 1]))
    print("prima < 30:", prima)
    print("ke_biner(13) =", ke_biner(13))
    print("Semua uji algoritma_mudah.py lolos.")
