"""Edge list, adjacency matrix, dan adjacency list (Subbab 20.3, Kode 20.1).

Graf contoh Gambar 20.2: tujuh vertex A..G, tak berarah, tujuh edge.
"""

VERTEX = ["A", "B", "C", "D", "E", "F", "G"]
EDGE = [("A", "B"), ("A", "C"), ("B", "D"), ("B", "E"),
        ("C", "F"), ("E", "F"), ("F", "G")]          # edge list


def adjacency_matrix(vertex, edge):
    idx = {v: i for i, v in enumerate(vertex)}
    n = len(vertex)
    M = [[0] * n for _ in range(n)]
    for u, v in edge:
        M[idx[u]][idx[v]] = 1
        M[idx[v]][idx[u]] = 1      # tak berarah: simetris
    return M


def adjacency_list(vertex, edge):
    adj = {v: [] for v in vertex}
    for u, v in edge:
        adj[u].append(v)
        adj[v].append(u)           # tak berarah: catat di kedua ujung
    for v in adj:
        adj[v].sort()              # urut abjad agar hasil BFS/DFS tetap
    return adj


def ada_edge_list(edge, u, v):
    """Cek edge pada edge list: harus memindai semua edge, O(|E|)."""
    return any((a, b) in ((u, v), (v, u)) for a, b in edge)


if __name__ == "__main__":
    M = adjacency_matrix(VERTEX, EDGE)
    adj = adjacency_list(VERTEX, EDGE)
    assert M[0] == [0, 1, 1, 0, 0, 0, 0]          # baris A
    assert all(M[i][j] == M[j][i] for i in range(7) for j in range(7))
    assert adj["F"] == ["C", "E", "G"]
    # jumlah derajat = 2 x banyak edge (handshaking lemma)
    assert sum(len(t) for t in adj.values()) == 2 * len(EDGE)
    assert sum(map(sum, M)) == 2 * len(EDGE)
    assert [len(adj[v]) for v in VERTEX] == [2, 3, 2, 1, 2, 3, 1]
    assert ada_edge_list(EDGE, "F", "E") and not ada_edge_list(EDGE, "A", "G")
    for v in VERTEX:
        print(v, adj[v])
    print("graf_representasi.py: semua uji lolos")
