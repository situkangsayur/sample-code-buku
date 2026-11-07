-- Kode 10.9: tabel peringatan fraud yang membuat sink idempotent.
-- Dijalankan otomatis oleh container clickhouse saat pertama kali dibuat.
CREATE TABLE IF NOT EXISTS peringatan_fraud (
  window_start DateTime,
  id_rekening  String,
  n_trx        UInt32,
  total        Int64,
  n_perangkat  UInt32
) ENGINE = ReplacingMergeTree
ORDER BY (id_rekening, window_start);

-- Contoh membaca hasil yang sudah dirapikan (jalankan manual):
-- SELECT * FROM peringatan_fraud FINAL WHERE window_start >= now() - INTERVAL 1 HOUR;
