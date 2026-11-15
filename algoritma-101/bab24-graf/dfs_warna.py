"""DFS tiga warna pada graf berarah: deteksi cycle dan topological sort
(Algoritma 24.3, Kode 24.4).

PUTIH = belum ditemukan, ABU = sedang di call stack, HITAM = selesai.
Edge ke vertex ABU adalah back edge, tanda ada cycle. Urutan selesai
yang dibalik adalah topological sort bila tidak ada cycle.
"""
PUTIH, ABU, HITAM = 0, 1, 2


def dfs_warna(vertex, adj):
    warna = {v: PUTIH for v in vertex}
    hasil, ada_cycle = [], False

    def kunjungi(u):
        nonlocal ada_cycle
        warna[u] = ABU
        for v in adj[u]:
            if warna[v] == ABU:          # back edge
                ada_cycle = True
            elif warna[v] == PUTIH:
                kunjungi(v)
        warna[u] = HITAM
        hasil.append(u)                  # urutan selesai

    for v in vertex:
        if warna[v] == PUTIH:
            kunjungi(v)
    return None if ada_cycle else hasil[::-1]


if __name__ == "__main__":
    paket = ["json", "http", "db", "web", "app"]
    adj = {"json": ["http", "db"], "http": ["web"], "db": ["app"],
           "web": ["app"], "app": []}
    urut = dfs_warna(paket, adj)
    assert urut == ["json", "db", "http", "web", "app"], urut
    pos = {v: i for i, v in enumerate(urut)}
    assert all(pos[u] < pos[v] for u in adj for v in adj[u])
    assert dfs_warna(["a", "b", "c"], {"a": ["b"], "b": ["c"], "c": ["a"]}) is None
    # graf berarah Gambar 20.3(a) (Bab 20) punya cycle Q -> S -> Q
    g = {"P": ["Q", "R"], "Q": ["S"], "R": ["S"], "S": ["Q"]}
    assert dfs_warna(list("PQRS"), g) is None
    # tanpa edge S -> Q graf itu DAG
    g["S"] = []
    assert dfs_warna(list("PQRS"), g) == ["P", "R", "Q", "S"]
    print("dfs_warna.py:", urut, "semua uji lolos")
