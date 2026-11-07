"""Kode 9.2 dan eksperimen join: AQE, broadcast vs sort-merge.

    python gen_data.py --baris 2000000 --keluar data
    spark-submit aqe_join.py data
"""
import os
import sys
import time

from pyspark.sql import SparkSession
from pyspark.sql import functions as F

base = sys.argv[1] if len(sys.argv) > 1 else os.environ.get("BASE", "data")
spark = SparkSession.builder.appName("aqe-join").getOrCreate()

# Kode 9.2: konfigurasi AQE yang umum disentuh
spark.conf.set("spark.sql.adaptive.enabled", "true")
spark.conf.set("spark.sql.adaptive.coalescePartitions.enabled", "true")
spark.conf.set("spark.sql.adaptive.advisoryPartitionSizeInBytes", "128m")
spark.conf.set("spark.sql.adaptive.skewJoin.enabled", "true")
spark.conf.set("spark.sql.adaptive.skewJoin.skewedPartitionFactor", "5")
spark.conf.set("spark.sql.adaptive.skewJoin.skewedPartitionThresholdInBytes", "256m")

trx = spark.read.parquet(f"{base}/silver/transaksi/")
nsb = spark.read.parquet(f"{base}/silver/nasabah/")


def laporan():
    return (trx.filter(F.col("tanggal") >= "2026-10-01")
               .join(nsb, "id_nasabah")
               .groupBy("tanggal", "cabang")
               .agg(F.sum("nominal").alias("total")))


for nama, ambang in [("broadcast otomatis", "10m"), ("paksa sort-merge", "-1")]:
    spark.conf.set("spark.sql.autoBroadcastJoinThreshold", ambang)
    df = laporan()
    print(f"\n===== {nama} =====")
    df.explain()
    t0 = time.perf_counter()
    df.write.mode("overwrite").format("noop").save()   # jalankan tanpa menulis
    print(f"waktu: {time.perf_counter() - t0:.2f} s")
spark.stop()
