"""HyperLogLog sederhana (Kode 33.4).

m = 2^p register. Setiap item di-hash 64 bit: p bit pertama memilih
register, sisanya dipakai untuk menghitung posisi bit 1 pertama.
"""
import hashlib
import math


class HyperLogLog:
    def __init__(self, p=10):
        self.p = p
        self.m = 1 << p
        self.reg = [0] * self.m
        self.alpha = 0.7213 / (1 + 1.079 / self.m)   # konstanta untuk m >= 128

    def tambah(self, item):
        x = int.from_bytes(hashlib.sha256(item.encode()).digest()[:8], "big")
        j = x >> (64 - self.p)                       # p bit pertama: nomor register
        w = x & ((1 << (64 - self.p)) - 1)           # sisa 64 - p bit
        rho = (64 - self.p) - w.bit_length() + 1     # posisi bit 1 pertama dari kiri
        self.reg[j] = max(self.reg[j], rho)

    def taksir(self):
        z = sum(2.0 ** -r for r in self.reg)
        e = self.alpha * self.m * self.m / z
        nol = self.reg.count(0)
        if e <= 2.5 * self.m and nol > 0:            # koreksi rentang kecil
            e = self.m * math.log(self.m / nol)
        return e


if __name__ == "__main__":
    hll = HyperLogLog(p=10)
    for i in range(100000):
        hll.tambah(f"pengunjung-{i % 50000}")        # 50.000 berbeda, tiap dua kali
    t = hll.taksir()
    galat = abs(t - 50000) / 50000
    print(f"taksiran: {t:,.0f}  galat relatif: {galat:.3%}")
    print(f"galat baku teori: {1.04 / math.sqrt(hll.m):.2%}")      # 3.25%
    print(f"memori register: {hll.m} x 6 bit = {hll.m * 6 // 8} byte")
    assert galat < 3 * 1.04 / math.sqrt(hll.m)
    kecil = HyperLogLog(p=10)
    for i in range(100):
        kecil.tambah(str(i))
    assert abs(kecil.taksir() - 100) < 10
    print("semua uji lolos")
