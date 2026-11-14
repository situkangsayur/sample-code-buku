"""Binary search tree (Algoritma 19.1, Kode 19.1, Tabel 19.1).

Kunci unik. Duplikat diabaikan.
"""


class Node:
    def __init__(self, kunci):
        self.kunci = kunci
        self.kiri = None
        self.kanan = None


def sisip(akar, kunci):
    """Mengembalikan akar tree setelah kunci disisipkan (rekursif)."""
    if akar is None:
        return Node(kunci)
    if kunci < akar.kunci:
        akar.kiri = sisip(akar.kiri, kunci)
    elif kunci > akar.kunci:
        akar.kanan = sisip(akar.kanan, kunci)
    return akar


def cari(akar, kunci):
    """Iteratif. Mengembalikan (node atau None, banyak perbandingan)."""
    langkah = 0
    x = akar
    while x is not None:
        langkah += 1
        if kunci == x.kunci:
            return x, langkah
        x = x.kiri if kunci < x.kunci else x.kanan
    return None, langkah


def inorder(akar, hasil):
    if akar is not None:
        inorder(akar.kiri, hasil)
        hasil.append(akar.kunci)
        inorder(akar.kanan, hasil)
    return hasil


def tinggi(akar):
    """Tinggi tree kosong -1, tree satu node 0."""
    if akar is None:
        return -1
    return 1 + max(tinggi(akar.kiri), tinggi(akar.kanan))


def minimum(akar):
    while akar.kiri is not None:
        akar = akar.kiri
    return akar


def hapus(akar, kunci):
    """Tiga kasus: daun, satu anak, dua anak (ganti dengan successor)."""
    if akar is None:
        return None
    if kunci < akar.kunci:
        akar.kiri = hapus(akar.kiri, kunci)
    elif kunci > akar.kunci:
        akar.kanan = hapus(akar.kanan, kunci)
    else:
        if akar.kiri is None:
            return akar.kanan
        if akar.kanan is None:
            return akar.kiri
        s = minimum(akar.kanan)          # successor inorder
        akar.kunci = s.kunci
        akar.kanan = hapus(akar.kanan, s.kunci)
    return akar


def bangun(urutan):
    akar = None
    for k in urutan:
        akar = sisip(akar, k)
    return akar


if __name__ == "__main__":
    akar = bangun([50, 30, 70, 20, 40, 60, 80, 35])
    assert inorder(akar, []) == [20, 30, 35, 40, 50, 60, 70, 80]
    assert tinggi(akar) == 3
    node, langkah = cari(akar, 35)
    assert node.kunci == 35 and langkah == 4      # 50, 30, 40, 35
    node, langkah = cari(akar, 65)
    assert node is None and langkah == 3          # 50, 70, 60
    assert minimum(akar).kunci == 20

    # hapus node dengan dua anak (30): diganti successor 35
    akar = hapus(akar, 30)
    assert akar.kiri.kunci == 35
    assert inorder(akar, []) == [20, 35, 40, 50, 60, 70, 80]

    # sisip terurut: tree menjadi rantai, tinggi n - 1
    rantai = bangun(list(range(1, 11)))
    assert tinggi(rantai) == 9
    print("bst.py: semua uji lolos")
