"""Bab 3: menghitung ruang kunci Enigma I (Angkatan Darat), lima rotor, sepuluh kabel."""
from math import factorial, comb, perm


def colokan(p, n=26):
    """Banyak cara memasang p kabel (p pasang huruf) pada n huruf:
    n! / ((n - 2p)! * p! * 2^p)."""
    return factorial(n) // (factorial(n - 2 * p) * factorial(p) * 2 ** p)


if __name__ == "__main__":
    urutan_rotor = perm(5, 3)   # 5 * 4 * 3 = 60
    posisi_awal = 26 ** 3       # 17.576
    cincin = 26 ** 2            # 676; cincin rotor kiri tidak memengaruhi langkah
    plug = colokan(10)
    assert urutan_rotor == 60 and posisi_awal == 17_576 and cincin == 676
    assert plug == 150_738_274_937_250
    total = urutan_rotor * posisi_awal * cincin * plug
    tanpa_cincin = urutan_rotor * posisi_awal * plug
    print(f"colokan 10 kabel : {plug:,}".replace(",", "."))
    print(f"tanpa cincin     : {tanpa_cincin:,}".replace(",", "."))
    print(f"dengan cincin    : {total:,}".replace(",", "."))
    assert tanpa_cincin == 158_962_555_217_826_360_000
    # Lama brute force bila satu juta kunci diperiksa per detik.
    tahun = total / 1e6 / (365.25 * 24 * 3600)
    print(f"1 juta kunci/detik: {tahun:.2e} tahun")
    # Tabel banyak kabel 0..13 (puncaknya di 11 kabel).
    nilai = {p: colokan(p) for p in range(14)}
    assert max(nilai, key=nilai.get) == 11
    assert comb(26, 2) == colokan(1) == 325
    print("semua uji lolos")
