"""Operasi kubus OLAP dengan SQL DuckDB (Kode 2.x).

roll-up, drill-down, slice, dice, dan pivot di atas data transaksi sintetis.
"""
import duckdb

from bangkit_data import bangkit

con = duckdb.connect()
trx = bangkit(100_000)
con.register("trx_df", trx.to_arrow())
con.sql("""CREATE TABLE trx AS
  SELECT *, year(waktu) AS tahun, quarter(waktu) AS kuartal, month(waktu) AS bulan
  FROM trx_df""")

# Roll-up: dari (cabang, bulan) naik ke (cabang) lalu ke total keseluruhan.
print(con.sql("""
  SELECT cabang, bulan, SUM(nominal) AS total
  FROM trx WHERE bulan <= 2
  GROUP BY ROLLUP (cabang, bulan)
  ORDER BY cabang NULLS LAST, bulan NULLS LAST LIMIT 8"""))

# CUBE: semua kombinasi subtotal produk x kanal sekaligus.
print(con.sql("""
  SELECT produk, kanal, COUNT(*) AS jml, GROUPING(produk, kanal) AS tingkat
  FROM trx GROUP BY CUBE (produk, kanal)
  ORDER BY tingkat, produk, kanal LIMIT 8"""))

# Slice: kunci satu dimensi (kanal = 'QRIS').
print(con.sql("SELECT cabang, SUM(nominal) AS total FROM trx "
              "WHERE kanal = 'QRIS' GROUP BY cabang ORDER BY cabang"))

# Dice: batasi beberapa dimensi sekaligus.
print(con.sql("""SELECT cabang, kanal, SUM(nominal) AS total FROM trx
  WHERE cabang IN ('BGR01','BDG01') AND kanal IN ('mobile','ATM') AND kuartal = 1
  GROUP BY ALL ORDER BY ALL"""))

# Pivot: kanal menjadi kolom.
print(con.sql("""PIVOT (SELECT cabang, kanal, nominal FROM trx)
  ON kanal USING SUM(nominal) GROUP BY cabang ORDER BY cabang"""))
