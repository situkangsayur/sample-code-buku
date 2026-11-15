"""N-ary tree: list of children, traversal, first-child next-sibling, dan
indeks array untuk complete k-ary tree (Subbab N-ary Tree Bab 19).

Contoh: tree folder Gambar 19.2. Ukuran file dalam KB adalah angka rekaan.
"""
from collections import deque


class NodeNary:
    def __init__(self, nama, ukuran=0):
        self.nama = nama
        self.ukuran = ukuran      # ukuran file; folder = 0
        self.anak = []            # list of children, urut dari kiri

    def tambah_anak(self, node):
        self.anak.append(node)    # O(1) amortized
        return node


def preorder(node, kedalaman=0, hasil=None):
    """Kunjungi node, lalu setiap child dari kiri ke kanan."""
    if hasil is None:
        hasil = []
    hasil.append((kedalaman, node.nama))
    for c in node.anak:
        preorder(c, kedalaman + 1, hasil)
    return hasil


def postorder(node, hasil=None):
    """Kunjungi semua child lebih dulu, node paling akhir."""
    if hasil is None:
        hasil = []
    for c in node.anak:
        postorder(c, hasil)
    hasil.append(node.nama)
    return hasil


def total_ukuran(node):
    """Postorder: ukuran folder = ukuran sendiri + ukuran semua child."""
    return node.ukuran + sum(total_ukuran(c) for c in node.anak)


def level_order(akar):
    hasil, q = [], deque([akar])
    while q:
        u = q.popleft()
        hasil.append(u.nama)
        q.extend(u.anak)          # semua child masuk queue
    return hasil


def tinggi(node):
    if not node.anak:
        return 0
    return 1 + max(tinggi(c) for c in node.anak)


def ke_first_child_next_sibling(node):
    """Mengembalikan dict nama -> (first child, next sibling)."""
    hasil = {node.nama: (None, None)}

    def isi(u):
        fc = u.anak[0].nama if u.anak else None
        hasil[u.nama] = (fc, hasil.get(u.nama, (None, None))[1])
        for i, c in enumerate(u.anak):
            ns = u.anak[i + 1].nama if i + 1 < len(u.anak) else None
            hasil[c.nama] = (None, ns)
            isi(c)

    isi(node)
    return hasil


# Complete k-ary tree di array, indeks mulai 0 (Python dan Rust).
def anak_k(i, k):
    return list(range(k * i + 1, k * i + k + 1))


def parent_k(i, k):
    return (i - 1) // k


def contoh_folder():
    akar = NodeNary("/")
    home = akar.tambah_anak(NodeNary("home"))
    etc = akar.tambah_anak(NodeNary("etc"))
    bin_ = akar.tambah_anak(NodeNary("bin"))
    ani = home.tambah_anak(NodeNary("ani"))
    budi = home.tambah_anak(NodeNary("budi"))
    ani.tambah_anak(NodeNary("a.py", 3))
    ani.tambah_anak(NodeNary("b.txt", 5))
    budi.tambah_anak(NodeNary("c.pdf", 20))
    etc.tambah_anak(NodeNary("hosts", 1))
    for nama, kb in [("ls", 10), ("cp", 12), ("mv", 8)]:
        bin_.tambah_anak(NodeNary(nama, kb))
    return akar


if __name__ == "__main__":
    akar = contoh_folder()
    pre = [n for _, n in preorder(akar)]
    assert pre == ["/", "home", "ani", "a.py", "b.txt", "budi", "c.pdf",
                   "etc", "hosts", "bin", "ls", "cp", "mv"]
    assert postorder(akar) == ["a.py", "b.txt", "ani", "c.pdf", "budi", "home",
                               "hosts", "etc", "ls", "cp", "mv", "bin", "/"]
    assert level_order(akar) == ["/", "home", "etc", "bin", "ani", "budi",
                                 "hosts", "ls", "cp", "mv", "a.py", "b.txt", "c.pdf"]
    assert total_ukuran(akar) == 59
    assert total_ukuran(akar.anak[0]) == 28          # home
    assert tinggi(akar) == 3
    assert len(akar.anak) == 3                       # degree root
    fcns = ke_first_child_next_sibling(akar)
    assert fcns["/"] == ("home", None)
    assert fcns["home"] == ("ani", "etc")
    assert fcns["bin"] == ("ls", None)
    assert fcns["cp"] == (None, "mv")
    # ternary tree (k = 3): child indeks 0 adalah 1, 2, 3; child 1 adalah 4, 5, 6
    assert anak_k(0, 3) == [1, 2, 3] and anak_k(1, 3) == [4, 5, 6]
    assert all(parent_k(c, 3) == i for i in range(10) for c in anak_k(i, 3))
    for d, n in preorder(akar):
        print("    " * d + n)
    print("nary_tree.py: semua uji lolos")
