# Bab 4 - Lakehouse dan Medallion Architecture

Contoh kode lengkap untuk Bab 4 buku *Data Engineering 101*. Studi kasus: transaksi
sintetis bank syariah digital (semua identitas dibangkitkan acak, bukan data nyata).

Semua contoh Python berjalan **tanpa server**: katalog Iceberg memakai SQLite dan
warehouse berupa folder lokal `./lake` (lihat `katalog.py`). Lab dengan katalog REST
dan object storage S3 tersedia di folder `lab/`.

## Persiapan

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```

## Daftar contoh

| Berkas | Isi | Kaitan di buku |
|---|---|---|
| `data_contoh.py` | Pembangkit data bronze kotor (nominal teks, duplikat) | dipakai semua contoh |
| `katalog.py` | Membuka katalog Iceberg lokal (SQLite) atau REST (`LAKE_CATALOG=rest`) | dipakai semua contoh |
| `folder_parquet_rapuh.py` | Menimpa partisi Parquet berkas demi berkas: pembaca melihat campuran versi | Kode 4.1, 4.2 |
| `iceberg_dasar.py` | Tabel Iceberg pertama, snapshot, time travel, schema evolution, rollback | Kode 4.3, 4.4, 4.10 |
| `intip_metadata.py` | Menelusuri metadata.json -> manifest list -> manifest -> berkas data | Kode 4.5 |
| `occ_commit.py` | Simulasi commit optimistik dengan pemeriksaan konflik per partisi | Kode 4.6, 4.7, Algoritma 4.1 |
| `rust-occ/` | CAS dengan `AtomicU64` di Rust (hanya pustaka standar) | Kode 4.8 |
| `partisi_tersembunyi.py` | Hidden partitioning `days(waktu)` dan partition evolution `bucket(16, ...)` | Kode 4.12 |
| `delta_merge.py` | MERGE koreksi, riwayat, time travel, isi `_delta_log` dengan delta-rs | Kode 4.14 |
| `rawat_tabel.py` | Compaction, expire snapshots, mencari orphan files | Kode 4.16, Algoritma 4.2 |
| `medallion.py` | Pipeline bronze -> silver -> gold yang idempotent (PyIceberg, Polars, DuckDB) | Kode 4.19-4.22 |
| `duckdb_baca.py` | Membaca tabel Iceberg dan Delta dari DuckDB | Kode 4.24 |
| `spark/medallion_spark.py` | PySpark + Iceberg: DDL berpartisi, MERGE, time travel, rollback, partition evolution, rewrite_data_files | Kode 4.9, 4.11, 4.13, 4.17 |
| `spark/rawat_tabel.sql` | Prosedur perawatan tabel di Spark SQL | Kode 4.15 |
| `spark-scala/` | Bronze -> silver dengan Spark (Scala) lalu MERGE | Kode 4.23 |
| `lab/docker-compose.yml` | Server S3 (RustFS) + katalog REST Iceberg | Kode 4.25 |
| `lab/gold_duckdb.sql` | DuckDB membaca gold lewat katalog REST | Kode 4.26 |

Kode 4.18 (satu transaksi di tiga lapis) adalah data ilustrasi dan tidak punya berkas.

## Menjalankan (mode lokal)

```bash
python folder_parquet_rapuh.py
python iceberg_dasar.py && python intip_metadata.py
python occ_commit.py
python partisi_tersembunyi.py
python delta_merge.py
python rawat_tabel.py                       # HAPUS_YATIM=1 untuk benar-benar menghapus
TOKEN_SALT=rahasia-lab python medallion.py 2026-11-02
TOKEN_SALT=rahasia-lab python medallion.py 2026-11-02   # dijalankan ulang: hasil identik
TOKEN_SALT=rahasia-lab python medallion.py 2026-11-03
python duckdb_baca.py

# Rust (toolchain stabil)
cargo run --release --manifest-path rust-occ/Cargo.toml

# Spark (butuh Java 17/21; paket Iceberg diunduh otomatis pada run pertama)
pip install pyspark==4.0.1
python spark/medallion_spark.py
```

Untuk Scala: `cd spark-scala && sbt package`, lalu `spark-submit` dengan konfigurasi
katalog `lake` yang sama seperti `spark/medallion_spark.py` dan variabel `TOKEN_SALT`.

## Lab: katalog REST dan object storage

```bash
cd lab
cp .env.contoh .env            # ganti sandi; berkas .env tidak masuk Git
docker compose up -d           # port bisa diubah lewat S3_PORT dan REST_PORT di .env
cd ..
export LAKE_CATALOG=rest S3_ACCESS_KEY=... S3_SECRET_KEY=...
# bila port diubah: export REST_URI=http://localhost:18181 S3_ENDPOINT=http://localhost:19000
TOKEN_SALT=rahasia-lab python medallion.py 2026-11-02
export AWS_ACCESS_KEY_ID=$S3_ACCESS_KEY AWS_SECRET_ACCESS_KEY=$S3_SECRET_KEY
duckdb -c ".read lab/gold_duckdb.sql"
```

Image `iceberg-rest-fixture` adalah katalog rujukan untuk pengujian (tanpa autentikasi).
Untuk produksi gunakan katalog REST yang dirawat seperti Apache Polaris atau Lakekeeper.

## Catatan versi

Versi yang diuji tercantum di `requirements.txt` (PyIceberg 0.12, Polars 2.0, DuckDB 2.0,
delta-rs 1.6), PySpark 4.0.1 dengan `iceberg-spark-runtime-4.0_2.13:1.10.0`.
Pada PyIceberg versi ini, `expire_snapshots` hanya membuang metadata; berkas lama dihapus
terpisah (lihat `rawat_tabel.py`). API PyIceberg dan DuckDB bergerak cepat; cocokkan dengan
dokumentasi versi Anda.
