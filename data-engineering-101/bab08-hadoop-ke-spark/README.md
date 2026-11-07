# Bab 8 - Dari Hadoop ke Spark

Contoh kode lengkap untuk Bab 8 buku *Data Engineering 101*.

| Berkas | Isi | Rujukan di buku |
|---|---|---|
| `gen_data.py` | Pembangkit data sintetis transaksi bank syariah digital (CSV + Parquet silver) | dipakai semua contoh |
| `mapreduce_sim.py` | Simulasi MapReduce satu proses, dengan dan tanpa combiner | Algoritma 8.1-8.2, contoh combiner |
| `rdd_total_kota.py` | Total per kota dengan API RDD, `reduceByKey` vs `groupByKey` | Kode 8.1 |
| `cache_persist.py` | `persist` untuk hasil antara yang dipakai dua kali | Kode 8.2 |
| `harian_dataframe.py` | Laporan harian dengan DataFrame dan SQL, `explain()` | Kode 8.3-8.5 |
| `udf_zakat.py` | UDF biasa vs Pandas UDF vs fungsi bawaan, dengan pengukuran waktu | Kode 8.6 |
| `scala-harian/` | Job yang sama dalam Scala (`sbt package`) | Kode 8.7 |
| `docker-compose.yml` | Klaster Spark standalone 1 master + 2 worker + RustFS | Kode 8.8 |
| `gold_harian.py` | Job silver ke gold | Kode 8.9-8.10 |

Nomor Kode dapat bergeser sedikit bila isi buku berubah; cocokkan dengan judul listing.

## Menjalankan secara lokal

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt          # butuh Java 17+ untuk PySpark
python gen_data.py --baris 1000000 --keluar data
python mapreduce_sim.py
spark-submit rdd_total_kota.py data/trx.csv
spark-submit harian_dataframe.py data
spark-submit --master "local[4]" udf_zakat.py data
spark-submit gold_harian.py data
```

Scala:

```bash
cd scala-harian && sbt package
spark-submit --class Harian target/scala-2.12/harian_2.12-0.1.jar ../data
```

## Menjalankan di klaster Docker

```bash
cp .env.contoh .env            # lalu ganti nilainya
set -a; . ./.env; set +a       # muat S3_ACCESS_KEY/S3_SECRET_KEY ke shell
docker compose up -d
# unggah folder data/silver ke bucket "lake" di RustFS
# (konsol http://localhost:9001, atau aws --endpoint-url http://localhost:9000 s3 cp --recursive)
docker compose exec spark-master /opt/spark/bin/spark-submit \
  --master spark://spark-master:7077 --total-executor-cores 4 \
  --packages org.apache.hadoop:hadoop-aws:3.3.4 \
  --conf spark.hadoop.fs.s3a.endpoint=http://s3:9000 \
  --conf spark.hadoop.fs.s3a.path.style.access=true \
  --conf spark.hadoop.fs.s3a.access.key=$S3_ACCESS_KEY \
  --conf spark.hadoop.fs.s3a.secret.key=$S3_SECRET_KEY \
  /opt/kerja/gold_harian.py s3a://lake
```

UI master: http://localhost:8080, Spark UI aplikasi: http://localhost:4040.
Eksperimen: matikan satu worker (`docker kill <nama-container-worker>`) saat job berjalan,
lalu amati task yang diulang di tab Stages.

Versi `hadoop-aws` harus cocok dengan versi Hadoop di dalam image Spark.
