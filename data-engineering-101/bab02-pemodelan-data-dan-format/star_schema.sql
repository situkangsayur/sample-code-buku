-- Star schema transaksi rekening bank syariah (Kode 2.x). Jalankan: duckdb bank.duckdb < star_schema.sql
CREATE OR REPLACE TABLE dim_waktu (
  sk_waktu   INTEGER PRIMARY KEY,      -- format YYYYMMDD
  tanggal    DATE NOT NULL,
  hari       VARCHAR, bulan INTEGER, kuartal INTEGER, tahun INTEGER,
  hari_libur BOOLEAN, ramadan BOOLEAN);
CREATE OR REPLACE TABLE dim_nasabah (
  sk_nasabah     INTEGER PRIMARY KEY,  -- surrogate key
  id_nasabah     VARCHAR NOT NULL,     -- natural key dari sistem sumber
  segmen         VARCHAR, kota VARCHAR,
  berlaku_dari   DATE NOT NULL,
  berlaku_sampai DATE NOT NULL DEFAULT DATE '9999-12-31',
  aktif          BOOLEAN NOT NULL);
CREATE OR REPLACE TABLE dim_produk (
  sk_produk INTEGER PRIMARY KEY, nama_produk VARCHAR, jenis_akad VARCHAR);
CREATE OR REPLACE TABLE dim_cabang (
  sk_cabang INTEGER PRIMARY KEY, kode_cabang VARCHAR, kota VARCHAR, wilayah VARCHAR);
CREATE OR REPLACE TABLE dim_kanal (
  sk_kanal INTEGER PRIMARY KEY, kanal VARCHAR);
CREATE OR REPLACE TABLE fakta_transaksi (
  id_transaksi VARCHAR,                -- degenerate dimension
  sk_waktu INTEGER, sk_nasabah INTEGER, sk_produk INTEGER,
  sk_cabang INTEGER, sk_kanal INTEGER,
  nominal DECIMAL(18,2), biaya DECIMAL(18,2));

-- Isi contoh kecil
INSERT INTO dim_waktu VALUES
  (20260315, DATE '2026-03-15', 'Minggu', 3, 1, 2026, true,  true),
  (20260810, DATE '2026-08-10', 'Senin',  8, 3, 2026, false, false);
INSERT INTO dim_nasabah VALUES
  (101, '7712', 'ritel', 'Bogor',   DATE '2024-01-15', DATE '2026-06-30', false),
  (245, '7712', 'ritel', 'Bandung', DATE '2026-07-01', DATE '9999-12-31', true),
  (102, '8820', 'UMKM',  'Bogor',   DATE '2023-05-02', DATE '9999-12-31', true);
INSERT INTO dim_produk VALUES (1, 'Tabungan Wadiah', 'wadiah'), (2, 'Pembiayaan Kendaraan', 'murabahah');
INSERT INTO dim_cabang VALUES (1, 'BGR01', 'Bogor', 'Jabar'), (2, 'BDG01', 'Bandung', 'Jabar');
INSERT INTO dim_kanal VALUES (1, 'mobile'), (2, 'ATM'), (3, 'QRIS');
INSERT INTO fakta_transaksi VALUES
  ('T-1', 20260315, 101, 1, 1, 1, 250000, 0),
  ('T-2', 20260315, 102, 1, 1, 3, 75000, 0),
  ('T-3', 20260810, 245, 1, 2, 2, 500000, 6500);

-- Total nominal per kota pada saat transaksi terjadi (SCD tipe 2)
SELECT n.kota, SUM(f.nominal) AS total
FROM fakta_transaksi f JOIN dim_nasabah n USING (sk_nasabah)
GROUP BY n.kota ORDER BY total DESC;

-- Total nominal per kota menurut alamat SEKARANG (lewat natural key)
SELECT cur.kota, SUM(f.nominal) AS total
FROM fakta_transaksi f
JOIN dim_nasabah n   ON f.sk_nasabah = n.sk_nasabah
JOIN dim_nasabah cur ON cur.id_nasabah = n.id_nasabah AND cur.aktif
GROUP BY cur.kota ORDER BY total DESC;
