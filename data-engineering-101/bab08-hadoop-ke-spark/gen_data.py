"""Pembangkit data sintetis transaksi bank syariah digital (Bab 8-9).

Contoh:
    python gen_data.py --baris 1000000 --keluar data
Menghasilkan:
    data/trx.csv                 (kota,nominal,status) untuk Kode 8.1 (RDD)
    data/silver/transaksi/       Parquet: id_trx,id_nasabah,id_cabang,tanggal,nominal,status,kanal
    data/silver/nasabah/         Parquet: id_nasabah,cabang,segmen
    data/silver/cabang/          Parquet: id_cabang,cabang,wilayah
    data/silver/rekening/        Parquet: id_rekening,saldo
"""
import argparse
import os

import numpy as np
import pandas as pd

KOTA = ["BGR", "JKT", "BDG", "SBY", "MDN", "MKS", "SMG", "YOG", "PLB", "DPS"]
WILAYAH = {"BGR": "Jabar", "JKT": "Jakarta", "BDG": "Jabar", "SBY": "Jatim", "MDN": "Sumut",
           "MKS": "Sulsel", "SMG": "Jateng", "YOG": "DIY", "PLB": "Sumsel", "DPS": "Bali"}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--baris", type=int, default=1_000_000)
    ap.add_argument("--nasabah", type=int, default=100_000)
    ap.add_argument("--keluar", default="data")
    ap.add_argument("--seed", type=int, default=42)
    a = ap.parse_args()
    rng = np.random.default_rng(a.seed)
    os.makedirs(a.keluar, exist_ok=True)

    cabang = pd.DataFrame({"id_cabang": np.arange(len(KOTA)), "cabang": KOTA,
                           "wilayah": [WILAYAH[k] for k in KOTA]})
    nasabah = pd.DataFrame({
        "id_nasabah": np.arange(a.nasabah, dtype=np.int64),
        "cabang": rng.choice(KOTA, a.nasabah),
        "segmen": rng.choice(["ritel", "umkm", "korporat"], a.nasabah, p=[0.85, 0.13, 0.02]),
    })
    tanggal = pd.to_datetime("2026-09-01") + pd.to_timedelta(rng.integers(0, 61, a.baris), "D")
    trx = pd.DataFrame({
        "id_trx": np.arange(a.baris, dtype=np.int64),
        "id_nasabah": rng.integers(0, a.nasabah, a.baris),
        "id_cabang": rng.integers(0, len(KOTA), a.baris),
        "tanggal": tanggal.date.astype(str),
        "nominal": np.round(rng.lognormal(12, 1.2, a.baris), 0),
        "status": rng.choice(["SUKSES", "GAGAL"], a.baris, p=[0.97, 0.03]),
        "kanal": rng.choice(["mobile", "atm", "qris", "teller"], a.baris, p=[0.6, 0.15, 0.2, 0.05]),
    })
    rekening = pd.DataFrame({"id_rekening": np.arange(a.nasabah, dtype=np.int64),
                             "saldo": np.round(rng.lognormal(16, 1.5, a.nasabah), 0)})

    s = os.path.join(a.keluar, "silver")
    for nama, df in [("cabang", cabang), ("nasabah", nasabah), ("rekening", rekening)]:
        os.makedirs(os.path.join(s, nama), exist_ok=True)
        df.to_parquet(os.path.join(s, nama, "part-0.parquet"), index=False)
    os.makedirs(os.path.join(s, "transaksi"), exist_ok=True)
    trx.to_parquet(os.path.join(s, "transaksi", "part-0.parquet"), index=False)

    kota = cabang.set_index("id_cabang").loc[trx["id_cabang"], "cabang"].to_numpy()
    pd.DataFrame({"kota": kota, "nominal": trx["nominal"], "status": trx["status"]}).to_csv(
        os.path.join(a.keluar, "trx.csv"), index=False, header=False)
    print("selesai:", a.baris, "transaksi ->", a.keluar)


if __name__ == "__main__":
    main()
