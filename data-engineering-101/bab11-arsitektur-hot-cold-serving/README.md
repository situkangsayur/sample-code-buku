# Bab 11 - Arsitektur hot dan cold beserta serving layer

Contoh kode untuk Bab 11 buku *Data Engineering 101* (studi kasus bank syariah digital,
semua data sintetis).

| Berkas | Isi | Kode di buku |
|---|---|---|
| `slo_freshness.py` | kepatuhan SLO kesegaran dan sisa error budget | Kode 11.1 |
| `lambda_merge.sql`, `lambda_demo.py` | kueri gabungan batch view + real-time view (Lambda), dijalankan di DuckDB | Kode 11.2 |
| `scala-kappa/` | job Spark Structured Streaming versi kedua yang me-replay topik ke tabel Iceberg berversi | Kode 11.3, Algoritma 11.1 |
| `iceberg_maintenance.sql` | compaction, rewrite manifest, expire snapshot, hapus berkas yatim | Kode 11.4 |
| `clickhouse_hot.sql`, `clickhouse/storage.xml` | Kafka engine, materialized view, SummingMergeTree, TTL ke volume dingin | Kode 11.5 |
| `uji_clickhouse_chdb.py` | uji logika Kode 11.5 tanpa server (chDB) | - |
| `cache_aside.py` | cache-aside dengan jitter dan kunci tunggal, demo stampede, XFetch | Kode 11.6, Algoritma 11.2 |
| `agregat-rust/` | state agregat yang dapat digabung (monoid) | Kode 11.7 |
| `pg_matview.sql` | materialized view PostgreSQL dengan REFRESH CONCURRENTLY | Kode 11.8 |
| `feature_repo/fitur_rekening.py`, `feature_repo/feature_store.yaml` | definisi fitur rekening dengan Feast | Kode 11.9 |
| `buat_data_fitur.py`, `pakai_fitur.py` | data fitur sintetis; fitur offline (point-in-time) dan online | - |
| `rekonsiliasi.py` | rekonsiliasi harian agregat hot vs gold (DuckDB) | Kode 11.10, Algoritma 11.3 |
| `biaya.py` | model biaya kasar per jalur (harga ilustrasi) | - |
| `docker-compose.yml` | Redpanda, ClickHouse, Valkey, object storage S3 (SeaweedFS), katalog Iceberg REST, Spark | Kode 11.11 |
| `generator.py` | generator transaksi sintetis ke topik `bank.transaksi`, termasuk event terlambat | - |

## Menjalankan contoh tanpa server

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python slo_freshness.py
python lambda_demo.py
python rekonsiliasi.py
python biaya.py
python cache_aside.py --fake          # memakai fakeredis
python uji_clickhouse_chdb.py
python buat_data_fitur.py && (cd feature_repo && feast apply) && python pakai_fitur.py
(cd agregat-rust && cargo run)
```

## Laboratorium jalur hot dan cold

```bash
cp .env.example .env               # isi CLICKHOUSE_PASSWORD
docker compose up -d
python generator.py --n 5000 --telat 20
docker compose exec -T clickhouse sh -c 'clickhouse-client --password "$CLICKHOUSE_PASSWORD" --multiquery' < clickhouse_hot.sql
python cache_aside.py                  # memakai Valkey di localhost:6379
```

Job Kappa (`scala-kappa`, `sbt package`) dan perawatan Iceberg dijalankan di kontainer `spark`
dengan katalog `lake` yang menunjuk ke katalog REST dan endpoint S3 lokal, misalnya:

```bash
--conf spark.sql.catalog.lake=org.apache.iceberg.spark.SparkCatalog \
--conf spark.sql.catalog.lake.type=rest \
--conf spark.sql.catalog.lake.uri=http://iceberg-rest:8181 \
--conf spark.sql.catalog.lake.io-impl=org.apache.iceberg.aws.s3.S3FileIO \
--conf spark.sql.catalog.lake.s3.endpoint=http://s3:8333 \
--conf spark.sql.catalog.lake.s3.path-style-access=true
```

Catatan:
- Kata sandi di `docker-compose.yml` hanya untuk latihan. Versi image dikunci; perbarui ke rilis
  stabil terbaru saat mencoba.
- SeaweedFS tanpa konfigurasi identitas menerima akses tanpa kredensial. Cukup untuk laptop,
  jangan dipakai di jaringan bersama.
- Feast di sini memakai SQLite sebagai online store; ganti ke Redis/Valkey lewat
  `feature_store.yaml` (contoh ada di komentar berkas itu).
- Nomor Kode mengikuti urutan di bab; periksa kembali bila bab disunting.
