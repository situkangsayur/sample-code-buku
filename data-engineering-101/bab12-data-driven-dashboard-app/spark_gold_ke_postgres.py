"""Memuat agregat gold (Iceberg) ke PostgreSQL serving secara idempotent.

Prasyarat: Spark dengan katalog Iceberg bernama 'lake' dan driver JDBC PostgreSQL,
mis. spark-submit --packages org.postgresql:postgresql:42.7.4 ...
Variabel lingkungan PG_USER dan PG_PASSWORD diisi dari secret manager.
"""
import os

from pyspark.sql import SparkSession, functions as F

spark = SparkSession.builder.appName("gold-ke-serving").getOrCreate()

harian = (spark.table("lake.gold.fct_transaksi")
          .groupBy("tanggal", "kode_cabang", "kanal")
          .agg(F.sum("nominal").alias("nominal"),
               F.countDistinct("nasabah_token").alias("nasabah_aktif"),
               F.max("updated_at").alias("data_per")))

(harian.write.format("jdbc")
 .option("url", os.environ.get("PG_URL", "jdbc:postgresql://serving:5432/gold"))
 .option("dbtable", "public.fct_transaksi_harian")
 .option("user", os.environ["PG_USER"])
 .option("password", os.environ["PG_PASSWORD"])
 .option("truncate", "true")      # kosongkan lalu isi: GRANT dan RLS tetap
 .mode("overwrite").save())
spark.stop()
