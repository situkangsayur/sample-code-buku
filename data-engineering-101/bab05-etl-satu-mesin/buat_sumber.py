"""Membuat basis data sumber tiruan (DuckDB) yang meniru tabel core.transaksi.

Di produksi sumbernya PostgreSQL inti; di sini cukup berkas DuckDB agar
contoh incremental load dapat dijalankan tanpa server.
"""
import duckdb

con = duckdb.connect("data/core.duckdb")
con.sql("""
CREATE OR REPLACE TABLE transaksi AS
SELECT id_trx, rek, kanal, TRY_CAST(nominal AS BIGINT) AS nominal,
       CAST(waktu AS TIMESTAMP) AS updated_at
FROM read_parquet('data/bronze/trx/*/*.parquet')
QUALIFY row_number() OVER (PARTITION BY id_trx) = 1
""")
print(con.sql("SELECT count(*), min(updated_at), max(updated_at) FROM transaksi").fetchall())
