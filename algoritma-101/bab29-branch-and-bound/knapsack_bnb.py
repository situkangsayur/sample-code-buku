"""Knapsack 0/1 dengan branch and bound (best-first, batas fractional knapsack).

Bab 29 buku Algoritma 101 (Algoritma 29.1, 25.2; Kode 29.1).
Instance bersama Bab 25, 25, 26, 27: W = 10,
barang (berat, nilai): 1=(5,10), 2=(4,40), 3=(6,30), 4=(3,50).
"""
import heapq

W = 10
ITEMS = [(5, 10), (4, 40), (6, 30), (3, 50)]  # (berat, nilai), barang 1..4


def bound(i, w, v, items, cap):
    """Batas atas: isi sisa kapasitas secara fractional mulai barang ke-i."""
    if w > cap:
        return 0
    ub = v
    sisa = cap - w
    while i < len(items) and items[i][0] <= sisa:
        sisa -= items[i][0]
        ub += items[i][1]
        i += 1
    if i < len(items):
        ub += items[i][1] * sisa / items[i][0]  # pecahan barang berikutnya
    return ub


def knapsack_bnb(items, cap, trace=None):
    """Kembalikan (nilai terbaik, daftar nomor barang asli, banyak node dibuat)."""
    # urutkan menurut rasio nilai/berat menurun; simpan nomor asli (mulai 1)
    order = sorted(range(len(items)), key=lambda k: items[k][1] / items[k][0], reverse=True)
    its = [items[k] for k in order]
    best_v, best_set = 0, []
    # heap Python adalah min-heap, jadi batas disimpan negatif
    heap = [(-bound(0, 0, 0, its, cap), 0, 0, 0, [])]
    made = 1
    while heap:
        neg_ub, i, w, v, chosen = heapq.heappop(heap)
        ub = -neg_ub
        if trace is not None:
            trace.append((i, w, v, ub, best_v))
        if ub <= best_v or i == len(its):
            continue  # dipangkas: batasnya tidak lebih baik dari solusi terbaik
        wi, vi = its[i]
        for take in (True, False):
            nw, nv = (w + wi, v + vi) if take else (w, v)
            if nw > cap:
                continue  # tidak layak
            nchosen = chosen + [order[i] + 1] if take else chosen
            made += 1
            if nv > best_v:
                best_v, best_set = nv, nchosen
            nub = bound(i + 1, nw, nv, its, cap)
            if nub > best_v:
                heapq.heappush(heap, (-nub, i + 1, nw, nv, nchosen))
    return best_v, sorted(best_set), made


if __name__ == "__main__":
    tr = []
    v, s, made = knapsack_bnb(ITEMS, W, tr)
    print("nilai terbaik:", v, "barang:", s, "node dibuat:", made)
    for row in tr:
        print("ambil node: level=%d w=%d v=%d ub=%.1f best=%d" % row)
    assert v == 90 and s == [2, 4]
    assert bound(0, 0, 0, sorted(ITEMS, key=lambda t: t[1] / t[0], reverse=True), W) == 105
    # uji silang dengan brute force pada instance acak kecil
    import itertools
    import random
    rnd = random.Random(25)
    for _ in range(300):
        n = rnd.randint(1, 9)
        its = [(rnd.randint(1, 12), rnd.randint(1, 40)) for _ in range(n)]
        cap = rnd.randint(1, 30)
        bf = max(sum(its[k][1] for k in c)
                 for r in range(n + 1) for c in itertools.combinations(range(n), r)
                 if sum(its[k][0] for k in c) <= cap)
        assert knapsack_bnb(its, cap)[0] == bf
    print("semua uji lolos")
