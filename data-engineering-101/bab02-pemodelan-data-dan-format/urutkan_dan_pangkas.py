"""Pengaruh pengurutan data terhadap predicate pushdown (Kode 2.x).

Data yang sama ditulis dua kali: acak dan terurut menurut waktu. Lalu dihitung
berapa row group yang dapat dilewati untuk filter satu minggu.
"""
import datetime as dt
import os

import duckdb
import pyarrow.parquet as pq

from bangkit_data import bangkit

os.makedirs("data", exist_ok=True)
con = duckdb.connect()
con.register("df", bangkit(1_000_000).to_arrow())
con.sql("COPY (SELECT * FROM df ORDER BY random()) TO 'data/acak.parquet' "
        "(FORMAT PARQUET, ROW_GROUP_SIZE 100000)")
con.sql("COPY (SELECT * FROM df ORDER BY waktu) TO 'data/urut.parquet' "
        "(FORMAT PARQUET, ROW_GROUP_SIZE 100000)")

awal, akhir = dt.datetime(2026, 10, 1), dt.datetime(2026, 10, 8)
for f in ["data/acak.parquet", "data/urut.parquet"]:
    md = pq.ParquetFile(f).metadata
    idx = md.schema.to_arrow_schema().get_field_index("waktu")
    dibaca = 0
    for r in range(md.num_row_groups):
        st = md.row_group(r).column(idx).statistics
        # row group harus dibaca bila rentang [min, max] bersinggungan dengan filter
        if st.max >= awal and st.min < akhir:
            dibaca += 1
    print(f"{f:<20} row group dibaca: {dibaca} dari {md.num_row_groups}")
