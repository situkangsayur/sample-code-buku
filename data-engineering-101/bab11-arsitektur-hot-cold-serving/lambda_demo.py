"""Menjalankan Kode 11.2 (lambda_merge.sql) di DuckDB dengan data sintetis.

batch_view_cabang_jam mencakup 00.00-14.00; realtime_view_cabang_menit berisi
data sejak 13.00 (sebagian tumpang tindih dengan batch, sengaja). Kueri hanya
mengambil real-time view sejak batas batch, sehingga tidak ada hitungan ganda.
Jalankan: python lambda_demo.py
"""
from pathlib import Path
import duckdb

con = duckdb.connect()
con.execute("""
CREATE TABLE batch_meta AS SELECT TIMESTAMP '2026-10-20 14:00' AS tercakup_sampai;
CREATE TABLE batch_view_cabang_jam AS
  SELECT TIMESTAMP '2026-10-20 00:00' + INTERVAL (h) HOUR AS jam, c AS cabang,
         10 AS jumlah, 1000000 AS total
  FROM range(14) t(h), (VALUES ('BDG'), ('JKT')) v(c);
CREATE TABLE realtime_view_cabang_menit AS
  SELECT TIMESTAMP '2026-10-20 13:00' + INTERVAL (m) MINUTE AS menit, c AS cabang,
         1 AS jumlah, 100000 AS total
  FROM range(180) t(m), (VALUES ('BDG'), ('JKT')) v(c);
""")
sql = Path(__file__).with_name("lambda_merge.sql").read_text()
print(con.execute(sql).df())
# harapan: 14 jam x 10 = 140 dari batch + 120 menit (14.00-16.00) x 1 = 120 -> 260 per cabang
