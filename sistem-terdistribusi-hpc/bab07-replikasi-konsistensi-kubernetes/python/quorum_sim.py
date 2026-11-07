"""Simulasi quorum (Subbab 7.2.3): seberapa sering pembaca melihat versi usang.

Setiap tulisan hanya sampai ke W replika acak (sisanya tertinggal). Pembaca bertanya
ke R replika acak dan mengambil versi tertinggi. Bila W + R > N, versi usang mustahil.
Pemakaian: python quorum_sim.py
"""
import random


def coba(N, W, R, ulang=20_000):
    usang = 0
    for _ in range(ulang):
        replika = [1] * N                       # semua punya v1
        for i in random.sample(range(N), W):    # tulis v2 ke W replika
            replika[i] = 2
        dibaca = max(replika[i] for i in random.sample(range(N), R))
        usang += dibaca < 2
    return usang / ulang


if __name__ == "__main__":
    random.seed(1)
    for N, W, R in [(3, 2, 2), (3, 1, 1), (3, 1, 2), (5, 3, 3), (5, 2, 3), (5, 1, 1)]:
        print(f"N={N} W={W} R={R}  W+R>N={W + R > N!s:5}  baca usang: {coba(N, W, R):6.1%}")
