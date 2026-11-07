"""Kode 9.11: baseline satu mesin dengan DuckDB untuk kueri gold yang sama.

    python baseline_duckdb.py data
"""
import os
import sys
import time

import duckdb

base = sys.argv[1] if len(sys.argv) > 1 else "data"
os.makedirs(f"{base}/gold", exist_ok=True)
con = duckdb.connect()
t0 = time.perf_counter()
con.sql(f"""
    COPY (
      SELECT t.tanggal, c.wilayah, c.cabang,
             SUM(t.nominal) AS total, COUNT(DISTINCT t.id_nasabah) AS nasabah_aktif
      FROM read_parquet('{base}/silver/transaksi/*.parquet') t
      JOIN read_parquet('{base}/silver/cabang/*.parquet')    c USING (id_cabang)
      WHERE t.status = 'SUKSES'
      GROUP BY ALL
    ) TO '{base}/gold/harian_duckdb' (FORMAT parquet, PARTITION_BY (tanggal), OVERWRITE_OR_IGNORE)
""")
print(f"DuckDB: {time.perf_counter() - t0:.2f} s")
