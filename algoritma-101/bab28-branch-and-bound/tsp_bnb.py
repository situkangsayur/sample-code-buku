"""TSP dengan branch and bound (depth-first, batas sisi keluar termurah).

Bab 28 buku Algoritma 101 (Algoritma 28.3, Kode 28.3).
Lima kota A..E, jarak simetris. Tur mulai dan berakhir di A.
"""
import itertools

D = [
    #  A  B  C  D  E
    [0, 3, 1, 5, 8],  # A
    [3, 0, 6, 7, 9],  # B
    [1, 6, 0, 4, 2],  # C
    [5, 7, 4, 0, 3],  # D
    [8, 9, 2, 3, 0],  # E
]


def min_out(D):
    """Sisi keluar termurah setiap kota (tanpa sisi ke dirinya sendiri)."""
    n = len(D)
    return [min(D[i][j] for j in range(n) if j != i) for i in range(n)]


def tsp_bnb(D):
    n = len(D)
    m = min_out(D)
    best = [float("inf"), None]
    stats = {"node": 0, "pangkas": 0}

    def lb(path, cost):
        # setiap kota yang belum ditinggalkan harus keluar lewat paling sedikit sisi termurahnya
        sisa = [k for k in range(n) if k not in path]
        return cost + m[path[-1]] + sum(m[k] for k in sisa)

    def visit(path, cost):
        stats["node"] += 1
        if len(path) == n:
            total = cost + D[path[-1]][0]  # kembali ke A
            if total < best[0]:
                best[0], best[1] = total, path + [0]
            return
        if lb(path, cost) >= best[0]:
            stats["pangkas"] += 1
            return
        for k in range(n):
            if k not in path:
                visit(path + [k], cost + D[path[-1]][k])

    visit([0], 0)
    return best[0], best[1], stats


def tsp_brute(D):
    n = len(D)
    return min(sum(D[a][b] for a, b in zip((0,) + p, p + (0,)))
               for p in itertools.permutations(range(1, n)))


if __name__ == "__main__":
    cost, tour, st = tsp_bnb(D)
    print("panjang tur:", cost, "tur:", "".join("ABCDE"[k] for k in tour))
    print("statistik:", st, "batas akar:", sum(min_out(D)))
    assert cost == tsp_brute(D) == 16
    import random
    rnd = random.Random(11)
    for _ in range(100):
        n = rnd.randint(3, 7)
        M = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(i + 1, n):
                M[i][j] = M[j][i] = rnd.randint(1, 30)
        assert tsp_bnb(M)[0] == tsp_brute(M)
    print("semua uji lolos")
