"""Floyd-Warshall: jarak terpendek semua pasangan simpul.

Bab 29 buku Algoritma 101, Algoritma 29.8.
"""

INF = float("inf")


def floyd_warshall(w):
    """w adalah adjacency matrix n x n; INF bila tidak ada sisi.

    Setelah putaran k, d[i][j] adalah jarak terpendek dari i ke j
    yang simpul perantaranya hanya boleh dari {0, ..., k}.
    """
    n = len(w)
    d = [baris[:] for baris in w]
    for k in range(n):
        for i in range(n):
            for j in range(n):
                if d[i][k] + d[k][j] < d[i][j]:
                    d[i][j] = d[i][k] + d[k][j]
    return d


def ada_siklus_negatif(d):
    return any(d[i][i] < 0 for i in range(len(d)))


if __name__ == "__main__":
    # graf Gambar 29.5: simpul 1..4 di buku = indeks 0..3 di sini
    w = [[0, 3, INF, 7],
         [8, 0, 2, INF],
         [5, INF, 0, 1],
         [2, INF, INF, 0]]
    d = floyd_warshall(w)
    for baris in d:
        print(baris)
    assert d == [[0, 3, 5, 6],
                 [5, 0, 2, 3],
                 [3, 6, 0, 1],
                 [2, 5, 7, 0]]
    assert not ada_siklus_negatif(d)
    neg = [[0, 1], [-3, 0]]
    assert ada_siklus_negatif(floyd_warshall(neg))
    print("semua uji lolos")
