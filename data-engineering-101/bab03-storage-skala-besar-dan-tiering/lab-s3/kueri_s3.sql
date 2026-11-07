-- Kueri langsung ke object storage dengan DuckDB (Kode 3.x). Jalankan: duckdb < kueri_s3.sql
-- Ganti KEY_ID dan SECRET sesuai .env; jangan menulis kredensial produksi di berkas.
INSTALL httpfs; LOAD httpfs;
CREATE OR REPLACE SECRET lab_s3 (
  TYPE s3, KEY_ID 'admin', SECRET 'ganti-dengan-rahasia-panjang',
  ENDPOINT 'localhost:9000', URL_STYLE 'path', USE_SSL false);

-- Partition pruning: hanya awalan tanggal=2026-01-19 yang dibuka
SELECT tanggal, kanal, SUM(nominal) AS total
FROM read_parquet('s3://bank-lake/bronze/transaksi/*/*.parquet', hive_partitioning = true)
WHERE tanggal = '2026-01-19'
GROUP BY ALL ORDER BY total DESC;

-- Bandingkan dengan seluruh bulan
SELECT COUNT(*), SUM(nominal)
FROM read_parquet('s3://bank-lake/bronze/transaksi/*/*.parquet', hive_partitioning = true);
