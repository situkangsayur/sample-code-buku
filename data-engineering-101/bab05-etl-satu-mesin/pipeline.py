"""Pipeline bronze -> silver -> gold untuk SATU tanggal, idempotent.

Pemakaian:  TOKEN_SALT=rahasia python pipeline.py 2026-11-02
Jalankan dua kali: jumlah baris dan total gold harus identik.
"""
import os
import pathlib
import shutil
import sys

import duckdb
import polars as pl

D = pathlib.Path("data")


def tulis_partisi(df: pl.DataFrame, tujuan: pathlib.Path) -> None:
    """Tulis ke lokasi sementara, lalu ganti partisi secara utuh."""
    tmp = tujuan.with_name(tujuan.name + ".tmp")
    shutil.rmtree(tmp, ignore_errors=True)
    tmp.mkdir(parents=True)
    df.write_parquet(tmp / "part-0.parquet")
    lama = tujuan.with_name(tujuan.name + ".old")
    if tujuan.exists():
        tujuan.rename(lama)
    tmp.rename(tujuan)                    # rename direktori: atomik di satu filesystem
    shutil.rmtree(lama, ignore_errors=True)


def bronze_ke_silver(tgl: str, salt: str) -> pl.DataFrame:
    bronze = pl.scan_parquet(D / f"bronze/trx/tanggal={tgl}/*.parquet")
    silver = (bronze
        .with_columns(
            pl.col("nominal").cast(pl.Float64, strict=False).cast(pl.Int64, strict=False),
            pl.col("waktu").str.to_datetime(),
            pl.col("kanal").str.to_uppercase())
        .filter(pl.col("nominal").is_not_null() & (pl.col("nominal") > 0))
        .sort("_ingest_ts", descending=True)
        .unique(subset="id_trx", keep="first", maintain_order=True)   # dedup
        .drop("nik")                                                   # PII keluar
        .collect())
    # pseudonymization rekening dengan hash bersalt di DuckDB
    silver = duckdb.execute("""
        SELECT id_trx, sha256(? || rek) AS rek_token, id_nasabah,
               kanal, nominal, waktu, CAST(? AS DATE) AS tanggal
        FROM silver""", [salt, tgl]).pl()
    cek = {
        "baris > 0": silver.height > 0,
        "id unik": silver["id_trx"].n_unique() == silver.height,
        "nominal positif": bool((silver["nominal"] > 0).all()),
        "tanpa rek asli": "rek" not in silver.columns,
    }
    gagal = [k for k, ok in cek.items() if not ok]
    if gagal:
        raise ValueError(f"silver {tgl} gagal: {gagal}")   # gagal dengan keras
    return silver


def silver_ke_gold(tgl: str) -> pl.DataFrame:
    return duckdb.execute(f"""
        SELECT t.tanggal, n.cabang, t.kanal,
               count(*)                    AS jml_trx,
               sum(t.nominal)              AS total_nominal,
               count(DISTINCT t.rek_token) AS rek_aktif
        FROM read_parquet('{D}/silver/trx/tanggal={tgl}/*.parquet') t
        JOIN read_parquet('{D}/bronze/nasabah/nasabah.parquet') n USING (id_nasabah)
        GROUP BY ALL ORDER BY ALL""").pl()


if __name__ == "__main__":
    tgl = sys.argv[1] if len(sys.argv) > 1 else "2026-11-02"
    salt = os.environ.get("TOKEN_SALT", "ganti-di-produksi")
    tulis_partisi(bronze_ke_silver(tgl, salt), D / f"silver/trx/tanggal={tgl}")
    tulis_partisi(silver_ke_gold(tgl), D / f"gold/fakta_trx_harian/tanggal={tgl}")
    g = pl.read_parquet(D / f"gold/fakta_trx_harian/tanggal={tgl}/*.parquet")
    print(f"gold {tgl}: {g.height} baris, total {g['total_nominal'].sum()}")
