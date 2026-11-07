-- Memuat gold ke PostgreSQL sebagai serving store, dari DuckDB.
-- Idempotent: tabel lama dibuang dan dibuat ulang dari seluruh gold dalam satu transaksi,
-- sehingga menjalankan ulang memberi hasil yang sama dan pembaca tidak melihat tabel setengah terisi.
INSTALL postgres; LOAD postgres;
ATTACH 'host=localhost dbname=postgres user=postgres password=lab' AS pg (TYPE postgres);
BEGIN;
DROP TABLE IF EXISTS pg.public.gold_harian_cabang;
CREATE TABLE pg.public.gold_harian_cabang AS
  SELECT * FROM read_parquet('data/gold/harian_cabang/*.parquet');
COMMIT;
