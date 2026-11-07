"""Validasi batch terhadap data contract. Bila bronze_transaksi.parquet belum ada,
skrip membuat contoh berisi satu pelanggaran agar hasilnya terlihat."""
import os
from datetime import datetime

import polars as pl
import yaml


def validasi(df: pl.DataFrame, kontrak: dict) -> list[str]:
    salah = []
    for k in kontrak["skema"]:
        n = k["nama"]
        if n not in df.columns:
            salah.append(f"kolom hilang: {n}")
            continue
        if k.get("wajib") and df[n].null_count() > 0:
            salah.append(f"{n}: {df[n].null_count()} nilai null")
        if k.get("unik") and df[n].n_unique() != df.height:
            salah.append(f"{n}: tidak unik")
        if k.get("aturan") == "> 0" and (df[n] <= 0).any():
            salah.append(f"{n}: ada nilai <= 0")
    return salah


if __name__ == "__main__":
    if not os.path.exists("bronze_transaksi.parquet"):
        pl.DataFrame({
            "id_transaksi": ["T1", "T2", "T2"],
            "nik": ["3201011234560001", "3201011234560002", None],
            "nominal": [150000.0, -5000.0, 70000.0],
            "waktu": [datetime(2026, 12, 28, 9, 0)] * 3,
        }).write_parquet("bronze_transaksi.parquet")
    kontrak = yaml.safe_load(open("contract.yaml"))
    df = pl.read_parquet("bronze_transaksi.parquet")
    masalah = validasi(df, kontrak)
    if masalah:
        raise SystemExit("Kontrak dilanggar: " + "; ".join(masalah))
    print("Kontrak dipenuhi")
