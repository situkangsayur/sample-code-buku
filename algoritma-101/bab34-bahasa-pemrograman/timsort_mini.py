"""Bab 34: Timsort mini dengan kebijakan merge Powersort.

Versi sederhana dari list.sort() CPython 3.11+: mencari run alami,
memperpanjang run pendek dengan binary insertion sort sampai minrun,
lalu menggabung run memakai urutan "power" dari Munro dan Wild.
Galloping mode dihilangkan agar kode tetap pendek.
Indeks mulai 0 (Python), berbeda dengan pseudocode di buku yang mulai 1.
"""
import random

MIN_MERGE = 64


def hitung_minrun(n):
    """minrun di rentang [32, 64] untuk n >= 64 (sama dengan CPython)."""
    r = 0
    while n >= MIN_MERGE:
        r |= n & 1
        n >>= 1
    return n + r


def panjang_run(a, lo, hi, key):
    """Panjang run alami mulai lo. Run turun tegas dibalik di tempat."""
    if lo + 1 == hi:
        return 1
    j = lo + 1
    if key(a[j]) < key(a[lo]):          # turun tegas (agar tetap stabil)
        while j + 1 < hi and key(a[j + 1]) < key(a[j]):
            j += 1
        a[lo:j + 1] = a[lo:j + 1][::-1]
    else:                               # naik tidak tegas
        while j + 1 < hi and not key(a[j + 1]) < key(a[j]):
            j += 1
    return j + 1 - lo


def binary_insertion(a, lo, hi, mulai, key):
    """a[lo:mulai] sudah terurut; sisipkan a[mulai:hi] satu per satu."""
    for i in range(mulai, hi):
        x = a[i]
        kiri, kanan = lo, i
        while kiri < kanan:             # cari posisi paling kanan (stabil)
            tengah = (kiri + kanan) // 2
            if key(x) < key(a[tengah]):
                kanan = tengah
            else:
                kiri = tengah + 1
        a[kiri + 1:i + 1] = a[kiri:i]
        a[kiri] = x


def merge(a, lo, mid, hi, key):
    """Gabung a[lo:mid] dan a[mid:hi]; ambil kiri bila sama (stabil)."""
    kiri = a[lo:mid]
    i, j, k = 0, mid, lo
    while i < len(kiri) and j < hi:
        if key(a[j]) < key(kiri[i]):
            a[k] = a[j]
            j += 1
        else:
            a[k] = kiri[i]
            i += 1
        k += 1
    a[k:k + len(kiri) - i] = kiri[i:]


def power(s1, n1, n2, n):
    """Power batas antara run [s1, s1+n1) dan [s1+n1, s1+n1+n2)."""
    a = 2 * s1 + n1                     # dua kali titik tengah run kiri
    b = a + n1 + n2                     # dua kali titik tengah run kanan
    k = 0
    while True:
        k += 1
        if (a << k) // (2 * n) != (b << k) // (2 * n):
            return k


def timsort(a, key=lambda x: x):
    n = len(a)
    if n < 2:
        return a
    minrun = hitung_minrun(n)
    stack, powers = [], []              # stack berisi (awal, panjang)
    lo = 0
    while lo < n:
        m = panjang_run(a, lo, n, key)
        if m < minrun:                  # perpanjang run pendek
            ujung = min(lo + minrun, n)
            binary_insertion(a, lo, ujung, lo + m, key)
            m = ujung - lo
        if stack:
            s1, n1 = stack[-1]
            p = power(s1, n1, m, n)
            while powers and powers[-1] > p:
                (sa, na), (sb, nb) = stack[-2], stack[-1]
                merge(a, sa, sb, sb + nb, key)
                stack[-2:] = [(sa, na + nb)]
                powers.pop()
            powers.append(p)
        stack.append((lo, m))
        lo += m
    while len(stack) > 1:               # gabung sisa dari atas
        (sa, na), (sb, nb) = stack[-2], stack[-1]
        merge(a, sa, sb, sb + nb, key)
        stack[-2:] = [(sa, na + nb)]
    return a


def hitung_run(a):
    """Banyak run naik alami (untuk ilustrasi di buku)."""
    return 1 + sum(1 for i in range(1, len(a)) if a[i] < a[i - 1]) if a else 0


if __name__ == "__main__":
    assert hitung_minrun(63) == 63
    assert hitung_minrun(64) == 32
    assert hitung_minrun(2112) == 33
    assert 32 <= hitung_minrun(10**6) <= 64

    rng = random.Random(33)
    for n in [0, 1, 2, 5, 63, 64, 65, 200, 1000, 5000]:
        data = [rng.randint(0, 50) for _ in range(n)]
        assert timsort(data[:]) == sorted(data)

    # data hampir terurut: sedikit run, tetap benar
    hampir = list(range(3000))
    for _ in range(10):
        i, j = rng.randrange(3000), rng.randrange(3000)
        hampir[i], hampir[j] = hampir[j], hampir[i]
    assert timsort(hampir[:]) == sorted(hampir)

    # stabil: urut menurut nilai, nama asli tetap berurutan
    mhs = [("Ani", 80), ("Budi", 75), ("Citra", 80), ("Dewi", 75), ("Eka", 90)]
    hasil = timsort(mhs[:], key=lambda t: t[1])
    assert hasil == [("Budi", 75), ("Dewi", 75), ("Ani", 80), ("Citra", 80), ("Eka", 90)]
    assert hasil == sorted(mhs, key=lambda t: t[1])

    big = [(rng.randint(0, 9), i) for i in range(4000)]
    assert timsort(big[:], key=lambda t: t[0]) == sorted(big, key=lambda t: t[0])

    # contoh power di buku: n = 8, run [0,3) dan [3,5)
    assert power(0, 3, 2, 8) == 1
    assert power(3, 2, 3, 8) == 2
    # contoh di buku: empat run panjang 2 (n = 8)
    assert [power(0, 2, 2, 8), power(2, 2, 2, 8), power(4, 2, 2, 8)] == [2, 1, 2]
    # Coba Sendiri: run panjang 5, 1, 2
    assert [power(0, 5, 1, 8), power(5, 1, 2, 8)] == [1, 2]
    print("timsort_mini: semua uji lolos")
