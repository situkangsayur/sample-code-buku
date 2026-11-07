"""Kode 4.24: membaca tabel Iceberg (gold) dan Delta dari DuckDB.
Jalankan medallion.py dan delta_merge.py lebih dulu."""
import duckdb

from katalog import buka_katalog

gold = buka_katalog().load_table("gold.trx_harian_cabang")
con = duckdb.connect()
con.sql("INSTALL iceberg; LOAD iceberg; INSTALL delta; LOAD delta;")

# Iceberg: tunjuk metadata.json terbaru yang diberikan katalog
print(con.sql(f"""
    SELECT cabang, SUM(jml_trx) AS trx, SUM(total) AS total
    FROM iceberg_scan('{gold.metadata_location}')
    GROUP BY cabang ORDER BY total DESC LIMIT 3"""))

# snapshot yang tersedia untuk time travel
print(con.sql(f"""SELECT sequence_number, snapshot_id
    FROM iceberg_snapshots('{gold.metadata_location}')"""))

# Delta: cukup tunjuk folder tabel
print(con.sql("SELECT * FROM delta_scan('delta/silver_trx') ORDER BY id_trx"))
