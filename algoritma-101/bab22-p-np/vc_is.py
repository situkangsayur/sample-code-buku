"""Reduksi Independent Set ke Vertex Cover (Contoh di subbab 29.4).

S independent set di G  <=>  V \\ S vertex cover di G.
Program ini memeriksa kesetaraan itu dengan brute force pada graf kecil.
"""
from itertools import combinations


def independen(sisi, s):
    return all(not (u in s and v in s) for u, v in sisi)


def cover(sisi, c):
    return all(u in c or v in c for u, v in sisi)


def reduksi_is_ke_vc(n, sisi, k):
    """Instance (G, k) Independent Set -> instance (G, n - k) Vertex Cover."""
    return n, sisi, n - k


def ada_is(n, sisi, k):
    return any(independen(sisi, set(s)) for s in combinations(range(n), k))


def ada_vc(n, sisi, k):
    return any(cover(sisi, set(c)) for c in combinations(range(n), k))


# graf contoh: path 0-1-2-3-4 ditambah sisi 1-3
G_SISI = [(0, 1), (1, 2), (2, 3), (3, 4), (1, 3)]

if __name__ == "__main__":
    print(independen(G_SISI, {0, 2, 4}))     # True
    print(cover(G_SISI, {1, 3}))             # True
    for k in range(0, 6):
        n2, s2, k2 = reduksi_is_ke_vc(5, G_SISI, k)
        assert ada_is(5, G_SISI, k) == ada_vc(n2, s2, k2)
    assert ada_is(5, G_SISI, 3) and not ada_is(5, G_SISI, 4)
    print("semua uji lolos")
