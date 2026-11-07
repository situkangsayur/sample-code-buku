"""Total nominal per kanal dengan Polars (Kode 1.4, versi Python)."""
import polars as pl

hasil = (
    pl.scan_parquet("../lake/silver/transaksi.parquet")  # lazy: belum membaca apa pun
    .group_by("kanal")
    .agg(pl.col("nominal").sum().alias("total"), pl.len().alias("jml"))
    .sort("total", descending=True)
    .collect()                                          # di sini rencana dijalankan
)
print(hasil)
