"""2-approximation vertex cover dan pembanding brute force (Algoritma 32.2)."""
from itertools import combinations


def vc_aproksimasi(sisi):
    cover = set()
    for u, v in sisi:                  # urutan sisi menentukan hasil
        if u not in cover and v not in cover:
            cover.add(u)               # ambil kedua ujung sisi yang belum tertutup
            cover.add(v)
    return cover


def vc_optimal(n, sisi):
    for k in range(n + 1):
        for c in combinations(range(n), k):
            s = set(c)
            if all(u in s or v in s for u, v in sisi):
                return s
    return set(range(n))


if __name__ == "__main__":
    sisi = [(0, 1), (1, 2), (2, 3), (3, 4), (1, 3)]   # graf Bab 22
    a = vc_aproksimasi(sisi)
    o = vc_optimal(5, sisi)
    print(sorted(a), sorted(o))        # [0, 1, 2, 3] [1, 3]
    assert len(a) <= 2 * len(o)
    # bintang: pusat 0, daun 1..6
    bintang = [(0, i) for i in range(1, 7)]
    print(sorted(vc_aproksimasi(bintang)), sorted(vc_optimal(7, bintang)))
    # uji acak kecil: rasio tidak pernah lebih dari 2
    import random
    rng = random.Random(1)
    for _ in range(300):
        n = rng.randint(2, 9)
        s = [(u, v) for u in range(n) for v in range(u + 1, n) if rng.random() < 0.35]
        assert len(vc_aproksimasi(s)) <= 2 * len(vc_optimal(n, s))
    print("semua uji lolos")
