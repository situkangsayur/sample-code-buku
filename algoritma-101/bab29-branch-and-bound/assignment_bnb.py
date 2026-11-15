"""Assignment problem dengan branch and bound (best-first, batas minimum per baris).

Bab 29 buku Algoritma 101 (Subbab 25.2, Gambar 29.2).
Baris = orang a..d, kolom = pekerjaan 1..4 (matriks contoh Levitin).
"""
import heapq
import itertools

C = [
    [9, 2, 7, 8],  # a
    [6, 4, 3, 7],  # b
    [5, 8, 1, 8],  # c
    [7, 6, 9, 4],  # d
]


def lower_bound(cost, assigned, C):
    """Biaya yang sudah pasti + minimum tiap baris berikutnya pada kolom yang masih bebas."""
    n = len(C)
    used = set(assigned)
    lb = cost
    for r in range(len(assigned), n):
        lb += min(C[r][c] for c in range(n) if c not in used)
    return lb


def assignment_bnb(C, trace=None):
    n = len(C)
    best_cost, best = float("inf"), None
    heap = [(lower_bound(0, [], C), 0, [])]
    made = 1
    while heap:
        lb, cost, assigned = heapq.heappop(heap)
        if trace is not None:
            trace.append((lb, assigned))
        if lb >= best_cost:
            continue  # tidak mungkin lebih murah dari solusi terbaik
        r = len(assigned)
        if r == n:
            best_cost, best = cost, assigned
            continue
        for c in range(n):
            if c in assigned:
                continue
            nc = cost + C[r][c]
            na = assigned + [c]
            made += 1
            nlb = lower_bound(nc, na, C)
            if nlb < best_cost:
                heapq.heappush(heap, (nlb, nc, na))
    return best_cost, best, made


if __name__ == "__main__":
    tr = []
    cost, sol, made = assignment_bnb(C, tr)
    print("biaya minimum:", cost, "penugasan:", [(chr(97 + r), c + 1) for r, c in enumerate(sol)])
    print("node dibuat:", made)
    for lb, a in tr:
        print("ambil lb=%d penugasan=%s" % (lb, [c + 1 for c in a]))
    assert lower_bound(0, [], C) == 10
    assert cost == 13 and sol == [1, 0, 2, 3]
    # uji silang dengan brute force (semua permutasi)
    import random
    rnd = random.Random(7)
    for _ in range(200):
        n = rnd.randint(1, 6)
        M = [[rnd.randint(1, 20) for _ in range(n)] for _ in range(n)]
        bf = min(sum(M[r][p[r]] for r in range(n)) for p in itertools.permutations(range(n)))
        assert assignment_bnb(M)[0] == bf
    print("semua uji lolos")
