"""Job bronze -> silver dengan fitur keamanan Spark dan tokenisasi Pandas UDF.
Nama opsi dapat berbeda antarversi Spark/Hadoop; cocokkan dengan dokumentasi.
Kredensial S3A dan TOKEN_KEY diisi dari Vault ke environment.
"""
import hashlib
import hmac
import os

import pandas as pd
from pyspark.sql import SparkSession
from pyspark.sql.functions import pandas_udf

spark = (SparkSession.builder
         .appName("bronze-ke-silver")
         .config("spark.authenticate", "true")
         .config("spark.network.crypto.enabled", "true")
         .config("spark.io.encryption.enabled", "true")
         .config("spark.hadoop.fs.s3a.endpoint", os.environ.get("S3_ENDPOINT", "https://rustfs:9000"))
         .config("spark.hadoop.fs.s3a.connection.ssl.enabled", "true")
         .config("spark.hadoop.fs.s3a.path.style.access", "true")
         .getOrCreate())

KUNCI = os.environ["TOKEN_KEY"].encode()


@pandas_udf("string")
def token(s: pd.Series) -> pd.Series:
    return s.map(lambda v: None if v is None else
                 "tok_" + hmac.new(KUNCI, v.encode(), hashlib.sha256).hexdigest()[:20])


bronze = spark.read.parquet("s3a://bronze/nasabah/")
silver = (bronze
          .withColumn("nik_token", token("nik"))
          .withColumn("hp_token", token("no_hp"))
          .drop("nik", "no_hp", "nama"))          # PII asli tidak sampai silver
silver.write.mode("overwrite").parquet("s3a://silver/nasabah/")
spark.stop()
