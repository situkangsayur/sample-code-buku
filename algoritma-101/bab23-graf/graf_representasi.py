"""Adjacency matrix dan adjacency list (Subbab 20.2, Kode 23.1).

Graf contoh Gambar 23.1: tujuh simpul A..G, tak berarah.
"""

SIMPUL = ["A", "B", "C", "D", "E", "F", "G"]
SISI = [("A", "B"), ("A", "C"), ("B", "D"), ("B", "E"),
        ("C", "F"), ("E", "F"), ("F", "G")]


def adjacency_matrix(simpul, sisi):
    idx = {v: i for i, v in enumerate(simpul)}
    n = len(simpul)
    M = [[0] * n for _ in range(n)]
    for u, v in sisi:
        M[idx[u]][idx[v]] = 1
        M[idx[v]][idx[u]] = 1      # tak berarah: simetris
    return M


def adjacency_list(simpul, sisi):
    adj = {v: [] for v in simpul}
    for u, v in sisi:
        adj[u].append(v)
        adj[v].append(u)
    for v in adj:
        adj[v].sort()              # urut abjad agar hasil BFS/DFS tetap
    return adj


if __name__ == "__main__":
    M = adjacency_matrix(SIMPUL, SISI)
    adj = adjacency_list(SIMPUL, SISI)
    assert M[0] == [0, 1, 1, 0, 0, 0, 0]          # baris A
    assert all(M[i][j] == M[j][i] for i in range(7) for j in range(7))
    assert adj["F"] == ["C", "E", "G"]
    # jumlah derajat = 2 x banyak sisi (handshaking lemma)
    assert sum(len(t) for t in adj.values()) == 2 * len(SISI)
    assert sum(map(sum, M)) == 2 * len(SISI)
    for v in SIMPUL:
        print(v, adj[v])
    print("graf_representasi.py: semua uji lolos")
