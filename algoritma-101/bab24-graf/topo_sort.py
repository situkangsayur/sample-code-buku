"""Topological sort dengan algoritma Kahn (Algoritma 24.2, Kode 24.3).

Sisi u -> v berarti u harus dikerjakan sebelum v
(mis. paket v bergantung pada paket u).
"""
from collections import deque


def topo_kahn(simpul, sisi):
    masuk = {v: 0 for v in simpul}       # in-degree
    adj = {v: [] for v in simpul}
    for u, v in sisi:
        adj[u].append(v)
        masuk[v] += 1
    q = deque(sorted(v for v in simpul if masuk[v] == 0))
    hasil = []
    while q:
        u = q.popleft()
        hasil.append(u)
        for v in adj[u]:
            masuk[v] -= 1
            if masuk[v] == 0:
                q.append(v)
    if len(hasil) < len(simpul):
        return None                       # ada siklus
    return hasil


if __name__ == "__main__":
    paket = ["json", "http", "db", "web", "app"]
    butuh = [("json", "http"), ("json", "db"), ("http", "web"),
             ("db", "app"), ("web", "app")]
    urut = topo_kahn(paket, butuh)
    assert urut == ["json", "http", "db", "web", "app"], urut
    pos = {v: i for i, v in enumerate(urut)}
    assert all(pos[u] < pos[v] for u, v in butuh)
    # siklus: a -> b -> c -> a tidak punya urutan
    assert topo_kahn(["a", "b", "c"], [("a", "b"), ("b", "c"), ("c", "a")]) is None
    print("topo_sort.py:", urut, "semua uji lolos")
