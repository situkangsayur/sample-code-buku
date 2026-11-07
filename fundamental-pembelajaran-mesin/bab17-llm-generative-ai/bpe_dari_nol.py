"""Kode 14.1 - Byte pair encoding (BPE) dari nol, mengikuti Sennrich dkk. (2016).

Melatih aturan merge pada korpus kecil berbahasa Indonesia, lalu memakai
aturan itu untuk memecah kata baru. Penanda akhir kata: '_'.
"""
from collections import Counter


def hitung_pasangan(kosakata):
    pasangan = Counter()
    for kata, frek in kosakata.items():
        simbol = kata.split()
        for a, b in zip(simbol, simbol[1:]):
            pasangan[a, b] += frek
    return pasangan


def gabung(pasangan, kosakata):
    a, b = pasangan
    baru = {}
    for kata, frek in kosakata.items():
        s, hasil, i = kata.split(), [], 0
        while i < len(s):
            if i + 1 < len(s) and s[i] == a and s[i + 1] == b:
                hasil.append(a + b); i += 2
            else:
                hasil.append(s[i]); i += 1
        baru[" ".join(hasil)] = frek
    return baru


def latih_bpe(korpus, n_merge):
    kosakata = {" ".join(k) + " _": f for k, f in korpus.items()}
    aturan = []
    for langkah in range(n_merge):
        pasangan = hitung_pasangan(kosakata)
        terbaik = max(pasangan, key=pasangan.get)   # seri: yang muncul lebih dulu
        print(langkah + 1, terbaik, pasangan[terbaik])
        aturan.append(terbaik)
        kosakata = gabung(terbaik, kosakata)
    return aturan, kosakata


def tokenisasi(kata, aturan):
    simbol = {" ".join(kata) + " _": 1}
    for p in aturan:                                 # terapkan sesuai urutan
        simbol = gabung(p, simbol)
    return next(iter(simbol)).split()


if __name__ == "__main__":
    korpus = {"makan": 6, "makanan": 4, "dimakan": 3, "minum": 3, "minuman": 2}
    aturan, kosakata = latih_bpe(korpus, 7)
    print("kosakata akhir:", kosakata)
    for kata in ["makanan", "dimakan", "minuman", "makanlah", "dimakani"]:
        print(f"{kata:10s} ->", tokenisasi(kata, aturan))
