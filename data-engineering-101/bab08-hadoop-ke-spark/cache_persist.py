"""Kode 8.2: menyimpan hasil antara yang dipakai dua action.

    spark-submit cache_persist.py data
Untuk RustFS (S3): BASE=s3a:// spark-submit ... (lihat README).
"""
import os
import sys

from pyspark import StorageLevel
from pyspark.sql import SparkSession
from pyspark.sql import functions as F

base = sys.argv[1] if len(sys.argv) > 1 else os.environ.get("BASE", "data")
spark = SparkSession.builder.appName("cache-persist").getOrCreate()
trx = spark.read.parquet(f"{base}/silver/transaksi/")
cabang = spark.read.parquet(f"{base}/silver/cabang/")

bersih = (trx.filter(F.col("status") == "SUKSES")
             .join(F.broadcast(cabang), "id_cabang"))
bersih.persist(StorageLevel.MEMORY_AND_DISK)

harian = bersih.groupBy("tanggal").agg(F.sum("nominal").alias("total"))
per_cab = bersih.groupBy("cabang").agg(F.count("*").alias("jumlah"))
harian.write.mode("overwrite").parquet(f"{base}/gold/harian/")   # hitung + simpan
per_cab.write.mode("overwrite").parquet(f"{base}/gold/cabang/")  # pakai simpanan
bersih.unpersist()
spark.stop()
