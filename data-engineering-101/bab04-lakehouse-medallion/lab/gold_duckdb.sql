-- Kode 4.26: membaca lapis gold lewat katalog REST dari DuckDB.
-- Jalankan setelah docker compose up dan medallion.py dengan LAKE_CATALOG=rest:
--   export AWS_ACCESS_KEY_ID=$S3_ACCESS_KEY AWS_SECRET_ACCESS_KEY=$S3_SECRET_KEY
--   duckdb -c ".read lab/gold_duckdb.sql"
-- Kredensial dibaca dari variabel lingkungan, tidak ditulis di berkas ini.
INSTALL iceberg; LOAD iceberg;
INSTALL httpfs;  LOAD httpfs;

CREATE SECRET lab_s3 (TYPE s3, PROVIDER credential_chain, CHAIN 'env',
  ENDPOINT 'localhost:9000', URL_STYLE 'path', USE_SSL false,
  REGION 'us-east-1');

ATTACH 'lake' AS lake (TYPE iceberg,
  ENDPOINT 'http://localhost:8181', AUTHORIZATION_TYPE 'none');

SELECT cabang, SUM(total) AS total_nov
FROM lake.gold.trx_harian_cabang
WHERE tanggal BETWEEN DATE '2026-11-01' AND DATE '2026-11-30'
GROUP BY cabang
ORDER BY total_nov DESC;
