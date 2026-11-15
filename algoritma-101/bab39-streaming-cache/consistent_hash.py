"""Bab 39: consistent hashing (Karger dkk. 1997) dengan virtual node.

Jalankan: python3 consistent_hash.py
"""
from bisect import bisect_right

MASK64 = (1 << 64) - 1


def fnv1a64(data: bytes) -> int:
    h = 0xCBF29CE484222325
    for b in data:
        h ^= b
        h = (h * 0x100000001B3) & MASK64
    return h


def mix64(x: int) -> int:
    x ^= x >> 30
    x = (x * 0xBF58476D1CE4E5B9) & MASK64
    x ^= x >> 27
    x = (x * 0x94D049BB133111EB) & MASK64
    x ^= x >> 31
    return x


def h64(s: str) -> int:
    return mix64(fnv1a64(s.encode()))


class Ring:
    def __init__(self, nodes, vnodes=100):
        self.vnodes = vnodes
        self.points = []  # list terurut pasangan (posisi, node)
        for n in nodes:
            self.add(n)

    def add(self, node):
        for i in range(self.vnodes):
            self.points.append((h64(f"{node}#{i}"), node))
        self.points.sort()

    def remove(self, node):
        self.points = [pt for pt in self.points if pt[1] != node]

    def lookup(self, key):
        """Node pertama searah jarum jam dari posisi key: O(log V) dengan binary search."""
        pos = h64(key)
        i = bisect_right(self.points, (pos, chr(0x10FFFF)))
        if i == len(self.points):
            i = 0  # memutar ke awal ring
        return self.points[i][1]


def mod_n(key, nodes):
    return nodes[h64(key) % len(nodes)]


if __name__ == "__main__":
    keys = [f"sesi:{i}" for i in range(10_000)]
    old_nodes = ["cache-A", "cache-B", "cache-C", "cache-D"]
    new_nodes = old_nodes + ["cache-E"]

    moved_mod = sum(mod_n(k, old_nodes) != mod_n(k, new_nodes) for k in keys)

    ring = Ring(old_nodes, vnodes=100)
    before = {k: ring.lookup(k) for k in keys}
    ring.add("cache-E")
    after = {k: ring.lookup(k) for k in keys}
    moved_ring = sum(before[k] != after[k] for k in keys)
    # key yang pindah pada ring hanya pindah ke node baru
    assert all(after[k] == "cache-E" for k in keys if before[k] != after[k])

    print(f"hash mod N : {moved_mod} dari {len(keys)} key pindah ({moved_mod / 100:.1f}%)")
    print(f"ring 100 vn: {moved_ring} dari {len(keys)} key pindah ({moved_ring / 100:.1f}%)")
    assert moved_mod > 7000 and moved_ring < 3000

    # sebaran beban per node dengan sedikit dan banyak virtual node
    for v in (1, 10, 100):
        r = Ring(old_nodes, vnodes=v)
        load = {n: 0 for n in old_nodes}
        for k in keys:
            load[r.lookup(k)] += 1
        print(f"vnodes = {v:>3}: beban = {sorted(load.values())}")
    print("semua uji consistent_hash lolos")
