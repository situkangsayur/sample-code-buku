"""Masalah berkas kecil: data sama, 1 berkas besar vs 1.000 berkas kecil (Kode 3.x).

Berjalan di disk lokal; efeknya jauh lebih besar di object storage karena
setiap berkas berarti beberapa permintaan HTTP.
"""
import os
import shutil
import statistics
import time

import duckdb

from bangkit_data import bangkit

df = bangkit(1_000_000)
con = duckdb.connect()
con.register("df", df.to_arrow())

shutil.rmtree("data/kecil", ignore_errors=True)
os.makedirs("data/kecil", exist_ok=True)
con.sql("COPY df TO 'data/besar.parquet' (FORMAT PARQUET)")
n = 1000
per = df.height // n
for i in range(n):
    df.slice(i * per, per).write_parquet(f"data/kecil/part-{i:04d}.parquet")


def ukur(pola: str, ulang: int = 5) -> float:
    w = []
    for _ in range(ulang):
        t = time.perf_counter()
        con.sql(f"SELECT kanal, SUM(nominal) FROM read_parquet('{pola}') GROUP BY kanal").fetchall()
        w.append(time.perf_counter() - t)
    return statistics.median(w)


print(f"1 berkas besar    : {ukur('data/besar.parquet'):.3f} s")
print(f"{n} berkas kecil : {ukur('data/kecil/*.parquet'):.3f} s")
