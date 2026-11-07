"""Kode 9.4: salting pada join dua tabel besar dengan kunci skewed.

Transaksi di-join dengan tabel rekening (terlalu besar untuk di-broadcast) pada
id_rekening. Satu rekening penampung (id 0) memuat 40 persen transaksi.
Garam hanya diberikan pada kunci berat: transaksi kunci berat mendapat garam
acak 0..N-1, dan baris rekening kunci berat digandakan N kali.
Bila sisi lain kecil (mis. dimensi merchant), pakai broadcast join saja.

    spark-submit salting.py 5000000
"""
import sys
import time

from pyspark.sql import SparkSession
from pyspark.sql import functions as F

n_baris = int(sys.argv[1]) if len(sys.argv) > 1 else 5_000_000
n_rekening = 1_000_000
N = 16  # jumlah garam

spark = SparkSession.builder.appName("salting").getOrCreate()
spark.conf.set("spark.sql.autoBroadcastJoinThreshold", "-1")  # paksa shuffle join
spark.conf.set("spark.sql.adaptive.skewJoin.enabled", "false")

# 40 persen transaksi milik rekening penampung 0, sisanya merata
trx = (spark.range(n_baris)
       .withColumn("id_rekening",
                   F.when(F.rand(1) < 0.4, F.lit(0))
                    .otherwise((F.rand(2) * n_rekening).cast("long")))
       .withColumn("nominal", (F.rand(3) * 500_000).cast("long")))
rekening = (spark.range(n_rekening).withColumnRenamed("id", "id_rekening")
            .withColumn("id_cabang", (F.col("id_rekening") % 50).cast("int")))

# kunci berat ditemukan dari distribusi, bukan ditebak
trx.groupBy("id_rekening").count().orderBy(F.desc("count")).show(3)
berat = [0]
kunci_berat = F.col("id_rekening").isin(berat)


def ukur(nama, df):
    t0 = time.perf_counter()
    df.write.mode("overwrite").format("noop").save()
    print(f"{nama:12s}: {time.perf_counter() - t0:.2f} s")


biasa = (trx.join(rekening, "id_rekening")
            .groupBy("id_cabang").agg(F.sum("nominal").alias("total")))
ukur("tanpa garam", biasa)

trx_s = trx.withColumn("garam",
    F.when(kunci_berat, (F.rand(seed=7) * N).cast("int")).otherwise(F.lit(0)))
semua = F.array(*[F.lit(i) for i in range(N)])
rek_s = rekening.withColumn("garam",
    F.explode(F.when(kunci_berat, semua).otherwise(F.array(F.lit(0)))))
print("baris rekening setelah digandakan:", rek_s.count())   # n_rekening + (N - 1)
hasil = (trx_s.join(rek_s, ["id_rekening", "garam"])
              .groupBy("id_cabang").agg(F.sum("nominal").alias("total")))
ukur("dengan garam", hasil)

# hasil kedua cara harus sama
beda = biasa.exceptAll(hasil).count()
print("baris berbeda:", beda)
spark.stop()
