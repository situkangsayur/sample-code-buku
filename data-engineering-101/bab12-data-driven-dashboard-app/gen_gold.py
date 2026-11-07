"""Membangkitkan gold.duckdb sintetis untuk contoh Bab 12.

Tabel: fct_transaksi_harian(tanggal, kode_cabang, kanal, nominal, nasabah_aktif, data_per)
       label_fraud(trx_id, label, alasan, analis, waktu)  -- tabel operasional
"""
import datetime as dt

import duckdb
import numpy as np
import pandas as pd

rng = np.random.default_rng(42)
hari = pd.date_range("2026-09-01", "2026-12-28", freq="D")
baris = []
for t in hari:
    for cab, skala in [("BGR", 1.0), ("BDG", 1.4), ("DPK", 0.8)]:
        for kanal in ["mobile", "atm", "qris"]:
            n = rng.poisson(1200 * skala)
            baris.append((t.date(), cab, kanal,
                          float(rng.lognormal(12, 1.1, n).sum().round()),
                          int(n * 0.6)))
df = pd.DataFrame(baris, columns=["tanggal", "kode_cabang", "kanal",
                                  "nominal", "nasabah_aktif"])
df["data_per"] = dt.datetime(2026, 12, 28, 5, 10)

con = duckdb.connect("gold.duckdb")
con.execute("CREATE OR REPLACE TABLE fct_transaksi_harian AS SELECT * FROM df")
con.execute("""CREATE TABLE IF NOT EXISTS label_fraud(
    trx_id VARCHAR, label VARCHAR, alasan VARCHAR,
    analis VARCHAR, waktu TIMESTAMP)""")
print(con.sql("SELECT kode_cabang, count(*), sum(nominal) FROM fct_transaksi_harian GROUP BY 1"))
con.close()
