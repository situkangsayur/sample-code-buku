"""Pola map-reduce atas banyak berkas CSV kecil dengan dask.delayed.

Langkah:
    python buat_data.py --berkas 500           # membuat data/transaksi_XXX.csv
    python dask_berkas.py --alamat tcp://localhost:8786
    python dask_berkas.py --serial             # pembanding satu proses
"""
import argparse
import glob
import time

import dask
import pandas as pd


def baca(path: str) -> pd.DataFrame:
    return pd.read_csv(path)


def ganti_akar(path: str, akar: str | None) -> str:
    # klien melihat data/..., worker Docker melihat /data/... (lihat docker-compose.yml)
    return path if akar is None else path.replace("data/", akar.rstrip("/") + "/", 1)


def olah(df: pd.DataFrame) -> pd.Series:
    # map: total nominal per kanal untuk satu berkas
    return df.groupby("kanal")["nominal"].sum()


def gabung(xs: list) -> pd.Series:
    # reduce: jumlahkan hasil parsial semua berkas
    return pd.concat(xs).groupby(level=0).sum().sort_index()


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--alamat", default=None)
    ap.add_argument("--pola", default="data/transaksi_*.csv")
    ap.add_argument("--serial", action="store_true")
    ap.add_argument("--akar-worker", default=None, help="mis. /data untuk worker Docker")
    a = ap.parse_args()
    berkas = sorted(glob.glob(a.pola))
    t0 = time.perf_counter()
    if a.serial:
        hasil = gabung([olah(baca(p)) for p in berkas])
    else:
        from dask.distributed import Client
        client = Client(a.alamat) if a.alamat else Client()   # tanpa alamat: klaster lokal
        print("dashboard:", client.dashboard_link)
        d_baca, d_olah, d_gabung = dask.delayed(baca), dask.delayed(olah), dask.delayed(gabung)
        graf = d_gabung([d_olah(d_baca(ganti_akar(p, a.akar_worker))) for p in berkas])  # belum dihitung (lazy)
        hasil = graf.compute()
    print(hasil)
    print(f"{len(berkas)} berkas, {time.perf_counter() - t0:.2f} s")


if __name__ == "__main__":
    main()
