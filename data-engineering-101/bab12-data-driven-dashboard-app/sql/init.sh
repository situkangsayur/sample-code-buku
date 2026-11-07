#!/bin/sh
# Dijalankan sekali oleh image postgres saat volume data masih kosong.
# Membuat tabel agregat contoh dan akun read-only untuk alat BI.
# Password diambil dari variabel lingkungan BI_READER_PASSWORD (lihat .env).
set -e
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" \
     -v pw="$BI_READER_PASSWORD" <<'EOSQL'
CREATE TABLE IF NOT EXISTS fct_transaksi_harian (
  tanggal date, kode_cabang text, kanal text,
  nominal numeric(20,2), nasabah_aktif bigint, data_per timestamp);
CREATE ROLE bi_reader LOGIN PASSWORD :'pw';
GRANT CONNECT ON DATABASE gold TO bi_reader;
GRANT USAGE ON SCHEMA public TO bi_reader;
GRANT SELECT ON ALL TABLES IN SCHEMA public TO bi_reader;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT ON TABLES TO bi_reader;
EOSQL
