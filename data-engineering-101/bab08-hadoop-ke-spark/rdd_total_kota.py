"""Kode 8.1: total transaksi per kota dengan API RDD.

    python gen_data.py --baris 1000000
    spark-submit rdd_total_kota.py data/trx.csv
"""
import sys

from pyspark.sql import SparkSession

spark = SparkSession.builder.appName("rdd-total-kota").getOrCreate()
sc = spark.sparkContext
jalur = sys.argv[1] if len(sys.argv) > 1 else "data/trx.csv"

baris = sc.textFile(jalur)                          # transformation (lazy)


def urai(s):
    kota, nominal, status = s.split(",")
    return kota, float(nominal), status


pasangan = (baris.map(urai)                          # narrow
                 .filter(lambda t: t[2] == "SUKSES")  # narrow
                 .map(lambda t: (t[0], t[1])))       # narrow
total = pasangan.reduceByKey(lambda a, b: a + b)     # wide: shuffle (dengan combiner)

for kota, nilai in sorted(total.collect()):          # action: kerja dimulai
    print(kota, nilai)

# bandingkan dengan groupByKey yang mengirim semua nilai mentah
boros = pasangan.groupByKey().mapValues(sum)
print("hasil sama:", dict(boros.collect()) == dict(total.collect()))
print(total.toDebugString().decode())               # lihat lineage dan batas stage
spark.stop()
