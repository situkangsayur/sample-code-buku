"""Membangkitkan bronze sintetis untuk Bab 6: transaksi harian dan profil nasabah.

  python siapkan_bronze.py 2026-11-01            -> satu partisi tgl
  python siapkan_bronze.py 2026-11-01 --sabotase -> + 50 trx_id ganda dan 1 akad tidak valid
Partisi ditulis UTUH (overwrite), sehingga menjalankan ulang aman (idempotent).
"""
import argparse
import datetime as dt
import pathlib
import shutil

import numpy as np
import polars as pl

AKAD = ["murabahah", "musyarakah", "mudharabah", "ijarah", "wadiah"]
BRONZE = pathlib.Path("data/bronze")


def tulis_utuh(df: pl.DataFrame, folder: pathlib.Path) -> None:
    tmp = folder.with_name(folder.name + ".tmp")
    shutil.rmtree(tmp, ignore_errors=True)
    tmp.mkdir(parents=True)
    df.write_parquet(tmp / "part-0.parquet")
    shutil.rmtree(folder, ignore_errors=True)
    tmp.rename(folder)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("tgl")
    ap.add_argument("--baris", type=int, default=20_000)
    ap.add_argument("--sabotase", action="store_true")
    a = ap.parse_args()
    tgl = dt.date.fromisoformat(a.tgl)
    rng = np.random.default_rng(int(tgl.strftime("%Y%m%d")))   # deterministik per tanggal
    n_nas = 2_000
    # profil nasabah: segmen berubah sesekali -> bahan snapshot SCD tipe 2
    nas = pl.DataFrame({
        "nasabah_id": np.arange(1, n_nas + 1),
        "cabang_id": rng.integers(1, 7, n_nas),
        "segmen": rng.choice(["ritel", "prioritas", "umkm"], n_nas),
        "updated_at": [dt.datetime.combine(tgl - dt.timedelta(days=1), dt.time(22))] * n_nas,
    })
    tulis_utuh(nas, BRONZE / "nasabah" / f"tgl={tgl}")
    n = a.baris
    trx = pl.DataFrame({
        "trx_id": [f"T{tgl:%Y%m%d}{i:07d}" for i in range(n)],
        "rekening_id": rng.integers(1, n_nas + 1, n),
        "jenis_akad": rng.choice(AKAD, n),
        "nominal": rng.integers(10_000, 5_000_000, n).astype(str),
        "waktu_trx": [dt.datetime.combine(tgl, dt.time()) + dt.timedelta(seconds=int(s))
                      for s in rng.integers(0, 86_400, n)],
    })
    if a.sabotase:
        trx = pl.concat([trx, trx.head(50)])                       # 50 trx_id ganda
        trx = trx.with_columns(pl.when(pl.int_range(pl.len()) == 0)
                               .then(pl.lit("riba")).otherwise(pl.col("jenis_akad"))
                               .alias("jenis_akad"))               # akad tidak valid
    trx = trx.with_columns(pl.lit(dt.datetime.now()).alias("_ingest_ts"),
                           pl.lit("core.transaksi").alias("_source"),
                           pl.lit(f"{tgl}").alias("_batch_id"))
    tulis_utuh(trx, BRONZE / "transaksi" / f"tgl={tgl}")
    print(f"bronze {tgl}: {trx.height} transaksi{' (SABOTASE)' if a.sabotase else ''}")


if __name__ == "__main__":
    main()
