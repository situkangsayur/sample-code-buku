"""Kueri yang sama dengan Polars, DuckDB, dan DataFusion (satu node)."""
import datetime as dt

import duckdb
import polars as pl
from datafusion import SessionContext

TRX, NAS = "data/bronze/trx/", "data/bronze/nasabah/nasabah.parquet"

# 1) Polars lazy
p = (pl.scan_parquet(TRX + "*/*.parquet", hive_partitioning=True)
       .filter(pl.col("tanggal") >= dt.date(2026, 11, 3))
       .join(pl.scan_parquet(NAS).select("id_nasabah", "cabang"), on="id_nasabah")
       .group_by("tanggal", "cabang")
       .agg(pl.col("nominal").cast(pl.Int64, strict=False).sum().alias("total"))
       .sort("tanggal", "cabang")
       .collect(engine="streaming"))

# 2) DuckDB: SQL langsung atas Parquet
d = duckdb.sql(f"""
    SELECT tanggal, cabang, SUM(TRY_CAST(nominal AS BIGINT)) AS total
    FROM read_parquet('{TRX}*/*.parquet', hive_partitioning = true)
    JOIN '{NAS}' USING (id_nasabah)
    WHERE tanggal >= DATE '2026-11-03'
    GROUP BY ALL ORDER BY ALL""").pl()

# 3) DataFusion
ctx = SessionContext()
ctx.sql(f"""CREATE EXTERNAL TABLE trx STORED AS PARQUET
            PARTITIONED BY (tanggal) LOCATION '{TRX}'""")
ctx.register_parquet("nasabah", NAS)
f = ctx.sql("""
    SELECT CAST(tanggal AS DATE) AS tanggal, cabang,
           SUM(TRY_CAST(nominal AS BIGINT)) AS total
    FROM trx JOIN nasabah USING (id_nasabah)
    WHERE CAST(tanggal AS DATE) >= DATE '2026-11-03'
    GROUP BY 1, 2 ORDER BY 1, 2""").to_polars()

print(p.head(), d.head(), f.head(), sep="\n")
print("total sama:", p["total"].sum() == d["total"].sum() == f["total"].sum())
