"""Hash table dengan separate chaining (Algoritma 18.2, Kode 18.1).

Setiap slot berisi list pasangan (kunci, nilai). Tabel diperbesar dua kali
lipat bila load factor alpha = n / m melewati MAKS_ALPHA.
Indeks Python mulai 0, sama dengan rumus h(k) = k mod m.
"""

MAKS_ALPHA = 1.0


class HashTableChaining:
    def __init__(self, m=11):
        self.m = m
        self.n = 0
        self.slot = [[] for _ in range(m)]

    def _h(self, kunci):
        # hash() bawaan Python, lalu dipetakan ke 0..m-1
        return hash(kunci) % self.m

    def put(self, kunci, nilai):
        rantai = self.slot[self._h(kunci)]
        for i, (k, _) in enumerate(rantai):
            if k == kunci:            # kunci sudah ada: ganti nilainya
                rantai[i] = (kunci, nilai)
                return
        rantai.append((kunci, nilai))
        self.n += 1
        if self.n / self.m > MAKS_ALPHA:
            self._rehash(2 * self.m + 1)

    def get(self, kunci):
        for k, v in self.slot[self._h(kunci)]:
            if k == kunci:
                return v
        return None                   # padanan nil

    def remove(self, kunci):
        rantai = self.slot[self._h(kunci)]
        for i, (k, _) in enumerate(rantai):
            if k == kunci:
                del rantai[i]
                self.n -= 1
                return True
        return False

    def _rehash(self, m_baru):
        lama = self.slot
        self.m = m_baru
        self.n = 0
        self.slot = [[] for _ in range(m_baru)]
        for rantai in lama:
            for k, v in rantai:
                self.put(k, v)

    def alpha(self):
        return self.n / self.m


def demo_tabel_buku():
    """Kunci contoh di buku dengan m = 11, h(k) = k mod 11."""
    t = HashTableChaining(11)
    for k in [23, 15, 42, 34, 12, 57, 31, 45]:
        t.put(k, "data-" + str(k))
    return t


if __name__ == "__main__":
    t = demo_tabel_buku()
    # isi slot sesuai Gambar 18.2: slot 1 = 23, 34, 12, 45
    assert [k for k, _ in t.slot[1]] == [23, 34, 12, 45]
    assert [k for k, _ in t.slot[9]] == [42, 31]
    assert [k for k, _ in t.slot[2]] == [57]
    assert round(t.alpha(), 2) == 0.73
    assert t.get(12) == "data-12"
    assert t.get(99) is None
    assert t.remove(34) and not t.remove(34)
    assert [k for k, _ in t.slot[1]] == [23, 12, 45]

    # rehashing: tambah kunci sampai alpha > 1
    for k in range(100, 110):
        t.put(k, k)
    assert t.m == 23 and t.alpha() <= 1.0
    for k in [23, 15, 42, 12, 57, 31, 45] + list(range(100, 110)):
        assert t.get(k) is not None
    # kunci string juga bisa
    s = HashTableChaining()
    s.put("tazkia", 1)
    s.put("sentul", 2)
    s.put("tazkia", 3)
    assert s.get("tazkia") == 3 and s.n == 2
    print("hash_chaining.py: semua uji lolos")
