"""Belajar ambang dari data dan batas sampel PAC (Algoritma 34.1, Kode 34.1).

Data: (skor, label). Hipotesis: "label 1 bila skor >= t".
Algoritma memilih t yang kesalahannya paling kecil di data training
(empirical risk minimization).
"""
import math
import random


def belajar_ambang(data):
    data = sorted(data)                       # O(n log n)
    calon = [data[0][0]] + [x for x, _ in data] + [data[-1][0] + 1]
    terbaik_t, terbaik_salah = None, len(data) + 1
    for t in calon:
        salah = sum((x >= t) != (y == 1) for x, y in data)
        if salah < terbaik_salah:
            terbaik_t, terbaik_salah = t, salah
    return terbaik_t, terbaik_salah


def batas_pac(ukuran_h, eps, delta):
    """m >= (1/eps) (ln|H| + ln(1/delta)) untuk learner yang konsisten."""
    return math.ceil((math.log(ukuran_h) + math.log(1 / delta)) / eps)


DATA = [(2, 0), (3, 0), (5, 0), (6, 1), (8, 1), (9, 1), (4, 0), (7, 1)]

if __name__ == "__main__":
    print(belajar_ambang(DATA))               # (6, 0)
    print(batas_pac(1001, 0.05, 0.01))        # 231
    # simulasi: ambang sebenarnya 600 pada skor 0..999
    rng = random.Random(42)
    latih = [(x, int(x >= 600)) for x in (rng.randrange(1000) for _ in range(231))]
    t, salah = belajar_ambang(latih)
    uji = [(x, int(x >= 600)) for x in range(1000)]
    galat_uji = sum((x >= t) != (y == 1) for x, y in uji) / len(uji)
    print(t, salah, galat_uji)
    assert salah == 0 and galat_uji <= 0.05
    assert belajar_ambang(DATA) == (6, 0)
    assert batas_pac(1001, 0.05, 0.01) == 231
    print("semua uji lolos")
