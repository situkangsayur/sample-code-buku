"""Kode 12.x: as-of join DuckDB untuk fitur yang benar secara point-in-time."""
import duckdb

con = duckdb.connect()
con.sql("""
  CREATE TABLE trx AS SELECT * FROM (VALUES
    ('R1', TIMESTAMP '2026-12-01 10:00', 500000),
    ('R1', TIMESTAMP '2026-12-01 10:05', 9000000)) t(rek, ts, nominal);
  CREATE TABLE saldo AS SELECT * FROM (VALUES
    ('R1', TIMESTAMP '2026-12-01 08:00', 12000000),
    ('R1', TIMESTAMP '2026-12-01 10:06', 2500000)) s(rek, ts, saldo);
""")

print("BENAR: as-of join (saldo terakhir sebelum transaksi)")
print(con.sql("""
  SELECT t.rek, t.ts, t.nominal, s.saldo AS saldo_sebelum
  FROM trx t ASOF JOIN saldo s
    ON t.rek = s.rek AND t.ts >= s.ts
  ORDER BY t.ts
"""))

print("SALAH: join ke saldo terbaru (data leakage)")
print(con.sql("""
  SELECT t.rek, t.ts, t.nominal, s.saldo AS saldo_terbaru
  FROM trx t JOIN (SELECT rek, arg_max(saldo, ts) AS saldo FROM saldo GROUP BY rek) s
    USING (rek)
  ORDER BY t.ts
"""))
