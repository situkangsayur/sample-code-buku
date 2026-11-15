"""Menghitung ruang kunci Enigma tiga rotor angkatan darat Jerman (Kode 33.1).

Anggapan model (disebut di Bab 33.1):
- 3 rotor dipilih berurutan dari 5 rotor yang tersedia;
- posisi awal setiap rotor 26 kemungkinan;
- plugboard dengan tepat 10 kabel (20 huruf dipasangkan);
- ring setting dan reflektor tidak dihitung.
"""
from math import factorial


def urutan_rotor(tersedia=5, dipakai=3):
    return factorial(tersedia) // factorial(tersedia - dipakai)


def posisi_awal(dipakai=3):
    return 26 ** dipakai


def plugboard(kabel=10):
    # pilih 2*kabel huruf, pasangkan; urutan pasangan dan isi pasangan tidak penting
    return factorial(26) // (factorial(26 - 2 * kabel) * factorial(kabel) * 2 ** kabel)


def ruang_kunci():
    return urutan_rotor() * posisi_awal() * plugboard()


if __name__ == "__main__":
    print(urutan_rotor())            # 60
    print(posisi_awal())             # 17576
    print(plugboard())               # 150738274937250
    total = ruang_kunci()
    print(total)                     # 158962555217826360000
    print(f"{total:.3e}")            # 1.590e+20
    tahun = total / 1e8 / (365 * 24 * 3600)
    print(f"{tahun:,.0f} tahun pada 1e8 kunci per detik")
    assert urutan_rotor() == 60
    assert plugboard() == 150738274937250
    assert total == 158962555217826360000
    # tanpa plugboard ruangnya kecil: 60 * 17576 = 1.054.560
    assert urutan_rotor() * posisi_awal() == 1054560
    print("semua uji lolos")
