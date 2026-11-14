"""Closest pair naif (Algoritma 24.2, Kode 24.2).

Membandingkan semua n(n-1)/2 pasangan. Jarak dibandingkan dalam bentuk
kuadrat agar tidak perlu akar.
"""


def closest_pair_naif(titik):
    n = len(titik)
    terbaik = None
    pasangan = None
    for i in range(n - 1):
        for j in range(i + 1, n):
            dx = titik[i][0] - titik[j][0]
            dy = titik[i][1] - titik[j][1]
            d2 = dx * dx + dy * dy
            if terbaik is None or d2 < terbaik:
                terbaik = d2
                pasangan = (titik[i], titik[j])
    return pasangan, terbaik


if __name__ == "__main__":
    P = [(2, 3), (12, 30), (40, 50), (5, 1), (12, 10), (3, 4)]
    pas, d2 = closest_pair_naif(P)
    assert pas == ((2, 3), (3, 4)) and d2 == 2
    # banyak pasangan untuk n = 6 adalah 15
    assert len(P) * (len(P) - 1) // 2 == 15
    print("closest_pair.py: pasangan", pas, "jarak^2", d2, "semua uji lolos")
