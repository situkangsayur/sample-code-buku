"""Menelusuri graf: BFS dan DFS dasar (Algoritma 20.1-20.2, Kode 20.4).

Hanya urutan kunjungan. Jarak, parent, komponen, dan topological sort
ada di Bab 24 (folder bab24-graf).
"""
from collections import deque

from graf_representasi import VERTEX, EDGE, adjacency_list


def bfs(adj, s):
    ditemukan = {s}
    urutan = []
    q = deque([s])
    while q:
        u = q.popleft()
        urutan.append(u)                 # kunjungi u
        for v in adj[u]:
            if v not in ditemukan:       # tandai saat ditemukan
                ditemukan.add(v)
                q.append(v)
    return urutan


def dfs(adj, u, dikunjungi=None, urutan=None):
    if dikunjungi is None:
        dikunjungi, urutan = set(), []
    dikunjungi.add(u)
    urutan.append(u)                     # kunjungi u
    for v in adj[u]:
        if v not in dikunjungi:
            dfs(adj, v, dikunjungi, urutan)
    return urutan


def dfs_iteratif(adj, s):
    """Stack eksplisit; tetangga dimasukkan terbalik agar urutannya
    sama dengan versi rekursif."""
    dikunjungi, urutan = set(), []
    stack = [s]
    while stack:
        u = stack.pop()
        if u in dikunjungi:
            continue
        dikunjungi.add(u)
        urutan.append(u)
        for v in reversed(adj[u]):
            if v not in dikunjungi:
                stack.append(v)
    return urutan


def dfs_postorder(adj, u, dikunjungi=None, selesai=None):
    if dikunjungi is None:
        dikunjungi, selesai = set(), []
    dikunjungi.add(u)
    for v in adj[u]:
        if v not in dikunjungi:
            dfs_postorder(adj, v, dikunjungi, selesai)
    selesai.append(u)
    return selesai


if __name__ == "__main__":
    adj = adjacency_list(VERTEX, EDGE)
    assert bfs(adj, "A") == ["A", "B", "C", "D", "E", "F", "G"]
    assert dfs(adj, "A") == ["A", "B", "D", "E", "F", "C", "G"]
    assert dfs_iteratif(adj, "A") == dfs(adj, "A")
    assert dfs_postorder(adj, "A") == ["D", "C", "G", "F", "E", "B", "A"]
    # latihan: BFS dan DFS dari D dan dari G
    assert bfs(adj, "D") == ["D", "B", "A", "E", "C", "F", "G"]
    assert dfs(adj, "G") == ["G", "F", "C", "A", "B", "D", "E"]
    assert dfs_postorder(adj, "G") == ["D", "E", "B", "A", "C", "F", "G"]
    # graf tidak terhubung: BFS dari A tidak mencapai H dan I
    adj2 = adjacency_list(VERTEX + ["H", "I"], EDGE + [("H", "I")])
    assert set(bfs(adj2, "A")) == set(VERTEX)
    # rantai panjang: versi iteratif aman, versi rekursif melampaui batas
    n = 100_000
    rantai = {i: [j for j in (i - 1, i + 1) if 0 <= j < n] for i in range(n)}
    assert len(dfs_iteratif(rantai, 0)) == n
    try:
        dfs(rantai, 0)
        assert False, "seharusnya RecursionError"
    except RecursionError:
        pass
    print("BFS:", bfs(adj, "A"))
    print("DFS:", dfs(adj, "A"))
    print("telusur.py: semua uji lolos")
