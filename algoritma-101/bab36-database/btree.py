"""Bab 36: B-tree dengan minimum degree t (gaya CLRS).

Setiap node selain root berisi t-1 sampai 2t-1 key.
search mengembalikan (node, indeks) dan menghitung node yang dikunjungi,
karena di database satu node = satu page di disk.
Indeks mulai 0 (Python).
"""
import bisect
import math
import random


class Node:
    def __init__(self, leaf=True):
        self.keys = []
        self.children = []
        self.leaf = leaf


class BTree:
    def __init__(self, t=3):
        self.t = t
        self.root = Node()

    def search(self, k):
        """(node, i, banyak node dikunjungi) atau (None, -1, banyak)."""
        x, kunjung = self.root, 0
        while True:
            kunjung += 1
            i = bisect.bisect_left(x.keys, k)   # binary search di dalam node
            if i < len(x.keys) and x.keys[i] == k:
                return x, i, kunjung
            if x.leaf:
                return None, -1, kunjung
            x = x.children[i]                    # turun satu level

    def _split_child(self, x, i):
        t = self.t
        y = x.children[i]
        z = Node(leaf=y.leaf)
        tengah = y.keys[t - 1]
        z.keys = y.keys[t:]
        y.keys = y.keys[:t - 1]
        if not y.leaf:
            z.children = y.children[t:]
            y.children = y.children[:t]
        x.keys.insert(i, tengah)
        x.children.insert(i + 1, z)

    def insert(self, k):
        r = self.root
        if len(r.keys) == 2 * self.t - 1:      # root penuh: tinggi bertambah
            s = Node(leaf=False)
            s.children.append(r)
            self.root = s
            self._split_child(s, 0)
        self._insert_nonfull(self.root, k)

    def _insert_nonfull(self, x, k):
        while not x.leaf:
            i = bisect.bisect_right(x.keys, k)
            if len(x.children[i].keys) == 2 * self.t - 1:
                self._split_child(x, i)
                if k > x.keys[i]:
                    i += 1
            x = x.children[i]
        bisect.insort(x.keys, k)

    def tinggi(self):
        h, x = 0, self.root
        while not x.leaf:
            x, h = x.children[0], h + 1
        return h

    def inorder(self, x=None):
        x = x or self.root
        if x.leaf:
            yield from x.keys
            return
        for i, k in enumerate(x.keys):
            yield from self.inorder(x.children[i])
            yield k
        yield from self.inorder(x.children[-1])


def cek_invarian(tree, x=None, depth=0, daun=None):
    x = x or tree.root
    daun = daun if daun is not None else set()
    t = tree.t
    if x is not tree.root:
        assert t - 1 <= len(x.keys) <= 2 * t - 1
    assert x.keys == sorted(x.keys)
    if x.leaf:
        daun.add(depth)
    else:
        assert len(x.children) == len(x.keys) + 1
        for c in x.children:
            cek_invarian(tree, c, depth + 1, daun)
    return daun


if __name__ == "__main__":
    rng = random.Random(34)
    kunci = rng.sample(range(1, 100_000), 10_000)
    bt = BTree(t=50)
    for k in kunci:
        bt.insert(k)
    assert len(cek_invarian(bt)) == 1           # semua leaf sama dalam
    assert list(bt.inorder()) == sorted(kunci)
    n, t = len(kunci), bt.t
    assert bt.tinggi() <= math.log((n + 1) / 2, t)
    for k in rng.sample(kunci, 500):
        node, i, kunjung = bt.search(k)
        assert node is not None and node.keys[i] == k
        assert kunjung <= bt.tinggi() + 1
    assert bt.search(0)[0] is None
    print("n = %d, t = %d, tinggi = %d" % (n, t, bt.tinggi()))

    kecil = BTree(t=2)                           # contoh di buku
    for k in [10, 20, 5, 6, 12, 30, 7, 17]:
        kecil.insert(k)
    assert kecil.root.keys == [10, 20]
    assert [c.keys for c in kecil.root.children] == [[5, 6, 7], [12, 17], [30]]
    print("root:", kecil.root.keys, "anak:", [c.keys for c in kecil.root.children])
    assert kecil.search(17)[2] == 2              # root [10, 20], lalu leaf [12, 17]
    print("btree: semua uji lolos")
