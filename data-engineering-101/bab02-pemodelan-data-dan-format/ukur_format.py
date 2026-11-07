"""Membandingkan CSV, JSON Lines, dan Parquet: ukuran dan waktu kueri (Kode 2.x).

Pemakaian: python ukur_format.py --baris 2000000
"""
import argparse
import os
import statistics
import time

import duckdb

from bangkit_data import bangkit

ap = argparse.ArgumentParser()
ap.add_argument("--baris", type=int, default=2_000_000)
ap.add_argument("--ulang", type=int, default=5)
a = ap.parse_args()

os.makedirs("data", exist_ok=True)
con = duckdb.connect()
con.register("df", bangkit(a.baris).to_arrow())
con.sql("COPY df TO 'data/trx.csv' (HEADER)")
con.sql("COPY df TO 'data/trx.json' (FORMAT JSON)")           # JSON Lines
con.sql("COPY df TO 'data/trx.parquet' (FORMAT PARQUET, COMPRESSION ZSTD)")

KUERI = {
    "agregasi": "SELECT kanal, SUM(nominal) FROM '{f}' GROUP BY kanal",
    "filter":   "SELECT COUNT(*), SUM(nominal) FROM '{f}' "
                "WHERE waktu >= TIMESTAMP '2026-10-01' AND waktu < TIMESTAMP '2026-10-08'",
}
print(f"{'berkas':<18}{'MB':>8}{'agregasi (s)':>15}{'filter (s)':>12}")
for f in ["data/trx.csv", "data/trx.json", "data/trx.parquet"]:
    hasil = []
    for q in KUERI.values():
        waktu = []
        for _ in range(a.ulang):                 # ulangi, laporkan median
            t = time.perf_counter()
            con.sql(q.format(f=f)).fetchall()
            waktu.append(time.perf_counter() - t)
        hasil.append(statistics.median(waktu))
    mb = os.path.getsize(f) / 2**20
    print(f"{f:<18}{mb:>8.1f}{hasil[0]:>15.3f}{hasil[1]:>12.3f}")
