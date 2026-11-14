"""Bab 35: urutan join dengan dynamic programming (gagasan System R, Selinger 1979).

Model biaya sederhana: biaya sebuah plan left-deep = jumlah ukuran semua
hasil antara (termasuk hasil akhir). Ukuran hasil join himpunan tabel S:
    |S| = hasil kali kardinalitas * hasil kali selektivitas predikat di dalam S
DP atas subset:  best[S] = min_{r in S} best[S - {r}] + ukuran(S)
Dibandingkan dengan brute force atas semua permutasi.
"""
from itertools import combinations, permutations

KARD = {"M": 2_000, "K": 200_000, "MK": 500, "D": 100}   # M sudah difilter prodi
SEL = {frozenset({"M", "K"}): 1 / 10_000,
       frozenset({"K", "MK"}): 1 / 500,
       frozenset({"MK", "D"}): 1 / 100}


def ukuran(S):
    hasil = 1.0
    for t in S:
        hasil *= KARD[t]
    for pasangan, s in SEL.items():
        if pasangan <= S:
            hasil *= s
    return round(hasil)


def dp_urutan_join(tabel):
    """Kembalikan (biaya, urutan) terbaik dan tabel DP per ukuran subset."""
    best = {frozenset([t]): (0, (t,)) for t in tabel}
    for ukuran_s in range(2, len(tabel) + 1):
        for S in map(frozenset, combinations(tabel, ukuran_s)):
            kandidat = []
            for r in S:                        # r = tabel yang di-join terakhir
                biaya_sisa, urut = best[S - {r}]
                kandidat.append((biaya_sisa + ukuran(S), urut + (r,)))
            best[S] = min(kandidat)
    return best[frozenset(tabel)], best


def brute_force(tabel):
    terbaik = None
    for urut in permutations(tabel):
        biaya = sum(ukuran(frozenset(urut[:i])) for i in range(2, len(urut) + 1))
        if terbaik is None or biaya < terbaik[0]:
            terbaik = (biaya, urut)
    return terbaik


if __name__ == "__main__":
    tabel = ["M", "K", "MK", "D"]
    assert ukuran(frozenset({"M", "K"})) == 40_000
    assert ukuran(frozenset({"MK", "D"})) == 500
    assert ukuran(frozenset({"M", "D"})) == 200_000      # cross product
    (biaya, urut), best = dp_urutan_join(tabel)
    print("DP   :", biaya, urut)
    print("brute:", brute_force(tabel))
    assert biaya == brute_force(tabel)[0]
    for S, (c, u) in sorted(best.items(), key=lambda x: (len(x[0]), sorted(x[0]))):
        if len(S) >= 2:
            print("%-16s ukuran=%-8d best=%-8d urutan=%s"
                  % ("{" + ",".join(sorted(S)) + "}", ukuran(S), c, "-".join(u)))
    # DP memeriksa 2^n subset, brute force n! urutan
    assert len(best) == 2 ** len(tabel) - 1
    print("join_dp: semua uji lolos")
