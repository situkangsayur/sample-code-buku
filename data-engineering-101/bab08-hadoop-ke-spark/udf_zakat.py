"""Kode 8.6: UDF biasa vs Pandas UDF vs fungsi bawaan (ilustrasi zakat 2,5 persen).

    spark-submit udf_zakat.py data
Contoh zakat hanya ilustrasi pemrograman, bukan aturan perhitungan zakat yang lengkap.
"""
import os
import sys
import time

import pandas as pd
from pyspark.sql import SparkSession
from pyspark.sql import functions as F

NISAB = 85_000_000.0  # nilai ilustrasi dalam rupiah

base = sys.argv[1] if len(sys.argv) > 1 else os.environ.get("BASE", "data")
spark = SparkSession.builder.appName("udf-zakat").getOrCreate()
rekening = spark.read.parquet(f"{base}/silver/rekening/")


@F.udf("double")
def zakat_udf(saldo):
    return saldo * 0.025 if saldo >= NISAB else 0.0


@F.pandas_udf("double")
def zakat_vec(saldo: pd.Series) -> pd.Series:
    return (saldo * 0.025).where(saldo >= NISAB, 0.0)


zakat_bawaan = F.when(F.col("saldo") >= NISAB, F.col("saldo") * 0.025).otherwise(0.0)

for nama, kolom in [("udf biasa", zakat_udf("saldo")),
                    ("pandas udf", zakat_vec("saldo")),
                    ("fungsi bawaan", zakat_bawaan)]:
    t0 = time.time()
    total = rekening.select(kolom.alias("z")).agg(F.sum("z")).first()[0]
    print(f"{nama:14s} total={total:,.0f}  waktu={time.time() - t0:.2f} s")
spark.stop()
