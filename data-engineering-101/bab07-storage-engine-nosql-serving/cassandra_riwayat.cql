-- Riwayat transaksi per nasabah: satu partisi per (nasabah, bulan), terurut waktu menurun.
CREATE KEYSPACE IF NOT EXISTS bank
  WITH replication = {'class': 'NetworkTopologyStrategy', 'datacenter1': 1};

CREATE TABLE IF NOT EXISTS bank.trx_per_nasabah (
  nasabah_id  bigint,
  bulan       text,          -- bucket bulan, mis. '2026-11', mencegah partisi raksasa
  waktu_trx   timestamp,
  trx_id      text,
  jenis_akad  text,
  nominal     decimal,
  keterangan  text,
  PRIMARY KEY ((nasabah_id, bulan), waktu_trx, trx_id)
) WITH CLUSTERING ORDER BY (waktu_trx DESC, trx_id ASC);

-- 50 transaksi terakhir nasabah 1001 bulan ini: satu partisi, sudah terurut
SELECT waktu_trx, jenis_akad, nominal FROM bank.trx_per_nasabah
WHERE nasabah_id = 1001 AND bulan = '2026-11' LIMIT 50;
