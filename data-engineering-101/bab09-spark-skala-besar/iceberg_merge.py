"""Kode 9.7 dan 9.8: MERGE, dynamic partition overwrite, dan perawatan tabel Iceberg.

Memakai katalog Iceberg tipe hadoop di folder lokal (cukup untuk latihan).
    spark-submit --packages org.apache.iceberg:iceberg-spark-runtime-3.5_2.12:1.6.1 \
      iceberg_merge.py data
Sesuaikan versi iceberg-spark-runtime dengan versi Spark Anda (3.5 atau 4.0).
"""
import os
import sys

from pyspark.sql import SparkSession
from pyspark.sql import functions as F

base = sys.argv[1] if len(sys.argv) > 1 else os.environ.get("BASE", "data")
gudang = os.path.abspath(os.path.join(base, "lakehouse"))
spark = (SparkSession.builder.appName("iceberg-merge")
         .config("spark.sql.extensions",
                 "org.apache.iceberg.spark.extensions.IcebergSparkSessionExtensions")
         .config("spark.sql.catalog.lake", "org.apache.iceberg.spark.SparkCatalog")
         .config("spark.sql.catalog.lake.type", "hadoop")
         .config("spark.sql.catalog.lake.warehouse", gudang)
         .getOrCreate())

trx = (spark.read.parquet(f"{base}/silver/transaksi/")
       .withColumn("tanggal", F.to_date("tanggal")))
spark.sql("CREATE NAMESPACE IF NOT EXISTS lake.silver")
spark.sql("CREATE NAMESPACE IF NOT EXISTS lake.gold")
trx.writeTo("lake.silver.transaksi").partitionedBy(F.days("tanggal")).createOrReplace()

# data koreksi: 1000 transaksi lama berubah nominal + 10 transaksi baru
koreksi = (trx.limit(1000).withColumn("nominal", F.col("nominal") + 1)
           .unionByName(trx.limit(10).withColumn("id_trx", F.col("id_trx") + 10**12)))
koreksi.createOrReplaceTempView("koreksi_hari_ini")

spark.sql("""
MERGE INTO lake.silver.transaksi t
USING koreksi_hari_ini k
ON t.id_trx = k.id_trx
WHEN MATCHED THEN UPDATE SET *
WHEN NOT MATCHED THEN INSERT *""")

spark.sql("""CREATE TABLE IF NOT EXISTS lake.gold.harian_cabang
             (tanggal DATE, id_cabang BIGINT, total DOUBLE) USING iceberg
             PARTITIONED BY (tanggal)""")
spark.conf.set("spark.sql.sources.partitionOverwriteMode", "dynamic")
spark.sql("""
INSERT OVERWRITE lake.gold.harian_cabang
SELECT tanggal, id_cabang, SUM(nominal) AS total
FROM lake.silver.transaksi
WHERE tanggal = DATE '2026-10-06'
GROUP BY tanggal, id_cabang""")

# perawatan (Kode 9.8)
spark.sql("""CALL lake.system.rewrite_data_files(
  table => 'silver.transaksi', strategy => 'sort', sort_order => 'id_cabang',
  options => map('target-file-size-bytes', '268435456'))""").show()
spark.sql("""CALL lake.system.expire_snapshots(
  table => 'silver.transaksi', older_than => current_timestamp(), retain_last => 1)""").show()
spark.sql("SELECT COUNT(*) FROM lake.silver.transaksi.snapshots").show()
spark.stop()
