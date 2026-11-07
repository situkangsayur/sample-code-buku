"""Melihat isi berkas Parquet dari dalam: row group, kompresi, statistik (Kode 2.x).

Jalankan ukur_format.py lebih dulu agar data/trx.parquet tersedia.
"""
import pyarrow.parquet as pq

md = pq.ParquetFile("data/trx.parquet").metadata
print("row group:", md.num_row_groups, "| baris:", md.num_rows)
rg = md.row_group(0)
for i in range(rg.num_columns):
    c = rg.column(i)
    st = c.statistics
    print(f"{c.path_in_schema:<14} {c.compression:<6} {str(c.encodings):<40}"
          f" {c.total_compressed_size:>10} / {c.total_uncompressed_size:>10} byte"
          f"  min={st.min if st else None} max={st.max if st else None}")
