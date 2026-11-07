-- Tabel transaksi untuk dashboard real-time di ClickHouse
CREATE TABLE trx (
  waktu       DateTime,
  cabang_id   UInt16,
  rekening_id UInt64,
  jenis       LowCardinality(String),
  nominal     Decimal(18, 2)
) ENGINE = MergeTree
PARTITION BY toYYYYMM(waktu)
ORDER BY (cabang_id, waktu);

-- dasbor: nominal per cabang per jam hari ini
SELECT cabang_id, toStartOfHour(waktu) AS jam, sum(nominal) AS total
FROM trx
WHERE waktu >= today()
GROUP BY cabang_id, jam
ORDER BY cabang_id, jam;

-- Memuat gold dari Parquet di object storage (RustFS lab, endpoint S3 http://s3:9000).
-- INSERT INTO ... SELECT FROM s3() saja TIDAK idempotent: bila task diulang setelah gagal
-- di tengah jalan, baris yang sama masuk dua kali. Pola tabel bayangan + EXCHANGE TABLES
-- (database engine Atomic, bawaan ClickHouse) membuat pemuatan aman diulang.
-- Ganti KEY/SECRET dengan kredensial dari .env, atau pakai named collection.
-- DROP TABLE IF EXISTS gold_harian_cabang_baru;
-- CREATE TABLE gold_harian_cabang_baru AS gold_harian_cabang;
-- INSERT INTO gold_harian_cabang_baru
--   SELECT * FROM s3('http://s3:9000/lake/gold/harian_cabang/*.parquet', 'KEY', 'SECRET', 'Parquet');
-- EXCHANGE TABLES gold_harian_cabang_baru AND gold_harian_cabang;
-- DROP TABLE gold_harian_cabang_baru;
--
-- Varian per partisi (hanya satu tanggal berubah): isi tabel bayangan untuk tanggal itu, lalu
-- ALTER TABLE gold_harian_cabang REPLACE PARTITION <partisi> FROM gold_harian_cabang_baru;
