"""Kode 4.9, 4.11, 4.13, dan 4.17: Iceberg dengan PySpark: DDL berpartisi, MERGE koreksi,
time travel, rollback, partition evolution, dan prosedur perawatan.

Mode bawaan: Spark lokal + katalog "hadoop" di folder ./lake-spark (tanpa server).
Untuk katalog REST + S3 (docker-compose), jalankan dengan LAKE_CATALOG=rest.
Pemakaian: python spark/medallion_spark.py   (butuh Java 17/21 dan internet
untuk mengunduh paket Iceberg pada run pertama)
"""
import os

from pyspark.sql import SparkSession

PAKET = ["org.apache.iceberg:iceberg-spark-runtime-4.0_2.13:1.10.0"]
b = (SparkSession.builder.appName("bab04-medallion").master("local[2]")
     .config("spark.sql.extensions",
             "org.apache.iceberg.spark.extensions.IcebergSparkSessionExtensions")
     .config("spark.sql.catalog.lake", "org.apache.iceberg.spark.SparkCatalog"))
if os.environ.get("LAKE_CATALOG") == "rest":
    PAKET.append("org.apache.iceberg:iceberg-aws-bundle:1.10.0")
    b = (b.config("spark.sql.catalog.lake.type", "rest")
          .config("spark.sql.catalog.lake.uri", "http://localhost:8181")
          .config("spark.sql.catalog.lake.io-impl",
                  "org.apache.iceberg.aws.s3.S3FileIO")
          .config("spark.sql.catalog.lake.s3.endpoint", "http://localhost:9000")
          .config("spark.sql.catalog.lake.s3.path-style-access", "true"))
else:
    b = (b.config("spark.sql.catalog.lake.type", "hadoop")
          .config("spark.sql.catalog.lake.warehouse", "lake-spark"))
spark = b.config("spark.jars.packages", ",".join(PAKET)).getOrCreate()
sql = lambda q: spark.sql(q)

sql("CREATE NAMESPACE IF NOT EXISTS lake.silver")
sql("DROP TABLE IF EXISTS lake.silver.trx")
sql("""CREATE TABLE lake.silver.trx (
         id_trx BIGINT, id_rekening BIGINT, waktu TIMESTAMP,
         nominal DECIMAL(18,2), kanal STRING, status STRING)
       USING iceberg PARTITIONED BY (days(waktu))""")
sql("""INSERT INTO lake.silver.trx VALUES
       (1, 71, TIMESTAMP '2026-11-01 09:14:05', 250000, 'QRIS', 'SUKSES'),
       (2, 72, TIMESTAMP '2026-11-01 10:01:00',  75000, 'ATM',  'SUKSES'),
       (3, 73, TIMESTAMP '2026-11-02 08:30:00', 1500000,'MOBILE','SUKSES')""")
sid_awal = sql("SELECT snapshot_id FROM lake.silver.trx.snapshots "
               "ORDER BY committed_at DESC LIMIT 1").first()[0]

spark.createDataFrame(
    [(2, 72, "2026-11-01 10:01:00", 75000.0, "ATM", "BATAL"),
     (3, 73, "2026-11-02 08:30:00", 1250000.0, "MOBILE", "SUKSES"),
     (4, 74, "2026-11-02 11:00:00", 40000.0, "AGEN", "SUKSES")],
    "id_trx long, id_rekening long, waktu string, nominal double, "
    "kanal string, status string").selectExpr(
    "id_trx", "id_rekening", "CAST(waktu AS TIMESTAMP) AS waktu",
    "CAST(nominal AS DECIMAL(18,2)) AS nominal", "kanal", "status"
).createOrReplaceTempView("koreksi_harian")

sql("""MERGE INTO lake.silver.trx t
       USING koreksi_harian k ON t.id_trx = k.id_trx
       WHEN MATCHED AND k.status = 'BATAL' THEN DELETE
       WHEN MATCHED THEN UPDATE SET *
       WHEN NOT MATCHED THEN INSERT *""")
sql("SELECT * FROM lake.silver.trx ORDER BY id_trx").show()
sql(f"SELECT COUNT(*) AS n_awal FROM lake.silver.trx VERSION AS OF {sid_awal}").show()
sql("SELECT committed_at, snapshot_id, operation FROM lake.silver.trx.snapshots").show(truncate=False)

# partition evolution: data lama tetap, data baru ikut spec baru
sql("ALTER TABLE lake.silver.trx ADD PARTITION FIELD bucket(16, id_rekening)")

# perawatan tabel (lihat juga spark/rawat_tabel.sql)
sql("CALL lake.system.rewrite_data_files(table => 'silver.trx')").show()
sql(f"CALL lake.system.rollback_to_snapshot('silver.trx', {sid_awal})").show()
sql("SELECT COUNT(*) AS n_setelah_rollback FROM lake.silver.trx").show()
spark.stop()
