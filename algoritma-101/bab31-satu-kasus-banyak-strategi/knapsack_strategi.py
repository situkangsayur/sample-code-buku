"""Satu instance knapsack 0/1, empat strategi: brute force, greedy, branch and bound, DP.

Bab 31 buku Algoritma 101 (Kode 31.1, 27.2, 27.4; Tabel 31.1-27.5; Algoritma 31.1-27.2).
Instance bersama Bab 25, 25, 26: W = 10,
barang (berat, nilai): 1=(5,10), 2=(4,40), 3=(6,30), 4=(3,50).
Setiap fungsi mengembalikan (nilai, himpunan barang, banyak langkah dasar).
"""
import heapq
import random

W = 10
ITEMS = [(5, 10), (4, 40), (6, 30), (3, 50)]


def brute_force(items, cap):
    """Coba semua 2^n himpunan bagian; langkah = himpunan yang diperiksa."""
    n = len(items)
    best_v, best_s = 0, []
    for mask in range(1 << n):
        w = sum(items[i][0] for i in range(n) if mask >> i & 1)
        v = sum(items[i][1] for i in range(n) if mask >> i & 1)
        if w <= cap and v > best_v:
            best_v, best_s = v, [i + 1 for i in range(n) if mask >> i & 1]
    return best_v, best_s, 1 << n


def greedy(items, cap, kriteria="rasio"):
    """Ambil barang menurut satu kriteria selama masih muat; langkah = barang diperiksa."""
    kunci = {
        "nilai": lambda i: -items[i][1],
        "berat": lambda i: items[i][0],
        "rasio": lambda i: -items[i][1] / items[i][0],
    }[kriteria]
    w = v = 0
    s = []
    for i in sorted(range(len(items)), key=kunci):
        if w + items[i][0] <= cap:
            w += items[i][0]
            v += items[i][1]
            s.append(i + 1)
    return v, sorted(s), len(items)


def _bound(i, w, v, its, cap):
    ub, sisa = v, cap - w
    while i < len(its) and its[i][0] <= sisa:
        sisa -= its[i][0]
        ub += its[i][1]
        i += 1
    if i < len(its):
        ub += its[i][1] * sisa / its[i][0]
    return ub


def branch_and_bound(items, cap):
    """Best-first dengan batas fractional knapsack; langkah = node yang dibuat."""
    order = sorted(range(len(items)), key=lambda k: items[k][1] / items[k][0], reverse=True)
    its = [items[k] for k in order]
    best_v, best_s, made = 0, [], 1
    heap = [(-_bound(0, 0, 0, its, cap), 0, 0, 0, [])]
    while heap:
        neg_ub, i, w, v, s = heapq.heappop(heap)
        if -neg_ub <= best_v or i == len(its):
            continue
        for take in (True, False):
            nw, nv = (w + its[i][0], v + its[i][1]) if take else (w, v)
            if nw > cap:
                continue
            ns = s + [order[i] + 1] if take else s
            made += 1
            if nv > best_v:
                best_v, best_s = nv, ns
            ub = _bound(i + 1, nw, nv, its, cap)
            if ub > best_v:
                heapq.heappush(heap, (-ub, i + 1, nw, nv, ns))
    return best_v, sorted(best_s), made


def branch_and_bound_dfs(items, cap):
    """Depth-first (backtracking + batas); langkah = node yang dikunjungi. Padanan versi Rust."""
    order = sorted(range(len(items)), key=lambda k: items[k][1] / items[k][0], reverse=True)
    its = [items[k] for k in order]
    best = [0, [], 0]

    def go(i, w, v, chosen):
        best[2] += 1
        if v > best[0]:
            best[0], best[1] = v, list(chosen)
        if i == len(its) or _bound(i, w, v, its, cap) <= best[0]:
            return  # daun, atau dipangkas oleh batas
        if w + its[i][0] <= cap:
            chosen.append(order[i] + 1)
            go(i + 1, w + its[i][0], v + its[i][1], chosen)
            chosen.pop()
        go(i + 1, w, v, chosen)

    go(0, 0, 0, [])
    return best[0], sorted(best[1]), best[2]


