"""Bab 35: urutan probing dict CPython (Objects/dictobject.c, 3.12).

    perturb = hash
    i = hash & mask
    ulangi: perturb >>= 5;  i = (5*i + perturb + 1) & mask
Juga model kecil tata letak compact dict: tabel indices + array entries.
"""
PERTURB_SHIFT = 5


def urutan_probe(h, mask, banyak):
    """Slot pertama sampai ke-banyak yang dicoba untuk hash h."""
    perturb = h & ((1 << 64) - 1)       # hash diperlakukan sebagai unsigned
    i = h & mask
    hasil = [i]
    while len(hasil) < banyak:
        perturb >>= PERTURB_SHIFT
        i = (i * 5 + perturb + 1) & mask
        hasil.append(i)
    return hasil


class CompactDict:
    """Model sederhana: indices (hash table kecil) + entries (urut sisip)."""

    def __init__(self, ukuran=8):
        self.mask = ukuran - 1
        self.indices = [None] * ukuran   # None = kosong
        self.entries = []                # (hash, key, value)

    def _cari_slot(self, key):
        h = hash(key)
        perturb = h & ((1 << 64) - 1)
        i = h & self.mask
        while True:
            idx = self.indices[i]
            if idx is None or self.entries[idx][1] == key:
                return i
            perturb >>= PERTURB_SHIFT
            i = (i * 5 + perturb + 1) & self.mask

    def put(self, key, value):
        # usable fraction 2/3: tabel 8 slot menampung 5 entri
        assert len(self.entries) < (2 * (self.mask + 1)) // 3, "perlu resize"
        i = self._cari_slot(key)
        if self.indices[i] is None:
            self.indices[i] = len(self.entries)
            self.entries.append((hash(key), key, value))
        else:
            h, k, _ = self.entries[self.indices[i]]
            self.entries[self.indices[i]] = (h, k, value)

    def get(self, key):
        idx = self.indices[self._cari_slot(key)]
        return None if idx is None else self.entries[idx][2]


if __name__ == "__main__":
    # contoh di buku: hash(13) = 13, tabel 8 slot (mask 7)
    assert hash(13) == 13
    assert urutan_probe(13, 7, 4) == [5, 2, 3, 0]
    assert urutan_probe(5, 7, 3) == [5, 2, 3]
    # setelah perturb habis, i = 5i + 1 mod 8 mengunjungi semua slot
    assert sorted(urutan_probe(0, 7, 8)) == list(range(8))

    d = CompactDict()
    for k, v in [(5, "a"), (13, "b"), (21, "c"), (2, "d")]:
        d.put(k, v)
    assert d.get(13) == "b" and d.get(21) == "c" and d.get(99) is None
    assert [e[1] for e in d.entries] == [5, 13, 21, 2]   # urutan sisip terjaga
    print("indices:", d.indices)
    print("entries:", [(k, v) for _, k, v in d.entries])

    # dict asli menjaga urutan sisip (dijamin sejak Python 3.7)
    asli = {}
    for k in [5, 13, 21, 2]:
        asli[k] = True
    assert list(asli) == [5, 13, 21, 2]
    print("dict_probe: semua uji lolos")
