"""Kode 8.9: job silver ke gold, ringkasan harian per cabang.

Lokal :  spark-submit gold_harian.py data
RustFS: spark-submit --master spark://spark-master:7077 --total-executor-cores 4 \
           --packages org.apache.hadoop:hadoop-aws:3.3.4 \
           --conf spark.hadoop.fs.s3a.endpoint=http://s3:9000 \
           --conf spark.hadoop.fs.s3a.path.style.access=true \
           --conf spark.hadoop.fs.s3a.access.key=$S3_ACCESS_KEY \
           --conf spark.hadoop.fs.s3a.secret.key=$S3_SECRET_KEY \
           gold_harian.py s3a://lake
"""
import os
import sys

from pyspark.sql import SparkSession
from pyspark.sql import functions as F

base = sys.argv[1] if len(sys.argv) > 1 else os.environ.get("BASE", "data")
spark = SparkSession.builder.appName("gold-harian").getOrCreate()
trx = spark.read.parquet(f"{base}/silver/transaksi/")
cab = spark.read.parquet(f"{base}/silver/cabang/")

gold = (trx.filter(F.col("status") == "SUKSES")
           .join(F.broadcast(cab), "id_cabang")
           .groupBy("tanggal", "wilayah", "cabang")
           .agg(F.sum("nominal").alias("total"),
                F.countDistinct("id_nasabah").alias("nasabah_aktif")))
gold.explain()
(gold.write.mode("overwrite")
     .partitionBy("tanggal")
     .parquet(f"{base}/gold/harian_cabang/"))
spark.stop()
