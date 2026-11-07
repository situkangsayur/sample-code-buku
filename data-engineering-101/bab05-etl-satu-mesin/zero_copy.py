"""Berpindah engine tanpa salin: PyArrow -> Polars -> DuckDB -> Arrow."""
import duckdb
import polars as pl
import pyarrow.parquet as pq

tbl = pq.read_table("data/bronze/trx/tanggal=2026-11-01/part-0.parquet")  # Arrow
df = pl.from_arrow(tbl)            # Polars memakai buffer Arrow yang sama (umumnya)
res = duckdb.sql("""
    SELECT upper(kanal) AS kanal, count(*) AS n
    FROM df GROUP BY ALL ORDER BY n DESC
""").pl()                          # DuckDB membaca df Polars, hasilnya Polars
out = res.to_arrow()               # kembali ke tabel Arrow
print(res)
print(type(out))
