"""Pembangkit data sintetis bank syariah digital untuk Bab 5.

Menulis layer bronze berpartisi tanggal:
  data/bronze/trx/tanggal=YYYY-MM-DD/part-0.parquet
  data/bronze/nasabah/nasabah.parquet
Data sengaja diberi "kotoran": duplikat id_trx, nominal berupa teks rusak,
dan kanal dengan huruf besar/kecil campur. Semua identitas acak (bukan data nyata).
Pemakaian: python gen_data.py --baris 1_000_000 --hari 7
"""
import argparse
import datetime as dt
import pathlib

import numpy as np
import polars as pl

KANAL = ["qris", "QRIS", "atm", "mobile", "Mobile", "teller"]
CABANG = ["Jakarta", "Bandung", "Bogor", "Surabaya", "Medan", "Makassar"]


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--baris", type=int, default=1_000_000, help="total baris transaksi")
    ap.add_argument("--hari", type=int, default=7)
    ap.add_argument("--nasabah", type=int, default=100_000)
    ap.add_argument("--mulai", default="2026-11-01")
    ap.add_argument("--out", default="data/bronze")
    a = ap.parse_args()
    rng = np.random.default_rng(42)
    out = pathlib.Path(a.out)

    # dimensi nasabah: satu rekening per nasabah
    n = a.nasabah
    nasabah = pl.DataFrame({
        "id_nasabah": np.arange(1, n + 1),
        "rek": [f"71{i:08d}" for i in range(1, n + 1)],
        "cabang": rng.choice(CABANG, n),
        "nik": [f"3201{rng.integers(10**11, 10**12)}" for _ in range(n)],
    })
    (out / "nasabah").mkdir(parents=True, exist_ok=True)
    nasabah.write_parquet(out / "nasabah" / "nasabah.parquet")

    mulai = dt.date.fromisoformat(a.mulai)
    per_hari = a.baris // a.hari
    for h in range(a.hari):
        tgl = mulai + dt.timedelta(days=h)
        idx = rng.integers(0, n, per_hari)
        detik = rng.integers(0, 86_400, per_hari)
        nominal = rng.integers(1_000, 5_000_000, per_hari).astype(str).astype(object)
        rusak = rng.random(per_hari) < 0.001          # 0,1% nominal rusak
        nominal[rusak] = "12a.0"
        df = pl.DataFrame({
            "id_trx": [f"T{tgl:%Y%m%d}{i:09d}" for i in range(per_hari)],
            "id_nasabah": nasabah["id_nasabah"].to_numpy()[idx],
            "rek": nasabah["rek"].to_numpy()[idx],
            "nik": nasabah["nik"].to_numpy()[idx],
            "kanal": rng.choice(KANAL, per_hari),
            "nominal": nominal.tolist(),
            "waktu": [(dt.datetime.combine(tgl, dt.time()) + dt.timedelta(seconds=int(s))).isoformat()
                      for s in detik],
        })
        # duplikat dari jendela tumpang tindih: 0,5% baris muncul dua kali
        dup = df.sample(fraction=0.005, seed=h)
        df = pl.concat([df, dup]).with_columns(
            pl.lit(dt.datetime.now()).alias("_ingest_ts"),
            pl.lit("core.transaksi").alias("_source"))
        d = out / "trx" / f"tanggal={tgl}"
        d.mkdir(parents=True, exist_ok=True)
        df.write_parquet(d / "part-0.parquet")
        print(f"{tgl}: {df.height} baris")


if __name__ == "__main__":
    main()
