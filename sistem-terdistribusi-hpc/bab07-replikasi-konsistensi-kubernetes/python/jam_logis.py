"""Kode 7.1: Lamport clock dan vector clock, plus contoh Gambar 7.1 dan contoh konflik.

Pemakaian: python jam_logis.py
"""


class Lamport:
    def __init__(self): self.c = 0
    def lokal(self):    self.c += 1; return self.c
    def kirim(self):    self.c += 1; return self.c
    def terima(self, t): self.c = max(self.c, t) + 1; return self.c


def vc_lokal(v, i):
    v = list(v); v[i] += 1; return v


def vc_terima(lokal, masuk, i):          # vector clock proses i menerima pesan
    v = [max(a, b) for a, b in zip(lokal, masuk)]
    v[i] += 1
    return v


def vc_banding(a, b):
    if a == b: return "sama"
    if all(x <= y for x, y in zip(a, b)): return "a sebelum b"
    if all(x >= y for x, y in zip(a, b)): return "b sebelum a"
    return "concurrent (konflik)"


if __name__ == "__main__":
    # Gambar 7.1: tiga proses
    p1, p2, p3 = Lamport(), Lamport(), Lamport()
    print("P1 lokal :", p1.lokal())          # 1
    t = p1.kirim(); print("P1 kirim :", t)   # 2
    print("P2 lokal :", p2.lokal())          # 1
    print("P2 terima:", p2.terima(t))        # max(1,2)+1 = 3
    t = p2.kirim(); print("P2 kirim :", t)   # 4
    print("P3 lokal :", p3.lokal())          # 1
    print("P3 terima:", p3.terima(t))        # max(1,4)+1 = 5
    print("P3 lokal :", p3.lokal())          # 6
    print("P1 lokal :", p1.lokal())          # 3, concurrent dengan kejadian di P3

    # contoh konflik profil pengguna (replika A=0, B=1, C=2)
    a = vc_lokal([0, 0, 0], 0)               # A ubah alamat      [1,0,0]
    b = vc_terima([0, 0, 0], a, 1)           # B terima, lalu ...
    b = [1, 1, 0]                            # B ubah telepon     [1,1,0]
    c = vc_lokal([0, 0, 0], 2)               # C ubah alamat      [0,0,1]
    print(a, b, "->", vc_banding(a, b))
    print(b, c, "->", vc_banding(b, c))
