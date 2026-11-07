-- Jalankan di PostgreSQL 15+ sebagai admin: psql -f rls.sql
CREATE SCHEMA IF NOT EXISTS gold;
CREATE TABLE IF NOT EXISTS gold.transaksi (id bigint, kode_cabang text, nominal numeric);
CREATE TABLE IF NOT EXISTS gold.nasabah (id_nasabah bigint, nik text, segmen text, kota text);
INSERT INTO gold.transaksi VALUES (1,'BGR',100000),(2,'DPK',250000),(3,'BGR',75000);
INSERT INTO gold.nasabah VALUES (1,'3201011234560001','ritel','Bogor');

DO $$ BEGIN CREATE ROLE analis_cabang NOLOGIN; EXCEPTION WHEN duplicate_object THEN NULL; END $$;
GRANT USAGE ON SCHEMA gold TO analis_cabang;
GRANT SELECT ON gold.transaksi TO analis_cabang;

-- Row-level: analis hanya melihat cabangnya sendiri
ALTER TABLE gold.transaksi ENABLE ROW LEVEL SECURITY;
DROP POLICY IF EXISTS cabang_sendiri ON gold.transaksi;
CREATE POLICY cabang_sendiri ON gold.transaksi
  FOR SELECT TO analis_cabang
  USING (kode_cabang = current_setting('app.cabang'));

-- Column-level: kolom NIK tidak dapat dipilih
REVOKE SELECT ON gold.nasabah FROM analis_cabang;
GRANT SELECT (id_nasabah, segmen, kota) ON gold.nasabah TO analis_cabang;

-- Uji sebagai analis Bogor
SET ROLE analis_cabang;
SET app.cabang = 'BGR';
SELECT DISTINCT kode_cabang FROM gold.transaksi;     -- hanya BGR
SELECT id_nasabah, segmen FROM gold.nasabah;         -- boleh
\set ON_ERROR_STOP off
SELECT nik FROM gold.nasabah;                        -- ERROR: permission denied
RESET ROLE;
