"""Pembangkit data transaksi sintetis bank syariah digital.

Semua data acak (sintetis), bukan data nasabah sungguhan.
Pemakaian:
    python bangkit_data.py --baris 1000000 --keluar data/transaksi.csv
"""
import argparse
import os

import numpy as np
import polars as pl

KANAL = ["mobile", "ATM", "agen", "QRIS", "teller"]
PRODUK = ["wadiah", "mudharabah", "murabahah", "musyarakah", "ijarah"]
CABANG = ["BGR01", "BDG01", "JKT01", "JKT02", "SBY01", "MDN01", "MKS01"]


def bangkit(n: int, seed: int = 42) -> pl.DataFrame:
    rng = np.random.default_rng(seed)
    awal = np.datetime64("2026-01-01T00:00:00")
    detik = rng.integers(0, 365 * 24 * 3600, size=n)
    waktu = (awal + detik.astype("timedelta64[s]")).astype("datetime64[us]")
    # nominal berdistribusi log-normal: banyak transaksi kecil, sedikit yang besar
    nominal = np.round(rng.lognormal(mean=11.5, sigma=1.1, size=n), -2)
    return pl.DataFrame(
        {
            "id_transaksi": [f"T-{i:09d}" for i in range(n)],
            "id_rekening": rng.integers(1, 200_000, size=n).astype(str),
            "waktu": waktu,
            "kanal": rng.choice(KANAL, size=n, p=[0.55, 0.15, 0.1, 0.15, 0.05]),
            "produk": rng.choice(PRODUK, size=n, p=[0.5, 0.2, 0.15, 0.1, 0.05]),
            "cabang": rng.choice(CABANG, size=n),
            "nominal": nominal,
        }
    ).sort("waktu")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--baris", type=int, default=1_000_000)
    ap.add_argument("--keluar", default="data/transaksi.csv")
    a = ap.parse_args()
    os.makedirs(os.path.dirname(a.keluar) or ".", exist_ok=True)
    df = bangkit(a.baris)
    df.write_csv(a.keluar)
    print(f"{df.height} baris ditulis ke {a.keluar}")
