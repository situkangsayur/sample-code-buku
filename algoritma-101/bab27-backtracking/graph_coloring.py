"""Bab 27: pewarnaan graf dengan m warna (Algoritma 27.4; versi Rust di Kode 27.4).

Simpul 0..n-1 di Python; di buku simpul diberi nama A..E.
warna 1..m, 0 berarti belum diwarnai.
"""


def color_graph(adj, m, all_solutions=False):
    n = len(adj)
    color = [0] * n
    out = []

    def safe(v, c):
        return all(color[u] != c for u in adj[v])

    def go(v):
        if v == n:
            out.append(color[:])
            return not all_solutions        # True: berhenti di solusi pertama
        for c in range(1, m + 1):
            if safe(v, c):
                color[v] = c
                if go(v + 1):
                    return True
                color[v] = 0                # undo
        return False

    go(0)
    return out


# Graf Gambar 27.5: A-B, A-C, B-C, B-E, C-D, C-E, D-E
EDGES = [(0, 1), (0, 2), (1, 2), (1, 4), (2, 3), (2, 4), (3, 4)]


def build(n, edges):
    adj = [[] for _ in range(n)]
    for u, v in edges:
        adj[u].append(v)
        adj[v].append(u)
    return adj


def chromatic_number(adj):
    m = 1
    while not color_graph(adj, m):
        m += 1
    return m


if __name__ == "__main__":
    adj = build(5, EDGES)
    first = color_graph(adj, 3)
    print("pewarnaan pertama:", first[0])
    assert first[0] == [1, 2, 3, 2, 1]
    assert color_graph(adj, 2) == []
    print("banyak pewarnaan 3 warna:", len(color_graph(adj, 3, True)))
    assert len(color_graph(adj, 3, True)) == 6
    assert chromatic_number(adj) == 3
    # graf lengkap K4 butuh 4 warna
    k4 = build(4, [(a, b) for a in range(4) for b in range(a + 1, 4)])
    assert chromatic_number(k4) == 4
    print("semua uji lolos")
