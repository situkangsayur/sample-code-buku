"""Schema evolution sederhana pada berkas Parquet (Kode 2.x).

Versi 1 tidak punya kolom kanal; versi 2 menambah kanal dan memperlebar
tipe nominal dari INTEGER ke BIGINT. union_by_name membaca keduanya.
"""
import os

import duckdb

os.makedirs("data/evolusi", exist_ok=True)
con = duckdb.connect()
con.sql("""COPY (SELECT 'T-1' AS id_trx, 250000::INTEGER AS nominal)
  TO 'data/evolusi/v1.parquet' (FORMAT PARQUET)""")
con.sql("""COPY (SELECT 'T-2' AS id_trx, 9000000000::BIGINT AS nominal, 'QRIS' AS kanal)
  TO 'data/evolusi/v2.parquet' (FORMAT PARQUET)""")

# Tanpa union_by_name kolom dicocokkan menurut posisi; dengan union_by_name
# menurut nama. Kolom yang tidak ada terbaca NULL, tipe dilebarkan ke BIGINT.
print(con.sql("""SELECT * FROM read_parquet('data/evolusi/*.parquet', union_by_name = true)
  ORDER BY id_trx"""))
print(con.sql("""DESCRIBE SELECT * FROM read_parquet('data/evolusi/*.parquet',
  union_by_name = true)"""))
