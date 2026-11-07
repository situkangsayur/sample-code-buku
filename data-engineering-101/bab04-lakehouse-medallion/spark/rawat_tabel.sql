-- Kode 4.15: tiga tugas perawatan rutin tabel Iceberg (Spark SQL).
-- Jadwalkan harian atau mingguan lewat orchestrator (Bab 6).

-- 1. compaction: satukan berkas kecil menjadi berkas sekitar 512 MB
CALL lake.system.rewrite_data_files(
  table   => 'silver.trx',
  options => map('target-file-size-bytes', '536870912'));

-- 1b. satukan manifest kecil agar perencanaan kueri tetap cepat
CALL lake.system.rewrite_manifests('silver.trx');

-- 2. expire snapshots: batas time travel sesuai kebijakan retensi
CALL lake.system.expire_snapshots(
  table       => 'silver.trx',
  older_than  => TIMESTAMP '2026-10-01 00:00:00',
  retain_last => 10);

-- 3. hapus berkas yatim dari job yang gagal (beri jeda aman, mis. 3 hari)
CALL lake.system.remove_orphan_files(
  table      => 'silver.trx',
  older_than => TIMESTAMP '2026-10-20 00:00:00');
