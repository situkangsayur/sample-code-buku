"""Lima tahap data engineering lifecycle dalam satu berkas (Kode 1.2).

generation -> ingestion -> storage -> transformation -> serving,
semuanya di satu laptop dengan Polars dan DuckDB.
"""
import os
from datetime import datetime, timezone

import duckdb
import polars as pl

from bangkit_data import bangkit

os.makedirs("lake/bronze", exist_ok=True)
os.makedirs("lake/silver", exist_ok=True)
os.makedirs("lake/gold", exist_ok=True)

# 1. Generation: sistem sumber menghasilkan transaksi (di sini: data sintetis)
sumber = bangkit(200_000)
sumber.write_csv("lake/ekspor_core_banking.csv")

# 2. Ingestion + storage: ambil apa adanya, beri jejak asal, simpan sebagai bronze
raw = pl.read_csv("lake/ekspor_core_banking.csv", infer_schema=False)  # semua teks
raw = raw.with_columns(
    pl.lit(datetime.now(timezone.utc).isoformat()).alias("_ingest_ts"),
    pl.lit("core_banking.csv").alias("_source"),
)
raw.write_parquet("lake/bronze/transaksi.parquet")

# 3. Transformation: bersihkan (silver) lalu agregasi (gold) dengan SQL
con = duckdb.connect()
con.sql("""
COPY (
  SELECT DISTINCT id_transaksi, id_rekening,
         CAST(waktu AS TIMESTAMP)      AS waktu,
         kanal, produk, cabang,
         CAST(nominal AS DECIMAL(18,2)) AS nominal
  FROM 'lake/bronze/transaksi.parquet'
  WHERE nominal IS NOT NULL
) TO 'lake/silver/transaksi.parquet' (FORMAT PARQUET)
""")
con.sql("""
COPY (
  SELECT CAST(waktu AS DATE) AS tanggal, cabang, kanal,
         COUNT(*) AS jml_trx, SUM(nominal) AS total
  FROM 'lake/silver/transaksi.parquet'
  GROUP BY ALL
) TO 'lake/gold/trx_harian.parquet' (FORMAT PARQUET)
""")

# 4. Serving: pertanyaan kepala cabang dijawab dari gold, bukan dari sistem sumber
print(con.sql("""
  SELECT cabang, SUM(total) AS total_jan
  FROM 'lake/gold/trx_harian.parquet'
  WHERE tanggal < DATE '2026-02-01'
  GROUP BY cabang ORDER BY total_jan DESC
"""))