def dynamic_programming(items, cap):
    """Tabel V[i][w]; langkah = sel tabel yang diisi (n x (W+1))."""
    n = len(items)
    V = [[0] * (cap + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        wi, vi = items[i - 1]
        for w in range(cap + 1):
            V[i][w] = V[i - 1][w]
            if wi <= w and V[i - 1][w - wi] + vi > V[i][w]:
                V[i][w] = V[i - 1][w - wi] + vi
    s, w = [], cap  # telusur balik
    for i in range(n, 0, -1):
        if V[i][w] != V[i - 1][w]:
            s.append(i)
            w -= items[i - 1][0]
    return V[n][cap], sorted(s), n * (cap + 1)


def uji_silang(T=300, N=10, seed=27):
    """Algoritma 31.2: semua strategi eksak harus sama dengan brute force."""
    rnd = random.Random(seed)            # seed tetap: hasil dapat diulang
    for _ in range(T):
        n = rnd.randint(1, N)
        its = [(rnd.randint(1, 15), rnd.randint(1, 50)) for _ in range(n)]
        cap = rnd.randint(1, 40)
        b = brute_force(its, cap)[0]
        assert branch_and_bound(its, cap)[0] == b, (its, cap)
        assert branch_and_bound_dfs(its, cap)[0] == b, (its, cap)
        assert dynamic_programming(its, cap)[0] == b, (its, cap)
        assert greedy(its, cap, "rasio")[0] <= b, (its, cap)
    return True


def acak(n, seed, skala=1):
    rnd = random.Random(seed)
    its = [(rnd.randint(1, 30), rnd.randint(1, 60)) for _ in range(n)]
    cap = sum(w for w, _ in its) // 2
    return [(w * skala, v) for w, v in its], cap * skala


def rasio_sama(n, seed):
    """Nilai = berat (semua rasio sama), berat genap, kapasitas ganjil: batas tidak membantu."""
    rnd = random.Random(seed)
    its = [(w, w) for w in (2 * rnd.randint(1, 50) for _ in range(n))]
    return its, sum(w for w, _ in its) // 2 | 1


if __name__ == "__main__":
    print("Instance bersama, W =", W)
    hasil = {
        "brute force": brute_force(ITEMS, W),
        "greedy nilai": greedy(ITEMS, W, "nilai"),
        "greedy berat": greedy(ITEMS, W, "berat"),
        "greedy rasio": greedy(ITEMS, W, "rasio"),
        "branch and bound": branch_and_bound(ITEMS, W),
        "B&B depth-first": branch_and_bound_dfs(ITEMS, W),
        "dynamic programming": dynamic_programming(ITEMS, W),
    }
    for nama, (v, s, langkah) in hasil.items():
        print("%-20s nilai=%3d barang=%s langkah=%d" % (nama, v, s, langkah))
        assert v == 90 and s == [2, 4]

    assert uji_silang()
    print("uji silang 300 instance: lolos")

    # varian: barang 3 diganti (7, 63); greedy rasio gagal
    VAR = [(5, 10), (4, 40), (7, 63), (3, 50)]
    print("Varian:", greedy(VAR, W, "rasio"), brute_force(VAR, W))
    assert greedy(VAR, W, "rasio")[0] == 90 and brute_force(VAR, W)[0] == 113

    # pertumbuhan banyak langkah pada instance acak
    print("n  2^n  node_BnB  sel_DP  optimum  greedy_rasio")
    for n in (10, 20, 30, 40):
        its, cap = acak(n, seed=n)
        v1, _, nb = branch_and_bound(its, cap)
        v2, _, nd = dynamic_programming(its, cap)
        assert v1 == v2 == branch_and_bound_dfs(its, cap)[0]
        if n <= 20:
            assert brute_force(its, cap)[0] == v1
        print(n, 2 ** n, nb, nd, v1, greedy(its, cap, "rasio")[0])
    # berat dikali 1000: DP membengkak, B&B tidak berubah
    its, cap = acak(20, seed=20, skala=1000)
    print("skala 1000:", branch_and_bound(its, cap)[2], "node B&B;",
          len(its) * (cap + 1), "sel DP")
    # instance rasio sama: B&B mendekati 2^n, DP tetap kecil
    print("rasio sama: n  2^n  node_BnB  sel_DP")
    for n in (8, 12, 16, 20):
        its, cap = rasio_sama(n, seed=n)
        v1, _, nb = branch_and_bound(its, cap)
        v2, _, nd = dynamic_programming(its, cap)
        assert v1 == v2
        print(n, 2 ** n, nb, nd)
    print("semua uji lolos")
