"""Simulasi ring all-reduce (reduce-scatter lalu all-gather) dengan NumPy.

Setiap 'GPU' adalah satu larik. Program menghitung jumlah byte yang dikirim tiap peserta
dan memeriksa hasilnya sama dengan jumlah biasa.
    python ring_allreduce.py --peserta 4 --ukuran 1000000
"""
import argparse

import numpy as np


def ring_allreduce(data: list[np.ndarray]) -> tuple[list[np.ndarray], int]:
    N = len(data)
    buf = [d.copy() for d in data]
    potong = [np.array_split(b, N) for b in buf]     # gradien dipotong menjadi N bagian
    terkirim = 0
    # Fase 1: reduce-scatter, N-1 langkah. Pada langkah s, peserta i mengirim
    # potongan (i - s) mod N ke tetangga kanan, yang menjumlahkannya.
    for s in range(N - 1):
        kiriman = [(i, (i - s) % N, potong[i][(i - s) % N].copy()) for i in range(N)]
        for i, c, isi in kiriman:
            potong[(i + 1) % N][c] += isi
            terkirim += isi.nbytes
    # Kini peserta i memegang potongan (i + 1) mod N yang sudah lengkap jumlahnya.
    # Fase 2: all-gather, N-1 langkah: edarkan potongan lengkap.
    for s in range(N - 1):
        kiriman = [(i, (i + 1 - s) % N, potong[i][(i + 1 - s) % N].copy()) for i in range(N)]
        for i, c, isi in kiriman:
            potong[(i + 1) % N][c] = isi
            terkirim += isi.nbytes
    return [np.concatenate(p) for p in potong], terkirim // N


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--peserta", type=int, default=4)
    ap.add_argument("--ukuran", type=int, default=1_000_000)
    a = ap.parse_args()
    rng = np.random.default_rng(0)
    data = [rng.standard_normal(a.ukuran).astype(np.float32) for _ in range(a.peserta)]
    hasil, per_peserta = ring_allreduce(data)
    acuan = np.sum(data, axis=0)
    ok = all(np.allclose(h, acuan, rtol=1e-5, atol=1e-5) for h in hasil)
    S = data[0].nbytes
    teori = 2 * (a.peserta - 1) / a.peserta * S
    print(f"N={a.peserta} S={S / 1e6:.1f} MB  kirim/peserta={per_peserta / 1e6:.2f} MB "
          f"(teori 2(N-1)/N*S = {teori / 1e6:.2f} MB)  {'LULUS' if ok else 'GAGAL'}")


if __name__ == "__main__":
    main()
