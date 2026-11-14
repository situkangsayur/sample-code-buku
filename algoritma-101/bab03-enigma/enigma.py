"""Bab 3: simulator Enigma I (tiga rotor dari rotor I-V, reflector B, plugboard).

Wiring rotor dan reflector mengikuti dokumentasi Enigma I yang banyak dipublikasikan.
Huruf dinyatakan sebagai angka 0..25 (A=0).
"""
from string import ascii_uppercase as ABJAD

ROTOR = {
    "I": ("EKMFLGDQVZNTOWYHXUSPAIBRCJ", "Q"),
    "II": ("AJDKSIRUXBLHWTMCQGZNPYFVOE", "E"),
    "III": ("BDFHJLCPRTXVZNYEIWGAKMUSQO", "V"),
    "IV": ("ESOVPZJAYQUIRHXLNFTGKDCMWB", "J"),
    "V": ("VZBRGITYUPSDNHLXAWMJQOFECK", "Z"),
}
REFLECTOR_B = "YRUHQSLDPXNGOKMIEBFZCWVJAT"


def a2i(c):
    return ord(c) - ord("A")


class Enigma:
    def __init__(self, urutan=("I", "II", "III"), cincin="AAA", posisi="AAA", colokan=""):
        # indeks 0 = rotor kiri, 2 = rotor kanan (rotor cepat)
        self.maju = [[a2i(c) for c in ROTOR[r][0]] for r in urutan]
        self.mundur = []
        for w in self.maju:
            inv = [0] * 26
            for i, o in enumerate(w):
                inv[o] = i
            self.mundur.append(inv)
        self.takik = [a2i(ROTOR[r][1]) for r in urutan]
        self.cincin = [a2i(c) for c in cincin]
        self.pos = [a2i(c) for c in posisi]
        self.plug = list(range(26))
        for pasangan in colokan.split():
            x, y = a2i(pasangan[0]), a2i(pasangan[1])
            self.plug[x], self.plug[y] = y, x
        self.refl = [a2i(c) for c in REFLECTOR_B]

    def langkah(self):
        """Rotor berputar SEBELUM huruf disandikan, termasuk double stepping."""
        if self.pos[1] == self.takik[1]:
            self.pos[1] = (self.pos[1] + 1) % 26
            self.pos[0] = (self.pos[0] + 1) % 26
        elif self.pos[2] == self.takik[2]:
            self.pos[1] = (self.pos[1] + 1) % 26
        self.pos[2] = (self.pos[2] + 1) % 26

    def _lewat(self, x, i, tabel):
        geser = self.pos[i] - self.cincin[i]
        return (tabel[i][(x + geser) % 26] - geser) % 26

    def huruf(self, c):
        self.langkah()
        x = self.plug[a2i(c)]
        for i in (2, 1, 0):  # kanan ke kiri
            x = self._lewat(x, i, self.maju)
        x = self.refl[x]
        for i in (0, 1, 2):  # kiri ke kanan
            x = self._lewat(x, i, self.mundur)
        return ABJAD[self.plug[x]]

    def sandi(self, teks):
        return "".join(self.huruf(c) for c in teks if c in ABJAD)


if __name__ == "__main__":
    # Vektor uji yang dikenal luas: I-II-III, cincin AAA, posisi AAA, tanpa colokan.
    assert Enigma().sandi("AAAAA") == "BDZGO"

    kunci = dict(urutan=("II", "IV", "V"), cincin="BUL", posisi="RTZ",
                 colokan="AV BS CG DL FU HZ IN KM OW RX")
    asli = "WETTERVORHERSAGEFUERDIENORDSEE"
    sandi = Enigma(**kunci).sandi(asli)
    print("asli :", asli)
    print("sandi:", sandi)
    # Sifat 1: mesin bersifat reciprocal; menyandikan dua kali mengembalikan teks asli.
    assert Enigma(**kunci).sandi(sandi) == asli
    # Sifat 2: tidak ada huruf yang disandikan menjadi dirinya sendiri.
    teks = ABJAD * 40
    hasil = Enigma(**kunci).sandi(teks)
    assert all(a != b for a, b in zip(teks, hasil))
    # Double stepping: posisi ADU -> ADV -> AEW -> BFX (rotor tengah melangkah dua kali).
    e = Enigma(posisi="ADU")
    urutan = []
    for _ in range(3):
        e.langkah()
        urutan.append("".join(ABJAD[p] for p in e.pos))
    assert urutan == ["ADV", "AEW", "BFX"], urutan
    print("semua uji lolos")
