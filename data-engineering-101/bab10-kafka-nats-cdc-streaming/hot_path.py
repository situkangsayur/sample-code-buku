"""Kode 10.7 dan 10.8: hot path dengan Spark Structured Streaming.

1. Membaca topik CDC bank.public.transaksi dari Redpanda/Kafka.
2. Mengurai amplop Debezium dan menulis setiap event ke bronze Iceberg (append).
3. Menghitung aturan fraud (window 1 menit, watermark 2 menit) dan menulis
   peringatan ke ClickHouse lewat foreachBatch (sink idempotent).

Pemakaian (dari folder ini, setelah docker compose up dan daftar_connector.py):
    python hot_path.py
    LAKE_ROOT=file:///tmp/lake python hot_path.py     # tanpa object storage, di disk lokal

Dependensi JAR (Kafka, Iceberg, hadoop-aws) diunduh otomatis lewat
spark.jars.packages; versinya harus cocok dengan PySpark 3.5 / Scala 2.12.
"""
import os

import clickhouse_connect
from pyspark.sql import SparkSession, functions as F, types as T

BROKER = os.getenv("KAFKA_BROKER", "localhost:19092")
LAKE_ROOT = os.getenv("LAKE_ROOT", "s3a://lake")          # bucket "lake" di RustFS
S3_ENDPOINT = os.getenv("S3_ENDPOINT", "http://localhost:9000")
S3_ACCESS_KEY = os.getenv("S3_ACCESS_KEY", "labadmin")
S3_SECRET_KEY = os.getenv("S3_SECRET_KEY", "rahasia_lab")
CH_HOST = os.getenv("CLICKHOUSE_HOST", "localhost")

PAKET = ",".join([
    "org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.1",
    "org.apache.iceberg:iceberg-spark-runtime-3.5_2.12:1.6.1",
    "org.apache.hadoop:hadoop-aws:3.3.4",
])

# --- katalog lake: Iceberg dengan katalog Hadoop di LAKE_ROOT/warehouse ---
spark = (SparkSession.builder.appName("hot-path")
         .config("spark.jars.packages", PAKET)
         .config("spark.sql.extensions",
                 "org.apache.iceberg.spark.extensions.IcebergSparkSessionExtensions")
         .config("spark.sql.catalog.lake", "org.apache.iceberg.spark.SparkCatalog")
         .config("spark.sql.catalog.lake.type", "hadoop")
         .config("spark.sql.catalog.lake.warehouse", f"{LAKE_ROOT}/warehouse")
         .config("spark.hadoop.fs.s3a.endpoint", S3_ENDPOINT)
         .config("spark.hadoop.fs.s3a.path.style.access", "true")
         .config("spark.hadoop.fs.s3a.access.key", S3_ACCESS_KEY)
         .config("spark.hadoop.fs.s3a.secret.key", S3_SECRET_KEY)
         .config("spark.sql.session.timeZone", "UTC")
         .config("spark.sql.shuffle.partitions", "4")      # cukup untuk laptop
         # state besar: pakai RocksDB, bukan memori JVM
         .config("spark.sql.streaming.stateStore.providerClass",
                 "org.apache.spark.sql.execution.streaming.state.RocksDBStateStoreProvider")
         .getOrCreate())
spark.sparkContext.setLogLevel("WARN")

# --- Kode 10.7: membaca CDC dan menulis bronze ---
AFTER = T.StructType([
    T.StructField("id_trx", T.StringType()),
    T.StructField("id_rekening", T.StringType()),
    T.StructField("id_perangkat", T.StringType()),
    T.StructField("nominal", T.LongType()),
    T.StructField("waktu", T.LongType())])          # mikrodetik epoch dari Debezium
ENV = T.StructType([T.StructField("after", AFTER),
                    T.StructField("op", T.StringType()),
                    T.StructField("ts_ms", T.LongType())])

raw = (spark.readStream.format("kafka")
       .option("kafka.bootstrap.servers", BROKER)
       .option("subscribe", "bank.public.transaksi")
       .option("startingOffsets", "earliest").load())

trx = (raw.select(F.from_json(F.col("value").cast("string"), ENV).alias("e"))
          .where(F.col("e.op").isin("c", "r"))       # insert dan snapshot awal
          .select("e.after.*", "e.ts_ms")
          .withColumn("event_time", F.expr("timestamp_micros(waktu)")))

# tabel bronze dibuat sekali; streaming toTable lalu hanya menambah
spark.sql("CREATE NAMESPACE IF NOT EXISTS lake.bronze")
spark.sql("""
    CREATE TABLE IF NOT EXISTS lake.bronze.transaksi_cdc (
        id_trx STRING, id_rekening STRING, id_perangkat STRING,
        nominal BIGINT, waktu BIGINT, ts_ms BIGINT, event_time TIMESTAMP)
    USING iceberg PARTITIONED BY (days(event_time))""")

bronze = (trx.writeStream.format("iceberg").outputMode("append")
          .option("checkpointLocation", f"{LAKE_ROOT}/ckpt/bronze_trx")
          .trigger(processingTime="10 seconds")
          .toTable("lake.bronze.transaksi_cdc"))

# --- Kode 10.8: aturan fraud ke ClickHouse ---
agregat = (trx
    .withWatermark("event_time", "2 minutes")
    .groupBy(F.window("event_time", "1 minute"), "id_rekening")
    .agg(F.count("*").alias("n_trx"),
         F.sum("nominal").alias("total"),
         F.approx_count_distinct("id_perangkat").alias("n_perangkat"))
    .where("n_trx > 5 AND n_perangkat > 1"))


def ke_clickhouse(batch_df, batch_id):
    """Dipanggil sekali per micro-batch. Bila batch diulang setelah restart,
    baris yang sama ditulis ulang dan ReplacingMergeTree menggabungkannya."""
    pdf = (batch_df.select(F.col("window.start").alias("window_start"),
                           "id_rekening", "n_trx", "total", "n_perangkat")
                   .toPandas())
    if len(pdf):
        ch = clickhouse_connect.get_client(host=CH_HOST, password="rahasia_lab")
        ch.insert_df("peringatan_fraud", pdf)
        print(f"batch {batch_id}: {len(pdf)} peringatan ditulis ke ClickHouse")


hot = (agregat.writeStream.outputMode("update")
       .foreachBatch(ke_clickhouse)
       .option("checkpointLocation", f"{LAKE_ROOT}/ckpt/fraud_hot")
       .start())

print("hot path berjalan; Spark UI di http://localhost:4040 (tab Structured Streaming)")
spark.streams.awaitAnyTermination()
