"""Hash table dengan open addressing dan linear probing (Algoritma 18.3, Tabel 18.2).

Slot kosong ditandai None. Slot bekas hapus ditandai HAPUS (tombstone) supaya
pencarian kunci lain yang melewati slot itu tidak berhenti terlalu cepat.
Tabel diperbesar bila alpha melewati MAKS_ALPHA.
"""

HAPUS = object()      # penanda tombstone
MAKS_ALPHA = 0.75


class HashTableLinear:
    def __init__(self, m=11, maks_alpha=MAKS_ALPHA):
        self.m = m
        self.maks_alpha = maks_alpha
        self.n = 0
        self.kunci = [None] * m
        self.nilai = [None] * m

    def _h(self, k):
        return hash(k) % self.m

    def put(self, k, v):
        """Mengembalikan banyak probe yang dipakai (untuk tabel tracing)."""
        if (self.n + 1) / self.m > self.maks_alpha:
            self._rehash(2 * self.m + 1)
        i = self._h(k)
        probe = 1
        bekas = -1                     # tombstone pertama yang ditemui
        while self.kunci[i] is not None:
            if self.kunci[i] is HAPUS:
                if bekas < 0:
                    bekas = i
            elif self.kunci[i] == k:   # kunci sudah ada
                self.nilai[i] = v
                return probe
            i = (i + 1) % self.m
            probe += 1
        if bekas >= 0:
            i = bekas
        self.kunci[i] = k
        self.nilai[i] = v
        self.n += 1
        return probe

    def get(self, k):
        i = self._h(k)
        for _ in range(self.m):
            if self.kunci[i] is None:  # slot kosong asli: pasti tidak ada
                return None
            if self.kunci[i] is not HAPUS and self.kunci[i] == k:
                return self.nilai[i]
            i = (i + 1) % self.m
        return None

    def remove(self, k):
        i = self._h(k)
        for _ in range(self.m):
            if self.kunci[i] is None:
                return False
            if self.kunci[i] is not HAPUS and self.kunci[i] == k:
                self.kunci[i] = HAPUS
                self.nilai[i] = None
                self.n -= 1
                return True
            i = (i + 1) % self.m
        return False

    def _rehash(self, m_baru):
        pasangan = [(k, v) for k, v in zip(self.kunci, self.nilai)
                    if k is not None and k is not HAPUS]
        self.m = m_baru
        self.n = 0
        self.kunci = [None] * m_baru
        self.nilai = [None] * m_baru
        for k, v in pasangan:
            self.put(k, v)


if __name__ == "__main__":
    # tanpa rehash agar sama dengan Tabel 18.2 (alpha akhir 8/11)
    t = HashTableLinear(11, maks_alpha=1.0)
    probes = [t.put(k, k) for k in [23, 15, 42, 34, 12, 57, 31, 45]]
    assert probes == [1, 1, 1, 2, 3, 4, 2, 6], probes
    assert t.kunci == [None, 23, 34, 12, 15, 57, 45, None, None, 42, 31]
    assert t.get(45) == 45 and t.get(1) is None
    # hapus 12 lalu cari 45: harus tetap ketemu karena ada tombstone
    assert t.remove(12)
    assert t.kunci[3] is HAPUS
    assert t.get(45) == 45
    # sisip 56 (56 mod 11 = 1) memakai ulang tombstone di slot 3
    t.put(56, 56)
    assert t.kunci[3] == 56
    # rehash otomatis saat alpha akan melewati 0.75
    t.maks_alpha = MAKS_ALPHA
    for k in range(200, 210):
        t.put(k, k)
    assert t.m > 11 and t.n / t.m <= MAKS_ALPHA
    for k in [23, 15, 42, 34, 57, 31, 45, 56] + list(range(200, 210)):
        assert t.get(k) == k
    print("hash_linear_probing.py: semua uji lolos")
