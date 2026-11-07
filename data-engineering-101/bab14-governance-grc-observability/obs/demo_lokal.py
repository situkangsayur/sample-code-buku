"""Demo lokal: membangkitkan transaksi sintetis 5 pekan, lalu menghilangkan 40%
baris pada jam terakhir (kasus format tanggal) agar pemeriksaan volume menyala."""
import os
import sys

import duckdb
import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(__file__))
from cek_tabel import kirim, periksa  # noqa: E402

rng = np.random.default_rng(1)
akhir = pd.Timestamp.now(tz="UTC").floor("h").tz_localize(None)  # UTC naif
jam = pd.date_range(akhir - pd.Timedelta(days=35), akhir, freq="h", inclusive="both")
baris = []
for j in jam:
    dasar = 50_000 if 8 <= j.hour <= 20 else 8_000
    n = int(rng.normal(dasar, 0.03 * dasar))      # pola musiman per jam
    if j == akhir - pd.Timedelta(hours=1):
        n = int(n * 0.6)                       # 40% baris hilang
    menit = 0 if j == akhir else 30
    baris.append(pd.DataFrame({"event_time": [j + pd.Timedelta(minutes=menit)] * max(n, 1)}))
df = pd.concat(baris)
con = duckdb.connect()
con.sql("SET TimeZone = 'UTC'")
con.register("trx", df)
con.sql("CREATE TABLE silver_transaksi AS SELECT * FROM trx")
m = periksa(con, "silver_transaksi")
kirim(m, "silver.transaksi") if m else print("OK")
