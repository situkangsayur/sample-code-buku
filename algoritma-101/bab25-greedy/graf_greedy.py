"""Dijkstra, Prim, dan Kruskal pada graf berbobot Gambar 23.2(b)
(Algoritma 25.5-22.6, Kode 25.3 dan 22.5)."""
import heapq

SISI = [("A", "B", 4), ("A", "C", 2), ("B", "C", 1), ("B", "D", 5),
        ("C", "D", 8), ("C", "E", 10), ("D", "E", 2), ("D", "F", 6),
        ("E", "F", 3)]


def adjacency(sisi):
    adj = {}
    for u, v, w in sisi:
        adj.setdefault(u, []).append((v, w))
        adj.setdefault(v, []).append((u, w))   # tak berarah
    return adj


def dijkstra(adj, s):
    """Versi lazy: entri lama di heap dilewati saat diambil.
    Mengembalikan jarak, parent, dan urutan simpul yang difinalkan."""
    jarak = {v: float("inf") for v in adj}
    parent = {v: None for v in adj}
    jarak[s] = 0
    heap = [(0, s)]
    selesai, urutan = set(), []
    while heap:
        d, u = heapq.heappop(heap)
        if u in selesai:
            continue                       # entri basi
        selesai.add(u)
        urutan.append((u, d))
        for v, w in adj[u]:
            if d + w < jarak[v]:           # relaksasi
                jarak[v] = d + w
                parent[v] = u
                heapq.heappush(heap, (jarak[v], v))
    return jarak, parent, urutan


def prim(adj, s):
    """Mengembalikan daftar sisi MST dan total bobotnya."""
    di_tree = {s}
    heap = [(w, s, v) for v, w in adj[s]]
    heapq.heapify(heap)
    mst, total = [], 0
    while heap and len(di_tree) < len(adj):
        w, u, v = heapq.heappop(heap)
        if v in di_tree:
            continue
        di_tree.add(v)
        mst.append((u, v, w))
        total += w
        for x, wx in adj[v]:
            if x not in di_tree:
                heapq.heappush(heap, (wx, v, x))
    return mst, total


class UnionFind:
    def __init__(self, elemen):
        self.induk = {x: x for x in elemen}
        self.ukuran = {x: 1 for x in elemen}

    def find(self, x):
        while self.induk[x] != x:
            self.induk[x] = self.induk[self.induk[x]]   # path halving
            x = self.induk[x]
        return x

    def union(self, a, b):
        ra, rb = self.find(a), self.find(b)
        if ra == rb:
            return False                   # sudah satu komponen: siklus
        if self.ukuran[ra] < self.ukuran[rb]:
            ra, rb = rb, ra
        self.induk[rb] = ra
        self.ukuran[ra] += self.ukuran[rb]
        return True


def kruskal(simpul, sisi):
    uf = UnionFind(simpul)
    mst, total, ditolak = [], 0, []
    for u, v, w in sorted(sisi, key=lambda e: e[2]):
        if uf.union(u, v):
            mst.append((u, v, w))
            total += w
        else:
            ditolak.append((u, v, w))
    return mst, total, ditolak


if __name__ == "__main__":
    adj = adjacency(SISI)
    jarak, parent, urutan = dijkstra(adj, "A")
    assert jarak == {"A": 0, "B": 3, "C": 2, "D": 8, "E": 10, "F": 13}
    assert [u for u, _ in urutan] == ["A", "C", "B", "D", "E", "F"]
    # jalur terpendek A -> F
    t, rute = "F", []
    while t is not None:
        rute.append(t)
        t = parent[t]
    assert rute[::-1] == ["A", "C", "B", "D", "E", "F"]

    mst, total = prim(adj, "A")
    assert total == 13 and len(mst) == 5
    assert mst == [("A", "C", 2), ("C", "B", 1), ("B", "D", 5),
                   ("D", "E", 2), ("E", "F", 3)]
    mst_k, total_k, tolak = kruskal(sorted(adj), SISI)
    assert total_k == 13
    assert [(u, v) for u, v, _ in mst_k] == [("B", "C"), ("A", "C"), ("D", "E"),
                                             ("E", "F"), ("B", "D")]
    assert ("A", "B", 4) in tolak

    # Dijkstra gagal dengan bobot negatif (graf berarah kecil, Subbab 22.5)
    g = {"S": [("A", 2), ("B", 3)], "A": [("C", 1)], "B": [("A", -2)], "C": []}
    jarak_neg, _, urut_neg = dijkstra(g, "S")
    # A difinalkan dengan jarak 2, lalu C = 3. Jalur benar S-B-A-C = 2.
    assert [u for u, _ in urut_neg] == ["S", "A", "B", "C"]
    assert jarak_neg["C"] == 3
    print("Dijkstra:", urutan)
    print("graf_greedy.py: semua uji lolos")
