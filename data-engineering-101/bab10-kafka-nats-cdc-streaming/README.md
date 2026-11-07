# Bab 10 - Kafka, NATS, CDC, dan Stream Processing

Contoh kode lengkap untuk Bab 10 buku *Data Engineering 101*: hot path dari PostgreSQL
lewat CDC Debezium ke Redpanda (API Kafka), diolah Spark Structured Streaming, lalu ditulis ke
bronze Iceberg di RustFS (object storage S3) dan ke ClickHouse. NATS JetStream disertakan sebagai pembanding.

| Berkas | Isi | Rujukan di buku |
|---|---|---|
| `producer_transaksi.py` | Producer `acks=all` + idempotence; pesan membawa `id_perangkat` dan `event_time` untuk Flink; mode uji throughput (`--jumlah`, `--acks`, `--partisi`) | Kode 10.1 |
| `consumer-rust/` | Consumer at-least-once dengan commit manual dan pemrosesan idempotent (rdkafka) | Kode 10.2, Algoritma 10.1 |
| `skema/transaksi.avsc` | Skema Avro event transaksi versi 2 | Kode 10.3 |
| `daftar_connector.py` | Mendaftarkan connector Debezium PostgreSQL; opsi `--outbox` untuk outbox event router | Kode 10.5 |
| `nats_jetstream.py` | NATS core vs JetStream: deduplikasi `Nats-Msg-Id` dan durable pull consumer | Kode 10.6 |
| `hot_path.py` | CDC ke bronze Iceberg, lalu aturan fraud (window 1 menit, watermark 2 menit) ke ClickHouse | Kode 10.7-10.8 |
| `init/clickhouse.sql` | Tabel `peringatan_fraud` dengan `ReplacingMergeTree` | Kode 10.9 |
| `scala-fraud/` | Aturan fraud dalam Scala dengan sink Kafka `bank.peringatan` | Kode 10.10 |
| `flink_fraud.sql` | Aturan yang sama dalam Flink SQL (pembanding) | Kode 10.11 |
| `docker-compose.yml` | PostgreSQL, Redpanda, Debezium Connect, ClickHouse, NATS, RustFS | Kode 10.12 |
| `generator.py` | Pola curiga, satu late event yang diterima, satu di bawah watermark; opsi `--akad` (outbox) | Kode 10.13 |
| `init/postgres.sql` | Tabel `transaksi`, `akad`, dan `outbox` | Subbab Praktik |

Nomor Kode dapat bergeser sedikit bila isi buku berubah; cocokkan dengan judul listing.

## Menyiapkan

```bash
docker compose up -d                       # tunggu sampai semua container sehat
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt            # Java 17 untuk PySpark
```

Alamat: Kafka API `localhost:19092`, Kafka Connect `http://localhost:8083`, ClickHouse
`http://localhost:8123`, NATS `localhost:4222` (monitor `http://localhost:8222`), konsol RustFS
`http://localhost:9001` (labadmin/rahasia_lab, atau nilai S3_ACCESS_KEY/S3_SECRET_KEY di `.env`).

## Menjalankan hot path

```bash
python daftar_connector.py                 # CDC tabel transaksi -> bank.public.transaksi
python hot_path.py                         # biarkan berjalan di terminal sendiri
python generator.py                        # di terminal lain: skenario buku
python generator.py --tanpa-skenario --normal 500   # lalu lintas normal

# melihat event CDC dan peringatan
docker compose exec redpanda rpk topic consume bank.public.transaksi -n 3
docker compose exec clickhouse clickhouse-client --password rahasia_lab \
  -q "SELECT * FROM peringatan_fraud FINAL ORDER BY window_start"
```

Tanpa object storage, simpan tabel Iceberg dan checkpoint di disk lokal:
`LAKE_ROOT=file:///tmp/lake python hot_path.py`.

Versi Scala:

```bash
cd scala-fraud && sbt package
spark-submit --class FraudStream \
  --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.1,org.apache.hadoop:hadoop-aws:3.3.4 \
  --conf spark.hadoop.fs.s3a.endpoint=http://localhost:9000 \
  --conf spark.hadoop.fs.s3a.path.style.access=true \
  --conf spark.hadoop.fs.s3a.access.key=labadmin \
  --conf spark.hadoop.fs.s3a.secret.key=rahasia_lab \
  target/scala-2.12/fraud-scala_2.12-0.1.jar localhost:19092 s3a://lake/ckpt
docker compose exec redpanda rpk topic consume bank.peringatan
```

## Producer, consumer, dan NATS

```bash
python producer_transaksi.py                         # satu transaksi T-881 ke bank.transaksi
cd consumer-rust && cargo run --release              # consumer group fraud-rust
python producer_transaksi.py --jumlah 200000 --acks 1 --partisi 6   # uji throughput
python nats_jetstream.py
```

Flink SQL (Kode 10.11) membaca topik `bank.transaksi` yang diisi `producer_transaksi.py`;
isi dulu topiknya, misalnya `python producer_transaksi.py --jumlah 5000`, lalu jalankan
`flink_fraud.sql` di Flink SQL Client dengan konektor Kafka di classpath.

## Outbox pattern

```bash
python daftar_connector.py --outbox
python generator.py --tanpa-skenario --akad
docker compose exec redpanda rpk topic consume pembiayaan.akad -n 1
```

## Skenario uji (Subbab Praktik)

1. Tujuh transaksi dari dua perangkat menghasilkan satu peringatan di ClickHouse.
2. Event terlambat satu menit memperbarui window; event terlambat lima menit masuk bronze tetapi
   diabaikan agregasi (lihat metrik state operator di Spark UI `http://localhost:4040`).
3. Matikan `hot_path.py` di tengah lalu nyalakan lagi: periksa peringatan dan baris bronze ganda.
4. `docker compose stop connect` lima menit sambil menulis, pantau
   `SELECT slot_name, pg_size_pretty(pg_wal_lsn_diff(pg_current_wal_lsn(), restart_lsn)) FROM pg_replication_slots;`
   lalu `docker compose start connect`.
5. Bandingkan throughput `acks` 0, 1, `all` pada 1, 3, dan 6 partisi, lalu dengan JetStream.

## Membersihkan

```bash
python daftar_connector.py --hapus
docker compose down -v
```

Catatan: satu laptop dan satu broker tanpa replikasi tidak mewakili angka produksi. Kata sandi
di sini hanya untuk latihan; di produksi gunakan pengelola rahasia dan kunci versi image.
