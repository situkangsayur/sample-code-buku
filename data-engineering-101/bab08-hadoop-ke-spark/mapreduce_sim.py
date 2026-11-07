"""Simulasi MapReduce di satu proses (Algoritma 8.1 dan 8.2).

Menghitung total transaksi SUKSES per kota dari beberapa "blok", dengan dan tanpa combiner,
sekaligus menghitung berapa byte yang akan dikirim lewat jaringan saat shuffle.

    python mapreduce_sim.py --blok 100 --baris-per-blok 10000 --reducer 4
"""
import argparse
import random
from collections import defaultdict

KOTA = ["BGR", "JKT", "BDG", "SBY", "MDN"]
UKURAN_PASANGAN = 20  # perkiraan byte per pasangan (kota, nominal)


def buat_blok(n_blok, n_baris, seed=1):
    rnd = random.Random(seed)
    return [[f"{rnd.choice(KOTA)},{rnd.randint(10, 500)},{'SUKSES' if rnd.random() < 0.97 else 'GAGAL'}"
             for _ in range(n_baris)] for _ in range(n_blok)]


def fungsi_map(baris):
    kota, nominal, status = baris.split(",")
    if status == "SUKSES":
        yield kota, int(nominal)


def fungsi_combine(pasangan):
    lokal = defaultdict(int)
    for k, v in pasangan:
        lokal[k] += v
    return list(lokal.items())


def fungsi_reduce(kota, nilai):
    return kota, sum(nilai)


def partitioner(key, r):
    # hash stabil (hash() Python diacak per proses)
    return sum(key.encode()) % r


def jalankan(blok, r, pakai_combiner):
    ember = [[[] for _ in range(r)] for _ in blok]   # [map_task][reducer]
    byte_dikirim = 0
    for i, b in enumerate(blok):                      # fase map, satu task per blok
        keluaran = [p for baris in b for p in fungsi_map(baris)]
        if pakai_combiner:
            keluaran = fungsi_combine(keluaran)
        for k, v in keluaran:
            ember[i][partitioner(k, r)].append((k, v))
        byte_dikirim += len(keluaran) * UKURAN_PASANGAN
    hasil = {}
    for j in range(r):                                # fase reduce
        tarikan = sorted(p for i in range(len(blok)) for p in ember[i][j])  # shuffle + sort
        kelompok = defaultdict(list)
        for k, v in tarikan:
            kelompok[k].append(v)
        for k, vs in kelompok.items():
            kk, tot = fungsi_reduce(k, vs)
            hasil[kk] = tot
    return hasil, byte_dikirim


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--blok", type=int, default=100)
    ap.add_argument("--baris-per-blok", type=int, default=10_000)
    ap.add_argument("--reducer", type=int, default=4)
    a = ap.parse_args()
    blok = buat_blok(a.blok, a.baris_per_blok)
    h1, b1 = jalankan(blok, a.reducer, False)
    h2, b2 = jalankan(blok, a.reducer, True)
    assert h1 == h2, "combiner tidak boleh mengubah hasil"
    for k in sorted(h1):
        print(f"{k}: {h1[k]}")
    print(f"byte shuffle tanpa combiner : {b1:,}")
    print(f"byte shuffle dengan combiner: {b2:,}  (hemat {b1 / b2:,.0f} kali)")
