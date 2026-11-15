"""ADT graf dengan adjacency list berbasis dict of set (Subbab 20.4, Kode 20.2).

Graf tak berarah secara bawaan; berarah=True untuk graf berarah.
tetangga() mengembalikan list terurut agar hasil di buku selalu sama.
"""


class Graf:
    def __init__(self, berarah=False):
        self.berarah = berarah
        self.adj = {}                       # vertex -> set tetangga

    def tambah_vertex(self, v):
        self.adj.setdefault(v, set())

    def tambah_edge(self, u, v):
        self.tambah_vertex(u)
        self.tambah_vertex(v)
        self.adj[u].add(v)
        if not self.berarah:
            self.adj[v].add(u)

    def hapus_edge(self, u, v):
        self.adj[u].discard(v)
        if not self.berarah:
            self.adj[v].discard(u)

    def hapus_vertex(self, v):
        for u in self.adj:                  # buang semua edge ke v
            self.adj[u].discard(v)
        del self.adj[v]

    def ada_edge(self, u, v):
        return u in self.adj and v in self.adj[u]

    def tetangga(self, u):
        return sorted(self.adj[u])

    def derajat(self, u):                   # out-degree bila berarah
        return len(self.adj[u])

    def banyak_edge(self):
        total = sum(len(s) for s in self.adj.values())
        return total if self.berarah else total // 2


def in_degree(g, v):
    return sum(1 for u in g.adj if v in g.adj[u])


if __name__ == "__main__":
    g = Graf()
    for u, v in [("A", "B"), ("A", "C"), ("B", "D"), ("B", "E"),
                 ("C", "F"), ("E", "F"), ("F", "G")]:
        g.tambah_edge(u, v)
    assert len(g.adj) == 7 and g.banyak_edge() == 7
    assert g.tetangga("B") == ["A", "D", "E"]
    assert g.ada_edge("F", "E") and g.ada_edge("E", "F")
    assert not g.ada_edge("A", "G")
    g.hapus_edge("E", "F")
    assert not g.ada_edge("F", "E") and g.banyak_edge() == 6
    g.hapus_vertex("G")
    assert "G" not in g.adj and g.tetangga("F") == ["C"]
    assert g.banyak_edge() == 5

    # graf berarah Gambar 20.3(a): P->Q, Q->S, P->R, R->S, S->Q
    h = Graf(berarah=True)
    for u, v in [("P", "Q"), ("Q", "S"), ("P", "R"), ("R", "S"), ("S", "Q")]:
        h.tambah_edge(u, v)
    assert h.ada_edge("S", "Q") and h.ada_edge("Q", "S")
    assert not h.ada_edge("Q", "P")
    out = {v: h.derajat(v) for v in "PQRS"}
    inn = {v: in_degree(h, v) for v in "PQRS"}
    assert out == {"P": 2, "Q": 1, "R": 1, "S": 1}
    assert inn == {"P": 0, "Q": 2, "R": 1, "S": 2}
    assert sum(out.values()) == sum(inn.values()) == h.banyak_edge() == 5
    print("graf_adt.py: semua uji lolos")
