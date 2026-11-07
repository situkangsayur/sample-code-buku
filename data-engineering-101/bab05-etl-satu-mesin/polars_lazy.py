"""Eager vs lazy di Polars, dan membaca rencana kueri (explain)."""
import polars as pl

SRC = "data/bronze/trx/*/*.parquet"

# eager: seluruh kolom dibaca dulu, baru disaring
df_eager = pl.read_parquet(SRC).filter(pl.col("kanal") == "QRIS")

# lazy: susun rencana, biarkan optimizer bekerja, baru eksekusi
q = (pl.scan_parquet(SRC, hive_partitioning=True)
       .filter(pl.col("kanal") == "QRIS")
       .select("id_trx", "rek", "nominal", "waktu"))
print(q.explain())          # perhatikan SELECTION dan PROJECT di simpul scan
df_lazy = q.collect()
print(df_eager.height, df_lazy.height)

# expression (cepat) vs map_elements (lambat, Python per baris)
cepat = df_lazy.with_columns(
    (pl.col("nominal").cast(pl.Float64, strict=False) * 1.1).alias("nominal_x"))
print(cepat.head(3))

# streaming engine: memproses per potongan, cocok untuk data > RAM
agg = (pl.scan_parquet(SRC)
         .group_by("kanal").agg(pl.len())
         .collect(engine="streaming"))
print(agg)
