"""Bab 37: HNSW mini (Malkov dan Yashunin, 2020) untuk vector search.

Setiap vektor diberi level acak l = floor(-ln(U) * mL), mL = 1/ln(M).
Layer atas jarang dan dipakai untuk melompat jauh; layer 0 berisi semua.
Pencarian: greedy dari entry point di layer teratas, turun layer demi
layer, lalu beam search selebar ef di layer 0.
Seleksi tetangga memakai M terdekat (versi sederhana, tanpa heuristik).
"""
import heapq
import math
import random


HITUNG = [0]                                       # banyak perhitungan jarak


def jarak(a, b):
    HITUNG[0] += 1
    return math.dist(a, b)                         # Euclid


class HNSW:
    def __init__(self, M=8, ef_construction=64, seed=36):
        self.M, self.M0 = M, 2 * M                 # layer 0 boleh 2M tetangga
        self.ef_c = ef_construction
        self.mL = 1 / math.log(M)
        self.rng = random.Random(seed)
        self.data, self.graf = [], []              # graf[i][layer] = set tetangga
        self.entry, self.top = None, -1

    def _search_layer(self, q, masuk, ef, layer):
        dikunjungi = set(masuk)
        calon = [(jarak(q, self.data[e]), e) for e in masuk]   # min-heap
        hasil = [(-d, e) for d, e in calon]                    # max-heap (negatif)
        heapq.heapify(calon)
        heapq.heapify(hasil)
        while calon:
            d, c = heapq.heappop(calon)
            if d > -hasil[0][0]:
                break                              # calon terdekat lebih jauh dari hasil terjauh
            for e in self.graf[c][layer]:
                if e in dikunjungi:
                    continue
                dikunjungi.add(e)
                de = jarak(q, self.data[e])
                if len(hasil) < ef or de < -hasil[0][0]:
                    heapq.heappush(calon, (de, e))
                    heapq.heappush(hasil, (-de, e))
                    if len(hasil) > ef:
                        heapq.heappop(hasil)
        return sorted((-d, e) for d, e in hasil)

    def insert(self, v):
        i = len(self.data)
        self.data.append(v)
        level = int(-math.log(1 - self.rng.random()) * self.mL)
        self.graf.append([set() for _ in range(level + 1)])
        if self.entry is None:
            self.entry, self.top = i, level
            return
        ep = [self.entry]
        for lc in range(self.top, level, -1):      # turun greedy (ef = 1)
            ep = [self._search_layer(v, ep, 1, lc)[0][1]]
        for lc in range(min(self.top, level), -1, -1):
            dekat = self._search_layer(v, ep, self.ef_c, lc)
            batas = self.M0 if lc == 0 else self.M
            for _, e in dekat[:self.M]:
                self.graf[i][lc].add(e)
                self.graf[e][lc].add(i)
                if len(self.graf[e][lc]) > batas:  # pangkas tetangga terjauh
                    terjauh = max(self.graf[e][lc], key=lambda x: jarak(self.data[e], self.data[x]))
                    self.graf[e][lc].discard(terjauh)
            ep = [e for _, e in dekat]
        if level > self.top:
            self.entry, self.top = i, level

    def search(self, q, k=10, ef=50):
        ep = [self.entry]
        for lc in range(self.top, 0, -1):
            ep = [self._search_layer(q, ep, 1, lc)[0][1]]
        return [e for _, e in self._search_layer(q, ep, max(ef, k), 0)[:k]]


def brute_force(data, q, k):
    return sorted(range(len(data)), key=lambda i: jarak(q, data[i]))[:k]


if __name__ == "__main__":
    rng = random.Random(2020)
    dim, n = 8, 2000
    data = [[rng.random() for _ in range(dim)] for _ in range(n)]
    h = HNSW(M=8, ef_construction=64)
    for v in data:
        h.insert(v)
    per_level = {}
    for g in h.graf:
        per_level[len(g) - 1] = per_level.get(len(g) - 1, 0) + 1
    print("banyak node per level teratas:", dict(sorted(per_level.items())))
    assert per_level[0] > n // 2                   # sebagian besar hanya di layer 0

    query = [[rng.random() for _ in range(dim)] for _ in range(50)]
    benar = [set(brute_force(data, q, 10)) for q in query]
    for ef in (10, 50):
        HITUNG[0], recall = 0, 0.0
        for q, b in zip(query, benar):
            recall += len(b & set(h.search(q, k=10, ef=ef))) / 10
        recall /= len(query)
        print("ef = %2d: recall@10 = %.3f, rata-rata %d jarak per query (brute force %d)"
              % (ef, recall, HITUNG[0] // len(query), n))
        assert HITUNG[0] // len(query) < n
    assert recall >= 0.9
    print("hnsw_mini: semua uji lolos")
