"""Uji stres: membandingkan solusi cepat dengan brute force (Kode 34.2).

Soal: jumlah subarray kontigu (tidak kosong) terbesar.
solusi_cepat_salah meniru jawaban yang lolos contoh soal
tetapi salah bila semua bilangan negatif.
"""
import random


def brute_force(a):
    n = len(a)
    return max(sum(a[i:j + 1]) for i in range(n) for j in range(i, n))   # O(n^3)


def solusi_cepat_salah(a):
    terbaik = kini = 0                  # BUG: mulai dari 0
    for x in a:
        kini = max(0, kini + x)
        terbaik = max(terbaik, kini)
    return terbaik


def solusi_cepat_benar(a):              # Kadane, O(n)
    terbaik = kini = a[0]
    for x in a[1:]:
        kini = max(x, kini + x)
        terbaik = max(terbaik, kini)
    return terbaik


def uji_stres(f, percobaan=1000, seed=0):
    rng = random.Random(seed)
    for _ in range(percobaan):
        a = [rng.randint(-5, 5) for _ in range(rng.randint(1, 6))]
        if f(a) != brute_force(a):
            return a                    # contoh penyangkal
    return None


if __name__ == "__main__":
    contoh = [-2, 1, -3, 4, -1, 2, 1, -5, 4]
    print(solusi_cepat_salah(contoh), solusi_cepat_benar(contoh))   # 6 6
    c = uji_stres(solusi_cepat_salah)
    print("contoh penyangkal:", c, solusi_cepat_salah(c), brute_force(c))
    assert c is not None and all(x < 0 for x in c)
    assert uji_stres(solusi_cepat_benar) is None
    print("semua uji lolos")
