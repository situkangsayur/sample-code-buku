"""Kode 8.3 dan 8.4: laporan harian per cabang dengan DataFrame dan dengan SQL.

    spark-submit harian_dataframe.py data
"""
import os
import sys

from pyspark.sql import SparkSession
from pyspark.sql import functions as F

base = sys.argv[1] if len(sys.argv) > 1 else os.environ.get("BASE", "data")
spark = SparkSession.builder.appName("harian").getOrCreate()
trx = spark.read.parquet(f"{base}/silver/transaksi/")
nsb = spark.read.parquet(f"{base}/silver/nasabah/")

harian = (trx
  .filter(F.col("tanggal") >= "2026-10-01")
  .join(nsb, "id_nasabah")
  .groupBy("tanggal", "cabang")
  .agg(F.sum("nominal").alias("total"),
       F.count("*").alias("jumlah")))
harian.explain(mode="formatted")

# versi SQL: rencana fisiknya sama
trx.createOrReplaceTempView("trx")
nsb.createOrReplaceTempView("nasabah")
sql = spark.sql("""
    SELECT t.tanggal, n.cabang, SUM(t.nominal) AS total, COUNT(*) AS jumlah
    FROM trx t JOIN nasabah n USING (id_nasabah)
    WHERE t.tanggal >= '2026-10-01'
    GROUP BY t.tanggal, n.cabang""")
sql.explain()

(harian.write.mode("overwrite")
   .partitionBy("tanggal")
   .parquet(f"{base}/gold/harian_df/"))
spark.stop()
