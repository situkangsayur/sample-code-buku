"""BFS dan DFS pada adjacency list (Algoritma 23.1 dan 20.2, Kode 23.2)."""
from collections import deque

from graf_representasi import SIMPUL, SISI, adjacency_list


def bfs(adj, s):
    """Mengembalikan urutan kunjungan, jarak (banyak sisi), dan parent."""
    jarak = {s: 0}
    parent = {s: None}
    urutan = []
    q = deque([s])
    while q:
        u = q.popleft()
        urutan.append(u)
        for v in adj[u]:
            if v not in jarak:          # belum pernah ditemukan
                jarak[v] = jarak[u] + 1
                parent[v] = u
                q.append(v)
    return urutan, jarak, parent


def jalur(parent, t):
    """Menyusun jalur s -> t dari tabel parent."""
    hasil = []
    while t is not None:
        hasil.append(t)
        t = parent[t]
    return hasil[::-1]


def dfs(adj, s, dikunjungi=None, urutan=None):
    """DFS rekursif."""
    if dikunjungi is None:
        dikunjungi, urutan = set(), []
    dikunjungi.add(s)
    urutan.append(s)
    for v in adj[s]:
        if v not in dikunjungi:
            dfs(adj, v, dikunjungi, urutan)
    return urutan


def dfs_iteratif(adj, s):
    """DFS dengan stack eksplisit; tetangga dimasukkan terbalik agar
    urutannya sama dengan versi rekursif."""
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


def banyak_komponen(adj):
    dikunjungi = set()
    k = 0
    for v in adj:
        if v not in dikunjungi:
            k += 1
            dikunjungi.update(bfs(adj, v)[0])
    return k


if __name__ == "__main__":
    adj = adjacency_list(SIMPUL, SISI)
    urutan, jarak, parent = bfs(adj, "A")
    assert urutan == ["A", "B", "C", "D", "E", "F", "G"]
    assert jarak == {"A": 0, "B": 1, "C": 1, "D": 2, "E": 2, "F": 2, "G": 3}
    assert jalur(parent, "G") == ["A", "C", "F", "G"]
    assert dfs(adj, "A") == ["A", "B", "D", "E", "F", "C", "G"]
    assert dfs_iteratif(adj, "A") == dfs(adj, "A")
    assert banyak_komponen(adj) == 1
    adj2 = adjacency_list(SIMPUL + ["H", "I"], SISI + [("H", "I")])
    assert banyak_komponen(adj2) == 2
    print("BFS:", urutan, jarak)
    print("DFS:", dfs(adj, "A"))
    print("bfs_dfs.py: semua uji lolos")
