"""Bab 40: approximate nearest neighbor dengan greedy search di graf (satu lapis HNSW).

Graf k-NN dibangun brute force (O(n^2), hanya untuk contoh). Pencarian memakai
beam berukuran ef seperti lapis paling bawah HNSW (Malkov dan Yashunin 2020).
Jalankan: python3 ann_graph.py
"""
import heapq
import math

MASK64 = (1 << 64) - 1


class SplitMix64:
    """Pembangkit bilangan acak kecil yang sama persis dengan versi Rust."""

    def __init__(self, seed):
        self.s = seed & MASK64

    def next(self):
        self.s = (self.s + 0x9E3779B97F4A7C15) & MASK64
        z = self.s
        z = ((z ^ (z >> 30)) * 0xBF58476D1CE4E5B9) & MASK64
        z = ((z ^ (z >> 27)) * 0x94D049BB133111EB) & MASK64
        return z ^ (z >> 31)

    def uniform(self):
        return (self.next() >> 11) / float(1 << 53)


def dist(a, b):
    return math.sqrt(sum((x - y) ** 2 for x, y in zip(a, b)))


def make_points(n, dim, rng):
    return [[rng.uniform() for _ in range(dim)] for _ in range(n)]


def build_knn_graph(points, k):
    graph = []
    for i, p in enumerate(points):
        nb = sorted((dist(p, q), j) for j, q in enumerate(points) if j != i)[:k]
        graph.append([j for _, j in nb])
    # jadikan tidak berarah supaya graf lebih mudah dinavigasi
    for i in range(len(points)):
        for j in list(graph[i]):
            if i not in graph[j]:
                graph[j].append(i)
    return graph


def greedy_search(points, graph, query, entry, ef, k):
    """Beam search: candidates (min-heap) dan results (max-heap, ukuran ef)."""
    evals = 1
    d0 = dist(points[entry], query)
    visited = {entry}
    candidates = [(d0, entry)]
    results = [(-d0, entry)]
    while candidates:
        d, c = heapq.heappop(candidates)
        if d > -results[0][0]:
            break  # kandidat terdekat sudah lebih jauh dari hasil terjauh
        for nb in graph[c]:
            if nb in visited:
                continue
            visited.add(nb)
            dn = dist(points[nb], query)
            evals += 1
            if len(results) < ef or dn < -results[0][0]:
                heapq.heappush(candidates, (dn, nb))
                heapq.heappush(results, (-dn, nb))
                if len(results) > ef:
                    heapq.heappop(results)
    best = sorted((-d, i) for d, i in results)[:k]
    return [i for _, i in best], evals


def brute_force(points, query, k):
    return [i for _, i in sorted((dist(p, query), i) for i, p in enumerate(points))[:k]]


if __name__ == "__main__":
    rng = SplitMix64(38)
    n, dim, k = 2000, 16, 10
    pts = make_points(n, dim, rng)
    graph = build_knn_graph(pts, k=8)
    queries = make_points(50, dim, rng)
    print(f"n = {n}, dimensi = {dim}, brute force = {n} jarak per query")
    prev = 0.0
    for ef in (10, 20, 50, 100):
        hit, ev = 0, 0
        for q in queries:
            exact = set(brute_force(pts, q, k))
            got, e = greedy_search(pts, graph, q, entry=0, ef=ef, k=k)
            hit += len(exact & set(got))
            ev += e
        recall = hit / (k * len(queries))
        print(f"ef = {ef:3d}: recall@10 = {recall:.3f}, rata-rata jarak dihitung = {ev / len(queries):.0f}")
        assert recall >= prev - 1e-9  # ef lebih besar tidak menurunkan recall pada data ini
        prev = recall
    assert prev > 0.99
    print("semua uji ann_graph lolos")
